from users.models import User
from django.db import models
from model_utils import Choices

from LibraryManagementSystem.validatiors import phone_no_validation

# Create your models here.
from settings.models import CourseBatch

STATUS = Choices(
    'Active',
    'Passed',
    'Droped',
)


def get_document_filename(instance, filename):
    return "student/%s/%s" % (
        instance.course_batch,
        instance.roll_no + '.' + filename.split('.')[-1]
    )


class Student(models.Model):
    name = models.CharField(max_length=32)
    roll_no = models.CharField(max_length=32)
    dob = models.DateField()
    phone_no = models.CharField(max_length=15, validators=[phone_no_validation])
    address = models.CharField(max_length=128)
    user = models.ForeignKey(User, related_name="students", on_delete=models.DO_NOTHING)
    course_batch = models.ForeignKey(CourseBatch, related_name='students', on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=12, choices=STATUS, default='Active')
    photo = models.ImageField(upload_to=get_document_filename, default=None, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'students'
        verbose_name_plural = 'Students'
        verbose_name = "Student"
        ordering = ['-roll_no']

    def save(self, *args, **kwargs):
        self.roll_no = self.course_batch.course.code + "-" + self.course_batch.batch.code + "-" + str(
            self.course_batch.students.count() + 1)
        user = User(email=self.roll_no + '@student.com', username=self.roll_no, password='student123', is_active=True)
        user.save()
        self.user = user
        super().save(*args, **kwargs)
