from django.conf.urls import url
from custom_profile import views
from custom_profile.models import Profile

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.index, name='index'),
    # url(r'subscri/be/$', Profile.subscribe, name='subscribe'),
]