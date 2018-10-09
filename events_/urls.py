from django.conf.urls import url
from events_ import views, forms

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.index, name='index'),
    url(r'edit/(?P<id>[0-9]+)$', views.edit, name='edit'),
    url(r'create$', views.create, name='create'),
    url(r'^change_avatar', views.change_avatar, name='change_avatar'),
    url(r'^change_mini', views.change_mini, name='change_mini'),
    url(r'^get_subscribers$', views.get_subscribers, name='get_subscribers'),
    url(r'^change_default_image$', views.change_default_image, name='change_default_image'),
    url(r'^get_images_by_categories$', views.get_images_by_categories, name='get_images_by_categories'),
    url(r'^delete_event$', views.delete_event, name='delete_event'),  # Удаление события
    url(r'^create_news$', views.create_news, name='create_news'),  # создание новости
    url(r'^edit_news$', views.edit_news, name='edit_news'),  # редактирование новости
    url(r'^delete_event_news$', views.delete_event_news, name='delete_event_news'),  # удаление новости

    # url(r'^save_image', views.save_image, name='save_image'),
]
