# -*- coding: utf-8 -*-
from common.fields import StringManyToManyField
from orgs.mixins import BulkOrgResourceModelSerializer
from perms.models import TaskPermission

__all__ = [
    'TaskPermissionListSerializer',
    'TaskPermissionCreateUpdateSerializer'
]


class TaskPermissionListSerializer(BulkOrgResourceModelSerializer):
    users = StringManyToManyField(many=True, read_only=True)
    user_groups = StringManyToManyField(many=True, read_only=True)
    tasks = StringManyToManyField(many=True, read_only=True)
    jobs = StringManyToManyField(many=True, read_only=True)

    class Meta:
        model = TaskPermission
        fields = '__all__'


class TaskPermissionCreateUpdateSerializer(BulkOrgResourceModelSerializer):
    class Meta:
        model = TaskPermission
        exclude = ('date_created',)
