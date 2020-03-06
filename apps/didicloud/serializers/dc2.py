# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from ..models import Dc2

__all__ = [
    'Dc2Serializer'
]


class Dc2Serializer(serializers.ModelSerializer):
    """
    资产的数据结构
    """
    class Meta:
        model = Dc2
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
