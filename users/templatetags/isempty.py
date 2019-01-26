from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def isempty(value):
    if len(value) > 1:
        return True
    else:
        return False
