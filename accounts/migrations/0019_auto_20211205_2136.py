# Generated by Django 3.2.9 on 2021-12-05 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_alter_meeting_time_slott'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='t9to10',
            new_name='t09to10',
        ),
        migrations.AlterField(
            model_name='meeting',
            name='time_slott',
            field=models.CharField(default='t09to10', max_length=50),
        ),
    ]
