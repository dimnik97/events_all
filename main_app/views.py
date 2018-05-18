from django.shortcuts import render_to_response, get_object_or_404
from events_.models import Event, EventParty
from custom_profile.models import Users, Profile

def index(request):
    user_id = request.user.pk
    events = Event.get_events()
    events_dict = []

    # todo вынести в отдельную функцию
    for number in range(len(events)):
        try:

            # prof_id = Profile.objects.get(id=request.user.id).id
            current_event_id = events[number].id
            EventParty.objects.get(user_id=request.user.id, event_id=current_event_id)

            events_dict.append({
                'event': events[number],
                'party_flag': 1
            })

        except:
            events_dict.append({
                'event': events[number],
                'party_flag': 0
            })

    context = {
        'title': "Лента событий",

        'events': events_dict,


        'user': Users.get_user(user_id),
        'locate': Users.get_user_locations(user_id),
        # 'user_url': Users.get_absolute_url(user_id)
    }

    # events = Event.get_events()
    # "events": events
    return render_to_response('index.html', context)
