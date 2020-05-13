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
bulk_router.register('tasks-template', api.TaskTemplateViewSet, 'task-template')
bulk_router.register(r'file-deploy-executions', api.FileDeployExecutionViewSet, 'file-deploy-executions')

urlpatterns = [
    path('tasks/<uuid:pk>/run/', api.TaskRun.as_view(), name='task-run'),
    path('celery/task/<uuid:pk>/log/', api.CeleryTaskLogApi.as_view(), name='celery-task-log'),
    path('celery/task/<uuid:pk>/result/', api.CeleryResultApi.as_view(), name='celery-result'),
    path('file/upload/', api.UploadFileApi.as_view(), name='file-upload'),
    path('file/delete/', api.DeleteFileApi.as_view(), name='file-delete')
]

urlpatterns += router.urls
urlpatterns += bulk_router.urls
