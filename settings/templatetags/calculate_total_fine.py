from datetime import datetime

from django import template

from borrows.models import Borrow
from settings.models import Setting

register = template.Library()


@register.filter(name='calculate_total_fine')
def has_group(datas):
    total_fine = 0

    setting = Setting.objects.first()
    renew_days = setting.renew_days

    fine_amount = setting.fine_amount

    for data in datas:
        issued_date = data.issued_date
        return_date = data.return_date

        today = return_date or datetime.now().date()

        fine_days = (today - issued_date).days - renew_days

        amount = 0

        if fine_days > 0:
            amount = fine_days * fine_amount

        total_fine = total_fine + amount

    return total_fine
