# Generated by Django 3.1 on 2021-11-04 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0005_auto_20211104_1422'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='clients',
        ),
    ]