#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from appconf.models import Database, Project, AppOwner

# Create your models here.
class Require(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"标题", null=True, blank=False)
    description = models.CharField(max_length=5000, verbose_name=u"需求描述", null=True, blank=True)
    status = models.BooleanField(verbose_name=u"部署状态", default=False)
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    operating_time = models.DateTimeField(verbose_name=u"预约操作时间", null=True, blank=False)
    update_time = models.DateTimeField(verbose_name=u"更新时间", auto_now=True)
    order_user = models.CharField(max_length=255, verbose_name=u"提交用户", null=True, blank=True)
    owner = models.ForeignKey(AppOwner, verbose_name=u"负责人", on_delete=models.deletion.SET_NULL, null=True, blank=False)
    completion_time = models.DateTimeField(verbose_name=u"完成时间", null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-completion_time','operating_time']

class DBScript(models.Model):
    db_name = models.ForeignKey(Database, verbose_name=u"数据库", on_delete=models.deletion.SET_NULL, null=True, blank=False)
    description = models.CharField(max_length=5000, verbose_name=u"更新描述", null=True, blank=True)
    script_name = models.CharField(max_length=255, verbose_name=u"脚本名称", null=True, blank=False)
    status = models.BooleanField(verbose_name=u"部署状态", default=False)
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    operating_time = models.DateTimeField(verbose_name=u"预约操作时间", null=True, blank=False)
    update_time = models.DateTimeField(verbose_name=u"更新时间", auto_now=True)
    order_user = models.CharField(max_length=255, verbose_name=u"提交用户", null=True, blank=True)
    env = models.CharField(max_length=10, verbose_name=u"环境", null=True, blank=False)
    completion_time = models.DateTimeField(verbose_name=u"完成时间", null=True, blank=True)

    def __unicode__(self):
        return self.script_name

    class Meta:
        ordering = ['-completion_time','operating_time']


class Deploy(models.Model):
    app_name = models.ForeignKey(Project, verbose_name=u"应用名称", on_delete=models.deletion.SET_NULL, null=True, blank=False)
    description = models.CharField(max_length=5000, verbose_name=u"更新描述", null=True, blank=False)
    version = models.CharField(max_length=255, verbose_name=u"程序版本号", blank=False,unique=True)
    status = models.BooleanField(verbose_name=u"部署状态", default=False)
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now_add=True)
    operating_time = models.DateTimeField(verbose_name=u"预约操作时间", null=True, blank=False)
    update_time = models.DateTimeField(verbose_name=u"更新时间", auto_now=True)
    order_user = models.CharField(max_length=255, verbose_name=u"提交用户", null=True, blank=True)
    order_status = models.BooleanField(verbose_name=u"工单状态", default=False)
    dbscript = models.ForeignKey(DBScript, verbose_name=u"数据库工单", on_delete=models.deletion.SET_NULL, null=True, blank=True)
    is_new = models.BooleanField(verbose_name=u"是否新应用", default=False)
    is_tested = models.IntegerField(u"是否测试通过，0：未确定，1：测试通过，2：测试未通过", default=0, null=True, blank=False)
    completion_time = models.DateTimeField(verbose_name=u"完成时间", null=True, blank=True)

    def __unicode__(self):
        return self.version

    class Meta:
        unique_together = ('app_name', 'version',)
        ordering = ['-completion_time','operating_time']


class Document(models.Model):
    doc_id = models.IntegerField(u"文档编号", default=0)
    name = models.CharField(u"应用名称", max_length=50, default=None, null=False, blank=False)
    description = models.CharField(u"应用描述", max_length=5000, null=True, blank=True)
    current_ver = models.CharField(u"当前版本", max_length=255, null=True, blank=True)
    next_ver = models.CharField(u"后续版本", max_length=255, null=True, blank=True)
    language_type = models.CharField(u"语言类型", max_length=30, null=True, blank=False)
    app_type = models.CharField(u"程序类型", max_length=30, null=True, blank=False)
    app_arch = models.CharField(u"程序框架", max_length=30, null=True, blank=True)
    code_address = models.CharField(u"代码库地址", max_length=255, null=True, blank=False)
    start_cmd = models.CharField(u"启动命令", max_length=255, null=True, blank=True)
    stop_cmd = models.CharField(u"停止命令", max_length=255, null=True, blank=True)
    config_detail = models.TextField(u"配置文件说明", max_length=1000, null=True, blank=True)
    docker_expose = models.TextField(u"Docker容器说明", max_length=1000, null=True, blank=True)
    app_monitor = models.CharField(u"需要的业务监控项", max_length=255, null=True, blank=True)
    need_ha = models.CharField(u"高可用说明", default="无需高可用", max_length=30, null=False, blank=False)
    need_dn = models.CharField(u"需要新增域名", max_length=255, null=True, blank=True)
    need_location = models.CharField(u"需要新增二级目录", max_length=255, null=True, blank=True)
    uri_mapping_from = models.CharField(u"URI映射来源", max_length=255, null=True, blank=True)
    uri_mapping_to = models.CharField(u"URI映射目标", max_length=255, null=True, blank=True)
    need_wan = models.CharField(u"是否需要访问外网", default="否", max_length=2, null=False, blank=False)
    requester = models.CharField(u"调用方", max_length=255, null=True, blank=True)
    rely_on = models.TextField(u"应用依赖的其他需求", max_length=255, null=True, blank=True)
    product_id = models.IntegerField(u"所属产品线", default=0, null=True, blank=True)
    dev_id = models.IntegerField(u"开发负责人", default=0, null=True, blank=True)
    ops_id = models.IntegerField(u"运维负责人", default=0, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('doc_id', 'current_ver',)
