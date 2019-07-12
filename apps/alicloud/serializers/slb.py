# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from ..models import Slb

__all__ = [
    'SlbSerializer'
]


class SlbSerializer(serializers.ModelSerializer):
    """
    资产的数据结构
    """
    class Meta:
        model = Slb
        fields = '__all__'
