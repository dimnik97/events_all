from django.conf.urls import url
from chats import views

urlpatterns = [
    url(r'^$', views.home, name=''),
    url(r'^peer', views.home, name='peer'),
    url(r'^room', views.home, name='room'),
    url(r'^dlg', views.room, name='dlg'),
    url(r'^create_room$', views.create_room, name='dlg'),
    url(r'^join_room$', views.join_room, name='dlg'),
    url(r'^decline_room$', views.decline_room, name='dlg'),
]
