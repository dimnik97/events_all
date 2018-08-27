from django.contrib import admin
from .models import Room, ChatMessage, RoomMembers

admin.site.register(Room)
admin.site.register(ChatMessage)
admin.site.register(RoomMembers)