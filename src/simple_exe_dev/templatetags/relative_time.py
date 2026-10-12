from datetime import datetime

from django import template
from django.utils import timezone
from django.utils.timesince import timesince, timeuntil

register = template.Library()


@register.filter
def relative(value: datetime) -> str:
    """'in 3 hours' or '3 hours ago', to the largest unit only."""
    if value > timezone.now():
        return f'in {timeuntil(value, depth=1)}'
    return f'{timesince(value, depth=1)} ago'
