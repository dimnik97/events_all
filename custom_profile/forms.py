from allauth.account.adapter import DefaultAccountAdapter
from django import forms

from cities.models import Countries


# Форма регистрации
class SignupForm(forms.Form):
    first_name = forms.CharField(
        required=True, max_length=30, label='First name'
    )
    last_name = forms.CharField(
        required=True, max_length=30, label='Last name'
    )

    # profile
    birth_date = forms.DateField(required=False, widget=forms.SelectDateWidget(years=range(1900, 2012)))
    phone = forms.CharField(required=False, max_length=30, label='Phone number')  # TODO Добавить валидацию или маску

    # TODO Вернуться к этому позже
    # birth_country = forms.ModelChoiceField(
    #     required=False,
    #     queryset=Countries.objects.all().values_list('country_id', flat=True).distinct(),
    #     widget=autocomplete.ModelSelect2(url='country-autocomplete')
    # )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = forms.HiddenInput()
        self.fields['last_name'].widget = forms.HiddenInput()
        # profile
        self.fields['phone'].widget = forms.HiddenInput()
        self.fields['birth_date'].widget = forms.HiddenInput()

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        # profile
        user.profile.phone = self.cleaned_data['phone']
        user.profile.birth_date = self.cleaned_data['birth_date']
        user.save()