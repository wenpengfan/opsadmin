#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from orders.models import Deploy, Document, Config
from orders.forms import DeployForm, DeployEditForm, DocumentForm
from appconf.models import Product, Project, AppOwner 
from accounts.permission import permission_verify, permission_deny
from lib.api import pages
from lib.dingding import dingding_msg
from lib.harbor import check_image_tag
import datetime
import json


@login_required
@permission_verify()
def deploy_list(request):
    deploy_status = request.GET.get('deploy_status','')
    keyword = request.GET.get('keyword','').encode('utf8')
    if keyword:
        keyword_deploy = Deploy.objects.filter(Q(app_name__name__icontains=keyword) \
                                              | Q(order_user=keyword))
    else:
        keyword_deploy = Deploy.objects.all()

    if request.user.is_superuser:
        if not deploy_status:
            all_deploy = Deploy.objects.filter(status=0) & keyword_deploy
        elif deploy_status == '-1':
            all_deploy = keyword_deploy 
        else:
            all_deploy = Deploy.objects.filter(status=deploy_status) & keyword_deploy
    else:
        username = request.user.username
        if not deploy_status:
            owner = Deploy.objects.filter(Q(app_name__product__owner__username__username=username) & Q(status=0)) & keyword_deploy
            ops = Deploy.objects.filter(Q(app_name__ops__username__username=username) & Q(status=0)) & keyword_deploy
            deploys = Deploy.objects.filter(Q(order_user=username) & Q(status=0)) & keyword_deploy
            all_deploy = owner | ops | deploys
        elif deploy_status == '-1':
            owner = Deploy.objects.filter(app_name__product__owner__username__username=username) & keyword_deploy
            ops = Deploy.objects.filter(app_name__ops__username__username=username) & keyword_deploy
            deploys = Deploy.objects.filter(order_user=username) & keyword_deploy
            all_deploy = owner | ops | deploys
        else:
            owner = Deploy.objects.filter(Q(app_name__product__owner__username__username=username) & Q(status=deploy_status)) & keyword_deploy
            ops = Deploy.objects.filter(Q(app_name__ops__username__username=username) & Q(status=deploy_status)) & keyword_deploy
            deploys = Deploy.objects.filter(Q(order_user=username) & Q(status=deploy_status)) & keyword_deploy
            all_deploy = owner | ops | deploys

    page_len = request.GET.get('page_len', '')
    deploys_list, p, deploys, page_range, current_page, show_first, show_end, end_page = pages(all_deploy, request)
    return render(request, 'orders/deploy_list.html', locals())


@login_required
@permission_verify()
def deploy_add(request):
    status = 0
    if request.method == 'POST':
        form = DeployForm(request.POST)
        if form.is_valid():
            app_name_id = form.cleaned_data["app_name"].id
            version = form.cleaned_data["version"]
            if ".Test" in version or ".Release" in version:
                status = 4
            else:
                deploy_form = form.save(commit=False)
                deploy_form.order_user = request.user.username
                if not Deploy.objects.filter(app_name_id=app_name_id).exists():
                    deploy_form.is_new = True 
                deploy_status = Deploy.objects.filter(Q(app_name_id=app_name_id) & Q(status=0))
                if deploy_status.exists(): 
                    status = 3 
                else:
                    deploy_form.save()
                    status = 1
                    return HttpResponseRedirect(reverse('deploy_doc')+"?app_name_id=%s&version=%s" % (app_name_id, version))
        else:
            status = 2 
    else:
        form = DeployForm()

    results = {
        'form': form,
        'status': status,
        'request': request,
    }
    return render(request, 'orders/deploy_base.html', results)


@login_required
@permission_verify()
def deploy_edit(request, deploy_id):
    try:
        if request.user.is_superuser or request.user.is_staff:
            deploy = Deploy.objects.get(id=deploy_id)
        else:
            deploy = Deploy.objects.get(Q(id=deploy_id) & Q(order_user=request.user.username))
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    if request.method == 'POST':
        form = DeployEditForm(request.POST, instance=deploy)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('deploy_doc')+"?app_name_id=%s&version=%s" % (deploy.app_name_id, deploy.version))
    else:
        form = DeployEditForm(instance=deploy)

    results = {
        'form': form,
        'deploy_id': deploy_id,
        'request': request,
    }
    return render(request, 'orders/deploy_base.html', results)


@login_required
@permission_verify()
def deploy_del(request):
    deploy_id = request.GET.get('id', '')
    if deploy_id:
        try:
            if request.user.is_superuser or request.user.is_staff:
                deploy = Deploy.objects.get(id=deploy_id)
                Document.objects.filter(Q(doc_id=deploy.app_name_id) & Q(next_ver=deploy.version)).delete()
                Deploy.objects.filter(id=deploy_id).delete()
            else:
                deploy = Deploy.objects.get(Q(id=deploy_id) & Q(order_user=request.user.username))
                Document.objects.filter(Q(doc_id=deploy.app_name_id) & Q(next_ver=deploy.version)).delete()
                Deploy.objects.filter(Q(id=deploy_id) & Q(order_user=request.user.username)).delete()
        except:
            return HttpResponseRedirect(reverse('permission_deny'))

    deploy_id_all = str(request.POST.get('deploy_id_all', ''))
    if deploy_id_all:
        for deploy_id in deploy_id_all.split(','):
            try:
                if request.user.is_superuser or request.user.is_staff:
                    deploy = Deploy.objects.get(id=deploy_id)
                else:
                    deploy = Deploy.objects.get(Q(id=deploy_id) & Q(order_user=request.user.username))
            except:
                return HttpResponseRedirect(reverse('permission_deny'))

            if deploy.status == 0: 
                Document.objects.filter(Q(doc_id=deploy.app_name_id) & Q(next_ver=deploy.version)).delete()
                Deploy.objects.filter(id=deploy_id).delete()

    return HttpResponseRedirect(reverse('deploy_list'))


@login_required
@permission_verify()
def deploy_finish(request, deploy_id):
    if deploy_id:
        deploy = Deploy.objects.get(id=deploy_id)

        document = Document.objects.filter(Q(doc_id=deploy.app_name_id) & Q(next_ver=deploy.version)).values().first()
        document.pop("id")
        document.pop("doc_id")
        document.pop("next_ver")
        document.pop("product_id")
        document.pop("dev_id")
        document.pop("ops_id")
        document["current_ver"] = deploy.version
        Project.objects.filter(id=deploy.app_name_id).update(**document)

        Deploy.objects.filter(id=deploy_id).update(status=1, update_time=datetime.datetime.now(),completion_time=datetime.datetime.now())

        app_name = Deploy.objects.filter(id=deploy_id).values("app_name__name").first()
        msg_user = AppOwner.objects.filter(username__username=deploy.order_user).values("dingding").first()

        if msg_user is not None and app_name is not None and deploy.version is not None:
            if msg_user["dingding"] is not None:
                dingding_msg.delay(msg_user["dingding"], u"您的工单（编号：%s）已处理，应用名：%s，版本号：%s" % (deploy_id, app_name["app_name__name"], deploy.version))

    return HttpResponseRedirect(reverse('deploy_list'))


@login_required
@permission_verify()
def deploy_detail(request, deploy_id):
    try:
        if request.user.is_superuser or request.user.is_staff:
            deploy = Deploy.objects.get(id=deploy_id)
        else:
            deploy = Deploy.objects.get(Q(id=deploy_id) & Q(order_user=request.user.username))
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    document = Project.objects.all().first()

    cur_doc = Document.objects.filter(Q(doc_id=deploy.app_name_id) & Q(next_ver=deploy.version)).values().first()
    his_doc = Project.objects.filter(id=deploy.app_name_id).values().first()

    format = lambda s: '' if s is None else s

    doc_diff = {}
    if his_doc and cur_doc:
        for key in cur_doc.keys():
            if key in his_doc.keys() and key not in ['id', 'current_ver']:
                if format(cur_doc[key]) != format(his_doc[key]):
                    name = document._meta.get_field(key).verbose_name
                    doc_diff[name] = [his_doc[key], cur_doc[key]]

    results = {
        'description': deploy.description,
        'doc_diff': doc_diff,
    }
    return render(request, 'orders/deploy_detail.html', results)


@login_required
@permission_verify()
def deploy_doc(request):
    app_name_id = request.GET.get('app_name_id', '')
    latest_ver = request.GET.get('version', '')
    try:
        if request.user.is_superuser or request.user.is_staff:
            project = Project.objects.get(id=app_name_id)
        else:
            project = Project.objects.get(Q(id=app_name_id) & Q(dev__username__username=request.user.username))
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=project)
        if form.is_valid():
            Document.objects.update_or_create(doc_id=app_name_id, \
                                              current_ver=project.current_ver, \
                                              next_ver=latest_ver, \
                                              name=project.name, \
                                              product_id=project.product_id, \
                                              dev_id=project.dev_id, \
                                              ops_id=project.ops_id, \
                                              defaults=form.cleaned_data)
            Deploy.objects.filter(Q(app_name_id=app_name_id) & Q(version=latest_ver)).update(order_status=1)

            if Deploy.objects.get(Q(app_name_id=app_name_id) & Q(version=latest_ver)).is_new == True:
                Project.objects.filter(id=app_name_id).update(language_type=form.cleaned_data["language_type"], \
                                                              app_type=form.cleaned_data["app_type"], \
                                                              code_address=form.cleaned_data["code_address"])


            deploy_id = Deploy.objects.get(Q(app_name_id=app_name_id) & Q(version=latest_ver)).id
            app_name = Project.objects.get(id=app_name_id).name 
            msg_user = Project.objects.filter(id=app_name_id).values("ops__dingding").first()
            if msg_user is not None:
                if msg_user["ops__dingding"] is not None:
                    dingding_msg.delay(msg_user["ops__dingding"], \
                                       u"您有应用更新（编号：%s）需要处理，应用名：%s，版本号：%s" \
                                       % (deploy_id, app_name, latest_ver))
                else:
                    ops_leader = Product.objects.filter(name=u"运维").values("owner__dingding").first()
                    if ops_leader is not None:
                        if ops_leader["owner__dingding"] is not None:
                            dingding_msg.delay(ops_leader["owner__dingding"], \
                                               u"有新的应用更新（编号：%s）需要分配运维，应用名：%s，版本号：%s" \
                                               % (deploy_id, app_name, latest_ver))

            return HttpResponseRedirect(reverse('deploy_list'))
    else:
        form = DocumentForm(instance=project)
        deploy_id = Deploy.objects.get(Q(app_name_id=app_name_id) & Q(version=latest_ver)).id

    results = {
        'form': form,
        'app_name_id': app_name_id,
        'version': latest_ver,
        'deploy_id': deploy_id,
        'request': request,
    }
    return render(request, 'orders/deploy_document.html', results)


@login_required
@permission_verify()
def deploy_test_status(request):
    status = {}
    deploy_id_all = str(request.POST.get('deploy_id_all', ''))
    if deploy_id_all:
        for deploy_id in deploy_id_all.split(','):
            try:
                deploy = Deploy.objects.get(id=deploy_id)
                product_name = Project.objects.get(id=deploy.app_name_id).product.codename
                repo_name = "%s/%s" % (product_name, deploy.app_name)
                tag = "%s.Release" % deploy.version
                result = check_image_tag(repo_name, tag)
                if result:
                    status[deploy_id] = 1 
                    Document.objects.filter(Q(name=deploy.app_name) & Q(next_ver=deploy.version)) \
                                    .update(next_ver=tag)
                    Deploy.objects.filter(id=deploy_id).update(version=tag, is_tested=1)
                else:
                    status[deploy_id] = 2
                    Deploy.objects.filter(id=deploy_id).update(is_tested=2)
            except:
                return HttpResponseRedirect(reverse('permission_deny'))
    return HttpResponse(json.dumps(status, ensure_ascii=False))
