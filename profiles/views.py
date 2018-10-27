import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.views.generic import FormView

from cities_.models import CityTable
from groups.models import Group
from images_custom.models import PhotoEditor
from profiles.forms import ImageUploadForm
from profiles.models import Profile, ProfileAvatar, Users, ProfileSubscribers
from django.shortcuts import get_object_or_404, render_to_response, render, redirect


# Редирект на аккаунт пользователя
@login_required(login_url='/accounts/login/')
def my_profile(request):
    url = '/profile/' + str(request.user.id)
    return redirect(url)


@login_required(login_url='/accounts/login/')
def detail(request, id):   # TODO переделать, 4 запроса, серьезно?
    user = request.user  # Залогиненный пользователь
    cur_user = get_object_or_404(User, id=id)  # Отвечает за юзера, который отобразится в профиле
    avatar, created = ProfileAvatar.objects.get_or_create(user=cur_user)  # Аватар
    groups_count = Group.objects.filter(membership__person=cur_user.profile).count()  # Количество групп пользователя
    subscribers = ProfileSubscribers.objects.filter(from_profile=cur_user.profile).count()  # Количество подписчиков
    followers = ProfileSubscribers.objects.filter(to_profile=cur_user.profile).count()  # Количество подписок
    friend_flag = 'remove' if ProfileSubscribers.objects.filter(from_profile=user.profile,  # Добавлен в друзья?
                                                                to_profile=cur_user.profile).count() else 'add'

    from django.utils import timezone
    if (timezone.now() - cur_user.profile.last_activity).seconds > 1800:
        is_online = 'Последний раз в сети ' + str(cur_user.profile.last_activity)
    elif (timezone.now() - cur_user.profile.last_activity).seconds > 900:
        is_online = 'Последний раз в сети менее 15 минут назад'
    else:
        is_online = 'online'

    context = {
        'user': user,
        'cur_user': cur_user,
        'avatar': avatar,
        'is_online': is_online,
        'followers': followers,
        'friend_flag': friend_flag,
        'groups_count': groups_count,
        'subscribers': subscribers,
    }
    return render_to_response('profile_detail.html', context)


# Добавление или удаление подписки
@login_required(login_url='/accounts/login/')
def add_or_remove_friends(request):
    if request.is_ajax():
        try:
            user_id = request.POST['user_id']
            if user_id != request.user.id:
                action = request.POST['action']
                new_friend = User.objects.get(id=user_id)

                if action == "add":
                    ProfileSubscribers.make_friend(request, new_friend)
                else:
                    ProfileSubscribers.remove_friend(request, new_friend)
        except KeyError:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    else:
        raise Http404


@login_required(login_url='/accounts/login/')
def edit_view(request):
    context, is_validate = Profile.edit(request)
    if is_validate is True:
        return HttpResponse(json.dumps(context))
    return render(request, 'profile_edit.html', context)


class Edit(FormView):
    @staticmethod
    def change_avatar(request):
        if request.method == 'POST' and request.is_ajax():
            return PhotoEditor.load_image(request)
        context = {
            'image_file': ImageUploadForm(),
            'avatar': ProfileAvatar.objects.get(user=request.user.id),
            'url': request.META['PATH_INFO'],
            'save_url': '/profile/save_image'
        }
        return render(request, 'change_avatar.html', context)

    @staticmethod
    def change_mini(request):
        if request.method == 'POST' and request.is_ajax():
            return PhotoEditor.load_image(request)

        url = request.user.profileavatar.reduced_url
        path = request.user.profileavatar.reduced_path

        image_attr = PhotoEditor.get_image_size(path)

        context = {
            'image_file': ImageUploadForm(),
            'reduced': url,
            'image_attr': image_attr,
            'url': request.META['PATH_INFO'],
            'save_url': '/profile/save_image'
        }
        return render(request, 'change_mini.html', context)

    @staticmethod
    def save_image(request):
        if request.method == 'POST' and request.is_ajax():
            model = request.user.profileavatar
            return PhotoEditor.save_image(request, model)


def get_subscribers(request):
    context = ProfileSubscribers.get_subscribers(request)
    if not context['flag']:
        return render(request, 'subscribers.html', context)
    else:
        return render(request, 'search_subscribers_items.html', context)


def get_followers(request):
    context = ProfileSubscribers.get_followers(request)
    if not context['flag']:
        return render(request, 'subscribers.html', context)
    else:
        return render(request, 'search_subscribers_items.html', context)


def custom_fields_for_signup(request):
    city_list = CityTable.objects.filter(city__isnull=False).values('city', 'city_id').order_by('city')
    user_city = Users.get_user_locations(request)
    context = {
        'city_list': city_list,
        'user_city': user_city
    }
    return HttpResponse(render_to_string('custom_fields_for_signup.html', context=context))
