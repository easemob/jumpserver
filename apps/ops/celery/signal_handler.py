# -*- coding: utf-8 -*-
#
import logging

from django.core.cache import cache
from celery import subtask
from celery.signals import (
    worker_ready, worker_shutdown, after_setup_logger
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from kombu.utils.encoding import safe_str
from django_celery_beat.models import PeriodicTask

from common.utils import get_logger, get_object_or_none
from ops.models import CrontabTask, CrontabJob
from .decorator import get_after_app_ready_tasks, get_after_app_shutdown_clean_tasks
from .logger import CeleryTaskFileHandler

logger = get_logger(__file__)
safe_str = lambda x: x


@worker_ready.connect
def on_app_ready(sender=None, headers=None, **kwargs):
    if cache.get("CELERY_APP_READY", 0) == 1:
        return
    cache.set("CELERY_APP_READY", 1, 10)
    tasks = get_after_app_ready_tasks()
    logger.debug("Work ready signal recv")
    logger.debug("Start need start task: [{}]".format(", ".join(tasks)))
    for task in tasks:
        subtask(task).delay()


@worker_shutdown.connect
def after_app_shutdown_periodic_tasks(sender=None, **kwargs):
    if cache.get("CELERY_APP_SHUTDOWN", 0) == 1:
        return
    cache.set("CELERY_APP_SHUTDOWN", 1, 10)
    tasks = get_after_app_shutdown_clean_tasks()
    logger.debug("Worker shutdown signal recv")
    logger.debug("Clean period tasks: [{}]".format(', '.join(tasks)))
    PeriodicTask.objects.filter(name__in=tasks).delete()


@after_setup_logger.connect
def add_celery_logger_handler(sender=None, logger=None, loglevel=None, format=None, **kwargs):
    if not logger:
        return
    task_handler = CeleryTaskFileHandler()
    task_handler.setLevel(loglevel)
    formatter = logging.Formatter(format)
    task_handler.setFormatter(formatter)
    logger.addHandler(task_handler)


@receiver(post_save, sender=CrontabTask, dispatch_uid="my_unique_identifier")
def on_crontab_task_create_or_update(sender, instance=None, created=False, **kwargs):
    if not created:
        logger.info("Cron task `{}` create signal received".format(instance.name))
        periodic_task = get_object_or_none(PeriodicTask, name=instance.name)
        if periodic_task:
            periodic_task.enabled = instance.enabled
            periodic_task.save()
        logger.info("Cron task `{}` enabled turn to {}".format(instance, instance.enabled))


@receiver(post_save, sender=CrontabJob, dispatch_uid="my_unique_identifier")
def on_crontab_job_create_or_update(sender, instance=None, created=False, **kwargs):
    if not created:
        logger.info("Cron job `{}` create signal received".format(instance.name))
        periodic_task = get_object_or_none(PeriodicTask, name=instance.name)
        if periodic_task:
            periodic_task.enabled = instance.enabled
            periodic_task.save()
        logger.info("Cron job `{}` enabled turn to {}".format(instance, instance.enabled))
