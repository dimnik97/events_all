from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from custom_profile.models import Profile, Subscribers
from django.shortcuts import get_object_or_404, render_to_response


def index(request, id):
    user = get_object_or_404(User, id=id)
    friend_object, created = Subscribers.objects.get_or_create(current_user=request.user.profile)
    friends = [friend for friend in friend_object.users.all() if friend != request.user.profile]

    context = {
        'title': 'Профиль',
        'user': user,
        'users': Profile.get_users(),
        "friends": friends
    }
    return render_to_response('user_profile.html', context)

@login_required
def add_or_remove_friends(request):
    user_id = request.POST['user_id']
    verb = request.POST['verb']
    n_f = get_object_or_404(User, id=user_id)
    owner = request.user.profile
    new_friend = Profile.objects.get(user=n_f)

    if verb == "add":
        # new_friend.followers.add(owner)
        Subscribers.make_friend(owner, new_friend)
    else:
        # new_friend.followers.remove(owner)
        Subscribers.remove_friend(owner, new_friend)

    return Subscribers(new_friend.get_absolute_url())
