# Generated by Django 3.1 on 2021-05-09 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время редактирования')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_1c', models.CharField(blank=True, editable=False, max_length=255, null=True, verbose_name='UUID (1C)')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Филиал',
                'verbose_name_plural': 'Филиалы',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Время редактирования')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('id_1c', models.CharField(blank=True, editable=False, max_length=255, null=True, verbose_name='UUID (1C)')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Наименование')),
                ('territory', models.CharField(blank=True, max_length=200, null=True, verbose_name='Территория')),
                ('days_of_the_week', models.CharField(blank=True, max_length=200, null=True, verbose_name='Дни недели')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Адрес')),
                ('phone', models.CharField(blank=True, max_length=200, null=True, verbose_name='Телефон')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contractors.branch', verbose_name='Идентификатор Филиал')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
    ]
