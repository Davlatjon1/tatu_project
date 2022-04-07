# Generated by Django 3.1 on 2022-01-04 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0012_review_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': '', 'verbose_name_plural': 'Список продуктов'},
        ),
        migrations.AddField(
            model_name='category',
            name='show_bot',
            field=models.BooleanField(default=True, verbose_name='Показывать в боте'),
        ),
        migrations.AddField(
            model_name='category',
            name='uuid_1c',
            field=models.CharField(blank=True, editable=False, max_length=255, null=True, unique=True, verbose_name='UUID (1C)'),
        ),
    ]
