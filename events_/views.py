import json
import os
from os import path as op
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, render_to_response, render, redirect
from django.template.loader import render_to_string

from cities_.models import CityTable
from events_.forms import EventForm, CreateEventNews
from events_all.helper import parse_from_error_to_json
from groups.models import Group
from images_custom.models import PhotoEditor
from profiles.forms import ImageUploadForm
from .models import Event, Event_avatar, EventNews, EventMembership, EventCategory, EventLikes, EventViews


def index(request, id):
    event_id = id
    event_detail = get_object_or_404(Event, id=event_id)  # Получение эвента
    if request.user.is_authenticated:
        user = request.user  # Получение юзера
    else:
        user = False

    if user != event_detail.creator_id:
        if int(event_detail.active) == 3:
            context = {
                'error': 'Событие удалено'
            }
            return render_to_response('events_/detail.html', context)

        if int(event_detail.active) == 4:
            context = {
                'error': 'Событие заблокировано'
            }
            return render_to_response('events_/detail.html', context)

    categories = event_detail.category.all()

    # Права на редактирование
    is_creator = False
    if event_detail.creator_id == user and user is not False:
        is_creator = True

    is_editor = False
    if event_detail.created_by_group:
        is_editor = Group.is_editor(request, event_detail.created_by_group.id)
    # Права на редактирование

    party_flag = '',  # если пользователь уже подписан на выбранное событие
    if not is_creator and user is not False:
        try:
            if EventMembership.objects.get(person=user.profile, event=event_detail):
                party_flag = True
        except EventMembership.DoesNotExist:
            party_flag = False

    if int(event_detail.active) == 2 and party_flag is False:
        context = {
            'error': 'Зыкрытое событие, нет доступа'
        }
        return render_to_response('events_/detail.html', context)

    subscribers = EventMembership.objects.filter(event=event_detail)[:5]

    news = EventNews.objects.filter(news_event=event_detail).order_by('-create_time')
    form = CreateEventNews()

    can_change_news = False
    if is_creator or is_editor:
        can_change_news = True

    try:
        EventViews.objects.create(event=event_detail, user=None if user is False else user)  # Проставляем просмотры
    except:
        pass

    context = {
        'news_form': form,
        'title': 'Профиль',
        'user': user,
        'event': event_detail,
        'subscribers': subscribers,
        'party_flag': party_flag,
        'is_creator': is_creator,
        'is_editor': is_editor,
        "csrf_token": get_token(request),
        "news": render_to_string('events_/news.html', {'news': news, 'can_change_news': can_change_news}),
        'categories': categories,
        'error': False,
        'active': event_detail.active
    }

    if 'is_card_on_event_map' in request.GET:
        return HttpResponse(json.dumps(render_to_string('events_/card.html', context)))
    else:
        return render_to_response('events_/detail.html', context)


def subsc_unsubsc(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                event = Event.objects.get(id=request.POST['event_id'])
                action = request.POST['action']
                user = request.user

                if action == "subscribe":
                    EventMembership.subscribe(event, user)
                else:
                    EventMembership.unsubscribe(event, user)
            except Event.DoesNotExist:
                return HttpResponse('Error')
            return HttpResponse(str(200))
        else:
            raise Http404
    else:
        return HttpResponse(str(401))  # Не авторизован


@login_required(login_url='/accounts/login/')
def change_avatar(request):
    if request.method == 'POST' and request.is_ajax():
        return PhotoEditor.load_image(request)
    context = {
        'image_file': ImageUploadForm(),
        'avatar': Event_avatar.objects.get(user=request.user.id),
        'url': request.META['PATH_INFO'],
        'save_url': '/profile/save_image'
    }
    return render(request, 'profiles/change_avatar.html', context)


@login_required(login_url='/accounts/login/')
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
    return render(request, 'profiles/change_mini.html', context)


@login_required(login_url='/accounts/login/')
def edit(request, id, group_id=None):
    user = request.user
    try:
        user_city = request.user.profile.location
    except:
        user_city = CityTable.objects.get(city='Москва')
    event = get_object_or_404(Event, id=id)
    if event.creator_id == user:
        if request.method == 'POST':
            form = EventForm(request.POST, request.FILES, request.GET)
            if form.is_valid():
                result = form.save(request)
                if result['status'] == 200 or result['status'] == 400:
                    return HttpResponse(json.dumps(result))
            else:
                data = parse_from_error_to_json(request, form)
                return HttpResponse(json.dumps(data))
        else:
            user_city = event.location
            form = EventForm({'id': event.id,
                              'name': event.name,
                              'description': event.description,
                              'start_time': event.start_time,
                              'end_time': event.end_time,
                              'active': event.active
                              })

        avatar = Event_avatar.objects.get(event=event)
        city_list = CityTable.objects.filter(city__isnull=False).values('city', 'city_id').order_by('city')
        categories = EventCategory.objects.all()
        selected_categories = event.category.all()

        context = {
            'title': 'Редактирование события',
            'form': form,
            "csrf_token": get_token(request),
            'avatar': avatar,
            'city_list': city_list,
            'user_city': user_city,
            'geo_point': event.geo_point,
            'categories': list(set(categories) - set(selected_categories)),
            'selected_categories': selected_categories,
            'active': event.active,
            'id': event.id
        }

        return render_to_response('events_/edit.html', context)
    raise Http404


@login_required(login_url='/accounts/login/')
def create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, request.GET)
        if form.is_valid():
            result = form.save(request, 1)  # 1 - флаг создания
            if result['status'] == 200:
                return HttpResponse(json.dumps(result))
            return HttpResponse(json.dumps(result))
        else:
            data = parse_from_error_to_json(request, form)
            return HttpResponse(json.dumps(data))
    else:
        form = EventForm()

    try:
        user_city = request.user.profile.location
    except:
        user_city = CityTable.objects.get(city='Москва')
    categories = EventCategory.objects.all()

    context = {
        'title': 'Создание события',
        'form': form,
        "csrf_token": get_token(request),
        'city_list': CityTable.all_city_exclude_user_city(user_city),
        'user_city': user_city,
        'categories': categories,
        'user': request.user
    }
    return render_to_response('events_/create.html', context)


@login_required(login_url='/accounts/login/')
def change_default_image(request):
    result = {
        'image': 'default.png',
        'image_names': ['default'] * 3
    }
    if 'json' in request.POST:
        json_items = json.loads(request.POST['json'])
        categories = []
        file_names = []
        for key in json_items:
            categories.append(key)
            file_names.append(json_items[key])

        if len(json_items) == 1:
            try:
                open(op.join('media', 'avatar_event_default', categories[0], file_names[0] + '.png'))
                result['image'] = op.join(categories[0], file_names[0] + '.png')
                result['image_names'][0] = file_names[0]
                return HttpResponse(json.dumps(result))
            except IOError:
                return HttpResponse(json.dumps(result))

        file_name = ''
        i = 0
        for name in file_names:
            result['image_names'][i] = name
            file_name = file_name + '_' + name
            i = i + 1

        file_name = file_name + '.png'
        try:
            open(op.join('media', 'avatar_event_default', 'general', file_name))
            result['image'] = op.join('general', file_name)
            result['image_names'][0] = file_names[0]
            return HttpResponse(json.dumps(result))
        except IOError:
            if len(categories) == 2:
                result = PhotoEditor.create_image_for_two_categories(categories, file_name, file_names)
                return HttpResponse(json.dumps(result))
            if len(categories) == 3:
                result = PhotoEditor.create_image_for_three_categories(categories, file_name, file_names)
                return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(json.dumps(result))


@login_required(login_url='/accounts/login/')
def get_images_by_categories(request):   # TODO Вынести в класс работы с изображениями
    if 'categories' in request.POST:
        category = request.POST['categories']
        directory = op.join('media', 'avatar_event_default', category)
        files = os.listdir(directory)

        file_list = list()
        for file in files:
            if os.path.splitext(file)[1] == '.png' or os.path.splitext(file)[1] == '.jpg' or os.path.splitext(file)[1] == '.svg':
                file_list.append(op.join('media', 'avatar_event_default', category, file))
        return HttpResponse(json.dumps(file_list))
    return HttpResponse('error')


def get_subscribers(request):
    context = EventMembership.get_subscribers(request)
    if not context['flag']:
        return render(request, 'profiles/subscribers.html', context)
    else:
        return render(request, 'profiles/search_subscribers_items.html', context)


# Восстановить или удалить событие
def delete_event(request):
    event_id = request.POST['event_id']
    is_restore = request.POST['is_restore']
    try:
        event = Event.objects.get(id=event_id)
        if request.user != event.creator_id:
            return HttpResponse('Недостаточно прав для редактирования')
        if is_restore == 'true':
            event.active = '1'
        else:
            event.active = '3'
        event.save()
        return HttpResponse(str(200))
    except Event.DoesNotExist:
        return HttpResponse('Error')


# Восстановить или удалить событие
def create_news(request):
    if request.method == 'POST':
        form = CreateEventNews(request.POST, request.FILES, request.GET)
        if form.is_valid():
            return EventNews.check_rights_and_create_news(request, form)  # Вынес, чтобы не захлямлять вьюху
    raise Http404

# Удаление новостей событий
def delete_event_news(request):
    if 'event_id' in request.POST:
        event_detail = get_object_or_404(Event, id=request.POST['event_id'])  # Получение эвента
        try:
            if event_detail.creator_id == request.user:
                EventNews.objects.get(id=request.POST['news_id']).delete()
                return HttpResponse(200)
            is_editor = False
            if event_detail.created_by_group:
                is_editor = Group.is_editor(request, event_detail.created_by_group.id)
            if is_editor == 1:
                EventNews.objects.get(id=request.POST['news_id']).delete()
                return HttpResponse(200)
        except EventNews.DoesNotExist:
            return HttpResponse(400)
        raise Http404


def edit_news(request):
    if 'event_id' in request.POST and 'news_id' in request.POST:
        event_detail = get_object_or_404(Event, id=request.POST['event_id'])  # Получение эвента
        form = CreateEventNews(request.POST, request.FILES, request.GET)

        try:
            if event_detail.creator_id == request.user:
                form.save(request, event_detail)
                return HttpResponse(200)
            is_editor = False
            if event_detail.created_by_group:
                is_editor = Group.is_editor(request, event_detail.created_by_group.id)
            if is_editor == 1:
                form.save(request, event_detail)
                return HttpResponse(200)
        except EventNews.DoesNotExist:
            return HttpResponse(400)
    raise Http404


# Простановка лайка (добавление в закладки)
def like(request):
    try:
        EventLikes.objects.create(event_id=request.POST['event_id'], user=request.user)
        return HttpResponse(200)
    except:
        return HttpResponse(400)


# Удаляем лайк (удаление из закладки)
def unlike(request):
    try:
        EventLikes.objects.get(event_id=request.POST['event_id'], user=request.user).delete()
        return HttpResponse(200)
    except:
        return HttpResponse(400)
