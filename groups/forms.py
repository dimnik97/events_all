from django import forms

from groups.models import Group, GroupSubscribers, AllRoles


class GroupsForm(forms.Form):
    id = forms.CharField(required=False, max_length=30, label='Название группы')
    name = forms.CharField(required=True, max_length=30, widget=forms.HiddenInput(), label='Название группы')
    description = forms.CharField(required=True, max_length=30, label='Описание')
    CHOICES_С = (('1', 'Открытая'),
                 ('2', 'Закрытая'))
    type = forms.ChoiceField(widget=forms.Select, choices=CHOICES_С, label='Тип группы', required=False)

    def save(self, request):
        group, created = Group.objects.get_or_create(
            group_id=self.cleaned_data['id']
        )
        subscribers, created = GroupSubscribers.objects.get_or_create(
            group_id=group.id
        )
        if not created:
            if subscribers.role == 'admin':
                return 'Нет прав'
        group.name = self.cleaned_data['name']
        group.description = self.cleaned_data['description']
        group.type = self.cleaned_data['type']
        group.creator = request.user
        group.save()

        if created:
            subscribers.user_id.add(request.user)
            subscribers.role = AllRoles.objects.get(id=3)
            subscribers.save()
        return group.id
