# -*- coding: utf-8 -*-
from rest_framework.pagination import LimitOffsetPagination

from alicloud.models import RosTemplate
from common.permissions import IsOrgAdminOrAppUser
from orgs.mixins import OrgBulkModelViewSet
from alicloud import serializers


class RosTemplateViewSet(OrgBulkModelViewSet):
    """
    API endpoint that allows Asset to be viewed or edited.
    """
    filter_fields = ('name', 'region')
    search_fields = filter_fields
    ordering_fields = ('name', 'region')
    queryset = RosTemplate.objects.all()
    serializer_class = serializers.RosTemplateSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsOrgAdminOrAppUser,)
