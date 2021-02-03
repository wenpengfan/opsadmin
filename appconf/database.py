#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from appconf.models import Database
from appconf.forms import DatabaseForm
from config.views import get_dir
from accounts.permission import permission_verify
import datetime
import os


@login_required
@permission_verify()
def database_list(request):
    all_database = Database.objects.all()
    results = {
        'all_database':  all_database,
    }
    return render(request, 'appconf/database_list.html', results)


@login_required
@permission_verify()
def database_del(request):
    database_id = request.GET.get('id', '')
    if database_id:
        Database.objects.filter(id=database_id).delete()

    database_id_all = str(request.POST.get('database_id_all', ''))
    if database_id_all:
        for database_id in database_id_all.split(','):
            Database.objects.filter(id=database_id).delete()

    return HttpResponseRedirect(reverse('database_list'))


@login_required
@permission_verify()
def database_add(request):
    if request.method == 'POST':
        form = DatabaseForm(request.POST)
        if form.is_valid():
            db_name = form.cleaned_data["name"]
            pro_script_path = os.path.join(get_dir("script_path"), db_name, "Pro")
            pre_script_path = os.path.join(get_dir("script_path"), db_name, "Pre")
            if not os.path.exists(pro_script_path):
                os.makedirs(pro_script_path)
            if not os.path.exists(pre_script_path):
                os.makedirs(pre_script_path)

            form.save()
            return HttpResponseRedirect(reverse('database_list'))
    else:
        form = DatabaseForm()

    results = {
        'form': form,
        'request': request,
    }
    return render(request, 'appconf/database_base.html', results)


@login_required
@permission_verify()
def database_edit(request, database_id):
    database = Database.objects.get(id=database_id)
    if request.method == 'POST':
        form = DatabaseForm(request.POST, instance=database)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('database_list'))
    else:
        form = DatabaseForm(instance=database)

    results = {
        'form': form,
        'database_id': database_id,
        'request': request,
    }
    return render(request, 'appconf/database_base.html', results)
