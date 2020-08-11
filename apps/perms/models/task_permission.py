# -*- coding: utf-8 -*-
import uuid
from orgs.mixins import OrgModelMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

__all__ = [
    'TaskPermission',
]


class TaskPermission(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    users = models.ManyToManyField('users.User', blank=True, verbose_name=_("User"))
    user_groups = models.ManyToManyField('users.UserGroup', blank=True, verbose_name=_("User group"))
    tasks = models.ManyToManyField('ops.TaskMeta', blank=True, verbose_name=_("Task"))
    jobs = models.ManyToManyField('ops.Job', blank=True, verbose_name=_("Job"))
    comment = models.TextField(verbose_name=_('Comment'), blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))
