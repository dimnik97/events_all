# Generated by Django 2.0.6 on 2018-06-19 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20180619_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='allroles',
            name='ru_role',
            field=models.TextField(default=None),
        ),
    ]
