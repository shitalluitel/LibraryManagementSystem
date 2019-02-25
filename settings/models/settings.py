from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from users.models import User


class Setting(models.Model):
    renew_days = models.PositiveIntegerField(default=15)
    fine_amount = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(1)], default=5)
    books_allowed = models.PositiveIntegerField(default=3)
    timestamp = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    # user = models.ForeignKey(User, related_name='settings', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = "settings"
        verbose_name_plural = "Settings"
        verbose_name = "Setting"

    @staticmethod
    def get_renew_days():
        setting = Setting.objects.first()
        return setting.renew_days

    @staticmethod
    def get_fine_amount():
        setting = Setting.objects.first()
        return setting.fine_amount

    @staticmethod
    def get_books_allowed():
        setting = Setting.objects.first()
        return setting.books_allowed
