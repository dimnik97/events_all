# Generated by Django 2.0.5 on 2018-06-10 03:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import events_all.helper


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('sex', models.CharField(choices=[('1', 'Мужчина'), ('2', 'Женщина')], default=1, max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профили',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='ProfileAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_update', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('image', models.ImageField(default='avatar/default/img.jpg', upload_to=events_all.helper.ImageHelper.upload_to)),
                ('user', models.OneToOneField(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Аватары',
                'verbose_name_plural': 'Аватары',
            },
        ),
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Подписчики',
                'verbose_name_plural': 'Подписчики',
            },
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messages', models.CharField(choices=[('1', 'Открыть сообщения для всех'), ('2', 'Написать могут только те, на кого я подписан'), ('3', 'Закрыть сообщения для всех')], default=1, max_length=2)),
                ('birth_date', models.CharField(choices=[('1', 'Видно всем'), ('2', 'Видно только подписчикам'), ('3', 'Скрыть для всех')], default=1, max_length=2)),
                ('invite', models.CharField(choices=[('1', 'Приглашать могут все'), ('2', 'Приглашать могут только те, на кого я подписан ')], default=1, max_length=2)),
                ('near_invite', models.CharField(choices=[('1', 'Включено'), ('2', 'Выключено')], default=1, max_length=2)),
                ('user', models.OneToOneField(default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Пользовательские настройки',
                'verbose_name_plural': 'Пользовательские настройки',
            },
        ),
    ]
