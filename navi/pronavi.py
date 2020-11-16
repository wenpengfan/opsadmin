#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Min
from navi.models import pro, category
from navi.forms import pro_form, category_form
from accounts.permission import permission_verify 

@login_required
@permission_verify()
def index(request):
    temp_name = "navi/navi-header.html" 
    min_gategory_id = category.objects.aggregate(Min('id'))["id__min"]
    category_id = request.GET.get('id', min_gategory_id)
    if category_id:
        all_pronavi = pro.objects.filter(category_id=category_id)
    else:
        all_pronavi = pro.objects.all()
    all_category = category.objects.all()
    env = "pro"
    return render(request, "navi/pro_index.html", locals())


@login_required
@permission_verify()
def add(request):
    temp_name = "navi/manage-header.html"
    if request.method == "POST":
        n_form = pro_form(request.POST)
        if n_form.is_valid():
            n_form.save()
            return HttpResponseRedirect(reverse('pro_manage'))
    else:
        n_form = pro_form()

    return render(request, "navi/pro_add.html", locals())


@login_required
@permission_verify()
def delete(request):
    temp_name = "navi/manage-header.html"
    navi_id = request.GET.get('id', '')
    if navi_id:
        pro.objects.filter(id=navi_id).delete()

    navi_id_all = str(request.POST.get('navi_id_all', ''))
    if navi_id_all:
        for navi_id in navi_id_all.split(','):
            pro.objects.filter(id=navi_id).delete()

    return HttpResponseRedirect(reverse('pro_manage'))


@login_required
@permission_verify()
def manage(request):
    temp_name = "navi/manage-header.html"
    allnavi = pro.objects.all()
    return render(request, "navi/pro_manage.html", locals())


@login_required
@permission_verify()
def edit(request):
    temp_name = "navi/manage-header.html"
    if request.method == 'GET':
        item = request.GET.get("id")
        pro_obj = pro.objects.get(id=item)
        category_obj = category.objects.all()
    return render(request, "navi/pro_edit.html", locals())  


@login_required
@permission_verify()
def save(request):
    temp_name = "navi/manage-header.html"
    if request.method == 'POST':
        ids = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        url = request.POST.get('url')
        category_id = request.POST.get('category')
        category_instance = category.objects.get(id=category_id)
        navi_item = pro.objects.get(id=ids)
        navi_item.name = name
        navi_item.description = desc
        navi_item.url = url
        navi_item.category = category_instance
        navi_item.save()
        status = 1
    else:
        status = 2
    allnavi = pro.objects.all()
    return render(request, "navi/pro_edit.html", locals())