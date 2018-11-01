import datetime

from django import forms
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from cities_.models import CityTable
from events_.models import Event, Event_avatar, EventCategory, EventNews, EventMembership, EventGeo, \
    EventCategoryRelation
from events_all.widgets import CustomDateTimePicker
from groups.models import Group


class CreateEventNews(forms.Form):
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={'onkeyup': '1textarea_resize(event, 15, 2)'}),
                           max_length=1000, label='Новость') #TODO 1 в onkeyup - заглушка, нужно переделать
    event_id = forms.CharField(required=False, widget=forms.HiddenInput(), max_length=30, label='event_id')
    news = forms.CharField(required=False, widget=forms.HiddenInput(), max_length=30, label='edit_id')

    # image = forms.ImageField(required=False, label='Фото')

    @staticmethod
    def save(request, event):
        if 'text' in request.POST and request.POST['text'] != '':
            if 'news' in request.POST and request.POST['news'] != '':
                news = get_object_or_404(EventNews, id=request.POST['news'])
                news.text = request.POST['text']
                news.news_creator = request.user
                if 'image' in request.FILES:
                    news.news_image = ''
                news.save()
                return {'status': 100, 'text': request.POST['text'], 'id': news.id}
            else:
                news = EventNews()
                news.news_creator = request.user
                news.text = request.POST['text']
                news.news_event = event
                if event.created_by_group:
                    news.news_group = event.created_by_group
                event.last_update = datetime.datetime.now()  # Апдейт события, для ее продвижения
                event.save()
                can_change_news = True
                if 'image' in request.FILES:
                    news.news_image = ''
                news.save()

                result = {
                    'text': render_to_string('events_/news.html', {'news': EventNews.objects.filter(id=news.id),
                                                                 'can_change_news': can_change_news}),
                    'status': 201,
                }
            return result
        return {'status': 400}


class EventForm(forms.Form):
    id = forms.CharField(required=False, widget=forms.HiddenInput(), max_length=30, label='id')
    name = forms.CharField(required=True, max_length=100, label='Название события')
    description = forms.CharField(required=False, widget=forms.Textarea(), max_length=1000, label='Описание')

    start_time = forms.CharField(required=False,
                                 widget=CustomDateTimePicker(prams={'default_time': '1'}),
                                 label='Дата начала')
    end_time = forms.CharField(required=False,
                               widget=CustomDateTimePicker(prams={'default_time_plus_delta': '1'}),
                               label='Дата окончания')
    CHOICES = (('1', 'Открытое'),
               ('2', 'Закрытое'))
    active = forms.ChoiceField(widget=forms.Select, choices=CHOICES, label='Тип события', required=True)

    # метод для сохранения данных из формы, вызывается аяксом, валидируется на стороне сервера
    def save(self, request, is_creation=None):
        result = {
            'status': 200,
            'url': '',
            'wrong_field': ''
        }
        try:
            cities = CityTable.objects.get(city_id=request.POST['location'])
            categories = (request.POST['categories']).split(',')
            categories.pop()
            if len(categories) == 0:
                result['status'] = 400  # Ошибка
                result['wrong_field'] = 'categories'
                return result
            if len(categories) > 3:
                categories = categories[:3]  # Ограничение на 3 категории

            if is_creation == 1:  # Если создание
                event = Event()
                if 'group_id' in request.POST and request.POST['group_id']:   # Создано ли от группы?
                    is_editor = Group.is_editor(request, request.POST['group_id'])
                    if is_editor is True:
                        group = Group.objects.get(pk=int(request.POST['group_id']))
                        event.created_by_group = group
                    else:
                        return

            else:  # Если редактирование
                event = Event.objects.get(id=request.POST['id'])

            event.name = request.POST['name']
            if 'description' in request.POST:
                event.description = request.POST['description']

            try:
                event_geo = EventGeo.objects.create(name=request.POST['geo_name'],
                                                    lat=float(request.POST['lat']),
                                                    lng=float(request.POST['lng']))
                event.geo_point = event_geo
            except KeyError:
                pass

            event.creator_id = request.user
            event.location = cities
            event.location_name = cities.city
            event.start_time = request.POST['start_time']
            event.end_time = request.POST['end_time']
            event.active = request.POST['active']
            event.save()

            if is_creation == 1:
                EventMembership.objects.create(event=event, person=request.user.profile)
                # Временное решение
                Event_avatar.objects.create(event=event)
                # Временное решение
            else:
                EventCategoryRelation.objects.filter(event=event).delete()
            for category in categories:
                EventCategoryRelation.objects.create(event=event, category=EventCategory.objects.get(id=category))
            result['url'] = event.id
            return result
        except CityTable.DoesNotExist:
            result['status'] = 400  # Ошибка
            return result

