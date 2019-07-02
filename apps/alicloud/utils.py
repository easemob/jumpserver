# -*- coding: utf-8 -*-

import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from django.conf import settings
from common.utils import get_logger


class AliCloudUtil(object):
    def __init__(self):
        self.AccessKeyId = settings.ALY_ACCESS_KEY
        self.AccessKeySecret = settings.ALY_ACCESS_SECRET
        self.clt_conn_list = [AcsClient(settings.ALY_ACCESS_KEY, settings.ALY_ACCESS_SECRET, r) for r in
                              settings.ALY_REGION_LIST]
        self.logger = get_logger(__name__)

    def get_ecs_result(self, result):
        insert_result = []
        for Instance in result:
            if Instance['InstanceNetworkType'] == 'vpc':
                InnerAddress = Instance['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
            elif Instance['InstanceNetworkType'] == 'classic':
                InnerAddress = Instance['InnerIpAddress']['IpAddress'][0]
            else:
                InnerAddress = None
            if Instance['PublicIpAddress']['IpAddress']:
                PublicIpAddress = Instance['PublicIpAddress']['IpAddress'][0]
            else:
                PublicIpAddress = None
            insert_result.append({
                'inner_ip': InnerAddress, 'public_ip': PublicIpAddress,
                'instance_name': Instance['InstanceName'], 'instance_id': Instance['InstanceId'],
                'region': Instance['RegionId'], 'status': Instance['Status'],
                'cpu': Instance['Cpu'], 'memory': Instance['Memory'],
                'network_type': Instance['InstanceNetworkType'], 'instance_charge_type': Instance['InstanceChargeType'],
                'maximum_bandwidth': Instance['InternetMaxBandwidthOut'], 'io_optimized': Instance['IoOptimized'],
                'expired_time': Instance['ExpiredTime'], 'instance_type': Instance['InstanceType']
            })
        return insert_result

    def get_ecs_instances(self, pageSize=100):
        result = []
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        for clt in self.clt_conn_list:
            pageNumber = 1
            request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
            clt_result = json.loads(clt.do_action_with_exception(request))
            result += clt_result['Instances']['Instance']
            totalCount = clt_result['TotalCount']
            while totalCount > pageNumber * pageSize:
                pageNumber += 1
                request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
                clt_result = json.loads(clt.do_action_with_exception(request))
                result += clt_result['Instances']['Instance']
        result_dict = {}
        for r in result:
            result_dict[r['InstanceId']] = r
        result_dict_keys = result_dict.keys()
        return self.get_ecs_result(result)
