import json

from django.db import models
from model_utils import Choices

# Create your models here.
BOOK_STATUS = Choices('available', 'pending', 'booked')


class BookQuerySet(models.QuerySet):
    def serialize(self):
        list_values = list(self.values('name', 'edition', 'author', 'publisher', 'id'))
        return json.dumps(list_values)


class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)


class Book(models.Model):
    name = models.CharField(max_length=64)
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

    def __str__(self):
        return self.name

    def serialize(self):
        data = {
            'name': self.name,
            'edition': self.edition,
            'author': self.author,
            'publisher': self.publisher,
            'id': self.id,
        }
        data = json.dumps(data)
        return data


class BookUnit(models.Model):
    book = models.ForeignKey(Book, related_name="book_units", on_delete=models.DO_NOTHING)
    acc = models.CharField(max_length=4)
    status = models.CharField(max_length=64, choices=BOOK_STATUS, default=BOOK_STATUS.available)

    is_deleted = models.BooleanField(default=False)
    remarks = models.TimeField(max_length=128, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = "book_units"
        verbose_name = "Book Unit"
        verbose_name_plural = "Book Units"
        ordering = ['acc']

    def __str__(self):
        return "Book: {}, Acc: {}".format(self.book, self.acc)

    def is_available(self):
        return self.status == BOOK_STATUS.available

    def is_pending(self):
        return self.status == BOOK_STATUS.pending

    def is_booked(self):
        return self.status == BOOK_STATUS.booked
