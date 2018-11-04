from django.conf.urls import url

from cities_.models import CityTable

urlpatterns = [
    url(r'^find_city$', CityTable.find_city, name='find_city'),
    url(r'^get_cities$', CityTable.get_cities, name='get_cities'),  # Option с выбранным по ip списком городов
    url(r'^get_cities_for_event$', CityTable.get_cities_for_event, name='get_cities_for_event'),
]