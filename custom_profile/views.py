from django.contrib.auth.models import User

from custom_profile.models import Users
from django.shortcuts import get_object_or_404, render_to_response


def index(request, id):
    user = get_object_or_404(User, id=id)

    context = {
        'title': 'Профиль',
        'user': user
    }
    return render_to_response('user_profile.html', context)