from django.conf.urls import url
from custom_profile import views, forms

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.index, name='index'),
    url(r'^edit$', views.Edit.edit_view, name='edit'),
    url(r'^load_image', views.Edit.load_image, name='load_image'),
    url(r'^load_image_to_crop', views.Edit.load_image_to_crop, name='load_image_to_crop'),
    url(r'^get_subscribers$', views.get_subscribers, name='get_subscribers$'),
    url(r'add_or_remove_friends/$', views.add_or_remove_friends, name='add_or_remove_friends'),
]