from django.conf.urls import url
from groups import views

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.detail, name='views'),
    url(r'create$', views.create, name='edit_or_create'),
    url(r'edit/(?P<id>[0-9]+)$', views.edit, name='edit_or_create'),
    url(r'subscribe_group/$', views.subscribe_group, name='subscribe_group'),
    url(r'^change_avatar', views.change_avatar, name='change_avatar'),
    url(r'^change_mini', views.change_mini, name='change_mini'),
    url(r'^save_image', views.save_image, name='save_image'),

    url(r'^find_subscribers$', views.find_subscribers, name='find_subscribers'),
    url(r'^invite_group', views.invite_group, name='invite_group'),
    url(r'^add_to_editor', views.add_to_editor, name='add_to_editor'),
    url(r'^add_to_subscribers', views.add_to_subscribers, name='add_to_subscribers'),
    url(r'^delete_subscribers', views.delete_subscribers, name='delete_subscribers'),
    url(r'^delete_group', views.delete_group, name='delete_group'),
]
