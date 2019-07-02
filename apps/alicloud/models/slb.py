# -*- coding: utf-8 -*-
import uuid
from functools import reduce

from orgs.mixins import OrgModelMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


def default_node():
    try:
        from assets.models import Node
        root = Node.root()
        return root
    except:
        return None


class Ecs(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    instance_id = models.CharField(max_length=128, verbose_name=_('InstanceId'))
    inner_ip = models.CharField(max_length=128, verbose_name=_('InnerIp'), db_index=True)
    public_ip = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('PublicIp'))
    network_type = models.CharField(max_length=128, verbose_name=_('NetworkType'))
    instance_name = models.CharField(max_length=128, verbose_name=_('InstanceName'))
    region = models.CharField(max_length=128, verbose_name=_('RegionId'))
    status = models.CharField(max_length=128, verbose_name=_('Status'))
    io_optimized = models.BooleanField(verbose_name=_('IoOptimized'))
    expired_time = models.DateTimeField(verbose_name=_('ExpiredTime'))
    maximum_bandwidth = models.IntegerField(default=0, verbose_name=('InternetMaxBandwidthOut'))
    cpu = models.IntegerField(default=0, verbose_name=('Cpu'))
    memory = models.IntegerField(default=0, verbose_name=('Memory'))
    instance_charge_type = models.CharField(max_length=128, verbose_name=_('InstanceChargeType'))
    instance_type = models.CharField(max_length=128, verbose_name=_('InstanceType'))
    nodes = models.ManyToManyField('assets.Node', default=default_node, related_name='ecs', verbose_name=_("Nodes"))


    @property
    def instance_info(self):

        return '{}|{} '.format(
            self.instance_id,
            self.instance_name
        )

    def get_nodes(self):
        from assets.models import Node
        nodes = self.nodes.all() or [Node.root()]
        return nodes

    def get_all_nodes(self, flat=False):
        nodes = []
        for node in self.get_nodes():
            _nodes = node.get_ancestor(with_self=True)
            nodes.append(_nodes)
        if flat:
            nodes = list(reduce(lambda x, y: set(x) | set(y), nodes))
        return nodes

    def as_tree_node(self, parent_node):
        from common.tree import TreeNode
        icon_skin = 'file'

        data = {
            'id': str(self.id),
            'name': self.instance_name,
            'title': self.inner_ip,
            'pId': parent_node.key,
            'isParent': False,
            'open': False,
            'iconSkin': 'linux',
            'meta': {
                'type': 'asset',
                'asset': {
                    'id': self.id,
                    'hostname': self.instance_name,
                    'ip': self.inner_ip,
                }
            }
        }
        tree_node = TreeNode(**data)
        return tree_node



