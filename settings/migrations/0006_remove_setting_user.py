# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-25 07:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0005_setting_books_allowed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='setting',
            name='user',
        ),
    ]
