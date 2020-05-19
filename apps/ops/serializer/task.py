# -*- coding: utf-8 -*-
from rest_framework import serializers
from ops.models import TaskMeta, TaskExecution


class TaskMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskMeta
        fields = '__all__'


class TaskExecutionSerializer(serializers.ModelSerializer):
    is_success = serializers.SerializerMethodField(read_only=True)
    timedelta = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TaskExecution
        fields = '__all__'

    @staticmethod
    def get_is_success(obj):
        return obj.is_success

    @staticmethod
    def get_timedelta(obj):
        return obj.timedelta
