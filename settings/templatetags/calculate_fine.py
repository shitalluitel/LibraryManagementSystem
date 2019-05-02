from datetime import datetime

from django import template
from django.contrib.auth.models import Group

from borrows.models import Borrow
from settings.models import Setting

register = template.Library()


@register.filter(name='calculate_fine')
def calculate_fine(id):
    try:
        data = Borrow.objects.get(id=id)
    except Borrow.DoesNotExist:
        return 0

    issued_date = data.issued_date
    return_date = data.return_date

    setting = Setting.objects.first()
    renew_days = setting.renew_days
    fine_amount = setting.fine_amount

    today = return_date or datetime.now().date()
    fine_days = (today - issued_date).days - renew_days

    total_fine = 0

    if fine_days > 0:
        total_fine = fine_days * fine_amount

    print("User: {}, issued date: {} , fine: {}, fine days: {}, today: {}".format(data.student.name, data.issued_date,
                                                                                  total_fine, fine_days, today))

    return total_fine
