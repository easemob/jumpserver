# -*- coding: utf-8 -*-
from rest_framework import serializers

from ops.models import Job, JobExecution, CrontabJob


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExecution
        fields = '__all__'


class CrontabJobSerializer(serializers.ModelSerializer):
    arguments_data = serializers.JSONField()

    class Meta:
        model = CrontabJob
        fields = '__all__'

    @staticmethod
    def get_argument_data(obj):
        return obj.argument_data
