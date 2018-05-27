from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, redirect
from events_.models import Event, EventParty
from custom_profile.models import Users


def index(request):
    if request.user.is_authenticated:

        user_id = request.user.pk
        user = User.objects.get(id=user_id)

        events = Event.get_events()
        events_dict = []

        # todo вынести в отдельную функцию
        for number in range(len(events)):
            current_event = events[number]

            try:
                    EventParty.objects.get(user_id=user, event_id=current_event)

                    events_dict.append({
                        'event': current_event,
                        'party_flag': 1
                    })
            except:
                events_dict.append({
                    'event': current_event,
                    'party_flag': 0
                })

        context = {
            'title': "Лента событий",
            'events': events_dict,
            'user': user,
            'locate': Users.get_user_locations(user_id),
        }

        return render_to_response('index.html', context)
    else:
        return redirect('/accounts/login')
