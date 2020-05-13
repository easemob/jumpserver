# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import uuid
import json

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db import models

from common.utils import get_logger
from ops.ansible.arguments import CopyArguments
from orgs.models import Organization
from ..ansible.runner import CopyRunner
from ..inventory import JMSInventory

logger = get_logger(__file__)


class FileDeployExecution(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    src_file_list = models.TextField()
    hosts = models.ManyToManyField('assets.Asset')
    run_as = models.ForeignKey('assets.SystemUser', on_delete=models.CASCADE)
    dest = models.CharField(max_length=256)
    mode = models.CharField(max_length=8, verbose_name=_('Mode'))
    group = models.CharField(max_length=64, verbose_name=_('Group'))
    _result = models.TextField(blank=True, null=True, verbose_name=_('Result'))
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    is_finished = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(null=True)
    date_finished = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    @property
    def inventory(self):
        return JMSInventory(self.hosts.all(), run_as=self.run_as.username)

    @property
    def result(self):
        if self._result:
            return json.loads(self._result)
        else:
            return {}

    @property
    def src_file_list_json(self):
        if self.src_file_list:
            return json.loads(self.src_file_list)
        else:
            return []

    @src_file_list_json.setter
    def src_file_list_json(self, item):
        self.src_file_list = json.dumps(item)

    @result.setter
    def result(self, item):
        self._result = json.dumps(item)

    @property
    def is_success(self):
        if self._result is None or 'Error:' in self._result:
            return False
        return True

    def get_hosts_names(self):
        return ','.join(self.hosts.all().values_list('hostname', flat=True))

    def run(self):
        print('-' * 10 + ' ' + ugettext('Task start') + ' ' + '-' * 10)
        org = Organization.get_instance(self.run_as.org_id)
        org.change_to()
        self.date_start = timezone.now()
        runner = CopyRunner(self.inventory)
        try:
            files_args = []
            for f in self.src_file_list_json:
                files_args.append(CopyArguments(src=f, dest=self.dest, group=self.group, mode=self.mode)),
            result = runner.copy(pattern='all', files_args=files_args)
            self.result = result.results_command
        except Exception as e:
            print("Error occur: {}".format(e))
            self.result = {"error": str(e)}
        self.is_finished = True
        self.date_finished = timezone.now()
        self.save()
        print('-' * 10 + ' ' + ugettext('Task end') + ' ' + '-' * 10)
        return self.result
