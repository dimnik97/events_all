# Generated by Django 2.0.5 on 2018-05-08 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0002_auto_20180501_0209'),
        ('events_', '0002_auto_20180508_0304'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventparty',
            name='user_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='profile.Profile'),
            preserve_default=False,
        ),
    ]
