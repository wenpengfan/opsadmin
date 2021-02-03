#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from appconf.models import Project, AppOwner
from appconf.forms import ProjectForm, ProjectMiniForm 
from orders.models import Deploy
from lib.api import unicode2gb
from lib.dingding import dingding_msg
from accounts.permission import permission_verify
import csv
import datetime


@login_required
@permission_verify()
def project_list(request):
    all_project = Project.objects.filter(is_offline=False)
    results = {
        'all_project': all_project,
    }
    return render(request, 'appconf/project_list.html', results)


@login_required
@permission_verify()
def project_del(request):
    status = 0
    project_id = request.GET.get('id', '')
    all_project = Project.objects.filter(is_offline=False)
    if project_id:
        app_name = Project.objects.get(id=project_id).name
        if Deploy.objects.filter(app_name_id=project_id):
            status = 2
        else:
            Project.objects.filter(id=project_id).delete()
            status = 1

    project_id_all = str(request.POST.get('project_id_all', ''))
    if project_id_all:
        for project_id in project_id_all.split(','):
            app_name = Project.objects.get(id=project_id).name
            if Deploy.objects.filter(app_name_id=project_id):
                status = 2
                break
            else:
                Project.objects.filter(id=project_id).delete()
                status = 1

    results = {
        'all_project': all_project,
        'status': status,
        'app_name': app_name,
    }
    return render(request, 'appconf/project_list.html', results)


@login_required
@permission_verify()
def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project_list'))
    else:
        form = ProjectForm()

    results = {
        'form': form,
        'request': request,
    }
    return render(request, 'appconf/project_base.html', results)


@login_required
@permission_verify()
def project_add_mini(request):
    status = 0
    app_name_id = 0
    if request.method == 'POST':
        form = ProjectMiniForm(request.POST)
        if form.is_valid():
            pmini_form = form.save(commit=False)
            pmini_form.dev = AppOwner.objects.get(username__username=request.user.username)
            pmini_form.save()
            status = 1
            app_name = request.POST.get('name', '')
            app_name_id = Project.objects.get(name=app_name).id
        else:
            status = 2
    else:
        form = ProjectMiniForm()

    results = {
        'form': form,
        'request': request,
        'status': status,
        'app_name_id': app_name_id,
        'app_name': request.POST.get('name', ''),
    }
    return render(request, 'appconf/project_add_mini.html', results)


@login_required
@permission_verify()
def project_edit(request, project_id):
    project = Project.objects.get(id=project_id)
    ops_id = project.ops_id
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            priv_ops_id = ops_id
            if form.cleaned_data["ops"] is not None:
                cur_ops_id = form.cleaned_data["ops"].id
            else:
                cur_ops_id = None
            form.save()

            if priv_ops_id != cur_ops_id:
                msg_user = AppOwner.objects.filter(id=cur_ops_id).values("dingding").first()
                deploy = Deploy.objects.filter(Q(app_name_id=project_id) & Q(status=0))
                for d in deploy:
                    if msg_user is not None:
                        if msg_user["dingding"] is not None:
                            dingding_msg.delay(msg_user["dingding"], \
                                               u"您有应用更新（编号：%s）需要处理，应用名：%s，版本号：%s" \
                                               % (d.id, d.app_name, d.version))

            return HttpResponseRedirect(reverse('project_list'))
    else:
        form = ProjectForm(instance=project)

    results = {
        'form': form,
        'project_id': project_id,
        'request': request,
    }
    return render(request, 'appconf/project_base.html', results)


@login_required
@permission_verify()
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)

    results = {
        'project_detail': project
    }
    return render(request, 'appconf/project_detail.html', results)


@login_required
@permission_verify()
def project_export(request):
    export = request.GET.get("export", '')
    project_id_list = request.GET.getlist("g_check", '')
    if export == "part":
        if project_id_list:
            project_find = []
            for project_id in project_id_list:
                project_item = Project.objects.get(id=project_id)
                if project_item:
                    project_find.append(project_item)

    if export == "all":
        project_find = Project.objects.all()

    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
    file_name = 'opsadmin_project_' + now + '.csv'
    response['Content-Disposition'] = "attachment; filename=" + file_name
    writer = csv.writer(response)
    writer.writerow([unicode2gb(u'应用名称'), unicode2gb(u'应用描述'), unicode2gb(u'当前版本'), unicode2gb(u'语言类型'),
                     unicode2gb(u'程序类型'), unicode2gb(u'程序框架'), unicode2gb(u'代码库地址'), unicode2gb(u'启动命令'),
                     unicode2gb(u'停止命令'), unicode2gb(u'配置文件说明'), unicode2gb(u'Docker容器说明'), unicode2gb(u'需要的业务监控项'),
                     unicode2gb(u'高可用说明'), unicode2gb(u'需要新增域名'), unicode2gb(u'需要新增二级目录'),
                     unicode2gb(u'URI映射来源'), unicode2gb(u'URI映射目标'), unicode2gb(u'是否需要访问外网'),
                     unicode2gb(u'调用方'), unicode2gb(u'应用依赖的其他需求'), unicode2gb(u'所属产品线'),
                     unicode2gb(u'开发负责人'), unicode2gb(u'运维负责人')])
    for p in project_find:
        writer.writerow([unicode2gb(p.name), unicode2gb(p.description), unicode2gb(p.current_ver), unicode2gb(p.language_type),
                        unicode2gb(p.app_type), unicode2gb(p.app_arch), unicode2gb(p.code_address), unicode2gb(p.start_cmd),
                        unicode2gb(p.stop_cmd), unicode2gb(p.config_detail), unicode2gb(p.docker_expose), unicode2gb(p.app_monitor),
                        unicode2gb(p.need_ha), unicode2gb(p.need_dn), unicode2gb(p.need_location),
                        unicode2gb(p.uri_mapping_from), unicode2gb(p.uri_mapping_to), unicode2gb(p.need_wan),
                        unicode2gb(p.requester), unicode2gb(p.rely_on), unicode2gb(p.product.name),
                        unicode2gb(p.dev.name), unicode2gb(p.ops.name)])
    return response


@login_required
@permission_verify()
def project_offline(request):
    project_id = request.GET.get('id', '')
    if project_id:
        Project.objects.filter(id=project_id).update(is_offline=True)

        app_name = Project.objects.get(id=project_id).name
        msg_user = Project.objects.filter(id=project_id).values("ops__dingding").first()
        username = request.user.username

        if msg_user is not None:
            if msg_user["ops__dingding"] is not None:
                dingding_msg.delay(msg_user["ops__dingding"], \
                                   u"应用已下架，应用名：%s，操作者：%s" % (app_name, username))

    return HttpResponseRedirect(reverse('project_list'))
