from django import template

from events_all.helper import convert_base

register = template.Library()


# Если сообщение исходящее - меняем имя отправителя на имя пользователя
@register.filter
def income_or_outgoing(chat):
    flags = convert_base(chat.flags)
    if len(flags) > 1 and flags[1] == 1:
        return fullname(chat.user)
    return fullname(chat.peer)


@register.filter
def income_or_outgoing_id(chat):
    flags = convert_base(chat.flags)
    if len(flags) > 1 and flags[1] == 1:
        return chat.user.id
    return chat.peer.id


@register.filter
def income_or_outgoing_image(chat):
    flags = convert_base(chat.flags)
    if len(flags) > 1 and flags[1] == 1:
        return chat.user.profileavatar.mini_url
    return chat.peer.profileavatar.mini_url


@register.filter
def fullname(user):
    return user.first_name + ' ' + user.last_name