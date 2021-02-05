#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from orders import deploy, dbscript, require


urlpatterns = [
    url(r'^deploy/$', deploy.deploy_list, name='deploy_list'),
    url(r'^deployadd/$', deploy.deploy_add, name='deploy_add'),
    url(r'^deploydel/$', deploy.deploy_del, name='deploy_del'),
    url(r'^deployedit/(?P<deploy_id>\d+)/$', deploy.deploy_edit, name='deploy_edit'),
    url(r'^deployfinish/(?P<deploy_id>\d+)/$', deploy.deploy_finish, name='deploy_finish'),
    url(r'^deploydetail/(?P<deploy_id>\d+)/$', deploy.deploy_detail, name='deploy_detail'),
    url(r'^deploydoc/$', deploy.deploy_doc, name='deploy_doc'),
    url(r'^dbscript/$', dbscript.dbscript_list, name='dbscript_list'),
    url(r'^dbscriptadd/$', dbscript.dbscript_add, name='dbscript_add'),
    url(r'^dbscriptaddmini/$', dbscript.dbscript_add_mini, name='dbscript_add_mini'),
    url(r'^dbscriptdel/$', dbscript.dbscript_del, name='dbscript_del'),
    url(r'^dbscriptedit/(?P<dbscript_id>\d+)/$', dbscript.dbscript_edit, name='dbscript_edit'),
    url(r'^dbscriptfinish/(?P<dbscript_id>\d+)/$', dbscript.dbscript_finish, name='dbscript_finish'),
    url(r'^dbscriptdetail/(?P<dbscript_id>\d+)/$', dbscript.dbscript_detail, name='dbscript_detail'),
    url(r'^dbscriptdownload/(?P<dbscript_id>\d+)/$', dbscript.dbscript_download, name='dbscript_download'),
    url(r'^require/$', require.require_list, name='require_list'),
    url(r'^requireadd/$', require.require_add, name='require_add'),
    url(r'^requiredel/$', require.require_del, name='require_del'),
    url(r'^requireedit/(?P<require_id>\d+)/$', require.require_edit, name='require_edit'),
    url(r'^requirefinish/(?P<require_id>\d+)/$', require.require_finish, name='require_finish'),
    url(r'^requiredetail/(?P<require_id>\d+)/$', require.require_detail, name='require_detail'),
]
