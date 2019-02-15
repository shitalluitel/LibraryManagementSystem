import json

from django.db import models


class CourseQuerySet(models.QuerySet):
    def serialize(self):
        list_values = list(self.values('name', 'code', 'id'))
        return json.dumps(list_values)


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)


class Course(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=10, unique=True)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = CourseManager()

    class Meta:
        db_table = "courses"
        ordering = ['name']
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        # app_label = 'courses'

    def __str__(self):
        return self.name

    def serialize(self):
        data = {
            "name": self.name,
            "code": self.code,
            "id": self.id
        }
        data = json.dumps(data)
        return data
