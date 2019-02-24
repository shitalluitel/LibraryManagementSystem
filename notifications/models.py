from django.db import models


# Create your models here.
from users.models import User


class Notification(models.Model):
    message = models.TextField(max_length=512)
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.DO_NOTHING)
