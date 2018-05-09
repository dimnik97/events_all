from django.contrib.auth.models import User
from django.http import JsonResponse
import helper
from urllib import parse
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class signup_validator():
    def email_and_password(request):
        if request.method == 'POST':
            dict_ = dict(parse.parse_qsl(request.POST.get('data')))
            validate_email = EmailValidator()

            status = ''
            data = {
                'status': status
            }

            try:
                email = dict_['email']
            except:
                data['status'] = helper.validate_error('empty', 'e-mail')
                return data

            if '@' in email:
                try:
                    validate_email(email)

                    if (str(User.objects.filter(email__iexact=dict_['email']).exists()) == True):
                        data['status'] = helper.validate_error(
                            'True',
                            'e-mail'
                        )
                        return data
                except ValidationError as e:
                    data['status'] = helper.validate_error('format', 'e-mail')
                    return data

                min_length = 5
                try:
                    password = dict_['password1']
                except:
                    data['status'] = helper.validate_error('empty', 'password')
                    return data

                if len(password) < min_length:
                    data['status'] = ('Слишком короткий пароль! Минимальное количество символов {0}').format(min_length)
                    return data

                # check for digit
                if not any(char.isdigit() for char in password):
                    data['status'] = 'Пароль должен содержать хотя бы одно число'
                    return data

                # check for letter
                if not any(char.isalpha() for char in password):
                    data['status'] = 'Пароль должен содержать хотя бы одну латинскую букву'
                    return data
            else:
                data['status'] = helper.validate_error('format', 'e-mail')
        return data


