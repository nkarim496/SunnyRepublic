# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-19 14:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sunny', '0005_auto_20170831_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sunny.Teacher'),
            preserve_default=False,
        ),
    ]
