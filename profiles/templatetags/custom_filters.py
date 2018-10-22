from django import template

from events_.models import EventMembership

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
