from django.conf.urls import url
from company_profile import views

urlpatterns = [
    url(r'^(?P<id>[0-9]+)$', views.detail, name='index'),
    # url(r'edit/(?P<id>[0-9]+)$', views.edit, name='edit'),
    # url(r'create$', views.create, name='create'),
]
