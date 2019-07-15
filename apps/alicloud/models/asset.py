# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Asset(models.Model):
    id = models.UUIDField(primary_key=True)
    node_id = models.UUIDField()
    type = models.CharField(max_length=128, verbose_name=_('AssetType'))
    instance_id = models.CharField(max_length=128, verbose_name=_('InstanceId'))
    instance_name = models.CharField(max_length=128, verbose_name=_('InstanceName'))
    status = models.CharField(max_length=128, verbose_name=_('Status'))

    class Meta:
        db_table = 'alicloud_assets'
