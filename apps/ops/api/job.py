from celery.task import PeriodicTask
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from common.permissions import IsValidUser
from ops.celery import app
from ops.celery.utils import create_or_update_celery_periodic_tasks
from ops.models import Job, get_object_or_none, JobExecution, CrontabJob
from ops.serializer import JobSerializer, JobExecutionSerializer, CrontabJobSerializer
from ops.tasks import manual_execute_job, interval_execute_job
from orgs.mixins import OrgBulkModelViewSet

__all__ = [
    'JobApiView',
    'JobExecute',
    'JobExecutionViewSet',
    'CrontabJobViewSet'
]


class JobApiView(APIView):
    permission_classes = (IsValidUser,)

    def get(self, request, *args, **kwargs):
        query_set = Job.objects.order_by('-date_created')
        paginator = LimitOffsetPagination()
        page_data = paginator.paginate_queryset(query_set, request)
        data = JobSerializer(page_data, many=True).data
        return paginator.get_paginated_response(data)

    def post(self, request, *args, **kwargs):
        data = request.data
        job = Job.objects.create(name=data.get('name'), description=data.get('description'))
        job.update_tasks(data.get('tasks'))
        job.created_by = self.request.user
        return Response({"status": 'ok'})

    def delete(self, request, *args, **kwargs):
        job = get_object_or_none(Job, id=kwargs.get('pk'))
        if job:
            job.delete()
            return Response({"status": 'ok'})
        else:
            return Response(data={"status": 'fail'}, status=status.HTTP_404_NOT_FOUND)


class JobExecutionViewSet(OrgBulkModelViewSet):
    queryset = JobExecution.objects.all().order_by('-date_execute')
    serializer_class = JobExecutionSerializer
    filter_fields = ('execute_user', 'job')
    search_fields = filter_fields
    ordering_fields = ('date_execute',)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsValidUser,)

    def partial_update(self, request, *args, **kwargs):
        execution = self.get_object()
        app.control.revoke(task_id=str(execution.id), terminate=True)
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class JobExecute(APIView):
    permission_classes = (IsValidUser,)
    allow_methods = ('post',)

    def post(self, request, *args, **kwargs):
        job = get_object_or_none(Job, id=kwargs.get('pk'))
        arguments_data = request.data.get('arguments_data')
        t = manual_execute_job.delay(job, arguments_data, request.user.username)
        return Response({"task": t.id})


class CrontabJobViewSet(OrgBulkModelViewSet):
    queryset = CrontabJob.objects.all().order_by('-date_created')
    serializer_class = CrontabJobSerializer
    filter_fields = ('name',)
    search_fields = filter_fields
    ordering_fields = ('date_created',)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsValidUser,)

    def create_crontab_celery_task(self, detail):
        tasks = {
            detail.name: {
                "task": interval_execute_job.name,
                "crontab": detail.crontab,
                "args": (str(detail.job.id), detail.arguments_data),
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
