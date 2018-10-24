import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.template.loader import render_to_string
from django.views.generic import FormView

from cities_.models import CityTable
from groups.models import Group
from images_custom.models import PhotoEditor
from profiles.forms import ImageUploadForm
from profiles.models import Profile, ProfileAvatar, Users
from django.shortcuts import get_object_or_404, render_to_response, render, redirect


# Редирект на аккаунт пользователя
@login_required(login_url='/accounts/login/')
def my_profile(request):
    url = '/profile/' + str(request.user.id)
    return redirect(url)


@login_required(login_url='/accounts/login/')
def detail(request, id):
    account = request.user.id  # Залогиненный пользователь
    user = get_object_or_404(User, id=id)  # Отвечает за юзера, который отобразится в профиле

    avatar, created = ProfileAvatar.objects.get_or_create(user=user)

    subscribers_object = user.profile.subscribers
    profile = user.profile

    subscribers = [
        User.objects.get(id=subscriber.user_id)
        for subscriber in subscribers_object.all().select_related("user__profileavatar").only(
            "user__first_name", 'user__last_name', 'user_id')[:5] if subscriber != profile
    ]

    groups_count = Group.objects.filter(membership__person=profile).count()

    if Profile.objects.filter(user=account, subscribers=profile).exists():
        friend_flag = 'remove'
    else:
        friend_flag = 'add'

    followers = Profile.objects.filter(subscribers=profile.id).select_related("user__profileavatar").only(
        "user__first_name", 'user__last_name', 'user_id')[:5]

    from django.utils import timezone

    if (timezone.now() - user.profile.last_activity).seconds > 1800:
        is_online = 'Последний раз в сети ' + str(user.profile.last_activity)
    elif (timezone.now() - user.profile.last_activity).seconds > 900:
        is_online = 'Последний раз в сети менее 15 минут назад'
    else:
        is_online = 'online'

    context = {
        'is_online': is_online,
        'title': 'Профиль',
        'user': user,
        'users': Profile.objects.all().select_related("user__profileavatar").only("user__first_name", 'user__last_name', 'user_id'),
        'followers': followers,
        'groups_count': groups_count,
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
            if user_id != request.user.id:
                action = request.POST['action']
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
    context = Profile.get_subscribers(request)
    if not context['flag']:
        return render(request, 'subscribers.html', context)
    else:
        return render(request, 'search_subscribers_items.html', context)


def get_followers(request):
    user_id = request.GET.get('user', 1)
    flag = False

    if 'value' in request.POST and 'search' in request.POST:
        # TODO Тут ошибка, знаю, надо доделать, не работает паджинация
        from django.db.models import Q
        user = User.objects.get(id=user_id)
        followers = Profile.objects.filter(Q(user__first_name__istartswith=request.POST['value'])
                                           | Q(user__last_name__istartswith=request.POST['value']),
                                           subscribers=user.profile)
        flag = True
    else:
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

    context = {'items': followers, 'user_id': user_id, 'action': False, 'type': 'followers'}
    if not flag:
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
