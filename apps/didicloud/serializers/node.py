# -*- coding: utf-8 -*-
from rest_framework import serializers
from assets.models import Node
from ..models import *


class NodeDc2Serializer(serializers.ModelSerializer):
    assets = serializers.PrimaryKeyRelatedField(many=True, queryset=Dc2.objects.all())

    class Meta:
        model = Node
        fields = ['assets']
