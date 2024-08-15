# Generated by Django 5.1 on 2024-08-14 23:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_distribuidor_hh_proyectosaagrupar_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distribuidor_hh',
            name='horas_empleado',
        ),
        migrations.RemoveField(
            model_name='distribuidor_hh',
            name='id_proyecto',
        ),
        migrations.AlterField(
            model_name='hh_estimado_detalle_semanal',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 14, 19, 21, 46, 330735), verbose_name='Fecha'),
        ),
    ]
