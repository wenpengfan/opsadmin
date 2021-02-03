#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework import serializers
from appconf.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    dev_name = serializers.CharField(source='dev.name')
    ops_name = serializers.CharField(source='ops.name')

    class Meta:
        model = Project    
        fields = ("name", "current_ver", "app_type", "app_arch", "dev_name", "ops_name",)

class ProjectProductSerializer(serializers.ModelSerializer):
    product_codename = serializers.CharField(source='product.codename')

    class Meta:
        model = Project
        fields = ("product_codename",)