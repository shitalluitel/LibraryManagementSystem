from datetime import datetime

from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='calculate_fine')
def has_group(date):
    today = datetime.now().date()
    fine_days = (today - date).days
    # days = fine_day
    total_fine = 0
    if fine_days > 15:
        total_fine = fine_days * 5

    return total_fine
