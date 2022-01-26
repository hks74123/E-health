# Generated by Django 3.2.9 on 2021-12-05 15:28

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20211205_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='time_slott',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 12, 5, 20, 57, 48, 939129)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_in',
            field=models.TimeField(default=datetime.datetime(2021, 12, 5, 20, 57, 48, 939129)),
        ),
    ]
