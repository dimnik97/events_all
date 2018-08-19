import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.middleware.csrf import get_token
from django.views.generic import FormView

from groups.models import Group
from images_custom.models import PhotoEditor
from profiles.forms import EditProfile, EditUserSettings, ImageUploadForm
from profiles.models import Profile, ProfileAvatar
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from events_all.helper import parse_from_error_to_json


# Редирект на аккаунт пользователя
@login_required(login_url='/accounts/login/')
def my_profile(request):
    url = '/profile/' + str(request.user.id)
    return redirect(url)


@login_required(login_url='/accounts/login/')
def detail(request, id):
    account = request.user.id  # Залогиненный пользователь
    user = get_object_or_404(
        User, id=id)  # Отвечает за юзера, который отобразится в профиле

    avatar, created = ProfileAvatar.objects.get_or_create(user=user)

    subscribers_object = user.profile.subscribers
    profile = user.profile
    # TODO выборка из 5 показываемых
    subscribers = [
        User.objects.get(id=subscriber.user_id)
        for subscriber in subscribers_object.all() if subscriber != profile
    ]

    groups = Group.objects.all()

    friend_flag = 'add'
    try:
        # TODO Долго, переписать
        for item in request.user.profile.subscribers.all():
            if item == profile:
                friend_flag = 'remove'
    except:
        friend_flag = 'add'

    followers = Profile.objects.filter(subscribers=profile.id)

    context = {
        'title': 'Профиль',
        'user': user,
        'users': Profile.get_users(),
        'followers': followers,
        'groups': groups,
        'subscribers': subscribers,
        'account': account,
        'friend_flag': friend_flag,
        'avatar': avatar
    }
    return render_to_response('profile_detail.html', context)


# Добавление или удаление подписки
@login_required(login_url='/accounts/login/')
def add_or_remove_friends(request):
    if request.is_ajax():
        try:
            user_id = request.POST['user_id']
            action = request.POST['action']
            owner = request.user
            new_friend = User.objects.get(id=user_id)

            if action == "add":
                Profile.make_friend(request, new_friend)
            else:
                Profile.remove_friend(request, new_friend)
        except KeyError:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    else:
        raise Http404


class Edit(FormView):
    @login_required(login_url='/accounts/login/')
    @staticmethod
    def edit_view(request):
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

        form = EditProfile({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'birth_date': user.profile.birth_date,
            'phone': user.profile.phone,
            'description': user.profile.description,
            'gender': user.profile.gender
        })
        form_private = EditUserSettings({
            'messages':
                user.usersettings.messages,
            'birth_date':
                user.usersettings.birth_date,
            'invite':
                user.usersettings.invite,
            'near_invite':
                user.usersettings.near_invite,
        })
        context = {
            'title': 'Профиль',
            'form': form,
            'form_private': form_private,
            "csrf_token": get_token(request),
            'avatar': ProfileAvatar.objects.get(user=request.user.id)
        }
        return render(request, 'profile_edit.html', context)

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
    context = Profile.get_subscribers(request)
    return render(request, 'subscribers.html', context)


def get_followers(request):
    user_id = request.GET.get('user', 1)

    followers = Profile.objects.filter(
        subscribers=User.objects.get(id=user_id).profile.id)

    page = request.GET.get('page', 1)
    paginator = Paginator(followers, 20)
    try:
        followers = paginator.page(page)
    except PageNotAnInteger:
        followers = paginator.page(1)
    except EmptyPage:
        followers = paginator.page(paginator.num_pages)

    context = {'items': followers, 'user_id': user_id, 'action': False}
    return render(request, 'subscribers.html', context)
