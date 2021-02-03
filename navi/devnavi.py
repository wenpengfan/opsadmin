#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from navi.models import dev 
from navi.forms import dev_form
from accounts.permission import permission_verify

@login_required
@permission_verify()
def index(request):
    temp_name = "navi/navi-header.html"
    all_devnavi = dev.objects.all()
    return render(request, "navi/dev_index.html", locals())


@login_required
@permission_verify()
def add(request):
    temp_name = "navi/manage-header.html"
    if request.method == "POST":
        n_form = dev_form(request.POST)
        if n_form.is_valid():
            n_form.save()
            return HttpResponseRedirect(reverse('dev_manage'))
    else:
        n_form = dev_form()

    return render(request, "navi/dev_add.html", locals())


@login_required
@permission_verify()
def delete(request):
    temp_name = "navi/manage-header.html"
    navi_id = request.GET.get('id', '')
    if navi_id:
        dev.objects.filter(id=navi_id).delete()

    navi_id_all = str(request.POST.get('navi_id_all', ''))
    if navi_id_all:
        for navi_id in navi_id_all.split(','):
            dev.objects.filter(id=navi_id).delete()

    return HttpResponseRedirect(reverse('dev_manage'))


@login_required
@permission_verify()
def manage(request):
    temp_name = "navi/manage-header.html"
    allnavi = dev.objects.all()
    return render(request, "navi/dev_manage.html", locals())


@login_required
@permission_verify()
def edit(request):
    temp_name = "navi/manage-header.html"
    if request.method == 'GET':
        item = request.GET.get("id")
        obj = dev.objects.get(id=item)
    return render(request, "navi/dev_edit.html", locals())


@login_required
@permission_verify()
def save(request):
    temp_name = "navi/manage-header.html"
    if request.method == 'POST':
        ids = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        url = request.POST.get('url')
        navi_item = dev.objects.get(id=ids)
        navi_item.name = name
        navi_item.description = desc
        navi_item.url = url
        navi_item.save()
        status = 1
    else:
        status = 2
    allnavi = dev.objects.all()
    return render(request, "navi/dev_edit.html", locals())
