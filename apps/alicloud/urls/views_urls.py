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
    path('billing/', views.BillingView.as_view(), name='alicloud-billing-query'),
    path('template/ecs/', views.EcsTemplateListView.as_view(), name='alicloud-template-ecs-list'),
    path('template/ecs/<uuid:pk>/', views.EcsTeplateDetailView.as_view(), name='alicloud-template-ecs-detail'),
    path('template/ecs/create/', views.EcsTemplateCreateView.as_view(), name='alicloud-template-ecs-create'),
    path('template/ecs/<uuid:pk>/update/', views.EcsTemplateUpdateView.as_view(), name='alicloud-template-ecs-update'),
    path('template/ecs/<uuid:pk>/clone/', views.EcsTemplateCloneView.as_view(), name='alicloud-template-ecs-clone'),
    path('template/slb/', views.SlbTemplate.as_view(), name='alicloud-template-slb-list'),
    path('template/ros/', views.RosTemplate.as_view(), name='alicloud-template-ros-list'),
    path('template/ros/create/', views.RosTeplateCreateView.as_view(), name='alicloud-template-ros-create'),
    path('template/ros/<uuid:pk>/stack/create/', views.RosStackCreateView.as_view(), name='alicloud-ros-stack-create')
]
