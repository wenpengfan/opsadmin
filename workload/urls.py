#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from workload import summary, delay 


urlpatterns = [
    url(r'^summary/$', summary.summary_list, name='summary_list'),
    url(r'^delay/$', delay.delay_list, name='delay_list'),
]
