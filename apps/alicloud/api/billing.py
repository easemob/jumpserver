# -*- coding:utf-8 -*-
#
# Created Time: 2019-07-05 16:06
# Be From: ZouRi
# Last Modified: x
# e6b0b8e8bf9ce5b9b4e8bdbbefbc8ce6b0b8e8bf9ce783ade6b3aae79b88e79cb6
#

import arrow

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
        dateformat = "%Y-%m-%dT%H:%M:%SZ"

        taskids = list()
        for bill_cycle in [m[0].format("YYYY-MM") for m in arrow.Arrow.span_range('month',
                                                                                  datetime.strptime(begin_time,
                                                                                                    dateformat),
                                                                                  datetime.strptime(end_time,
                                                                                                    dateformat))]:
            taskids.append(sync_billing_info_manual.delay(bill_cycle).id)
        return Response({"task": taskids})


class BillingQuery(APIView):
    begin_time = None
    end_time = None
    node = None

    def _get_bill_cycles(self):
        if self.begin_time:
            dateformat = "%Y-%m-%dT%H:%M:%SZ"
            return [m[0].format("YYYY-MM") for m in arrow.Arrow.span_range('month',
                                                                           datetime.strptime(
                                                                               self.begin_time,
                                                                               dateformat),
                                                                           datetime.strptime(
                                                                               self.end_time,
                                                                               dateformat))]
        return None

    def get(self, *args, **kwargs):
        self.begin_time = self.request.query_params.get('begin_time', None)
        self.end_time = self.request.query_params.get('end_time', None)
        node_key = self.request.query_params.get('key')

        if not node_key or (node_key == "1"):
            # self.node = Node.root()
            # queryset = [self.node]
            queryset = None
        else:
            self.node = Node.objects.get(key=node_key)
            queryset = sorted([self.node])
        info = self.get_node_money(queryset)
        return Response(info)

    def get_node_money(self, node_keys):
        """
        获取节点下所有实例的订单金额
        :param node_keys:
        :return:
        """

        res_data = {}
        total_money = 0.0
        if node_keys:
            for node_key in node_keys:
                node_money = 0.0
                res_data[node_key.key] = dict()
                _, instance_info = self.get_all_instance(node_key.key)
                for node_info in instance_info:
                    money = self.get_instance_payment(node_info.instance_id)
                    total_money += money
                    node_money += money
                    if node_info.type in res_data[node_key.key].keys():
                        res_data[node_key.key][node_info.type]["money"] += money
                        res_data[node_key.key][node_info.type]["instance_list"][node_info.instance_id]=dict(
                            money=money, instance_name=node_info.instance_name
                        )
                    else:
                        res_data[node_key.key][node_info.type] = dict(
                            money=money, instance_list={node_info.instance_id: dict(
                                money=money, instance_name=node_info.instance_name
                            )})
                res_data[node_key.key]["node_money"] = node_money
        else:
            res_data["1"] = dict()
            bill_cycles = self._get_bill_cycles()
            result = Billing.objects.filter(cycle__in=bill_cycles) \
                .values('product_code', 'product_name') \
                .annotate(total_money=Sum('payment_amount'))
            for t in result:
                total_money += t["total_money"]
                res_data["1"][t["product_code"]] = dict(money=t["total_money"],
                    instance_list={t["product_code"]: dict(money=t["total_money"], instance_name=t["product_name"])})
            res_data["1"]["node_money"] = total_money

        res_data['total_money'] = total_money
        return res_data

    def get_instance_payment(self, instance_id):
        """
        获取目标实例的订单金额
        :param instance_id: 实例ID
        :return float: money
        """
        if not self.begin_time:
            bill_cycles = [arrow.utcnow().format('YYYY-MM')]
        else:
            bill_cycles = self._get_bill_cycles()
        orders_info = Billing.objects.filter(
            cycle__in=bill_cycles,
            instance_id=instance_id
        ).aggregate(Sum('payment_amount'))
        if orders_info['payment_amount__sum']:
            return orders_info['payment_amount__sum']
        return 0.0

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

        assets_ids = Node.objects.filter(key__startswith=node)
        assets_list = Asset.objects.filter(node_id__in=assets_ids)
        total_num = assets_list.count()

        return total_num, assets_list


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
