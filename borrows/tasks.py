from __future__ import absolute_import, unicode_literals

from datetime import datetime
import random
from celery.task import task
from django.db import transaction

# from notifications.models import Notification
from notifications.signals import notify

from settings.models import Setting, User
from .models import Borrow


@task(name="calculate_fine")
@transaction.atomic
def calculate_fine():
    borrows = Borrow.objects.filter(status='approved', notified=False)
    setting = Setting.objects.first()
    # list_msg = []
    for data in borrows:
        issued_date = data.issued_date
        today = datetime.now().date()

        fine_days = (today - issued_date).days - setting.renew_days

        if fine_days > 0:
            # notification = Notification(
            #     message="Renew date for book {} exceeded".format(data.book_unit.book_code),
            #     user=data.student.user
            # )
            # notification.save()

            notify.send(User.objects.filter(is_admin=True).first(), recipient=data.student.user,
                        verb='Fine Notification',
                        description="Renew date for book {} exceeded".format(data.book_unit.book_code))

            data.notified = True
            data.save()

    # return list_msg
