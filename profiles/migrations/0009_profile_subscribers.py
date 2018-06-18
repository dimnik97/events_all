# Generated by Django 2.0.6 on 2018-06-17 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_remove_profile_subscribers'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='_profile_subscribers_+', to='profiles.Profile'),
        ),
    ]
