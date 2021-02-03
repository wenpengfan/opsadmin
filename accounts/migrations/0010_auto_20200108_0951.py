# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-01-08 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200108_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='delegatelist',
            name='delegate_from_id',
            field=models.IntegerField(null=True, verbose_name='\u59d4\u6d3e\u4ebaID'),
        ),
        migrations.AddField(
            model_name='delegatelist',
            name='delegate_to_id',
            field=models.IntegerField(null=True, verbose_name='\u63a5\u53d7\u59d4\u6d3e\u4ebaID'),
        ),
        migrations.AlterField(
            model_name='delegatelist',
            name='delegate_from',
            field=models.IntegerField(null=True, verbose_name='\u59d4\u6d3e\u4eba'),
        ),
        migrations.AlterField(
            model_name='delegatelist',
            name='delegate_to',
            field=models.IntegerField(null=True, verbose_name='\u63a5\u53d7\u59d4\u6d3e'),
        ),
    ]
