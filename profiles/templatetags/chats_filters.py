from django import template

from events_all.helper import convert_base

register = template.Library()


# Если сообщение исходящее - меняем имя отправителя на имя пользователя
# TODO Как будет нечего делать - заменить эти 3 метода на один большой
@register.filter
def income_or_outgoing(chat):
    flags = convert_base(chat.flags)
    if len(flags) > 4 and flags[-6] == 1:
        return fullname(chat.user)
    if len(flags) > 1 and flags[-2] == 1:
        return fullname(chat.user)
    return fullname(chat.peer)


@register.filter
def income_or_outgoing_id(chat):
    flags = convert_base(chat.flags)
    if len(flags) > 4 and flags[-6] == 1:
        return fullname(chat.user)
    if len(flags) > 1 and flags[-2] == 1:
        return fullname(chat.user)
    return chat.peer.id


@register.filter
def income_or_outgoing_image(chat):
    flags = convert_base(chat.flags)
    if len(flags) > 1 and flags[-2] == 1:
        return chat.user.profileavatar.mini_url
    return chat.peer.profileavatar.mini_url


@register.filter
def fullname(user):
    return user.first_name + ' ' + user.last_name


@register.filter
def status(peer):
    return peer['status']


@register.filter
def message_flag(chat):
    flags = convert_base(chat.flags)
    result = ''
    if len(flags) == 7 and flags[-7] == 1:
        result = 'blocked'  # Заблокировано до того момента, пока пользователь не вступит в чат
    elif len(flags) == 8 and flags[-7] == 1:
        result = 'repost'  # Репост
    return result


@register.filter
def except_text(peer):
    return peer['text']