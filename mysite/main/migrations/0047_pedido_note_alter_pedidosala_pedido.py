# Generated by Django 4.1.7 on 2023-05-15 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_merge_20230515_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='note',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='pedidosala',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pedido'),
        ),
    ]
