# Generated by Django 3.1.13 on 2021-10-10 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kblock', '0014_auto_20211010_1836'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yourmodel',
            name='slug',
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='name',
            field=models.CharField(default='ok', max_length=12),
        ),
    ]