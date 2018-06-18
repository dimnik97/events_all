from django.contrib.auth.models import User
from django.db import models


# Что должно быть у группы
# Название
# Описание
# Подписчики
# Аватарка
# Возможность подписаться
# Настройки группы

# Группы
from profiles.models import Profile


class Group(models.Model):
    # Общая информация
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    # status = models.TextField(null=True, blank=True, max_length=100)
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
    inviter = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="membership_invites",
    )
    invite_reason = models.CharField(max_length=64)


# Admin могут редактировать саму группу(название, фото, описание), добавлять и удалять редакторов, создавать посты
# Editor могут добавлять посты
class AllRoles(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.TextField(User)
    able_edit = models.BooleanField()
    able_delete = models.BooleanField()

    able_create_event = models.BooleanField()
    able_edit_event = models.BooleanField()
    able_delete_event = models.BooleanField()


# Подписчики группы
class GroupSubscribers(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ManyToManyField(User)
    group_id = models.ForeignKey(Group, related_name="owner", null=True, on_delete=models.CASCADE)
    role = models.ForeignKey(AllRoles, related_name="roles", on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = ('Подписчики группы')
        verbose_name_plural = ('Подписчики группы')

    @classmethod
    def subscribe(cls, group_id, user_id):
        subscribers, created = cls.objects.get_or_create(
            group_id=group_id
        )
        subscribers.user_id.add(user_id)

    @classmethod
    def unsubscribe(cls, group_id, user_id):
        subscribers, created = cls.objects.get_or_create(
            group_id=group_id
        )
        subscribers.user_id.remove(user_id)

    # Возвращает абсолютный URL
    @models.permalink
    def get_absolute_url(user_id):
        return "/group/%i/" % user_id



