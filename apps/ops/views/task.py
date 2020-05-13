# ~*~ coding: utf-8 ~*~

from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, ListView

from assets.models import SystemUser
from common.mixins import DatetimeSearchMixin
from common.permissions import PermissionsMixin, IsOrgAdmin
from ops.models.task import FileDeployExecution
from ..models import Task

__all__ = [
    'TaskTemplateListView',
    'FileTaskCreateView',
    'FileTaskListView'
]


class TaskTemplateListView(PermissionsMixin, ListView):
    model = Task
    ordering = ('-date_created',)
    template_name = 'ops/task_template.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('Task list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class FileTaskListView(PermissionsMixin, DatetimeSearchMixin, TemplateView):
    template_name = 'ops/file_task_list.html'
    permission_classes = [IsOrgAdmin]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('文件分发'),
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class FileTaskCreateView(PermissionsMixin, TemplateView):
    model = Task
    template_name = 'ops/file_task_create.html'
    permission_classes = [IsOrgAdmin]

    def get_system_user(self):
        return SystemUser.objects.all().only('id', 'name')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('创建文件分发'),
            'system_user': self.get_system_user()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
