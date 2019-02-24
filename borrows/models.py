from django.db import models
from books.models import BookUnit

from model_utils import Choices

from students.models import Student
from users.models import User

STATUS = Choices('pending', 'approved', 'cancelled', 'returned')


# Create your models here.
class Borrow(models.Model):
    student = models.ForeignKey(Student, related_name='borrows', on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, related_name='borrows', on_delete=models.DO_NOTHING, null=True)
    book_unit = models.ForeignKey(BookUnit, related_name="borrows", on_delete=models.DO_NOTHING)
    issued_date = models.DateField(null=True)
    return_date = models.DateField(null=True)
    # fine = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS, default=STATUS.pending)
    notified = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.book_unit)

    class Meta:
        db_table = "borrows"
        ordering = ['-created_at']
        verbose_name = "Borrow"
        verbose_name_plural = "Borrows"
        app_label = 'borrows'
        permissions = (
            ('view_borrow', 'Can view borrow'),
        )

    def is_pending(self):
        return self.status == STATUS.pending

    def is_approved(self):
        return self.status == STATUS.approved

    def is_cancelled(self):
        return self.status == STATUS.cancelled

    def is_returned(self):
        return self.status == STATUS.returned

    def get_issued_date(self):
        return str(self.issued_date)
