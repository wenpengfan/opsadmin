#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config.views import get_dir
import MySQLdb

def get_conn():
    host = get_dir("cmdb_host") 
    port = int(get_dir("cmdb_port"))
    username = get_dir("cmdb_user") 
    password = get_dir("cmdb_password") 
    database = get_dir("cmdb_database") 

    conn = MySQLdb.connect(host=host, port=port, user=username, passwd=password, db=database, charset='utf8')

    return conn
    
