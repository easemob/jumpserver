# -*- coding: utf-8 -*-
from django.utils import timezone
from django_celery_beat.models import PeriodicTask
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsValidUser
from common.utils import get_object_or_none
from ops.celery.utils import create_or_update_celery_periodic_tasks
from ops.models import TaskMeta, TaskExecution, CrontabTask
from ops.serializer import TaskMetaSerializer, TaskExecutionSerializer, CrontabTaskSerializer
from orgs.mixins import OrgBulkModelViewSet
from ops.tasks import manual_execute_task, interval_execute_task

__all__ = [
    'TaskManagementViewSet',
    'TaskExecute',
    'TaskExecutionViewSet',
    'CrontabTaskViewSet'
]


class TaskManagementViewSet(OrgBulkModelViewSet):
    queryset = TaskMeta.objects.all().order_by('-date_created')
    serializer_class = TaskMetaSerializer
    filter_fields = ('name',)
    search_fields = filter_fields
    ordering_fields = ('date_created',)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsValidUser,)
    date_format = '%Y-%m-%d'

    def _date_filter_queryset(self):
        queryset = super().get_queryset()
        date_from_s = self.request.query_params.get('date_from')
        date_to_s = self.request.query_params.get('date_to')
        date_from = date_to = ''
        if date_from_s:
            date_from = timezone.datetime.strptime(date_from_s, self.date_format)
            tz = timezone.get_current_timezone()
            date_from = tz.localize(date_from)

        if date_to_s:
            date_to = timezone.datetime.strptime(
                date_to_s + ' 23:59:59', self.date_format + ' %H:%M:%S'
            )
            date_to = date_to.replace(
                tzinfo=timezone.get_current_timezone()
            )

        if date_from:
            queryset = queryset.filter(date_created__gte=date_from)
        if date_to:
            queryset = queryset.filter(date_created__lte=date_to)
        return queryset

    def _filter_task_type(self, queryset):
        task_type = self.request.query_params.get('task_type')
        if task_type:
            queryset.filter(task_type=self.request.query_params.get('task_type'))
        return queryset

    def _filter_serach(self, queryset):
        search = self.request.query_params.get('search')
        if search:
            queryset.filter(name__contains=search)
        return queryset

    def get_queryset(self):
        queryset = self._date_filter_queryset()
        queryset = self._filter_task_type(queryset)
        return queryset


class TaskExecutionViewSet(OrgBulkModelViewSet):
    queryset = TaskExecution.objects.all().order_by('-date_created')
    serializer_class = TaskExecutionSerializer
    filter_fields = ('execute_user', 'task_meta')
    search_fields = filter_fields
    ordering_fields = ('date_created', 'date_start')
    pagination_class = LimitOffsetPagination
    permission_classes = (IsValidUser,)


class TaskExecute(APIView):
    permission_classes = (IsValidUser,)
    allow_methods = ('post',)

    def post(self, request, *args, **kwargs):
        task_meta = get_object_or_none(TaskMeta, id=request.data.get('task_meta_id'))
        task = task_meta.task_info
        arguments_data = request.data.get('arguments_data')
        t = manual_execute_task.delay(task, arguments_data, request.user.username)
        return Response({"task": t.id})


class CrontabTaskViewSet(OrgBulkModelViewSet):
    queryset = CrontabTask.objects.all().order_by('-date_created')
    serializer_class = CrontabTaskSerializer
    filter_fields = ('name',)
    search_fields = filter_fields
    ordering_fields = ('date_created',)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsValidUser,)

    def create_crontab_celery_task(self, detail):
        tasks = {
            detail.name: {
                "task": interval_execute_task.name,
                "crontab": detail.crontab,
                "args": (str(detail.task_meta.id), detail.arguments_data, 'crontab'),
                "enabled": detail.enabled,
            }
        }
        create_or_update_celery_periodic_tasks(tasks)

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.created_by = self.request.user.username
        instance.save()
        self.create_crontab_celery_task(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.created_by = self.request.user.username
        instance.save()

    def perform_destroy(self, instance):
        periodic_task = get_object_or_none(PeriodicTask, name=instance.name)
        if periodic_task:
            periodic_task.delete()
        instance.delete()
