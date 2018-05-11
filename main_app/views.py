from django.shortcuts import render_to_response, get_object_or_404
from events_.models import Event
from custom_profile.models import Users

def index(request):
    user_id = request.user.pk
    context = {
        'title': "Лента событий",

        'events': Event.get_events(),


        'user': Users.get_user(user_id),
        'locate': Users.get_user_locations(user_id),
        # 'user_url': Users.get_absolute_url(user_id)
    }

    # events = Event.get_events()
    # "events": events
    return render_to_response('index.html', context)
