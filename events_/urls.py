from django.conf.urls import url
from events_ import views

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.index, name='index'),  # Детальная эвента
    url(r'edit/(?P<id>[0-9]+)$', views.edit, name='edit'),  # Реадактирование эвента
    url(r'create$', views.create, name='create'),  # Создание профиля
    url(r'^change_avatar', views.change_avatar, name='change_avatar'),  # Смена аватара
    url(r'^change_mini', views.change_mini, name='change_mini'),  # Смена миниатюры
    url(r'^get_subscribers$', views.get_subscribers, name='get_subscribers'),  # Получение подписчиков события

    url(r'^user_manager$', views.user_manager, name='user_manager'),  # Получение запросов на подписку/приглашений
    url(r'^change_default_image$', views.change_default_image, name='change_default_image'),
    url(r'^get_images_by_categories$', views.get_images_by_categories, name='get_images_by_categories'),
    url(r'^delete_event$', views.delete_event, name='delete_event'),  # Удаление события
    url(r'^create_news$', views.create_news, name='create_news'),  # создание новости
    url(r'^edit_news$', views.edit_news, name='edit_news'),  # редактирование новости
    url(r'^delete_event_news$', views.delete_event_news, name='delete_event_news'),  # удаление новости

    url(r'^like$', views.like, name='like'),  # проставление лайка (добавление в закладки)
    url(r'^unlike$', views.unlike, name='unlike'),  # удаление лайка (добавление в закладки)
]
