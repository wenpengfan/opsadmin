# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-01-08 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200101_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='delegatelist',
            name='delegate_from_name',
            field=models.CharField(max_length=50, null=True, verbose_name='\u59d4\u6d3e\u4eba\u59d3\u540d'),
        ),
        migrations.AddField(
            model_name='delegatelist',
            name='delegate_to_name',
            field=models.CharField(max_length=50, null=True, verbose_name='\u63a5\u53d7\u59d4\u6d3e\u4eba\u59d3\u540d'),
        ),
    ]
