from django.utils import timezone
from django.utils.timesince import timesince


def get_time_since(dt):
    delta = timezone.now() - dt

    if delta.total_seconds() < 60:
        return 'now'

    return f'{timesince(dt, timezone.now()).split(',')[0]} ago'
