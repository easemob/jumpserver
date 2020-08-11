# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.utils.translation import ugettext as _
from assets.models import Node
from common.permissions import PermissionsMixin, IsOrgAdmin
from ops.models import TaskMeta, Job
from perms.forms.task_permission import TaskPermissionForm
from perms.models import TaskPermission


class TaskPermissionListView(PermissionsMixin, TemplateView):
    template_name = 'perms/task_permission_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Perms'),
            'action': _('Task permission list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class TaskPermissionCreateView(PermissionsMixin, CreateView):
    model = TaskPermission
    form_class = TaskPermissionForm
    template_name = 'perms/task_permission_create_update.html'
    success_url = reverse_lazy('perms:task-permission-list')
    permission_classes = [IsOrgAdmin]

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        nodes_id = self.request.GET.get("nodes")
        tasks_id = self.request.GET.get("tasks")
        jobs_id = self.request.GET.get("job")
        if nodes_id:
            nodes_id = nodes_id.split(",")
            nodes = Node.objects.filter(id__in=nodes_id).exclude(id=Node.root().id)
            form['nodes'].initial = nodes
        if tasks_id:
            tasks_id = tasks_id.split(",")
            tasks = TaskMeta.objects.filter(id__in=tasks_id)
            form['tasks'].initial = tasks
        if jobs_id:
            jobs_id = jobs_id.split(",")
            job = Job.objects.filter(id__in=jobs_id)
            form['jobs'].initial = job
        return form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Perms'),
            'action': _('创建任务权限'),
            'api_action': "create",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AssetPermissionUpdateView(PermissionsMixin, UpdateView):
    model = TaskPermission
    form_class = TaskPermissionForm
    template_name = 'perms/task_permission_create_update.html'
    success_url = reverse_lazy("perms:task-permission-list")
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Perms'),
            'action': _('更新任务权限'),
            'api_action': "update",
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)