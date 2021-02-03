#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import Q
from accounts.models import DelegateList
from accounts.forms import DelegateListForm
from appconf.models import AppOwner
from accounts.permission import permission_verify, permission_deny


@login_required
@permission_verify()
def delegate_list(request):
    all_delegate = [] 
    delegate = DelegateList.objects.all()
    for dele in delegate:
        dele_dict = {}
        dele_dict["delegate_from"] = dele.delegate_from_name 
        dele_dict["delegate_to"] = dele.delegate_to_name 
        dele_dict["id"] = dele.id 
        dele_dict["operator"] = dele.operator
        dele_dict["starttime"] = dele.starttime
        dele_dict["endtime"] = dele.endtime
        dele_dict["delegate_status"] = dele.delegate_status
        all_delegate.append(dele_dict)
    kwargs = {
        'all_delegate': all_delegate,
    }
    return render(request, 'accounts/delegate_list.html', kwargs)


@transaction.atomic
@login_required
@permission_verify()
def delegate_add(request):
    status = 0
    if request.method == 'POST':
        form = DelegateListForm(request.POST)
        if form.is_valid():
            dele_from = form.cleaned_data["delegate_from"]
            dele_to = form.cleaned_data["delegate_to"]
            starttime = form.cleaned_data["starttime"]
            endtime = form.cleaned_data["endtime"]
            if dele_from != dele_to:
                if starttime < endtime:
                    delegate_exists = DelegateList.objects.filter(Q(delegate_from_id=dele_from) & Q(delegate_to_id=dele_to))
                    if delegate_exists:
                        for dele in delegate_exists:
                            if starttime >= dele.endtime or endtime <= dele.starttime:
                                delegable = 1
                            else:
                                delegable = 0
                                break

                        if delegable == 1:
                            delegate_form = form.save(commit=False)
                            delegate_form.operator = request.user.username
                            delegate_form.delegater_dingding = delegate_exists[0].delegater_dingding
                            delegate_form.delegate_from = delegate_exists[0].delegate_from 
                            delegate_form.delegate_from_id = delegate_exists[0].delegate_from_id 
                            delegate_form.delegate_from_name = delegate_exists[0].delegate_from_name 
                            delegate_form.delegate_to = delegate_exists[0].delegate_to
                            delegate_form.delegate_to_id = delegate_exists[0].delegate_to_id 
                            delegate_form.delegate_to_name = delegate_exists[0].delegate_to_name 
                            delegate_form.save()
                            status = 1
                            return HttpResponseRedirect(reverse('delegate_list'))
                        else:
                            status = 4
                    else:
                        appowner_dfrom = AppOwner.objects.get(id=dele_from)
                        appowner_dto = AppOwner.objects.get(id=dele_to)
                        delegate_form = form.save(commit=False)
                        delegate_form.operator = request.user.username
                        delegate_form.delegater_dingding = appowner_dfrom.dingding
                        delegate_form.delegate_from = appowner_dfrom.username_id
                        delegate_form.delegate_from_id = appowner_dfrom.id
                        delegate_form.delegate_from_name = appowner_dfrom.name
                        delegate_form.delegate_to = appowner_dto.username_id
                        delegate_form.delegate_to_id = appowner_dto.id
                        delegate_form.delegate_to_name = appowner_dto.name
                        delegate_form.save()
                        status = 1
                        return HttpResponseRedirect(reverse('delegate_list'))
                else:
                    status = 2
            else:
                status = 3
    else:
        form = DelegateListForm()

    results = {
        'form': form,
        'status': status,
        'request': request,
    }
    return render(request, 'accounts/delegate_add.html', results)


@transaction.atomic
@login_required
@permission_verify()
def delegate_del(request, ids):
    if ids:
        try:
            delegate = DelegateList.objects.get(id=ids)
        except:
            return HttpResponseRedirect(reverse('permission_deny'))

        if delegate.delegate_status == 1:
            owner_dele_from = {} 
            owner_dele_from["dingding"] = delegate.delegater_dingding
            owner_dele_from["username_id"] = delegate.delegate_from 
            AppOwner.objects.filter(id=delegate.delegate_from_id).update(**owner_dele_from)

        DelegateList.objects.filter(id=ids).delete()

    return HttpResponseRedirect(reverse('delegate_list'))
