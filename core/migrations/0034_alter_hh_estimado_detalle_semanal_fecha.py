# Generated by Django 4.1.8 on 2024-08-23 21:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_alter_hh_estimado_detalle_semanal_fecha_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hh_estimado_detalle_semanal',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 23, 17, 10, 2, 648672), verbose_name='Fecha'),
        ),
    ]