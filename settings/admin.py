from django.contrib import admin

# Register your models here.
from .models import Course, Batch, CourseBatch

admin.site.register(Course)
admin.site.register(Batch)
admin.site.register(CourseBatch)