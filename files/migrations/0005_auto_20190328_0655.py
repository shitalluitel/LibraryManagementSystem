# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-28 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_file_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='type',
            field=models.CharField(choices=[('Select Type', ''), ('Notice', 'Notice'), ('Result', 'Resut'), ('Syllabus', 'Syllabus')], max_length=16),
        ),
    ]