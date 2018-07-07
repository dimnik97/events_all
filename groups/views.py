from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from groups.forms import GroupsForm
from groups.models import Group, AllRoles, Membership
from images_custom.models import PhotoEditor
from profiles.forms import ImageUploadForm


@login_required(login_url='/accounts/login/')
def detail(request, id):
    try:
        group = Group.objects.get(id=id)
    except Group.DoesNotExist:
        # Написать сюда 404
        pass

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
    }
    return render_to_response('group_detail.html', context)


@login_required(login_url='/accounts/login/')
def edit_or_create(request, id=None):
    if request.method == 'POST':
        form = GroupsForm(request.POST)
        if form.is_valid():
            id = form.save(request)
            print('save')
            return redirect('/groups/' + str(id))
    else:
        if id:
            group = get_object_or_404(Group, id=id)
            form = GroupsForm({
                'id': id,
                'name': group.name,
                'status': group.status,
                'description': group.description,
                'type': group.type
            })
        else:
            form = GroupsForm()

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

    return render_to_response('group_edit_or_create.html', context)


def subscribe_group(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                group = Group.objects.get(id=request.POST['group_id'])
                action = request.POST['action']
                user = request.user
                if action == "add":
                    Membership.subscribe(user, group)
                elif action == 'remove':
                    Membership.unsubscribe(user, group)
                else:
                    return HttpResponse(str(400))  # Todo Посмотреть что по статусам
            except KeyError:
                return HttpResponse('Error')
            return HttpResponse(str(200))
        else:
            raise Http404
    else:
        return redirect('/accounts/login')


def select_roles(request):
    # TODO Сменить жесткую привязку
    id = 5

    try:
        group = Group.objects.get(id=id)
    except Group.DoesNotExist:
        # TODO заполнить
        pass
    # TODO Сменить жесткую привязку

    editors_object = Membership.objects.filter(group=group, role=AllRoles.objects.get(role='editor'))
    editors = [editor for editor in editors_object.all()]

    members_object = Membership.objects.filter(group=group, role=AllRoles.objects.get(role='subscribers'))
    members = [member for member in members_object.all()]

    left_side = editors
    right_side = members
    context = {
        'left_side': left_side,
        'right_side': right_side,
        'group': group
    }
    return render_to_response('includes/select_roles.html', context)


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


def add_to_editor(request):
    try:
        users_object = Membership.objects.get(group_id=request.POST['group_id'],
                                              person=request.POST['user'],
                                              role=AllRoles.objects.get(role='subscribers'))
        users_object.role = AllRoles.objects.get(role='editor')
        users_object.save()
    except:
        return HttpResponse('Error')
    return HttpResponse(str(200))


def add_to_subscribers(request):
    try:
        users_object = Membership.objects.get(group_id=request.POST['group_id'],
                                              person=request.POST['user'],
                                              role=AllRoles.objects.get(role='editor'))
        users_object.role = AllRoles.objects.get(role='subscribers')
        users_object.save()
    except:
        return HttpResponse('Error')
    return HttpResponse(str(200))


def delete_subscribers(request):
    try:
        users_object = Membership.objects.get(group_id=request.POST['group_id'],
                                              person=request.POST['user'])
        users_object.delete()
    except:
        return HttpResponse('Error')
    return HttpResponse(str(200))


def change_avatar(request):
    if request.method == 'POST' and request.is_ajax():
        return PhotoEditor.load_image(request)
    context = {
        'image_file': ImageUploadForm(),
        'url': request.META['PATH_INFO'],
        'save_url': '/profile/save_image'
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
        'save_url': '/profile/save_image'
    }
    return render(request, 'change_mini.html', context)


def save_image(request):
    if request.method == 'POST' and request.is_ajax():
        model = request.user.profileavatar
        return PhotoEditor.save_image(request, model)
