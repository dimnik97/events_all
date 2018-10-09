import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.functional import curry
from events_all import helper
from images_custom.models import PhotoEditor
from profiles.models import Profile


# Admin могут редактировать саму группу(название, фото, описание), добавлять и удалять редакторов, создавать посты
# Editor могут добавлять посты
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
        verbose_name = 'Роли участников группы'
        verbose_name_plural = 'Роли участников группы'


# Группы
class Group(models.Model):
    # Общая информация
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    status = models.TextField(null=True, blank=True, max_length=100)
    name = models.TextField(null=True, blank=True, max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    create_date = models.DateField(auto_now_add=True)
    # Настройки группы
    CHOICES_ACTIVE = (('1', 'Активная'),
                      ('2', 'Удаленная'),
                      ('3', 'Заблокированная'),)
    active = models.CharField(  # для бана
        max_length=2,
        choices=CHOICES_ACTIVE,
        default=1,
    )
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
        verbose_name = 'Группы'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.name

    # Проверка, является ли пользователь админом переданной группы
    @classmethod
    def is_group_admin(cls, request, group_id):
        admin = Group.objects.filter(id=group_id, creator=request.user)
        if admin.exists():
            return True
        return False

    # Проверка на возможность создавать посты
    @classmethod
    def is_editor(cls, request, group_id):
        try:
            user = Membership.objects.get(group_id=group_id, person=request.user.profile)
        except Membership.DoesNotExist:
            return False

        if user.role.role == 'admin' or user.role.role == 'editor':
            return True
        return False

    # Проверка группы на
    @classmethod
    def verification_of_rights(cls, request, group_id):
        group = Group.objects.get(id=group_id)
        is_admin = cls.is_group_admin(request, group_id)

        if group.active == '1':
            context = {'status': True}
        elif str(group.active) == '2':
            context = {
                'group': group,
                'text': 'Группа была удалена',
                'status': False,
                'is_admin': is_admin
            }
        elif str(group.active) == '3':
            context = {
                'group': group,
                'text': 'Группа была заблокирована',
                'status': False,
                'is_admin': is_admin
            }
        else:
            context = {
                'group': group,
                'text': 'Что-то пошло не так',
                'status': False,
                'is_admin': is_admin
            }
        if str(group.type) == '2':
            user = Membership.objects.filter(group=group.id, person=request.user.profile)
            if user.exists():
                context = {
                    'status': True
                }
            else:
                context = {
                    'group': group,
                    'text': 'Отправить заявку',
                    'invite': True,
                    'status': False,
                    'is_admin': is_admin
                }
        return context


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_joined = models.DateField(null=True, blank=True, default=datetime.date.today)
    role = models.ForeignKey(AllRoles, related_name="roles", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписчики группы'
        verbose_name_plural = 'Подписчики группы'

    def __str__(self):
        return str(self.group.name) + ' подписчик ' + str(self.person)

    # Подписка на пользователя
    @classmethod
    def subscribe(cls, user, group):
        Membership.objects.create(group=group,
                                  person=user.profile,
                                  role=AllRoles.objects.get(role='subscribers'))

    # Отписка от пользователя
    @classmethod
    def unsubscribe(cls, user, group):
        Membership.objects.get(group=group, person=user.profile).delete()


# Аватарки и миниатюры пользователей
class GroupAvatar(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, default=True)
    last_update = models.DateField(null=True, blank=True, default=datetime.date.today)
    image = models.ImageField(
        # upload_to=curry(helper.ImageHelper.upload_to, prefix='groups'),
        upload_to=helper.ImageHelper.upload_to,
        default='avatar/default/img.jpg')

    class Meta:
        verbose_name = 'Аватары группы'
        verbose_name_plural = 'Аватары группы'

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
            cls=GroupAvatar,
            admin_panel=admin_panel,
            image_type=image_type,
            request=request)

    def delete_photo(self, using=None):
        PhotoEditor.delete_photo(
            self_cls=self,
            using=using,
            cls=GroupAvatar
        )

    def get_absolute_url(self):
        return 'photo_detail', None, {'object_id': self.id}


