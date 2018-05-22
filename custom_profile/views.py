from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.middleware.csrf import get_token

from custom_profile.forms import Edit_profile
from custom_profile.models import Profile, Subscribers, ProfileAvatar
from django.shortcuts import get_object_or_404, render_to_response


def index(request, id):
    account = None
    if request.user.is_authenticated:
        account = request.user.id  # Залогиненный пользователь
    user = get_object_or_404(User, id=id)  # Отвечает за юзера, который отобразится в профиле

    avatar, created = ProfileAvatar.objects.get_or_create(user=user)

    friend_flag = 'add'
    try:
        if Subscribers.objects.filter(users=user.profile, current_user=request.user.profile):
            friend_flag = 'remove'
    except:
        friend_flag = 'add'

    friend_object, created = Subscribers.objects.get_or_create(current_user=user)
    friends = [friend for friend in friend_object.users.all() if friend != user]

    context = {
        'title': 'Профиль',
        'user': user,
        'users': Profile.get_users(),
        'friends': friends,
        'account': account,
        'friend_flag': friend_flag,
        'avatar': avatar
    }
    return render_to_response('user_profile.html', context)


# Добавление или удаление подписки
@login_required
def add_or_remove_friends(request):
    if request.is_ajax():
        try:
            user_id = request.POST['user_id']
            action = request.POST['action']
            owner = request.user
            new_friend = User.objects.get(id=user_id)

            if action == "add":
                Subscribers.make_friend(owner, new_friend)
            else:
                Subscribers.remove_friend(owner, new_friend)
        except KeyError:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    else:
        raise Http404


def edit(request):
    if request.method == 'POST':
        form = Edit_profile(request.POST)
        if form.is_valid():
            Edit_profile.save_model()
            pass  # does nothing, just trigger the validation
    else:
        # BookFormSet = inlineformset_factory(User, Profile, fields=('title',))
        # user = request.user
        user = request.user
        form = Edit_profile({'first_name': user.first_name,
                             'last_name': user.last_name,
                             'email': user.email,
                             'birth_date': user.profile.birth_date,
                             'phone': user.profile.phone
                             })

    context = {
        'title': 'Профиль',
        'form': form,
        "csrf_token": get_token(request),
        'avatar': ProfileAvatar.objects.get(user=request.user.id)
    }
    return render_to_response('edit.html', context)
