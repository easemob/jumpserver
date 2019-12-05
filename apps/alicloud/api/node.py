# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.db.models import Q
from rest_framework import generics

from assets.models import Node
from common.permissions import IsOrgAdmin, IsValidUser, PermissionsMixin
from common.tree import TreeNodeSerializer
from ..models import *
from ..serializers import *


class NodeChildrenAsTreeApi(generics.ListAPIView):
    """
    节点子节点作为树返回，
    [
      {
        "id": "",
        "name": "",
        "pId": "",
        "meta": ""
      }
    ]

    """
    permission_classes = (IsValidUser,)
    serializer_class = TreeNodeSerializer
    node = None
    is_root = False

    def get_queryset(self):
        node_key = self.request.query_params.get('key')
        if node_key:
            self.node = Node.objects.get(key=node_key)
            queryset = self.node.get_children(with_self=False)
        else:
            self.is_root = True
            self.node = Node.root()
            queryset = list(self.node.get_children(with_self=True))
            nodes_invalid = Node.objects.exclude(key__startswith=self.node.key)
            queryset.extend(list(nodes_invalid))
        queryset = [self.as_tree_node(node) for node in queryset]
        queryset = sorted(queryset)
        return queryset

    def as_tree_node(self, node):
        from common.tree import TreeNode
        from assets.serializers import NodeSerializer
        name = '{} ({})'.format(node.value, self.assets_amount(node))
        node_serializer = NodeSerializer(instance=node)
        data = {
            'id': node.key,
            'name': name,
            'title': name,
            'pId': node.parent_key,
            'isParent': True,
            'open': node.is_root(),
            'meta': {
                'node': node_serializer.data,
                'type': 'node'
            }
        }
        tree_node = TreeNode(**data)
        return tree_node

    def assets_amount(self, node):
        asset_type = self.request.query_params.get('type')
        cache_key = ''
        if asset_type == 'ecs':
            cache_key = '_ECS_NODE_ASSETS_AMOUNT_{}'.format(node.key)
        if asset_type == 'slb':
            cache_key = '_SLB_NODE_ASSETS_AMOUNT_{}'.format(node.key)
        if asset_type == 'oss':
            cache_key = '_OSS_NODE_ASSETS_AMOUNT_{}'.format(node.key)
        if asset_type == 'rds':
            cache_key = '_RDS_NODE_ASSETS_AMOUNT_{}'.format(node.key)
        if asset_type == 'kvstore':
            cache_key = '_KVSTORE_NODE_ASSETS_AMOUNT_{}'.format(node.key)
        cached = cache.get(cache_key)
        if cached is not None:
            return cached
        assets_amount = self.get_all_assets(node).count()
        cache.set(cache_key, assets_amount, 3600)
        return assets_amount

    def get_all_assets(self, node):
        pattern = r'^{0}$|^{0}:'.format(node.key)
        asset_type = self.request.query_params.get('type')
        args = []
        kwargs = {}
        assets = []
        if node.is_root():
            args.append(Q(nodes__key__regex=pattern) | Q(nodes=None))
        else:
            kwargs['nodes__key__regex'] = pattern
        if asset_type == 'ecs':
            assets = Ecs.objects.filter(*args, **kwargs).distinct()
        if asset_type == 'slb':
            assets = Slb.objects.filter(*args, **kwargs).distinct()
        if asset_type == 'kvstore':
            assets = KvStore.objects.filter(*args, **kwargs).distinct()
        if asset_type == 'rds':
            assets = Rds.objects.filter(*args, **kwargs).distinct()
        if asset_type == 'oss':
            assets = Oss.objects.filter(*args, **kwargs).distinct()
        return assets

    def filter_assets(self, queryset):
        asset_type = self.request.query_params.get('type')
        include_assets = self.request.query_params.get('assets', '0') == '1'
        if not include_assets:
            return queryset

        assets = ''
        if self.node.is_default_node():
            if asset_type == 'ecs':
                assets = Ecs.objects.filter(Q(nodes__id=self.id) | Q(nodes__isnull=True))
            if asset_type == 'rds':
                assets = Rds.objects.filter(Q(nodes__id=self.id) | Q(nodes__isnull=True))
            if asset_type == 'kvstore':
                assets = KvStore.objects.filter(Q(nodes__id=self.id) | Q(nodes__isnull=True))
            if asset_type == 'slb':
                assets = Slb.objects.filter(Q(nodes__id=self.id) | Q(nodes__isnull=True))
            if asset_type == 'oss':
                assets = Oss.objects.filter(Q(nodes__id=self.id) | Q(nodes__isnull=True))
        else:
            if asset_type == 'ecs':
                assets = Ecs.objects.filter(nodes__id=self.id)
            if asset_type == 'rds':
                assets = Rds.objects.filter(nodes__id=self.id)
            if asset_type == 'kvstore':
                assets = KvStore.objects.filter(nodes__id=self.id)
            if asset_type == 'slb':
                assets = Slb.objects.filter(nodes__id=self.id)
            if asset_type == 'oss':
                assets = Oss.objects.filter(nodes__id=self.id)

        assets = assets.distinct()
        for asset in assets:
            queryset.append(asset.as_tree_node(self.node))
        return queryset

    def filter_queryset(self, queryset):
        queryset = self.filter_assets(queryset)
        queryset = self.filter_refresh_nodes(queryset)
        return queryset

    def filter_refresh_nodes(self, queryset):
        if self.request.query_params.get('refresh', '0') == '1':
            cache.delete_pattern('*NODE_ASSETS_AMOUNT*')
        return queryset


class NodeAddEcsApi(generics.UpdateAPIView):
    serializer_class = NodeEcsSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        ret = instance.ecs.add(*tuple(assets))


class NodeRemoveEcsApi(generics.UpdateAPIView):
    serializer_class = NodeEcsSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        if instance != Node.root():
            instance.ecs.remove(*tuple(assets))
        else:
            assets = [asset for asset in assets if asset.nodes.count() > 1]
            instance.ecs.remove(*tuple(assets))


class NodeReplaceEcsApi(generics.UpdateAPIView):
    serializer_class = NodeEcsSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        for asset in assets:
            asset.nodes.set([instance])


class NodeAddSlbApi(generics.UpdateAPIView):
    serializer_class = NodeSlbSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        ret = instance.slb.add(*tuple(assets))


class NodeReplaceSlbApi(generics.UpdateAPIView):
    serializer_class = NodeSlbSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        for asset in assets:
            asset.nodes.set([instance])


class NodeRemoveSlbApi(generics.UpdateAPIView):
    serializer_class = NodeSlbSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        if instance != Node.root():
            instance.slb.remove(*tuple(assets))
        else:
            assets = [asset for asset in assets if asset.nodes.count() > 1]
            instance.slb.remove(*tuple(assets))


class NodeAddRdsApi(generics.UpdateAPIView):
    serializer_class = NodeRdsSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        ret = instance.rds.add(*tuple(assets))


class NodeReplaceRdsApi(generics.UpdateAPIView):
    serializer_class = NodeRdsSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        for asset in assets:
            asset.nodes.set([instance])


class NodeRemoveRdsApi(generics.UpdateAPIView):
    serializer_class = NodeRdsSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        if instance != Node.root():
            instance.rds.remove(*tuple(assets))
        else:
            assets = [asset for asset in assets if asset.nodes.count() > 1]
            instance.rds.remove(*tuple(assets))


class NodeAddOssApi(generics.UpdateAPIView):
    serializer_class = NodeOssSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        ret = instance.oss.add(*tuple(assets))


class NodeReplaceOssApi(generics.UpdateAPIView):
    serializer_class = NodeOssSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        for asset in assets:
            asset.nodes.set([instance])


class NodeRemoveOssApi(generics.UpdateAPIView):
    serializer_class = NodeOssSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        if instance != Node.root():
            instance.oss.remove(*tuple(assets))
        else:
            assets = [asset for asset in assets if asset.nodes.count() > 1]
            instance.oss.remove(*tuple(assets))


class NodeAddKvStoreApi(generics.UpdateAPIView):
    serializer_class = NodeKvStoreSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        ret = instance.kvstore.add(*tuple(assets))


class NodeReplaceKvStoreApi(generics.UpdateAPIView):
    serializer_class = NodeKvStoreSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        for asset in assets:
            asset.nodes.set([instance])


class NodeRemoveKvStoreApi(generics.UpdateAPIView):
    serializer_class = NodeKvStoreSerializer
    queryset = Node.objects.all()
    permission_classes = (IsOrgAdmin,)
    instance = None

    def perform_update(self, serializer):
        assets = serializer.validated_data.get('assets')
        instance = self.get_object()
        if instance != Node.root():
            instance.kvstore.remove(*tuple(assets))
        else:
            assets = [asset for asset in assets if asset.nodes.count() > 1]
            instance.kvstore.remove(*tuple(assets))
