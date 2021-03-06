# Generated by Django 2.0.6 on 2018-06-19 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0010_auto_20180618_0925'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AllRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.TextField(default=None)),
                ('able_edit', models.BooleanField()),
                ('able_delete', models.BooleanField()),
                ('able_create_event', models.BooleanField()),
                ('able_edit_event', models.BooleanField()),
                ('able_delete_event', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(blank=True, max_length=100, null=True)),
                ('name', models.TextField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('1', 'Открытая'), ('2', 'Закрытая')], default=1, max_length=2)),
                ('creator', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Группы',
                'verbose_name_plural': 'Группы',
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField()),
                ('invite_reason', models.CharField(default=None, max_length=64)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.Group')),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membership_invites', to='profiles.Profile')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.Profile')),
                ('role', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='groups.AllRoles')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(through='groups.Membership', to='profiles.Profile'),
        ),
    ]
