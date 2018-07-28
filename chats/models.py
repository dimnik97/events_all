from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from events_all.helper import convert_base
from profiles.models import Profile


class Room(models.Model):
    """
    Model to represent a chat room
    """
    name = models.TextField(max_length=100, default=None)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    additional_info = models.IntegerField()

    def __str__(self):
        """
        String to represent the room
        """
        return self.room_to


# TODO добавить индексы
class ChatMessage(models.Model):
    """
    Model to represent a chat message
    """
    user = models.ForeignKey(User, related_name='user_from', on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    # text_html = models.TextField(blank=True)
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
            if len(flags) - 2 >= 0:
                if flags[1] == 1:
                    id = self.id
                    self.pk = None
                    self.user, self.peer = self.peer, self.user
                    self.flags = self.flags - 2  # теперь сообщение считается входящим
                    self.peer_msg_id = id
                    super(ChatMessage, self).save(force_insert, force_update)
            else:
                return


# # обработка сообщений (составление почтового ящика для каждого)
# def go_subscribe(sender, instance, created, **kwargs):
#     if created:
#         flags = convert_base(instance.flags)
#         if len(flags) - 2 >= 0:
#             if flags[1] == 1:
#                 id = instance.id
#                 instance.pk = None
#                 instance.user, instance.peer = instance.peer, instance.user
#                 instance.flags = instance.flags - 2  # теперь сообщение считается входящим
#                 instance.peer_msg_id = id
#                 instance.save()
#         else:
#             return
#         # elif flags[len(flags) - 5] == 1:
#         #     # TODO дописать
#         #     array = Room.objects.filter(member=instance.user)
#
#
# signals.post_save.connect(go_subscribe, sender=ChatMessage)


