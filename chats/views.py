from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.safestring import mark_safe
import json

from chats.models import ChatMessage, Room, RoomMembers


def home(request):

    # TODO паджинация
    chats = ChatMessage.objects.filter(user=request.user).order_by('-peer__id', '-room', '-created').distinct('peer__id', 'room')
    is_room = 0
    # TODO ну тут как-то совсем не очень написано
    try:
        request_peer = request.GET['peer_id']
    except MultiValueDictKeyError:
        request_peer = False
    try:
        request_peer = request.GET['room_id']
        is_room = 1
    except MultiValueDictKeyError:
        pass
    context = {
        'chats': chats,
        'is_request': request_peer,
        'is_room': is_room
    }
    return render(request, 'chats/index.html', context)


def room(request):
    try:
        peer = request.GET['d']
        messages = ChatMessage.objects.filter(user=request.user, peer=peer).order_by('created')
        is_room = False
    except KeyError:
        messages = ChatMessage.objects.filter(user=request.user, room=request.GET['r']).order_by('created')
        is_room = True

    user = request.user
    room_members = list()
    peer = {
        'status': 200,
        'peer': False,
        'text': '',
        'room': False
    }
    room_id = ''
    peer_id = ''
    if is_room:
        room_id = request.GET['r']
        flag = False
        members = RoomMembers.objects.filter(room_rel_id=request.GET['r'])
        for member in members:
            if member.user_rel == request.user:
                flag = True
            room_members.append(member.user_rel)
        if not flag:
            peer['status'] = '404'
            peer['text'] = 'У вас нет доступа в этот чат'
            # return # Придумать с этим что-нибудь
    else:
        try:
            peer_id = request.GET['d']
            peer['peer'] = User.objects.get(id=peer_id)
            # if peer['peer'].active == 2:
            #     peer['status'] = '403'
            #     peer['text'] = 'Пользователь был удален'
            # if peer['peer'].active == 3:
            #     peer['status'] = '403'
            #     peer['text'] = 'Пользователь был заблокирован'

            room_members.append(user)
            room_members.append(peer['peer'])
        except:
            peer['status'] = '404'
            peer['text'] = 'Пользователя с таким id не существует'

    context = {
        'peer_id_json': mark_safe(json.dumps(peer_id)),
        'room_id_json': mark_safe(json.dumps(room_id)),
        'messages': messages,
        'room_members': room_members,
        'peer': peer
    }
    return render(request, 'chats/room.html', context)
