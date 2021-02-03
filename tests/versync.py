#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import datetime
import json

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from accounts.permission import permission_verify
from appconf.models import Product
from tests.models import Versync, Apply, VersyncDetail
from lib.api import pages

@login_required
@permission_verify()
def versync_list(request):
    product_id = int(request.GET.get('product_id', 0))
    all_product = Product.objects.filter(qa_id__isnull=False)
    if product_id != 0:
        all_versync = Versync.objects.filter(product_id=product_id)
    else:
        all_versync = Versync.objects.all()
    page_len = request.GET.get('page_len', '')
    versyncs_list, p, versyncs, page_range, current_page, show_first, show_end, end_page = pages(all_versync, request)
    return render(request, 'tests/versync_list.html', locals())


@login_required
@permission_verify()
def version_sync(request):
    status = 0
    product_id = int(request.POST.get('product_id', 0))
    versync = Versync.objects.filter(Q(product_id=product_id) & Q(sync_status__in=[0, 1, 2]))
    if product_id != 0 and not versync.exists():
        if Apply.objects.filter(Q(product_id=product_id) & Q(status=1) & Q(feedback=0)).exists():
            status = 3
        else:
            Versync.objects.create(product_id=product_id,
                                   submittime=datetime.datetime.now(),
                                   progress=0,
                                   sync_status=0,)
            status = 1
    else:
        status = 2
    return HttpResponse(status)


@login_required
@permission_verify()
def sync_progress(request):
    progress = {}
    versync_id_all = str(request.POST.get('versync_id_all', ''))
    if versync_id_all:
        for versync_id in versync_id_all.split(','):
            try:
                versync = Versync.objects.get(id=versync_id)
                progress[versync_id] = "%s;%s;%s;%s" % (versync.progress,
                                                        versync.sync_status,
                                                        versync.starttime,
                                                        versync.endtime)
            except:
                return HttpResponseRedirect(reverse('permission_deny'))
    return HttpResponse(json.dumps(progress, ensure_ascii=False))


@login_required
@permission_verify()
def versync_del(request):
    status = 0
    versync_id = int(request.GET.get('id', 0))
    if id != 0:
        try:
            versync = Versync.objects.get(id=versync_id)
            if versync.sync_status == 3 or versync.sync_status == 4:
                VersyncDetail.objects.filter(versync=versync).delete()
                versync.delete()
                status = 1
            else:
                status = 2
        except:
            status = 3
    else:
        return HttpResponseRedirect(reverse('permission_deny'))

    product_id = int(request.GET.get('product_id', 0))
    all_product = Product.objects.filter(qa_id__isnull=False)
    if product_id != 0:
        all_versync = Versync.objects.filter(product_id=product_id)
    else:
        all_versync = Versync.objects.all()
    page_len = request.GET.get('page_len', '')
    versync_list, p, versyncs, page_range, current_page, show_first, show_end, end_page = pages(all_versync, request)
    return render(request, 'tests/versync_list.html', locals())
