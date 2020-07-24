# -*- coding: utf-8 -*-
from rest_framework import serializers

from ops.models import Job, JobExecution


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExecution
        fields = '__all__'
