# -*- coding:utf-8 -*-
#
# Created Time: 2019-07-05 16:20
# Be From: ZouRi 
# Last Modified: x
# e6b0b8e8bf9ce5b9b4e8bdbbefbc8ce6b0b8e8bf9ce783ade6b3aae79b88e79cb6
#
from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from ..models import Billing

__all__ = [
    'BillingSerializer'
]


class BillingSerializer(serializers.ModelSerializer):
    """
    资产的数据结构
    """
    class Meta:
        model = Billing
        fields = '__all__'
