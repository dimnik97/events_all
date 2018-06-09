from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, render_to_response


@login_required(login_url='/accounts/login/')
def detail(request, id):
    # user = get_object_or_404(Group, id=id)
    #
    # avatar, created = ProfileAvatar.objects.get_or_create(user=user)
    #
    # friend_flag = 'add'
    # try:
    #     if Subscribers.objects.filter(users=user.profile, current_user=request.user.profile):
    #         friend_flag = 'remove'
    # except:
    #     friend_flag = 'add'
    #
    # friend_object, created = Subscribers.objects.get_or_create(current_user=user)
    # friends = [friend for friend in friend_object.users.all() if friend != user]

    # context = {
    #     'title': 'Профиль',
    #     'user': user,
    #     'users': Profile.get_users(),
    #     'friends': friends,
    #     'account': account,
    #     'friend_flag': friend_flag,
    #     'avatar': avatar
    # }
    context = {}
    return render_to_response('user_profile.html', context)
