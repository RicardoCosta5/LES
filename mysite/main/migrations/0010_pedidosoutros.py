# Generated by Django 4.1.7 on 2023-03-25 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_delete_pedidosoutros'),
    ]

    operations = [
        migrations.CreateModel(
            name='PedidosOutros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assunto', models.CharField(max_length=255)),
                ('descricao', models.CharField(max_length=1200)),
                ('dia', models.DateField()),
            ],
        ),
    ]
