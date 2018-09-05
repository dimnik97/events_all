from django.conf.urls import url
from chats import views

urlpatterns = [
    url(r'^$', views.home, name=''),
    url(r'^peer', views.home, name='peer'),
    url(r'^room', views.home, name='room'),
    url(r'^dlg', views.room, name='dlg'),
    url(r'^read_message', views.read_message, name='read_message'),
    url(r'^get_dialogs', views.get_dialogs, name='get_dialogs'),
    url(r'^get_messages', views.get_messages, name='get_messages'),
    url(r'^create_room$', views.create_room, name='create_room'),
    url(r'^add_user_to_room$', views.add_user_to_room, name='add_user_to_room'),
    url(r'^join_room$', views.join_room, name='join_room'),
    url(r'^decline_room$', views.decline_room, name='decline_room'),
    url(r'^remove_user_from_room$', views.remove_user_from_room, name='remove_user_from_room'),
    url(r'^delete_message', views.delete_message, name='delete_message'),
]
