import datetime
import hashlib
import os

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import curry
from django_ipgeobase.models import IPGeoBase
from PIL import Image

import helper
from custom_profile import forms
from custom_profile.validator import SignupValidator


# Получение общей информации для пользователей
class Users:
    # Возвращает абсолютный URL
    @models.permalink
    def get_absolute_url(user_id):
        return "/profile/%i/" % user_id

    # Определение IP юзера
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def signup_check(request):
        return SignupValidator.email_and_password(request)

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


# Модель с дополнительными полями для user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    sex = models.IntegerField(default=0)

    class Meta:
        verbose_name = ('Профили')
        verbose_name_plural = ('Профили')

    def __str__(self):
        return self.user.first_name + self.user.last_name + ' (' + self.user.username + ')'

    def clean(self):
        cleaned_data = super(Profile, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')

    # Создание юзера с дополнительной информацией
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    # Сохранение юзера с дополнительной информацией
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    # Получение списка всех юзеров
    # TODO в будущем грохнуть метод
    def get_users():
        events = User.objects.all()
        return events

    def get_absolute_url(self):
        return "/profile/%i/" % self.id


# Модель "Дрзуей"
class Subscribers(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name="owner", null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ('Подписчики')
        verbose_name_plural = ('Подписчики')

    @classmethod
    def make_friend(cls, current_user, new_friend):
        subscribers, created = cls.objects.get_or_create(
            current_user=current_user
        )
        subscribers.users.add(new_friend)

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        subscribers, created = cls.objects.get_or_create(
            current_user=current_user
        )
        subscribers.users.remove(new_friend)

    # Возвращает абсолютный URL
    @models.permalink
    def get_absolute_url(user_id):
        return "/profile/%i/" % user_id


# Аватарки и миниатюры пользователей
class ProfileAvatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=True)
    last_update = models.DateField(null=True, blank=True, default=datetime.date.today)
    image = models.ImageField(upload_to=curry(helper.upload_to, prefix='avatar'),
                              default='avatar/default/img.png')
    reduced_image = models.ImageField(upload_to=curry(helper.upload_to, prefix='avatar', postfix='_reduced'),
                                      default='avatar/default/img.png')

    class Meta:
        verbose_name = ('Аватары')
        verbose_name_plural = ('Аватары')

    # Добавляем к свойствам объектов модели путь к миниатюре
    def _get_mini_path(self):
        return helper._add_mini(self.image.path)

    mini_path = property(_get_mini_path)
    # Добавляем к свойствам объектов модели урл миниатюры

    def _get_mini_url(self):
        return helper._add_mini(self.image.url)

    mini_url = property(_get_mini_url)

    # Создаем свою save
    # Добавляем:
    # - создание миниатюры
    # - удаление миниатюры и основного изображения
    #   при попытке записи поверх существующей записи
    def save(self, force_insert=False, force_update=False, using=None):
        try:
            obj = ProfileAvatar.objects.get(id=self.id)
            if obj.image.path != self.image.path:
                helper._del_mini(obj.image.path)
                obj.image.delete()
        except:
            pass
        super(ProfileAvatar, self).save()
        img = Image.open(self.image.path)
        # img.save(self.reduced_image.path, optimize=True, quality=15,
        #          progressive=True)

        new_photo = img
        new_photo.thumbnail(
            (1024, 1024),
            resample=Image.ANTIALIAS,
        )
        save_args = {'format': format}
        if format == 'JPEG':
            save_args['quality'] = 85
        new_photo.save(self.reduced_image.path, **save_args)


        # Миниатюрка
        img.thumbnail(
            (128, 128),
            Image.ANTIALIAS
        )
        img.save(self.mini_path)

    # Делаем свою delete с учетом миниатюры
    def delete(self, using=None):
        try:
            obj = ProfileAvatar.objects.get(id=self.id)
            helper._del_mini(obj.image.path)
            obj.image.delete()
        except (ProfileAvatar.DoesNotExist, ValueError):
            pass
        super(ProfileAvatar, self).delete()

    def get_absolute_url(self):
        return ('photo_detail', None, {'object_id': self.id})


# Аватарки и миниатюры пользователей
class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=True)
    CHOICES_M = (('1', 'Открыть сообщения для всех'),
                 ('2', 'Написать могут только те, на кого я подписан'),
                 ('3', 'Закрыть сообщения для всех'))

    CHOICES_D = (('1', 'Видно всем'),
                 ('2', 'Видно только подписчикам'),
                 ('3', 'Скрыть для всех'))

    CHOICES_I = (('1', 'Приглашать могут все'),
                 ('2', 'Приглашать могут только те, на кого я подписан '),)

    CHOICES_N = (('1', 'Включено'),
                 ('2', 'Выключено'),)

    messages = models.CharField(
        max_length=2,
        choices=CHOICES_M,
        default=1,
    )
    birth_date = models.CharField(
        max_length=2,
        choices=CHOICES_D,
        default=1,
    )
    invite = models.CharField(
        max_length=2,
        choices=CHOICES_I,
        default=1,
    )
    near_invite = models.CharField(
        max_length=2,
        choices=CHOICES_N,
        default=1,
    )

    class Meta:
        verbose_name = ('Пользовательские настройки')
        verbose_name_plural = ('Пользовательские настройки')

    def __str__(self):
        return 'Настройки пользователя ' + str(self.user.first_name)