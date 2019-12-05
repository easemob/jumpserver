import json

from aliyunsdkecs.request.v20140526.DescribeSecurityGroupsRequest import DescribeSecurityGroupsRequest
from django.test import TestCase

# Create your tests here.
from alicloud.utils import AliCloudUtil
from django.conf import settings

class TestAliApi(TestCase):
    def test_get_slb_info(self):
        ali_util = AliCloudUtil()
        # f = open("/tmp/a", 'w')
        for info in ali_util.get_ecs_instances():
            print(info.get('instance_id'), info.get('region'))
            # f.write(f"{info.get('instance_id')},{info.get('region')}\n")
        # f.closed()


    def test_query_enterprise_instance_type(self):
        from aliyunsdkcore.client import AcsClient
        from aliyunsdkecs.request.v20140526.DescribeInstanceTypesRequest import DescribeInstanceTypesRequest
        client = AcsClient(settings.ALY_ACCESS_KEY, settings.ALY_ACCESS_SECRET, 'cn-beijing')


        # request = DescribeInstanceTypesRequest()

        request = DescribeSecurityGroupsRequest()
        request.set_accept_format('json')
        response = client.do_action_with_exception(request)
        result = json.loads(response)

        for info in result['SecurityGroups']['SecurityGroup']:
            print(info['SecurityGroupType'], info['SecurityGroupId'], info['SecurityGroupName'], info['ResourceGroupId'], info['VpcId'])

            print(info)

        print(response)


        # id_list = []
        # for info in result['InstanceTypes']['InstanceType']:
        #     if info['InstanceFamilyLevel'] == 'EnterpriseLevel' and info['CpuCoreCount'] == 4 and info['MemorySize'] == 16.0:
        #         id_list.append(info['InstanceTypeId'])
        #         print(info)
        # print(id_list)

        # print(response)
        # python2:  print(response)
        # print(str(response, encoding='utf-8'))
