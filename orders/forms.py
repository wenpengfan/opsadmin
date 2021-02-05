#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from django import forms
from django.forms.widgets import * 
from orders.models import Deploy, DBScript, Require
from appconf.models import Project

class DeployForm(forms.ModelForm):

    class Meta:
        model = Deploy
        exclude = ("id", "status", "create_time", "update_time",
                   "order_user", "order_status", "is_new", "completion_time")

        widgets = {
            'app_name': Select(attrs={'class': 'selectpicker', 'data-live-search': 'true', 'data-width': '250px'}),
            'description': Textarea(attrs={'class': 'form-control', 'style': 'width:450px; height:100px'}),
            'version': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'operating_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:450px;',
                                                  'placeholder': u'2020-01-01 12:00:00', 'autocomplete': 'off'}),
            'dbscript': TextInput(attrs={'hidden': 'hidden'}),
        }

    def __init__(self, *args, **kwargs):
        super(DeployForm, self).__init__(*args, **kwargs)
        self.fields["app_name"].queryset= Project.objects.filter(is_offline=False)


class DeployEditForm(forms.ModelForm):

    class Meta:
        model = Deploy 
        exclude = ("id", "app_name", "version", "status", "create_time",
                   "update_time", "order_user", "order_status", "is_new")

        widgets = {
            'description': Textarea(attrs={'class': 'form-control', 'style': 'width:450px; height:100px'}),
            'operating_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:450px;',
                                                  'placeholder': u'2020-01-01 12:00:00', 'autocomplete': 'off'}),
            'dbscript': TextInput(attrs={'hidden': 'hidden'}),
        }


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Project 
        exclude = ("id", "name", "current_ver", "product", "dev", "ops", "is_offline",)

        widgets = {
            'description': Textarea(attrs={'class': 'form-control','style': 'width:450px; height:100px'}),
            'language_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_arch': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'code_address': URLInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'start_cmd': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'stop_cmd': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'config_detail': Textarea(attrs={'class': 'form-control','style': 'width:450px; height:100px'}),
            'docker_expose': Textarea(attrs={'class': 'form-control','style': 'width:450px; height:100px', 
                                             'placeholder': u'示例：\n'+
                                                            u'(1)应用端口：容器内端口为8080\n'+
                                                            u'(2)应用日志：容器内日志路径为/opt/logs\n'+
                                                            u'(3)数据文件：容器内数据文件路径/opt/data\n'+
                                                            u'(4)环境变量：KAFKA_SERVERS=10.20.2.12:9092 #kafka broker地址'}),
            'app_monitor': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'need_ha': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'need_dn': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'need_location': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'uri_mapping_from': TextInput(attrs={'class': 'form-control','style': 'width:250px;'}),
            'uri_mapping_to': TextInput(attrs={'class': 'form-control','style': 'width:250px;'}),
            'need_wan': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'requester': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'rely_on': Textarea(attrs={'class': 'form-control','style': 'width:450px; height:100px'}),
        }


class DBScriptForm(forms.ModelForm):

    class Meta:
        model = DBScript 
        exclude = ("id", "script_name", "env", "create_time", "update_time", "status", "order_user", "completion_time")

        widgets = {
            'db_name': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'description': Textarea(attrs={'class': 'form-control', 'style': 'width:450px; height:100px'}),
            'operating_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:450px;',
                                                  'placeholder': u'2020-01-01 12:00:00', 'autocomplete': 'off'}),
        }


class DBScriptEditForm(forms.ModelForm):

    class Meta:
        model = DBScript 
        exclude = ("id", "db_name", "env", "script_name", "create_time", "update_time", "status", "order_user", "completion_time")

        widgets = {
            'description': Textarea(attrs={'class': 'form-control', 'style': 'width:450px; height:100px'}),
            'operating_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:450px;',
                                                  'placeholder': u'2020-01-01 12:00:00', 'autocomplete': 'off'}),
        }


class RequireForm(forms.ModelForm):

    class Meta:
        model = Require 
        exclude = ("id", "create_time", "update_time", "status", "order_user", "completion_time")

        widgets = {
            'title': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'description': Textarea(attrs={'class': 'form-control', 'style': 'width:450px; height:100px'}),
            'operating_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:450px;',
                                                  'placeholder': u'2020-01-01 12:00:00', 'autocomplete': 'off'}),
            'owner': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
        }
