# Generated by Django 2.0.6 on 2018-06-18 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_profile_subscribers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscribers',
            field=models.ManyToManyField(blank=True, to='profiles.Profile'),
        ),
    ]