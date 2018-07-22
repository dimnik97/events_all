from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from chats.models import ChatMessage


def home(request):

    chats = ChatMessage.objects.filter(user=request.user).order_by('peer__id', '-created').distinct('peer__id')
    context = {
        'chats': chats
    }
    return render(request, 'chats/index.html', context)


def room(request, room_name):
    return render(request, 'chats/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
