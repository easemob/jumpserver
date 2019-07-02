# coding:utf-8
from django.urls import path
from rest_framework import routers

from .. import api

app_name = 'alicloud'

router = routers.DefaultRouter()
router.register('ecs', api.AliCloudECSViewSet, 'ecs')
urlpatterns = [
    # path('', api.AliCloudECSSyncUpdate.as_view(), name='ecs-sync'),
    path('ecs/sync', api.AliCloudECSSyncUpdate.as_view(), name='ecs-sync'),
    path('nodes/children/tree/', api.NodeChildrenAsTreeApi.as_view(), name='node-children-tree'),
    path('nodes/<uuid:pk>/ecs/', api.NodeAddEcsApi.as_view(), name='node-ecs'),
    path('nodes/<uuid:pk>/ecs/add/', api.NodeAddEcsApi.as_view(), name='node-add-ecs'),
    path('nodes/<uuid:pk>/ecs/replace/', api.NodeReplaceEcsApi.as_view(), name='node-replace-ecs'),
    path('nodes/<uuid:pk>/ecs/remove/', api.NodeRemoveEcsApi.as_view(), name='node-remove-ecs'),
]

urlpatterns += router.urls
