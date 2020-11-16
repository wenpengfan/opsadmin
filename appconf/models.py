#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from accounts.models import UserInfo


class AppOwner(models.Model):
    name = models.CharField(u"负责人姓名", max_length=50, null=False, blank=False)
    phone = models.CharField(u"负责人手机", max_length=50, unique=True, null=False, blank=False)
    qq = models.CharField(u"负责人QQ", max_length=100, null=True, blank=True)
    dingding  = models.CharField(u"负责人钉钉", max_length=100, null=True, blank=True)
    email = models.CharField(u"负责人邮箱", max_length=100, null=True, blank=True)
    username = models.ForeignKey(UserInfo, verbose_name="账号", on_delete=models.SET_NULL, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(u"产品线名称", max_length=50, unique=True, null=False, blank=False)
    codename = models.CharField(u"产品线代号", max_length=50, null=True, blank=False)
    owner = models.ForeignKey(
        AppOwner, verbose_name=u"产品线负责人",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='owner'
    )
    qa = models.ForeignKey(
        AppOwner, verbose_name=u"测试负责人",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='qa'
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Database(models.Model):
    name = models.CharField(u"数据库名称", max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(u"数据库描述", max_length=255, null=True, blank=True)
    product = models.ForeignKey(
            Product,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name=u"所属产品线"
    )
    ops = models.ForeignKey(
        AppOwner, verbose_name=u"运维负责人",
        null=True, blank=True,
        on_delete=models.SET_NULL
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Project(models.Model):
    LANGUAGE_TYPES = (
        ("Java", "Java"),
        ("Scala", "Scala"),
        ("PHP", "PHP"),
        ("Python", "Python"),
        ("Javascript", "Javascript"),
        ("C/C++", "C/C++"),
        ("Go", "Go"),
        ("Objective-C", "Objective-C"),
        ("Other", "Other"),
    )

    APP_TYPE = (
        ("定时", "定时"),
        ("常驻", "常驻"),
        ("客户端", "客户端"),
    )

    APP_ARCH = (
        ("Spring Boot 1.x", "Spring Boot 1.x"),
        ("Spring Boot 2.x", "Spring Boot 2.x"),
        ("Spark", "Spark"),
        ("Spark Steaming", "Spark Steaming"),
        ("Laravel", "Laravel"),
        ("Yii 2.x", "Yii 2.x"),
        ("WordPress", "WordPress"),
        ("Vue.js", "Vue.js"),
        ("Scrapy", "Scrapy"),
        ("Go-Kit", "Go-Kit"),
        ("Kratos", "Kratos"),
        ("Other", "Other"),
    )

    HA_TYPE = (
        ("程序原生支持高可用", "程序原生支持高可用"),
        ("无需高可用", "无需高可用"),
        ("需要额外配置高可用", "需要额外配置高可用"),
    )

    CHOISES = (
        ("是", "是"),
        ("否", "否"),
    )

    name = models.CharField(u"应用名称", max_length=50, unique=True, null=False, blank=False)
    description = models.CharField(u"应用描述", max_length=255, null=True, blank=True)
    current_ver = models.CharField(u"当前版本", default="0.0.0", max_length=255, null=False, blank=True)
    language_type = models.CharField(u"语言类型", choices=LANGUAGE_TYPES, max_length=30, null=True, blank=False)
    app_type = models.CharField(u"程序类型", choices=APP_TYPE, max_length=30, null=True, blank=False)
    app_arch = models.CharField(u"程序框架", choices=APP_ARCH, max_length=30, null=True, blank=True)
    code_address = models.CharField(u"代码库地址", max_length=255, null=True, blank=False)
    start_cmd = models.CharField(u"启动命令", max_length=255, null=True, blank=True)
    stop_cmd = models.CharField(u"停止命令", max_length=255, null=True, blank=True)
    config_detail = models.TextField(u"配置文件说明", max_length=5000, null=True, blank=True)
    docker_expose = models.TextField(u"Docker容器说明", max_length=5000, null=True, blank=True)
    app_monitor = models.CharField(u"需要的业务监控项", max_length=255, null=True, blank=True)
    need_ha = models.CharField(u"高可用说明", choices=HA_TYPE, default="无需高可用", max_length=30, null=False, blank=False)
    need_dn = models.CharField(u"需要新增域名", max_length=255, null=True, blank=True)
    need_location = models.CharField(u"需要新增二级目录", max_length=255, null=True, blank=True)
    uri_mapping_from = models.CharField(u"URI映射来源", max_length=255, null=True, blank=True)
    uri_mapping_to = models.CharField(u"URI映射目标", max_length=255, null=True, blank=True)
    need_wan = models.CharField(u"是否需要访问外网", choices=CHOISES, default="否", max_length=2, null=False, blank=False)
    requester = models.CharField(u"调用方", max_length=255, null=True, blank=True)
    rely_on = models.TextField(u"应用依赖的其他需求", max_length=255, null=True, blank=True)
    product = models.ForeignKey(
            Product,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            verbose_name=u"所属产品线"
    )
    dev = models.ForeignKey(
            AppOwner,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='dev',
            verbose_name=u"开发负责人"
    )
    ops = models.ForeignKey(
            AppOwner,
            null=True,
            blank=True,
            on_delete=models.SET_NULL,
            related_name='ops',
            verbose_name=u"运维负责人"
    )
    is_offline = models.BooleanField(u"是否下架", default=False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
