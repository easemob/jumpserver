# -*- coding: utf-8 -*-
from rest_framework import serializers
from assets.models import Node
from ..models import *


class NodeEcsSerializer(serializers.ModelSerializer):
    assets = serializers.PrimaryKeyRelatedField(many=True, queryset=Ecs.objects.all())

    class Meta:
        model = Node
        fields = ['assets']
