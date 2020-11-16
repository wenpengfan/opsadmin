# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-05-29 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0011_apply_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply',
            name='report_address',
            field=models.CharField(max_length=255, null=True, verbose_name='\u6d4b\u8bd5\u62a5\u544a\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='apply',
            name='description',
            field=models.CharField(blank=True, max_length=5000, null=True, verbose_name='\u9700\u6c42\u63cf\u8ff0'),
        ),
    ]