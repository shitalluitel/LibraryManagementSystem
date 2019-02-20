# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-10 17:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batch',
            options={'ordering': ['name'], 'permissions': (('add_group', 'Can add group'), ('change_group', 'Can change group'), ('delete_group', 'Can delete group'), ('view_group', 'Can view group'), ('view_batch', 'Can view batch')), 'verbose_name': 'Batch', 'verbose_name_plural': 'Batches'},
        ),
    ]