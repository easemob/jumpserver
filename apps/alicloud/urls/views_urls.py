# coding:utf-8
from django.urls import path
from .. import views

app_name = 'alicloud'

urlpatterns = [
    # Resource asset url
    path('', views.EcsListView.as_view(), name='alicloud-ecs-list'),
    path('ecs/', views.EcsListView.as_view(), name='alicloud-ecs-list'),
    path('slb/', views.SlbListView.as_view(), name='alicloud-slb-list'),
    path('kvstore/', views.KvStoreListView.as_view(), name='alicloud-kvstore-list'),
    path('rds/', views.RdsListView.as_view(), name='alicloud-rds-list'),
    path('oss/', views.OssListView.as_view(), name='alicloud-oss-list'),

]
