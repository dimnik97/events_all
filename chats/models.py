from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from events_.models import Event
from events_all.helper import convert_base
from groups.models import Group
from profiles.models import Profile


class Room(models.Model):
    name = models.TextField(max_length=200, default=None)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        super(Room, self).save(force_insert=force_insert, force_update=force_update, *args, **kwargs)
        RoomMembers.objects.create(user_rel=self.creator, room_rel=self, additional_info=1)
        RoomMembers.invite_message(self.creator, self, True)

    def get_absolute_url(self):
        return "/groups/%i" % self.group.id

    def __str__(self):
        """
        String to represent the room
        """
        return self.name

    class Meta:
        verbose_name = ('Чаты (групп, евентов)')
        verbose_name_plural = ('Чаты (групп, евентов)')


class RoomMembers(models.Model):
    user_rel = models.ForeignKey(User, on_delete=models.CASCADE)
    room_rel = models.ForeignKey(Room, on_delete=models.CASCADE)
    additional_info = models.IntegerField(null=True, default=None)  # права доступа

    def __str__(self):
        return self.user_rel.first_name + ' ' + self.user_rel.last_name + ' - группа ' + self.room_rel.name

    class Meta:
        verbose_name = ('Участники чатов')
        verbose_name_plural = ('Участники чатов')

    @classmethod
    def invite_message(self, user, room, is_invite):
        message_db = ChatMessage()
        message_db.user = user
        if is_invite:
            message_db.text = 'Присоединился к чату'
        else:
            message_db.text = 'Отключился от чата'
        message_db.flags = 34  # Отправленное в комнату
        message_db.room = room
        message_db.save()


# TODO добавить индексы
class ChatMessage(models.Model):
    user = models.ForeignKey(User, related_name='user_from', on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    created = models.DateTimeField(auto_now_add=True)
    flags = models.IntegerField()
    peer = models.ForeignKey(User, related_name='user_to', on_delete=models.CASCADE, null=True, blank=True)
    peer_msg = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        String to represent the message
        """
        return self.user.first_name + "  " + str(self.created)

    class Meta:
        verbose_name = ('Сообщения')
        verbose_name_plural = ('Сообщения')

    # Flags расшифровка
    # 1 - сообщение не прочитано
    # 2 - исходящее
    # 4 - отправленное подписчику
    # 8 - отредактированное
    # 16 - удаленное
    # 32 - отправлено в комнату
    @classmethod
    def message_flags(self, request, message):
        result = 1  # Сообщение считается непрочитанным сразу
        result = result + 2  # Сообщение всегда исходящее для написавшего

        dict = {
            'status': '200',
            'error': '',
            'result': -1
        }
        if message['is_room']:
            flag = False
            members = RoomMembers.objects.filter(room_rel_id=message['peer_id'])
            for member in members:
                if member.user_rel == request.scope['user']:
                    flag = True
            if flag:
                result = result + 32
            else:
                dict['status'] = '403'
                dict['error'] = 'Вы не можете отправлять сообщения в данный чат'
                return dict
        else:
            peer = User.objects.get(id=message['peer_id'])
            if int(peer.usersettings.messages) == 3:
                dict['status'] = '403'
                dict['error'] = 'Пользователь ограничил круг общения настройками приватности'
                return dict

            flag = False
            if int(peer.usersettings.messages) == 2:
                subscribers = Profile.objects.get(user_id=message['peer_id']).subscribers.all()
                for subscriber in subscribers:
                    if subscriber.user.id == request.scope['user'].id:
                        result = result + 4
                        flag = True
                if not flag:
                    dict['status'] = '403'
                    dict['error'] = 'Пользователь ограничил круг общения настройками приватности'

            if int(peer.usersettings.messages) == 1:
                subscribers = Profile.objects.get(user=request.scope['user']).subscribers.all()
                for subscriber in subscribers:
                    if subscriber.user.id == message['peer_id']:
                        result = result + 4

        dict['result'] = result
        return dict

    def save(self, force_insert=False, force_update=False):
        is_new = self.id is None
        super(ChatMessage, self).save(force_insert, force_update)
        if is_new:
            flags = convert_base(self.flags)
            if len(flags) > 4 and flags[-2] == 1:  # Если отправленное в комнату
                if flags[-6] == 1:
                    members = RoomMembers.objects.exclude(user_rel_id=self.user_id).filter(room_rel=self.room)
                    for member in members:
                        id = self.id
                        self.pk = None
                        self.user = member.user_rel
                        self.flags = self.flags - 2  # теперь сообщение считается входящим
                        self.peer_msg_id = id
                        super(ChatMessage, self).save(force_insert, force_update)
            else:
                id = self.id
                self.pk = None
                self.user, self.peer = self.peer, self.user
                self.flags = self.flags - 2  # теперь сообщение считается входящим
                self.peer_msg_id = id
                super(ChatMessage, self).save(force_insert, force_update)
                return
        else:
            return

