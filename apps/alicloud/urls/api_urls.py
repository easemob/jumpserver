# coding:utf-8
from django.urls import path
from rest_framework import routers

from .. import api

app_name = 'alicloud'

router = routers.DefaultRouter()
router.register('ecs', api.AliCloudEcsViewSet, 'ecs')
router.register('rds', api.AliCloudRdsViewSet, 'rds')
router.register('kvstore', api.AliCloudKvStoreViewSet, 'kvstore')
router.register('slb', api.AliCloudSlbViewSet, 'slb')
router.register('oss', api.AliCloudOssViewSet, 'oss')

urlpatterns = [
    # path('', api.AliCloudECSSyncUpdate.as_view(), name='ecs-sync'),
    path('ecs/sync', api.AliCloudEcsSyncUpdate.as_view(), name='ecs-sync'),
    path('slb/sync', api.AliCloudSlbSyncUpdate.as_view(), name='slb-sync'),
    path('rds/sync', api.AliCloudRdsSyncUpdate.as_view(), name='rds-sync'),
    path('kvstore/sync', api.AliCloudKvStoreSyncUpdate.as_view(), name='kvstore-sync'),
    path('oss/sync', api.AliCloudOssSyncUpdate.as_view(), name='oss-sync'),
    path('nodes/children/tree/', api.NodeChildrenAsTreeApi.as_view(), name='node-children-tree'),
    path('nodes/<uuid:pk>/ecs/', api.NodeAddEcsApi.as_view(), name='node-ecs'),
    path('nodes/<uuid:pk>/ecs/add/', api.NodeAddEcsApi.as_view(), name='node-add-ecs'),
    path('nodes/<uuid:pk>/ecs/replace/', api.NodeReplaceEcsApi.as_view(), name='node-replace-ecs'),
    path('nodes/<uuid:pk>/ecs/remove/', api.NodeRemoveEcsApi.as_view(), name='node-remove-ecs'),
    path('nodes/<uuid:pk>/slb/add/', api.NodeAddSlbApi.as_view(), name='node-add-slb'),
    path('nodes/<uuid:pk>/slb/replace/', api.NodeReplaceSlbApi.as_view(), name='node-replace-slb'),
    path('nodes/<uuid:pk>/kvstore/add/', api.NodeAddKvStoreApi.as_view(), name='node-add-kvstore'),
    path('nodes/<uuid:pk>/kvstore/replace/', api.NodeReplaceKvStoreApi.as_view(), name='node-replace-kvstore'),
    path('nodes/<uuid:pk>/rds/add/', api.NodeAddRdsApi.as_view(), name='node-add-rds'),
    path('nodes/<uuid:pk>/rds/replace/', api.NodeReplaceRdsApi.as_view(), name='node-replace-rds'),
    path('nodes/<uuid:pk>/oss/add/', api.NodeAddOssApi.as_view(), name='node-add-oss'),
    path('nodes/<uuid:pk>/oss/replace/', api.NodeReplaceOssApi.as_view(), name='node-replace-oss'),
]

urlpatterns += router.urls
