# Generated by Django 4.1.8 on 2024-09-06 01:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_alter_hh_estimado_detalle_semanal_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hh_estimado_detalle_semanal',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 5, 21, 29, 45, 625285), verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='historialcambios',
            name='fecha',
            field=models.DateTimeField(verbose_name='Fecha Acción'),
        ),
        migrations.AlterField(
            model_name='historialcambios',
            name='prioridad',
            field=models.IntegerField(default=0, verbose_name='Prioridad'),
        ),
    ]
