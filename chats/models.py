from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from events_all.helper import convert_base


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


# Flags расшифровка
# 1 - сообщение не прочитано
# 2 - исходящее
# 4 - отправленное другом
# 8 - отредактированное
# 16 - удаленное
# 32 - отправлено в комнату
# TODO добавить индексы
class ChatMessage(models.Model):
    """
    Model to represent a chat message
    """
    user = models.ForeignKey(User, related_name='user_from', on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    text_html = models.TextField(blank=True)
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

    def save(self):
        self.text_html = '<p>' + self.text + '</p>'
        super(ChatMessage, self).save()


# обработка сообщений (составление почтового ящика для каждого)
def go_subscrib(sender, instance, created, **kwargs):
    if created:
        flags = convert_base(instance.flags)
        peer_message = instance
        peer_message.pk = None
        peer_message.peer_msg = instance.pk
        if flags[len(flags) - 2] == 1:
            peer_message.user, peer_message.peer = peer_message.peer, peer_message.user
            peer_message.flags = instance.flags - 2  # теперь сообщение считается входящим
            peer_message.save()
        elif flags[len(flags) - 5] == 1:
            # TODO дописать
            array = Room.objects.filter(member=instance.user)


signals.post_save.connect(go_subscrib, sender=ChatMessage)


