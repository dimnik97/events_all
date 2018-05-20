from django.conf.urls import url
from custom_profile import views

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.index, name='index'),
    url(r'^edit$', views.edit, name='edit'),
    url(r'add_or_remove_friends/$', views.add_or_remove_friends, name='add_or_remove_friends'),
]