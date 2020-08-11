# ~*~ coding: utf-8 ~*~

from __future__ import absolute_import, unicode_literals
from django import forms
from django.utils.translation import ugettext_lazy as _

from orgs.mixins import OrgModelForm
from orgs.utils import current_org
from assets.models import Asset, Node
from perms.models import TaskPermission

__all__ = [
    'TaskPermissionForm',
]


class TaskPermissionForm(OrgModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users_field = self.fields.get('users')
        users_field.queryset = current_org.get_org_users()

    class Meta:
        model = TaskPermission
        exclude = (
            'id', 'date_created', 'created_by', 'org_id'
        )
        widgets = {
            'users': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _("User")}
            ),
            'user_groups': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _("User group")}
            ),
            'tasks': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _("Task")}
            ),
            'jobs': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _("Job")}
            ),
            'nodes': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _("Node")}
            ),
            'system_users': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _('System user')}
            ),
        }
        labels = {
            'nodes': _("Node"),
        }

    def clean_user_groups(self):
        users = self.cleaned_data.get('users')
        user_groups = self.cleaned_data.get('user_groups')

        if not users and not user_groups:
            raise forms.ValidationError(
                _("User or group at least one required"))
        return self.cleaned_data["user_groups"]
