# ~*~ coding: utf-8 ~*~
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic import TemplateView, DetailView
from common.mixins import DatetimeSearchMixin
from common.permissions import PermissionsMixin, IsOrgAdmin, IsValidUser
from ..models import Task, TaskMeta

__all__ = [
    'TaskManagementListView',
    'TaskDetailInfoView',
    'TaskExecutionHistoryView',
    'TaskUpdateView',
    'CronTabTaskListView',
    'CronTabTaskCreateView',
    'UserTaskListView'
]


class TaskManagementListView(PermissionsMixin, TemplateView):
    template_name = 'ops/task_management_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('任务管理'),
            'task_type': TaskMeta.TASK_TYPE_CHOICE,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserTaskListView(PermissionsMixin, TemplateView):
    template_name = 'ops/user_task_list.html'
    permission_classes = [IsValidUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('任务查看'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskDetailInfoView(PermissionsMixin, DetailView):
    model = TaskMeta
    template_name = 'ops/task_detail_info.html'
    permission_classes = [IsValidUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Task detail'),
            'task_info': self.get_object().task_info
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskExecutionHistoryView(PermissionsMixin, DetailView):
    model = TaskMeta
    template_name = 'ops/task_execution_history.html'
    permission_classes = [IsValidUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Task run history'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskUpdateView(PermissionsMixin, View):
    permission_classes = [IsOrgAdmin]

    def get(self, request, **kwargs):
        task_meta = TaskMeta.objects.get(pk=kwargs.pop('pk'))
        task_type = task_meta.task_type
        if task_type == 'file_deploy':
            return redirect(reverse('ops:file-task-update', kwargs={'pk': str(task_meta.id)}))


class CronTabTaskListView(PermissionsMixin, TemplateView):
    template_name = 'ops/crontab_task_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('定时任务管理'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class CronTabTaskCreateView(PermissionsMixin, DetailView):
    template_name = 'ops/crontab_task_create.html'
    permission_classes = [IsOrgAdmin]
    model = TaskMeta

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('定时任务创建'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
