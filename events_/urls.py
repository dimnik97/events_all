from django.conf.urls import url
from events_ import views

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.index, name='index'),
    url(r'edit/(?P<id>[0-9]+)$', views.edit, name='edit'),
    url(r'create$', views.create, name='create'),
]
