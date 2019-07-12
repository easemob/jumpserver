# -*- coding:utf-8 -*-
#
# Created Time: 2019-07-05 16:06
# Be From: ZouRi
# Last Modified: x
# e6b0b8e8bf9ce5b9b4e8bdbbefbc8ce6b0b8e8bf9ce783ade6b3aae79b88e79cb6
#
from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from ..tasks import sync_billing_info_manual
from common.permissions import IsOrgAdmin
from common.tree import TreeNodeSerializer
from ..serializers import *
from django.db.models import Sum


class BillingQuerySyncTask(APIView):

    def post(self, *args, **kwargs):
        data = self.request.data
        begin_time = data.get('begin_time', None)
        end_time = data.get('end_time', None)
        task = sync_billing_info_manual.delay(begin_time, end_time)
        return Response({"task": task.id})


class BillingQuery(APIView):
    begin_time = None
    end_time = None
    node = None

    def get(self, *args, **kwargs):
        self.begin_time = self.request.query_params.get('begin_time', None)
        self.end_time = self.request.query_params.get('end_time', None)
        node_key = self.request.query_params.get('key')

        if node_key:
            self.node = Node.objects.get(key=node_key)
            # queryset = self.node.get_all_assets()
            # print(queryset)
            queryset = [self.node]
        else:
            self.node = Node.root()
            # queryset = list(self.node.get_children(with_self=True))
            # nodes_invalid = Node.objects.exclude(key__startswith=self.node.key)
            # queryset.extend(list(nodes_invalid))
            queryset = [self.node]
        queryset = sorted(queryset)
        print(queryset)
        info = self.get_node_money(queryset)
        return info

    def get_node_money(self, node_keys):
        """
        获取节点下所有实例的订单金额
        :param node_keys:
        :return:
        """
        res_data = {}
        total_money = 0
        for node_key in node_keys:
            # 新增节点
            node_info = {
                'ecs': {
                    'money': 0,
                },
                'slb': {
                    'money': 0,
                },
                'kvstore': {
                    'money': 0,
                },
                'rds': {
                    'money': 0,
                },
                'oss': {
                    'money': 0,
                }
            }

            instance_num, instance_info = self.get_all_instance(node_key)
            # 节点下实例花费金额
            node_money = 0

            for _type, instances in instance_info.items():
                instance_list = {}
                for i in instances:
                    instance_money = self.get_orders_payment(i.instance_id)
                    instance_list[i.instance_id] = {
                        'money': instance_money,
                        'instance_name': i.instance_name
                    }
                    node_money += instance_money

                    # 节点类型下总数据
                    node_info[_type]['money'] += instance_money

                # noinspection PyTypeChecker
                node_info[_type]['instance_list'] = instance_list

            # 节点总花费
            node_info['node_money'] = node_money

            res_data[node_key.key] = node_info
            total_money += node_money
        res_data['total_money'] = total_money
        return Response(res_data)

    def get_orders_payment(self, instance_id):
        """
        获取目标实例的订单金额
        :param instance_id: 实例ID
        :return: 金钱
        """
        if not self.begin_time:
            today = datetime.now()
            begin_time = datetime.strptime(today.strftime("%Y-%m-01T00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ")
            end_time = datetime.strptime(today.strftime("%Y-%m-%dT00:00:00Z"), "%Y-%m-%dT%H:%M:%SZ")
        else:
            begin_time = datetime.strptime(self.begin_time, "%Y-%m-%dT%H:%M:%SZ")
            end_time = datetime.strptime(self.end_time, "%Y-%m-%dT%H:%M:%SZ")
        orders_info = Billing.objects.filter(
                payment_time__range=(begin_time, end_time),
                instance_ids__contains=instance_id
            ).aggregate(Sum('payment_amount'))
        if orders_info['payment_amount__sum']:
            return orders_info['payment_amount__sum']
        return 0.0

    @staticmethod
    def get_all_instance(node):
        """
        获取指定节点下所有实例
        :param node:
        :return:
        """
        pattern = r'^{0}$|^{0}:'.format(node.key)
        args = []
        kwargs = {}

        if node.is_root():
            args.append(Q(nodes__key__regex=pattern) | Q(nodes=None))
        else:
            kwargs['nodes__key__regex'] = pattern

        ecs_assets = Ecs.objects.filter(*args, **kwargs).distinct()
        slb_assets = Slb.objects.filter(*args, **kwargs).distinct()
        kvstore_assets = KvStore.objects.filter(*args, **kwargs).distinct()
        rds_assets = Rds.objects.filter(*args, **kwargs).distinct()
        oss_assets = Oss.objects.filter(*args, **kwargs).distinct()

        assets = {
            'ecs': list(ecs_assets),
            'slb': list(slb_assets),
            'kvstore': list(kvstore_assets),
            'rds': list(rds_assets),
            'oss': list(oss_assets)
        }

        total_num = ecs_assets.count() + slb_assets.count() + kvstore_assets.count() + \
            rds_assets.count() + oss_assets.count()

        return total_num, assets


class BillingQueryNode(ListAPIView):
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
    permission_classes = (IsOrgAdmin,)
    serializer_class = TreeNodeSerializer
    node = None
    is_root = False
    begin_time = None
    end_time = None

    def get_queryset(self):
        self.begin_time = self.request.query_params.get('begin_time', None)
        self.end_time = self.request.query_params.get('end_time', None)
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
        instance_num = self.assets_amount(node)
        name = f'{node.value} ({instance_num})'
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
        # 获取节点下所有实例
        total_num = 0
        all_key = {
            'kvstore': '_KVSTORE_NODE_ASSETS_AMOUNT_{}'.format(node.key),
            'rds': '_RDS_NODE_ASSETS_AMOUNT_{}'.format(node.key),
            'oss': '_OSS_NODE_ASSETS_AMOUNT_{}'.format(node.key),
            'slb': '_SLB_NODE_ASSETS_AMOUNT_{}'.format(node.key),
            'ecs': '_ECS_NODE_ASSETS_AMOUNT_{}'.format(node.key),
        }
        for i_name, i_key in all_key.items():
            assets_amount = self.get_all_assets(node, i_name)
            total_num += assets_amount
        return total_num

    @staticmethod
    def get_all_assets(node, asset_type):
        # 获取所有实例
        pattern = r'^{0}$|^{0}:'.format(node.key)
        args = []
        kwargs = {}

        if node.is_root():
            args.append(Q(nodes__key__regex=pattern) | Q(nodes=None))
        else:
            kwargs['nodes__key__regex'] = pattern

        if asset_type == 'ecs':
            assets = Ecs.objects.filter(*args, **kwargs).distinct()
        elif asset_type == 'slb':
            assets = Slb.objects.filter(*args, **kwargs).distinct()
        elif asset_type == 'kvstore':
            assets = KvStore.objects.filter(*args, **kwargs).distinct()
        elif asset_type == 'rds':
            assets = Rds.objects.filter(*args, **kwargs).distinct()
        elif asset_type == 'oss':
            assets = Oss.objects.filter(*args, **kwargs).distinct()
        else:
            assets = []
        return len(assets)



