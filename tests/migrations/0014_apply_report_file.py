# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-06-01 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0013_apply_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply',
            name='report_file',
            field=models.CharField(max_length=255, null=True, verbose_name='\u6d4b\u8bd5\u62a5\u544a\u6587\u4ef6'),
        ),
    ]
