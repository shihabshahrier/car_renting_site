# Generated by Django 4.2.3 on 2023-08-01 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rename_address_driver_curent_city_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='curent_city',
            new_name='current_city',
        ),
    ]