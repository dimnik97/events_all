from django import template

from events_.models import EventMembership, EventViews, EventLikes
from events_all import helper
from groups.models import Membership

register = template.Library()


@register.filter
def count(members):
    return members.count()


@register.filter
def is_subscribe(event_id, arg):
    try:
        EventMembership.objects.get(person=arg.profile, event_id=event_id)
        return True
    except:
        return False


@register.filter
def is_subscribe_group(group_id, arg):
    try:
        Membership.objects.get(person=arg.profile, group_id=group_id)
        return True
    except:
        return False


@register.filter
def view(event_id):
    return EventViews.objects.filter(event_id=event_id).count()


@register.filter
def likes(event_id):
    return EventLikes.objects.filter(event_id=event_id).count()


@register.filter
def ev_send(event_id):
    cnt = EventMembership.objects.filter(event_id=event_id, role__role='send').count()
    if cnt == 0:
        cnt = ''
    else:
        cnt = '(' + str(cnt) + ')'
    return cnt


@register.filter
def ev_inv(event_id):
    cnt = EventMembership.objects.filter(event_id=event_id, role__role='invite').count()
    if cnt == 0:
        cnt = ''
    else:
        cnt = '(' + str(cnt) + ')'
    return cnt


@register.filter
def others(length):
    length = length - 3
    if length > 10:
        res = '< 10'
    else:
        res = '+' + str(length)
    return res


@register.filter
def like(event_id, user):
    try:  # если неавторизован
        if EventLikes.objects.filter(event_id=event_id, user=user).exists():
            return 'src=/static/img/star.svg data-like=unlike'   # Лайк стоит        убрать Хардкод # TODO
        return 'src=/static/img/star_empty.svg data-like=like'   # Лайк не стоит       убрать Хардкод # TODO
    except:
        return 'src=/static/img/star_empty.svg data-like=like'   # Лайк не стоит     убрать Хардкод # TODO


# Проверка ролей для групп
@register.filter
def ru_role(group, profile_id):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("""SELECT r.ru_role FROM groups_membership m
                        left join groups_allroles r on m.role_id = r.id
                        where m.group_id = %s 
                        and ( r.role = 'admin' or r.role = 'editor') 
                        and m.person_id = %s""", [group.id, profile_id])

    row = helper.dictfetchall(cursor)
    try:
        return row[0]['ru_role']
    except IndexError:
        return ''