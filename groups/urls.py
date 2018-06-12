from django.conf.urls import url
from groups import views

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.detail, name='index'),
    # url(r'edit/(?P<id>[0-9]+)$', views.edit, name='edit'),
    url(r'create$', views.edit_or_create, name='edit_or_create'),
    url(r'edit/(?P<id>[0-9]+)$', views.edit_or_create, name='edit_or_create'),
]
