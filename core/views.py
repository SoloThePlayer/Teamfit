from django.shortcuts import redirect, render
from .models import Ventas, Perfil_hh_Detalle_Semanal, Disponibilidad, Hh_Estimado_Detalle_Semanal, Graficos, historialCambios, proyectosAAgrupar
from .forms import VentasForm, DispForm, UploadFileForm, LoginForm, CrearUsuarioAdmin, proyectosForm
from datetime import datetime, timedelta, time
import random
import requests
import json
from openpyxl import load_workbook
import csv
from django.contrib import messages
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
import pytz

# Create your views here.

def subirProyectos(request, upload='Sh'):
    data = {'form':UploadFileForm()}
    showTable = False
    
    if(upload=="Can"):
        request.session.pop('df_proyectos')
        return redirect (subirProyectos)
    if(upload=="Up"):
        df = cambiarFormatoAlmacenarDb(request.session['df_proyectos'])
        for _, row in df.iterrows():
            proyecto = proyectosAAgrupar(
                id=row['id'],
                proyecto=row['proyecto'],
                lineaNegocio=row['lineaNegocio'],
                tipo=row['tipo'],
                cliente=row['cliente'],
                pm=row['pm'],
                createDate=row['createDate'],
                cierre=row['cierre'],
                primeraTarea=row['primeraTarea'],
                ultimaTarea=row['ultimaTarea'],
                egresosNoHHCLP=row['egresosNoHHCLP'],
                montoOfertaCLP=row['montoOfertaCLP'],
                usoAgencia=row['usoAgencia'],
                desfaseDias=row['desfaseDias'],
                ocupacionInicio=row['ocupacionInicio']
            )
            proyecto.save()
        request.session.pop('df_proyectos')
        return redirect(ver_proyectos)
    
    if request.method == 'POST' and 'file' in request.FILES:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if not file.name.endswith(('.csv', '.xlsx')):
                data['mesg'] = 'Archivo no compatible. Por favor, selecciona un archivo CSV o XLSX.'
            else:
                df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
                required_columns = ['id', 'Proyecto', 'Línea de Negocio', 'tipo', 'cliente', 'pm', 'create_date', 
                                    'Cierre', 'Primer Timesheet', 'Último Timesheet', 'Egresos No HH CLP', 'Monto Oferta CLP',
                                    'C/Agencia', 'Desfase Inicio (días)', 'Ocupación Al Iniciar (%)']
                if not all(col in df.columns for col in required_columns):
                    data['mesg'] = 'El archivo no contiene las columnas requeridas (idTipoProyecto, fecha). Por favor, sube un archivo con estas columnas.'
                else:
                    df = cambiarFormatoAlmacenarDf(df)
                    datosDfDict = df.to_dict(orient='records')
                    data["proyectos"] = datosDfDict
                    request.session['df_proyectos'] = datosDfDict
                    showTable = True
        else:
            data["mesg"] = "El valor es inválido"
    data["showTable"] = showTable
        
    return render(request, "core/subirProyectos.html", data)

def cambiarFormatoAlmacenarDf(df):
    df = df
    df['create_date'] = df['create_date'].astype(str)
    df['Cierre'] = df['Cierre'].astype(str)
    df['Primer Timesheet'] = df['Primer Timesheet'].astype(str)
    df['Último Timesheet'] = df['Último Timesheet'].astype(str)
    df.rename(columns={'Proyecto': 'proyecto'}, inplace=True)
    df.rename(columns={'Línea de Negocio': 'lineaNegocio'}, inplace=True)
    df.rename(columns={'create_date': 'createDate'}, inplace=True)
    df.rename(columns={'Cierre': 'cierre'}, inplace=True)
    df.rename(columns={'Primer Timesheet': 'primeraTarea'}, inplace=True)
    df.rename(columns={'Último Timesheet': 'ultimaTarea'}, inplace=True)
    df.rename(columns={'Egresos No HH CLP': 'egresosNoHHCLP'}, inplace=True)
    df.rename(columns={'Monto Oferta CLP': 'montoOfertaCLP'}, inplace=True)    
    df.rename(columns={'C/Agencia': 'usoAgencia'}, inplace=True)
    df.rename(columns={'Desfase Inicio (días)': 'desfaseDias'}, inplace=True)
    df.rename(columns={'Ocupación Al Iniciar (%)': 'ocupacionInicio'}, inplace=True)
    df['ocupacionInicio'] = df['ocupacionInicio'].round(2)
    df['ocupacionInicio'] = df['ocupacionInicio'] * 100
    
    return df

def cambiarFormatoAlmacenarDb(df):
    df = pd.DataFrame(df)
    df['createDate'] = pd.to_datetime(df['createDate'])
    df['cierre'] = pd.to_datetime(df['cierre'])
    df['primeraTarea'] = pd.to_datetime(df['primeraTarea'])
    df['ultimaTarea'] = pd.to_datetime(df['ultimaTarea'])
    df['cliente'] = df['cliente'].fillna(0)
    df['cliente'] = df['cliente'].astype(int)
    df['usoAgencia'] = df['usoAgencia'].fillna(0)
    df['usoAgencia'] = df['usoAgencia'].replace({'Sí': 1, 'no': 0}).astype(bool)
    df['montoOfertaCLP'] = df['montoOfertaCLP'].fillna(0)
    df['montoOfertaCLP'] = df['montoOfertaCLP'].astype(int)
    df['desfaseDias'] = df['desfaseDias'].fillna(0)
    df['desfaseDias'] = df['desfaseDias'].astype(int) 
    df['ocupacionInicio'] = df['ocupacionInicio'].astype(float) 
    return df

def graficar_Datos(request):
    graficos = Graficos.objects.all()
    data_list = list(graficos.values())
    additional_data = pd.DataFrame(data_list)
    
    bar_chart = go.Figure(data=[
        go.Bar(name='HH requerido', x=additional_data['semana'], y=additional_data['hhRequerido']),
        go.Bar(name='HH disponible', x=additional_data['semana'], y=additional_data['hhDisponible'])
    ])
    bar_chart = bar_chart.to_html(full_html=False)
    
    line_chart = px.line(additional_data, x='semana', y='utilizacion', title='Utilización (%)')
    line_chart = line_chart.to_html(full_html=False)
    
    data = {'bar':bar_chart, 'line':line_chart}
    
    sobreU = False
    subU = False
    for val in graficos:
        if(val.utilizacion > 100):
            sobreU = True
        elif(val.utilizacion < 80):
            subU = True
    if(sobreU and subU):
        data['mesg'] = 'Se estima subtilización bajo un 80% y sobreutilización mayor a 100%, por lo que se sugiere ajustar la disponibilidad de equipo de proyecto o modificar requerimientos de horas futuras.'
    elif (sobreU):
        data['mesg'] = 'Se estima sobreutilización sobre un 100%,  por lo que se sugiere ajustar la disponibilidad de equipo de proyecto o modificar requerimientos de horas futuras'
    elif (subU):
        data['mesg'] = 'Se estima subtilización bajo un 80%. por lo que se sugiere ajustar la disponibilidad de equipo de proyecto o modificar requerimientos de horas futuras'
    else:
        data['mesg'] = 'No se visualizaron momentos en que haya sobreutilización ni subtulización.'
    
    return render(request, 'core/dashboard.html', data)
    

def development_Buttons(request):
    forms = [VentasForm() for _ in range(5)]
    data = {"VentasForms":forms, "DispForm":DispForm}
    
    #Escribe Tu Código Acá
    #se carga el formulario
    data = {}
    data['form'] = UploadFileForm()  # Inicializa el formulario en GET
    data["datosDB"] = Ventas.objects.all()
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if not file.name.endswith(('.csv', '.xlsx')):
                # Mostrar un mensaje de error
                return render(request, 'boton.html', {'form': form, 'error_message': 'Archivo no compatible. Por favor, selecciona un archivo CSV o XLSX.'})

            df = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)
            required_columns = ['idTipoProyecto', 'fecha']
            if not all(col in df.columns for col in required_columns):
                return render(request, 'core/boton.html', {'form': form, 'error_message': 'El archivo no contiene las columnas requeridas (idTipoProyecto, fecha). Por favor, sube un archivo con estas columnas.'})
            
           # Convertir el DataFrame a una lista de diccionarios
            datos_formularios = df.to_dict(orient='records')
            
            # Crear formularios VentasForm con datos iniciales
            forms = []
            for datos in datos_formularios:
                fecha=str(datos['fecha'])
                fecha = fecha[:10]
                
                initial_data = {
                    'idTipoProyecto': datos['idTipoProyecto'],
                    'fecha': fecha
                }
                form = VentasForm(initial=initial_data)
                forms.append(form)
            data['VentasForms'] = forms
            return render(request, 'core/boton.html', data)
            
            # forms = [VentasForm(initial=datos) for datos in datos_formularios]
            # data['VentasForms'] = forms
            # return render(request, 'core/boton.html', {'VentasForms': forms})
            
            # Aquí puedes procesar el archivo según tus necesidades
            # Por ejemplo, guardarlo en la base de datos o procesarlo de alguna manera
            # return HttpResponse('Archivo subido correctamente.') 
        else:
            data["mesg"] = "El formulario en inválido"
            return render(request, 'core/boton.html', data)
    else:
        form = UploadFileForm()
        data["form"] = form
    return render(request, 'core/boton.html', data)

def llenar_DB(request):
    Hh_Estimado_Detalle_Semanal.objects.all().delete()
    Perfil_hh_Detalle_Semanal.objects.all().delete()
    historialCambios.objects.all().delete()
    proyectosAAgrupar.objects.all().delete()
    User.objects.all().delete()

    
    proyecto1 = proyectosAAgrupar.objects.update_or_create(
            id = 446,
            proyecto = 'PRY2023-106',
            lineaNegocio = 'SGE',
            tipo = 'Reportabilidad y Plataforma',
            cliente = 6057,
            pm = 'katherina@rodaenergia.cl', 
            createDate = datetime.strptime('2023-05-10 21:20:14', "%Y-%m-%d %H:%M:%S"),
            cierre = datetime.strptime('2023-05-10', "%Y-%m-%d").date(),
            primeraTarea = datetime.strptime('2023-05-04', "%Y-%m-%d").date(),
            ultimaTarea = datetime.strptime('2023-05-10', "%Y-%m-%d").date(),
            egresosNoHHCLP = 0,
            montoOfertaCLP = 1530218,
            usoAgencia = False,
            desfaseDias = 0,
            ocupacionInicio = 69.0
    )
    
    #Usuario de testing
    usuario = User.objects.create_user(username="admin", password='Admin@123')
    usuario.first_name = "Pedro"
    usuario.last_name = "Martinez"
    usuario.email = "admin@admin.com"
    usuario.is_superuser = True
    usuario.is_staff = True
    usuario.save()
    
    #Crear un usuario inactivo y modificar el login para no dejarlo loguearse
    usuarioAnon = User.objects.create_user(username="Anon", password='anon') #ZKfg!)nkLSp163SD
    usuarioAnon.first_name = "Anonimo"
    usuarioAnon.last_name = "anon"
    usuarioAnon.email = "none"
    usuarioAnon.is_superuser = False
    usuarioAnon.is_staff = False
    usuarioAnon.is_active = False
    usuarioAnon.save()
    
    Perfil_hh_Detalle_Semanal.objects.update_or_create(
        idTipoProyecto = '1', 
        numSemana = '1', 
        hh = 1.8
        )
    Perfil_hh_Detalle_Semanal.objects.update_or_create(
        idTipoProyecto = '1', 
        numSemana = '2', 
        hh = 2.1
        )
    Perfil_hh_Detalle_Semanal.objects.update_or_create(
        idTipoProyecto = '1', 
        numSemana = '3', 
        hh = 1.9
        )
    Perfil_hh_Detalle_Semanal.objects.update_or_create(
        idTipoProyecto = '1', 
        numSemana = '4', 
        hh = 1.5
        )
    Perfil_hh_Detalle_Semanal.objects.update_or_create(
        idTipoProyecto = '2', 
        numSemana = '1', 
        hh = 1.5
        )
    Perfil_hh_Detalle_Semanal.objects.update_or_create(
        idTipoProyecto = '2', 
        numSemana = '2', 
        hh = 3
        )
    return redirect(pagina_principal)

#Casi Funcional
def newCreateJoinDB():
    # Obtener todas las ventas
    ventas = Ventas.objects.all()

    for venta in ventas:
        # Buscar el correspondiente Perfil_hh_Detalle_Semanal por idTipoProyecto
        perfiles_hh = Perfil_hh_Detalle_Semanal.objects.filter(idTipoProyecto=venta.idTipoProyecto)
        fechaInicial = venta.fecha
        semanaInicial = fechaInicial.isocalendar()[1]
        print(str(venta.id) + ": \n")
        if perfiles_hh:
            for i, perfil in enumerate(perfiles_hh):
                fecha = venta.fecha + timedelta(days=(i*7))
                semanaPredecir = fecha.isocalendar()[1]
                semanaProyecto = (semanaPredecir - semanaInicial) + 1
                perfil_HH = Perfil_hh_Detalle_Semanal.objects.filter(idTipoProyecto=venta.idTipoProyecto, numSemana=semanaProyecto)
                horasHombre = perfil_HH[0].hh
                anio = fecha.year
                
                # print("Fecha: " + str(fecha) + " - ID perfilHH: " + str(perfil_HH[0].id) + " - Ventas: " + str(venta.id) + 
                #       " - Año: " + str(anio) + " - Semana del Año: " +  str(semanaPredecir) + " - Horas: " + str(horasHombre) +
                #       "  - Semana Proyecto: " + str(semanaProyecto))
                
                hhDetalleSemana = Hh_Estimado_Detalle_Semanal(fecha=fecha, anio=anio, semana=semanaPredecir, idVentas=venta, 
                                                             idPerfilHhDetalleSemanal=perfil_HH[0], hh=horasHombre)
                checkData = Hh_Estimado_Detalle_Semanal.objects.filter(semana=semanaPredecir, idVentas=venta, anio=anio)
                checkData = list(checkData.values())
                checkData = len(checkData)
                    
                if(checkData == 0):
                    print("Datos Guardados")
                    hhDetalleSemana.save()
                else:
                    print("Datos NO guardados")
                    continue
    return True

def create_additional_table():
    Graficos.objects.all().delete()
    data = Hh_Estimado_Detalle_Semanal.objects.all()
    data_list = list(data.values())
    df = pd.DataFrame(data_list)
    
    disp = Disponibilidad.objects.all()
    dispList = list(disp.values())
    dfDisp = pd.DataFrame(dispList)
    dfDisp.rename(columns={'hh': 'hh_disp'}, inplace=True)
    
    weekly_data = df.groupby('semana')['hh'].sum().reset_index()
    weekly_data.rename(columns={'hh': 'hh_req'}, inplace=True)
    weekly_data = pd.merge(dfDisp, weekly_data, on='semana', how='outer')
    weekly_data['utilizacion'] = round((weekly_data['hh_req'] / weekly_data['hh_disp']) * 100, 1)
    weekly_data = weekly_data.dropna()
    
    for idx, row in weekly_data.iterrows():
        grafico = Graficos(
            semana=row['semana'],
            hhDisponible=row['hh_disp'],
            hhRequerido=row['hh_req'],
            utilizacion=row['utilizacion']
        )
        grafico.save()
    
    return True

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                nombre = user.first_name
                apellido = user.last_name
                desc = f"El usuario {nombre} {apellido} ha iniciado sesión"
                almacenado = almacenarHistorial(desc, "2", user)
                print(almacenado)
                return redirect(pagina_principal)
            else:
                data = {'mesg':'Usuario o contraseña incorrectos', 'form':LoginForm}
                #form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
         data = {'form': LoginForm}
    return render(request, 'core/login.html', data)

#Crear un cerrar sesión
def cerrar_sesion(request):
    nombre = request.user.first_name
    apellido = request.user.last_name
    user = request.user
    desc = f"El usuario {nombre} {apellido} ha cerrado sesión"
    almacenado = almacenarHistorial(desc, "2", user)
    logout(request)
    return redirect(iniciar_sesion) 

def crear_usuarios(request):
    data = {'form':CrearUsuarioAdmin}
    return render(request, 'core/crearUsuarios.html', data)

def pagina_principal(request):
    if not request.user.is_authenticated:
        return redirect(iniciar_sesion)
    
    data = {}
    return render(request, 'core/index1.html', data)

#Almacena el historial solicitando desc, tipoInfo y usuario
def almacenarHistorial(desc, tipoInfo, usuario):
    histCambios = historialCambios()   

    fecha = timezone.now()
    print(fecha)
    histCambios.fecha = fecha
    
    print(histCambios.fecha)
        
    if(len(desc) > 300):
        desc = desc[:300]
        print("Demasiados caracteres en la descripción")
    histCambios.desc = desc
        
    tiposInformaciones = {"1":"Modificación en la DB", "2": "Informativo", "3":"Error", "4":"Otro"}
    if(tipoInfo not in tiposInformaciones):
        tipoInfo = "4"
    histCambios.tipoInfo = tiposInformaciones[tipoInfo]
    
    if(usuario is None):
        print("El usuario es inexistente")
        usuario = User.objects.get(username="Anon")
        histCambios.usuario = usuario
        
    histCambios.usuario = usuario
    histCambios.save()
    return histCambios
    
def ver_proyectos(request):
    #data = {}
    #return render(request, 'core/verProyectos.html', data)
    proyectos = proyectosAAgrupar.objects.all()
    return render(request, 'core/verProyectos.html', {'proyectos': proyectos})
