# Generated by Django 4.1.7 on 2023-05-21 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_delete_turma_remove_dsd_agrupamento_remove_dsd_nome_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DSD',
            new_name='Turma',
        ),
    ]