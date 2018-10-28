import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from chats.models import Room, RoomMembers
from groups.forms import GroupsForm
from groups.models import Group, AllRoles, Membership, GroupAvatar
from images_custom.models import PhotoEditor
from profiles.forms import ImageUploadForm


@login_required(login_url='/accounts/login/')
def detail(request, id):
    context = Group.verification_of_rights(request, id)
    if context['status']:
        group = get_object_or_404(Group, id=id)

        members = Membership.objects.filter(group=group, role__role__in=['admin', 'editor', 'subscribers'])\
            .only('role')

        try:
            roles = Membership.objects.get(person=request.user.profile, group=id).role
        except Membership.DoesNotExist:
            roles = ''

        chat = Room.objects.get(group=group.id)

        context = {
            'roles': roles,
            'group': group,
            'members': members,
            'avatar': GroupAvatar.objects.get(group=group.id),
            'chat': chat,
            'user': request.user
        }
    else:
        return render_to_response('groups/error.html', context)
    return render_to_response('groups/detail.html', context)


# Список всех групп
@login_required(login_url='/accounts/login/')
def view(request):
    is_my = False
    if 'id' in request.GET:  # Если нет id, то ошибка
        user = User.objects.get(id=request.GET['id'])
        if user == request.user:
            is_my = True
    else:
        return  # TODO Придумать как обрабатывать ошибки
    context = {
        'user': user,
        'is_my': is_my
    }
    return render_to_response('groups/view.html', context)


# Получение списка всех групп с последующей фильтрацией
def get_groups(request):
    is_my = False  # Если страница пользователя, то показывать административные поля
    user = request.user  # По умолчанию юзер из реквеста
    # Параметры приходящие постом
    if 'name' in request.POST:
        name = request.POST['name']
    else:
        name = ''

    if 'all' in request.POST:
        groups = Group.objects.filter(name__icontains=name)\
            .only('id', 'name', 'status', ).select_related('groupavatar')
    else:
        groups = Group.objects.filter(membership__person=user.profile, name__icontains=name)\
            .only('id', 'name', 'status', ).select_related('groupavatar')
    # Параметры приходящие постом

    page = request.GET.get('page', 1)
    paginator = Paginator(groups, 20)
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)

    context = {
        'user': user,
        'is_my': is_my,
        'find': name,
        'groups': groups
    }
    return render_to_response('groups/groups_template.html', context)


def get_invite(request):
    if 'id' in request.GET:
        user_id = request.GET['id']
        if int(user_id) == request.user.id:
            Membership.objects.filter(person=request.user.profile)
            members = Membership.objects.filter(person=request.user.profile, role__role__in=['invite', 'send']).order_by(
                'date_joined').select_related('group')
            context = Group.paginator(request, members)
            context.update({'user': request.user})
            return render_to_response('groups/invite_template.html', context)
    else:
        return


@login_required(login_url='/accounts/login/')
def edit(request, id=None):
    if request.method == 'POST':
        form = GroupsForm(request.POST)
        if form.is_valid():
            id = form.save(request)
            return redirect('/groups/' + str(id))
    else:
        group = get_object_or_404(Group, id=id)
        if Group.is_group_admin(request, id):
            context = Group.verification_of_rights(request, id)
            if context['status']:
                form = GroupsForm({
                    'id': id,
                    'name': group.name,
                    'status': group.status,
                    'description': group.description,
                    'type': group.type
                })
            else:
                return render_to_response('groups/error.html', context)
        else:
            context = {'is_not_admin': True}
            return render_to_response('groups/error.html', context)
    try:
        roles = Membership.objects.get(person=request.user.profile, group=id).role
    except Membership.DoesNotExist:
        roles = ''

    #  TODO оптимизировать
    members = Membership.objects.filter(group=group).only('role', 'person').\
        select_related('person__user__profileavatar', 'person__user')

    editors = set()
    subscribers = set()
    invited = set()
    sends = set()
    for member in members:
        if member.role.role == 'editor':
            editors.add(member)
        if member.role.role == 'subscribers':
            subscribers.add(member)
        if member.role.role == 'invite':
            invited.add(member)
        if member.role.role == 'send':
            sends.add(member)

    left_side = editors
    right_side = subscribers

    invited = invited
    sends = sends

    context = {
        'id': id,
        'roles': roles,
        'form': form,
        "csrf_token": get_token(request),
        'left_side': left_side,
        'right_side': right_side,
        'invited': invited,
        'sends': sends,
        'group': group
    }
    return render_to_response('groups/edit.html', context)


@login_required(login_url='/accounts/login/')
def create(request, id=None):
    if request.method == 'POST':
        form = GroupsForm(request.POST)
        if form.is_valid():
            id = form.save(request)
            GroupAvatar.objects.create(group_id=id)
            name = request.POST['name'] + ' - группа'
            Room.objects.create(name=name, creator=request.user, group_id=id)

            return redirect('/groups/' + str(id))
    else:
        form = GroupsForm()

    try:
        roles = Membership.objects.get(person=request.user.profile, group=id).role
    except Membership.DoesNotExist:
        roles = ''

    context = {
        'id': id,
        'roles': roles,
        'form': form,
        "csrf_token": get_token(request),
    }

    return render_to_response('groups/create.html', context)


def subscribe_group(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                group = Group.objects.get(id=request.POST['group_id'])
                action = request.POST['action']
                user = request.user
                if action == "add":
                    room = Room.objects.get(group=group)
                    if not RoomMembers.objects.filter(user_rel=request.user, room_rel=room):
                        RoomMembers.objects.create(user_rel=request.user, room_rel=room)
                        Membership.subscribe(user, group)
                        RoomMembers.invite_message(request.user, room.id, True)
                elif action == 'remove':
                    Membership.unsubscribe(user, group)
                    room = Room.objects.get(group=group)
                    member = RoomMembers.objects.filter(user_rel=request.user,
                                                        room_rel=room)

                    member.delete()
                    RoomMembers.invite_message(request.user, room.id, False)
                else:
                    return HttpResponse(str(400))  # Todo Посмотреть что по статусам
            except KeyError:
                return HttpResponse('Error')
            return HttpResponse(str(200))
        else:
            raise Http404
    else:
        return redirect('/accounts/login')


# Поиск подписчика по имени или фамилии
def find_subscribers(request):
    from django.db.models import Q
    users_object = Membership.objects.filter(Q(person__user__first_name__istartswith=request.POST['value'])
                                             | Q(person__user__last_name__istartswith=request.POST['value']),
                                             group_id=request.POST['group_id'],
                                             role=AllRoles.objects.get(role='subscribers'))
    users = [user for user in users_object]

    context = {
        'users': users
    }
    return render(request, 'includes/select_roles_users.html', context)


# Смена с подписчика на едитора
def add_to_editor(request):
    group_id = request.POST['group_id']
    if Group.is_group_admin(request, group_id):
        try:
            users_object = Membership.objects.get(group_id=group_id,
                                                  person=request.POST['user'],
                                                  role=AllRoles.objects.get(role='subscribers'))
            users_object.role = AllRoles.objects.get(role='editor')
            users_object.save()
        except:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    return HttpResponse('Недостаточно прав для редактирования')


# Смена с едитора на подписчика
def add_to_subscribers(request):
    group_id = request.POST['group_id']
    if Group.is_group_admin(request, group_id):
        try:
            users_object = Membership.objects.get(group_id=group_id,
                                                  person=request.POST['user'],
                                                  role=AllRoles.objects.get(role='editor'))
            users_object.role = AllRoles.objects.get(role='subscribers')
            users_object.save()
        except:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    return HttpResponse('Недостаточно прав для редактирования')


def send_an_application(request):
    if 'group_id' in request.POST:
        group_id = request.POST['group_id']
        if Membership.send_an_application(request.user, group_id):
            return HttpResponse(str(200))
    return HttpResponse(str(400))


def invite(request):
    result = {
        'status': 200,
        'text': '',
        'invalide_name': '',
        'added_array': ''
    }
    if 'group_id' in request.POST:
        group_id = request.POST['group_id']
        if 'added_users' in request.POST:
            added_users = request.POST['added_users']
            added_users = added_users.split(' ')
            added_users.pop()
            for user in added_users:
                if not Membership.invite(user, group_id):
                    result['status'] = '400'
                    result['text'] = 'Внезапная ошибка'
                    return HttpResponse(result)

            result['added_array'] = request.POST['added_users']
            return HttpResponse(json.dumps(result))
        else:
            result['status'] = '400'
            result['text'] = 'Не добавлено ни одного пользователя'
            result['invalide_name'] = 'added_users'
    return HttpResponse(json.dumps(result))


def cancel(request):
    if 'group_id' in request.POST:
        group_id = request.POST['group_id']
        if 'user_id' in request.POST:
            user_id = request.POST['user_id']
            if Membership.cancel(user_id, group_id):
                return HttpResponse(str(200))
    return HttpResponse(str(400))


def accept(request):
    if 'group_id' in request.POST:
        group_id = request.POST['group_id']
        if 'user_id' in request.POST:
            user_id = request.POST['user_id']
            if Membership.accept(user_id, group_id):
                return HttpResponse(str(200))
    return HttpResponse(str(400))


# Удаление подписчика
def delete_subscribers(request):
    group_id = request.POST['group_id']
    if Group.is_group_admin(request, group_id):
        try:
            users_object = Membership.objects.get(group_id=group_id,
                                                  person=request.POST['user'])
            users_object.delete()
        except Membership.DoesNotExist:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    return HttpResponse('Недостаточно прав для редактирования')


# Удаление группы
def delete_group(request):
    group_id = request.POST['group_id']
    if Group.is_group_admin(request, group_id):
        try:
            Group.objects.get(id=group_id).update(active=2)  # TODO Проверить
        except Group.DoesNotExist:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    return HttpResponse('Недостаточно прав для редактирования')


def change_avatar(request):
    if request.method == 'POST' and request.is_ajax():
        return PhotoEditor.load_image(request)
    context = {
        'image_file': ImageUploadForm(),
        'url': request.META['PATH_INFO'],
        'save_url': '/groups/save_image'
    }
    return render(request, 'profiles/change_avatar.html', context)


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
        'save_url': '/groups/save_image'
    }
    return render(request, 'profiles/change_mini.html', context)


def save_image(request):
    if request.method == 'POST' and request.is_ajax():
        model = GroupAvatar.objects.get_or_create(group_id=request.POST['model'])[0]
        return PhotoEditor.save_image(request, model)
