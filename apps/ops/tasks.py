# coding: utf-8
import os
import subprocess
import datetime
from functools import reduce

from celery.result import allow_join_result
from django.conf import settings
from celery import shared_task, subtask
from celery.exceptions import SoftTimeLimitExceeded
from django.utils import timezone

from common.utils import get_logger, get_object_or_none
from .celery.decorator import (
    register_as_period_task, after_app_shutdown_clean_periodic,
    after_app_ready_start
)
from .celery.utils import create_or_update_celery_periodic_tasks
from .models import Task, CommandExecution, CeleryTask, JobExecution, TaskMeta, Job

logger = get_logger(__file__)


def rerun_task():
    pass


@shared_task
def run_ansible_task(tid, callback=None, **kwargs):
    """
    :param tid: is the tasks serialized data
    :param callback: callback function name
    :return:
    """
    task = get_object_or_none(Task, id=tid)
    if task:
        result = task.run()
        if callback is not None:
            subtask(callback).delay(result, task_name=task.name)
        return result
    else:
        logger.error("No task found")


@shared_task
def manual_execute_task(task, arguments_data, execute_user):
    if task:
        result = task.manual_run(arguments_data, execute_user)
        return result
    else:
        logger.error("No task found")


@shared_task
def interval_execute_task(task_meta_id, arguments_data, execute_user):
    task_meta = get_object_or_none(TaskMeta, id=task_meta_id)
    if task_meta:
        task = task_meta.task_info
        result = task.interval_run(arguments_data, execute_user)
        return result
    else:
        logger.error("No task found")


def execute_job(job, arguments_data, execute_user, task_id):
    job_task = job.start_job_task
    if not job_task:
        return None
    logger.info(task_id)
    tasks = [manual_execute_task.signature((task_meta.task_info, arguments_data, execute_user)) for task_meta in
             job_task.task_meta.all()]
    job_execution = JobExecution.objects.create(id=task_id, job=job, state='executing', arguments_data=arguments_data,
                                                execute_user=execute_user)
    job_execution.save()
    loop_counter = 0
    while len(tasks) > 0 and job_execution.state == 'executing':
        loop_counter += 1
        logger.info('current tasks %s', tasks)
        from celery import group
        with allow_join_result():
            logger.info('begin to execute %s step', loop_counter)
            executions = group(tasks)().get()
        for e in executions:
            logger.info("execution data %s", e)
            logger.info('is success: %s', e.is_success)
        executions_id = [str(exe.id) for exe in executions]
        job_execution.add_task_execute_id(executions_id)
        is_all_success = reduce(lambda x, y: x and y, [exe.is_success for exe in executions])
        logger.info('current step %s execute finished, result is %s', loop_counter, is_all_success)
        if is_all_success and job_task.success_next_job_task_id:
            tasks = [manual_execute_task.signature((task_meta.task_info, arguments_data, execute_user)) for task_meta in
                     job_task.success_next_job_task.task_meta.all()]
            job_task = job_task.success_next_job_task

        elif not is_all_success and job_task.failure_next_job_task_id:
            tasks = [manual_execute_task.signature((task_meta.task_info, arguments_data, execute_user)) for task_meta in
                     job_task.failure_next_job_task.task_meta.all()]
            job_task = job_task.failure_next_job_task
        else:
            tasks = []
            logger.info('no next step, set tasks empty')
        job_execution.refresh_from_db()
        logger.info('job execution current state is %s', job_execution.state)
        if job_execution.state == 'cancel':
            tasks = []
            logger.warning('job is cancel')
    logger.info('job execute finished')
    job_execution.state = 'finish'
    job_execution.save()


@shared_task
def interval_execute_job(job_id, arguments_data):
    job = get_object_or_none(Job, id=job_id)
    if not job:
        logger.error("No job found")
    execute_job(job, arguments_data, 'crontab', interval_execute_job.request.id)


@shared_task
def manual_execute_job(job, arguments_data, execute_user):
    execute_job(job, arguments_data, execute_user, manual_execute_job.request.id)


@shared_task(soft_time_limit=60)
def run_command_execution(cid, **kwargs):
    execution = get_object_or_none(CommandExecution, id=cid)
    if execution:
        try:
            execution.run()
        except SoftTimeLimitExceeded:
            logger.error("Run time out")
    else:
        logger.error("Not found the execution id: {}".format(cid))


@shared_task
@after_app_shutdown_clean_periodic
@register_as_period_task(interval=3600 * 24)
def clean_tasks_adhoc_period():
    logger.debug("Start clean task adhoc and run history")
    tasks = Task.objects.all()
    for task in tasks:
        adhoc = task.adhoc.all().order_by('-date_created')[5:]
        for ad in adhoc:
            ad.history.all().delete()
            ad.delete()


@shared_task
@after_app_shutdown_clean_periodic
@register_as_period_task(interval=3600 * 24)
def clean_celery_tasks_period():
    expire_days = 30
    logger.debug("Start clean celery task history")
    one_month_ago = timezone.now() - timezone.timedelta(days=expire_days)
    tasks = CeleryTask.objects.filter(date_start__lt=one_month_ago)
    for task in tasks:
        if os.path.isfile(task.full_log_path):
            try:
                os.remove(task.full_log_path)
            except (FileNotFoundError, PermissionError):
                pass
        task.delete()
    tasks = CeleryTask.objects.filter(date_start__isnull=True)
    tasks.delete()
    command = "find %s -mtime +%s -name '*.log' -type f -exec rm -f {} \\;" % (
        settings.CELERY_LOG_DIR, expire_days
    )
    subprocess.call(command, shell=True)
    command = "echo > {}".format(os.path.join(settings.LOG_DIR, 'celery.log'))
    subprocess.call(command, shell=True)


@shared_task
@after_app_ready_start
def create_or_update_registered_periodic_tasks():
    from .celery.decorator import get_register_period_tasks
    for task in get_register_period_tasks():
        create_or_update_celery_periodic_tasks(task)


@shared_task
def hello(name, callback=None):
    import time
    time.sleep(10)
    print("Hello {}".format(name))


@shared_task
# @after_app_shutdown_clean_periodic
# @register_as_period_task(interval=30)
def hello123():
    print("{} Hello world".format(datetime.datetime.now().strftime("%H:%M:%S")))
    from celery import group
    with allow_join_result():
        result = group([hello_callback.signature(('421',)), hello_callback.signature(('632',))])().get()
        print(result)
        result = group([hello_callback.signature(('abc',)), hello_callback.signature(('zzz',))])().get()
        print(result)
        return result


@shared_task
def hello_callback(result):
    print(result)
    print("Hello callback")
    return 123
