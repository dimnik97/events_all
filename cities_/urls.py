from django.conf.urls import url

from cities_.models import CityTable

urlpatterns = [
    url(r'^find_city$', CityTable.find_city, name='find_city'),
]