# Generated by Django 3.1 on 2021-05-09 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contractors', '0002_auto_20210509_2223'),
    ]

    operations = [
        migrations.RenameField(
            model_name='branch',
            old_name='id_1c',
            new_name='uuid_1c',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='id_1c',
            new_name='uuid_1c',
        ),
    ]
