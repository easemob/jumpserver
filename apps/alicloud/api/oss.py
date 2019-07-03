# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from alicloud import serializers
from assets.models import Node
from common.permissions import IsOrgAdmin, IsOrgAdminOrAppUser
from rest_framework.response import Response

from common.utils import get_object_or_none
from ..tasks import sync_oss_list_info_manual
from ..models import *


class AliCloudOssSyncUpdate(APIView):
    permission_classes = (IsOrgAdmin,)

    def post(self, request, *args, **kwargs):
        task = sync_oss_list_info_manual.delay()
        return Response({"task": task.id})


class AliCloudOssViewSet(ReadOnlyModelViewSet):
    filter_fields = ("instance_name", "instance_id", "region")
    search_fields = filter_fields
    ordering_fields = ("instance_name", "region" 'create_time')
    queryset = Oss.objects.all()
    serializer_class = serializers.OssSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsOrgAdminOrAppUser,)

    def set_assets_node(self, assets):
        if not isinstance(assets, list):
            assets = [assets]
        node = Node.root()
        node_id = self.request.query_params.get('node_id')
        if node_id:
            node = get_object_or_none(Node, pk=node_id)
        node.assets.add(*assets)

    def filter_node(self, queryset):
        node_id = self.request.query_params.get("node_id")
        if not node_id:
            return queryset

        node = get_object_or_404(Node, id=node_id)
        show_current_asset = self.request.query_params.get("show_current_asset") in ('1', 'true')

        if node.is_root() and show_current_asset:
            queryset = queryset.filter(
                Q(nodes=node_id) | Q(nodes__isnull=True)
            )
        elif node.is_root() and not show_current_asset:
            pass
        elif not node.is_root() and show_current_asset:
            queryset = queryset.filter(nodes=node)
        else:
            queryset = queryset.filter(
                nodes__key__regex='^{}(:[0-9]+)*$'.format(node.key),
            )
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = self.filter_node(queryset)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset().distinct()
        return queryset



