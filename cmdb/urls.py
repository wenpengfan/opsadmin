#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from cmdb import idc


urlpatterns = [
    url(r'^idc/$', idc.idc, name='idc'),
    url(r'^idcadd/$', idc.idc_add, name='idc_add'),
    url(r'^idcdel/$', idc.idc_del, name='idc_del'),
    url(r'^idcedit/(?P<idc_id>\d+)/$', idc.idc_edit, name='idc_edit'),
    url(r'^idclist/(?P<idc_id>\d+)/$', idc.idc_list, name='idc_list'),

]
