# Generated by Django 2.0.5 on 2018-05-12 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_set', to='custom_profile.Profile')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendship_creator_set', to='custom_profile.Profile')),
            ],
        ),
    ]