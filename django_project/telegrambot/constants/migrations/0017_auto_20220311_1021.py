# Generated by Django 3.1 on 2022-03-11 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0016_auto_20220311_1006'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='settingsapi',
            name='check_before_order',
        ),
        migrations.RemoveField(
            model_name='settingsapi',
            name='type_of_act_sverki',
        ),
        migrations.AddField(
            model_name='constants',
            name='check_before_order',
            field=models.BooleanField(default=False, verbose_name='Проверить перед заказа'),
        ),
        migrations.AddField(
            model_name='constants',
            name='type_of_act_sverki',
            field=models.CharField(blank=True, choices=[('text', 'Текст'), ('file_pdf', 'Файл (pdf)')], default='file_pdf', max_length=255, verbose_name='Тип акта сверки'),
        ),
        migrations.AlterField(
            model_name='channel',
            name='constant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='constants.constants', verbose_name='Константа'),
        ),
    ]
