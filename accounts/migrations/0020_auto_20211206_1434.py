# Generated by Django 3.2.9 on 2021-12-06 09:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20211205_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateField(default=datetime.date(2021, 12, 6)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_in',
            field=models.TimeField(default=datetime.time(9, 0)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_out',
            field=models.TimeField(default=datetime.time(17, 0)),
        ),
    ]