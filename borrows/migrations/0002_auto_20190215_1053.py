# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-02-15 10:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_auto_20190207_1114'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('borrows', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='student',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='borrows', to='students.Student'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='borrow',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='borrows', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
