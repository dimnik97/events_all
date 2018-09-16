import operator

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from chats.models import ChatMessage, Room, RoomMembers


@login_required(login_url='/accounts/login/')
def home(request):
    # TODO паджинация
    chat_type = 'error'
    request_peer = False
    if 'room' in request.GET:
        request_peer = request.GET['room']
        chat_type = 'room'
    elif 'peer' in request.GET:
        request_peer = request.GET['peer']
        chat_type = 'peer'

    context = {
        # 'chats': chats,
        'is_request': request_peer,
        'url_type': chat_type
    }
    return render(request, 'chats/index.html', context)


def get_dialogs(request):
    name = ''
    if 'name' in request.GET:
        name = request.GET['name']

    from django.db.models import Q
    chats = ChatMessage.objects.filter(
        Q(room__name__istartswith=name)
        | Q(peer__last_name__istartswith=name)
        | Q(peer__first_name__istartswith=name),
        user=request.user).order_by('-peer__id', '-room__id', '-created').distinct(
        'peer__id', 'room__id')

    chats = sorted(chats, key=operator.attrgetter('created'), reverse=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(chats, 10)
    try:
        chats = paginator.page(page)
    except PageNotAnInteger:
        chats = paginator.page(1)
    except EmptyPage:
        chats = paginator.page(paginator.num_pages)

    context = {'chats': chats}
    return render(request, 'chats/dialogs_template.html', context)


@login_required(login_url='/accounts/login/')
def room(request):
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
    room = ''
    room_name = ''
    chat_type = ''
    if 'room' in request.GET:
        chat_type = 'room'
    elif 'peer' in request.GET:
        chat_type = 'peer'

    if chat_type == 'room':
        room_id = request.GET[chat_type]
        flag = False
        members = RoomMembers.objects.filter(room_rel_id=request.GET['room'])
        try:
            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            context = {
                'status': '',
                'text': ''
            }
            context['status'] = 404
            context['text'] = 'Чат не создан, либо у вас нет доступа к данному чату'
            return render(request, 'chats/room.html', context)

        for member in members:
            if member.user_rel == request.user:
                flag = True
                if member.joined == False and member.user_rel == request.user:
                    peer['status'] = '404'
                    peer['text'] = 'Сначала присоединитесь к чату'
                    break
            room_members.append(member.user_rel)
        if not flag:
            peer['status'] = '404'
            peer['text'] = 'У вас нет доступа в этот чат'
        else:
            room_name = Room.objects.get(id=room_id).name
    else:
        try:
            peer_id = request.GET[chat_type]
            peer['peer'] = User.objects.get(id=peer_id)
            # if peer['peer'].active == 2:
            #     peer['status'] = '403'
            #     peer['text'] = 'Пользователь был удален'
            # if peer['peer'].active == 3:
            #     peer['status'] = '403'
            #     peer['text'] = 'Пользователь был заблокирован'

            room_members.append(user)
            room_members.append(peer['peer'])
            room_name = peer['peer'].first_name + ' ' + peer['peer'].last_name
        except:
            peer['status'] = '404'
            peer['text'] = 'Пользователя с таким id не существует'
    context = {
        'peer_id_json': mark_safe(json.dumps(peer_id)),
        'room_id_json': mark_safe(json.dumps(room_id)),
        'room_members': room_members,
        'peer': peer,
        'user': request.user,
        'chat_type': chat_type,
        'chat_id': request.GET[chat_type],
        'room_name': room_name,
        'room': room,
        'status': 200
    }
    return render(request, 'chats/room.html', context)


def get_messages(request):
    messages = []
    chat_type = ''
    if 'room' in request.GET:
        chat_type = 'room'
        messages = ChatMessage.objects.filter(user=request.user, room=request.GET[chat_type]).order_by('-created')
    elif 'peer' in request.GET:
        chat_type = 'peer'
        messages = ChatMessage.objects.filter(user=request.user, peer=request.GET[chat_type]).order_by('-created')

    page = request.GET.get('page', 1)
    paginator = Paginator(messages, 20)
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)

    context = {
        'messages': messages,
        'chat_type': chat_type,
        'chat_id': request.GET[chat_type]
    }
    return render(request, 'chats/messages_template.html', context)


def create_room(request):
    result = Room.create_room(request)
    return HttpResponse(json.dumps(result))


def add_user_to_room(request):
    result = Room.add_user_to_room(request)
    return HttpResponse(json.dumps(result))


def join_room(request):
    result = Room.join_room(request)
    return HttpResponse(json.dumps(result))


def decline_room(request):
    result = Room.decline_room(request)
    return HttpResponse(json.dumps(result))


def remove_user_from_room(request):
    result = Room.remove_user_from_room(request)
    return HttpResponse(json.dumps(result))


def delete_message(request):
    result = ChatMessage.delete_message(request)
    return HttpResponse(json.dumps(result))


def read_message(request):
    result = ChatMessage.read_messages(request)
    return HttpResponse(json.dumps(result))