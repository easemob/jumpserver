# coding:utf-8
from django.urls import path
from .. import views

app_name = 'didicloud'

urlpatterns = [
    # Resource asset url
    path('', views.Dc2ListView.as_view(), name='didicloud-dc2-list'),
    path('dc2/', views.Dc2ListView.as_view(), name='didicloud-dc2-list'),
]
