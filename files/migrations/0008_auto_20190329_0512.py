# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-29 05:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_auto_20190328_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='type',
            field=models.CharField(choices=[('', 'Select Type'), ('Result', 'Result'), ('Syllabus', 'Syllabus')], max_length=16),
        ),
    ]
