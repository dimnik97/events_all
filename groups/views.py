from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, render_to_response, redirect

from events_all import helper
from groups.forms import GroupsForm
from groups.models import Group, AllRoles, Membership


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
        roles = AllRoles.objects.get(id=3)

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
        roles = AllRoles.objects.get(role='subscribers')

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
                # if action == "subscribe":
                #     GroupSubscribers.subscribe(event, user)
                # else:
                #     GroupSubscribers.unsubscribe(event, user)
            except KeyError:
                return HttpResponse('Error')
            return HttpResponse(str(200))
        else:
            raise Http404
    else:
        return redirect('/accounts/login')