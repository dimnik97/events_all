# Generated by Django 2.1.1 on 2018-09-28 15:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events_', '0017_auto_20180928_1552'),
        ('groups', '0009_auto_20180827_1701'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=3000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('flags', models.IntegerField()),
                ('peer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_to', to=settings.AUTH_USER_MODEL)),
                ('peer_msg', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chats.ChatMessage')),
            ],
            options={
                'verbose_name': 'Сообщения',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default=None, max_length=200)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events_.Event')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='groups.Group')),
            ],
            options={
                'verbose_name': 'Чаты (групп, евентов)',
                'verbose_name_plural': 'Чаты (групп, евентов)',
            },
        ),
        migrations.CreateModel(
            name='RoomMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('additional_info', models.IntegerField(default=None, null=True)),
                ('joined', models.BooleanField(default=True)),
                ('room_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.Room')),
                ('user_rel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Участники чатов',
                'verbose_name_plural': 'Участники чатов',
            },
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chats.Room'),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_from', to=settings.AUTH_USER_MODEL),
        ),
    ]
