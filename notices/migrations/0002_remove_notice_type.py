# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-29 05:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='type',
        ),
    ]
