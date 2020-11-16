#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import FileResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from orders.models import DBScript, Deploy
from orders.forms import DBScriptForm, DBScriptEditForm
from appconf.models import Database, AppOwner
from config.views import get_dir
from accounts.permission import permission_verify, permission_deny
from lib.api import pages
from lib.dingding import dingding_msg
import datetime
import os
import shutil


@login_required
@permission_verify()
def dbscript_list(request):
    dbscript_status = request.GET.get('dbscript_status','')
    keyword = request.GET.get('keyword','').encode('utf8')
    if keyword:
        keyword_dbscript = DBScript.objects.filter(Q(db_name__name__icontains=keyword) \
                                                  | Q(order_user=keyword))
    else:
        keyword_dbscript = DBScript.objects.all()

    if request.user.is_superuser:
        if not dbscript_status:
            all_dbscript = DBScript.objects.filter(status=0) & keyword_dbscript
        elif dbscript_status == '-1':
            all_dbscript = keyword_dbscript
        else:
            all_dbscript = DBScript.objects.filter(status=dbscript_status) & keyword_dbscript
    else:
        username = request.user.username
        if not dbscript_status:
            owner = DBScript.objects.filter(Q(db_name__product__owner__username__username=username) & Q(status=0)) & keyword_dbscript
            ops = DBScript.objects.filter(Q(db_name__ops__username__username=username) & Q(status=0)) & keyword_dbscript
            dbscripts = DBScript.objects.filter(Q(order_user=username) & Q(status=0)) & keyword_dbscript
            all_dbscript = owner | ops | dbscripts
        elif dbscript_status == '-1':
            owner = DBScript.objects.filter(db_name__product__owner__username__username=username) & keyword_dbscript
            ops = DBScript.objects.filter(db_name__ops__username__username=username) & keyword_dbscript
            dbscripts = DBScript.objects.filter(order_user=username) & keyword_dbscript
            all_dbscript = owner | ops | dbscripts
        else:
            owner = DBScript.objects.filter(Q(db_name__product__owner__username__username=username) & Q(status=dbscript_status)) & keyword_dbscript
            ops = DBScript.objects.filter(Q(db_name__ops__username__username=username) & Q(status=dbscript_status)) & keyword_dbscript
            dbscripts = DBScript.objects.filter(Q(order_user=username) & Q(status=dbscript_status)) & keyword_dbscript
            all_dbscript = owner | ops | dbscripts

    page_len = request.GET.get('page_len', '')
    dbscripts_list, p, dbscripts, page_range, current_page, show_first, show_end, end_page = pages(all_dbscript, request)
    return render(request, 'orders/dbscript_list.html', locals())


@login_required
@permission_verify()
def dbscript_add(request):
    status = 0
    if request.method == 'POST':
        dbscript_file = request.FILES.get("dbscript_file", None)
        env_list = request.POST.getlist('checkbox_env')
        if env_list:
            for env in env_list:
                form = DBScriptForm(request.POST)
                if form.is_valid() and dbscript_file:
                    db_name = form.cleaned_data["db_name"].name
                    script_path = os.path.join(get_dir("script_path"), db_name, env)
                    if not os.path.exists(script_path):
                        os.makedirs(script_path)

                    file = os.path.join(script_path, dbscript_file.name)
                    if not os.path.exists(file):
                        destination = open(file, 'wb+')
                        for chunk in dbscript_file.chunks():
                            destination.write(chunk)
                        destination.close() 

                        db_form = form.save(commit=False)
                        db_form.script_name = dbscript_file.name
                        db_form.order_user = request.user.username 
                        db_form.env = env
                        db_form.save()
                        
                        dbscript_id = db_form.id
                        msg_user = Database.objects.filter(name=db_name).values("ops__dingding").first() 
                        if db_name is not None and msg_user is not None:
                            if msg_user["ops__dingding"] is not None:
                                dingding_msg.delay(msg_user["ops__dingding"], \
                                                   u"您有数据库更新（编号：%s）需要处理，环境：%s，数据库名：%s，脚本：%s" \
                                                   % (dbscript_id, env, db_name, dbscript_file.name))
                        status = 1
                    else:
                        status = 3
                        break
                else:
                    status = 2
                    break
            if status == 1:
                return HttpResponseRedirect(reverse('dbscript_list'))
        else:
            form = DBScriptForm(request.POST)
            status = 4
    else:
        form = DBScriptForm()

    results = {
        'form': form,
        'status': status,
        'request': request,
    }
    return render(request, 'orders/dbscript_base.html', results)


@login_required
@permission_verify()
def dbscript_add_mini(request):
    status = 0
    dbscript_id = 0
    if request.method == 'POST':
        form = DBScriptForm(request.POST)
        dbscript_file = request.FILES.get("dbscript_file", None)
        env = "Pro"
        if form.is_valid() and dbscript_file:
            db_name = form.cleaned_data["db_name"].name
            script_path = os.path.join(get_dir("script_path"), db_name, env)
            if not os.path.exists(script_path):
                os.makedirs(script_path)

            file = os.path.join(script_path, dbscript_file.name)
            if not os.path.exists(file):
                destination = open(file, 'wb+')
                for chunk in dbscript_file.chunks():
                    destination.write(chunk)
                destination.close() 

                db_form = form.save(commit=False)
                db_form.script_name = dbscript_file.name
                db_form.order_user = request.user.username 
                db_form.env = env
                db_form.save()
                dbscript_id = db_form.id

                msg_user = Database.objects.filter(name=db_name).values("ops__dingding").first() 
                if db_name is not None and msg_user is not None:
                    if msg_user["ops__dingding"] is not None:
                        dingding_msg.delay(msg_user["ops__dingding"], \
                                           u"您有数据库更新（编号：%s）需要处理，环境：%s，数据库名：%s，脚本：%s" \
                                           % (dbscript_id, env, db_name, dbscript_file.name))

                status = 1
                dbscript_id = DBScript.objects.get(Q(db_name__name=db_name) & Q(script_name=dbscript_file.name) & Q(status=0)).id
            else:
                status = 3
        else:
            status = 2
    else:
        form = DBScriptForm()

    results = {
        'form': form,
        'request': request,
        'status': status,
        'dbscript_id': dbscript_id,
    }
    return render(request, 'orders/dbscript_add_mini.html', results)


@login_required
@permission_verify()
def dbscript_edit(request, dbscript_id):
    try:
        if request.user.is_superuser or request.user.is_staff:
            dbscript = DBScript.objects.get(id=dbscript_id)
        else:
            dbscript = DBScript.objects.get(Q(id=dbscript_id) & Q(order_user=request.user.username))
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    if request.method == 'POST':
        form = DBScriptEditForm(request.POST, instance=dbscript)
        if form.is_valid():
            db_form = form.save(commit=False)
            db_form.order_user = request.user.username 
            db_form.save()
            return HttpResponseRedirect(reverse('dbscript_list'))
    else:
        form = DBScriptEditForm(instance=dbscript)

    results = {
        'form': form,
        'dbscript_id': dbscript_id,
        'request': request,
    }
    return render(request, 'orders/dbscript_base.html', results)


@login_required
@permission_verify()
def dbscript_del(request):
    dbscript_id = request.GET.get('id', '')
    if dbscript_id:
        try:
            if request.user.is_superuser or request.user.is_staff:
                dbscript = DBScript.objects.get(id=dbscript_id)
                DBScript.objects.filter(id=dbscript_id).delete()
            else:
                dbscript = DBScript.objects.get(Q(id=dbscript_id) & Q(order_user=request.user.username))
                DBScript.objects.filter(Q(id=dbscript_id) & Q(order_user=request.user.username)).delete()
        except:
            return HttpResponseRedirect(reverse('permission_deny'))

        script_path = os.path.join(get_dir("script_path"), dbscript.db_name.name, dbscript.env)
        file = os.path.join(script_path, dbscript.script_name)
        if os.path.exists(file):
            os.remove(file)

    dbscript_id_all = str(request.POST.get('dbscript_id_all', ''))
    if dbscript_id_all:
        for dbscript_id in dbscript_id_all.split(','):
            try:
                if request.user.is_superuser or request.user.is_staff:
                    dbscript = DBScript.objects.get(id=dbscript_id)
                else:
                    dbscript = DBScript.objects.get(Q(id=dbscript_id) & Q(order_user=request.user.username))
            except:
                return HttpResponseRedirect(reverse('permission_deny'))

            script_path = os.path.join(get_dir("script_path"), dbscript.db_name.name, dbscript.env)

            if dbscript.status == 0: 
                DBScript.objects.filter(id=dbscript_id).delete()
                file = os.path.join(script_path, dbscript.script_name)
                if os.path.exists(file):
                    os.remove(file)

    return HttpResponseRedirect(reverse('dbscript_list'))


@login_required
@permission_verify()
def dbscript_finish(request, dbscript_id):
    if dbscript_id:
        DBScript.objects.filter(id=dbscript_id).update(status=1, update_time=datetime.datetime.now(),completion_time=datetime.datetime.now())

        dbscript = DBScript.objects.get(id=dbscript_id)

        script_path = os.path.join(get_dir("script_path"), dbscript.db_name.name, dbscript.env)
        archive_path = os.path.join(script_path, "archive")
        archive_file = str(dbscript.id) + "_" + dbscript.script_name
        if not os.path.exists(archive_path):
            os.makedirs(archive_path)

        srcfile = os.path.join(script_path, dbscript.script_name)
        dstfile = os.path.join(archive_path, archive_file)
        if os.path.exists(srcfile):
            shutil.move(srcfile, dstfile)

        db_name = DBScript.objects.filter(id=dbscript_id).values("db_name__name").first()
        msg_user = AppOwner.objects.filter(username__username=dbscript.order_user).values("dingding").first()

        if msg_user is not None and db_name is not None and dbscript.script_name is not None:
            if msg_user["dingding"] is not None:
                dingding_msg.delay(msg_user["dingding"], \
                                   u"您的工单（编号：%s）已处理，环境：%s，数据库名：%s，脚本：%s" \
                                   % (dbscript_id, dbscript.env, db_name["db_name__name"], dbscript.script_name))

    return HttpResponseRedirect(reverse('dbscript_list'))


@login_required
@permission_verify()
def dbscript_detail(request, dbscript_id):
    try:
        if request.user.is_superuser or request.user.is_staff:
            dbscript = DBScript.objects.filter(id=dbscript_id)
        else:
            dbscript = DBScript.objects.filter(Q(id=dbscript_id) & Q(order_user=request.user.username))
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    dbscript_desc = dbscript.values("description").first()

    if dbscript_desc["description"] is None:
        dbscript = Deploy.objects.filter(dbscript__id=dbscript_id).order_by("-create_time")

    results = {                          
        'dbscript_detail': dbscript,     
    }
    return render(request, 'orders/dbscript_detail.html', results)


@login_required
@permission_verify()
def dbscript_download(request, dbscript_id):
    status = 0
    try:
        if request.user.is_superuser or request.user.is_staff:
            dbscript = DBScript.objects.get(id=dbscript_id)
        else:
            dbscript = DBScript.objects.get(Q(id=dbscript_id) & Q(order_user=request.user.username))
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    script_path = os.path.join(get_dir("script_path"), dbscript.db_name.name, dbscript.env)
    archive_path = os.path.join(script_path, "archive")
    archive_file = str(dbscript.id) + "_" + dbscript.script_name

    if dbscript.status == 1:
        file = os.path.join(archive_path, archive_file)
    elif dbscript.status == 0:
        file = os.path.join(script_path, dbscript.script_name)

    if os.path.exists(file):
        destination = open(file, 'rb')
        response = FileResponse(destination)  
        response["Content-Type"] = "application/octet-stream"
        response["Content-Disposition"] = 'attachment;filename="%s"' % dbscript.script_name.encode('utf8')  
        status = 1
        return response 
    else:
        status = 2

    return HttpResponseRedirect(reverse('dbscript_list'))
