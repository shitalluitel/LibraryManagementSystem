from datetime import datetime

from django import template
from django.contrib.auth.models import Group

from settings.models import Setting

register = template.Library()


@register.filter(name='calculate_fine')
def has_group(date):
    setting = Setting.objects.first()
    renew_days = setting.renew_days
    fine_amount = setting.fine_amount

    today = datetime.now().date()
    fine_days = (today - date).days - renew_days

    total_fine = 0

    if fine_days > 0:
        total_fine = fine_days * fine_amount

    return total_fine
