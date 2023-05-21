# Generated by Django 4.1.7 on 2023-05-21 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_anoletivo_ativo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dsd',
            name='Agrupamento',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='DataFim',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='Datainicial',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='Nome',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='Periodo',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='codCurso',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='codDocente',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='curso',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='departDocente',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='departamento',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='disciplina',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='docente',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='factor',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='funcDocente',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='horasPeri',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='horasSem',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='horasServ',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='instDocente',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='instituic',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='instituto',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
        migrations.AlterField(
            model_name='dsd',
            name='turma',
            field=models.CharField(default='2022/2023', max_length=255),
        ),
    ]