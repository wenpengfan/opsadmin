#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *
from navi.models import dev, pro, test, category


class dev_form(forms.ModelForm):

    def clean(self):
        cleaned_data = super(dev_form, self).clean()
        value = cleaned_data.get('name')
        try:
            dev.objects.get(name=value)
            self._errors['name']=self.error_class([u"%s的信息已经存在" % value])
        except dev.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = dev 
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'description': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'url': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
        }
        
class test_form(forms.ModelForm):

    def clean(self):
        cleaned_data = super(test_form, self).clean()
        value = cleaned_data.get('name')
        try:
            test.objects.get(name=value)
            self._errors['name']=self.error_class([u"%s的信息已经存在" % value])
        except test.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = test 
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'description': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'url': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
        }

class pro_form(forms.ModelForm):

    def clean(self):
        cleaned_data = super(pro_form, self).clean()
        value = cleaned_data.get('name')
        try:
            pro.objects.get(name=value)
            self._errors['name']=self.error_class([u"%s的信息已经存在" % value])
        except pro.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = pro 
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'description': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'url': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'category': Select(attrs={'class': 'form-control','style': 'width:150px;'}),
        }

class category_form(forms.ModelForm):

    class Meta:
        model = category
        exclude = ("id",)
        widgets = {
            'title': TextInput(attrs={'class': 'form-control','style': 'width:150px;'}),
        }