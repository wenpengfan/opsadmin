# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-12-24 05:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20190628_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='dbscript',
            name='env',
            field=models.CharField(choices=[('\u9884\u53d1\u5e03', 'Pre'), ('\u751f\u4ea7', 'Pro')], default='Pro', max_length=10, verbose_name='\u73af\u5883'),
        ),
    ]