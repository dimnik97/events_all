from django.contrib import admin
from .models import Event
from .models import EventParty

admin.site.register(Event)
admin.site.register(EventParty)