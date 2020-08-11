# -*- coding: utf-8 -*-
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination

from common.permissions import IsOrgAdmin, IsValidUser
from common.utils import get_object_or_none
from ops.models import Job, TaskMeta
from ops.serializer import TaskMetaSerializer, JobSerializer
from ..models import TaskPermission
from ..hands import (
    User, UserGroup
)
from .. import serializers

__all__ = [
    'TaskPermissionViewSet',
    'UserGrantedJobsApi',
    'UserGrantedTasksApi',
]


class TaskPermissionViewSet(viewsets.ModelViewSet):
    """
    任务授权列表的增删改查api
    """
    queryset = TaskPermission.objects.all()
    serializer_class = serializers.TaskPermissionCreateUpdateSerializer
    pagination_class = LimitOffsetPagination
    filter_fields = ('name',)
    permission_classes = (IsOrgAdmin,)

    def get_serializer_class(self):
        if self.action in ("list", 'retrieve') and \
                self.request.query_params.get("display"):
            return serializers.TaskPermissionListSerializer
        return self.serializer_class

    def filter_job(self, queryset):
        job_id = self.request.query_params.get('job_id')
        job_name = self.request.query_params.get('job_name')
        if job_id:
            job = get_object_or_none(Job, pk=job_id)
        elif job_name:
            job = get_object_or_none(Job, name=job_name)
        else:
            return queryset
        if not job:
            return queryset.none()
        queryset = queryset.filter(jobs=job)
        return queryset

    def filter_task(self, queryset):
        task_id = self.request.query_params.get('task_id')
        task_name = self.request.query_params.get('task_name')
        if task_id:
            task = get_object_or_none(TaskMeta, pk=task_id)
        elif task_name:
            task = get_object_or_none(TaskMeta, name=task_name)
        else:
            return queryset
        if not task:
            return queryset.none()
        queryset = queryset.filter(tasks=task)
        return queryset

    def filter_user(self, queryset):
        user_id = self.request.query_params.get('user_id')
        username = self.request.query_params.get('username')
        if user_id:
            user = get_object_or_none(User, pk=user_id)
        elif username:
            user = get_object_or_none(User, username=username)
        else:
            return queryset
        if not user:
            return queryset.none()
        queryset = queryset.filter(users=user)
        return queryset

    def filter_user_group(self, queryset):
        user_group_id = self.request.query_params.get('user_group_id')
        user_group_name = self.request.query_params.get('user_group')
        if user_group_id:
            group = get_object_or_none(UserGroup, pk=user_group_id)
        elif user_group_name:
            group = get_object_or_none(UserGroup, name=user_group_name)
        else:
            return queryset
        if not group:
            return queryset.none()
        queryset = queryset.filter(user_groups=group)
        return queryset

    def filter_keyword(self, queryset):
        keyword = self.request.query_params.get('search')
        if not keyword:
            return queryset
        queryset = queryset.filter(name__icontains=keyword)
        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = self.filter_keyword(queryset)
        queryset = self.filter_user(queryset)
        queryset = self.filter_user_group(queryset)
        queryset = self.filter_job(queryset)
        queryset = self.filter_task(queryset)
        return queryset

    def get_queryset(self):
        return self.queryset.all().prefetch_related(
            "tasks", "jobs", "users", "user_groups"
        )


class UserGrantedTasksApi(ListAPIView):
    permission_classes = (IsValidUser,)
    serializer_class = TaskMetaSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        groups = user.groups.all()
        arg = Q(users=user) | Q(user_groups__in=groups)
        return TaskMeta.objects.filter(id__in=TaskPermission.objects.filter(arg).values_list('tasks', flat=True))

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if self.request.query_params.get('search'):
            queryset = queryset.filter(name__contains=self.request.query_params.get('search'))
        return queryset


class UserGrantedJobsApi(ListAPIView):
    permission_classes = (IsValidUser,)
    serializer_class = JobSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        groups = user.groups.all()
        arg = Q(users=user) | Q(user_groups__in=groups)
        return Job.objects.filter(id__in=TaskPermission.objects.filter(arg).values_list('jobs', flat=True))

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if self.request.query_params.get('search'):
            queryset = queryset.filter(name__contains=self.request.query_params.get('search'))
        return queryset
