# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import uuid
from django.utils.translation import ugettext_lazy as _
from django.db import models

from common.utils import get_logger

logger = get_logger(__file__)


class TaskArgument(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'), unique=True)
    default_value = models.CharField(max_length=256, verbose_name=_('Default Value'), default='')
    description = models.CharField(max_length=256, verbose_name=_('Description'))
    constraint_regex = models.CharField(max_length=128, verbose_name=_('Constraint Regex'))
    constraint_description = models.CharField(max_length=256, verbose_name=_('Constraint Description'))
    date_created = models.DateTimeField(auto_now_add=True)
