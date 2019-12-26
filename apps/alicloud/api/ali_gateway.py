# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework.response import Response
from alicloud.ali_utils import EcsClient
from common.permissions import IsValidUser, IsOrgAdmin


class AliCloudEcsTemplate(APIView):
    permission_classes = (IsValidUser,)

    def get(self, request, *args, **kwargs):
        return Response({"task": 1})


class AliCloudEcsRegion(APIView):
    permission_classes = (IsValidUser,)

    def get(self, request, *args, **kwargs):
        return Response({"task": 1})


class AliCloudEcsZone(APIView):
    permission_classes = (IsValidUser,)

    def get(self, request, *args, **kwargs):
        region = kwargs.pop('region')
        ecs = EcsClient(region)
        result = ecs.query_zones()
        return Response(result)


class AliCloudEcsVpc(APIView):
    permission_classes = (IsValidUser,)

    def get(self, request, *args, **kwargs):
        region = kwargs.pop('region')
        ecs = EcsClient(region)
        result = ecs.get_vpc()
        return Response(result)


class AliCloudEcsVswitch(APIView):
    permission_classes = (IsValidUser,)

    def get(self, request, *args, **kwargs):
        region = kwargs.pop('region')
        vpc_id = kwargs.pop('vpc')
        ecs = EcsClient(region)
        result = ecs.get_vswitch(vpc_id)
        return Response(result)


class AliCloudEcsSecurityGroup(APIView):
    permission_classes = (IsValidUser,)

    def get(self, request, *args, **kwargs):
        region = kwargs.pop('region')
        ecs = EcsClient(region)
        result = ecs.get_security_group(network_type=request.query_params.get('networkType'),
                                        vpc_id=request.query_params.get('vpcId'))
        return Response(result)


class AliCloudEcsInstanceType(APIView):
    permission_classes = (IsValidUser,)

    def get(self, request, *args, **kwargs):
        region = kwargs.pop('region')
        zone = kwargs.pop('zone')
        ecs = EcsClient(region)
        result = ecs.query_instance_type_by_condition(cores=request.query_params.get('cores'),
                                                      memory=request.query_params.get('memory'),
                                                      network_type=request.query_params.get('network_type'), zone=zone)
        return Response(result)


class AliCloudEcsImage(APIView):
    permission_classes = (IsValidUser,)

    def get(self, request, *args, **kwargs):
        region = kwargs.pop('region')
        ecs = EcsClient(region)
        result = ecs.query_self_images()
        return Response(result)
