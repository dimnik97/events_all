from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Event, EventParty, Event_avatar


def index(request, id):
    event_detail = get_object_or_404(Event, id=id)
    user_id = request.user.pk
    user = User.objects.get(id=user_id)

    avatar, created = Event_avatar.objects.get_or_create(event=event_detail)

    sub_flag = 'subscribe'
    try:
        if EventParty.objects.get(user_id=user, event_id=event_detail):
            sub_flag = 'unsubscribe'
    except:
        sub_flag = 'subscribe'

    ev_object, created = EventParty.objects.get_or_create(event_id=id)
    subs = [friend for friend in ev_object.user_id.all()]

    context = {
        'title': 'Профиль',
        'user': user,
        'event': event_detail,
        'subs': subs,
        'sub_flag': sub_flag,
        'avatar': avatar
    }
    return render_to_response('event_detail.html', context)


def subsc_unsubsc(request):
    if request.is_ajax():
        try:
            # user_id = request.POST['user_id']
            event = Event.objects.get(id=request.POST['event_id'])
            action = request.POST['action']
            user = get_object_or_404(User, id=request.user.id)
            # owner = request.user.profile

            if action == "subscribe":
                EventParty.subscr_to_event(event,user)
            else:
                EventParty.unsubscr_from_event(event,user)
        except KeyError:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    else:
        raise Http404
