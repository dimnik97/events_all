from django.conf.urls import url

from . import views
from custom_profile.models import Users
from events_.models import EventParty

urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'signup_check/$', Users.signup_check, name='signup_check'),
     url(r'subscribe_event/$', EventParty.subscribe_event, name='subscribe_event'),
     # url(r'unsubscribe_event/$', EventParty.unsubscribe_event, name='unsubscribe_event'),
]