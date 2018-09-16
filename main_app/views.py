from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from events_.models import Event, EventParty
from profiles.models import Users


def index(request):
    if request.user.is_authenticated:

        user_id = request.user.pk
        user = User.objects.get(id=user_id)

        location = 1 # Заглушка
        # events = Event.get_events()
        # events_dict = []

        # todo вынести в отдельную функцию
        # for number in range(len(events)):
        #     current_event = events[number]
        #
        #     try:
        #             EventParty.objects.get(user_id=user, event_id=current_event)
        #
        #             events_dict.append({
        #                 'event': current_event,
        #                 'party_flag': 1
        #             })
        #     except:
        #         events_dict.append({
        #             'event': current_event,
        #             'party_flag': 0
        #         })

        context = {
            'title': "Лента событий",
            # 'events': events_dict,
            'user': user,
            'locate': Users.get_user_locations(user_id),
        }

        return render_to_response('index.html', context)
    else:
        return redirect('/accounts/login')


def get_infinite_events(request):

    category = request.GET.get('cat', None);
    events = Event.get_events(category)

    page = request.GET.get('page', 1)
    paginator = Paginator(events, 20)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    context = {'events': events, 'action': False}
    return render(request, 'event_item.html', context)
