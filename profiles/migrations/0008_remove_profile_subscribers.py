# Generated by Django 2.0.6 on 2018-06-17 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20180617_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='subscribers',
        ),
    ]
