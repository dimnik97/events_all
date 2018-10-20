from django import forms

from events_.models import Event
from groups.models import Group, Membership, AllRoles


class GroupsForm(forms.Form):
    id = forms.IntegerField(required=False, widget=forms.HiddenInput(), label='Название группы')
    name = forms.CharField(required=True, max_length=100, label='Название группы')
    status = forms.CharField(required=False, max_length=100, label='Краткое описание')
    description = forms.CharField(required=False, max_length=1000, label='Описание')
    CHOICES_С = (('1', 'Открытая'),
                 ('2', 'Закрытая'))
    type = forms.ChoiceField(widget=forms.Select, choices=CHOICES_С, label='Тип группы', required=False)

    def save(self, request):
        # Редактирование группы
        if self.cleaned_data['id']:
            try:
                group = Group.objects.get(id=self.cleaned_data['id'])
            except Group.DoesNotExist:
                return 'Запрашиваемая группа не найдена'
        # Создание группы
        else:
            group = Group.objects.create( creator=request.user)
            save_group(self, group)

            Membership.objects.create(group=group, person=request.user.profile, role=AllRoles.objects.get(role='admin'))
            return group.id

        # Редактирование группы
        try:
            membership = Membership.objects.get(group=group, person=request.user.profile)
        except Membership.DoesNotExist:
            return 'Пользователь не найден'
        # Проверка на права доступа (редактировать может только админ)
        if membership.role == AllRoles.objects.get(role='admin'):
            save_group(self, group)
        else:
            return 'Нет прав'

        return group.id


def save_group(self, group):
    group.name = self.cleaned_data['name']
    group.description = self.cleaned_data['description']
    group.status = self.cleaned_data['status']
    # Если группа закрытая, то "закрываются" и все события с ней связанные, так же в обратную сторону
    group.type = self.cleaned_data['type']
    group.save()
    from django.db.models import Q
    Event.objects.filter(Q(active='1') | Q(active='2'), created_by_group=group, ) \
        .update(active=self.cleaned_data['type'])
