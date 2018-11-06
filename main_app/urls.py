from django.conf.urls import url

from . import views
from profiles.models import Users
from events_.models import Event
from events_ import views as event_view

urlpatterns = [
     url(r'^map$', views.event_map, name='map'),
     url(r'^signup_check/$', Users.signup_check, name='signup_check'),
     url(r'^subscribe_event/$', event_view.subsc_unsubsc, name='subscribe_event'),
     url(r'^get_infinite_events$', views.get_infinite_events, name='get_infinite_events'),
     url(r'^get_events_map$', views.get_events_map, name='get_events_map'),
     # Ленты
     url(r'^get_group_events$', views.get_group_events, name='get_group_events'),  # Лента группы, через view
     url(r'^get_friend_events$', views.get_friend_events, name='get_friend_events'),  # Лента группы, через view
     url(r'^active_user_events$', views.active_user_events, name='active_user_events'),  # Лента активных евентов юзера
     url(r'^ended_user_events$', views.ended_user_events, name='ended_user_events'),  # Лента завершенных евентов юзера
     url(r'^user_events$', views.user_events, name='user_events'),  # Лента всех эвентов пользователя
     url(r'^get_events/$', Event.get_events, name='get_events'),  # Основная лента
     url(r'^get_new_events/$', views.get_new_events, name='get_new_events'),  # получение новых событий
     url(r'^get_new_events_count/$', views.get_new_events_count, name='get_new_events_count'),  # количество новых
     # Ленты
]
