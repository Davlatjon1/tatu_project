# Generated by Django 3.1 on 2022-02-25 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0009_auto_20220225_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constants',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование'),
        ),
    ]