# Generated by Django 4.1.8 on 2024-08-07 19:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0021_alter_hh_estimado_detalle_semanal_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hh_estimado_detalle_semanal',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 7, 15, 13, 53, 260157), verbose_name='Fecha'),
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NUMRUT', models.IntegerField(verbose_name='Numero RUT')),
                ('DVRUN', models.CharField(max_length=1, verbose_name='Digito Verificador')),
                ('fechaNacimiento', models.DateField(verbose_name='Fecha de Nacimiento')),
                ('cargo', models.CharField(max_length=150, verbose_name='Cargo Empleado')),
                ('telefono', models.CharField(max_length=12, verbose_name='Número de contacto')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='historialCambios',
            fields=[
                ('idHist', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Historial')),
                ('fecha', models.DateTimeField(verbose_name='Fecha Accion')),
                ('desc', models.CharField(max_length=300, verbose_name='Descripción')),
                ('tipoInfo', models.CharField(max_length=50, verbose_name='Tipo de información')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
