#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from django import forms
from django.forms.widgets import Select, TextInput, Textarea, URLInput

from tests.models import Environment, Apply
from appconf.models import Product, Project


class EnvForm(forms.ModelForm):

    class Meta:
        model = Environment
        exclude = ("id", "project", "is_enable", "test_ver",)

        widgets = {
            'pre_pid': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'pre_tid': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'test_pid': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'test_tid': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }


    def __init__(self, *args, **kwargs):
        super(EnvForm, self).__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.filter(is_offline=False)


class ApplyForm(forms.ModelForm):

    class Meta:
        model = Apply
        exclude = ("id", "createtime", "finishtime", "updatetime", "status",
                   "order_user", "report_address", "report_file", "feedback",)

        widgets = {
            'product': Select(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'description': Textarea(attrs={'class': 'form-control', 'style': 'width:450px; height:100px'}),
        }

    def __init__(self, *args, **kwargs):
        super(ApplyForm, self).__init__(*args, **kwargs)
        self.fields["product"].queryset = Product.objects.filter(qa_id__isnull=False)


class ApplyFinishForm(forms.ModelForm):

    class Meta:
        model = Apply
        exclude = ("id", "createtime", "finishtime", "updatetime", "status",
                   "order_user", "product", "description", "report_file", "feedback",)

        widgets = {
            'report_address': URLInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }
