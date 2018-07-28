from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from chats.models import ChatMessage
from events_all.helper import convert_base


def home(request):
    # TODO паджинация
    chats = ChatMessage.objects.filter(user=request.user).order_by('-peer__id', '-created').distinct('peer__id')

    context = {
        'chats': chats
    }
    return render(request, 'chats/index.html', context)


def room(request):
    messages = ChatMessage.objects.filter(user=request.user, peer=request.GET['d']).order_by('created')
    user = request.user
    peer = User.objects.get(id=request.GET['d'])

    room_members = list()
    room_members.append(user)
    room_members.append(peer)

    context = {
        'room_name_json': mark_safe(json.dumps(request.GET['d'])),
        'messages': messages,
        'room_members': room_members
    }
    return render(request, 'chats/room.html', context)
