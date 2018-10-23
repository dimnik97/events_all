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

    city_list = CityTable.objects.filter(city__isnull=False).values('city', 'city_id').order_by('city')
    try:
        user_city = request.user.profile.location
    except:
        user_city = CityTable.objects.get(city='Москва')

    context = {
        'user': user,
        'locate': Users.get_user_locations(user),
        'category_list': category_list,
        'city_list': city_list,
        'user_city': user_city
    }

    return render_to_response('index.html', context)


# Получение данных на карту событий
def event_map(request):
    user = request.user
    # Не забыть про закрытые эвенты
    city_list = CityTable.objects.filter(city__isnull=False).values('city', 'city_id').order_by('city')
    try:
        user_city = request.user.profile.location
    except:
        user_city = CityTable.objects.get(city='Москва')
    events = Event.objects.filter(location=user_city.city_id).only('name', 'geo_point__lng',
                                                                   'geo_point__lat', 'geo_point__name',
                                                                   'id').select_related('event_avatar')

    context = {
        'user': user,
        'locate': Users.get_user_locations(user),
        'city_list': city_list,
        'user_city': user_city,
        'events': list(events)
    }

    return render_to_response('event_map.html', context)


# Получение данных на карту событий при смене города
def get_event_map(request):
    if 'city_id' in request.POST:
        city_id = request.POST['city_id']
        events = Event.objects.filter(location=city_id).only('name', 'geo_point__lng',
                                                             'geo_point__lat', 'geo_point__name',
                                                             'id').select_related('event_avatar')
        result = []
        for event in events:
            result.append({
                'name': event.name,
                'lat': event.geo_point.lat,
                'lng': event.geo_point.lng,
                'image': event.event_avatar.mini_url,
            })
        return HttpResponse(json.dumps(result))


# Паджинация основной ленты
def get_infinite_events(request):
    events = Event.get_events(request)
    context = Event.paginator(request, events)
    return render(request, 'event_item.html', context)


# Подгрузка новых событий
def get_new_events(request):
    if 'last_update' in request.POST and request.POST['last_update'] != '':
        events = Event.get_events(request, request.POST['last_update'])
        context = Event.paginator(request, events)
        return render(request, 'event_item.html', context)


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
    return render(request, 'event_item.html', context)


def ended_user_events(request):
    # Получение ленты неактивных событий
    id = request.GET['id']
    user = get_object_or_404(User, id=id)
    events = Event.get_ended_or_active_user_events(request, user, 'ended')
    context = Event.paginator(request, events)
    context.update({'get_page_url': 'ended', 'id': id})
    return render(request, 'event_item.html', context)


def user_events(request):
    # Получение ленты событий созданных пользователем
    id = request.GET['id']
    events = Event.get_user_events(request, id)
    context = Event.paginator(request, events)
    context.update({'get_page_url': 'user_events', 'id': id})
    return render(request, 'event_item.html', context)


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
    return render(request, 'event_item.html', context)
