#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from tests import apply, versync, environment


urlpatterns = [
    url(r'^apply/$', apply.apply_list, name='apply_list'),
    url(r'^applyadd/$', apply.apply_add, name='apply_add'),
    url(r'^applydel/$', apply.apply_del, name='apply_del'),
    url(r'^applyedit/$', apply.apply_edit, name='apply_edit'),
    url(r'^applyfinish/$', apply.apply_finish, name='apply_finish'),
    url(r'^applydetail/(?P<apply_id>\d+)/$', apply.apply_detail, name='apply_detail'),
    url(r'^applyagree/$', apply.apply_agree, name='apply_agree'),
    url(r'^applyreject/$', apply.apply_reject, name='apply_reject'),
    url(r'^versync/$', versync.versync_list, name='versync_list'),
    url(r'^versyncdel/$', versync.versync_del, name='versync_del'),
    url(r'^versyncsubmit/$', versync.version_sync, name='version_sync'),
    url(r'^versyncprogress/$', versync.sync_progress, name='versync_progress'),
    url(r'^environment/$', environment.env_prepare, name='env_prepare'),
    url(r'^envprojsync/$', environment.project_sync, name='env_project_sync'),
    url(r'^envedit/$', environment.env_edit, name='env_edit'),
    url(r'^envsave/$', environment.env_save, name='env_save'),
    url(r'^envdisable/$', environment.env_disable, name='env_disable'),
    url(r'^envenable/$', environment.env_enable, name='env_enable'),
    url(r'^envtasklog/$', environment.env_task_log, name='env_task_log'),
    url(r'^envtaskstatus/$', environment.env_task_status, name='env_task_status'),
]
