# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import uuid
import json

from celery.result import allow_join_result
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.db import models

from common.utils import get_logger, get_object_or_none
from ops.models import TaskExecution, TaskMeta
from celery import group

logger = get_logger(__file__)


class JobTask(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    task_meta = models.ManyToManyField('ops.TaskMeta')
    job = models.CharField(max_length=64)
    success_next_job_task_id = models.CharField(max_length=64, null=True, default=None)
    failure_next_job_task_id = models.CharField(max_length=64, null=True, default=None)

    @property
    def success_next_job_task(self):
        return get_object_or_none(JobTask, id=self.success_next_job_task_id)

    @property
    def failure_next_job_task(self):
        return get_object_or_none(JobTask, id=self.failure_next_job_task_id)


class JobExecution(models.Model):
    EXECUTION_STATE = (
        ('executing', '正在执行'),
        ('finish', '完成'),
        ('cancel', '取消')
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    job = models.ForeignKey('ops.Job', on_delete=models.CASCADE)
    state = models.CharField(choices=EXECUTION_STATE, max_length=32)
    execute_user = models.CharField(max_length=128, blank=True, default='system')
    date_execute = models.DateTimeField(auto_now_add=True)
    _task_execute_id = models.TextField()
    _arguments_data = models.TextField(blank=True, null=True, )

    @property
    def arguments_data(self):
        if self._arguments_data:
            return json.loads(self._arguments_data)
        else:
            return {}

    @arguments_data.setter
    def arguments_data(self, item):
        self._arguments_data = json.dumps(item)

    @property
    def task_execute_id(self):
        if self._task_execute_id:
            return json.loads(self._task_execute_id)
        else:
            return []

    @property
    def task_execute(self):
        result = []
        for ids in self.task_execute_id:
            result.append(
                [{'name': e.task_meta.name, 'id': str(e.id), 'is_success': e.is_success, 'date_start': e.date_start,
                  'timedelta': round(e.timedelta.total_seconds(), 2)} for e in
                 TaskExecution.objects.filter(id__in=ids)])
        return result

    def add_task_execute_id(self, id_list):
        task_ids = self.task_execute_id
        task_ids.append(id_list)
        self._task_execute_id = json.dumps(task_ids)
        self.save()


class Job(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'), unique=True)
    description = models.CharField(max_length=128, verbose_name=_('Description'))
    crontab = models.CharField(verbose_name=_("Crontab"), null=True, blank=True, max_length=128,
                               help_text=_("5 * * * *"))
    is_periodic = models.BooleanField(default=False)
    created_by = models.CharField(max_length=128, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    start_job_task_id = models.CharField(max_length=64, null=True, default=None)

    @property
    def start_job_task(self):
        return get_object_or_none(JobTask, id=self.start_job_task_id)

    @property
    def all_job_task(self):
        # 现在只管成功的
        all_job_task = []
        next_job_task_job = self.start_job_task_id
        while next_job_task_job:
            job_task = get_object_or_none(JobTask, id=next_job_task_job)
            all_job_task.append(job_task)
            next_job_task_job = job_task.success_next_job_task_id if job_task else None
        return all_job_task

    @property
    def all_task_meta(self):
        all_task_meta = []
        for job_task in self.all_job_task:
            all_task_meta.append(job_task.task_meta.all())
        return all_task_meta

    @property
    def all_task_arguments_unique(self):
        arguments = None
        for task_meta_list in self.all_task_meta:
            for task_meta_id in task_meta_list:
                args = get_object_or_none(TaskMeta, id=str(task_meta_id.id)).task_info.arguments.all()
                if not arguments:
                    arguments = args
                else:
                    arguments.union(args)
        return arguments

    def update_tasks(self, tasks):
        JobTask.objects.filter(job=self).delete()
        job_task_id = None
        tasks.reverse()
        for task_list in tasks:
            new_job_task = JobTask.objects.create(job=str(self.id))
            [new_job_task.task_meta.add(task_id) for task_id in task_list]
            new_job_task.success_next_job_task_id = job_task_id
            new_job_task.save()
            job_task_id = str(new_job_task.id)
        self.start_job_task_id = job_task_id
        self.save()

    def __str__(self):
        return '{0.name}({0.description})'.format(self)


class CrontabJob(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    job = models.ForeignKey('ops.Job', on_delete=models.CASCADE)
    description = models.CharField(max_length=128, verbose_name=_('Description'))
    crontab = models.CharField(verbose_name=_("Crontab"), null=True, blank=True, max_length=128,
                               help_text=_("5 * * * *"))
    enabled = models.BooleanField(default=True)
    created_by = models.CharField(max_length=128, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    _arguments_data = models.TextField(blank=True, null=True, )

    @property
    def arguments_data(self):
        if self._arguments_data:
            return json.loads(self._arguments_data)
        else:
            return {}

    @arguments_data.setter
    def arguments_data(self, item):
        self._arguments_data = json.dumps(item)
