# Generated by Django 3.1 on 2021-05-10 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0003_auto_20210509_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='deletion_mark',
            field=models.BooleanField(default=False, verbose_name='Пометка удаления'),
        ),
    ]
