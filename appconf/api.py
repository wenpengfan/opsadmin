#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from appconf.models import Project
from appconf.serializer import ProjectSerializer, ProjectProductSerializer


class api_project_list(APIView):

    def get(self, request, format=None):
        type = request.GET.get('type', '')
        product = request.GET.get('product', '')
        if type and product:
            project = Project.objects.filter(Q(language_type=type) \
                                             & Q(product__codename=product) \
                                             & Q(is_offline=False))
        else:
            project = {} 
            
        project_serializer = ProjectSerializer(project, many=True)
        return Response(project_serializer.data)

class api_project_product(APIView):

    def get(self, request, format=None):
        proj_name = request.GET.get('name', '')
        if type:
            project = Project.objects.filter(name=proj_name)
        else:
            project = {}
        proj_prod_serializer = ProjectProductSerializer(project, many=True)
        return Response(proj_prod_serializer.data)
