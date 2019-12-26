# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormMixin
from alicloud.ali_utils import EcsClient
from alicloud.forms import EcsTemplateCreateForm
from alicloud.models import EcsTemplate
from assets.models import Node, Label
from common.permissions import PermissionsMixin, IsValidUser


class EcsTemplateListView(TemplateView):
    template_name = 'alicloud/ecs_template.html'

    def get_context_data(self, **kwargs):
        Node.root()
        context = {
            'app': _('Ecs'),
            'action': _('Ecs list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class EcsTeplateCreateView(FormMixin, TemplateView):
    model = EcsTemplate
    form_class = EcsTemplateCreateForm
    template_name = 'alicloud/ecs_template_create.html'
    success_url = reverse_lazy('alicloud:alicloud-template-ecs-list')

    def get_context_data(self, **kwargs):
        ecs = EcsClient()
        context = {
            'app': _('Assets'),
            'action': _('Create asset'),
            'region_list': ecs.query_region()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class EcsTeplateDetailView(PermissionsMixin, DetailView):
    model = EcsTemplate
    context_object_name = 'ecs_template'
    template_name = 'alicloud/ecs_template_detail.html'
    permission_classes = [IsValidUser]

    # def get_queryset(self):
    #     return super().get_queryset().prefetch_related(
    #         "nodes",
    #     ).select_related('admin_user', 'domain')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Template'),
            'action': _('Template detail'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SlbTemplate(TemplateView):
    template_name = 'alicloud/slb_template.html'

    def get_context_data(self, **kwargs):
        Node.root()
        context = {
            'app': _('Slb'),
            'action': _('Slb list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
