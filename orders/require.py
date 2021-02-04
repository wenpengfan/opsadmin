#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from orders.models import Require 
from orders.forms import RequireForm
from appconf.models import AppOwner
from accounts.permission import permission_verify, permission_deny
from lib.api import pages
from lib.dingding import dingding_msg
import datetime


@login_required
@permission_verify()
def require_list(request):
    require_status = request.GET.get('require_status','')
    keyword = request.GET.get('keyword','').encode('utf8')
    if keyword:
        keyword_require = Require.objects.filter(Q(title__icontains=keyword) \
                                                | Q(owner__username__username__icontains=keyword) \
                                                | Q(order_user__icontains=keyword))
    else:
        keyword_require = Require.objects.all() 

    if request.user.is_superuser or request.user.is_staff:
        if not require_status:
            all_require = Require.objects.filter(status=0) & keyword_require
        elif require_status == '-1':
            all_require = keyword_require
        else:
            all_require = Require.objects.filter(status=require_status) & keyword_require
    else:
        username = request.user.username
        if not require_status:
            owner = Require.objects.filter(Q(owner__username__username=username) & Q(status=0)) & keyword_require
            requires = Require.objects.filter(Q(order_user=username) & Q(status=0)) & keyword_require
            all_require = owner | requires
        elif require_status == '-1':
            owner = Require.objects.filter(owner__username__username=username) & keyword_require
            requires = Require.objects.filter(order_user=username) & keyword_require
            all_require = owner | requires
        else:
            owner = Require.objects.filter(Q(owner__username__username=username) & Q(status=require_status)) & keyword_require
            requires = Require.objects.filter(Q(order_user=username) & Q(status=require_status)) & keyword_require
            all_require = owner | requires

    page_len = request.GET.get('page_len', '')
    requires_list, p, requires, page_range, current_page, show_first, show_end, end_page = pages(all_require, request)
    return render(request, 'orders/require_list.html', locals())


@login_required
@permission_verify()
def require_add(request):
    if request.method == 'POST':
        form = RequireForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            owner = form.cleaned_data["owner"]
            msg_user = AppOwner.objects.filter(name=owner).values("dingding").first()

            db_form = form.save(commit=False)
            db_form.order_user = request.user.username 
            db_form.save()
            require_id = db_form.id
            
            if title is not None and msg_user is not None:
                if msg_user["dingding"] is not None:
                    dingding_msg.delay(msg_user["dingding"], u"您有新的工单（编号：%s）需要处理，标题为：%s" % (require_id, title))
            return HttpResponseRedirect(reverse('require_list'))
    else:
        form = RequireForm()

    results = {
        'form': form,
        'request': request,
    }
    return render(request, 'orders/require_base.html', results)


@login_required
@permission_verify()
def require_edit(request, require_id):
    try:
        if request.user.is_superuser or request.user.is_staff:
            require = Require.objects.get(id=require_id)
            owner_id = require.owner_id
        else:
            require = Require.objects.get(Q(id=require_id) & Q(order_user=request.user.username))
            owner_id = require.owner_id
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    if request.method == 'POST':
        form = RequireForm(request.POST, instance=require)
        if form.is_valid():
            priv_owner_id = owner_id 
            cur_owner_id = form.cleaned_data["owner"].id
            title = form.cleaned_data["title"]
            form.save()

            if priv_owner_id != cur_owner_id:
                msg_user = AppOwner.objects.filter(id=cur_owner_id).values("dingding").first()
                if title is not None and msg_user is not None:
                    if msg_user["dingding"] is not None:
                        dingding_msg.delay(msg_user["dingding"], u"您有新的工单（编号：%s）需要处理，标题为：%s" % (require_id, title))
            return HttpResponseRedirect(reverse('require_list'))
    else:
        form = RequireForm(instance=require)

    results = {
        'form': form,
        'require_id': require_id,
        'request': request,
    }
    return render(request, 'orders/require_base.html', results)


@login_required
@permission_verify()
def require_del(request):
    require_id = request.GET.get('id', '')
    if require_id:
        try:
            if request.user.is_superuser or request.user.is_staff:
                Require.objects.filter(id=require_id).delete()
            else:
                Require.objects.filter(Q(id=require_id) & Q(order_user=request.user.username)).delete()
        except:
            return HttpResponseRedirect(reverse('permission_deny'))

    require_id_all = str(request.POST.get('require_id_all', ''))
    if require_id_all:
        for require_id in require_id_all.split(','):
            if request.user.is_superuser or request.user.is_staff:
                require = Require.objects.get(id=require_id)
            else:
                try:
                    require = Require.objects.get(Q(id=require_id) & Q(order_user=request.user.username))
                except:
                    return HttpResponseRedirect(reverse('permission_deny'))

            if require.status == 0: 
                Require.objects.filter(id=require_id).delete()

    return HttpResponseRedirect(reverse('require_list'))


@login_required
@permission_verify()
def require_finish(request, require_id):
    if require_id:
            Require.objects.filter(id=require_id).update(status=1, update_time=datetime.datetime.now(),completion_time=datetime.datetime.now())

            require = Require.objects.get(id=require_id)
            title = require.title
            msg_user = AppOwner.objects.filter(username__username=require.order_user).values("dingding").first()
            if msg_user is not None and title is not None:
                if msg_user["dingding"] is not None:
                    dingding_msg.delay(msg_user["dingding"], u"您的工单（编号：%s）已处理，标题为：%s" % (require_id, title))

    return HttpResponseRedirect(reverse('require_list'))


@login_required
@permission_verify()
def require_detail(request, require_id):
    try:
        if request.user.is_superuser or request.user.is_staff:
            require = Require.objects.filter(id=require_id)
        else:
            require = Require.objects.filter(Q(id=require_id) & Q(order_user=request.user.username))
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    results = {
        'require_detail': require,
    }
    return render(request, 'orders/require_detail.html', results)
