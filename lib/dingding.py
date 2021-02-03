#! /usr/bin/env python
# -*- coding: utf-8 -*-

from celery import shared_task
from config.views import get_dir
import urllib
import urllib2
import json
import time


def dingding_token():
    corpid = get_dir("dingding_corpid")
    corpsecret = get_dir("dingding_corpsecret")
    url = 'https://oapi.dingtalk.com/gettoken?corpid=%s&corpsecret=%s'
    page = urllib.urlopen(url % (corpid, corpsecret))
    str = page.read()
    dict = json.loads(str)
    token = dict["access_token"]
    return token


@shared_task
def dingding_msg(uid, text):
    json_content = {
                    "touser"  : uid,
                    "agentid" : "249216975",
                    "msgtype" : "text",
                    "text"    : {
                    "content" : text
                                }
                   }
    jdata = json.dumps(json_content)
    access_token = dingding_token()
    url = 'https://oapi.dingtalk.com/message/send?access_token=%s' % access_token
    req = urllib2.Request(url, jdata)
    req.add_header('content-type', 'application/json')
    response = urllib2.urlopen(req)
    return response.read()
