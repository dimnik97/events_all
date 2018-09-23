from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, render

from cities.models import CityTable
from events_.models import Event, EventCategory
from profiles.models import Users


def index(request):
    user = request.user
    category_list = EventCategory.objects.all()

    city_list = CityTable.objects.filter(city__isnull=False).values('city', 'city_id').order_by('city')[:10]
    user_city = Users.get_user_locations(request)

    context = {
        'title': "Лента событий",
        'user': user,
        'locate': Users.get_user_locations(user),
        'category_list': category_list,
        'city_list': city_list,
        'user_city': user_city
    }

    return render_to_response('index.html', context)


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
