# Generated by Django 4.1.8 on 2024-08-23 23:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_historialcambios_prioridad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hh_estimado_detalle_semanal',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 23, 19, 15, 26, 870789), verbose_name='Fecha'),
        ),
    ]
