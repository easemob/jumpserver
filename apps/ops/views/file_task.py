# ~*~ coding: utf-8 ~*~
import json

from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, UpdateView
from rest_framework.reverse import reverse_lazy

from assets.models import SystemUser
from common.mixins import DatetimeSearchMixin
from common.permissions import PermissionsMixin, IsOrgAdmin
from ops.serializer import FileDeployTaskSerializer
from ..models import TaskMeta, TaskArgument

__all__ = [
    'FileTaskCreateView',
    'FileTaskListView',
    'FileTaskUpdateView'
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


class FileTaskUpdateView(PermissionsMixin, TemplateView):
    template_name = 'ops/task_file_deploy_update.html'
    success_url = reverse_lazy('ops:task-management-list')
    permission_classes = [IsOrgAdmin]

    def get_system_user(self):
        return SystemUser.objects.all().only('id', 'name')

    def get_task_argument(self):
        return TaskArgument.objects.all().only('id', 'name')

    def get_context_data(self, **kwargs):
        task_meta = TaskMeta.objects.get(id=str(kwargs.pop('pk')))
        task_info = task_meta.task_info
        form_data = {}
        form_data['name'] = task_meta.name
        form_data['description'] = task_meta.description
        form_data['arguments'] = [str(i) for i in task_info.arguments.all().values('id').values_list('id', flat=True)]
        hosts = task_info.hosts.all()
        form_data['hosts'] = [str(i) for i in hosts.values_list('id', flat=True)]
        form_data['hosts_info'] = [{'hostname': h.hostname, 'ip': h.ip} for h in hosts]
        form_data['run_as'] = str(task_info.run_as_id)
        for field in task_info.get_fields:
            form_data[field[0]] = field[1]

        form_data['src_file_list'] = json.loads(form_data['src_file_list'])

        context = {
            'app': _('Ops'),
            'action': _('更新文件分发'),
            'system_user': self.get_system_user(),
            'task_argument': self.get_task_argument(),
            'task_meta': task_meta,
            'task_info': task_info,
            'form_data': form_data
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class FileTaskCreateView(PermissionsMixin, TemplateView):
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
