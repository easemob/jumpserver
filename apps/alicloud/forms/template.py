# -*- coding: utf-8 -*-
#
from django import forms
from django.utils.translation import gettext_lazy as _

from common.utils import get_logger
from orgs.mixins import OrgModelForm

from ..models import EcsTemplate, DISK_CATEGORY

logger = get_logger(__file__)
__all__ = [
    'EcsTemplateCreateForm', 'EcsTemplateUpdateForm',
]

SG_LIST = (
    ('12334ads4234', '北京'),
    ('12334adsshanjh', '杭州'),
)


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
