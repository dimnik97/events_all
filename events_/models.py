from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from django.utils.functional import curry

import datetime
from events_all import helper
from groups.models import Group
from django.db.models.signals import post_save


class EventCategory(models.Model):
    name = models.CharField(max_length = 30)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + " " + str(self.name)

class EventStatus(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return str(self.id) + " " + str(self.name)


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    participants = models.IntegerField(null=True, blank=True)
    status = models.ForeignKey(EventStatus, on_delete=models.CASCADE, default=1)
    created_by_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def get_events():
        events = Event.objects.all()
        return events

    def __str__(self):
        return str(self.id) + '  Событие: ' + self.name + ' Создатель: ' + self.creator_id.first_name


# после создания события, создатель автоматически добавляется в участники этого события
def event_creating_post_save(sender, instance, created, **kwargs):
    if created:
        EventParty.subscr_to_event(instance, instance.creator_id)


post_save.connect(event_creating_post_save, sender=Event)


class EventNews(models.Model):
    text = models.TextField(null=True,blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    news_creator = models.ForeignKey(User, on_delete = models.CASCADE)
    news_event = models.ForeignKey(Event, on_delete = models.CASCADE)

    # def save(self, request):



class Event_avatar(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, default=True)
    last_update = models.DateField(null=True, blank=True, default=datetime.date.today)
    image = models.ImageField(
        upload_to=curry(helper.upload_to, prefix='avatar_event'),
        # upload_to=helper.upload_to,
                              default='avatar_event/default/img.jpg')

    class Meta:
        verbose_name = ('Аватары')
        verbose_name_plural = ('Аватары')

    # Добавляем к свойствам объектов модели путь к миниатюре
    def _get_mini_path(self):
        return helper._add_mini(self.image.path, postfix='mini')

    # Добавляем к свойствам объектов модели урл миниатюры
    def _get_mini_url(self):
        return helper._add_mini(self.image.url, postfix='mini')

    # Добавляем к свойствам объектов модели путь к миниатюре
    def _get_reduced_path(self):
        return helper._add_mini(self.image.path, postfix='reduced')

    # Добавляем к свойствам объектов модели урл миниатюры
    def _get_reduced_url(self):
        return helper._add_mini(self.image.url, postfix='reduced')

    mini_path = property(_get_mini_path)
    mini_url = property(_get_mini_url)
    reduced_path = property(_get_reduced_path)
    reduced_url = property(_get_reduced_url)

    mini_url = property(_get_mini_url)

    # Создаем свою save
    # Добавляем:
    # - создание миниатюры
    # - удаление миниатюры и основного изображения
    #   при попытке записи поверх существующей записи
    def save(self, force_insert=False, force_update=False, using=None):
        try:
            obj = Event_avatar.objects.get(id=self.id)
            if obj.image.path != self.image.path:
                helper._del_mini(obj.image.path, postfix='mini')
                helper._del_mini(obj.image.path, postfix='reduced')
                if 'default' not in obj.image:
                    obj.image.delete()
        except:
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
            helper._del_mini(obj.image.path, postfix='mini')
            helper._del_mini(obj.image.path, postfix='reduced')
            obj.image.delete()
        except (Event_avatar.DoesNotExist, ValueError):
            pass
        super(Event_avatar, self).delete()


class EventParty(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ManyToManyField(User)
    event_id = models.ForeignKey(Event, on_delete = models.CASCADE)

    @classmethod
    def subscr_to_event(cls, ev_id, u_id):
        eventparty, created = cls.objects.get_or_create(
            event_id=ev_id
        )
        eventparty.user_id.add(u_id)

    @classmethod
    def unsubscr_from_event(cls, ev_id, u_id):
        eventparty, created = cls.objects.get_or_create(
            event_id=ev_id
        )
        eventparty.user_id.remove(u_id)

    def __str__(self):
        return self.event_id.name

