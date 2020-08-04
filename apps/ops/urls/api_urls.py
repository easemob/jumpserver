# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals

from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = "ops"

router = DefaultRouter()
router.register(r'tasks', api.TaskViewSet, 'task')
router.register(r'adhoc', api.AdHocViewSet, 'adhoc')
router.register(r'history', api.AdHocRunHistoryViewSet, 'history')
router.register(r'command-executions', api.CommandExecutionViewSet, 'command-execution')
bulk_router = BulkRouter()
bulk_router.register(r'tasks-file-deploy', api.FileDeployTaskViewSet, 'task-file-deploy')
bulk_router.register(r'tasks-management', api.TaskManagementViewSet, 'tasks-management')
bulk_router.register(r'crontab-tasks', api.CrontabTaskViewSet, 'crontab-task')
bulk_router.register(r'crontab-job', api.CrontabJobViewSet, 'crontab-job')
bulk_router.register(r'tasks-argument', api.TaskArgumentViewSet, 'task-argument')
bulk_router.register(r'tasks-executions', api.TaskExecutionViewSet, 'task-execution')
bulk_router.register(r'job-executions', api.JobExecutionViewSet, 'job-execution')

urlpatterns = [
    path('tasks/<uuid:pk>/run/', api.TaskRun.as_view(), name='task-run'),
    path('tasks/run', api.TaskExecute.as_view(), name='task-execute'),
    path('celery/task/<uuid:pk>/log/', api.CeleryTaskLogApi.as_view(), name='celery-task-log'),
    path('celery/task/<uuid:pk>/result/', api.CeleryResultApi.as_view(), name='celery-result'),
    path('file/upload/', api.UploadFileApi.as_view(), name='file-upload'),
    path('file/delete/', api.DeleteFileApi.as_view(), name='file-delete'),
    path('job/create/', api.JobApiView.as_view(), name='job-create'),
    path('job/list/', api.JobApiView.as_view(), name='job-list'),
    path('job/<uuid:pk>/run/', api.JobExecute.as_view(), name='job-execute'),
    path('job/<uuid:pk>remove/', api.JobApiView.as_view(), name='job-remove'),
]

urlpatterns += router.urls
urlpatterns += bulk_router.urls
