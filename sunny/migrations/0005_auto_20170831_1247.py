# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-31 09:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sunny', '0004_auto_20170830_1222'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='student',
            new_name='students',
        ),
    ]