from django.conf.urls import url
from groups import views

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.detail, name='detail'),  # Группа детально
    url(r'^create$', views.create, name='create'),  # Создание группы
    url(r'^edit/(?P<id>[0-9]+)$', views.edit, name='edit'),  # Редактирование группы
    url(r'^view$', views.view, name='view'),  # Список всех групп
    url(r'^get_groups$', views.get_groups, name='get_groups'),  # Паджинация
    url(r'^subscribe_group/$', views.subscribe_group, name='subscribe_group'),  # Подписка на группу
    url(r'^change_avatar', views.change_avatar, name='change_avatar'),  # Смена аватара
    url(r'^change_mini', views.change_mini, name='change_mini'),  # Смена минифицированной версии автара
    url(r'^save_image', views.save_image, name='save_image'),  # Сохранение аватара

    url(r'^invite$', views.invite, name='invite'),  # Приглашение в группу TODO
    url(r'^cancel$', views.cancel, name='cancel'),  # Отклонить заявку
    url(r'^accept$', views.accept, name='accept'),  # Принять заявку
    url(r'^send_an_application$', views.send_an_application, name='send_an_application'),  # Отправить заявку в группу

    url(r'^add_to_editor$', views.add_to_editor, name='add_to_editor'),  # Повышение до редактора
    url(r'^add_to_subscribers$', views.add_to_subscribers, name='add_to_subscribers'),  # Понижение до просто подписчика
    url(r'^delete_subscribers$', views.delete_subscribers, name='delete_subscribers'),  # Удаление подписчика
    url(r'^delete_group$', views.delete_group, name='delete_group'),  # Удаление группы
]
