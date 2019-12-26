# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from ..models import Ecs, EcsTemplate

__all__ = [
    'EcsSerializer', 'EcsTemplateSerializer',
]


class EcsSerializer(serializers.ModelSerializer):
    """
    资产的数据结构
    """
    class Meta:
        model = Ecs
        fields = '__all__'




class EcsTemplateSerializer(serializers.ModelSerializer):
    """
    ecs模板的数据结构
    """
    class Meta:
        model = EcsTemplate
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
