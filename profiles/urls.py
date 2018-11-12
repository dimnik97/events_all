from django.conf.urls import url
from profiles import views, forms

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.detail, name='detail'),  # детальный профиль
    url(r'^$', views.my_profile, name='detail'),  # для редиректа на свой профиль
    url(r'^edit/$', views.edit_view, name='edit'),  # редактирование профиля
    url(r'^view/$', views.view, name='view'),  # Просмотр всех пользователей

    url(r'^view_subscribers/$', views.view_subscribers, name='view_subscribers'),  # Список подписок
    url(r'^view_followers/$', views.view_followers, name='view_followers'),  # Список подписчиков
    url(r'^view_all_users/$', views.view_all_users, name='view_all_users'),  # Список пользователей

    url(r'^change_avatar', views.Edit.change_avatar, name='change_avatar'),  # Смена аватара
    url(r'^change_mini', views.Edit.change_mini, name='change_mini'),  # Смена миниатюры
    url(r'^save_image', views.Edit.save_image, name='save_image'),  # Сохранение картинки
    url(r'^get_subscribers$', views.get_subscribers, name='get_subscribers'),  # Просмотр тех, на кого подписан
    url(r'^get_followers$', views.get_followers, name='get_followers$'),  # Просмотр подписчиков
    url(r'^subscribe$', views.add_or_remove_friends, name='add_or_remove_friends'),  # добавление/удаление из друзей
]