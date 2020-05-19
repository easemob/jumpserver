# ~*~ coding: utf-8 ~*~

from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

from assets.models import SystemUser
from common.mixins import DatetimeSearchMixin
from common.permissions import PermissionsMixin, IsOrgAdmin
from ..models import Task, TaskArgument

__all__ = [
    'FileTaskCreateView',
    'FileTaskListView',
]


class FileTaskListView(PermissionsMixin, DatetimeSearchMixin, TemplateView):
    template_name = 'ops/task_file_deploy_list.html'
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
    template_name = 'ops/task_file_deploy_create.html'
    permission_classes = [IsOrgAdmin]

    def get_system_user(self):
        return SystemUser.objects.all().only('id', 'name')

    def get_task_argument(self):
        return TaskArgument.objects.all().only('id', 'name')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('创建文件分发'),
            'system_user': self.get_system_user(),
            'task_argument': self.get_task_argument()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
