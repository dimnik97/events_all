import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, render_to_response

from cities_.models import CityTable
from events_.forms import EventForm, CreateEventNews
from events_all.helper import parse_from_error_to_json
from groups.models import Group
from profiles.models import Users
from .models import Event, EventParty, Event_avatar, EventNews


def index(request, id):
    event_id = id
    event_detail = get_object_or_404(Event, id=event_id)
    user_id = request.user.pk
    user = User.objects.get(id=user_id)

    avatar, created = Event_avatar.objects.get_or_create(event=event_detail)

    is_creator = 0
    if event_detail.creator_id == user:
        is_creator = 1

    party_flag = '',  # если пользователь уже подписан на выбранное событие
    try:
        if EventParty.objects.get(user_id=user, event_id=event_detail):
            party_flag = 1
    except EventParty.DoesNotExist:
        party_flag = 0

    # преобразовываем дату в нужный формат. При выводе на js будет вызвана функция
    #  пересчета времени относительно часового пояса пользователя
    event_detail.start_time = event_detail.start_time.strftime("%Y-%m-%d %H:%M")

    ev_object, created = EventParty.objects.get_or_create(event_id=event_id)
    subs = [friend for friend in ev_object.user_id.all()]

    news = None

    is_editor = 0
    if Group.is_editor(request, event_detail.created_by_group.id):
        is_editor = 1

    if request.method == 'POST':
        form = CreateEventNews(request.POST, request.FILES, request.GET)
        if form.is_valid():
            if event_detail.creator_id == request.user:
                form.save(request, event_detail)
                # 1 - флаг для определения создания, а не редактирвания, обрабатывается в форме
            elif event_detail.created_by_group:
                if is_editor == 1:
                    form.save(request, event_detail)
            try:
                news = list(EventNews.objects.filter(news_event=event_detail))
            except EventNews.DoesNotExist:
                news = None
    else:
        form = CreateEventNews()

    # event_news = EventNews.objects.filter(news_event=event_detail)
    event_news = None

    context = {
        'news_form': form,
        'title': 'Профиль',
        'user': user,
        'event': event_detail,
        'subs': subs,
        'party_flag': party_flag,
        'avatar': avatar,
        'is_creator': is_creator,
        'is_editor': is_editor,
        'event_news': event_news,
        "csrf_token": get_token(request),
        "ajax_response": news
    }
    return render_to_response('event_detail.html', context)


@login_required(login_url='/accounts/login/')
def subsc_unsubsc(request):
    if request.is_ajax():
        try:
            event = Event.objects.get(id=request.POST['event_id'])
            action = request.POST['action']
            user = request.user

            if action == "subscribe":
                EventParty.subscr_to_event(event,user)
            else:
                EventParty.unsubscr_from_event(event,user)
        except Event.DoesNotExist:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    else:
        raise Http404


@login_required(login_url='/accounts/login/')
def edit(request, event_id, group_id=None):
    user = request.user
    user_city = Users.get_user_locations(request)
    event = get_object_or_404(Event, id=event_id)
    if event.creator_id == user:
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request)
            else:
                data = parse_from_error_to_json(request, form)
                return HttpResponse(json.dumps(data))
        else:
            user_city = event.location
            form = EventForm({'id': event.id,
                              'name': event.name,
                              'description': event.description,
                              'start_time': event.start_time,
                              'end_time': event.end_time,
                              })

        avatar = Event_avatar.objects.get(event=event)
        city_list = CityTable.objects.filter(city__isnull=False).values('city', 'city_id').order_by('city')

        context = {
            'title': 'Редактирование события',
            'form': form,
            "csrf_token": get_token(request),
            'avatar': avatar,
            'city_list': city_list,
            'user_city': user_city
        }

        return render_to_response('edit.html', context)
    else:
        raise Http404


@login_required(login_url='/accounts/login/')
def create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, request.GET)
        if form.is_valid():
            result = form.save(request, 1)  # 1 - флаг создания
            if result['status'] == 200:
                return HttpResponse(json.dumps(result))
        else:
            data = parse_from_error_to_json(request, form)
            return HttpResponse(json.dumps(data))
    else:
        form = EventForm()

    user_city = Users.get_user_locations(request)
    context = {
        'title': 'Создание события',
        'form': form,
        "csrf_token": get_token(request),
        'city_list': CityTable.all_city_exclude_user_city(user_city),
        'user_city': user_city
    }
    return render_to_response('create.html', context)


