# Generated by Django 4.1.7 on 2023-05-15 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_rename_codigo_docente_telefone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docente',
            name='email',
            field=models.CharField(default='gnomo', max_length=255),
        ),
    ]