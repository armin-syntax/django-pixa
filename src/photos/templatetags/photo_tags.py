from django import template

from ..models import Like, Save


register = template.Library()


@register.simple_tag
def is_liked_by(user, photo):
    return Like.objects.filter(user=user, photo=photo).exists()


@register.simple_tag
def is_saved_by(user, photo):
    return Save.objects.filter(user=user, photo=photo).exists()
