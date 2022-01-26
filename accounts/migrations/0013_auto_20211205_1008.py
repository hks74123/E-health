# Generated by Django 3.2.9 on 2021-12-05 04:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20211203_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='host',
            name='start_time',
        ),
        migrations.AddField(
            model_name='host',
            name='T_10to11',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='host',
            name='T_11to12',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='host',
            name='T_13to14',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='host',
            name='T_14to15',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='host',
            name='T_15to16',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='host',
            name='T_16to17',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='host',
            name='T_9to10',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 12, 5, 10, 8, 19, 565190)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_in',
            field=models.TimeField(default=datetime.datetime(2021, 12, 5, 10, 8, 19, 565190)),
        ),
    ]