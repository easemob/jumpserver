# ~*~ coding: utf-8 ~*~
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views import View
from django.views.generic import TemplateView, DetailView
from common.mixins import DatetimeSearchMixin
from common.permissions import PermissionsMixin, IsOrgAdmin
from ..models import Job, TaskMeta, JobExecution

__all__ = [
    'JobListView',
    'JobDetailView',
    'JobUpdateView',
    'JobCreateView',
    'JobExecutionHistoryView',
    'JobExecutionDetailView'
]


class JobListView(PermissionsMixin, DatetimeSearchMixin, TemplateView):
    template_name = 'ops/job_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('作业管理'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class JobDetailView(PermissionsMixin, DetailView):
    model = Job
    template_name = 'ops/job_detail.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('作业详情'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class JobCreateView(PermissionsMixin, TemplateView):
    template_name = 'ops/job_create.html'
    permission_classes = [IsOrgAdmin]

    def get_task_meta(self):
        return TaskMeta.objects.all().only('id', 'name', 'task_type')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('创建文件分发'),
            'task_meta': self.get_task_meta()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class JobUpdateView(PermissionsMixin, View):
    permission_classes = [IsOrgAdmin]

    def get(self, request, **kwargs):
        job_meta = Job.objects.get(pk=kwargs.pop('pk'))
        job_type = job_meta.job_type
        if job_type == 'file_deploy':
            return redirect(reverse('ops:file-job-update', kwargs={'pk': str(job_meta.id)}))


class JobExecutionHistoryView(PermissionsMixin, DetailView):
    model = Job
    template_name = 'ops/job_execution_history.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Task run history'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class JobExecutionDetailView(PermissionsMixin, DetailView):
    model = JobExecution
    template_name = 'ops/job_execution_detail.html'
    permission_classes = [IsOrgAdmin]

    def get_task_execution(self):
        return self.get_object().task_execute

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('执行详情'),
            'task_execution': self.get_task_execution()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
