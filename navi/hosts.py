#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from navi.models import hosts
from accounts.permission import permission_verify


@login_required
@permission_verify()
def index(request):
    hosts_order = request.GET.get('hosts_order', 'ip')
    all_hosts = hosts.objects.all().order_by(hosts_order)

    results = {
        'all_hosts': all_hosts,
        'hosts_order': hosts_order
    }
    return render(request, "navi/hosts_index.html", results)
