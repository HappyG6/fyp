# Generated by Django 3.1.13 on 2021-12-11 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kblock', '0027_auto_20211211_1623'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkhash',
            old_name='orihash',
            new_name='filehash',
        ),
    ]