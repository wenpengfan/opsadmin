#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from orders.models import Config
from orders.forms import ConfigScriptForm, ConfigScriptEditForm
from appconf.models import Database, AppOwner
from accounts.permission import permission_verify
from lib.api import pages
from lib.dingding import dingding_msg
import datetime


@login_required
@permission_verify()
def config_list(request):
    config_status = request.GET.get('config_status', '')
    keyword = request.GET.get('keyword', '').encode('utf8')
    if keyword:
        keyword_config = Config.objects.filter(Q(app_name__name__icontains=keyword) \
                                               | Q(order_user=keyword))
    else:
        keyword_config = Config.objects.all()

    if request.user.is_superuser:
        if not config_status:
            all_config = Config.objects.filter(status=0) & keyword_config
        elif config_status == '-1':
            all_config = keyword_config
        else:
            all_config = Config.objects.filter(status=config_status) & keyword_config
    else:
        username = request.user.username
        if not config_status:
            owner = Config.objects.filter(
                Q(app_name__product__owner__username__username=username) & Q(status=0)) & keyword_config
            ops = Config.objects.filter(Q(app_name__ops__username__username=username) & Q(status=0)) & keyword_config
            configs = Config.objects.filter(Q(order_user=username) & Q(status=0)) & keyword_config
            all_config = owner | ops | configs
        elif config_status == '-1':
            owner = Config.objects.filter(app_name__product__owner__username__username=username) & keyword_config
            ops = Config.objects.filter(app_name__ops__username__username=username) & keyword_config
            configs = Config.objects.filter(order_user=username) & keyword_config
            all_config = owner | ops | configs
        else:
            owner = Config.objects.filter(
                Q(app_name__product__owner__username__username=username) & Q(status=config_status)) & keyword_config
            ops = Config.objects.filter(
                Q(app_name__ops__username__username=username) & Q(status=config_status)) & keyword_config
            configs = Config.objects.filter(Q(order_user=username) & Q(status=config_status)) & keyword_config
            all_config = owner | ops | configs

    page_len = request.GET.get('page_len', '')
    configs_list, p, configs, page_range, current_page, show_first, show_end, end_page = pages(all_config, request)
    return render(request, 'orders/config_list.html', locals())


@login_required
@permission_verify()
def config_add(request):
    status = 0
    if request.method == 'POST':
        env_list = request.POST.getlist('checkbox_env')
        if env_list:
            for env in env_list:
                form = ConfigScriptForm(request.POST)
                if form.is_valid():
                    app_name = form.cleaned_data["app_name"].name
                    config_form = form.save(commit=False)
                    config_form.order_user = request.user.username
                    config_form.env = env
                    config_id = config_form.id
                    config_form.save()
                    msg_user = Database.objects.filter(name=app_name).values("ops__dingding").first()
                    if app_name is not None and msg_user is not None:
                        if msg_user["ops__dingding"] is not None:
                            dingding_msg.delay(msg_user["ops__dingding"],
                                               u"您有配置更新（编号：%s）需要处理，环境：%s，应用名称：%s，应用版本号:%s, 配置版本号：%s"
                                               % (config_id, env, app_name, config_form.app_version, config_form.conf_version))
                    status = 1
                else:
                    status = 3
                    break
            if status == 1:
                return HttpResponseRedirect(reverse('config_list'))
        else:
            form = ConfigScriptForm(request.POST)
            status = 4
    else:
        form = ConfigScriptForm()

    results = {
        'form': form,
        'status': status,
        'request': request,
    }
    return render(request, 'orders/config_base.html', results)

@login_required
@permission_verify()
def config_edit(request, config_id):
    try:
        if request.user.is_superuser or request.user.is_staff:
            config = Config.objects.get(id=config_id)
        else:
            config = Config.objects.get(Q(id=config_id) & Q(order_user=request.user.username))
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    if request.method == 'POST':
        form = ConfigScriptEditForm(request.POST, instance=config)
        if form.is_valid():
            config_form = form.save(commit=False)
            config_form.order_user = request.user.username
            config_form.save()
            return HttpResponseRedirect(reverse('config_list'))
    else:
        form = ConfigScriptEditForm(instance=config)

    results = {
        'form': form,
        'config_id': config_id,
        'request': request,
    }
    return render(request, 'orders/config_base.html', results)


@login_required
@permission_verify()
def config_del(request):
    config_id = request.GET.get('id', '')
    if config_id:
        try:
            if request.user.is_superuser or request.user.is_staff:
                Config.objects.filter(id=config_id).delete()
            else:
                Config.objects.filter(Q(id=config_id) & Q(order_user=request.user.username)).delete()
        except:
            return HttpResponseRedirect(reverse('permission_deny'))

    config_id_all = str(request.POST.get('config_id_all', ''))
    if config_id_all:
        for config_id in config_id_all.split(','):
            if request.user.is_superuser or request.user.is_staff:
                config = Config.objects.get(id=config_id)
            else:
                try:
                    config = Config.objects.get(Q(id=config_id) & Q(order_user=request.user.username))
                except:
                    return HttpResponseRedirect(reverse('permission_deny'))

            if config.status == 0:
                Config.objects.filter(id=config_id).delete()

    return HttpResponseRedirect(reverse('config_list'))


@login_required
@permission_verify()
def config_finish(request, config_id):
    if config_id:
        Config.objects.filter(id=config_id).update(status=1, update_time=datetime.datetime.now(),
                                                   completion_time=datetime.datetime.now())

        config = Config.objects.get(id=config_id)

        app_name = Config.objects.filter(id=config_id).values("app_name__name").first()
        msg_user = AppOwner.objects.filter(username__username=config.order_user).values("dingding").first()

        if msg_user is not None and app_name is not None:
            if msg_user["dingding"] is not None:
                dingding_msg.delay(msg_user["dingding"], \
                                   u"您的工单（编号：%s）已处理，环境：%s，应用名称：%s" \
                                   % (config_id, config.env, app_name["app_name__name"]))

    return HttpResponseRedirect(reverse('config_list'))


@login_required
@permission_verify()
def config_detail(request, config_id):
    try:
        if request.user.is_superuser or request.user.is_staff:
            config = Config.objects.filter(id=config_id)
        else:
            config = Config.objects.filter(Q(id=config_id) & Q(order_user=request.user.username))
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    config_desc = config.values("description").first()

    if config_desc["description"] is None:
        config = Config.objects.filter(config__id=config_id).order_by("-create_time")

    results = {
        'config_detail': config,

    }
    return render(request, 'orders/config_detail.html', results)
