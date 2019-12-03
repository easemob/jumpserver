# -*- coding: utf-8 -*-
#
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


@receiver(post_save, sender=Dc2, dispatch_uid="my_unique_identifier")
def on_dc2_created_or_update(sender, instance=None, created=False, **kwargs):
    if created:
        logger.info("Asset `{}` create signal received".format(instance))
        # 过期节点资产数量
        clean_all_assets_amount_cache()


@receiver(m2m_changed, sender=Dc2.nodes.through)
def on_node_dc2_changed(sender, instance=None, **kwargs):
    logger.debug("Node assets change signal {} received".format(instance))
    # 当节点和资产关系发生改变时，过期资产数量缓存
    clean_all_assets_amount_cache()
