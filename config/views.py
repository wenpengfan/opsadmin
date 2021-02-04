#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse
try:
    import ConfigParser as cp
except Exception as msg:
    print(msg)
    import ConfigParser as cp
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from accounts.permission import permission_verify
from lib.log import dic
import os


@login_required
@permission_verify()
def index(request):
    temp_name = "config/config-header.html"
    display_control = "none"
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = cp.RawConfigParser()
    all_level = dic
    all_filter = ("OpenLDAP", "WindowsAD")
    ldap_choice = ("True", "False")
    with open(dirs+'/opsadmin.conf', 'r') as cfgfile:
        config.readfp(cfgfile)
        engine = config.get('db', 'engine')
        host = config.get('db', 'host')
        port = config.get('db', 'port')
        user = config.get('db', 'user')
        password = config.get('db', 'password')
        database = config.get('db', 'database')
        redis_host = config.get('redis', 'redis_host')
        redis_port = config.get('redis', 'redis_port')
        redis_db = config.get('redis', 'redis_db')
        redis_password = config.get('redis', 'redis_password')
        log_path = config.get('log', 'log_path')
        log_level = config.get('log', 'log_level')
        script_path = config.get('script', 'script_path')
        ldap_enable = config.get('ldap', 'ldap_enable')
        ldap_server = config.get('ldap', 'ldap_server')
        ldap_port = config.get('ldap', 'ldap_port')
        base_dn = config.get('ldap', 'base_dn')
        ldap_manager = config.get('ldap', 'ldap_manager')
        ldap_password = config.get('ldap', 'ldap_password')
        ldap_filter = config.get('ldap', 'ldap_filter')
        require_group = config.get('ldap', 'require_group')
        nickname = config.get('ldap', 'nickname')
        is_active = config.get('ldap', 'is_active')
        is_superuser = config.get('ldap', 'is_superuser')
        cmdb_host = config.get('cmdb', 'cmdb_host')
        cmdb_port = config.get('cmdb', 'cmdb_port')
        cmdb_user = config.get('cmdb', 'cmdb_user')
        cmdb_password = config.get('cmdb', 'cmdb_password')
        cmdb_database = config.get('cmdb', 'cmdb_database')
        dingding_corpid = config.get('dingding', 'dingding_corpid')
        dingding_corpsecret = config.get('dingding', 'dingding_corpsecret')
        semaphore_domain = config.get('semaphore', 'semaphore_domain')
        semaphore_username = config.get('semaphore', 'semaphore_username')
        semaphore_password = config.get('semaphore', 'semaphore_password')
        harbor_domain = config.get('harbor', 'harbor_domain')
        harbor_username = config.get('harbor', 'harbor_username')
        harbor_password = config.get('harbor', 'harbor_password')
    return render(request, 'config/index.html', locals())


@login_required
@permission_verify()
def config_save(request):
    temp_name = "config/config-header.html"
    if request.method == 'POST':
        # db
        engine = request.POST.get('engine')
        host = request.POST.get('host')
        port = request.POST.get('port')
        user = request.POST.get('user')
        password = request.POST.get('password')
        database = request.POST.get('database')
        # redis 
        redis_host = request.POST.get('redis_host')
        redis_port = request.POST.get('redis_port')
        redis_db = request.POST.get('redis_db')
        redis_password = request.POST.get('redis_password')
        # log
        log_path = request.POST.get('log_path')
        log_level = request.POST.get('log_level')
        # script 
        script_path = request.POST.get('script_path')
        # ldap
        ldap_enable = request.POST.get('ldap_enable')
        ldap_server = request.POST.get('ldap_server')
        ldap_port = request.POST.get('ldap_port')
        base_dn = request.POST.get('base_dn')
        ldap_manager = request.POST.get('ldap_manager')
        ldap_password = request.POST.get('ldap_password')
        ldap_filter = request.POST.get('ldap_filter')
        require_group = request.POST.get('require_group')
        nickname = request.POST.get('nickname')
        is_active = request.POST.get('is_active')
        is_superuser = request.POST.get('is_superuser')
        # cmdb
        cmdb_host = request.POST.get('cmdb_host')
        cmdb_port = request.POST.get('cmdb_port')
        cmdb_user = request.POST.get('cmdb_user')
        cmdb_password = request.POST.get('cmdb_password')
        cmdb_database = request.POST.get('cmdb_database')
        # dingding
        dingding_corpid = request.POST.get('dingding_corpid')
        dingding_corpsecret = request.POST.get('dingding_corpsecret')
        # semaphore
        semaphore_domain = request.POST.get('semaphore_domain')
        semaphore_username = request.POST.get('semaphore_username')
        semaphore_password = request.POST.get('semaphore_password')
        # harbor
        harbor_domain = request.POST.get('harbor_domain')
        harbor_username = request.POST.get('harbor_username')
        harbor_password = request.POST.get('harbor_password')
        
        config = cp.RawConfigParser()
        dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config.add_section('db')
        config.set('db', 'engine', engine)
        config.set('db', 'host', host)
        config.set('db', 'port', port)
        config.set('db', 'user', user)
        config.set('db', 'password', password)
        config.set('db', 'database', database)
        config.add_section('redis')
        config.set('redis', 'redis_host', redis_host)
        config.set('redis', 'redis_port', redis_port)
        config.set('redis', 'redis_db', redis_db)
        config.set('redis', 'redis_password', redis_password)
        config.add_section('log')
        config.set('log', 'log_path', log_path)
        config.set('log', 'log_level', log_level)
        config.add_section('script')
        config.set('script', 'script_path', script_path)
        config.add_section('ldap')
        config.set('ldap', 'ldap_enable', ldap_enable)
        config.set('ldap', 'ldap_server', ldap_server)
        config.set('ldap', 'ldap_port', ldap_port)
        config.set('ldap', 'base_dn', base_dn)
        config.set('ldap', 'ldap_manager', ldap_manager)
        config.set('ldap', 'ldap_password', ldap_password)
        config.set('ldap', 'ldap_filter', ldap_filter)
        config.set('ldap', 'require_group', require_group)
        config.set('ldap', 'nickname', nickname)
        config.set('ldap', 'is_active', is_active)
        config.set('ldap', 'is_superuser', is_superuser)
        config.add_section('cmdb')
        config.set('cmdb', 'cmdb_host', cmdb_host)
        config.set('cmdb', 'cmdb_port', cmdb_port)
        config.set('cmdb', 'cmdb_user', cmdb_user)
        config.set('cmdb', 'cmdb_password', cmdb_password)
        config.set('cmdb', 'cmdb_database', cmdb_database)
        config.add_section('dingding')
        config.set('dingding', 'dingding_corpid', dingding_corpid)
        config.set('dingding', 'dingding_corpsecret', dingding_corpsecret)
        config.add_section('semaphore')
        config.set('semaphore', 'semaphore_domain', semaphore_domain)
        config.set('semaphore', 'semaphore_username', semaphore_username)
        config.set('semaphore', 'semaphore_password', semaphore_password)
        config.add_section('harbor')
        config.set('harbor', 'harbor_domain', harbor_domain)
        config.set('harbor', 'harbor_username', harbor_username)
        config.set('harbor', 'harbor_password', harbor_password)
        tips = u"保存成功！"
        display_control = ""
        with open(dirs+'/opsadmin.conf', 'wb') as cfgfile:
            config.write(cfgfile)
        with open(dirs+'/opsadmin.conf', 'r') as cfgfile:
            config.readfp(cfgfile)
            engine = config.get('db', 'engine')
            host = config.get('db', 'host')
            port = config.get('db', 'port')
            user = config.get('db', 'user')
            password = config.get('db', 'password')
            database = config.get('db', 'database')
            log_path = config.get('redis', 'redis_host')
            log_path = config.get('redis', 'redis_port')
            log_path = config.get('redis', 'redis_db')
            log_path = config.get('redis', 'redis_password')
            log_path = config.get('log', 'log_path')
            script_path = config.get('script', 'script_path')
            ldap_enable = config.get('ldap', 'ldap_enable')
            ldap_server = config.get('ldap', 'ldap_server')
            ldap_port = config.get('ldap', 'ldap_port')
            base_dn = config.get('ldap', 'base_dn')
            ldap_manager = config.get('ldap', 'ldap_manager')
            ldap_password = config.get('ldap', 'ldap_password')
            ldap_filter = config.get('ldap', 'ldap_filter')
            require_group = config.get('ldap', 'require_group')
            nickname = config.get('ldap', 'nickname')
            is_active = config.get('ldap', 'is_active')
            is_superuser = config.get('ldap', 'is_superuser')
            cmdb_host = config.get('cmdb', 'cmdb_host')
            cmdb_port = config.get('cmdb', 'cmdb_port')
            cmdb_user = config.get('cmdb', 'cmdb_user')
            cmdb_password = config.get('cmdb', 'cmdb_password')
            cmdb_database = config.get('cmdb', 'cmdb_database')
            dingding_corpid = config.get('dingding', 'dingding_corpid')
            dingding_corpsecret = config.get('dingding', 'dingding_corpsecret')
            semaphore_domain = config.get('semaphore', 'semaphore_domain')
            semaphore_username = config.get('semaphore', 'semaphore_username')
            semaphore_password = config.get('semaphore', 'semaphore_password')
            harbor_domain = config.get('harbor', 'harbor_domain')
            harbor_username = config.get('harbor', 'harbor_username')
            harbor_password = config.get('harbor', 'harbor_password')
    else:
        display_control = "none"
    return render(request, 'config/index.html', locals())


def get_dir(args):
    config = cp.RawConfigParser()
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(dirs+'/opsadmin.conf', 'r') as cfgfile:
        config.readfp(cfgfile)
        log_path = config.get('log', 'log_path')
        log_level = config.get('log', 'log_level')
        script_path = config.get('script', 'script_path')
        ldap_enable = config.get('ldap', 'ldap_enable')
        ldap_server = config.get('ldap', 'ldap_server')
        ldap_port = config.get('ldap', 'ldap_port')
        base_dn = config.get('ldap', 'base_dn')
        ldap_manager = config.get('ldap', 'ldap_manager')
        ldap_password = config.get('ldap', 'ldap_password')
        ldap_filter = config.get('ldap', 'ldap_filter')
        require_group = config.get('ldap', 'require_group')
        nickname = config.get('ldap', 'nickname')
        is_active = config.get('ldap', 'is_active')
        is_superuser = config.get('ldap', 'is_superuser')
        cmdb_host = config.get('cmdb', 'cmdb_host')
        cmdb_port = config.get('cmdb', 'cmdb_port')
        cmdb_user = config.get('cmdb', 'cmdb_user')
        cmdb_password = config.get('cmdb', 'cmdb_password')
        cmdb_database = config.get('cmdb', 'cmdb_database')
        dingding_corpid = config.get('dingding', 'dingding_corpid')
        dingding_corpsecret = config.get('dingding', 'dingding_corpsecret')
        semaphore_domain = config.get('semaphore', 'semaphore_domain')
        semaphore_username = config.get('semaphore', 'semaphore_username')
        semaphore_password = config.get('semaphore', 'semaphore_password')
        harbor_domain = config.get('harbor', 'harbor_domain')
        harbor_username = config.get('harbor', 'harbor_username')
        harbor_password = config.get('harbor', 'harbor_password')
    # 根据传入参数返回变量以获取配置，返回变量名与参数名相同
    if args:
        return vars()[args]
    else:
        return HttpResponse(status=403)

