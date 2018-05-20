from django.conf.urls import url
from events_ import views

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.index, name='index'),
]
