from django.shortcuts import render_to_response


def index(self):
    context = {
        'title': 'Профиль'
    }
    return render_to_response('index.html', context)