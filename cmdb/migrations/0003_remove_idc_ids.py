# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2021-02-03 15:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0002_auto_20210203_1534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idc',
            name='ids',
        ),
    ]