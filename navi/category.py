#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from navi.models import pro, category
from navi.forms import category_form
from accounts.permission import permission_verify


@login_required
@permission_verify()
def add(request):
    status = 0
    if request.method == "POST":
        form = category_form(request.POST)
        if form.is_valid():
            form.save()
            status = 1
        else:
            status = 2
    else:
        form = category_form()

    return render(request, "navi/category_add.html", locals())

@login_required
@permission_verify()
def delete(request):
    status = 0
    category_id = request.POST.get('category_id', '')
    if category_id:
        id = int(category_id.encode('utf8')) 
        if not pro.objects.filter(category_id=id).exists():
            category.objects.filter(id=id).delete()
            status = 1
        else:
            status = 3
    else:
        status = 2

    return HttpResponse(status) 