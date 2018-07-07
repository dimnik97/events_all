import datetime

from django.contrib.auth.models import User
from django.db import models

# Admin могут редактировать саму группу(название, фото, описание), добавлять и удалять редакторов, создавать посты
# Editor могут добавлять посты
from events_all import helper
from images_custom.models import PhotoEditor
from profiles.models import Profile


class AllRoles(models.Model):
    role = models.TextField(default=None)
    ru_role = models.TextField(default=None)
    able_edit = models.BooleanField()
    able_delete = models.BooleanField()

    able_create_event = models.BooleanField()
    able_edit_event = models.BooleanField()
    able_delete_event = models.BooleanField()

    def __str__(self):
        return self.role

    class Meta:
        verbose_name = ('Роли участников группы')
        verbose_name_plural = ('Роли участников группы')


# Группы
class Group(models.Model):
    # Общая информация
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    status = models.TextField(null=True, blank=True, max_length=100)
    name = models.TextField(null=True, blank=True, max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    create_date = models.DateField(auto_now_add=True)
    # Настройки группы
    active = models.BooleanField(default=True)  # для бана
    CHOICES_S = (('1', 'Открытая'),
                 ('2', 'Закрытая'))
    members = models.ManyToManyField(
        Profile,
        through='Membership',
        through_fields=('group', 'person'),
    )
    type = models.CharField(
        max_length=2,
        choices=CHOICES_S,
        default=1,
    )

    class Meta:
        verbose_name = ('Группы')
        verbose_name_plural = ('Группы')

    def __str__(self):
        return self.name


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_joined = models.DateField(null=True, blank=True, default=datetime.date.today)
    role = models.ForeignKey(AllRoles, related_name="roles", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ('Подписчики группы')
        verbose_name_plural = ('Подписчики группы')

    def __str__(self):
        return str(self.group.name) + ' подписчик ' + str(self.person)

    # Подписка на пользователя
    @classmethod
    def subscribe(cls, user, group):
        Membership.objects.create(group=group, person=user.profile, role=AllRoles.objects.get(role='subscribers'))

    # Отписка от пользователя
    @classmethod
    def unsubscribe(cls, user, group):
        Membership.objects.get(group=group, person=user.profile).delete()


# Аватарки и миниатюры пользователей
class GroupAvatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=True)
    last_update = models.DateField(null=True, blank=True, default=datetime.date.today)
    image = models.ImageField(upload_to=helper.upload_to,
                              default='avatar/default/img.jpg')

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

    def save(self, admin_panel=True, image_type='avatar', force_insert=False, force_update=False, using=None, request=None):
        PhotoEditor.save_photo(
            self_cls=self,
            cls=GroupAvatar,
            admin_panel=admin_panel,
            image_type=image_type,
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            request=request)

    def delete_photo(self, using=None):
        PhotoEditor.delete_photo(
            self = self,
            using=using,
            cls=GroupAvatar
        )

    def get_absolute_url(self):
        return ('photo_detail', None, {'object_id': self.id})


