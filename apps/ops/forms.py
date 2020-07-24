# -*- coding: utf-8 -*-
#
from django import forms

from assets.models import SystemUser
from orgs.mixins import OrgModelForm
from .models import CommandExecution, Job, JobTask


class CommandExecutionForm(forms.ModelForm):
    class Meta:
        model = CommandExecution
        fields = ['run_as', 'command']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        run_as_field = self.fields.get('run_as')
        run_as_field.queryset = SystemUser.objects.all()


class JobCreateForm(OrgModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Job
        fields = [
            'name', 'description'
        ]


class JobTaskForm(OrgModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = JobTask
        fields = [
            'task_meta', 'job'
        ]



