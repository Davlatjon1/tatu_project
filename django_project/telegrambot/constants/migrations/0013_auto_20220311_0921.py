# Generated by Django 3.1 on 2022-03-11 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0012_auto_20220307_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='constant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='constants.constants', verbose_name='Константа'),
        ),
    ]
