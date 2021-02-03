# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Idc(models.Model):
    name = models.CharField(u"服务器名称", max_length=255, unique=True)
    network = models.CharField(u"服务器外网IP", max_length=100, blank=True)
    intranet = models.CharField(u"服务器内网IP", max_length=100, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'数据中心'
        verbose_name_plural = verbose_name
