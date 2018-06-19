# Generated by Django 2.0.5 on 2018-06-18 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_', '0007_event_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]