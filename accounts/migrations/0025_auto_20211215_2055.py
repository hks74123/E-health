# Generated by Django 3.2.9 on 2021-12-15 15:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_profile_details'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='checked_out',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateField(default=datetime.date(2021, 12, 15)),
        ),
    ]
