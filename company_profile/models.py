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
class Group(models.Model):
    # Общая информация
    creator = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(null=True, blank=True, max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    create_date = models.DateField(auto_now_add=True)
    phone = models.TextField(null=True, blank=True)
    # Настройки группы
    CHOICES_S = (('1', 'Открытая'),
                 ('2', 'Закрытая'))

    type = models.CharField(
        max_length=2,
        choices=CHOICES_S,
        default=1,
    )

    class Meta:
        verbose_name = ('Группы')
        verbose_name_plural = ('Группы')

    def __str__(self):
        return self.group.name


# Подписчики группы
class GroupSubscribers(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ManyToManyField(User)
    group_id = models.ForeignKey(Group, related_name="owner", null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ('Подписчики группы')
        verbose_name_plural = ('Подписчики группы')

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
        return "/group/%i/" % user_id