# Generated by Django 5.0.7 on 2024-08-01 01:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_hh_estimado_detalle_semanal_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hh_estimado_detalle_semanal',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 31, 21, 43, 21, 518173), verbose_name='Fecha'),
        ),
    ]