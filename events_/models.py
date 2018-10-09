import json

from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.functional import curry

import datetime

from cities_.models import CityTable
from events_all import helper
from groups.models import Group

from profiles.models import Profile


class EventCategory(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + " " + str(self.name)

    class Meta:
        verbose_name = 'Категории событий'
        verbose_name_plural = 'Категории событий'


class EventStatus(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + " " + str(self.name)

    class Meta:
        verbose_name = 'Статус события'
        verbose_name_plural = 'Статус события'


class EventGeo(models.Model):
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    name = models.TextField(null=True, blank=True, max_length=100)

    def __str__(self):
        return str(self.lat) + " " + str(self.lng) + " " + str(self.name)

    class Meta:
        verbose_name = 'Гео меметки'
        verbose_name_plural = 'Гео метки'


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    participants = models.IntegerField(null=True, blank=True)  # Это поле точно нужно?
    status = models.ForeignKey(EventStatus, on_delete=models.CASCADE, default=1)
    created_by_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    members = models.ManyToManyField(
        Profile,
        through='EventMembership',
        through_fields=('event', 'person'),
    )
    category = models.ManyToManyField(
        EventCategory,
        through='EventCategoryRelation',
        through_fields=('event', 'category'),
    )
    geo_point = models.ForeignKey(EventGeo, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(CityTable, to_field='city_id', on_delete=models.CASCADE, default=None)
    location_name = models.CharField(max_length=100, null=True, blank=True)
    CHOICES_ACTIVE = (('1', 'Активный'),
                      ('2', 'Закрытый'),
                      ('3', 'Удаленный'),
                      ('4', 'Заблокированный'),)
    active = models.CharField(  # для бана
        max_length=2,
        choices=CHOICES_ACTIVE,
        default=1,
    )
    last_update = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'События'
        verbose_name_plural = 'События'

    # Получение эвентов с учетом фильтрации
    @staticmethod
    def get_events(request):
        from django.db.models import Q
        q_objects = Q()

        if 'category' in request.POST and request.POST['category'] != '':
            q_objects.add(Q(category=request.POST['category']), Q.AND)

        if 'location' in request.POST and request.POST['location'] != '':
            if int(request.POST['location']) > 0:
                q_objects.add(Q(location=request.POST['location']), Q.AND)

        if 'name' in request.POST and request.POST['name'] != '':
            q_objects.add(Q(name__icontains=request.POST['name']), Q.AND)

        from datetime import datetime
        if 'start_time' in request.POST and request.POST['start_time'] != '':
            start_time = datetime.utcfromtimestamp(int(request.POST['start_time'])/1000)
            q_objects.add(Q(start_time__gte=str(start_time)), Q.AND)
            # q_objects.add(Q(end_time__lte=datetime.strptime(request.POST['start_time'],
            # "%a, %d %b %Y %H:%M:%S %Z")), Q.OR)

        if 'end_time' in request.POST and request.POST['end_time'] != '':
            end_time = datetime.utcfromtimestamp(int(request.POST['end_time']) / 1000)
            q_objects.add(Q(start_time__lte=str(end_time)), Q.AND)

        q_objects.add(Q(active='1'), Q.AND)  # Не показывать в общей ленте закрытые события
        try:
            events = Event.objects.filter(q_objects). \
                only('name', 'creator_id__first_name', 'description',
                     'creator_id__last_name', 'created_by_group', 'created_by_group__name',
                     'start_time', 'end_time', 'geo_point__lat', 'geo_point__lng', 'geo_point__name',
                     'category__name', 'active'). \
                select_related('event_avatar', 'creator_id', 'creator_id__profileavatar',
                               'created_by_group__groupavatar'). \
                order_by('-last_update')
        except Event.DoesNotExist:
            return None
        return events

    def __str__(self):
        return str(self.id) + '  Событие: ' + self.name + ' Создатель: ' + self.creator_id.first_name


class EventCategoryRelation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Связка Категории событий'
        verbose_name_plural = 'Связка Категории событий'


class EventMembership(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_joined = models.DateField(null=True, blank=True, default=datetime.date.today)

    class Meta:
        verbose_name = 'Подписчики события'
        verbose_name_plural = 'Подписчики события'

    def __str__(self):
        return str(self.event.name) + ' подписчик ' + str(self.person)

    # Подписка на пользователя
    @classmethod
    def subscribe(cls, event, user):
        cls.objects.create(event=event, person=user.profile)

    # Отписка от пользователя
    @classmethod
    def unsubscribe(cls, event, user):
        cls.objects.get(event=event, person=user.profile).delete()

    # Список подписанных на событие
    @staticmethod
    def get_subscribers(request):
        if 'event' in request.GET:
            event_id = request.GET.get('event', 1)

            flag = False
            action = ''  # Просмотр

            event = Event.objects.get(id=event_id)
            if 'value' in request.POST and 'search' in request.POST:
                from django.db.models import Q
                subscribers = EventMembership.objects.filter(Q(person__user__last_name__icontains=request.POST['value']) | Q(
                    person__user__first_name__icontains=request.POST['value']), event=event)

                subscribers_object = subscribers
                subscribers = [
                    subscriber.person for subscriber in subscribers_object.all()
                ]
                flag = True
            else:
                subscribers_object = event.members
                subscribers = [
                    subscriber for subscriber in subscribers_object.all()
                ]

            page = request.GET.get('page', 1)
            paginator = Paginator(subscribers, 20)
            try:
                subscribers = paginator.page(page)
            except PageNotAnInteger:
                subscribers = paginator.page(1)
            except EmptyPage:
                subscribers = paginator.page(paginator.num_pages)

            return {
                'flag': flag,
                'items': subscribers,
                'user_id': event_id,
                'action': action,
                'type': 'subscribers',
                'is_profile': False
            }


class EventNews(models.Model):
    text = models.TextField(null=True, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    news_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    news_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    news_group = models.ForeignKey(Group, on_delete=models.CASCADE)
    news_image = models.ImageField(
        upload_to=curry(helper.ImageHelper.upload_to, prefix='news_img'),
        # upload_to=helper.ImageHelper.upload_to,
        default='avatar_event/default/img.jpg'
    )

    # Проверка прав на сохранение новости, проверка на количество новостей
    @staticmethod
    def check_rights_and_create_news(request, form):
        result = {
            'text': '',
            'creator': '',
            'status': 200,
        }
        if 'event_id' in request.POST:
            event_detail = get_object_or_404(Event, id=request.POST['event_id'])  # Получение эвента
            if event_detail.creator_id == request.user:  # Проверка на создателя
                date_from = datetime.datetime.now() - datetime.timedelta(days=1)
                if EventNews.objects.filter(news_event=event_detail, create_time__gte=date_from).count() < 5:
                    result = form.save(request, event_detail)
                    return HttpResponse(json.dumps(result))
                else:
                    result['status'] = 400
                    result['text'] = 'Количество новостей за день превышает 5'
                    return HttpResponse(json.dumps(result))
            elif event_detail.created_by_group:  # Проверка на то, что создано от группы
                is_editor = False
                if event_detail.created_by_group:
                    is_editor = Group.is_editor(request, event_detail.created_by_group.id)
                if is_editor == 1:
                    result = form.save(request, event_detail)
                    return HttpResponse(json.dumps(result))
                else:
                    result['status'] = 400
                    result['text'] = 'Вы не являетесь редактором от группы'
            else:
                result['status'] = 400
                result['text'] = 'Вы не являетесь создателем и не редактором от группы'
                return HttpResponse(json.dumps(result))
        else:
            result['status'] = 400
            result['text'] = 'Ошибка'
            return HttpResponse(json.dumps(result))

    class Meta:
        verbose_name = 'Новости событий'
        verbose_name_plural = 'Новости событий'

    # Добавляем к свойствам объектов модели путь к миниатюре
    def _get_reduced_path(self):
        return helper.ImageHelper.add_mini(self.news_image.path, postfix='reduced')

    # Добавляем к свойствам объектов модели урл миниатюры
    def _get_reduced_url(self):
        return helper.ImageHelper.add_mini(self.news_image.url, postfix='reduced')

    reduced_path = property(_get_reduced_path)
    reduced_url = property(_get_reduced_url)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            obj = EventNews.objects.get(id=self.id)
            if obj.news_image.path != self.news_image.path:
                helper.ImageHelper.del_mini(obj.news_image.path, postfix='reduced')
                if 'default' not in obj.news_image:
                    obj.image.delete()
        except EventNews.DoesNotExist:
            pass

        super(EventNews, self).save()
        reduced = Image.open(self.news_image.path)
        reduced = helper.create_medium_image(reduced)

        quality_val = 85
        reduced.save(self.reduced_path, quality=quality_val, optimize=True, progressive=True)

    def get_absolute_url(self):
        return "/groups/%i" % self.news_group.id


class Event_avatar(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, default=True)
    last_update = models.DateField(null=True, blank=True, default=datetime.date.today)
    image = models.ImageField(
        upload_to=curry(helper.ImageHelper.upload_to, prefix='avatar_event'),
        # upload_to=helper.ImageHelper.upload_to,
        default='avatar_event/default/img.jpg')

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

    # Создаем свою save
    # Добавляем:
    # - создание миниатюры
    # - удаление миниатюры и основного изображения
    #   при попытке записи поверх существующей записи
    def save(self, force_insert=False, force_update=False, using=None):
        try:
            obj = Event_avatar.objects.get(id=self.id)
            if obj.image.path != self.image.path:
                helper.ImageHelper.del_mini(obj.image.path, postfix='mini')
                helper.ImageHelper.del_mini(obj.image.path, postfix='reduced')
                if 'default' not in obj.image:
                    obj.image.delete()
        except Event_avatar.DoesNotExist:
            pass

        super(Event_avatar, self).save()
        mini = Image.open(self.image.path)
        reduced = Image.open(self.image.path)
        mini = helper.create_mini_image(mini)
        reduced = helper.create_medium_image(reduced)

        quality_val = 85
        mini.save(self.mini_path, quality=quality_val, optimize=True, progressive=True)
        reduced.save(self.reduced_path, quality=quality_val, optimize=True, progressive=True)

    # Делаем свою delete с учетом миниатюры

    def delete(self, using=None):
        try:
            obj = Event_avatar.objects.get(id=self.id)
            helper.ImageHelper.del_mini(obj.image.path, postfix='mini')
            helper.ImageHelper.del_mini(obj.image.path, postfix='reduced')
            obj.image.delete()
        except (Event_avatar.DoesNotExist, ValueError):
            pass
        super(Event_avatar, self).delete()


class EventParty(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ManyToManyField(User)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

    @classmethod
    def subscr_to_event(cls, ev_id, u_id):
        event_party, created = cls.objects.get_or_create(
            event_id=ev_id
        )
        event_party.user_id.add(u_id)

    @classmethod
    def unsubscr_from_event(cls, ev_id, u_id):
        event_party, created = cls.objects.get_or_create(
            event_id=ev_id
        )
        event_party.user_id.remove(u_id)

    def __str__(self):
        return self.event_id.name
