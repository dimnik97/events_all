from django import forms
from django.http import HttpResponse

from cities_.models import CityTable


class SignupForm(forms.Form):
    first_name = forms.CharField(
        required=True, max_length=30, label='Имя', help_text='field_d_none',
        widget=forms.TextInput(attrs={'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        required=True, max_length=30, label='Фамилия', help_text='field_d_none',
        widget=forms.TextInput(attrs={'placeholder': 'Фамилия'})
    )
    phone = forms.CharField(required=True, max_length=30, help_text='field_d_none',
                            widget=forms.TextInput(attrs={'placeholder': 'Телефонный номер'}),
                            label='Телефонный номер (необязательно)')
    GENDER = (('1', 'Мужской'), ('2', 'Женский'))
    gender = forms.ChoiceField(required=True, help_text='field_d_none',
                               label='Пол', widget=forms.Select, choices=GENDER)
    birth_date = forms.DateField(required=True,
                                 label='Дата рождения',
                                 help_text='field_d_none',
                                 widget=forms.TextInput(attrs={'placeholder': 'Дата рождения'}),
                                 input_formats=['%d-%m-%Y'])

    city_list = CityTable.objects.filter(city__isnull=False).values('city', 'city_id').order_by('city')

    # Create User and related models (ProfileAvatar, UserSettings)
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.profile.phone = self.cleaned_data['phone']
        user.profile.gender = self.cleaned_data['gender']
        user.profile.birth_date = self.cleaned_data['birth_date']
        if 'select_city' in request.POST:
            try:
                city = CityTable.objects.get(city_id=request.POST['select_city'])
                user.profile.location = city
                user.profile.location_name = city.city
            except CityTable.DoesNotExist:
                pass

        from profiles.models import ProfileAvatar, UserSettings
        ProfileAvatar.objects.create(user=user)
        UserSettings.objects.create(user=user)
        user.save()


class EditProfile(forms.Form):
    first_name = forms.CharField(required=True, max_length=30, label='Имя')
    last_name = forms.CharField(required=True, max_length=30, label='Фамилия')
    description = forms.CharField(required=False, max_length=2000,
                                  widget=forms.Textarea(attrs={'placeholder': 'Напишите немного о себе'}),
                                  label='Пара слов обо мне')
    birth_date = forms.DateField(required=True, label='Дата рождения', input_formats=['%d-%m-%Y'])
    phone = forms.CharField(required=False, max_length=30, label='Телефонный номер')

    vk = forms.CharField(required=False, max_length=30, label='Вконткте')
    twitter = forms.CharField(required=False, max_length=30, label='Твиттер')
    facebook = forms.CharField(required=False, max_length=30, label='Фейсбук')

    CHOICES_M = (('1', 'Мужской',),
                 ('2', 'Женский',))
    gender = forms.ChoiceField(widget=forms.Select, choices=CHOICES_M, label='Пол', required=False)

    def save(self, request):
        user = request.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # profile
        user.profile.description = self.cleaned_data['description']
        user.profile.phone = self.cleaned_data['phone']
        user.profile.birth_date = self.cleaned_data['birth_date']
        user.profile.vk = self.cleaned_data['vk']
        user.profile.twitter = self.cleaned_data['twitter']
        user.profile.facebook = self.cleaned_data['facebook']
        if 'select_city' in request.POST:
            try:
                city = CityTable.objects.get(city_id=request.POST['select_city'])
                user.profile.location = city
                user.profile.location_name = city.city
            except CityTable.DoesNotExist:
                pass
        user.profile.gender = self.cleaned_data['gender']
        user.save()
        return HttpResponse(str(200))


class EditUserSettings(forms.Form):
    CHOICES_M = (('1', 'Открыть сообщения для всех',),
                 ('2', 'Написать могут только те, на кого я подписан',),
                 ('3', 'Закрыть сообщения для всех',))
    messages = forms.ChoiceField(widget=forms.Select, choices=CHOICES_M, label='Настройки сообщений')

    CHOICES_I = (('1', 'Приглашать могут все',),
                 ('2', 'Приглашать могут только те, на кого я подписан ',),)
    invite = forms.ChoiceField(widget=forms.Select, choices=CHOICES_I, label='Приглашения')

    # CHOICES_N = (('1', 'Включено',),
    #              ('2', 'Выключено',),)
    # near_invite = forms.ChoiceField(widget=forms.Select, choices=CHOICES_N, label='События недалеко')

    def save(self, request):
        user = request.user
        user.usersettings.messages = self.cleaned_data['messages']
        # user.usersettings.birth_date = self.cleaned_data['birth_date']
        user.usersettings.invite = self.cleaned_data['invite']
        # user.usersettings.near_invite = self.cleaned_data['near_invite']
        user.usersettings.save()
        return HttpResponse(str(200))


class ImageUploadForm(forms.Form):
    load_image = forms.ImageField(label='')
