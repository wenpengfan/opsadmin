#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import cookielib
import time
import logging

from config.views import get_dir
from tests.models import Environment

logger = logging.getLogger("opsadmin")

semaphore_domain = semaphore_domain = get_dir("semaphore_domain")
semaphore_api = '%s/api' % semaphore_domain

def http_request(cookie, url, headers, method, data=None):
    cookie_handler = urllib2.HTTPCookieProcessor(cookie)
    url_opener = urllib2.build_opener(cookie_handler)
    urllib2.install_opener(url_opener)

    url = '%s/%s' % (semaphore_api, url.lstrip('/'))
    request = urllib2.Request(url, headers=headers, data=data)
    request.get_method = lambda: method
    response = urllib2.urlopen(request)

    return response

def http_get(cookie, url, headers=None):
    if not headers:
        headers = {"Accept": "application/json"}
    response = http_request(cookie, url, headers, "GET")

    return response


def http_post(cookie, url, data, headers=None):
    if not headers:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = http_request(cookie, url, headers, "POST", data)

    return response

def http_put(cookie, url, data, headers=None):
    if not headers:
        headers = {"Accept": "application/json"}
    response = http_request(cookie, url, headers, "PUT", data)

    return response

def semaphore_cookie():
    semaphore_domain = get_dir("semaphore_domain")
    api_url = "%s/api" % semaphore_domain
    login_url = "%s/auth/login" % api_url
    login_content = {
                     "auth": get_dir("semaphore_username"),
                     "password": get_dir("semaphore_password")
                    }
    cookie_jar = cookielib.CookieJar()
    cookie_handler = urllib2.HTTPCookieProcessor(cookie_jar)
    url_opener = urllib2.build_opener(cookie_handler)
    urllib2.install_opener(url_opener)

    jdata = json.dumps(login_content)
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    request = urllib2.Request(login_url, data=jdata, headers=headers)
    response = urllib2.urlopen(request)

    return cookie_jar


def launch_task(cookie, project_id, template_id, project_name, version):
    semaphore_domain = get_dir("semaphore_domain")
    api_url = "%s/api" % semaphore_domain
    task_url = "%s/project/%s/tasks" % (api_url, project_id)
    name_ = "%s_version" % project_name.replace("-", "_")
    env_conf = get_environment_conf(cookie, project_id, template_id)
    env_conf[name_] = version
    env = json.dumps(env_conf)
    logger.info("project: %s, version: %s, env: %s", project_name, version, env)
    task_content = {
                        "template_id": template_id,
                        "debug": False,
                        "dry_run": False,
                        "playbook": "",
                        "environment": env
                   }
    cookie_handler = urllib2.HTTPCookieProcessor(cookie)
    url_opener = urllib2.build_opener(cookie_handler)
    urllib2.install_opener(url_opener)

    body = json.dumps(task_content)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    request = urllib2.Request(task_url, data=body, headers=headers)
    response = urllib2.urlopen(request)

    ret = json.loads(response.read())
    return ret["id"]


def sync_nginx_conf(cookie, env, version):
    task_id = launch_task(cookie, env.test_pid, env.test_tid, env.project.name, version)
    task_status = get_task_status(cookie, env.test_pid, task_id)
    if task_status == 'waiting' or task_status == 'running':
        env.task_status = 1
    env.task_id = task_id
    env.save()
    while task_status == 'running' or task_status == 'waiting':
        time.sleep(5)
        task_status = get_task_status(cookie, env.test_pid, task_id)

    logger.info("project: %s, task_status: %s", env.project.name, task_status)
    if task_status == 'success':
        return True
    else:
        return False


def get_task_status(cookie, project_id, task_id):
    semaphore_domain = get_dir("semaphore_domain")
    api_url = "%s/api" % semaphore_domain
    task_url = "%s/project/%s/tasks" % (api_url, project_id)
    output_url = "%s/%s" % (task_url, task_id)

    cookie_handler = urllib2.HTTPCookieProcessor(cookie)
    url_opener = urllib2.build_opener(cookie_handler)
    urllib2.install_opener(url_opener)

    headers = {"Accept": "application/json"}
    request = urllib2.Request(output_url, headers=headers)
    response = urllib2.urlopen(request)

    ret = json.loads(response.read())
    return ret["status"]

def get_task_info(cookie, project_id, task_id):
    output_url = "/project/%s/tasks/%s" % (project_id, task_id)
    response = http_get(cookie, output_url)

    ret = json.loads(response.read())
    return ret

def get_task_output(cookie, project_id, task_id):
    output_url = "/project/%s/tasks/%s/output" % (project_id, task_id)
    response = http_get(cookie, output_url)

    ret = json.loads((response.read()))
    return ret

def get_environment_version(project_id, template_id, app_name):
    cookie = semaphore_cookie()
    env_conf = get_environment_conf(cookie, project_id, template_id)
    version_name = "%s_version" % app_name.replace("-", "_")
    if not env_conf.has_key(version_name):
        return None

    return env_conf[version_name]

def get_template_environment_id(cookie, project_id, template_id):
    template_url = "/project/%s/templates/%s" % (project_id, template_id)
    response = http_get(cookie, template_url)

    ret = json.loads(response.read())
    return ret["environment_id"]

def get_environment_conf(cookie, project_id, template_id):
    environment_info = get_environment_info(cookie, project_id, template_id)
    env_conf = json.loads(environment_info["json"])

    return env_conf


def get_environment_info(cookie, project_id, template_id):
    environment_id = get_template_environment_id(cookie, project_id, template_id)
    if not environment_id:
        logger.error("environment is not configured")
        return None

    environment_url = "/project/%s/environments/%s" % (project_id, environment_id)
    response = http_get(cookie, environment_url)

    ret = json.loads(response.read())
    return ret

def update_version(cookie, pid, tid, app_name, app_version):
    env_info = get_environment_info(cookie, pid, tid)

    version_name = "%s_version" % app_name.replace("-", "_")
    env_conf = get_environment_conf(cookie, pid, tid)
    env_conf[version_name] = app_version

    env_info["json"] = json.dumps(env_conf, indent=4)
    env_json = json.dumps(env_info)
    response = update_environment_info(cookie, pid, tid, env_json)
    status_code = response.getcode()

    if status_code != 204:
        logger.error('update_environment_info failed, status_code: %d', status_code)
        return False
    return True

def update_environment_info(cookie, project_id, template_id, env_json):
    environment_id = get_template_environment_id(cookie, project_id, template_id)
    if not environment_id:
        logger.error("environment is not configured")
        return None

    environment_url = "/project/%s/environment/%s" % (project_id, environment_id)
    response = http_put(cookie, environment_url, env_json)

    return response

