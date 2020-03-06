# coding:utf-8
from django.urls import path
from rest_framework import routers
from rest_framework_bulk.routes import BulkRouter

from .. import api

app_name = 'alicloud'

router = routers.DefaultRouter()
router.register('ecs', api.AliCloudEcsViewSet, 'ecs')
router.register('rds', api.AliCloudRdsViewSet, 'rds')
router.register('kvstore', api.AliCloudKvStoreViewSet, 'kvstore')
router.register('slb', api.AliCloudSlbViewSet, 'slb')
router.register('oss', api.AliCloudOssViewSet, 'oss')

bulk_router = BulkRouter()
bulk_router.register('template/ecs', api.EcsTemplateViewSet, 'ecs-template')
bulk_router.register('template/ros', api.RosTemplateViewSet, 'ros-template')

urlpatterns = [
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
    path('nodes/<uuid:pk>/slb/remove/', api.NodeRemoveSlbApi.as_view(), name='node-remove-slb'),
    path('nodes/<uuid:pk>/kvstore/add/', api.NodeAddKvStoreApi.as_view(), name='node-add-kvstore'),
    path('nodes/<uuid:pk>/kvstore/replace/', api.NodeReplaceKvStoreApi.as_view(), name='node-replace-kvstore'),
    path('nodes/<uuid:pk>/kvstore/remove/', api.NodeRemoveKvStoreApi.as_view(), name='node-remove-kvstore'),
    path('nodes/<uuid:pk>/rds/add/', api.NodeAddRdsApi.as_view(), name='node-add-rds'),
    path('nodes/<uuid:pk>/rds/replace/', api.NodeReplaceRdsApi.as_view(), name='node-replace-rds'),
    path('nodes/<uuid:pk>/rds/remove/', api.NodeRemoveRdsApi.as_view(), name='node-remove-rds'),
    path('nodes/<uuid:pk>/oss/add/', api.NodeAddOssApi.as_view(), name='node-add-oss'),
    path('nodes/<uuid:pk>/oss/replace/', api.NodeReplaceOssApi.as_view(), name='node-replace-oss'),
    path('nodes/<uuid:pk>/oss/remove/', api.NodeRemoveOssApi.as_view(), name='node-remove-oss'),
    path('nodes/tree/all/', api.BillingQueryNode.as_view(), name='billing-node-all-query'),
    path('billing/sync/', api.BillingQuerySyncTask.as_view(), name='billing-sync'),
    path('billing/node/query/', api.BillingQuery.as_view(), name='billing-query'),
    path('aligateway/<str:region>/zones', api.AliCloudEcsZone.as_view(), name="gateway-zones"),
    path('aligateway/<str:region>/<str:zone>/ecs/instanceTypes', api.AliCloudEcsInstanceType.as_view(),
         name="gateway-instance-type"),
    path('aligateway/<str:region>/images', api.AliCloudEcsImage.as_view(), name="gateway-images"),
    path('aligateway/<str:region>/vpcs', api.AliCloudEcsVpc.as_view(), name="gateway-vpcs"),
    path('aligateway/<str:region>/vpcs/<str:vpc>/vswitches', api.AliCloudEcsVswitch.as_view(),
         name="gateway-vswitches"),
    path('aligateway/<str:region>/sg', api.AliCloudEcsSecurityGroup.as_view(),
         name="gateway-sg"),

]

urlpatterns += router.urls + bulk_router.urls
