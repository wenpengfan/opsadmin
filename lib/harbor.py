#! /usr/bin/env python
# -*- coding: utf-8 -*-

from celery import shared_task
from config.views import get_dir
import requests
import json


def fetch_repos_id(proj_name):
    harbor_domain = get_dir("harbor_domain")
    username = get_dir("harbor_username")
    password = get_dir("harbor_password")
    proj_url = "%s/api/projects" % harbor_domain 
    proj_info = requests.get(proj_url, auth=(username, password)).json()
    for info in proj_info:
        if info["name"] == proj_name:
            return info["project_id"] 

        
def fetch_latest_tag(proj_name):
    latest_tag_dict = {}
    harbor_domain = get_dir("harbor_domain")
    username = get_dir("harbor_username")
    password = get_dir("harbor_password")
    repos_url = "%s/api/repositories" % harbor_domain 
    repos_id = fetch_repos_id(proj_name)
    all_repos = requests.get(repos_url, auth=(username, password), params={"project_id": repos_id}).json()
    for repo in all_repos:
        tag_url = "%s/%s/tags" %(repos_url, repo["name"])
        all_tags = requests.get(tag_url, auth=(username, password)).json()
        tags_sort = sorted(all_tags, key=lambda a: a["created"])
        for tag in tags_sort[::-1]:
            if '.Test' in tag["name"] or '.Release' in tag["name"]:
                tags_sort.remove(tag)
        latest_tag = tags_sort[-1]
        latest_tag_dict[repo["name"]] = latest_tag["name"]
    return latest_tag_dict


def retag_image_test(repo_name, tag):
    harbor_domain = get_dir("harbor_domain")
    username = get_dir("harbor_username")
    password = get_dir("harbor_password")
    tags_url = "%s/api/repositories/%s/tags" % (harbor_domain, repo_name) 
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    if tag.split('.')[-1] == "Test":
        body = json.dumps({"tag": tag, "src_image": "%s:%s" % (repo_name, tag), "override": True})
    else:
        body = json.dumps({"tag": "%s.Test" % tag, "src_image": "%s:%s" % (repo_name, tag), "override": True})
    response = requests.post(tags_url, data=body, auth=(username, password), headers=headers)
    if response.status_code == 200:
        result = True 
    else:
        result = False 
    return result 


@shared_task
def retag_image_release(repo_name, tag):
    harbor_domain = get_dir("harbor_domain")
    username = get_dir("harbor_username")
    password = get_dir("harbor_password")
    tags_url = "%s/api/repositories/%s/tags" % (harbor_domain, repo_name) 
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    if tag.split('.')[-1] == "Release":
        body = json.dumps({"tag": tag, "src_image": "%s:%s" % (repo_name, tag), "override": False})
    else:
        body = json.dumps({"tag": tag.replace('Test', 'Release'), "src_image": "%s:%s" % (repo_name, tag), "override": False})
    response = requests.post(tags_url, data=body, auth=(username, password), headers=headers)
    if response.status_code == 200:
        result = True 
    else:
        result = False 
    return result 

def check_image_tag(repo_name, tag):
    harbor_domain = get_dir("harbor_domain")
    username = get_dir("harbor_username")
    password = get_dir("harbor_password")
    tags_url = "%s/api/repositories/%s/tags/%s" % (harbor_domain, repo_name, tag) 
    response = requests.get(tags_url, auth=(username, password))
    if response.status_code == 200:
        result = True 
    else:
        result = False 
    return result 
