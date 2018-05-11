from django.shortcuts import render_to_response, get_object_or_404
from events_.models import Event
from custom_profile.models import Users

def index(request):
    user_id = request.user.pk
    context = {
        'title': "Лента событий",
<<<<<<< HEAD
        'user': Users.get_user(self),
        'locate': Users.get_user_locations(self),
        'events': Event.get_events(self)

    }

=======
        'user': Users.get_user(user_id),
        'locate': Users.get_user_locations(user_id),
        # 'user_url': Users.get_absolute_url(user_id)
    }

    # events = Event.get_events()
    # "events": events
>>>>>>> dd5e212959819d6b1e2e4a1145c9494c931b9395
    return render_to_response('index.html', context)
