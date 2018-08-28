import json

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

    # Создание комнаты
    @staticmethod
    def create_room(request):
        result = {
            'status': 200,
            'text': '',
            'invalide_name': '',
            'room_url': ''
        }
        room = Room()
        request_dump = json.dumps(request.POST, ensure_ascii=False)
        if 'dialog_name' in request.POST:
            room.name = request.POST['dialog_name']
        else:
            result['status'] = '400'
            result['text'] = 'Не заполнено название группы'
            result['invalide_name'] = 'dialog_name'

        added_users = list()
        if 'added_users' in request.POST:
            added_users = request.POST['added_users']
            added_users = added_users.split(' ')
            added_users.pop()
        else:
            result['status'] = '400'
            result['text'] = 'Не добавлено ни одного пользователя'
            result['invalide_name'] = 'added_users'
        room.creator = request.user
        room_id = room.save()
        objs = []
        for user_id in added_users:
            objs.append(RoomMembers(user_rel_id=user_id, room_rel_id=room_id, joined=False))
        RoomMembers.objects.bulk_create(objs)
        RoomMembers.invite_message(request.user, room_id, True)
        result['room_url'] = '/chats/?room=' + str(room_id)
        return result

    # Присоединение к комнате
    @staticmethod
    def join_room(request):
        result = {
            'status': 200,
            'text': '',
            'room_url': ''
        }
        try:
            if 'room_id' in request.POST:
                room_id = request.POST['room_id']
                member = RoomMembers.objects.get(user_rel=request.user, room_rel_id=room_id)
                member.joined = True
                member.save()
                last_message = ChatMessage.objects.order_by('room', '-created').filter(user=request.user,
                                                                                       room_id=room_id).distinct('room')[0]
                last_message.flags = last_message.flags - 64
                last_message.save()

                result['room_url'] = '/chats/?room=' + str(room_id)
            else:
                result['status'] = '400'
        except:
            result['status'] = '400'
        return result

    # Отклонить приглашение
    @staticmethod
    def decline_room(request):
        result = {
            'status': 200,
            'text': '',
            'room_url': '/chats/'
        }
        try:
            if 'room_id' in request.POST:
                room_id = request.POST['room_id']
                ChatMessage.objects.order_by('room', '-created').filter(user=request.user,
                                                                        room_id=room_id).distinct('room').delete()
                member = RoomMembers.objects.get(user_rel=request.user, room_rel_id=room_id)

                member.delete()
                member.save()
            else:
                result['status'] = '400'
        except:
            result['status'] = '400'
        return result

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        super(Room, self).save(force_insert=force_insert, force_update=force_update, *args, **kwargs)
        RoomMembers.objects.create(user_rel=self.creator, room_rel=self, additional_info=1)
        # RoomMembers.invite_message(self.creator, self.id, True)
        return self.id

    def get_absolute_url(self):
        result_url = ''
        if self.group is not None:
            result_url = "/group/%i" % self.group.id
        elif self.event is not None:
            result_url = "/events/%i" % self.group.id
        else:
            result_url = "javascript:vodi(0)"
        return result_url

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
    joined = models.BooleanField(default=True, blank=False)

    def __str__(self):
        return self.user_rel.first_name + ' ' + self.user_rel.last_name + ' - группа ' + self.room_rel.name

    class Meta:
        verbose_name = ('Участники чатов')
        verbose_name_plural = ('Участники чатов')

    @staticmethod
    def invite_message(user, room_id, is_invite):
        message_db = ChatMessage()
        message_db.user = user
        if is_invite:
            text = 'Присоединился к чату'
        else:
            text = 'Отключился от чата'
        message_db.text = text
        message_db.flags = 34  # Отправленное в комнату
        message_db.room_id = room_id
        message_id = message_db.save()


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
    # 64 - отправлено юзеру, который не принял запрос на чат
    # 128 - пересланное сообщение
    @staticmethod
    def message_flags(request, message):
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
        message_id = self.id
        if is_new:
            flags = convert_base(self.flags)
            if len(flags) > 4 and flags[-2] == 1:  # Если отправленное в комнату
                if flags[-6] == 1:
                    members = RoomMembers.objects.exclude(user_rel_id=self.user_id).filter(room_rel=self.room)
                    peer_msg_id = message_id
                    for member in members:
                        id = self.id
                        self.pk = None
                        self.user = member.user_rel
                        self.flags = self.flags - 2  # теперь сообщение считается входящим
                        self.peer_msg_id = peer_msg_id
                        if member.joined == False:
                            self.flags = self.flags + 64
                        super(ChatMessage, self).save(force_insert, force_update)
                return message_id
            else:
                id = self.id
                self.pk = None
                self.user, self.peer = self.peer, self.user
                self.flags = self.flags - 2  # теперь сообщение считается входящим
                self.peer_msg_id = id
                super(ChatMessage, self).save(force_insert, force_update)
                return self.id
        else:
            return

    # Редактирование сообщений
    @staticmethod
    def edit_message(user_id, message):
        dic = {
            'status': 100,
            'text': '',
            'message_id': message['edit_message_id']
        }
        try:
            edit_obj = ChatMessage.objects.get(id=message['edit_message_id'], user_id=user_id)
            edit_obj.text = message['text']
            edit_obj.flags = edit_obj.flags + 8
            edit_obj.save()
            related_messages = ChatMessage.objects.filter(peer_msg_id=message['edit_message_id'])
            for rel_message in related_messages:
                rel_message.text = message['text']
                rel_message.flags = rel_message.flags + 8
                rel_message.save()
        except ChatMessage.DoesNotExist:
            dic['status'] == 403
            dic['text'] == 'Сообщение не найдено'
        return dic

    # Редактирование сообщений TODO ПРОТЕСТИРОВАТЬ
    @staticmethod
    def delete_message(request):
        dic = {
            'status': 200,
            'text': '',
            'message_id': request.POST['message_id']
        }
        try:
            # удаление сообщения у отправителя
            delete_object = ChatMessage.objects.get(id=request.POST['message_id'], user_id=request.user.id)
            delete_object.text = '[Сообщение удалено]'
            delete_object.flags = delete_object.flags + 16
            delete_object.save()
            # удаление сообщения у тех, кому отправили
            related_messages = ChatMessage.objects.filter(peer_msg_id=request.POST['message_id'])
            for message in related_messages:
                message.text = '[Сообщение удалено]'
                message.flags = message.flags + 16
                message.save()
        except ChatMessage.DoesNotExist:
            dic['status'] == 403
            dic['text'] == 'Сообщение не найдено'
        return dic