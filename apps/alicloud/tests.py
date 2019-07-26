from django.test import TestCase

# Create your tests here.
from alicloud.utils import AliCloudUtil


class TestAliApi(TestCase):
    def test_get_slb_info(self):
        ali_util = AliCloudUtil()
        f = open("/tmp/a", 'w')
        for info in ali_util.get_ecs_instances():
            print(info.get('instance_id'), info.get('region'))
            f.write(f"{info.get('instance_id')},{info.get('region')}\n")
        f.closed()
