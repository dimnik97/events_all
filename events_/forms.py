from django import forms
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404


from events_.models import Event, Event_avatar
from events_all.widgets import CustomDateTimePicker


class EditEvent(forms.Form):
    id = forms.CharField(required=False, widget=forms.HiddenInput(), max_length=30, label='id')
    image = forms.ImageField(required=False, label='Фото')

    name = forms.CharField(required=True, max_length=30, label='Имя')
    description = forms.CharField(required=False, widget=forms.Textarea(), max_length=1000, label='Описание')
    start_time = forms.CharField(required=False,
                                 widget=CustomDateTimePicker(prams={'default_time': '1'}),
                                 label='Дата начала')
    end_time = forms.CharField(required=False,
                               widget=CustomDateTimePicker(prams={'default_time_plus_delta': '1'}),
                               label='Дата окончания')

    # метод для сохранения данных из формы
    def save(self, request, is_creation=None):

        if is_creation == 1:
            event = Event()
            event.creator_id = request.user

        else:
            event = get_object_or_404(Event, id=request.POST['id'])

        event.name = request.POST['name']
        event.description = request.POST['description']
        if request.POST['start_time'] is not None:
            event.start_time = request.POST['start_time']
        if request.POST['end_time'] is not None:
            event.end_time = request.POST['end_time']

        event.save()

        if len(request.FILES) > 0:
            if request.FILES['image'] is not None:
                event_photo = Event_avatar.objects.get_or_create(event=event)
                event_photo[0].image = request.FILES['image']
                event_photo[0].event = event
                event_photo[0].save()

        return HttpResponse(event.id)

