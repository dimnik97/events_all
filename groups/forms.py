from django import forms

from groups.models import Group, GroupSubscribers, AllRoles


class GroupsForm(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput(), label='Название группы')
    name = forms.CharField(required=True, max_length=30, label='Название группы')
    description = forms.CharField(required=True, max_length=30, label='Описание')
    CHOICES_С = (('1', 'Открытая'),
                 ('2', 'Закрытая'))
    type = forms.ChoiceField(widget=forms.Select, choices=CHOICES_С, label='Тип группы', required=False)

    def save(self, request):
        # Редактирование группы
        if self.cleaned_data['id']:
            try:
                group = Group.objects.get(
                    id=self.cleaned_data['id']
                )
            except Group.DoesNotExist:
                return 'Запрашиваемая группа не найдена'
        # Создание группы
        else:
            group = Group.objects.create(
                creator=request.user
            )
            group.name = self.cleaned_data['name']
            group.description = self.cleaned_data['description']
            group.type = self.cleaned_data['type']
            group.save()

        subscribers, created = GroupSubscribers.objects.get_or_create(
            group_id=group,
        )

        if created:
            subscribers.user_id.add(request.user)
            subscribers.role = AllRoles.objects.get(role='admin')
            subscribers.save()

        # Проверка на права доступа (редактировать может только админ)
        if subscribers.role == AllRoles.objects.get(role='admin') and not created:
            group.name = self.cleaned_data['name']
            group.description = self.cleaned_data['description']
            group.type = self.cleaned_data['type']
            group.save()
        else:
            return 'Нет прав'

        return group.id
