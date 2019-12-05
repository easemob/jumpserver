# -*- coding:utf-8 -*-
#
# Created Time: 2019-07-05 11:33
# Be From: ZouRi 
# Last Modified: x
# e6b0b8e8bf9ce5b9b4e8bdbbefbc8ce6b0b8e8bf9ce783ade6b3aae79b88e79cb6
#

from django.db import models
from orgs.mixins import OrgManager
from django.utils.translation import ugettext_lazy as _


class Billing(models.Model):
    id = models.AutoField(primary_key=True)
    instance_id = models.CharField(max_length=128, default="", verbose_name=_('InstanceId'))
    cycle = models.CharField(max_length=50, null=False, default="", verbose_name=('BillingCycle'))
    payment_amount = models.FloatField(null=False, default=0.0, verbose_name=_('PaymentAmount'))
    product_code = models.CharField(max_length=20, null=False, default="",  verbose_name=_('ProductCode'))
    product_name = models.CharField(max_length=200, null=False, default="", verbose_name=_('ProductName'))

    class Meta:
        unique_together = ("cycle", "product_code", "instance_id")
        db_table = 'alicloud_billing'
