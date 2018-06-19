from django.core.management.base import BaseCommand, CommandError
from django.utils.datetime_safe import datetime

from events_.models import Event, EventStatus


class Command(BaseCommand):
    args = ''
    help = 'Export data to remote server'

    def handle(self, *args, **options):
        # do something here


        events = Event.objects.filter(status__name ="active").exclude(end_time__gte=datetime.now())
        ended_status = EventStatus.objects.get(name="ended")
        for item in events:
            item.status = ended_status
            item.save()


        print(len(events))
