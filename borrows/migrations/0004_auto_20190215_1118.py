# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-15 11:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('borrows', '0003_auto_20190215_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='issued_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='return_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='borrows', to=settings.AUTH_USER_MODEL),
        ),
    ]
