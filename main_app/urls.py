from django.conf.urls import url

from . import views
from accounts.models import Users

urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'signup_check/$', Users.signup_check, name='signup_check'),
]