# Generated by Django 4.1.8 on 2024-08-23 23:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_alter_hh_estimado_detalle_semanal_fecha'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historialcambios',
            old_name='subcategoría',
            new_name='subcategoria',
        ),
        migrations.AlterField(
            model_name='hh_estimado_detalle_semanal',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 23, 19, 15, 35, 161480), verbose_name='Fecha'),
        ),
    ]
