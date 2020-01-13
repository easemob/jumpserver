# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import json

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormMixin
from alicloud.ali_utils import EcsClient, RosClient
from alicloud.forms import EcsTemplateCreateForm
from alicloud.forms.template import RosTemplateCreateForm, RosStackCreateForm
from alicloud.models import EcsTemplate, StackCreateRecord
from assets.models import Node
from django.shortcuts import render, redirect
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


class RosTemplate(TemplateView):
    template_name = 'alicloud/ros_template.html'

    def get_context_data(self, **kwargs):
        Node.root()
        context = {
            'app': _('Ros'),
            'action': _('Ros list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class RosTeplateCreateView(FormMixin, TemplateView):
    model = RosTemplate
    form_class = RosTemplateCreateForm
    template_name = 'alicloud/ros_template_create.html'
    success_url = reverse_lazy('alicloud:alicloud-template-ros-list')

    def get_context_data(self, **kwargs):
        ros = RosClient()
        context = {
            'app': _('Ros'),
            'action': _('Create Ros Template'),
            'region_list': ros.query_region()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class RosStackCreateView(FormMixin, TemplateView):
    template_name = 'alicloud/ros_stack_create.html'
    form_class = RosStackCreateForm
    success_url = reverse_lazy('alicloud:alicloud-template-ros-list')

    def get_context_data(self, **kwargs):
        ros = RosClient()
        context = {
            'app': _('Ros'),
            'action': _('Create Ros Template'),
            'region_list': ros.query_region()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(rid=self.kwargs.get('pk'), **self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            data = form.data.dict()
            data.pop('csrfmiddlewaretoken')
            params = data.copy()
            ros_client = RosClient(data.pop('region'))
            results = {}
            try:
                results = ros_client.create_stack(data.pop('StackName'), data.pop('TemplateBody'), data)
                StackCreateRecord.objects.create(uid=request.user.username, params=json.dumps(params), results=results)
            except Exception as e:
                msg = str(e)
                messages.warning(request, msg)
                context = self.get_context_data()
                context.update({"form": form})
                return render(request, self.template_name, context)
            msg = f"Create Stack successfully:{results}"
            messages.success(request, msg)
            return redirect('alicloud:alicloud-template-ros-list')
        else:
            context = self.get_context_data()
            context.update({"form": form})
            return render(request, self.template_name, context)
