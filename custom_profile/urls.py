from django.conf.urls import url
from custom_profile import views, forms

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.index, name='index'),
    url(r'^edit$', views.Edit.edit_view, name='edit'),
    url(r'add_or_remove_friends/$', views.add_or_remove_friends, name='add_or_remove_friends'),
]