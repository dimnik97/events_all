from django.conf.urls import url

from . import views
from custom_profile.models import Users

urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'signup_check/$', Users.signup_check, name='signup_check'),
]