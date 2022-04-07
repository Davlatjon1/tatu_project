# Generated by Django 3.1 on 2022-03-07 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0011_settingsapi_type_of_act_sverki'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingsapi',
            name='check_before_order',
            field=models.BooleanField(default=False, verbose_name='Проверить перед заказа'),
        ),
        migrations.AddField(
            model_name='settingsapi',
            name='url_to_check_before_order',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='URL Проверка перед заказа (API)'),
        ),
        migrations.AddField(
            model_name='settingsapi',
            name='url_to_update_order',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='URL Обновление/создание заказ (API)'),
        ),
    ]