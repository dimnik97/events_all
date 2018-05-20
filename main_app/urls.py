from django.conf.urls import url

from . import views
from custom_profile.models import Users
from events_.models import EventParty
from events_ import views as event_view

urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'signup_check/$', Users.signup_check, name='signup_check'),
     url(r'subscribe_event/$', event_view.subsc_unsubsc, name='subscribe_event'),
]