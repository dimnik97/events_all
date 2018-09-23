from django.db import models


# Создал так
# CREATE TABLE city_table
# SELECT distinct city, city_id, region, district
# FROM django_ipgeobase_ipgeobase
# where city is not null
class CityTable(models.Model):
    city = models.CharField(max_length=255, blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=False, unique=True, primary_key=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city_table'
