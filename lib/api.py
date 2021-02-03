#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.decorators.csrf import csrf_exempt
from lib.log import log
from config.views import get_dir
import logging
try:
    import json
except ImportError:
    import simplejson as json


def unicode2gb(args):
    """
    :参数 args:
    :返回: GB18030编码
    """
    if isinstance(args, unicode):
#        return args.encode('gb2312')
        return args.encode('gb18030')
    else:
        return args 


def page_list_return(total, current=1):
    """
    page
    分页，返回本次分页的最小页数到最大页数列表
    """
    min_page = current - 4 if current - 6 > 0 else 1
    max_page = min_page + 6 if min_page + 6 < total else total

    return range(min_page, max_page + 1)


def pages(post_objects, request):
    """
    page public function , return page's object tuple
    分页公用函数，返回分页的对象元组
    """

    page_len = request.GET.get('page_len', '')
    if not page_len:
        page_len = 10
    paginator = Paginator(post_objects, page_len)
    try:
        current_page = int(request.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(paginator.page_range), current_page)
    end_page = len(paginator.page_range)

    try:
        page_objects = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        page_objects = paginator.page(paginator.num_pages)

    show_first = 0
    show_end = 0

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end, end_page
