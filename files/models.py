import os

from django.db import models

# Create your models here.
from django.dispatch import receiver
from model_utils import Choices

from LibraryManagementSystem.settings import MEDIA_ROOT

TYPE = Choices(
    ('', 'Select Type'),
    ('Result', 'Result'),
    ('Syllabus', 'Syllabus')
)


def get_document_filename(instance, filename):
    return "%s/%s" % (instance.type, filename)


class File(models.Model):
    document = models.FileField(upload_to=get_document_filename)

    title = models.TextField(max_length=512)
    type = models.CharField(max_length=16, choices=TYPE)

    is_deleted = models.BooleanField(default=False)

    timestamp = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.document.name

    class Meta:
        db_table = "files"
        verbose_name = "File"
        verbose_name_plural = "Files"
        permissions = (
            ('view_file', 'Can view file'),
        )


@receiver(models.signals.post_delete, sender=File)
def auto_delete_folder_on_delete(sender, instance, **kwargs):
    """
    Deletes document from documentsystem
    when corresponding `Mediadocument` object is deleted.
    """
    # if instance.document:
    #     if os.path.isfile(instance.document.path):
    #         os.remove(instance.document.path)
    for root, dirs, files in os.walk(MEDIA_ROOT):
        for d in dirs:
            dir = os.path.join(root, d)
            # check if dir is empty
            if not os.listdir(dir):
                os.rmdir(dir)


@receiver(models.signals.pre_delete, sender=File)
def auto_pre_delete_document_on_delete(sender, instance, **kwargs):
    """
    Deletes document from documentsystem
    when corresponding `Mediadocument` object is deleted.
    """
    if instance.document:
        if os.path.isfile(instance.document.path):
            os.remove(instance.document.path)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_document_on_change(sender, instance, **kwargs):
    """
    Deletes old document from documentsystem
    when corresponding `Mediadocument` object is updated
    with new document.
    """
    if not instance.pk:
        return False

    try:
        old_document = File.objects.get(pk=instance.pk).document
    except File.DoesNotExist:
        return False

    new_document = instance.document
    if not old_document == new_document:
        if os.path.isfile(old_document.path):
            os.remove(old_document.path)
