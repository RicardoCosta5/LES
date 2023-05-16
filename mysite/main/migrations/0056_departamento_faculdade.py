# Generated by Django 4.1.7 on 2023-05-15 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0055_administrador'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='Departamento de Engenharia informática', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Faculdade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(default='FCT - Faculdade de Ciencias e Tecnologia', max_length=255)),
            ],
        ),
    ]