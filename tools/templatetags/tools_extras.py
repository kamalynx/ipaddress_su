from collections.abc import Iterable

from django import template


register = template.Library()


@register.filter
def is_iterable(data):
    return isinstance(data, Iterable) and not isinstance(data, str)
