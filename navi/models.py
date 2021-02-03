#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models


class category(models.Model):
    title = models.CharField(u"分类", max_length=10)
    
    def __unicode__(self):
        return self.title

class pro(models.Model):
    name = models.CharField(u"名称", max_length=50)
    description = models.CharField(u"描述", max_length=50)
    url = models.URLField(u"URL")
    category = models.ForeignKey(
                category, verbose_name=u"分类",
                on_delete=models.deletion.SET_NULL,
                null=True, blank=False
                )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['url']

class dev(models.Model):
    name = models.CharField(u"名称", max_length=50)
    description = models.CharField(u"描述", max_length=50)
    url = models.URLField(u"URL")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['url']
        
class test(models.Model):
    name = models.CharField(u"名称", max_length=50)
    description = models.CharField(u"描述", max_length=50)
    url = models.URLField(u"URL")

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['url']

class hosts(models.Model):
    ip = models.CharField(u"IP", max_length=50)
    url = models.URLField(u"URL")

    def __unicode__(self):
        return self.ip

    class Meta:
        ordering = ['ip']