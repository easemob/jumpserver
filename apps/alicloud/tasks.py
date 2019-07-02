# ~*~ coding: utf-8 ~*~
import json
from celery import shared_task
from django.db import transaction

from alicloud.models.ecs import Ecs
from assets.models import Node
from .utils import AliCloudUtil
from common.utils import get_logger, get_object_or_none

logger = get_logger(__file__)


@shared_task
def sync_ecs_list_info_manual():
    logger.info('ready to sync aly cloud ecs list')
    ali_util = AliCloudUtil()
    result = ali_util.get_ecs_instances()
    created, updated, failed = [], [], []
    node = Node.root()
    for info in result:
        logger.info(json.dumps(info))
        Ecs.objects.all().update(status='Destory')
        ecs = get_object_or_none(Ecs, instance_id=info.get('instance_id'))
        if not ecs:
            try:
                with transaction.atomic():
                    ecs = Ecs.objects.create(**info)
                    # need to add auto join node
                    ecs.nodes.set([node])
                    created.append(info['instance_name'])
            except Exception as e:
                failed.append('%s: %s' % (info['instance_name'], str(e)))
        else:
            for k, v in info.items():
                if v != '':
                    setattr(ecs, k, v)
            try:
                ecs.save()
                updated.append(info['instance_name'])
            except Exception as e:
                failed.append('%s: %s' % (info['instance_name'], str(e)))

    data = {
        'created': created,
        'created_info': 'Created {}'.format(len(created)),
        'updated': updated,
        'updated_info': 'Updated {}'.format(len(updated)),
        'failed': failed,
        'failed_info': 'Failed {}'.format(len(failed)),
        'valid': True,
        'msg': 'Created: {}. Updated: {}, Error: {}'.format(
            len(created), len(updated), len(failed))
    }
    logger.info('sync finish')
    logger.info(json.dumps(data))
    return data


@shared_task
def sync_slb_list_info_manual():
    logger.info('ready to sync aly cloud ecs list')
    ali_util = AliCloudUtil()
    result = ali_util.get_ecs_instances()
    created, updated, failed = [], [], []
    node = Node.root()
    for info in result:
        logger.info(json.dumps(info))
        Ecs.objects.all().update(status='Destory')
        ecs = get_object_or_none(Ecs, instance_id=info.get('instance_id'))
        if not ecs:
            try:
                with transaction.atomic():
                    ecs = Ecs.objects.create(**info)
                    # need to add auto join node
                    ecs.nodes.set([node])
                    created.append(info['instance_name'])
            except Exception as e:
                failed.append('%s: %s' % (info['instance_name'], str(e)))
        else:
            for k, v in info.items():
                if v != '':
                    setattr(ecs, k, v)
            try:
                ecs.save()
                updated.append(info['instance_name'])
            except Exception as e:
                failed.append('%s: %s' % (info['instance_name'], str(e)))

    data = {
        'created': created,
        'created_info': 'Created {}'.format(len(created)),
        'updated': updated,
        'updated_info': 'Updated {}'.format(len(updated)),
        'failed': failed,
        'failed_info': 'Failed {}'.format(len(failed)),
        'valid': True,
        'msg': 'Created: {}. Updated: {}, Error: {}'.format(
            len(created), len(updated), len(failed))
    }
    logger.info('sync finish')
    logger.info(json.dumps(data))
    return data
