# Generated by Django 4.1.8 on 2024-08-09 00:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_proyectosaagrupar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hh_estimado_detalle_semanal',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 8, 20, 33, 17, 616823), verbose_name='Fecha'),
        ),
    ]
