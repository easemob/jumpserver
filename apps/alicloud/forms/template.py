# -*- coding: utf-8 -*-
#
import json

from django import forms
from django.utils.translation import gettext_lazy as _
from common.utils import get_logger, get_object_or_none
from orgs.mixins import OrgModelForm

from ..models import EcsTemplate, DISK_CATEGORY, RosTemplate

logger = get_logger(__file__)
__all__ = [
    'EcsTemplateCreateForm', 'EcsTemplateUpdateForm',
]


class EcsTemplateCreateForm(OrgModelForm):
    disk_category = forms.ChoiceField(
        choices=DISK_CATEGORY, label="", initial='cloud_efficiency',
        widget=forms.Select(attrs={'class': 'form-control disk-category'})
    )

    class Meta:
        model = EcsTemplate
        fields = ('nodes', 'admin_user', 'domain')
        widgets = {
            'nodes': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': _('Nodes')
            }),
            'admin_user': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': _('Admin user')
            }),
            'domain': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': _('Domain')
            }),
        }
        labels = {
            'nodes': _("Node"),
        }
        help_texts = {
            'admin_user': _(
                'root or other NOPASSWD sudo privilege user existed in asset,'
                'If asset is windows or other set any one, more see admin user left menu'
            ),
            'domain': _("If your have some network not connect with each other, you can set domain")
        }


class EcsTemplateUpdateForm(OrgModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = EcsTemplate
        exclude = ('id',)
        widgets = {
            'nodes': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': _('Nodes')
            }),
            'admin_user': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': _('Admin user')
            }),
            'domain': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': _('Domain')
            }),
        }
        labels = {
            'nodes': _("Node"),
        }
        help_texts = {
            'admin_user': _(
                'root or other NOPASSWD sudo privilege user existed in asset,'
                'If asset is windows or other set any one, more see admin user left menu'
            ),
            'domain': _("If your have some network not connect with each other, you can set domain")
        }


class RosTemplateCreateForm(OrgModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = RosTemplate
        exclude = ('id', 'org_id', 'region')


class RosStackCreateForm(forms.Form):
    StackName = forms.CharField(label='StackName', strip=True, min_length=2, max_length=128, required=True)

    def __init__(self, rid, *args, **kwargs):
        super().__init__(*args, **kwargs)

        template = get_object_or_none(RosTemplate, id=rid)
        if template:
            body = json.loads(template.body)
            self.fields['TemplateBody'] = forms.CharField(widget=forms.HiddenInput, label='TemplateBody',
                                                          initial=template.body)
            params = body['Parameters']
            for k, v in params.items():
                filed_params = {}
                self.generate_lable(filed_params, k, v)
                self.generate_help_text(filed_params, v)
                self.generate_default_value(filed_params, v)
                filed_type = v.get('Type')
                if filed_type == 'Number':
                    self.handle_integer_type(filed_params, v)
                    self.fields[k] = forms.IntegerField(**filed_params)
                    continue

                if filed_type == 'String':
                    self.handle_string_type(filed_params, v)
                    self.fields[k] = forms.CharField(**filed_params)
                    continue

                if filed_type == 'Boolean':
                    self.fields[k] = forms.BooleanField(**filed_params)
                    continue

    def handle_string_type(self, params, v):
        params['strip'] = True
        min_value = v.get('MinLength')
        max_value = v.get('MaxLength')
        if min_value:
            params['min_length'] = min_value
        if max_value:
            params['max_length'] = max_value
        if v.get('NoEcho'):
            params['widget'] = forms.PasswordInput

    def handle_integer_type(self, params, v):
        min_value = v.get('MinValue')
        max_value = v.get('MaxValue')
        if min_value:
            params['min_value'] = min_value
        if max_value:
            params['max_value'] = max_value

    def generate_lable(self, params, k, v):
        label = v.get('Label')
        label = k if label else label
        params['label'] = label

    def generate_default_value(self, params, v):
        default = v.get('Default')
        if default:
            params['initial'] = default
        else:
            params['required'] = True

    def generate_help_text(self, params, v):
        help_text = v.get('Description')
        constraint_des = v.get('ConstraintDescription')
        if constraint_des:
            help_text = f'{help_text}<span style="color:red">({constraint_des})</span>'
        params['help_text'] = help_text
