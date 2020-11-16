#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *
from .models import Database, Product, Project, AppOwner


class AppOwnerForm(forms.ModelForm):

    class Meta:
        model = AppOwner
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'phone': TextInput(attrs={'class': 'form-control','style': 'width:450px'}),
            'qq': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'dingding': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'email': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'username': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'codename': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'owner': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'qa': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class DatabaseForm(forms.ModelForm):

    class Meta:
        model = Database 
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'description': Textarea(attrs={'class': 'form-control','style': 'width:450px; height:100px'}),
            'product': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'ops': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ("id", "current_ver", "is_offline",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
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
            'product': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'dev': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'ops': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class ProjectMiniForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ("name",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:250px;'}),
        }
