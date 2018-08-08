from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, render_to_response, redirect

from chats.models import Room, ChatMessage, RoomMembers
from groups.forms import GroupsForm
from groups.models import Group, AllRoles, Membership, GroupAvatar
from images_custom.models import PhotoEditor
from profiles.forms import ImageUploadForm


@login_required(login_url='/accounts/login/')
def detail(request, id):
    context = Group.verification_of_rights(request, id)
    if context['status']:
        group = get_object_or_404(Group, id=id)

        members_object = group.members.select_related()
        members = [member for member in members_object.all()]

        try:
            roles = Membership.objects.get(person=request.user.profile, group=id).role
        except Membership.DoesNotExist:
            roles = ''

        context = {
            'roles': roles,
            'group': group,
            'members': members,
            'avatar': GroupAvatar.objects.get(group=group.id)
        }
    else:
        return render_to_response('error_page.html', context)
    return render_to_response('detail_group.html', context)


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
                return render_to_response('error_page.html', context)
        else:
            context = {'is_not_admin': True}
            return render_to_response('error_page.html', context)
    try:
        roles = Membership.objects.get(person=request.user.profile, group=id).role
    except Membership.DoesNotExist:
        roles = ''

    editors_object = Membership.objects.filter(group=group, role=AllRoles.objects.get(role='editor'))
    editors = [editor for editor in editors_object.all()]

    members_object = Membership.objects.filter(group=group, role=AllRoles.objects.get(role='subscribers'))
    members = [member for member in members_object.all()]

    left_side = editors
    right_side = members

    context = {
        'id': id,
        'roles': roles,
        'form': form,
        "csrf_token": get_token(request),
        'left_side': left_side,
        'right_side': right_side,
        'group': group
    }
    return render_to_response('edit_group.html', context)


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

    return render_to_response('create_group.html', context)


def subscribe_group(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                group = Group.objects.get(id=request.POST['group_id'])
                action = request.POST['action']
                user = request.user
                if action == "add":
                    room = Room.objects.get(group=group)
                    RoomMembers.objects.create(user_rel=request.user, room_rel=room)
                    Membership.subscribe(user, group)
                    RoomMembers.invite_message(request.user, room, True)
                elif action == 'remove':
                    Membership.unsubscribe(user, group)
                    room = Room.objects.get(group=group)
                    member = RoomMembers.objects.get(user_rel=request.user,
                                                     room_rel=room)  # TODO Придумать как ограничить доступ к чатам

                    member.delete()
                    RoomMembers.invite_message(request.user, room, False)
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


def invite_group(request):
    group_id = request.POST['group_id']


# Удаление подписчика
def delete_subscribers(request):
    group_id = request.POST['group_id']
    if Group.is_group_admin(request, group_id):
        try:
            users_object = Membership.objects.get(group_id=group_id,
                                                  person=request.POST['user'])
            users_object.delete()
        except:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    return HttpResponse('Недостаточно прав для редактирования')


# Удаление группы
def delete_group(request):
    group_id = request.POST['group_id']
    if Group.is_group_admin(request, group_id):
        try:
            group_object = Group.objects.get(id=group_id)
        except:
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
    return render(request, 'change_avatar.html', context)


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
    return render(request, 'change_mini.html', context)


def save_image(request):
    if request.method == 'POST' and request.is_ajax():
        model = GroupAvatar.objects.get_or_create(group_id=request.POST['model'])[0]
        return PhotoEditor.save_image(request, model)
