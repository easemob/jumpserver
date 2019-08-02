# -*- coding:utf-8 -*-
#
# Created Time: 2019-08-01 15:00
# Be From: xiao bai
#
from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from ..models import Asset

__all__ = [
    'AssetSerializer'
]


class AssetSerializer(serializers.ModelSerializer):
    """
    资产的数据结构
    """
    class Meta:
        model = Asset
        fields = '__all__'
