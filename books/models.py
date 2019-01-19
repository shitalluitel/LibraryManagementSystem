from django.db import models
from model_utils import Choices

# Create your models here.
BOOK_STATUS = Choices('available', 'pending', 'booked')


class Book(models.Model):
    name = models.CharField(max_length=64)
    author = models.TextField(max_length=256)
    edition = models.CharField(max_length=64)
    publisher = models.TextField(max_length=512)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        db_table = "books"
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['name']

    def __str__(self):
        return self.name


class BookUnit(models.Model):
    book = models.ForeignKey(Book, related_name="book_units", on_delete=models.CASCADE)
    acc = models.CharField(max_length=4)
    status = models.CharField(max_length=64)

    class Meta:
        db_table = "book_units"
        verbose_name = "Book Unit"
        verbose_name_plural = "Book Units"
        ordering = ['acc']

    def __str__(self):
        return "Book: {}, Acc: {}".format(self.book, self.acc)
