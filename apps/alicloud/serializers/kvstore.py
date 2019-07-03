# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from ..models import KvStore

__all__ = [
    'KvStoreSerializer'
]


class KvStoreSerializer(serializers.ModelSerializer):
    """
    资产的数据结构
    """
    class Meta:
        model = KvStore
        fields = '__all__'
