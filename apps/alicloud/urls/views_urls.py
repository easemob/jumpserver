# coding:utf-8
from django.urls import path
from .. import views

app_name = 'alicloud'

urlpatterns = [
    # Resource asset url
    path('', views.EcsListView.as_view(), name='alicloud-ecs-list'),
    path('asset/', views.EcsListView.as_view(), name='alicloud-ecs-list'),

]
