from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, render_to_response, redirect

from events_.forms import EditEvent
from .models import Event, EventParty, Event_avatar


def index(request, id):
    event_detail = get_object_or_404(Event, id=id)
    user_id = request.user.pk
    user = User.objects.get(id=user_id)

    avatar, created = Event_avatar.objects.get_or_create(event=event_detail)

    is_creator = 0
    if event_detail.creator_id == user:
        is_creator = 1

    # party_flag = 1, если пользователь уже подписан на выбранное событие
    try:
        if EventParty.objects.get(user_id=user, event_id=event_detail):
            party_flag = 1
    except:
        party_flag = 0

    # преобразовываем дату в нужный формат. При выводе на js будет вызвана функция пересчета времени относительно часового пояса пользователя
    event_detail.start_time = event_detail.start_time.strftime("%Y-%m-%d %H:%M")

    ev_object, created = EventParty.objects.get_or_create(event_id=id)
    subs = [friend for friend in ev_object.user_id.all()]

    context = {
        'title': 'Профиль',
        'user': user,
        'event': event_detail,
        'subs': subs,
        'party_flag': party_flag,
        'avatar': avatar,
        'is_creator': is_creator
    }
    return render_to_response('event_detail.html', context)


def subsc_unsubsc(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                event = Event.objects.get(id=request.POST['event_id'])
                action = request.POST['action']
                user = request.user

                if action == "subscribe":
                    EventParty.subscr_to_event(event,user)
                else:
                    EventParty.unsubscr_from_event(event,user)
            except KeyError:
                return HttpResponse('Error')
            return HttpResponse(str(200))
        else:
            raise Http404
    else:
        return redirect('/accounts/login')


def edit(request, id):
    user = request.user
    if user.is_authenticated:
        event = get_object_or_404(Event, id=id)
        if event.creator_id == user:
            if request.method == 'POST':
                form = EditEvent(request.POST, request.FILES)
                if form.is_valid():
                    form.save(request)
            else:
                form = EditEvent({'id': event.id,
                                  'name': event.name,
                                  'description': event.description,
                                  'start_time': event.start_time,
                                  'end_time': event.end_time,
                                  })

            avatar, created = Event_avatar.objects.get_or_create(event=event)
            context = {
                'title': 'Редактирование события',
                'form': form,
                "csrf_token": get_token(request),
                'avatar': avatar
            }

            return render_to_response('edit.html', context)
        else:
            raise Http404
    else:
        return redirect('/accounts/login')


def create(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            form = EditEvent(request.POST, request.FILES, request.GET)
            if form.is_valid():
                response = form.save(request, 1)  # 1 - флаг для определения создания, а не редактирвания, обрабатывается в форме
                return redirect('/events/' + str(int(response.content)))
        else:
            form = EditEvent()

        context = {
            'title': 'Создание события',
            'form': form,
            "csrf_token": get_token(request)
        }
        return render_to_response('create.html', context)

    else:
        return redirect('/accounts/login')
