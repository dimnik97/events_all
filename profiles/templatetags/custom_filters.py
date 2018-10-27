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


@register.filter
def like(event_id, user):
    try:
        if EventLikes.objects.filter(event_id=event_id, user=user).exists():
            return 'src=/static/img/star.svg data-like=unlike'   # Лайк стоит убрать Хардкод # TODO
        return 'src=/static/img/star_empty.svg data-like=like'   # Лайк стоит, убрать Хардкод # TODO
    except:
        return 'src=/static/img/star_empty.svg data-like=like'   # Лайк не стоит убрать Хардкод # TODO
