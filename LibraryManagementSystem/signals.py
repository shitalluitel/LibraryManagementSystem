from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from LibraryManagementSystem.middleware import RequestMiddleware

from users.models import Logs


# this receiver is executed every-time some data is saved in any table

@receiver(pre_save)
def audit_log(sender, instance, **kwargs):
    # code to execute before every model save

    try:
        request = RequestMiddleware(get_response=None)
        table = sender._meta.verbose_name
        request = request.thread_local.current_request
        user = request.user

        if instance.pk and instance.is_deleted == False:
            user = user
            message = "Edited {}".format(instance)
            Logs(user=user, message=message, table=table).save()
            print("Edit")
        elif not instance.pk and instance.is_deleted == False:
            user = user
            message = "Created {}".format(instance)
            Logs(user=user, message=message, table=table).save()
        elif instance.pk and instance.is_deleted:
            user = user
            message = "Deleted {}".format(instance)
            Logs(user=user, message=message, table=table).save()
    except:
        pass


@receiver(post_delete)
def audit_delete_log(sender, instance, **kwargs):
    # code to execute before every model save
    try:
        if instance.pk:
            print("Delete ")
    except:
        pass
