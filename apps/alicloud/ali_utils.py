# -*- coding: utf-8 -*-
import json
import time

from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526.CreateLaunchTemplateRequest import CreateLaunchTemplateRequest
from aliyunsdkecs.request.v20140526.DescribeSecurityGroupsRequest import DescribeSecurityGroupsRequest
from aliyunsdkecs.request.v20140526.DescribeVSwitchesRequest import DescribeVSwitchesRequest
from aliyunsdkecs.request.v20140526.DescribeZonesRequest import DescribeZonesRequest
from aliyunsdkecs.request.v20140526.DescribeImagesRequest import DescribeImagesRequest
from aliyunsdkecs.request.v20140526.DescribeRecommendInstanceTypeRequest import DescribeRecommendInstanceTypeRequest
from aliyunsdkecs.request.v20140526.DescribeVpcsRequest import DescribeVpcsRequest
from aliyunsdkecs.request.v20140526.DescribeRegionsRequest import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526.RunInstancesRequest import RunInstancesRequest
from aliyunsdkros.request.v20190910.CreateStackRequest import CreateStackRequest
from aliyunsdkros.request.v20190910.GetStackRequest import GetStackRequest
from aliyunsdkros.request.v20190910.GetTemplateRequest import GetTemplateRequest
from aliyunsdkros.request.v20190910.ListTemplatesRequest import ListTemplatesRequest
from aliyunsdkros.request.v20190910.DescribeRegionsRequest import DescribeRegionsRequest as RosDescribeRegionsRequest
from alicloud.models import EcsTemplate
from alicloud.tasks import create_ecs_info_from_alicoud
from common.utils import get_object_or_none, get_logger
from django.conf import settings

logger = get_logger(__file__)


class AliClient:
    _all_clients = {}
    _AccessKeyId = settings.ALY_ACCESS_KEY
    _AccessKeySecret = settings.ALY_ACCESS_SECRET

    @staticmethod
    def get_client_by_region(region):
        client = AliClient._all_clients.get(region)
        if not client:
            client = AcsClient(AliClient._AccessKeyId, AliClient._AccessKeySecret, region, timeout=30)
            AliClient._all_clients[region] = client
        return client

    @staticmethod
    def get_all_clients():
        return AliClient._all_clients


class EcsClient:
    _all_region_ecs_clients = {}

    def __init__(self, region='cn-beijing'):
        self.region = region
        self.client = AliClient.get_client_by_region(self.region)

    def __new__(cls, *args, **kwargs):
        region = ''
        if len(args) == 0:
            region = 'cn-beijing'
        else:
            region = args[0]
        if not cls._all_region_ecs_clients.get(region):
            cls._all_region_ecs_clients[region] = super().__new__(cls)
        return cls._all_region_ecs_clients[region]

    def query_zones(self):
        request = DescribeZonesRequest()
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        result = json.loads(response)
        return [dict(ZoneId=info['ZoneId'], LocalName=info['LocalName'],
                     # InstanceTypes=info['AvailableInstanceTypes']['InstanceTypes'],
                     DiskCategories=info['AvailableDiskCategories']['DiskCategories']
                     ) for info in result['Zones']['Zone']]

    def query_region(self):
        request = DescribeRegionsRequest()
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        result = json.loads(response)
        return [dict(RegionId=info['RegionId'], LocalName=info['LocalName']) for info in result['Regions']['Region']]

    def query_self_images(self, ):
        request = DescribeImagesRequest()
        request.set_accept_format('json')
        request.set_ActionType('x86_64')
        request.set_ImageOwnerAlias('self')
        result = []
        for page_info in self.pagination_get_all_data(request):
            result.extend(
                [dict(ImageId=info['ImageId'], ImageName=info['ImageName'],
                      DiskDeviceMapping=info['DiskDeviceMappings']['DiskDeviceMapping']) for info in
                 page_info['Images']['Image']])
        return result

    def query_instance_type_by_condition(self, cores=None, memory=None, zone="cn-beijing-c", network_type=None):
        request = DescribeRecommendInstanceTypeRequest()
        request.set_accept_format('json')
        request.set_ZoneId(zone)
        if cores:
            request.set_Cores(cores)
        if memory:
            request.set_Memory(memory)
        if network_type:
            request.set_NetworkType(network_type)
        response = self.client.do_action_with_exception(request)
        for info in json.loads(response)['Data']['RecommendInstanceType']:
            print(info['InstanceType'])
        return json.loads(response)['Data']['RecommendInstanceType']

    def pagination_get_all_data(self, request, page_zie=50):
        page_number = 1
        request.set_PageSize(50)
        request.set_accept_format('json')
        request.set_PageNumber(page_number)
        response = self.client.do_action_with_exception(request)
        response_dict = json.loads(response)
        yield response_dict
        total_count = response_dict['TotalCount']
        while page_number * page_zie < total_count:
            request.set_PageNumber(page_number)
            response = self.client.do_action_with_exception(request)
            page_number += 1
            yield json.loads(response)

    def get_security_group(self, network_type='classic', vpc_id=''):
        request = DescribeSecurityGroupsRequest()
        request.set_IsQueryEcsCount(True)
        request.set_NetworkType(network_type)
        if network_type == 'vpc':
            request.set_VpcId(vpc_id)
        result = []
        for page_info in self.pagination_get_all_data(request):
            result.extend(
                [dict(SecurityGroupId=info['SecurityGroupId'], SecurityGroupName=info['SecurityGroupName'],
                      EcsCount=info['EcsCount']) for info in
                 page_info['SecurityGroups']['SecurityGroup']])
        return result

    def get_vpc(self):
        request = DescribeVpcsRequest()
        result = []
        for page_info in self.pagination_get_all_data(request):
            result.extend([dict(VpcName=info['VpcName'], VpcId=info['VpcId']) for info in page_info['Vpcs']['Vpc']])
        return result

    def get_vswitch(self, vpc_id):
        request = DescribeVSwitchesRequest()
        request.set_VpcId(vpc_id)
        result = []
        for page_info in self.pagination_get_all_data(request):
            result.extend([dict(VSwitchName=info['VSwitchName'], VSwitchId=info['VSwitchId'], ) for info in
                           page_info['VSwitches']['VSwitch']])
        return result

    def create_launch_template(self, name, image_id, sg_id, instance_type, network_type):

        request = CreateLaunchTemplateRequest()
        request.set_LaunchTemplateName(name)
        request.set_ImageOwnerAlias('self')
        request.set_ImageId(image_id)
        request.set_SecurityGroupId(sg_id)
        request.set_InstanceType(instance_type)
        request.set_InstanceChargeType('PrePaid')
        request.set_InternetChargeType('PayByTraffic')
        request.set_NetworkType('network_type')

    def create_and_run_instance(self, template, instance_name, amount, suffix_number, auto_renew):

        ecs_template = get_object_or_none(EcsTemplate, id=template)
        if not ecs_template:
            return ''
        client = AliClient.get_client_by_region(ecs_template.region)
        request = RunInstancesRequest()
        request.set_accept_format('json')
        request.set_ImageId(ecs_template.image)
        request.set_InstanceType(ecs_template.instance_type)
        request.set_SecurityGroupId(ecs_template.sg)
        instance_name = f'{instance_name}-[{suffix_number},{len(str(int(suffix_number) + int(amount)))}]'
        request.set_InstanceName(instance_name)
        if ecs_template.has_public_ip:
            request.set_InternetMaxBandwidthOut(ecs_template.internet_bandwidth)
            request.set_InternetChargeType(ecs_template.internet_charge_type)
        request.set_ZoneId(ecs_template.zone)
        request.set_SystemDiskCategory(ecs_template.system_disk_category)
        request.set_SystemDiskSize(ecs_template.system_disk_size)
        data_disk_list = []
        if ecs_template.data_disk_info:
            data_disk_info = json.loads(ecs_template.data_disk_info)
            for info in data_disk_info:
                print(info)
                tmp = {
                    'Size': info['size'],
                    'Category': info['category'],
                    'DeleteWithInstance': True
                }
                if info.get('SnapshotId'):
                    tmp['SnapshotId'] = info['snapshot_id']
                    continue
                data_disk_list.append(tmp)
        request.set_DataDisks(data_disk_list)
        request.set_Amount(amount)
        request.set_Period(ecs_template.period)
        request.set_InstanceChargeType(ecs_template.instance_charge_type)

        if ecs_template.password_inherit:
            request.set_PasswordInherit(True)
        else:
            request.set_Password(ecs_template.password)

        request.set_AutoRenew(auto_renew)
        if auto_renew:
            request.set_AutoRenewPeriod(1)
        try:
            response = client.do_action_with_exception(request)
            logger.info(response)
            result = json.loads(response)
            create_instance_id = result.get('InstanceIdSets').get('InstanceIdSet')
            result_str = json.dumps(create_instance_id)
            for instance_id in create_instance_id:
                create_ecs_info_from_alicoud.delay(ecs_template, [instance_id])
            return True, result_str
        except Exception as e:
            logger.error(str(e))
            return False, str(e)


class RosClient:
    _all_region_ros_clients = {}

    def __init__(self, region='cn-beijing'):
        self.region = region
        self.client = AliClient.get_client_by_region(self.region)

    def __new__(cls, *args, **kwargs):
        region = ''
        if len(args) == 0:
            region = 'cn-beijing'
        else:
            region = args[0]
        if not cls._all_region_ros_clients.get(region):
            cls._all_region_ros_clients[region] = super().__new__(cls)
        return cls._all_region_ros_clients[region]

    def query_region(self):
        request = RosDescribeRegionsRequest()
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        result = json.loads(response)
        return [dict(RegionId=info['RegionId'], LocalName=info['LocalName']) for info in result['Regions']]

    def pagination_get_all_data(self, request, page_zie=50):
        page_number = 1
        request.set_PageSize(50)
        request.set_accept_format('json')
        request.set_PageNumber(page_number)
        response = self.client.do_action_with_exception(request)
        print(response)
        response_dict = json.loads(response)
        yield response_dict
        total_count = response_dict['TotalCount']
        while page_number * page_zie < total_count:
            request.set_PageNumber(page_number)
            response = self.client.do_action_with_exception(request)
            page_number += 1
            yield json.loads(response)

    def list_templates(self):
        request = ListTemplatesRequest()
        result = []
        for page_info in self.pagination_get_all_data(request):
            result.extend([dict(SecurityGroupId=info['TemplateName'], SecurityGroupName=info['TemplateId']) for info in
                           page_info['Templates']])
        return result

    def get_template_info(self, template_id):
        request = GetTemplateRequest()
        request.set_accept_format('json')
        request.set_TemplateId(template_id)
        response = self.client.do_action_with_exception(request)
        return json.loads(response)

    def create_stack(self, stack_name, template_body, params):
        request = CreateStackRequest()
        request.set_accept_format('json')
        request.set_StackName(stack_name)
        request.set_TemplateBody(template_body)
        request.set_TimeoutInMinutes(10)
        request.set_Parameterss([dict(ParameterKey=k, ParameterValue=v) for k, v in params.items()])
        response = self.client.do_action_with_exception(request)
        stack_info = self.get_stack_info(json.loads(response).get('StackId'))
        timeout_second = 60
        while "COMPLETE" not in stack_info.get('status'):
            if timeout_second <= 0:
                return stack_info
            time.sleep(3)
            stack_info = self.get_stack_info(json.loads(response).get('StackId'))
            timeout_second -= 3
        return stack_info

    def get_stack_info(self, stack_id):
        request = GetStackRequest()
        request.set_StackId(stack_id)
        response = json.loads(self.client.do_action_with_exception(request))
        result = {}
        status = response.get('Status')
        result['status'] = status
        result['stack_id'] = stack_id
        if status == 'CREATE_COMPLETE':
            outputs = [dict(key=o.get('OutputKey'), value=o.get('OutputValue')) for o in response['Outputs']]
            result['outputs'] = outputs
        reason = response.get('StatusReason')
        result['reason'] = reason
        return result


if __name__ == '__main__':
    ros_util = RosClient()
    print(ros_util.get_template_info('99551324-d7a8-42df-bfbc-63bdb5550dc0'))

    # ecs_util = EcsClient('cn-beijing')
    # ecs_util.create_and_run_instance('daff82f1c259471794cf4b880b89658e')

    # ecs_util.get_vpc()
    # print('------')
    # ecs_util.get_vswitch('vpc-2ze7n373b4cp720g7h5o0')
    # ecs_util.query_instance_type_by_condition()
    # ecs_util.query_self_images()
