# Generated by Django 2.1b1 on 2018-07-28 07:31

from django.db import migrations, models
import events_all.helper


class Migration(migrations.Migration):

    dependencies = [
        ('events_', '0013_auto_20180715_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventnews',
            name='news_image',
            field=models.ImageField(default=None, upload_to=events_all.helper.ImageHelper.upload_to),
        ),
    ]
