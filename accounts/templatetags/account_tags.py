from django import template

from ..models import Relation


register = template.Library()


@register.simple_tag
def is_followed_by(user, current_user):
    return Relation.objects.filter(from_user=user, to_user=current_user).exists()
