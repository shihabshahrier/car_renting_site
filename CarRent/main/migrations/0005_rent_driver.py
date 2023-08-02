# Generated by Django 4.2.3 on 2023-08-01 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_garage_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='driver',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.driver'),
            preserve_default=False,
        ),
    ]