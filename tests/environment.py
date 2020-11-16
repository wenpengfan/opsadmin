#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import json
import random
import time
from pytz import timezone
from datetime import datetime
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from dwebsocket.decorators import accept_websocket

from accounts.permission import permission_verify
from appconf.models import Product, Project
from tests.models import Environment
from lib.api import pages
from lib.semaphore import semaphore_cookie, get_environment_version, get_task_info, get_task_status, get_task_output

import logging

logger = logging.getLogger("opsadmin")


@login_required
@permission_verify()
def env_prepare(request):
    product_id = int(request.GET.get('product_id', 0))
    all_product = Product.objects.filter(qa_id__isnull=False)
    if product_id != 0:
        project = Project.objects.filter(Q(product_id=product_id) & Q(is_offline=False))
        all_env = Environment.objects.filter(Q(project__in=project) & Q(is_enable=True))
    else:
        all_env = Environment.objects.all()
    page_len = request.GET.get('page_len', '')
    envs_list, p, envs, page_range, current_page, show_first, show_end, end_page = pages(all_env, request)
    return render(request, 'tests/env_prepare.html', locals())


@login_required
@permission_verify()
def project_sync(request):
    status = 0
    product_id = int(request.POST.get('product_id', 0))
    if product_id != 0:
        project = Project.objects.filter(product_id=product_id)
        for proj in project:
            if proj.is_offline == False:
                app_type = 0 if proj.docker_expose else 1
                env = Environment.objects.filter(project=proj)
                if not env:
                    Environment.objects.create(project=proj, is_enable=True, test_ver='0.0.0', pre_ver='0.0.0', app_type=app_type)
                else:
                    _env = Environment.objects.get(project=proj)
                    _env.app_type = app_type
                    _env.save()
            else:
                Environment.objects.filter(project=proj).delete()
            update_app_version(proj)
        Environment.objects.filter(project_id__isnull=True).delete()
        status = 1
    else:
        status = 2
    return HttpResponse(status)

def update_app_version(proj):
    env = Environment.objects.get(project=proj)
    cookie = semaphore_cookie()
    if env.pre_pid != 0 and env.pre_tid != 0:
        try:
            pre_version = get_environment_version(env.pre_pid, env.pre_tid, env.project.name)
            logging.info('name: %s, pre version: %s' % (env.project.name, pre_version))
            if pre_version:
                env.pre_ver = pre_version
            else:
                env.pre_ver = '0.0.0'
        except Exception as e:
            env.pre_ver = '0.0.0'
            logger.error(e)
    if env.test_pid != 0 and env.test_tid != 0:
        try:
            test_version = get_environment_version(env.test_pid, env.test_tid, env.project.name)
            logging.info('name: %s, test version: %s' % (env.project.name, test_version))
            if test_version:
                env.test_ver = test_version
            else:
                env.test_ver = '0.0.0'
        except Exception as e:
            env.test_ver = '0.0.0'
            logger.error(e)
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    env.endtime = now_time
    env.save()

@login_required
@permission_verify()
def env_edit(request):
    if request.method == 'GET':
        env_id = request.GET.get("id")
        env = Environment.objects.get(id=env_id)
        product_id = Project.objects.get(id=env.project_id).product_id
        project = Project.objects.filter(Q(product_id=product_id) & Q(is_offline=False))
        pid_perhaps = Environment.objects.filter(project__in=project).values("pre_pid").first()
    return render(request, "tests/env_edit.html", locals())  


@login_required
@permission_verify()
def env_save(request):
    if request.method == 'POST':
        env_id = request.POST.get('env_id')
        env_pre_pid = request.POST.get('env_pre_pid')
        env_pre_tid = request.POST.get('env_pre_tid')
        env_test_pid = request.POST.get('env_test_pid')
        env_test_tid = request.POST.get('env_test_tid')
        env = Environment.objects.get(id=env_id)
        env.pre_pid =env_pre_pid
        env.pre_tid = env_pre_tid
        env.test_pid = env_test_pid
        env.test_tid = env_test_tid
        env.save()
        status = 1
    else:
        status = 2
    envs = Environment.objects.all()
    return render(request, "tests/env_edit.html", locals())


@login_required
@permission_verify()
def env_disable(request):
    env_id_all = str(request.POST.get('env_id_all', ''))
    if env_id_all:
        for env_id in env_id_all.split(','):
            try:
                Environment.objects.filter(id=env_id).update(is_enable=False)
            except:
                return HttpResponseRedirect(reverse('permission_deny'))

    return HttpResponseRedirect(reverse('env_prepare'))


@login_required
@permission_verify()
def env_enable(request):
    env_id_all = str(request.POST.get('env_id_all', ''))
    if env_id_all:
        for env_id in env_id_all.split(','):
            try:
                Environment.objects.filter(id=env_id).update(is_enable=True)
            except:
                return HttpResponseRedirect(reverse('permission_deny'))

    return HttpResponseRedirect(reverse('env_prepare'))

@login_required
@permission_verify()
@accept_websocket
def env_task_log(request):
    if not request.is_websocket():
        env_id = request.GET.get("id")
        return render(request, 'tests/task_log.html', locals())
    else:
        env_id = 0
        for message in request.websocket:
            if message:
                env_id = message
                break
        try:
            cookie = semaphore_cookie()
            env = Environment.objects.filter(id=env_id).first()
            task_info = get_task_info(cookie, env.test_pid, env.task_id)
            task_status = task_info["status"]
            created_time = parse_datetime(task_info["created"])
            if task_status == 'waiting':
                request.websocket.send("*"*30 + "Waiting: " + created_time + "*"*30)
            while task_status == 'waiting':
                time.sleep(3)
                task_status = get_task_status(cookie, env.test_pid, env.task_id)

            task_info = get_task_info(cookie, env.test_pid, env.task_id)
            start_time = parse_datetime(task_info["start"])
            if start_time:
                request.websocket.send("*"*30 + "Start:   " + start_time + "*"*30 + "\n")
            while task_status == 'running':
                time.sleep(3)
                task_status = get_task_status(cookie, env.test_pid, env.task_id)
                if task_status != 'running':
                    ret = get_task_output(cookie, env.test_pid, env.task_id)
                    for line in ret:
                        request.websocket.send(line["output"])
                        time.sleep(random.randint(1,30)*0.01)
            else:
                 ret = get_task_output(cookie, env.test_pid, env.task_id)
                 for line in ret:
                     request.websocket.send(line["output"])
            task_info = get_task_info(cookie, env.test_pid, env.task_id)
            end_time = parse_datetime(task_info["end"])
            if end_time:
                request.websocket.send("*"*30 + "End:     " + end_time + "*"*30)
            request.websocket.send("*"*30 + "Status:  " + task_status + "*"*30)
        except Exception as e:
            logger.error(e)

def parse_datetime(t):
    if not t:
        return None
    src_datetime = datetime.strptime(t, '%Y-%m-%dT%H:%M:%SZ')
    tz_sh = timezone('Asia/Shanghai')
    tz_utc = timezone('UTC')
    dst_datetime = src_datetime.replace(tzinfo=tz_utc).astimezone(tz_sh)
    return dst_datetime.strftime('%Y-%m-%d %H:%M:%S')

def parse_datetime_timestamp(t):
    date_time = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = int(time.mktime(date_time.timetuple()))
    return str(timestamp)

@login_required
@permission_verify()
def env_task_status(request):
    env_status = {}
    environment_id_all = str(request.POST.get('environment_id_all', ''))
    if environment_id_all:
        for env_id in environment_id_all.split(','):
            try:
                env = Environment.objects.get(id=env_id)
                env_status[env_id] = "%s;%s;%s" % (env.task_status, env.project.name, env.endtime)
            except:
                return HttpResponseRedirect(reverse('permission_deny'))
    return HttpResponse(json.dumps(env_status, ensure_ascii=False))
