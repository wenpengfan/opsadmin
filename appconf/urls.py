#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from appconf import database, product, project, appowner, api


urlpatterns = [
    url(r'^appowneradd/$', appowner.appowner_add, name='appowner_add'),
    url(r'^appowneraddmini/$', appowner.appowner_add_mini, name='appowner_add_mini'),
    url(r'^appowner/$', appowner.appowner_list, name='appowner_list'),
    url(r'^appowneredit/(?P<appowner_id>\d+)/$', appowner.appowner_edit, name='appowner_edit'),
    url(r'^appownerdel/$', appowner.appowner_del, name='appowner_del'),
    url(r'^productadd/$', product.product_add, name='product_add'),
    url(r'^product/$', product.product_list, name='product_list'),
    url(r'^productplist/(?P<product_id>\d+)/$', product.project_list, name='product_project_list'),
    url(r'^productedit/(?P<product_id>\d+)/$', product.product_edit, name='product_edit'),
    url(r'^productdel/$', product.product_del, name='product_del'),
    url(r'^projectadd/$', project.project_add, name='project_add'),
    url(r'^projectaddmini/$', project.project_add_mini, name='project_add_mini'),
    url(r'^project/$', project.project_list, name='project_list'),
    url(r'^projectedit/(?P<project_id>\d+)/$', project.project_edit, name='project_edit'),
    url(r'^projectdel/$', project.project_del, name='project_del'),
    url(r'^projectoffline/$', project.project_offline, name='project_offline'),
    url(r'^projectexport/$', project.project_export, name='project_export'),
    url(r'^projectdetail/(?P<project_id>\d+)/$', project.project_detail, name='project_detail'),
    url(r'^databaseadd/$', database.database_add, name='database_add'),
    url(r'^database/$', database.database_list, name='database_list'),
    url(r'^databaseedit/(?P<database_id>\d+)/$', database.database_edit, name='database_edit'),
    url(r'^databasedel/$', database.database_del, name='database_del'),
    url(r'^api/project/$', api.api_project_list.as_view(), name='api_project_list'),
    url(r'^api/projectproduct/$', api.api_project_product.as_view(), name='api_project_product'),
]
