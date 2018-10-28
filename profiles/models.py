import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.http import Http404
from django.middleware.csrf import get_token
from django.utils.functional import curry
from django_ipgeobase.models import IPGeoBase

from cities_.models import CityTable
from events_all import helper
from events_all.helper import parse_from_error_to_json
from images_custom.models import PhotoEditor
from profiles.forms import EditProfile, EditUserSettings
from profiles.validator import SignupValidator


# Получение общей информации для юзера
class Users:
    # Определение IP юзера
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def signup_check(request):
        return SignupValidator.email_and_password(request)

    @staticmethod
    def get_user_locations(request, need_ip=False):
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
        if request.user.is_authenticated and need_ip is False:
            try:
                city_obj = CityTable.objects.get(city=request.user.profile.location_name)
            except CityTable.DoesNotExist:
                city_obj = CityTable.objects.get(city='Москва')  # TODO Так вообще можно?
            return city_obj
        else:
            ip = "212.49.98.48"
            # ip = Users.get_client_ip(request)  # TODO При переносе
            ipgeobases = IPGeoBase.objects.by_ip(ip)
            if ipgeobases.exists():
                return ipgeobases[0]
        raise Http404


# Доп данные для юзера
class Profile(models.Model):
    CHOICES_M = (('1', 'Мужчина'),
                 ('2', 'Женщина'),)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.TextField(null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(
        max_length=2,
        choices=CHOICES_M,
        default=1,
    )
    through_profile = models.ManyToManyField(
        'self',
        through='ProfileSubscribers',
        through_fields=('from_profile', 'to_profile'),
        symmetrical=False
    )
    CHOICES_ACTIVE = (('1', 'Активный'),
                      ('2', 'Удаленный'),
                      ('3', 'Заблокированный'),)
    active = models.CharField(  # для бана
        max_length=2,
        choices=CHOICES_ACTIVE,
        default=1,
    )
    location = models.ForeignKey(CityTable, to_field='city_id', on_delete=models.CASCADE, default=2732)
    location_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'Профили'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' (' + self.user.username + ')'

    # Создание юзера
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    # Сохранение юзера
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    @staticmethod
    def edit(request):
        user = request.user
        if request.method == 'POST':
            if request.POST['type'] == 'main_info':
                form = EditProfile(request.POST)
            elif request.POST['type'] == 'settings':
                form = EditUserSettings(request.POST)
            if form.is_valid():
                form.save(request)
            else:
                data = parse_from_error_to_json(request, form)
                return data, True
            if request.is_ajax:
                return True, True

        form = EditProfile({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'birth_date': user.profile.birth_date.strftime('%d-%m-%Y'),
            'phone': user.profile.phone,
            'description': user.profile.description,
            'gender': user.profile.gender
        })
        form_private = EditUserSettings({
            'messages':
                user.usersettings.messages,
            'birth_date':
                user.usersettings.birth_date,
            'invite':
                user.usersettings.invite,
            'near_invite':
                user.usersettings.near_invite,
        })
        context = {
            'title': 'Профиль',
            'form': form,
            'form_private': form_private,
            "csrf_token": get_token(request),
            'avatar': ProfileAvatar.objects.get(user=request.user.id)
        }
        return context, False

    # Возвращает абсолютный URL
    def get_absolute_url(self):
        return "/profile/%i" % self.user.id


class ProfileSubscribers(models.Model):
    from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='from_p')
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_p')
    date_subscribe = models.DateField(null=True, blank=True, default=datetime.date.today)

    class Meta:
        verbose_name = 'Подписчики'
        verbose_name_plural = 'Подписчики'

    # Подписка на пользователя
    @classmethod
    def make_friend(cls, request, new_friend):
        try:
            ProfileSubscribers.objects.create(from_profile=request.user.profile, to_profile=new_friend.profile)
        except ProfileSubscribers:
            raise Http404

    # Отписка от пользователя
    @classmethod
    def remove_friend(cls, request, new_friend):
        try:
            ProfileSubscribers.objects.get(from_profile=request.user.profile, to_profile=new_friend.profile).delete()
        except ProfileSubscribers.DoesNotExist:
            raise Http404

    @staticmethod
    def get_subscribers(request):
        if 'user' in request.GET:
            user_id = request.GET.get('user', 1)
        else:
            user_id = request.user.id

        flag = False
        action = ''  # Просмотр
        if 'action' in request.GET:
            action = request.GET.get('action')  # Тип - выбор подписчиков (с чекбоксами)
        else:
            if str(request.user.id) == str(user_id):
                action = 'context_menu'  # Тип - контекстное меню

        user = User.objects.get(id=user_id)
        if 'value' in request.POST and 'search' in request.POST:
            from django.db.models import Q
            subscribers_object = ProfileSubscribers.objects.filter(
                Q(to_profile__user__last_name__icontains=request.POST['value'])
                | Q(to_profile__user__first_name__icontains=request.POST['value']),
                from_profile=user.profile).select_related('from_profile__user__profileavatar'
                                                          , 'to_profile__user__profileavatar')
            flag = True
        else:
            subscribers_object = ProfileSubscribers.objects.filter(from_profile=user.profile) \
                .select_related('from_profile__user__profileavatar', 'to_profile__user__profileavatar')

        subscribers = [
            subscriber.to_profile for subscriber in subscribers_object.all()
        ]

        subscribers = helper.helper_paginator(request, subscribers)

        return {
            'flag': flag,
            'items': subscribers,
            'user_id': user_id,
            'action': action,
            'type': 'subscribers'
        }

    @staticmethod
    def get_followers(request):
        if 'user' in request.GET:
            user_id = request.GET.get('user', 1)
        else:
            user_id = request.user.id
        flag = False
        user = User.objects.get(id=user_id)
        if 'value' in request.POST and 'search' in request.POST:
            from django.db.models import Q
            followers_object = ProfileSubscribers.objects.filter(Q(user__first_name__istartswith=request.POST['value'])
                                                                 |Q(user__last_name__istartswith=request.POST['value']),
                                                                 to_profile=user.profile) \
                .select_related('from_profile__user__profileavatar',
                                'to_profile__user__profileavatar')
            flag = True
        else:
            followers_object = ProfileSubscribers.objects.filter(to_profile=user.profile) \
                .select_related('from_profile__user__profileavatar', 'to_profile__user__profileavatar')

        followers = [
            follower.to_profile for follower in followers_object.all()
        ]
        followers = helper.helper_paginator(request, followers)

        return {
            'flag': flag,
            'items': followers,
            'user_id': user_id,
            'action': False,
            'type': 'followers'
        }


# Аватарки и миниатюры пользователей
class ProfileAvatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=True)
    last_update = models.DateField(null=True, blank=True, default=datetime.date.today)
    image = models.ImageField(
        upload_to=curry(helper.ImageHelper.upload_to, prefix='avatar'),
        # upload_to=helper.ImageHelper.upload_to,
        default='avatar/default/img.jpg')

    class Meta:
        verbose_name = 'Аватары'
        verbose_name_plural = 'Аватары'

    # Добавляем к свойствам объектов модели путь к миниатюре
    def _get_mini_path(self):
        return helper.ImageHelper.add_mini(self.image.path, postfix='mini')

    # Добавляем к свойствам объектов модели урл миниатюры
    def _get_mini_url(self):
        return helper.ImageHelper.add_mini(self.image.url, postfix='mini')

    # Добавляем к свойствам объектов модели путь к миниатюре
    def _get_reduced_path(self):
        return helper.ImageHelper.add_mini(self.image.path, postfix='reduced')

    # Добавляем к свойствам объектов модели урл миниатюры
    def _get_reduced_url(self):
        return helper.ImageHelper.add_mini(self.image.url, postfix='reduced')

    mini_path = property(_get_mini_path)
    mini_url = property(_get_mini_url)
    reduced_path = property(_get_reduced_path)
    reduced_url = property(_get_reduced_url)

    def save(self, admin_panel=True, image_type='avatar', force_insert=False, force_update=False, using=None, request=None):
        PhotoEditor.save_photo(
            self_cls=self,
            cls=ProfileAvatar,
            admin_panel=admin_panel,
            image_type=image_type,
            request=request)

    def delete_photo(self, using=None):
        PhotoEditor.delete_photo(
            self=self,
            using=using,
            cls=ProfileAvatar
        )

    def get_absolute_url(self):
        return 'photo_detail', None, {'object_id': self.id}


# Настройки юзера
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
        verbose_name = 'Пользовательские настройки'
        verbose_name_plural = 'Пользовательские настройки'

    def __str__(self):
        return 'Пользовательские настройки ' + str(self.user.first_name)