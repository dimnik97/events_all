from django.shortcuts import render, render_to_response
from profile.models import Users

def index(self):
    context = {
        'title': 'Профиль'
    }
    return render_to_response('index.html', context)