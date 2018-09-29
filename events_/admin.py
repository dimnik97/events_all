from django.contrib import admin
from .models import Event, Event_avatar, EventCategory, EventStatus, EventNews, EventMembership

admin.site.register(Event)
admin.site.register(EventMembership)
admin.site.register(Event_avatar)
admin.site.register(EventCategory)
admin.site.register(EventStatus)
admin.site.register(EventNews)
