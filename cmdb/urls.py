#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from cmdb import asset ,idc


urlpatterns = [
    url(r'^asset/$', asset.asset_list, name='asset_list'),
    url(r'^assetdetail/(?P<asset_id>[a-z\d]+)/$', asset.asset_detail, name='asset_detail'),
    url(r'^idc/$', idc.idc, name='idc'),
    url(r'^idcadd/$', idc.idc_add, name='idc_add'),
    url(r'^idcdel/$', idc.idc_del, name='idc_del'),
    url(r'^idcedit/(?P<idc_id>\d+)/$', idc.idc_edit, name='idc_edit'),
    url(r'^idclist/(?P<idc_id>\d+)/$', idc.idc_list, name='idc_list'),

]
