# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-20 11:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['name'], 'verbose_name': 'Course', 'verbose_name_plural': 'Course'},
        ),
    ]
