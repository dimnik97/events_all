# Generated by Django 2.0.6 on 2018-06-17 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20180617_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='subscribers',
            field=models.ManyToManyField(null=True, related_name='_profile_subscribers_+', to='profiles.Profile'),
        ),
    ]