# -*- coding: utf-8 -*-
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from common.permissions import PermissionsMixin, IsOrgAdmin, IsAuditor


class ArgumentManagerListView(PermissionsMixin, TemplateView):
    template_name = 'ops/task_argument_list.html'
    permission_classes = [IsOrgAdmin | IsAuditor]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Ops'),
            'action': _('变量列表'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
