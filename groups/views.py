from PIL import Image
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
import os

from groups.forms import GroupsForm
from groups.models import Group, GroupSubscribers, AllRoles


class Vehicle(object):
    pass


@login_required(login_url='/accounts/login/')
def detail(request, id):
    try:
        group = Group.objects.get(id=id)
    except Group.DoesNotExist:
        # Написать сюда 404
        pass

    try:
        roles = GroupSubscribers.objects.get(user_id=request.user, group_id=id).role
    except GroupSubscribers.DoesNotExist:
        roles = AllRoles.objects.get(id=3)

    context = {
        'roles': roles,
        'group': group
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
                'description': group.description,
                'type': group.type
            })
        else:
            form = GroupsForm()

    try:
        roles = GroupSubscribers.objects.get(user_id=request.user, group_id=id).role
    except GroupSubscribers.DoesNotExist:
        roles = AllRoles.objects.get(id=3)

    context = {
        'roles': roles,
        'form': form,
        "csrf_token": get_token(request),
    }
    return render_to_response('group_edit_or_create.html', context)


def subscribe_group(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                event = Group.objects.get(id=request.POST['group_id'])
                action = request.POST['action']
                user = request.user.id
                if action == "subscribe":
                    GroupSubscribers.subscribe(event, user)
                else:
                    GroupSubscribers.unsubscribe(event, user)
            except KeyError:
                return HttpResponse('Error')
            return HttpResponse(str(200))
        else:
            raise Http404
    else:
        return redirect('/accounts/login')



    # i = 1
    # while i < 25:
    #     u = 'Cтаромонетный 18 кв 38_190,6 кв.м (ЖК Времена года)'
    #
    #     www = '/Users/dmitrij/Downloads/Для нового сайта RICCI/ВТОРИЧКА/Фото/' + u
    #
    #     stingr = www + '/' + str(i) + '.jpeg'
    #     try:
    #         os.mkdir(www + '_')
    #     except:
    #         pass
    #
    #     try:
    #         img = Image.open(stingr)
    #     except:
    #         img = Image.open(www + '/' + str(i) + '.jpg')
    #
    #     height = img.height
    #     width = img.width
    #
    #     max_width = 3500
    #     max_height = 3500
    #     if width >= max_width or height >= max_height:
    #         correlation = width / height
    #         height = width / correlation
    #         width = max_width
    #
    #         img.thumbnail(
    #             (width, height),
    #             Image.ANTIALIAS
    #         )
    #     quality_val = 85
    #     reduced = www + '_/' + str(i) + '.JPG'
    #     img.save(reduced, quality=quality_val, optimize=True, progressive=True)
    #
    #     i = i + 1
