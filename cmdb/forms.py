# -*- coding:utf-8 -*-

from django import forms
from django.forms.widgets import *

from .models import Idc


class IdcForm(forms.ModelForm):

    # def clean(self):
    #     cleaned_data = super(IdcForm, self).clean()
    #     value = cleaned_data.get('ids')
    #     try:
    #         Idc.objects.get(name=value)
    #         self._errors['ids'] = self.error_class(["%s的信息已经存在" % value])
    #     except Idc.DoesNotExist:
    #         pass
    #     return cleaned_data

    class Meta:
        model = Idc
        exclude = ("id",)

        widgets = {
            'ids': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'address': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'tel': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'contact': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'contact_phone': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'ip_range': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'jigui': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'bandwidth': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
        }
