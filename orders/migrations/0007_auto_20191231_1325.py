# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-12-31 05:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20191225_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deploy',
            name='description',
            field=models.CharField(max_length=5000, null=True, verbose_name='\u66f4\u65b0\u63cf\u8ff0'),
        ),
    ]
