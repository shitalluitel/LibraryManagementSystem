from django.db import models
from books.models import BookUnit

from model_utils import Choices

STATUS = Choices('pending', 'approved', 'cancelled')


# Create your models here.
class Borrow(models.Model):
    book_unit = models.ForeignKey(BookUnit, related_name="borrows", on_delete=models.DO_NOTHING)
    issued_date = models.DateField()
    return_date = models.DateField()
    fine = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # user = models.ForeignKey(User, related_name="borrows", on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=32, choices=STATUS, default=STATUS.pending)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.book_unit

    class Meta:
        db_table = "borrows"
        ordering = ['-created_at']
        verbose_name = "Borrow"
        verbose_name_plural = "Borrows"

    def is_pending(self):
        return self.status == STATUS.pending

    def is_approved(self):
        return self.status == STATUS.approved

    def is_cancelled(self):
        return self.status == STATUS.cancelled
