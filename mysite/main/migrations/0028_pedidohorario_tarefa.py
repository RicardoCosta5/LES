# Generated by Django 4.1.7 on 2023-04-27 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_remove_pedidohorario_status_pedido_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidohorario',
            name='tarefa',
            field=models.CharField(default='Criar', max_length=255),
        ),
    ]
