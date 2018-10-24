from django import template

from events_.models import EventMembership, EventViews, EventLikes

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
def view(event_id):
    return EventViews.objects.filter(event_id=event_id).count()


@register.filter
def likes(event_id):
    return EventLikes.objects.filter(event_id=event_id).count()
