# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-27 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_auto_20190326_0822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='type',
            field=models.CharField(choices=[('Notice', 'Notice'), ('Result', 'Result'), ('Syllabus', 'Syllabus')], max_length=16),
        ),
    ]
