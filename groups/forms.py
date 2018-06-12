from django import forms
from django.http import HttpResponse

from groups.models import Group


class GroupsForm(forms.Form):
    name = forms.CharField(required=True, max_length=30, label='Название группы')
    description = forms.CharField(required=True, max_length=30, label='Описание')
    CHOICES_С = (('1', 'Открытая'),
                 ('1', 'Закрытая'))
    type = forms.ChoiceField(widget=forms.Select, choices=CHOICES_С, label='Тип группы', required=False)

    def save(self, request):
        group = Group()
        group.name = self.cleaned_data['name']
        group.description = self.cleaned_data['description']
        group.type = self.cleaned_data['type']
        group.creator = request.user
        group.save()
        return HttpResponse(str(200))
