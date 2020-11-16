#! /usr/bin/env python
# -*- coding: utf-8 -*-

from celery.task import periodic_task 
from accounts.models import DelegateList
from appconf.models import AppOwner
from datetime import datetime


@periodic_task(run_every=300)
def delegate_start():
    delegate = DelegateList.objects.filter(delegate_status=0)
    if delegate:
        for dele in delegate:
            if dele.starttime <= datetime.now():
                owner_dele_from = {}
                owner_dele_to = AppOwner.objects.filter(username_id=dele.delegate_to).values("dingding").first()
                owner_dele_from["dingding"] = owner_dele_to["dingding"]
                owner_dele_from["username_id"] = dele.delegate_to
                AppOwner.objects.filter(id=dele.delegate_from_id).update(**owner_dele_from)

                dele.delegate_status = 1
                dele.save()


@periodic_task(run_every=300)
def delegate_stop():
    delegate = DelegateList.objects.filter(delegate_status=1) 
    if delegate:
        for dele in delegate:
            if dele.endtime <= datetime.now():
                owner_dele_from = {} 
                owner_dele_from["dingding"] = dele.delegater_dingding
                owner_dele_from["username_id"] = dele.delegate_from 
                AppOwner.objects.filter(id=dele.delegate_from_id).update(**owner_dele_from)
                
                DelegateList.objects.filter(id=dele.id).delete()
