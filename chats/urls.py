from django.conf.urls import url
from chats import views

urlpatterns = [
    url(r'^$', views.home, name=''),
    url(r'^dlg', views.room, name='dlg'),
]
