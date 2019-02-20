from django.contrib.auth.decorators import permission_required
from django.db import models
from students.models import Student


# Create your models here.

class Fine(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    student = models.OneToOneField(Student, on_delete=models.DO_NOTHING)
    timestamp = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = 'fines'
        verbose_name_plural = 'Fines'
        verbose_name = 'Fine'

    def __str__(self):
        return str(self.amount)
