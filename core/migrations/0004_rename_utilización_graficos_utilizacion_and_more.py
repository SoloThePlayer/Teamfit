# Generated by Django 4.1.8 on 2024-07-14 21:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_hh_estimado_detalle_semanal_anio_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='graficos',
            old_name='utilización',
            new_name='utilizacion',
        ),
        migrations.AlterField(
            model_name='hh_estimado_detalle_semanal',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 14, 17, 38, 44, 370567), verbose_name='Fecha'),
        ),
    ]
