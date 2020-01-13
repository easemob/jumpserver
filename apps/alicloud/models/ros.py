# -*- coding: utf-8 -*-
import uuid
from orgs.mixins import OrgModelMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class StackCreateRecord(OrgModelMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    params = models.TextField()
    uid = models.CharField(max_length=256)
    results = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))
