from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from model_utils import Choices

TYPE = Choices(
    ('', 'Select Type'),
    ('Notice', 'Notice'),
    ('Result', 'Result'),
    ('Syllabus', 'Syllabus')
)


# Create your models here.

class Notice(models.Model):
    notice = RichTextUploadingField('text')

    title = models.TextField(max_length=512)
    # type = models.CharField(max_length=16, choices=TYPE)

    is_deleted = models.BooleanField(default=False)

    timestamp = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'notices'
        verbose_name_plural = 'Notices'
        verbose_name = 'Notice'
