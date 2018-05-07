from django.shortcuts import render, render_to_response
from accounts.models import Users

def index(self):
    context = {
        'title': "Лента событий",
        'user': Users.get_user(self),
        'locate': Users.get_user_locations(self)
    }
    return render_to_response('index.html', context)