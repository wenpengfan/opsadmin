#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify, permission_deny
from lib.dingding import dingding_msg


@login_required
@permission_verify()
def delay_list(request):
    text = '正在建设'
    return render(request, 'workload/delay_list.html', locals())
