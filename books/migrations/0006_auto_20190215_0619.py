# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-15 06:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20190215_0612'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['name'], 'permissions': (('view_books', 'Can view books'), ('undo_book', 'Can undo books')), 'verbose_name': 'Book', 'verbose_name_plural': 'Books'},
        ),
    ]
