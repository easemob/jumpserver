# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals
from django.urls import path

from .. import views

__all__ = ["urlpatterns"]

app_name = "ops"

urlpatterns = [
    # Resource Task url
    path('task/', views.TaskListView.as_view(), name='task-list'),
    path('task/<uuid:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/<uuid:pk>/info', views.TaskDetailInfoView.as_view(), name='task-detail-info'),
    path('task/<uuid:pk>/update', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<uuid:pk>/adhoc/', views.TaskAdhocView.as_view(), name='task-adhoc'),
    path('task/<uuid:pk>/history/', views.TaskHistoryView.as_view(), name='task-history'),
    path('task/<uuid:pk>/execution/history/', views.TaskExecutionHistoryView.as_view(), name='task-execution-history'),
    path('adhoc/<uuid:pk>/', views.AdHocDetailView.as_view(), name='adhoc-detail'),
    path('adhoc/<uuid:pk>/history/', views.AdHocHistoryView.as_view(), name='adhoc-history'),
    path('adhoc/history/<uuid:pk>/', views.AdHocHistoryDetailView.as_view(), name='adhoc-history-detail'),
    path('celery/task/<uuid:pk>/log/', views.CeleryTaskLogView.as_view(), name='celery-task-log'),

    path('command-execution/', views.CommandExecutionListView.as_view(), name='command-execution-list'),
    path('command-execution/start/', views.CommandExecutionStartView.as_view(), name='command-execution-start'),

    path('task-argument', views.ArgumentManagerListView.as_view(), name='task-argument-list'),
    path('task-management', views.TaskManagementListView.as_view(), name='task-management-list'),
    path('user/tasks/', views.UserTaskListView.as_view(), name='user-task-list'),

    path('file-task/', views.FileTaskListView.as_view(), name='file-task-list'),
    path('file-task/create', views.FileTaskCreateView.as_view(), name='file-task-create'),
    path('file-task/<uuid:pk>/update', views.FileTaskUpdateView.as_view(), name='file-task-update'),

    path('job/', views.JobListView.as_view(), name='job-list'),
    path('job/create', views.JobCreateView.as_view(), name='job-create'),
    path('job/detail/<uuid:pk>', views.JobDetailView.as_view(), name='job-detail'),
    path('job/<uuid:pk>/execution/history/', views.JobExecutionHistoryView.as_view(), name='job-execution-history'),
    path('job/execution/<uuid:pk>/detail/', views.JobExecutionDetailView.as_view(), name='job-execution-detail'),
    path('user/jobs/', views.UserJobView.as_view(), name='user-job-list'),

    path('crontab/job/', views.CronTabJobListView.as_view(), name='cron-job-list'),
    path('crontab/job/<uuid:pk>/create', views.CronTabJobCreateView.as_view(), name='cron-job-create'),
    path('crontab/task/', views.CronTabTaskListView.as_view(), name='cron-task-list'),
    path('task/crontab/<uuid:pk>/create', views.CronTabTaskCreateView.as_view(), name='cron-task-create'),


]
