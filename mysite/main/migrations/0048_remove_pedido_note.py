# Generated by Django 4.1.7 on 2023-05-15 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_pedido_note_alter_pedidosala_pedido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='note',
        ),
    ]