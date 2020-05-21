# -*- coding: utf-8 -*-
from django.utils import timezone
from rest_framework.pagination import LimitOffsetPagination
from common.permissions import IsValidUser
from ops.models import FileDeployTask
from ops.serializer import FileDeployTaskSerializer
from orgs.mixins import OrgBulkModelViewSet

__all__ = [
    'FileDeployTaskViewSet',
]


class FileDeployTaskViewSet(OrgBulkModelViewSet):
    queryset = FileDeployTask.objects.all()
    serializer_class = FileDeployTaskSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsValidUser,)

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.last_modify_user = self.request.user
        instance.task_meta.created_by = self.request.user.username
        instance.save()

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.last_modify_user = self.request.user
        instance.save()
