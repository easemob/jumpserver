# coding:utf-8
from django.urls import path
from rest_framework import routers

from .. import api

app_name = 'didicloud'

router = routers.DefaultRouter()
router.register('dc2', api.DidiCloudDc2ViewSet, 'dc2')

urlpatterns = [
    path('dc2/sync', api.DidiCloudDc2SyncUpdate.as_view(), name='dc2-sync'),
    path('nodes/children/tree/', api.NodeChildrenAsTreeApi.as_view(), name='node-children-tree'),
    path('nodes/<uuid:pk>/dc2/', api.NodeAddDc2Api.as_view(), name='node-dc2'),
    path('nodes/<uuid:pk>/dc2/add/', api.NodeAddDc2Api.as_view(), name='node-add-dc2'),
    path('nodes/<uuid:pk>/dc2/replace/', api.NodeReplaceDc2Api.as_view(), name='node-replace-dc2'),
    path('nodes/<uuid:pk>/dc2/remove/', api.NodeRemoveDc2Api.as_view(), name='node-remove-dc2'),
]

urlpatterns += router.urls
