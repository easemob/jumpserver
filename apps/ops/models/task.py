# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import uuid
import json

from celery import current_task
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db import models
from rest_framework.exceptions import ParseError

from common.utils import get_logger
from ops.ansible.arguments import CopyArguments
from ..ansible.runner import CopyRunner
from ..inventory import JMSInventory

logger = get_logger(__file__)


class TaskMeta(models.Model):
    TASK_TYPE_CHOICE = (
        ('file_deploy', '文件分发'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    task_type = models.CharField(choices=TASK_TYPE_CHOICE, max_length=64)
    description = models.CharField(max_length=128, verbose_name=_('Description'))
    crontab = models.CharField(verbose_name=_("Crontab"), null=True, blank=True, max_length=128,
                               help_text=_("5 * * * *"))
    is_periodic = models.BooleanField(default=False)
    created_by = models.CharField(max_length=128, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)

    @property
    def task_info(self):
        if self.task_type == 'file_deploy':
            return FileDeployTask.objects.get(task_meta=self.id)

    @property
    def task_executions(self):
        return TaskExecution.objects.filter(task_meta=self.id)


class BaseTask(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    task_meta = models.ForeignKey('ops.TaskMeta', on_delete=models.CASCADE)
    hosts = models.ManyToManyField('assets.Asset')
    last_modify_user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    date_update = models.DateTimeField(auto_now=True, db_index=True)
    arguments = models.ManyToManyField('ops.TaskArgument')

    @property
    def get_hosts(self):
        return self.hosts.all()

    @property
    def get_arguments(self):
        return self.arguments.all()

    def _validate_arguments_data(self, argument_data):
        # TODO
        validated = True
        if not validated:
            raise ParseError(detail='', code=400)

    def manual_run(self, arguments_data):
        self._validate_arguments_data(arguments_data)

    def get_replaced_arguments(self, value, arguments_data):
        if '$' in value:
            for arg in self.get_arguments:
                value = value.replace('$' + arg.name, arguments_data.get(str(arg.id)))
        return value

    class Meta:
        abstract = True


class TaskExecution(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    task_meta = models.ForeignKey('ops.TaskMeta', related_name='task_execution', on_delete=models.CASCADE)
    execute_user = models.CharField(max_length=128, blank=True, default='system')
    _arguments_data = models.TextField(blank=True, null=True, )
    _result = models.TextField(blank=True, null=True, verbose_name=_('Result'))
    is_finished = models.BooleanField(default=False)
    manual = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_start = models.DateTimeField(null=True)
    date_finished = models.DateTimeField(null=True)

    @property
    def arguments_data(self):
        if self._arguments_data:
            return json.loads(self._arguments_data)
        else:
            return {}

    @property
    def result(self):
        if self._result:
            return json.loads(self._result)
        else:
            return {}

    @result.setter
    def result(self, item):
        self._result = json.dumps(item)

    @arguments_data.setter
    def arguments_data(self, item):
        self._arguments_data = json.dumps(item)

    @property
    def is_success(self):
        if self._result is None or 'Error:' in self._result or self.result.get('error'):
            return False
        return True

    @property
    def timedelta(self):
        if self.is_finished:
            return self.date_finished - self.date_start
        else:
            return 0.0


class FileDeployTask(BaseTask):
    src_file_list = models.TextField()
    run_as = models.ForeignKey('assets.SystemUser', on_delete=models.CASCADE)
    dest = models.CharField(max_length=256)
    mode = models.CharField(max_length=8, verbose_name=_('Mode'))
    group = models.CharField(max_length=64, verbose_name=_('Group'))

    def __str__(self):
        return self.task_meta.name

    @property
    def src_file_list_json(self):
        if self.src_file_list:
            return json.loads(self.src_file_list)
        else:
            return []

    @src_file_list_json.setter
    def src_file_list_json(self, item):
        self.src_file_list = json.dumps(item)

    @property
    def inventory(self):
        return JMSInventory(self.hosts.all(), run_as=self.run_as.username)

    @property
    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in
                FileDeployTask._meta.fields if field.name in ['src_file_list', 'dest', 'mode', 'group']]

    def manual_run(self, arguments_data, execute_user):
        super().manual_run(arguments_data)
        return self.run(arguments_data, execute_user, manual=True)

    def _get_file_args(self, arguments_data):
        files_args = []
        for f in self.src_file_list_json:
            files_args.append(
                CopyArguments(src=super().get_replaced_arguments(f, arguments_data),
                              dest=super().get_replaced_arguments(self.dest, arguments_data),
                              group=super().get_replaced_arguments(self.group, arguments_data),
                              mode=super().get_replaced_arguments(self.mode, arguments_data)))
        print(files_args)
        return files_args

    def run(self, arguments_data, execute_user='system', manual=True):
        print('-' * 10 + ' ' + ugettext('Task start') + ' ' + '-' * 10)
        date_start = timezone.now()
        try:
            hid = current_task.request.id
        except AttributeError:
            hid = str(uuid.uuid4())
        execution = TaskExecution.objects.create(id=hid, execute_user=execute_user, manual=manual,
                                                 task_meta=self.task_meta,
                                                 date_start=date_start)
        execution.arguments_data = arguments_data
        runner = CopyRunner(self.inventory)
        try:
            result = runner.copy(pattern='all', files_args=self._get_file_args(arguments_data))
            execution.result = result.results_command
        except Exception as e:
            print("Error occur: {}".format(e))
            execution.result = {"error": str(e)}
        execution.is_finished = True
        execution.date_finished = timezone.now()
        execution.save()
        print('-' * 10 + ' ' + ugettext('Task end') + ' ' + '-' * 10)
        return execution
