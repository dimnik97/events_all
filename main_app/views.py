import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render_to_response, render

from cities_.models import CityTable
from events_.models import Event, EventCategory
from profiles.models import Users


# Получение данных на основную ленту
def index(request):
    user = request.user
    category_list = EventCategory.objects.all()

    city_list = CityTable.objects.filter(city__isnull=False).values('city', 'city_id').order_by('city')
    user_city = Users.get_user_locations(request)

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
    user_city = Users.get_user_locations(request)
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
        from django.core import serializers
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

    page = request.GET.get('page', 1)
    paginator = Paginator(events, 20)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    context = {'events': events, 'action': False}
    return render(request, 'event_item.html', context)
