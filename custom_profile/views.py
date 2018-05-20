from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404

from custom_profile.models import Profile, Subscribers
from django.shortcuts import get_object_or_404, render_to_response


def index(request, id):
    user = get_object_or_404(User, id=id)
    # friend_object, created = Subscribers.objects.get_or_create(current_user=request.user.userprofile)
    # friends = [friend for friend in friend_object.users.all() if friend != request.user.userprofile]
    account = None
    if request.user.is_authenticated:
        account = request.user.id  # Залогиненный пользователь
    user = get_object_or_404(User, id=id)  # Отвечает за юзера, который отобразится в профиле

    friend_flag = 'add'
    try:
        if Subscribers.objects.filter(users=user.profile, current_user=request.user.profile):
            friend_flag = 'remove'
    except:
        friend_flag = 'add'

    friend_object, created = Subscribers.objects.get_or_create(current_user= user.profile)
    friends = [friend for friend in friend_object.users.all() if friend != user.profile]

    context = {
        'title': 'Профиль',
        'user': user,
        'users': Profile.get_users(),
        'friends': friends,
        'account': account,
        'friend_flag': friend_flag
    }
    return render_to_response('user_profile.html', context)


# Добавление или удаление подписки
@login_required
def add_or_remove_friends(request):
    if request.is_ajax():
        try:
            user_id = request.POST['user_id']
            action = request.POST['action']
            n_f = get_object_or_404(User, id=user_id)
            owner = request.user.profile
            new_friend = Profile.objects.get(user=n_f)

            if action == "add":
                Subscribers.make_friend(owner, new_friend)
            else:
                Subscribers.remove_friend(owner, new_friend)
        except KeyError:
            return HttpResponse('Error')
        return HttpResponse(str(200))
    else:
        raise Http404
