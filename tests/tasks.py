#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging

from celery.task import periodic_task
from django.db import transaction
from django.db.models import Q, Count

from appconf.models import Project
from tests.models import Environment, Versync, VersyncDetail
from lib.task import task_lock
from lib.harbor import fetch_latest_tag, retag_image_test
from lib.semaphore import semaphore_cookie, launch_task, sync_nginx_conf, get_task_status, get_environment_version, update_version

logger = logging.getLogger("opsadmin")

@transaction.atomic
@periodic_task(run_every=5)
@task_lock(timeout=60)
def versync_start():
    tag_success = []
    tag_failed = []
    versync_submit = Versync.objects.filter(sync_status=0)

    for versync in versync_submit:
        all_project = list(Project.objects.filter(product_id=versync.product.id).values_list("name", flat=True))

        for project in all_project:
            env = Environment.objects.filter(Q(project__name=project) & Q(is_enable=True))
            if not env:
                logger.warn("project: %s not found", project)
                continue
            env_value = env.values().first()
            pre_version = get_environment_version(env_value["pre_pid"], env_value["pre_tid"], project)
            if not pre_version:
                pre_version = "0.0.0"
            # For Docker APP
            if env_value["app_type"] == 0:
                codename = env.first().project.product.codename
                logger.info("codename: %s", codename)
                result = retag_image_test('%s/%s' % (codename, project), pre_version)
                logger.info("project: %s, version: %s, retag_image_test: %s", project, pre_version, result)
                if result:
                    VersyncDetail.objects.create(versync=versync,
                                                 project_id=env.values().first()["project_id"],
                                                 starttime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                                 task_status=0,
                                                 sync_version=pre_version)
                    env.update(task_status=0)
                    tag_success.append(project)
                else:
                    tag_failed.append(project)
            else:
                # For Non-Docker APP
                VersyncDetail.objects.create(versync=versync,
                                                 project_id=env.values().first()["project_id"],
                                                 starttime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                                 task_status=0,
                                                 sync_version=pre_version)
                env.update(task_status=0)
                tag_success.append(project)

        if tag_success and not tag_failed:
            Versync.objects.filter(Q(id=versync.id) & Q(sync_status=0)) \
                           .update(starttime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                                           sync_status=1,
                                                           progress=10)
        else:
            VersyncDetail.objects.filter(versync=versync).delete()
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            Versync.objects.filter(Q(id=versync.id) & Q(sync_status=0)) \
                           .update(starttime=now_time, endtime=now_time, sync_status=4)


@transaction.atomic
@periodic_task(run_every=5)
@task_lock(timeout=60)
def versync_run():
    task_submit = VersyncDetail.objects.filter(task_status=0)
    cookie = semaphore_cookie()
    for task in task_submit:
        try:
            version = task.sync_version
            env = Environment.objects.get(project=task.project)
            if env.app_type == 0:
                version = '%s.Test' % (version)

            logger.info("project: %s, version: %s", env.project.name, version)
            task_id = launch_task(cookie, env.test_pid, env.test_tid, task.project.name, version)
            env.task_id = task_id
            env.task_status = 1
            env.save()
            time.sleep(5)
            VersyncDetail.objects.filter(id=task.id).update(task_status=1, task_id=task_id)
        except Exception as e:
            logger.error("versync_run failed, error: %s", e)
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            Environment.objects.filter(task_id=task.id).update(task_status=3, endtime=now_time)
            VersyncDetail.objects.filter(id=task.id).update(endtime=now_time, task_status=3)
            Versync.objects.filter(Q(id=task.versync_id) & Q(sync_status=0)) \
                           .update(endtime=now_time, sync_status=4)


@transaction.atomic
@periodic_task(run_every=5)
@task_lock(timeout=60)
def update_task_status():
    task_running = VersyncDetail.objects.filter(task_status=1)
    cookie = semaphore_cookie()
    for task in task_running:
        try:
            env = Environment.objects.get(project=task.project)
            task_status = get_task_status(cookie, env.test_pid, task.task_id)
            logger.info("project: %s, task_status: %s", env.project.name, task_status)
            # app 同步成功后, 修改状态为2, 开始同步nginx
            if task_status == 'success':
                nginx_env = Environment.objects.filter(project__name='nginx').first()
                nginx_env.task_status = 0
                nginx_env.save()
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                Environment.objects.filter(task_id=task.task_id).update(task_status=2, endtime=now_time)
                VersyncDetail.objects.filter(id=task.id).update(endtime=now_time, task_status=2)
            elif task_status == 'error':
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                Environment.objects.filter(task_id=task.task_id).update(task_status=3, endtime=now_time)
                VersyncDetail.objects.filter(id=task.id).update(endtime=now_time, task_status=3)
        except Exception as e:
            logger.error("update_task_status failed, error: %s", e)
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            Environment.objects.filter(task_id=task.task_id).update(task_status=3, endtime=now_time)
            VersyncDetail.objects.filter(id=task.id).update(endtime=now_time, task_status=3)


@transaction.atomic
@periodic_task(run_every=5)
@task_lock(timeout=60)
def update_task_progress():
    progress_all = 80
    progress_step = {}
    total_all = VersyncDetail.objects.values("versync_id").annotate(total_cnt=Count('id'))
    for total in total_all:
        progress_step[total["versync_id"]] = progress_all / total["total_cnt"]

    end_all = VersyncDetail.objects.filter(task_status=2) \
                                        .values("versync_id") \
                                        .annotate(end_cnt=Count('id'))
    for end in end_all:
        progress = end["end_cnt"] * progress_step[end["versync_id"]]
        Versync.objects.filter(Q(id=end["versync_id"]) & Q(sync_status=1)) \
                       .update(progress=progress)


@transaction.atomic
@periodic_task(run_every=5)
@task_lock(timeout=60)
def versync_nginx():
    versync_running = Versync.objects.filter(sync_status=1)
    cookie = semaphore_cookie()
    for versync in versync_running:
        tasks = VersyncDetail.objects.filter(versync_id=versync.id).values("task_status")
        task_status = []
        for task in tasks:
            task_status.append(task["task_status"])
        if 3 in list(set(task_status)):
            Versync.objects.filter(id=versync.id).update(endtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                                        sync_status=4)
        if list(set(task_status)) == [2]:
            try:
                env = Environment.objects.filter(project__name='nginx').first()
                pre_version = get_environment_version(env.pre_pid, env.pre_tid, env.project.name)
                if not pre_version:
                    pre_version = "0.0.0"
                task_status = sync_nginx_conf(cookie, env, pre_version)
                if task_status:
                    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    env.endtime = now_time
                    env.task_status = 2
                    env.save()
                    VersyncDetail.objects.create(versync=versync,
                                                 project_id=env.project_id,
                                                 starttime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                                 task_status=2,
                                                 sync_version=pre_version)

                    Versync.objects.filter(Q(id=versync.id) & Q(sync_status=1)) \
                                   .update(starttime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                                                   sync_status=2,
                                                                   progress=90)
                else:
                    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                    env.task_status = 3
                    env.endtime = now_time
                    env.save()
                    Versync.objects.filter(Q(id=versync.id) & Q(sync_status=1)) \
                                    .update(endtime=now_time, sync_status=4)
            except Exception as e:
                logger.error("sync_nginx_conf failed, error: %s", e)
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                env = Environment.objects.filter(project__name='nginx').first()
                env.task_status = 3
                env.endtime = now_time
                env.save()
                Versync.objects.filter(Q(id=versync.id) & Q(sync_status=1)) \
                               .update(endtime=now_time, sync_status=4)


@transaction.atomic
@periodic_task(run_every=5)
@task_lock(timeout=60)
def versync_stop():
    versync_nginx = Versync.objects.filter(sync_status=2)
    for versync in versync_nginx:
        if versync.sync_status == 2:
            Versync.objects.filter(Q(id=versync.id) & Q(sync_status=2)) \
                           .update(endtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                   sync_status=3,
                                   progress=100)
            tasks = VersyncDetail.objects.filter(versync_id=versync.id)
            logger.info(tasks)
            for task in tasks:
                env = Environment.objects.filter(project=task.project)
                env_value = env.values().first()
                try:
                    test_version = task.sync_version
                    if env_value["app_type"] == 0:
                        test_version = '%s.Test' % test_version
                    cookie = semaphore_cookie()
                    result = update_version(cookie, env_value["test_pid"], env_value["test_tid"], task.project.name, test_version)
                    if not result:
                        logger.error("project: %s, test_version: %s, update_version failed, result: %s", task.project.name, test_version, result)
                        continue
                    logger.info("update_version, project: %s, pid: %s, tid: %s, test_version: %s, pre_version: %s",
                            task.project.name,
                            env_value["test_pid"],
                            env_value["test_tid"],
                            test_version,
                            task.sync_version)
                    env.update(test_ver=test_version, pre_ver=task.sync_version)
                except Exception as e:
                    logger.error(e)
                finally:
                    task.delete()

