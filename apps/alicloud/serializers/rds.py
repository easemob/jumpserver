# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from ..models import Rds

__all__ = [
    'RdsSerializer'
]


class RdsSerializer(serializers.ModelSerializer):
    """
    资产的数据结构
    """
    class Meta:
        model = Rds
        fields = '__all__'
