# Generated by Django 4.1.8 on 2024-10-10 23:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_remove_proyectosaagrupar_disponibilidad_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('rol', models.CharField(max_length=100)),
                ('horas_totales', models.IntegerField()),
                ('id_recurso', models.IntegerField()),
                ('id_empleado', models.IntegerField()),
            ],
            options={
                'db_table': 'RECURSO',
            },
        ),
        migrations.RemoveField(
            model_name='asignacion',
            name='recurso',
        ),
        migrations.AlterField(
            model_name='asignacion',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.proyectosaagrupar'),
        ),
        migrations.AlterField(
            model_name='hh_estimado_detalle_semanal',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 10, 20, 9, 53, 321183), verbose_name='Fecha'),
        ),
        migrations.AlterModelTable(
            name='asignacion',
            table='ASIGNACION',
        ),
        migrations.AddField(
            model_name='asignacion',
            name='empleado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.empleado'),
            preserve_default=False,
        ),
    ]
