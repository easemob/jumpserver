# -*- coding: utf-8 -*-
from rest_framework import serializers
from ops.models import TaskMeta, FileDeployTask
from ops.serializer import TaskMetaSerializer


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

    def update(self, instance, validated_data):
        task_meta_data = validated_data.pop('task_meta')
        task_meta = instance.task_meta
        task_meta.__dict__.update(**task_meta_data)
        task_meta.save()
        arguments = validated_data.pop('arguments')
        hosts = validated_data.pop('hosts')
        instance.__dict__.update(**validated_data)
        instance.arguments.set(arguments)
        instance.hosts.set(hosts)
        return instance

    class Meta:
        model = FileDeployTask
        fields = '__all__'
