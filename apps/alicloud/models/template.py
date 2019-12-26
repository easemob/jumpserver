# -*- coding: utf-8 -*-
import uuid
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


NETWORK_TYPE_CHOICES = (
    ('classic', 'classic'),
    ('vpc', 'vpc'),
)

DISK_CATEGORY = (
    ('cloud', 'cloud'),
    ('cloud_efficiency', 'cloud_efficiency'),
    ('cloud_ssd', 'cloud_ssd'),
    ('cloud_essd', 'cloud_essd')
)

INSTANCE_CHARGE_TYPE = (
    ('PrePaid', 'PrePaid'),
    ('PostPaid', 'PostPaid')
)

INTERNET_CHARGE_TYPE = (
    ('PayByTraffic', 'PayByTraffic'),
    ('PayByBandwidth', 'PayByBandwidth')
)


class EcsTemplate(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=256, blank=False)
    description = models.CharField(max_length=512, default='')
    region = models.CharField(max_length=256)
    zone = models.CharField(max_length=256)
    instance_type = models.CharField(max_length=256)
    cores = models.IntegerField()
    memory = models.IntegerField()
    image = models.CharField(max_length=256)
    sg = models.CharField(max_length=256)
    network_type = models.CharField(max_length=20, choices=NETWORK_TYPE_CHOICES)
    vpc = models.CharField(max_length=256, null=True, blank=True, default=None)
    vswitch = models.CharField(max_length=256, null=True, blank=True, default=None)
    password = models.CharField(max_length=256, null=True, blank=True, default='')
    password_inherit = models.BooleanField(default=True)
    system_disk_category = models.CharField(max_length=256, choices=DISK_CATEGORY, default="cloud_efficiency")
    system_disk_size = models.IntegerField(default=40)
    data_disk_info = models.TextField()
    instance_name = models.CharField(max_length=256)
    instance_charge_type = models.CharField(default='PrePaid', max_length=64, choices=INSTANCE_CHARGE_TYPE)
    has_public_ip = models.BooleanField(null=True, default=False)
    internet_bandwidth = models.IntegerField(null=True, default=0)
    internet_charge_type = models.CharField(default='PayByBandwidth', max_length=64, choices=INTERNET_CHARGE_TYPE)
    period = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))
    domain = models.ForeignKey("assets.Domain", null=True, blank=True, verbose_name=_("Domain"),
                               on_delete=models.SET_NULL)
    nodes = models.ManyToManyField('assets.Node', default=default_node, related_name='ecs_template', verbose_name=_("Nodes"))
    # Auth
    admin_user = models.ForeignKey('assets.AdminUser', on_delete=models.PROTECT, null=True,
                                   verbose_name=_("Admin user"),
                                   )
