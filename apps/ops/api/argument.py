# -*- coding: utf-8 -*-

from rest_framework.pagination import LimitOffsetPagination
from common.permissions import IsOrgAdminOrAppUser
from ops.models import TaskArgument
from ops.serializer import TaskArgumentSerializer
from orgs.mixins import OrgBulkModelViewSet

__all__ = [
    'TaskArgumentViewSet'
]


class TaskArgumentViewSet(OrgBulkModelViewSet):
    queryset = TaskArgument.objects.all()
    serializer_class = TaskArgumentSerializer
    filter_fields = ('name',)
    search_fields = filter_fields
    ordering_fields = ('-date_created',)
    pagination_class = LimitOffsetPagination
    permission_classes = (IsOrgAdminOrAppUser,)
