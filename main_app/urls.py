from django.conf.urls import url

from . import views
from profiles.models import Users
from events_.models import EventParty, Event
from events_ import views as event_view

urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'^event_map$', views.event_map, name='event_map'),
     url(r'^get_event_map$', views.get_event_map, name='get_event_map'),
     url(r'signup_check/$', Users.signup_check, name='signup_check'),
     url(r'subscribe_event/$', event_view.subsc_unsubsc, name='subscribe_event'),
     url(r'^get_events/$', Event.get_events, name='get_events'),
     url(r'^get_infinite_events$', views.get_infinite_events, name='get_infinite_events'),
]