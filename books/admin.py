from django.contrib import admin

# Register your models here.
from .models import BookUnit, Book

admin.site.register(Book)
admin.site.register(BookUnit)