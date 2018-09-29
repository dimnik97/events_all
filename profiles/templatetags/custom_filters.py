from django import template

register = template.Library()


@register.filter
def count(members):
    return members.count()
