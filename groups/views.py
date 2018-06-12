from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.shortcuts import render, get_object_or_404, render_to_response

from groups.forms import GroupsForm
from groups.models import Group


@login_required(login_url='/accounts/login/')
def detail(request, id):
    context = {}
    return render_to_response('detail.html', context)


@login_required(login_url='/accounts/login/')
def edit_or_create(request, id=None):
    if request.method == 'POST':
        form = GroupsForm(request.POST)
        if form.is_valid():
            form.save(request)
            print('save')
    else:
        if id:
            group = Group.objects.get_object_or_404(id=id)
            form = GroupsForm(group)
        else:
            form = GroupsForm()

    context = {
        'form': form,
        "csrf_token": get_token(request),
    }
    return render_to_response('edit_or_create.html', context)
