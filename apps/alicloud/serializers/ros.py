# -*- coding: utf-8 -*-
from rest_framework import serializers
from alicloud.models import RosTemplate


class RosTemplateSerializer(serializers.ModelSerializer):
    """
    ros模板的数据结构
    """
    class Meta:
        model = RosTemplate
        fields = '__all__'