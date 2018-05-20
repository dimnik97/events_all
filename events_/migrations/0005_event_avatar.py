# Generated by Django 2.0.5 on 2018-05-20 12:35

import datetime
from django.db import migrations, models
import django.db.models.deletion
import helper


class Migration(migrations.Migration):

    dependencies = [
        ('events_', '0004_eventparty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('image', models.ImageField(default='media/avatar/default/img.jpg', upload_to=helper.upload_to)),
                ('event', models.OneToOneField(default=True, on_delete=django.db.models.deletion.CASCADE, to='events_.Event')),
            ],
            options={
                'verbose_name': 'Аватары',
                'verbose_name_plural': 'Аватары',
            },
        ),
    ]