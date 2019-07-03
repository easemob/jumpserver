# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from assets.models import Node, Label
from common.permissions import AdminUserRequiredMixin


class SlbListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'alicloud/slb_list.html'

    def get_context_data(self, **kwargs):
        Node.root()
        context = {
            'app': _('Assets'),
            'action': _('Asset list'),
            'labels': Label.objects.all().order_by('name'),
            'nodes': Node.objects.all().order_by('-key'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
