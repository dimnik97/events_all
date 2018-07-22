from django.conf.urls import url
from chats import views

urlpatterns = [
    url(r'^$', views.home, name=''),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
