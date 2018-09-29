from django import forms
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from cities_.models import CityTable
from events_.models import Event, Event_avatar, EventCategory, EventNews, EventMembership
from events_all.widgets import CustomDateTimePicker
from groups.models import Group


class CreateEventNews(forms.Form):
    text = forms.CharField(required=False, widget=forms.Textarea(), max_length=1000, label='Новость')
    image = forms.ImageField(required=False, label='Фото')

    def save(self, request, event):
        news = EventNews()
        news.news_creator = request.user
        news.text = request.POST['text']
        news.news_event = event
        news.news_image = request.FILES['image']
        news.save()


class EventForm(forms.Form):
    id = forms.CharField(required=False, widget=forms.HiddenInput(), max_length=30, label='id')
    # image = forms.ImageField(required=False, label='Фото')
    name = forms.CharField(required=True, max_length=30, label='Название события')
    description = forms.CharField(required=False, widget=forms.Textarea(), max_length=1000, label='Описание')

    CATEGORY_CH = []
    for item in EventCategory.objects.all():
        CATEGORY_CH.append((item.id, item.name))

    category = forms.ChoiceField(required=False,
                                 label='Категория', widget=forms.Select, choices=CATEGORY_CH)

    start_time = forms.CharField(required=False,
                                 widget=CustomDateTimePicker(prams={'default_time': '1'}),
                                 label='Дата начала')
    end_time = forms.CharField(required=False,
                               widget=CustomDateTimePicker(prams={'default_time_plus_delta': '1'}),
                               label='Дата окончания')

    # метод для сохранения данных из формы, вызывается аяксом, валидируется на стороне сервера
    def save(self, request, is_creation=None):
        result = {
            'status': 200,
            'url': ''
        }
        try:
            cities = CityTable.objects.get(city_id=request.POST['location'])

            if is_creation == 1:  # Если создание
                event = Event()
                if 'group_id' in request.GET:   # Создано ли от группы?
                    group = Group.objects.get(pk=int(request.GET['group_id']))
                    event.created_by_group = group

            else:  # Если редактирование
                event = Event.objects.get(id=request.POST['id'])

            event.name = request.POST['name']
            if 'description' in request.POST:
                event.description = request.POST['description']

            try:
                geo_name = request.POST['geo_name']
                lat = request.POST['lat']
                lng = request.POST['lng']
            except KeyError:
                pass

            event.creator_id = request.user
            event.location = cities
            event.location_name = cities.city
            event.start_time = request.POST['start_time']
            event.end_time = request.POST['end_time']
            event.save()
            Event_Membership.objects.create(event=event, person=request.user.profile)
            result['url'] = event.id
            return result
        except CityTable.DoesNotExist:
            result['status'] = 400  # Ошибка
            return result

