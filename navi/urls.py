#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from navi import pronavi, devnavi, testnavi, hosts, category 


urlpatterns = [
    url(r'^devlist/$', devnavi.index, name='dev_index'),
    url(r'^devadd/$', devnavi.add, name='dev_add'),
    url(r'^devmanage/$', devnavi.manage, name='dev_manage'),
    url(r'^devdelete/$', devnavi.delete, name='dev_delete'),
    url(r'^devedit/$', devnavi.edit, name='dev_edit'),
    url(r'^devsave/$', devnavi.save, name='dev_save'),
    url(r'^prolist/$', pronavi.index, name='pro_index'),
    url(r'^proadd/$', pronavi.add, name='pro_add'),
    url(r'^promanage/$', pronavi.manage, name='pro_manage'),
    url(r'^prodelete/$', pronavi.delete, name='pro_delete'),
    url(r'^proedit/$', pronavi.edit, name='pro_edit'),
    url(r'^prosave/$', pronavi.save, name='pro_save'),
    url(r'^testlist/$', testnavi.index, name='test_index'),
    url(r'^testadd/$', testnavi.add, name='test_add'),
    url(r'^testmanage/$', testnavi.manage, name='test_manage'),
    url(r'^testdelete/$', testnavi.delete, name='test_delete'),
    url(r'^testedit/$', testnavi.edit, name='test_edit'),
    url(r'^testsave/$', testnavi.save, name='test_save'),
    url(r'^hosts/$', hosts.index, name='hosts_list'),
    url(r'^site/$', pronavi.manage, name='manage_site'),
    url(r'^categoryadd/$', category.add, name='category_add'),
    url(r'^categorydelete/$', category.delete, name='category_delete'),
]