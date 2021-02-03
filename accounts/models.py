#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.


class PermissionList(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.url)


class RoleList(models.Model):
    name = models.CharField(max_length=64)
    permission = models.ManyToManyField(PermissionList, blank=True)

    def __unicode__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email,
            username=username,
            password=password,
        )

        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserInfo(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True, db_index=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    nickname = models.CharField(max_length=64, null=True, blank=True)
    role = models.ForeignKey(RoleList, null=True, blank=True)
    ldap_name = models.CharField(max_length=64, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email
    
    class Meta:
        ordering = ['username']


class DelegateList(models.Model):
    delegate_from = models.IntegerField(u"委派人", null=True, blank=False)
    delegate_from_id = models.IntegerField(u"委派人ID", null=True, blank=False)
    delegate_from_name = models.CharField(u"委派人姓名", max_length=50, null=True, blank=False)
    delegater_dingding  = models.CharField(u"委派人钉钉", max_length=100, null=True, blank=True)
    delegate_to = models.IntegerField(u"接受委派", null=True, blank=False)
    delegate_to_id = models.IntegerField(u"接受委派人ID", null=True, blank=False)
    delegate_to_name = models.CharField(u"接受委派人姓名", max_length=50, null=True, blank=False)
    starttime = models.DateTimeField(verbose_name=u"委派开始时间", null=True, blank=False)
    endtime = models.DateTimeField(verbose_name=u"委派结束时间", null=True, blank=False)
    operator = models.CharField(u"操作人", max_length=255, null=True, blank=True)
    delegate_status = models.BooleanField(verbose_name=u"委派状态", default=False)

    def __unicode__(self):
        return self.delegate_from_name

    class Meta:
        index_together = ('delegate_from_id', 'delegate_to_id',)
        ordering = ['starttime']
