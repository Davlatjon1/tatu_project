# Generated by Django 3.1 on 2022-02-21 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0017_order_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='employment',
        ),
        migrations.RemoveField(
            model_name='item',
            name='factory',
        ),
        migrations.RemoveField(
            model_name='item',
            name='model',
        ),
        migrations.RemoveField(
            model_name='item',
            name='size',
        ),
    ]
