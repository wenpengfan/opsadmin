#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db import connection
from accounts.permission import permission_verify, permission_deny
import datetime


@login_required
@permission_verify()
def summary_list(request):
    names = []
    deploy_data = []
    dbscript_data = []
    require_data = []

    today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    yesterday = today - delta 
    start_date = request.GET.get('start_date', yesterday.strftime('%Y-%m-%d'))
    end_date = request.GET.get('end_date', today.strftime('%Y-%m-%d'))

    deploys = _summary_deploy(start_date, end_date)
    dbscripts = _summary_dbscript(start_date, end_date)
    requires = _summary_require(start_date, end_date)

    names = list(set(deploys.keys()+dbscripts.keys()+requires.keys()))
    for name in names:
        if deploys.has_key(name):
            deploy_data.append(deploys[name])
        else:
            deploy_data.append(0)
        if dbscripts.has_key(name):
            dbscript_data.append(dbscripts[name])
        else:
            dbscript_data.append(0)
        if requires.has_key(name):
            require_data.append(requires[name])
        else:
            require_data.append(0)

    results = {
        'start_date': start_date,
        'end_date': end_date,
        'labels': ",".join(names), 
        'deploy_data': deploy_data,
        'dbscript_data': dbscript_data,
        'require_data': require_data,
    }
    return render(request, 'workload/summary_list.html', results)


def _summary_deploy(sdate, edate):
    cursor = connection.cursor()
    deploy_sql = '''SELECT name, count(id) AS deploy_cnt FROM 
                 (SELECT a.id AS id, c.name AS name FROM 
                 orders_deploy a, appconf_project b, appconf_appowner c
                 WHERE a.app_name_id = b.id AND b.ops_id = c.id AND a.status = 1
                 AND (a.update_time >= '%s' AND a.update_time <= '%s')) d
                 GROUP BY name''' % ('%s 00:00:00' % sdate, '%s 23:59:59' % edate) 
    cursor.execute(deploy_sql)
    deploys = cursor.fetchall()
    return dict(deploys)


def _summary_dbscript(sdate, edate):
    cursor = connection.cursor()
    dbscript_sql = '''SELECT name, count(id) AS dbscript_cnt FROM 
                 (SELECT a.id AS id, c.name AS name FROM 
                 orders_dbscript a, appconf_database b, appconf_appowner c
                 WHERE a.db_name_id = b.id AND b.ops_id = c.id AND a.status = 1
                 AND (a.update_time >= '%s' AND a.update_time <= '%s')) d
                 GROUP BY name''' % ('%s 00:00:00' % sdate, '%s 23:59:59' % edate) 
    cursor.execute(dbscript_sql)
    dbscripts = cursor.fetchall()
    return dict(dbscripts)


def _summary_require(sdate, edate):
    cursor = connection.cursor()
    require_sql = '''SELECT name, count(id) AS require_cnt FROM 
                 (SELECT a.id AS id, b.name AS name FROM 
                 orders_require a, appconf_appowner b
                 WHERE a.owner_id = b.id AND a.status = 1
                 AND (a.update_time >= '%s' AND a.update_time <= '%s')) c
                 GROUP BY name''' % ('%s 00:00:00' % sdate, '%s 23:59:59' % edate) 
    cursor.execute(require_sql)
    requires = cursor.fetchall()
    return dict(requires)
