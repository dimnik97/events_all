from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from django.utils.functional import curry

import datetime
import helper
from custom_profile.models import Profile
from django.db.models.signals import post_save


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField(null=True,blank=True)
    creator_id = models.ForeignKey(User, on_delete = models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=True,blank=True)
    end_time = models.DateTimeField(null=True,blank=True)
    participants = models.IntegerField(null=True,blank=True)

    def get_events():
        events = Event.objects.all()
        return events

    def __str__(self):
        return str(self.id) + '  Событие: ' + self.name + ' Создатель: ' + self.creator_id.first_name


class Event_avatar(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, default=True)
    last_update = models.DateField(null=True, blank=True, default=datetime.date.today)
    image = models.ImageField(upload_to=curry(helper.upload_to, prefix='avatar_event'),
                              default='media/avatar/default/img.jpg')

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
            obj = Event_avatar.objects.get(id=self.id)
            if obj.image.path != self.image.path:
                helper._del_mini(obj.image.path)
                obj.image.delete()
        except:
            pass
        super(Event_avatar, self).save()
        img = Image.open(self.image.path)
        img.thumbnail(
            (128, 128),
            Image.ANTIALIAS
        )
        img.save(self.mini_path)

    # Делаем свою delete с учетом миниатюры
    def delete(self, using=None):
        try:
            obj = Event_avatar.objects.get(id=self.id)
            helper._del_mini(obj.image.path)
            obj.image.delete()
        except (Event_avatar.DoesNotExist, ValueError):
            pass
        super(Event_avatar, self).delete()

    def get_absolute_url(self):
        return ('photo_detail', None, {'object_id': self.id})


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


# после создания события, создатель автоматически добавляется в участники этого события
def event_creating_post_save(sender, instance, created, **kwargs):
    if created:
        event_join = EventParty()
        event_join.user_id = instance.creator_id
        event_join.event_id = instance
        event_join.save()
post_save.connect(event_creating_post_save, sender=Event)