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
    order_id = models.BigIntegerField(null=False, verbose_name=_('OrderId'))
    order_id_index = models.BigIntegerField(default=0, verbose_name=_('OrderIdIndex'))
    product_code = models.CharField(max_length=20, null=False, verbose_name=_('ProductCode'))
    payment_status = models.CharField(max_length=20, null=False, verbose_name=_('PaymentStatus'))
    order_type = models.CharField(max_length=20, null=False, verbose_name=_('OrderType'))
    payment_time = models.DateTimeField(verbose_name=_('PaymentTime'))
    create_time = models.DateTimeField(verbose_name=_('CreateTime'))
    payment_amount = models.FloatField(null=False, default=0.0, verbose_name=_('PaymentAmount'))
    payment_gross_amount = models.FloatField(null=False, default=0.0, verbose_name=_('PaymentGrossAmount'))
    instance_ids = models.TextField(verbose_name=_('InstanceIDs'))

    class Meta:
        unique_together = ("order_id", "order_id_index")
