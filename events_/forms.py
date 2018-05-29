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
                                 widget=CustomDateTimePicker(),
                                 label='Дата начала')
    end_time = forms.CharField(required=False,
                               widget=CustomDateTimePicker(),
                               label='Дата окончания')

    # метод для сохранения данных из формы
    def save(self, request, is_creation = None):

        if is_creation == 1:
            event = Event()
            event.creator_id = request.user
            event.name = request.POST['name']
            event.description = request.POST['description']
            if request.POST['start_time'] is not None:
                event.start_time = request.POST['start_time']
            if request.POST['end_time'] is not None:
                event.end_time = request.POST['end_time']

        else:

            event = get_object_or_404(Event, id=request.POST['id'])
            event.name = request.POST['name']
            event.description = request.POST['description']
            if request.POST['start_time'] is not None:
                event.start_time = request.POST['start_time']
            if request.POST['end_time'] is not None:
                event.end_time = request.POST['end_time']

        event.save()

        event_photo = Event_avatar()
        event_photo.image = request.POST['image']
        event_photo.event = event
        event_photo.save()

        return HttpResponse(str(200))

    def form_valid(self, form):
        form.save()
        return HttpResponse('OK')

    def form_invalid(self, form):
        errors_dict = json.dumps(dict([(k, [e for e in v]) for k, v in form.errors.items()]))
        return HttpResponseBadRequest(json.dumps(errors_dict))

