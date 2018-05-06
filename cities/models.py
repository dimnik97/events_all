from django.db import models

# Create your models here.

class Cities(models.Model):
    city_id = models.IntegerField(primary_key=True)
    country_id = models.IntegerField()
    important = models.BooleanField()
    region_id = models.IntegerField(blank=True, null=True)
    title_ru = models.CharField(max_length=150, blank=True, null=True)
    area_ru = models.CharField(max_length=150, blank=True, null=True)
    region_ru = models.CharField(max_length=150, blank=True, null=True)
    title_ua = models.CharField(max_length=150, blank=True, null=True)
    area_ua = models.CharField(max_length=150, blank=True, null=True)
    region_ua = models.CharField(max_length=150, blank=True, null=True)
    title_be = models.CharField(max_length=150, blank=True, null=True)
    area_be = models.CharField(max_length=150, blank=True, null=True)
    region_be = models.CharField(max_length=150, blank=True, null=True)
    title_en = models.CharField(max_length=150, blank=True, null=True)
    area_en = models.CharField(max_length=150, blank=True, null=True)
    region_en = models.CharField(max_length=150, blank=True, null=True)
    title_es = models.CharField(max_length=150, blank=True, null=True)
    area_es = models.CharField(max_length=150, blank=True, null=True)
    region_es = models.CharField(max_length=150, blank=True, null=True)
    title_pt = models.CharField(max_length=150, blank=True, null=True)
    area_pt = models.CharField(max_length=150, blank=True, null=True)
    region_pt = models.CharField(max_length=150, blank=True, null=True)
    title_de = models.CharField(max_length=150, blank=True, null=True)
    area_de = models.CharField(max_length=150, blank=True, null=True)
    region_de = models.CharField(max_length=150, blank=True, null=True)
    title_fr = models.CharField(max_length=150, blank=True, null=True)
    area_fr = models.CharField(max_length=150, blank=True, null=True)
    region_fr = models.CharField(max_length=150, blank=True, null=True)
    title_it = models.CharField(max_length=150, blank=True, null=True)
    area_it = models.CharField(max_length=150, blank=True, null=True)
    region_it = models.CharField(max_length=150, blank=True, null=True)
    title_pl = models.CharField(max_length=150, blank=True, null=True)
    area_pl = models.CharField(max_length=150, blank=True, null=True)
    region_pl = models.CharField(max_length=150, blank=True, null=True)
    title_ja = models.CharField(max_length=150, blank=True, null=True)
    area_ja = models.CharField(max_length=150, blank=True, null=True)
    region_ja = models.CharField(max_length=150, blank=True, null=True)
    title_lt = models.CharField(max_length=150, blank=True, null=True)
    area_lt = models.CharField(max_length=150, blank=True, null=True)
    region_lt = models.CharField(max_length=150, blank=True, null=True)
    title_lv = models.CharField(max_length=150, blank=True, null=True)
    area_lv = models.CharField(max_length=150, blank=True, null=True)
    region_lv = models.CharField(max_length=150, blank=True, null=True)
    title_cz = models.CharField(max_length=150, blank=True, null=True)
    area_cz = models.CharField(max_length=150, blank=True, null=True)
    region_cz = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '_cities'


class Countries(models.Model):
    country_id = models.IntegerField(primary_key=True)
    title_ru = models.CharField(max_length=60, blank=True, null=True)
    title_ua = models.CharField(max_length=60, blank=True, null=True)
    title_be = models.CharField(max_length=60, blank=True, null=True)
    title_en = models.CharField(max_length=60, blank=True, null=True)
    title_es = models.CharField(max_length=60, blank=True, null=True)
    title_pt = models.CharField(max_length=60, blank=True, null=True)
    title_de = models.CharField(max_length=60, blank=True, null=True)
    title_fr = models.CharField(max_length=60, blank=True, null=True)
    title_it = models.CharField(max_length=60, blank=True, null=True)
    title_pl = models.CharField(max_length=60, blank=True, null=True)
    title_ja = models.CharField(max_length=60, blank=True, null=True)
    title_lt = models.CharField(max_length=60, blank=True, null=True)
    title_lv = models.CharField(max_length=60, blank=True, null=True)
    title_cz = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '_countries'


class Regions(models.Model):
    region_id = models.IntegerField(primary_key=True)
    country_id = models.IntegerField()
    title_ru = models.CharField(max_length=150, blank=True, null=True)
    title_ua = models.CharField(max_length=150, blank=True, null=True)
    title_be = models.CharField(max_length=150, blank=True, null=True)
    title_en = models.CharField(max_length=150, blank=True, null=True)
    title_es = models.CharField(max_length=150, blank=True, null=True)
    title_pt = models.CharField(max_length=150, blank=True, null=True)
    title_de = models.CharField(max_length=150, blank=True, null=True)
    title_fr = models.CharField(max_length=150, blank=True, null=True)
    title_it = models.CharField(max_length=150, blank=True, null=True)
    title_pl = models.CharField(max_length=150, blank=True, null=True)
    title_ja = models.CharField(max_length=150, blank=True, null=True)
    title_lt = models.CharField(max_length=150, blank=True, null=True)
    title_lv = models.CharField(max_length=150, blank=True, null=True)
    title_cz = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = '_regions'
