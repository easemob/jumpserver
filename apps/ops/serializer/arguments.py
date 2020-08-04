# -*- coding: utf-8 -*-
from rest_framework import serializers

from ops.models import TaskArgument


class TaskArgumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskArgument
        fields = '__all__'
