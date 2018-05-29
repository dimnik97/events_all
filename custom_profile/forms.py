from allauth.account.adapter import DefaultAccountAdapter
from django import forms
from django.http import HttpResponse, Http404

from cities.models import Countries


# Форма регистрации
class SignupForm(forms.Form):
    first_name = forms.CharField(
        required=True, max_length=30, label='Имя', help_text='field_d_none'
    )
    last_name = forms.CharField(
        required=True, max_length=30, label='Фамилия', help_text='field_d_none'
    )
    GENDER = (('1', 'Мужской'), ('2', 'Женский'))
    phone = forms.CharField(required=False, max_length=30, help_text='field_d_none',
                            label='Телефонный номер (необязательно)')
    gender = forms.ChoiceField(required=False, help_text='field_d_none',
                               label='Пол', widget=forms.Select, choices=GENDER)
    # TODO Добавить валидацию или маску

    # TODO Вернуться к этому позже
    # birth_country = forms.ModelChoiceField(
    #     required=False,
    #     queryset=Countries.objects.all().values_list('country_id', flat=True).distinct(),
    #     widget=autocomplete.ModelSelect2(url='country-autocomplete')
    # )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile.phone = self.cleaned_data['phone']
        user.profile.sex = self.cleaned_data['gender']

        from custom_profile.models import ProfileAvatar
        ProfileAvatar.objects.create(user=user)
        user.save()


class EditProfile(forms.Form):
    first_name = forms.CharField(required=True, max_length=30, label='Имя')
    last_name = forms.CharField(required=True, max_length=30, label='Фамилия')

    CHOICES_С = (('1', 'Не работает',),)
    country = forms.ChoiceField(widget=forms.Select, choices=CHOICES_С, label='Страна', required=False)

    CHOICES_СITY = (('1', 'Не работает',),)
    city = forms.ChoiceField(widget=forms.Select, choices=CHOICES_СITY, label='Город', required=False)

    description = forms.CharField(required=False, max_length=2000, widget=forms.Textarea(), label='Пара слов обо мне')
    birth_date = forms.DateField(required=False,
                                 widget=forms.SelectDateWidget(years=range(1900, 2012)),
                                 label='Дата рождения')
    phone = forms.CharField(required=False, max_length=30, label='Телефонный номер')

    def save(self, request):
        user = request.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # profile
        user.profile.description = self.cleaned_data['description']
        user.profile.phone = self.cleaned_data['phone']
        user.profile.birth_date = self.cleaned_data['birth_date']
        user.save()
        return HttpResponse(str(200))


class EditUserSettings(forms.Form):
    CHOICES_M = (('1', 'Открыть сообщения для всех',),
               ('2', 'Написать могут только те, на кого я подписан',),
               ('3', 'Закрыть сообщения для всех',))
    messages = forms.ChoiceField(widget=forms.Select, choices=CHOICES_M, label='Настройки сообщений')

    CHOICES_D = (('1', 'Видно всем',),
               ('2', 'Видно только подписчикам',),
               ('3', 'Скрыть для всех',))
    birth_date = forms.ChoiceField(widget=forms.Select, choices=CHOICES_D, label='Отображения даты рождения')

    CHOICES_I = (('1', 'Приглашать могут все',),
                 ('2', 'Приглашать могут только те, на кого я подписан ',),)
    invite = forms.ChoiceField(widget=forms.Select, choices=CHOICES_I, label='Приглашения')

    CHOICES_N = (('1', 'Включено',),
                 ('2', 'Выключено',),)
    near_invite = forms.ChoiceField(widget=forms.Select, choices=CHOICES_N, label='События недалеко')

    def save(self, request):
        user = request.user
        user.usersettings.messages = self.cleaned_data['messages']
        user.usersettings.birth_date = self.cleaned_data['birth_date']
        user.usersettings.invite = self.cleaned_data['invite']
        user.usersettings.near_invite = self.cleaned_data['near_invite']
        user.usersettings.save()
        return HttpResponse(str(200))


class UserAvatarForm(forms.Form):
    messages = forms.ImageField(widget=forms.Select, label='Настройки сообщений')