from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.http import JsonResponse
from django_ipgeobase.models import IPGeoBase

#Необходимо для того, чтобы не запрашивался токен
from django.views.decorators.csrf import csrf_exempt
from profile.validator import signup_validator

# Получение общей информации для пользователей
class Users:
    # Получение модели юзера
    def get_user(self):
        try:
            return User.objects.get(id=self.user.id)
        except User.DoesNotExist:
            return None

    # Определение IP юзера
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    #TODO Переделать, проверка должна быть
    @csrf_exempt
    def signup_check(request):
        return JsonResponse(signup_validator.email_and_password(request))

    # Работает при помощи библиотеки ipgeobase
    # Иногда необходимо апдейтить базу python manage.py ipgeobase_update
    # -------------------------------------
    # Список методов:
    # print(ipgeobase.country)  # 'RU' - Страна
    # print(ipgeobase.district)  # Округ (для указанного ip - Уральский федеральный округ)
    # print(ipgeobase.region)  # Регион (Свердловская область)
    # print(ipgeobase.city)  # Населенный пункт (Екатеринбург)
    # print(ipgeobase.ip_block)  # IP-блок, в который попали (212.49.96.0 - 212.49.127.255)
    # print(ipgeobase.start_ip, ipgeobase.end_ip)  # (3560005632, 3560013823), IP-блок в числовом формате
    # print(ipgeobase.latitude, ipgeobase.longitude)  # (56.837814, 60.596844), широта и долгота
    def get_user_locations(request):
        ip = "212.49.98.48"
        # ipp = Users.get_client_ip(request)

        ipgeobases = IPGeoBase.objects.by_ip(ip)
        if ipgeobases.exists():
            return ipgeobases[0]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.TextField(null=True, blank = True)
    sex = models.IntegerField(default=0)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()