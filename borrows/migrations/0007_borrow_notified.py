# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-24 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrows', '0006_remove_borrow_fine'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='notified',
            field=models.BooleanField(default=False),
        ),
    ]