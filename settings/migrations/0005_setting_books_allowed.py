# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-20 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0004_auto_20190220_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='books_allowed',
            field=models.PositiveIntegerField(default=3),
        ),
    ]