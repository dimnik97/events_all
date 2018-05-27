import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.core.validators import EmailValidator
import django.contrib.auth.password_validation as validators


class SignupValidator():
    def email_and_password(request):
        if request.method == 'POST':
            email = request.POST['email']
            json_data = {}
            if '@' in email:
                try:
                    EmailValidator(email)
                    if User.objects.filter(email__iexact=email).exists() == True:
                        json_data["email"] = "Пользователь с данным Email уже зарегестрирован"

                except ValidationError as e:
                    json_data["email"] = e
            else:
                json_data["email"] = 'Введите корректный Email'

            try:
                validators.validate_password(request.POST['password1'])
            except ValidationError as e:
                json_data["password1"] = str(e)

            return HttpResponse(
                json.dumps(json_data, ensure_ascii=False),
                content_type="application/json"
            )



