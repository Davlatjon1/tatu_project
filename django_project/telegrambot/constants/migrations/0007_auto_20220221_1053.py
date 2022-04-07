# Generated by Django 3.1 on 2022-02-21 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0006_auto_20220219_2345'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='restrict_users_users',
            options={'verbose_name': 'Список исключений', 'verbose_name_plural': 'Список исключений'},
        ),
        migrations.AlterField(
            model_name='constants',
            name='restrict_users',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='constants.restrict_users_tgbot', verbose_name='Ограничение пользователей (ТГ БОТ)'),
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время редактирования')),
                ('channel_id', models.CharField(default='', max_length=100, verbose_name='Канал (ID)')),
                ('constant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constants.constants', verbose_name='Константа')),
            ],
            options={
                'verbose_name': 'Канал',
                'verbose_name_plural': 'Каналы',
            },
        ),
    ]