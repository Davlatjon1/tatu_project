# Generated by Django 3.1 on 2021-05-08 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instruments_telegram', '0009_remove_aboutus_id_1c'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_reason', models.CharField(max_length=64)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instruments_telegram.group')),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_invites', to='instruments_telegram.person')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instruments_telegram.person')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='instruments_telegram.Membership', to='instruments_telegram.Person'),
        ),
    ]