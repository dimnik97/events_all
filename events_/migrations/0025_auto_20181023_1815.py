# Generated by Django 2.1.1 on 2018-10-23 18:15

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events_', '0024_auto_20181022_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=datetime.date.today, null=True)),
            ],
            options={
                'verbose_name': 'Лайки',
                'verbose_name_plural': 'Лайки',
            },
        ),
        migrations.CreateModel(
            name='EventViews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=datetime.date.today, null=True)),
            ],
            options={
                'verbose_name': 'Просмотры',
                'verbose_name_plural': 'Просмотры',
            },
        ),
        migrations.AlterField(
            model_name='event',
            name='last_update',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 10, 23, 18, 15, 30, 398556, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='eventviews',
            name='event',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='events_.Event'),
        ),
        migrations.AddField(
            model_name='eventviews',
            name='user',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='eventlikes',
            name='event',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='events_.Event'),
        ),
        migrations.AddField(
            model_name='eventlikes',
            name='user',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
