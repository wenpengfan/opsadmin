# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-01-01 06:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200101_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delegatelist',
            name='delegate_status',
            field=models.BooleanField(default=False, verbose_name='\u59d4\u6d3e\u72b6\u6001'),
        ),
    ]