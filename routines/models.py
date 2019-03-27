from django.db import models

# Create your models here.
from model_utils import Choices

from settings.models import Course, Batch

DAYS = Choices('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
SEMS = Choices('1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th')


class Routine(models.Model):
    day = models.CharField(max_length=16, choices=DAYS)
    time_from = models.CharField(max_length=16)
    time_to = models.CharField(max_length=16)
    teacher = models.CharField(max_length=64)
    subject = models.CharField(max_length=64)
    course = models.ForeignKey(Course, related_name='routines')
    batches = models.ForeignKey(Batch, related_name='routines')
    semester = models.CharField(max_length=8, choices=SEMS)

    is_deleted = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return "Course: {}, Batch: {}, Semester: {}".format(self.course.name, self.batches.name, self.semester)
