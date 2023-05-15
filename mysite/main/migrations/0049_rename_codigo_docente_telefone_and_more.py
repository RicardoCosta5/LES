# Generated by Django 4.1.7 on 2023-05-15 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0048_remove_pedido_note'),
    ]

    operations = [
        migrations.RenameField(
            model_name='docente',
            old_name='codigo',
            new_name='telefone',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='arquivo',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='data_emissao_identificacao',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='data_nascimento',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='data_validade_identificacao',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='digito_verificacao',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='docente',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='identificacao',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='individuo',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='nacionalidade',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='nbsp',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='nif',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='pais_fiscal',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='sexo',
        ),
        migrations.RemoveField(
            model_name='docente',
            name='tipo_identificacao',
        ),
        migrations.RemoveField(
            model_name='funcionario',
            name='nome',
        ),
        migrations.AddField(
            model_name='docente',
            name='departamento',
            field=models.CharField(default='defaults', max_length=255),
        ),
        migrations.AddField(
            model_name='docente',
            name='email',
            field=models.CharField(default='gnomo', max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name='docente',
            name='faculdade',
            field=models.CharField(default='defaults', max_length=255),
        ),
        migrations.AddField(
            model_name='docente',
            name='first_name',
            field=models.CharField(default='gnomo', max_length=255),
        ),
        migrations.AddField(
            model_name='docente',
            name='gabinete',
            field=models.CharField(default='defaults', max_length=255),
        ),
        migrations.AddField(
            model_name='docente',
            name='last_name',
            field=models.CharField(default='gnomo', max_length=255),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='first_name',
            field=models.CharField(default='gnomo', max_length=255),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='last_name',
            field=models.CharField(default='gnomo', max_length=255),
        ),
        migrations.AlterField(
            model_name='docente',
            name='ativo',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='funcionario',
            name='email',
            field=models.CharField(default='gnomo', max_length=255),
        ),
        migrations.AlterField(
            model_name='pedidouc',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pedido'),
        ),
    ]
