# Generated by Django 4.1.8 on 2024-10-21 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0064_delete_hh_estimado_detalle_semanal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='tipo_proyecto',
        ),
        migrations.DeleteModel(
            name='Disponibilidad',
        ),
        migrations.DeleteModel(
            name='Proyecto',
        ),
        migrations.DeleteModel(
            name='Recurso',
        ),
        migrations.DeleteModel(
            name='TipoProyecto',
        ),
    ]
