#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import datetime

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from accounts.permission import permission_verify, permission_deny
from appconf.models import Product, Project, AppOwner
from tests.models import Apply, Environment
from tests.forms import ApplyForm, ApplyFinishForm
from lib.api import pages
from lib.dingding import dingding_msg
from lib.harbor import retag_image_release


@login_required
@permission_verify()
def apply_list(request):
    apply_status = request.GET.get('apply_status', '-1')
    if apply_status == '-1':
        all_apply = Apply.objects.all()
    else:
        all_apply = Apply.objects.filter(status=apply_status)
    page_len = request.GET.get('page_len', '')
    apply_list, p, applys, page_range, current_page, show_first, show_end, end_page = pages(all_apply, request)
    return render(request, 'tests/apply_list.html', locals())

@login_required
@permission_verify()
def apply_add(request):
    status = 0
    if request.method == 'POST':
        form = ApplyForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data["product"]
            if Apply.objects.filter(Q(product=product) & Q(feedback=0)).exists():
                status = 3
            else:
                msg_user = Product.objects.filter(id=product.id).values("qa__dingding").first()
                db_form = form.save(commit=False)
                db_form.order_user = request.user.username
                db_form.save()
                apply_id = db_form.id

                if msg_user is not None:
                    if msg_user["qa__dingding"] is not None:
                        dingding_msg.delay(msg_user["qa__dingding"], u"您有新的测试需求（编号：%s）需要处理，产品线：%s" % (apply_id, product))
                status = 1
        else:
            status = 2
    else:
        form = ApplyForm()

    results = {
        'form': form,
        'request': request,
        'status': status,
    }
    return render(request, 'tests/apply_base.html', results)


@login_required
@permission_verify()
def apply_del(request):
    apply_id = int(request.GET.get('id', 0))
    try:
        Apply.objects.filter(id=apply_id).delete()
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    apply_status = request.GET.get('apply_status', '-1')
    if apply_status == '-1':
        all_apply = Apply.objects.all()
    else:
        all_apply = Apply.objects.filter(status=apply_status)
    page_len = request.GET.get('page_len', '')
    apply_list, p, applys, page_range, current_page, show_first, show_end, end_page = pages(all_apply, request)
    return render(request, 'tests/apply_list.html', locals())


@login_required
@permission_verify()
def apply_edit(request):
    status = 0
    apply_id = int(request.GET.get('id', 0))
    try:
        apply = Apply.objects.get(id=apply_id)
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    if request.method == 'POST':
        form = ApplyForm(request.POST, instance=apply)
        if form.is_valid():
            db_form = form.save(commit=False)
            db_form.order_user = request.user.username
            db_form.save()
            status = 1
        else:
            status = 2
    else:
        form = ApplyForm(instance=apply)

    results = {
        'form': form,
        'request': request,
        'status': status,
    }
    return render(request, 'tests/apply_base.html', results)


@login_required
@permission_verify()
def apply_finish(request):
    status = 0
    apply_id = int(request.GET.get('id', 0))
    try:
        apply = Apply.objects.get(id=apply_id)
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    if request.method == 'POST':
        form = ApplyFinishForm(request.POST, instance=apply)
        if form.is_valid():
            report_addr = form.cleaned_data["report_address"]
            db_form = form.save(commit=False)
            db_form.report_file = report_addr.split('/')[-1]
            db_form.status = True
            db_form.finishtime = datetime.datetime.now()
            db_form.save()
            product_name = apply.product.name
            msg_user = AppOwner.objects.filter(username__username=apply.order_user).values("dingding").first()
            if msg_user is not None and product_name is not None:
                if msg_user["dingding"] is not None:
                    dingding_msg.delay(msg_user["dingding"], u"您的测试需求（编号：%s）已完成，产品线：%s，请及时确认是否上线！" % (apply_id, product_name))
            status = 1
        else:
            status = 2
    else:
        form = ApplyFinishForm(instance=apply)

    results = {
        'form': form,
        'request': request,
        'status': status,
        'apply_id': apply_id,
    }
    return render(request, 'tests/apply_finish.html', results)


@login_required
@permission_verify()
def apply_detail(request, apply_id):
    try:
        apply = Apply.objects.get(id=apply_id)
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    results = {
        'apply': apply,
    }
    return render(request, 'tests/apply_detail.html', results)


@login_required
@permission_verify()
def apply_agree(request):
    apply_id = int(request.GET.get('id', 0))
    try:
        apply = Apply.objects.filter(Q(id=apply_id) & Q(status=True) & Q(order_user=request.user.username))
        if apply:
            apply.update(feedback=1)
            product = apply.first().product
            all_project = Project.objects.filter(product=product)
            for project in all_project:
                env = Environment.objects.filter(Q(project=project) & Q(is_enable=True)).first()
                if env:
                    repo_name = "%s/%s" % (product.codename, project.name)
                    tag = "%s.Test" % (env.test_ver)
                    retag_image_release.delay(repo_name, tag)
        else:
            return HttpResponseRedirect(reverse('permission_deny'))
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    apply_status = request.GET.get('apply_status', '-1')
    if apply_status == '-1':
        all_apply = Apply.objects.all()
    else:
        all_apply = Apply.objects.filter(status=apply_status)
    page_len = request.GET.get('page_len', '')
    apply_list, p, applys, page_range, current_page, show_first, show_end, end_page = pages(all_apply, request)
    return render(request, 'tests/apply_list.html', locals())


@login_required
@permission_verify()
def apply_reject(request):
    apply_id = int(request.GET.get('id', 0))
    try:
        Apply.objects.filter(Q(id=apply_id) & Q(status=True) & Q(order_user=request.user.username)) \
                     .update(feedback=2)
    except:
        return HttpResponseRedirect(reverse('permission_deny'))

    apply_status = request.GET.get('apply_status', '-1')
    if apply_status == '-1':
        all_apply = Apply.objects.all()
    else:
        all_apply = Apply.objects.filter(status=apply_status)
    page_len = request.GET.get('page_len', '')
    apply_list, p, applys, page_range, current_page, show_first, show_end, end_page = pages(all_apply, request)
    return render(request, 'tests/apply_list.html', locals())
