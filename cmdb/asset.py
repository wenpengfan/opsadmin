#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from cmdb.connection import get_conn
from accounts.permission import permission_verify, permission_deny
from lib.api import pages


@login_required
@permission_verify()
def asset_list(request):
    keyword = request.GET.get('keyword','').encode("utf8")
    all_asset = []
    
    conn = get_conn() 
    if keyword:
        sql =  "select a.id,a.ip,a.public_ip,a.number,a.sn,a.comment,b.name \
                from assets_asset a left join orgs_organization b \
                on b.id = replace(a.org_id,'-','') \
                where a.ip like '%{0}%' \
                or a.public_ip like '%{0}%' \
                or a.number like '%{0}%' \
                or a.sn like '%{0}%' \
                or a.comment like '%{0}%' \
                order by a.ip".format(keyword)
    else:
        sql = "select a.id,a.ip,a.public_ip,a.number,a.sn,a.comment,b.name \
                from assets_asset a left join orgs_organization b \
                on b.id = replace(a.org_id,'-','') \
                order by a.ip"

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = cursor.description
    finally:
        cursor.close()
        conn.commit()
        conn.close()

    for row in results:
        asset_dict = {}
        for col in range(len(columns)):
            asset_dict[columns[col][0]] = row[col]
        all_asset.append(asset_dict)

    page_len = request.GET.get('page_len', '')
    assets_list, p, assets, page_range, current_page, show_first, show_end, end_page = pages(all_asset, request)
    return render(request, 'cmdb/asset_list.html', locals())


@login_required
@permission_verify()
def asset_detail(request, asset_id):
    all_detail = []

    conn = get_conn() 
    sql = "select hostname_raw,vendor,model,cpu_model,cpu_count,cpu_vcpus,\
            cpu_vcpus,memory,disk_total,platform,os,os_version,os_arch \
            from assets_asset where id = '%s'" % asset_id

    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        columns = cursor.description
    finally:
        cursor.close()
        conn.commit()
        conn.close()

    for row in results:
        asset_detail = {}
        for col in range(len(columns)):
            asset_detail[columns[col][0]] = row[col]
        all_detail.append(asset_detail)

    results = {
        'all_detail': all_detail 
    }

    return render(request, 'cmdb/asset_detail.html', results)

