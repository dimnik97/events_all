from django.conf.urls import url
from profiles import views, forms

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.detail, name='detail'),  # детальный профиль
    url(r'^$', views.my_profile, name='detail'),  # для редиректа на свой профиль
    url(r'^edit/$', views.edit_view, name='edit'),  # редактирование профиля
    url(r'^view$', views.view, name='view'),  # Список всех пользователей
    url(r'^change_avatar', views.Edit.change_avatar, name='change_avatar'),  # Смена аватара
    url(r'^change_mini', views.Edit.change_mini, name='change_mini'),  # Смена миниатюры
    url(r'^save_image', views.Edit.save_image, name='save_image'),  # Сохранение картинки
    url(r'^get_subscribers$', views.get_subscribers, name='get_subscribers'),  # Просмотр тех, на кого подписан
    url(r'^get_followers$', views.get_followers, name='get_followers$'),  # Просмотр подписчиков
    url(r'^subscribe$', views.add_or_remove_friends, name='add_or_remove_friends'),  # добавление/удаление из друзей

    url(r'^custom_fields_for_signup$', views.custom_fields_for_signup, name='custom_fields_for_signup'),  # кастомные поля для формы регистрации
]