# -*- coding: utf-8 -*-
from rest_framework import serializers
from ops.models import TaskMeta, FileDeployTask
from ops.serializer import TaskArgumentSerializer, TaskMetaSerializer


class FileDeployTaskSerializer(serializers.ModelSerializer):
    task_meta = TaskMetaSerializer(many=False)

    def create(self, validated_data):
        task_meta_data = validated_data.pop('task_meta')
        task_meta = TaskMeta.objects.create(**task_meta_data)
        arguments = validated_data.pop('arguments')
        hosts = validated_data.pop('hosts')
        file_task = FileDeployTask.objects.create(task_meta=task_meta, **validated_data)
        file_task.arguments.set(arguments)
        file_task.hosts.set(hosts)
        return file_task

    class Meta:
        model = FileDeployTask
        fields = '__all__'
