from functools import partial

from django import forms
from django.core.serializers import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from events_.models import Event


class EditEvent(forms.Form):
    id = forms.CharField(required=True, widget=forms.HiddenInput(), max_length=30, label='id')
    name = forms.CharField(required=True, max_length=30, label='Имя')
    description = forms.CharField(required=False, widget=forms.Textarea(), max_length=1000, label='Описание')
    start_time = forms.CharField(required=False,
                                 # widget=forms.TextInpit(attrs={"class": "datetimepicker"}),
                                 label='Дата начала')
    end_time = forms.CharField(required=False,
                               # widget=forms.TextInpit(attrs={"class": "datetimepicker"}),
                               label='Дата окончания')

    def save(self, request):
        event = get_object_or_404(Event, id=request.POST['id'])
        event.name = request.POST['name']
        event.description = request.POST['description']
        # event.start_time = request.POST['start_time']
        # event.end_time = request.POST['end_time']
        event.save()
        return HttpResponse(str(200))

    def form_valid(self, form):
        form.save()
        return HttpResponse('OK')

    def form_invalid(self, form):
        errors_dict = json.dumps(dict([(k, [e for e in v]) for k, v in form.errors.items()]))
        return HttpResponseBadRequest(json.dumps(errors_dict))



