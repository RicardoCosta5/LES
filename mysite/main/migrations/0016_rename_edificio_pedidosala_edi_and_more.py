# Generated by Django 4.1.7 on 2023-03-28 00:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_rename_edificio_pedidosala_edificio_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedidosala',
            old_name='edificio',
            new_name='edi',
        ),
        migrations.RenameField(
            model_name='pedidosala',
            old_name='sala',
            new_name='sal',
        ),
    ]
