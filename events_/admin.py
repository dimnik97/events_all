from django.contrib import admin
from .models import Event, EventParty, Event_avatar

admin.site.register(Event)
admin.site.register(EventParty)
admin.site.register(Event_avatar)