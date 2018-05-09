from django.shortcuts import render, render_to_response
<<<<<<< HEAD
from accounts.models import Users
from events_.models import Event, EventParty
=======
from profile.models import Users
>>>>>>> e37b78319d6bd3996b7a0729297e2f8a74e3a0ab

def index(self):
    context = {
        'title': "Лента событий",
        'user': Users.get_user(self),
        'locate': Users.get_user_locations(self)
    }

    events = Event.get_events()
    return render_to_response('index.html', {"context": context, "events": events})
