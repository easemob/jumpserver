# -*- coding: utf-8 -*-
#
from collections import defaultdict
from django.db.models.signals import post_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from common.utils import get_logger
from .models import *

logger = get_logger(__file__)


def clean_all_assets_amount_cache():
    logger.debug("Clear all amount cache")
    cache.delete_pattern('*NODE_ASSETS_AMOUNT*')
    pass


@receiver(post_save, sender=Ecs, dispatch_uid="my_unique_identifier")
def on_ecs_created_or_update(sender, instance=None, created=False, **kwargs):
    if created:
        logger.info("Asset `{}` create signal received".format(instance))
        # 过期节点资产数量
        clean_all_assets_amount_cache()


@receiver(m2m_changed, sender=Ecs.nodes.through)
def on_node_ecs_changed(sender, instance=None, **kwargs):
    logger.debug("Node assets change signal {} received".format(instance))
    # 当节点和资产关系发生改变时，过期资产数量缓存
    clean_all_assets_amount_cache()


@receiver(post_save, sender=Slb, dispatch_uid="my_unique_identifier")
def on_slb_created_or_update(sender, instance=None, created=False, **kwargs):
    if created:
        logger.info("Asset `{}` create signal received".format(instance))
        # 过期节点资产数量
        clean_all_assets_amount_cache()


@receiver(m2m_changed, sender=Slb.nodes.through)
def on_node_slb_changed(sender, instance=None, **kwargs):
    logger.debug("Node assets change signal {} received".format(instance))
    # 当节点和资产关系发生改变时，过期资产数量缓存
    clean_all_assets_amount_cache()



@receiver(post_save, sender=Rds, dispatch_uid="my_unique_identifier")
def on_rds_created_or_update(sender, instance=None, created=False, **kwargs):
    if created:
        logger.info("Asset `{}` create signal received".format(instance))
        # 过期节点资产数量
        clean_all_assets_amount_cache()


@receiver(m2m_changed, sender=Rds.nodes.through)
def on_node_rds_changed(sender, instance=None, **kwargs):
    logger.debug("Node assets change signal {} received".format(instance))
    # 当节点和资产关系发生改变时，过期资产数量缓存
    clean_all_assets_amount_cache()



@receiver(post_save, sender=Oss, dispatch_uid="my_unique_identifier")
def on_oss_created_or_update(sender, instance=None, created=False, **kwargs):
    if created:
        logger.info("Asset `{}` create signal received".format(instance))
        # 过期节点资产数量
        clean_all_assets_amount_cache()


@receiver(m2m_changed, sender=Oss.nodes.through)
def on_node_oss_changed(sender, instance=None, **kwargs):
    logger.debug("Node assets change signal {} received".format(instance))
    # 当节点和资产关系发生改变时，过期资产数量缓存
    clean_all_assets_amount_cache()



@receiver(post_save, sender=KvStore, dispatch_uid="my_unique_identifier")
def on_kvstore_created_or_update(sender, instance=None, created=False, **kwargs):
    if created:
        logger.info("Asset `{}` create signal received".format(instance))
        # 过期节点资产数量
        clean_all_assets_amount_cache()


@receiver(m2m_changed, sender=KvStore.nodes.through)
def on_node_kvstore_changed(sender, instance=None, **kwargs):
    logger.debug("Node assets change signal {} received".format(instance))
    # 当节点和资产关系发生改变时，过期资产数量缓存
    clean_all_assets_amount_cache()
