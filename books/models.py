import json

from django.db import models
from django.dispatch import receiver
from model_utils import Choices

# Create your models here.
BOOK_STATUS = Choices('available', 'pending', 'booked')


class BookQuerySet(models.QuerySet):
    def serialize(self):
        list_values = list(self.values('name', 'code', 'edition', 'author', 'publisher', 'id'))
        return json.dumps(list_values)


class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)


class Book(models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=16, unique=True)
    author = models.TextField(max_length=256)
    edition = models.CharField(max_length=64)
    publisher = models.TextField(max_length=512)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = BookManager()

    class Meta:
        db_table = "books"
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['name']
        unique_together = ('name', 'code', 'author', 'publisher', 'edition')
        permissions = (
            ('view_books', "Can view books"),
            ('undo_book', "Can undo books"),
            ('view_trash', 'Can view trash list of books')
        )

    def __str__(self):
        return self.name

    def clean(self):
        self.name = self.name.title()
        self.author = self.author.title()
        self.publisher = self.publisher.title()

    def serialize(self):
        data = {
            'name': self.name,
            'code': self.code,
            'edition': self.edition,
            'author': self.author,
            'publisher': self.publisher,
            'id': self.id,
        }
        data = json.dumps(data)
        return data


class BookUnit(models.Model):
    book = models.ForeignKey(Book, related_name="book_units", on_delete=models.DO_NOTHING)
    acc_no = models.CharField(max_length=16)
    book_code = models.CharField(max_length=16)
    status = models.CharField(max_length=64, choices=BOOK_STATUS, default=BOOK_STATUS.available)

    is_deleted = models.BooleanField(default=False)

    remarks = models.TextField(max_length=128, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = "book_units"
        verbose_name = "Book Unit"
        verbose_name_plural = "Book Units"
        ordering = ['acc_no']
        permissions = (
            ('view_bookunit', 'Can view bookunit'),
            ('undo_bookunit', 'Can undo bookunit'),
            ('order_bookunit', 'Can order bookunit'),
            ('assign_bookunit', 'Can assign bookunit'),
        )

    def __str__(self):
        return "Book: {}, Acc: {}".format(self.book, self.acc_no)

    def is_available(self):
        return self.status == BOOK_STATUS.available

    def is_pending(self):
        return self.status == BOOK_STATUS.pending

    def is_booked(self):
        return self.status == BOOK_STATUS.booked


@receiver(models.signals.pre_save, sender=BookUnit)
def auto_add_acc_no(sender, instance, **kwargs):
    """
    Creating acc_no
    """
    if not instance.acc_no:
        instance.acc_no = str(BookUnit.objects.count() + 1)

    if not instance.book_code:
        instance.book_code = instance.book.code + '-' + str(BookUnit.objects.filter(book=instance.book).count() + 1)
