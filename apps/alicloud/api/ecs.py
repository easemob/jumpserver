# -*- coding: utf-8 -*-
from django.db.models import Q, Count
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.utils.translation import ugettext_lazy as _
from alicloud import serializers
from alicloud.ali_utils import EcsClient
from assets.models import Node, AdminUser
from common.permissions import IsOrgAdmin, IsOrgAdminOrAppUser, IsValidUser
from rest_framework.response import Response
from common.utils import get_object_or_none
from common.tasks import send_mail_async
from orgs.mixins import OrgBulkModelViewSet
from ..tasks import sync_ecs_list_info_manual
from ..models import *


class AliCloudEcsSyncUpdate(APIView):
    permission_classes = (IsOrgAdmin,)

    def post(self, request, *args, **kwargs):
        task = sync_ecs_list_info_manual.delay()
        return Response({"task": task.id})


class AliCloudEcsViewSet(mixins.CreateModelMixin, ReadOnlyModelViewSet):
    filter_fields = ("instance_name", "instance_id", "inner_ip", "public_ip", 'status', "region")
    search_fields = filter_fields
    ordering_fields = ("instance_name", "inner_ip", "cpu", "memory", 'status', 'expired_time')
    queryset = Ecs.objects.all()
    serializer_class = serializers.EcsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsValidUser,)

    def set_assets_node(self, assets):
        if not isinstance(assets, list):
            assets = [assets]
        node = Node.root()
        node_id = self.request.query_params.get('node_id')
        if node_id:
            node = get_object_or_none(Node, pk=node_id)
        node.assets.add(*assets)

    def filter_node(self, queryset):
        unallocated = self.request.query_params.get("unallocated")
        if unallocated:
            queryset = queryset.annotate(num_nodes=Count('nodes'))
            queryset = queryset.filter((Q(num_nodes=0)) | (Q(nodes=Node.root()) & Q(num_nodes=1)))
            return queryset
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

    def notify_user_with_email(self, recipient_list, succeed, result):
        subject = '创建ECS结果'
        message = ''
        if succeed:
            message = f'<p style="color:green">创建成功, 实例id为:{result}</p>'
        else:
            message = f'<p style="color:red">创建失败, 错误信息为:{result}</p>'
        send_mail_async.delay(subject, message, recipient_list, html_message=message)

    def create(self, request, *args, **kwargs):
        # task = create_alicloud_ecs.delay(request.data, request.user.username, request.user.email)
        # return Response({"task": task.id})
        data = request.data
        ecs_client = EcsClient()
        succeed, result = ecs_client.create_and_run_instance(**request.data)
        self.notify_user_with_email([request.user.email], succeed, result)
        if succeed:
            template_id = data.pop('template')
            record = EcsCreateRecord.objects.create(result_ids=result, uid=request.user.username, **data)
            template = get_object_or_none(EcsTemplate, id=template_id)
            record.template = template
            record.save()
            return Response(data={'create_ids': result}, status=201)
        else:
            return Response(data={'error_info': result}, status=400)


class EcsTemplateViewSet(OrgBulkModelViewSet):
    """
    API endpoint that allows Asset to be viewed or edited.
    """
    filter_fields = ('name', 'instance_type', 'network_type', 'zone', 'region')
    search_fields = filter_fields
    ordering_fields = ('date_created', 'region', 'network_type', 'instance_type')
    queryset = EcsTemplate.objects.all()
    serializer_class = serializers.EcsTemplateSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsOrgAdminOrAppUser,)
    success_message = _("%(hostname)s was %(action)s successfully")

    def set_assets_node(self, assets):
        if not isinstance(assets, list):
            assets = [assets]
        node_id = self.request.query_params.get('node_id')
        if not node_id:
            return
        node = get_object_or_none(Node, pk=node_id)
        if not node:
            return
        node.ecs.add(*assets)

    def perform_create(self, serializer):
        assets = serializer.save()
        self.set_assets_node(assets)

    def filter_admin_user_id(self, queryset):
        admin_user_id = self.request.query_params.get('admin_user_id')
        if not admin_user_id:
            return queryset
        admin_user = get_object_or_404(AdminUser, id=admin_user_id)
        queryset = queryset.filter(admin_user=admin_user)
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = self.filter_admin_user_id(queryset)
        return queryset
