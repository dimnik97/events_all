import json

from django.db import models
from django.core import serializers


# Создал так
# CREATE TABLE city_table
# SELECT distinct city, city_id, region, district
# FROM django_ipgeobase_ipgeobase
# where city is not null
from django.http import HttpResponse


class CityTable(models.Model):
    city = models.CharField(max_length=255, blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=False, unique=True, primary_key=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def find_city(request):
        cities = ''
        try:
            if 'city_name' in request.POST:
                cities = CityTable.objects.filter(city__istartswith=request.POST['city_name'])
        except KeyError:
            return HttpResponse('Error')
        return HttpResponse(serializers.serialize('json', list(cities)))

    @staticmethod
    def all_city_exclude_user_city(user_city):
        return CityTable.objects.filter(city__isnull=False).\
            values('city', 'city_id').order_by('city').exclude(city=user_city.city)

