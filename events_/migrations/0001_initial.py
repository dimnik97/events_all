# Generated by Django 2.0.5 on 2018-05-07 03:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20180501_0209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('participants', models.IntegerField(null=True)),
                ('creator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='EventParty',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events_.Event')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
    ]
