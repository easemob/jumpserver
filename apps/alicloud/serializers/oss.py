# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from ..models import Oss

__all__ = [
    'OssSerializer'
]


class OssSerializer(serializers.ModelSerializer):
    """
    资产的数据结构
    """
    class Meta:
        model = Oss
        fields = '__all__'
