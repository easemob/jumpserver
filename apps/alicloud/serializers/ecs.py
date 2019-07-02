# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from ..models import Ecs

__all__ = [
    'EcsSerializer'
]


class EcsSerializer(serializers.ModelSerializer):
    """
    资产的数据结构
    """
    class Meta:
        model = Ecs
        fields = '__all__'



# class AssetAsNodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Asset
#         fields = ['id', 'hostname', 'ip', 'port', 'platform', 'protocol']
#
#
#
# class AssetSimpleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Asset
#         fields = ['id', 'hostname', 'port', 'ip', 'connectivity']
