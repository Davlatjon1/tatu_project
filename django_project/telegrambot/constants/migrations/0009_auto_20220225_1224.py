# Generated by Django 3.1 on 2022-02-25 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0008_auto_20220221_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='constants',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='constants',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='constants.currency', verbose_name='Основная валюта'),
        ),
    ]
