# Generated by Django 4.1.7 on 2023-05-16 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0054_pedidosala_dia_alter_funcionario_ativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidosala',
            name='tarefa',
            field=models.CharField(default='Criar', max_length=255),
        ),
    ]
