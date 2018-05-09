from django.shortcuts import render, render_to_response
from accounts.models import Users
from events_.models import Event, EventParty

def index(self):
    context = {
        'title': "Лента событий",
        'user': Users.get_user(self),
        'locate': Users.get_user_locations(self)
    }

    events = Event.get_events()
    return render_to_response('index.html', {"context": context, "events": events})
