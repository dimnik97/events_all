from django.conf.urls import url
from custom_profile import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^(?P<id>[0-9]+)$', views.index, name='index')
]