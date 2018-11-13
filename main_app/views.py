import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404

from cities_.models import CityTable
from events_.models import Event, EventCategory
from groups.models import Group, Membership
from profiles.models import Users


# Получение данных на основную ленту
def index(request):
    user = request.user
    category_list = EventCategory.objects.all()
    user_city = Users.get_user_locations(request, need_ip=False)  # город либо через IP либо через установленный
    city_list = CityTable.all_city_exclude_user_city(user_city)

    context = {
        'user': user,
        'category_list': category_list,
        'city_list': city_list,
        'user_city': user_city,
        'url': 'get_infinite_events',
        'page_url': '/',
        'filter_city': True
    }

    return render_to_response('main_app/index.html', context)


# Намеренное разделение на два одинаковых метода (в дальнейшем будет изменяться)
def friends(request):
    user = request.user
    category_list = EventCategory.objects.all()

    context = {
        'user': user,
        'category_list': category_list,
        'url': 'get_friend_events',
        'filter_city': False
    }

    return render_to_response('main_app/index.html', context)


# Получение данных на карту событий
def event_map(request):
    user = request.user
    category_list = EventCategory.objects.all()
    # Не забыть про закрытые эвенты
    user_city = Users.get_user_locations(request, need_ip=False)  # город либо через IP либо через установленный

    context = {
        'user': user,
        'category_list': category_list,
        'user_city': user_city,
    }

    return render_to_response('main_app/map.html', context)


# Паджинация основной ленты
def get_infinite_events(request):
    events = Event.get_events(request)
    context = Event.paginator(request, events)
    return render(request, 'main_app/event_item.html', context)


# Паджинация основной ленты
def get_friend_events(request):
    events = Event.get_friend_events(request)
    context = Event.paginator(request, events)
    return render(request, 'main_app/event_item.html', context)


# Карта событий
def get_events_map(request):
    events = []
    for event in Event.get_events(request, is_simple=True):
        if event.geo_point and event.geo_point.lat == event.geo_point.lat and event.geo_point.lng == event.geo_point.lng:
            events.append({
                'name': event.name,
                'lat': event.geo_point.lat,
                'lng': event.geo_point.lng,
                'id': event.id
            })

    return HttpResponse(json.dumps(events, ensure_ascii=False))


# Подгрузка новых событий
def get_new_events(request):
    if 'last_update' in request.POST and request.POST['last_update'] != '':
        events = Event.get_events(request, request.POST['last_update'])
        context = Event.paginator(request, events)
        return render(request, 'main_app/event_item.html', context)


def get_new_events_count(request):
    events_count = 0
    try:
        if 'last_update' in request.POST and request.POST['last_update'] != '':
            events_count = Event.get_events(request, request.POST['last_update']).count()
    finally:
        return HttpResponse(events_count)


def active_user_events(request):
    # Получение ленты активных событий
    id = request.GET['id']
    user = get_object_or_404(User, id=id)
    events = Event.get_ended_or_active_user_events(request, user, 'active')
    context = Event.paginator(request, events)
    context.update({'get_page_url': 'active', 'id': id})
    return render(request, 'main_app/event_item.html', context)


def ended_user_events(request):
    # Получение ленты неактивных событий
    id = request.GET['id']
    user = get_object_or_404(User, id=id)
    events = Event.get_ended_or_active_user_events(request, user, 'ended')
    context = Event.paginator(request, events)
    context.update({'get_page_url': 'ended', 'id': id})
    return render(request, 'main_app/event_item.html', context)


def user_events(request):
    # Получение ленты событий созданных пользователем
    id = request.GET['id']
    events = Event.get_user_events(request, id)
    context = Event.paginator(request, events)
    context.update({'get_page_url': 'user_events', 'id': id})
    return render(request, 'main_app/event_item.html', context)


def get_group_events(request):
    # Получение ленты неактивных событий
    id = request.GET['id']
    group = get_object_or_404(Group, id=id)
    if group.active != '1':  # Если группа закрыта или заблокирована
        try:
            Membership.objects.get(group_id=id, person=request.user.profile)  # Если подписчик
        except Membership.DoesNotExist:
            return False
    events = Event.get_group_events(request, group)
    context = Event.paginator(request, events)
    context.update({'get_page_url': 'groups', 'id': id})
    return render(request, 'main_app/event_item.html', context)
