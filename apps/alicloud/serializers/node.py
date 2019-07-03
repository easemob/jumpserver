# -*- coding: utf-8 -*-
from rest_framework import serializers
from assets.models import Node
from ..models import *


class NodeEcsSerializer(serializers.ModelSerializer):
    assets = serializers.PrimaryKeyRelatedField(many=True, queryset=Ecs.objects.all())

    class Meta:
        model = Node
        fields = ['assets']

class NodeSlbSerializer(serializers.ModelSerializer):
    assets = serializers.PrimaryKeyRelatedField(many=True, queryset=Slb.objects.all())

    class Meta:
        model = Node
        fields = ['assets']

class NodeRdsSerializer(serializers.ModelSerializer):
    assets = serializers.PrimaryKeyRelatedField(many=True, queryset=Rds.objects.all())

    class Meta:
        model = Node
        fields = ['assets']

class NodeKvStoreSerializer(serializers.ModelSerializer):
    assets = serializers.PrimaryKeyRelatedField(many=True, queryset=KvStore.objects.all())

    class Meta:
        model = Node
        fields = ['assets']

class NodeOssSerializer(serializers.ModelSerializer):
    assets = serializers.PrimaryKeyRelatedField(many=True, queryset=Oss.objects.all())

    class Meta:
        model = Node
        fields = ['assets']