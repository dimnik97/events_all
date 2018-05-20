from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Event, EventParty

# Create your views here.


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
                EventParty.unsubscr_to_event(event,user)
        except KeyError:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    else:
        raise Http404
