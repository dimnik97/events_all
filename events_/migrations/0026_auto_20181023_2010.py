# Generated by Django 2.1.1 on 2018-10-23 20:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events_', '0025_auto_20181023_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='last_update',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 10, 23, 20, 10, 51, 898319, tzinfo=utc)),
        ),
    ]