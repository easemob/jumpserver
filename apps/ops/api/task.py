# -*- coding: utf-8 -*-
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from common.mixins import DatetimeSearchMixin
from common.permissions import IsOrgAdminOrAppUser, IsValidUser
from ops.models import Task
from ops.models.task import FileDeployExecution
from ops.serializers import TaskSerializer, FileDeployExecutionSerializer
from orgs.mixins import OrgBulkModelViewSet
from ops.tasks import run_file_deploy_execution

__all__ = [
    'TaskTemplateViewSet',
    'FileDeployExecutionViewSet'
]


class TaskTemplateViewSet(OrgBulkModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_fields = ('name',)
    search_fields = filter_fields
    ordering_fields = ('-date_created',)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsOrgAdminOrAppUser,)


class FileDeployExecutionViewSet(OrgBulkModelViewSet):
    queryset = FileDeployExecution.objects.all()
    serializer_class = FileDeployExecutionSerializer
    filter_fields = ('name',)
    search_fields = filter_fields
    ordering_fields = ('-date_created')
    pagination_class = LimitOffsetPagination
    permission_classes = (IsValidUser,)
    date_format = '%Y-%m-%d'

    def _get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.query_params.get('user')
        date_from_s = self.request.query_params.get('date_from')
        date_to_s = self.request.query_params.get('date_to')
        date_from = date_to = ''
        if date_from_s:
            date_from = timezone.datetime.strptime(date_from_s, self.date_format)
            tz = timezone.get_current_timezone()
            date_from = tz.localize(date_from)
        else:
            date_from = timezone.now() - timezone.timedelta(7)

        if date_to_s:
            date_to = timezone.datetime.strptime(
                date_to_s + ' 23:59:59', self.date_format + ' %H:%M:%S'
            )
            date_to = date_to.replace(
                tzinfo=timezone.get_current_timezone()
            )
        else:
            date_to = timezone.now()
        if date_from:
            queryset = queryset.filter(date_start__gte=date_from)
        if date_to:
            queryset = queryset.filter(date_start__lte=date_to)
        if user:
            queryset = queryset.filter(user=user)
        return queryset

    def get_queryset(self):
        queryset = self._get_queryset()
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.user = self.request.user
        instance.save()
        transaction.on_commit(lambda: run_file_deploy_execution.apply_async(
            args=(instance.id,), task_id=str(instance.id)
        ))