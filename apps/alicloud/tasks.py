# ~*~ coding: utf-8 ~*~
import json

from celery import shared_task
from django.db import transaction

from ops.celery.decorator import register_as_period_task
from .models import *
from assets.models import Node, Asset
from .utils import AliCloudUtil
from common.utils import get_logger, get_object_or_none
from django.conf import settings

logger = get_logger(__file__)


@shared_task
@register_as_period_task(interval=3600*24)
def sync_ecs_list_info_manual():
    logger.info('ready to sync aly cloud ecs list')
    ali_util = AliCloudUtil()
    result = ali_util.get_ecs_instances()
    created, updated, failed = [], [], []
    j_created, j_updated, j_failed = [], [], []
    node = Node.root()
    Ecs.objects.all().update(status='Destory')
    for info in result:
        logger.info(json.dumps(info))
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

        if settings.AUTO_UPDATE_JUMPSERVER_ASSETS:
            asset = get_object_or_none(Asset, number=info.get('instance_id'))
            if not asset:
                try:
                    with transaction.atomic():
                        hostname = info.get('instance_name')
                        domain = None
                        admin_user = None
                        if settings.ENVIROMENT == 'PROD':
                            if 'ebs' in hostname:
                                domain = 'ebs'
                                admin_user = 'ebs-console'
                            elif 'vip6' in hostname:
                                domain = 'vip6'
                                admin_user = 'vip6-console'
                            elif 'hsb' in hostname:
                                domain = 'hsb'
                                admin_user = 'hsb-console'
                            elif 'vip5' in hostname:
                                domain = 'vip5'
                                admin_user = 'vip6-console'
                            elif 'usa' in hostname:
                                domain = 'osu'
                                admin_user = 'usa-console'
                            else:
                                domain = None
                                admin_user = None
                        attr = {
                            'number': 'instance_id',
                            'ip': info.get('inner_ip'),
                            'port': 3299,
                            'hostname': hostname,
                            'platform': 'Linux',
                            'domain': domain,
                            'admin_user': admin_user
                        }
                        asset = Asset.objects.create(**attr)
                        # need to add auto join node
                        asset.nodes.set([node])
                        j_created.append(info['instance_name'])
                except Exception as e:
                    j_failed.append('%s: %s' % (info['instance_name'], str(e)))
            else:
                setattr(ecs, 'hostname', info.get('hostname'))
                try:
                    asset.save()
                    j_updated.append(info['instance_name'])
                except Exception as e:
                    j_failed.append('%s: %s' % (info['instance_name'], str(e)))
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
    logger.info('ecs sync finish')
    logger.info(json.dumps(data))
    j_data = {
        'created': j_created,
        'created_info': 'Created {}'.format(len(j_created)),
        'updated': j_updated,
        'updated_info': 'Updated {}'.format(len(j_updated)),
        'failed': j_failed,
        'failed_info': 'Failed {}'.format(len(j_failed)),
        'valid': True,
        'msg': 'Created: {}. Updated: {}, Error: {}'.format(
            len(j_created), len(j_updated), len(j_failed))
    }
    logger.info('jump server asset update finish')
    logger.info(json.dumps(j_data))

    return data


@shared_task
@register_as_period_task(interval=3600*24)
def sync_slb_list_info_manual():
    logger.info('ready to sync aly cloud slb list')
    ali_util = AliCloudUtil()
    result = ali_util.get_slb_instances()
    created, updated, failed = [], [], []
    node = Node.root()
    Slb.objects.all().update(status='Destory')
    for info in result:
        logger.info(json.dumps(info))
        slb = get_object_or_none(Slb, instance_id=info.get('instance_id'))
        if not slb:
            try:
                with transaction.atomic():
                    slb = Slb.objects.create(**info)
                    # need to add auto join node
                    slb.nodes.set([node])
                    created.append(info['instance_name'])
            except Exception as e:
                failed.append('%s: %s' % (info['instance_name'], str(e)))
        else:
            for k, v in info.items():
                if v != '':
                    setattr(slb, k, v)
            try:
                slb.save()
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
@register_as_period_task(interval=3600*24)
def sync_rds_list_info_manual():
    logger.info('ready to sync aly cloud rds list')
    ali_util = AliCloudUtil()
    result = ali_util.get_rds_instances()
    created, updated, failed = [], [], []
    node = Node.root()
    Rds.objects.all().update(status='Destory')
    for info in result:
        logger.info(json.dumps(info))
        rds = get_object_or_none(Rds, instance_id=info.get('instance_id'))
        if not rds:
            try:
                with transaction.atomic():
                    rds = Rds.objects.create(**info)
                    # need to add auto join node
                    rds.nodes.set([node])
                    created.append(info['instance_name'])
            except Exception as e:
                failed.append('%s: %s' % (info['instance_name'], str(e)))
        else:
            for k, v in info.items():
                if v != '':
                    setattr(rds, k, v)
            try:
                rds.save()
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
@register_as_period_task(interval=3600*24)
def sync_kvstore_list_info_manual():
    logger.info('ready to sync aly cloud kvstore list')
    ali_util = AliCloudUtil()
    result = ali_util.get_kvstore_instances()
    created, updated, failed = [], [], []
    node = Node.root()
    KvStore.objects.all().update(status='Destory')
    for info in result:
        logger.info(json.dumps(info))
        kvstore = get_object_or_none(KvStore, instance_id=info.get('instance_id'))
        if not kvstore:
            try:
                with transaction.atomic():
                    kvstore = KvStore.objects.create(**info)
                    # need to add auto join node
                    kvstore.nodes.set([node])
                    created.append(info['instance_name'])
            except Exception as e:
                failed.append('%s: %s' % (info['instance_name'], str(e)))
        else:
            for k, v in info.items():
                if v != '':
                    setattr(kvstore, k, v)
            try:
                kvstore.save()
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
@register_as_period_task(interval=3600*24)
def sync_oss_list_info_manual():
    logger.info('ready to sync aly cloud oss list')
    ali_util = AliCloudUtil()
    result = ali_util.get_oss_instances()
    created, updated, failed = [], [], []
    node = Node.root()
    Oss.objects.all().update(status='Destory')
    for info in result:
        logger.info(json.dumps(info))
        oss = get_object_or_none(Oss, instance_id=info.get('instance_id'))
        if not oss:
            try:
                with transaction.atomic():
                    oss = Oss.objects.create(**info)
                    # need to add auto join node
                    oss.nodes.set([node])
                    created.append(info['instance_name'])
            except Exception as e:
                failed.append('%s: %s' % (info['instance_name'], str(e)))
        else:
            for k, v in info.items():
                if v != '':
                    setattr(oss, k, v)
            try:
                oss.save()
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
@register_as_period_task(interval=3600*24)
def sync_billing_info_manual(begin_time=None, end_time=None):
    logger.info('ready to sync aly cloud billing list')
    logger.info(f'同步订单区间为: {begin_time}______{end_time}')

    ali_util = AliCloudUtil()

    orders_num = 0  # 订单条数
    orders_details_num = 0  # 订单详情条数
    sync_success_orders = []
    sync_error_orders = {}
    sync_skip_orders = {}

    for orders in ali_util.get_orders_list(begin_time, end_time):
        logger.info(json.dumps(orders))
        orders_info = orders["Data"]["OrderList"]["Order"]
        for i in orders_info:
            order_summary = i
            order_id = order_summary['OrderId']
            if order_summary["PaymentStatus"] != "Paid":
                info = f"error {order_id}, 订单状态未支付, 跳过"
                logger.info(info)
                sync_skip_orders[order_id] = info

            elif order_summary["PretaxGrossAmount"] == 0.0:
                info = f"error {order_id}, 交易金额为0, 跳过"
                logger.info(info)
                sync_skip_orders[order_id] = info

            elif order_summary.get("PretaxGrossAmount") is None:
                info = f"error {order_id}, 错误订单, 没有类型"
                logger.info(info)
                sync_skip_orders[order_id] = info

            else:
                try:
                    details = ali_util.get_orders_details(order_id)
                    infos = details["Data"]["OrderList"]["Order"]
                    table_row_num = 0
                    for d in infos:
                        instance_ids = json.loads(d['InstanceIDs'])
                        for f in instance_ids:
                            f_payment_amount = d['PretaxAmount'] % len(instance_ids)
                            f_payment_gross_amount = d['PretaxAmount'] % len(instance_ids)
                            row_data = {
                                'product_code': d['ProductCode'],
                                'order_id': d['OrderId'],
                                'order_id_index': table_row_num,
                                'payment_status': d['PaymentStatus'],
                                'payment_time': d['PaymentTime'],
                                'order_type': d['OrderType'],
                                'create_time': d['CreateTime'],
                                'payment_gross_amount': f_payment_gross_amount,
                                'payment_amount': f_payment_amount,
                                'instance_ids': f,
                            }
                            sd = Billing.objects.filter(order_id=d['OrderId'], order_id_index=table_row_num).count()
                            if sd > 0:
                                logger.info(f"重复录入 {d['OrderId']}")
                                break

                            Billing.objects.create(**row_data)
                            table_row_num += 1
                        orders_details_num += 1
                    orders_num += 1
                    sync_success_orders.append(order_id)
                    logger.info(f"ok {order_id}")
                except Exception as e:
                    err = f"error {order_id} => {e}"
                    sync_error_orders['order_id'] = err
                    logger.error(err)

    data = {
        'orders_numbers': orders_num,
        'sync_error_orders': sync_error_orders,
        'sync_skip_orders': sync_skip_orders,
        'sync_success_orders': sync_success_orders
    }
    logger.info(data)
    logger.info('sync finish')
    if len(sync_error_orders) != 0:
        return False, data
    return True, data


