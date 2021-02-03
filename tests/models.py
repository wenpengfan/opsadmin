#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from appconf.models import Product, Project

# Create your models here.
class Environment(models.Model):
    project = models.ForeignKey(
            Project,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name=u"应用名称"
    )
    is_enable = models.BooleanField(verbose_name=u"是否同步", default=True)
    test_ver = models.CharField(verbose_name=u"测试版本", default="0.0.0", max_length=255, null=False, blank=True)
    pre_ver = models.CharField(verbose_name=u"预发布版本", default="0.0.0", max_length=255, null=False, blank=True)
    test_pid = models.IntegerField(verbose_name=u"TestAnsible项目号", default=0, null=True, blank=True)
    test_tid = models.IntegerField(verbose_name=u"TestAnsible模板号", default=0, null=True, blank=True)
    pre_pid = models.IntegerField(verbose_name=u"PreAnsible项目号", default=0, null=True, blank=True)
    pre_tid = models.IntegerField(verbose_name=u"PreAnsible模板号", default=0, null=True, blank=True)
    app_type = models.IntegerField(verbose_name=u"应用类型，0：docker，1：other", default=0, null=False, blank=True)
    task_id = models.IntegerField(verbose_name=u"Ansible任务号", default=0, null=True, blank=True)
    task_status = models.IntegerField(verbose_name=u"任务执行状态，0：提交，1：执行中，2：成功，3：失败", null=True, blank=False)
    endtime = models.DateTimeField(verbose_name=u"任务结束时间", null=True, blank=False)

    def __unicode__(self):
        return self.project

    class Meta:
        ordering = ['project']


class Versync(models.Model):
    product = models.ForeignKey(
            Product,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name=u"产品线名称"
    )
    submittime = models.DateTimeField(verbose_name=u"任务提交时间", null=True, blank=False)
    starttime = models.DateTimeField(verbose_name=u"任务开始时间", null=True, blank=False)
    endtime = models.DateTimeField(verbose_name=u"任务结束时间", null=True, blank=False)
    progress = models.IntegerField(verbose_name=u"任务进度", default=0, null=True, blank=False)
    sync_status = models.IntegerField(verbose_name=u"任务执行状态，0：提交，1：执行中，2：同步Nginx，3：成功，4：失败", null=True, blank=False)

    def __unicode__(self):
        return self.product

    class Meta:
        ordering = ['-id']


class VersyncDetail(models.Model):
    versync = models.ForeignKey(
            Versync,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name=u"同步任务号"
    )
    project = models.ForeignKey(
            Project,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name=u"应用名称"
    )
    starttime = models.DateTimeField(verbose_name=u"任务开始时间", null=True, blank=False)
    endtime = models.DateTimeField(verbose_name=u"任务结束时间", null=True, blank=False)
    task_status = models.IntegerField(verbose_name=u"任务执行状态，0：提交，1：执行中，2：成功，3：失败", null=True, blank=False)
    task_id = models.IntegerField(verbose_name=u"Ansible任务号", default=0, null=True, blank=True)
    sync_version = models.CharField(verbose_name=u"同步版本", default="0.0.0", max_length=255, null=False, blank=True)

    def __unicode__(self):
        return self.versync

    class Meta:
        ordering = ['-id']


class Apply(models.Model):
    product = models.ForeignKey(
            Product,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name=u"产品线名称"
    )
    description = models.CharField(max_length=5000, verbose_name=u"需求描述", null=True, blank=False)
    createtime = models.DateTimeField(verbose_name=u"需求创建时间", auto_now_add=True)
    finishtime = models.DateTimeField(verbose_name=u"测试完成时间", null=True, blank=False)
    updatetime = models.DateTimeField(verbose_name=u"更新时间", auto_now=True)
    order_user = models.CharField(max_length=255, verbose_name=u"提交用户", null=True, blank=True)
    status = models.BooleanField(verbose_name=u"需求状态", default=False)
    report_address = models.CharField(u"测试报告地址", max_length=255, null=True, blank=False)
    report_file = models.CharField(u"测试报告文件", max_length=255, null=True, blank=False)
    feedback = models.IntegerField(verbose_name=u"测试反馈，0：未反馈，1：同意上线，2：拒绝上线", default=0, null=True, blank=False)

    def __unicode__(self):
        return self.product

    class Meta:
        ordering = ['-id']
