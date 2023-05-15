# Generated by Django 4.1.7 on 2023-05-14 23:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0043_remove_pedidosoutros_assunto_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedidosala',
            old_name='desc',
            new_name='descri',
        ),
        migrations.RemoveField(
            model_name='pedidosala',
            name='assunto',
        ),
        migrations.RemoveField(
            model_name='pedidosala',
            name='dia',
        ),
        migrations.RemoveField(
            model_name='pedidosala',
            name='tipo',
        ),
        migrations.AddField(
            model_name='pedidosala',
            name='pedido',
            field=models.ForeignKey(default=158, on_delete=django.db.models.deletion.CASCADE, to='main.pedido'),
        ),
        migrations.AddField(
            model_name='pedidosala',
            name='status',
            field=models.CharField(default='Em Análise', max_length=255),
        ),
        migrations.AddField(
            model_name='pedidosala',
            name='uc',
            field=models.CharField(default='LES', max_length=255),
        ),
    ]
