from django.conf.urls import url
from .views import CountryAutocomplete

urlpatterns = [
    url(
        r'^country-autocomplete/$',
        CountryAutocomplete.as_view(),
        name='country-autocomplete',
    ),
]