import json

from django.db import models


class BatchQuerySet(models.QuerySet):
    def serialize(self):
        list_values = list(self.values('name', 'code', 'id'))
        return json.dumps(list_values)


class BatchManager(models.Manager):
    def get_queryset(self):
        return BatchQuerySet(self.model, using=self._db)


class Batch(models.Model):
    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=10, unique=True)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = BatchManager()

    class Meta:
        db_table = "batches"
        ordering = ['name']
        verbose_name = "Batch"
        verbose_name_plural = "Batches"

    def __str__(self):
        return self.name

    def serialize(self):
        data = {
            "name": self.name,
            "code": self.code,
            "id": self.id,
        }
        data = json.dumps(data)
        return data
