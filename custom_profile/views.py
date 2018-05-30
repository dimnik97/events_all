import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.template.loader import get_template, render_to_string
from django.views.generic import FormView

from custom_profile.forms import EditProfile, EditUserSettings
from custom_profile.models import Profile, Subscribers, ProfileAvatar
from django.shortcuts import get_object_or_404, render_to_response, redirect, render

from helper import parse_from_error_to_json


def index(request, id):
    if request.user.is_authenticated:
        account = request.user.id  # Залогиненный пользователь
        user = get_object_or_404(User, id=id)  # Отвечает за юзера, который отобразится в профиле

        avatar, created = ProfileAvatar.objects.get_or_create(user=user)

        friend_flag = 'add'
        try:
            if Subscribers.objects.filter(users=user.profile, current_user=request.user.profile):
                friend_flag = 'remove'
        except:
            friend_flag = 'add'

        friend_object, created = Subscribers.objects.get_or_create(current_user=user)
        friends = [friend for friend in friend_object.users.all() if friend != user]

        context = {
            'title': 'Профиль',
            'user': user,
            'users': Profile.get_users(),
            'friends': friends,
            'account': account,
            'friend_flag': friend_flag,
            'avatar': avatar
        }
        return render_to_response('user_profile.html', context)
    else:
        return redirect('/accounts/login')


# Добавление или удаление подписки
@login_required
def add_or_remove_friends(request):
    if request.is_ajax():
        try:
            user_id = request.POST['user_id']
            action = request.POST['action']
            owner = request.user
            new_friend = User.objects.get(id=user_id)

            if action == "add":
                Subscribers.make_friend(owner, new_friend)
            else:
                Subscribers.remove_friend(owner, new_friend)
        except KeyError:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    else:
        raise Http404


class Edit(FormView):
    def edit_view(request):
        if request.user.is_authenticated:
            user = request.user
            if request.method == 'POST':
                if request.POST['type'] == 'main_info':
                    form = EditProfile(request.POST)
                elif request.POST['type'] == 'settings':
                    form = EditUserSettings(request.POST)
                if form.is_valid():
                    form.save(request)
                    return HttpResponse(str(200))
                else:
                    data = parse_from_error_to_json(request, form)
                    return HttpResponse(json.dumps(data))

            form = EditProfile({'first_name': user.first_name,
                                'last_name': user.last_name,
                                'email': user.email,
                                'birth_date': user.profile.birth_date,
                                'phone': user.profile.phone,
                                'description': user.profile.description
                                })
            form_private = EditUserSettings({'messages': user.usersettings.messages,
                                             'birth_date': user.usersettings.birth_date,
                                             'invite': user.usersettings.invite,
                                             'near_invite': user.usersettings.near_invite,
                                             })
            context = {
                'title': 'Профиль',
                'form': form,
                'form_private': form_private,
                "csrf_token": get_token(request),
                'avatar': ProfileAvatar.objects.get(user=request.user.id)
            }

            return render_to_response('edit_user_profile.html', context)
        else:
            return redirect('/accounts/login')


def get_subscribers(request):
    user_id = request.GET.get('user', 1)
    is_my_account = False
    if str(request.user.id) == user_id:
        is_my_account = True
    friend_object, created = Subscribers.objects.get_or_create(current_user=user_id)
    friends = [friend for friend in friend_object.users.all() if friend != user_id]

    page = request.GET.get('page', 1)
    paginator = Paginator(friends, 20)
    try:
        friends = paginator.page(page)
    except PageNotAnInteger:
        friends = paginator.page(1)
    except EmptyPage:
        friends = paginator.page(paginator.num_pages)

    context = {
        'friends': friends,
        'user_id': user_id,
        'is_my_account': is_my_account
    }
    return render(request, 'subscribers.html', context)
