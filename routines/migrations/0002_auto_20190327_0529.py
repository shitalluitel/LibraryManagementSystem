# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-27 05:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='time_from',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='routine',
            name='time_to',
            field=models.CharField(max_length=16),
        ),
    ]
