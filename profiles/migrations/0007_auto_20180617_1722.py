# Generated by Django 2.0.6 on 2018-06-17 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20180617_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscribers',
            field=models.ManyToManyField(related_name='_profile_subscribers_+', to='profiles.Profile'),
        ),
    ]
