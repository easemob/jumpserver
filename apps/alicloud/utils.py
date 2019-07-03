# -*- coding: utf-8 -*-

import json

import oss2
import time
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest, DescribeDBInstanceAttributeRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkr_kvstore.request.v20150101 import DescribeInstancesRequest as kvInstancesRequest
from aliyunsdkr_kvstore.request.v20150101 import DescribeInstanceAttributeRequest
from django.conf import settings
from common.utils import get_logger


class AliCloudUtil(object):
    def __init__(self):
        self.AccessKeyId = settings.ALY_ACCESS_KEY
        self.AccessKeySecret = settings.ALY_ACCESS_SECRET
        self.clt_conn_list = [AcsClient(settings.ALY_ACCESS_KEY, settings.ALY_ACCESS_SECRET, r, timeout=30) for r in
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

    def get_slb_instances(self, pageSize=100):
        result = []
        insert_result = []
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        request.set_accept_format('json')
        for clt in self.clt_conn_list:
            pageNumber = 1
            request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
            clt_result = json.loads(clt.do_action_with_exception(request))
            result = result + clt_result['LoadBalancers']['LoadBalancer']
            totalCount = clt_result['TotalCount']
            while totalCount > pageNumber * pageSize:
                request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
                clt_result = json.loads(clt.do_action_with_exception(request), encoding='utf-8')
                result = result + clt_result['LoadBalancers']['LoadBalancer']
                pageNumber += 1
        for Instance in result:
            insert_result.append({
                'address_type': Instance['AddressType'],
                'instance_id': Instance['LoadBalancerId'],
                'instance_name': Instance.get('LoadBalancerName', ''),
                'address_ip_version': Instance.get('AddressIPVersion'),
                'network_type': Instance.get('NetworkType'),
                'address': Instance['Address'],
                'region': Instance['RegionId'],
                'status': Instance['LoadBalancerStatus'],
                'create_time': Instance['CreateTime']
            })
        return insert_result


    def get_kvstore_instances(self, pageSize=50):
        result = []
        request = kvInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        attributeRequest = DescribeInstanceAttributeRequest.DescribeInstanceAttributeRequest()
        attributeRequest.set_accept_format('json')
        for clt in self.clt_conn_list:
            pageNumber = 1
            request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
            clt_result = json.loads(clt.do_action_with_exception(request))
            region_result = clt_result['Instances']['KVStoreInstance']
            totalCount = clt_result['TotalCount']
            while totalCount > pageNumber * pageSize:
                request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
                clt_result = json.loads(clt.do_action_with_exception(request))
                region_result = region_result + clt_result['Instances']['KVStoreInstance']
                pageNumber += 1
            for Instance in region_result:
                result.append({
                    'instance_id': Instance['InstanceId'],
                    'network_type': Instance['NetworkType'],
                    'instance_name': Instance['InstanceName'],
                    'instance_class': Instance['InstanceClass'],
                    'engine_version': Instance['EngineVersion'],
                    'region': Instance['RegionId'],
                    'status': Instance['InstanceStatus'],
                    'capacity': Instance['Capacity'],
                    'qps': Instance['QPS'],
                    'bandwidth': Instance['Bandwidth'],
                    'connections': Instance['Connections'],
                    'expired_time': Instance['EndTime'],
                    'connection_domain': Instance['ConnectionDomain']
                })

        return result


    def get_rds_instances(self, pageSize=100):
        result = []
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_accept_format('json')
        attributeRequest = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        attributeRequest.set_accept_format('json')
        for clt in self.clt_conn_list:
            pageNumber = 1
            request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
            clt_result = json.loads(clt.do_action_with_exception(request))
            region_result = clt_result['Items']['DBInstance']
            totalCount = clt_result['PageRecordCount']
            while totalCount > pageNumber * pageSize:
                request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
                clt_result = json.loads(clt.do_action_with_exception(request), encoding='utf-8')
                region_result = region_result + clt_result['Items']['DBInstance']
                pageNumber += 1
            for Instance in region_result:
                attributeRequest.add_query_param("action_name", "DescribeDBInstanceAttribute")
                attributeRequest.add_query_param("DBInstanceId", Instance['DBInstanceId'])
                r = json.loads(clt.do_action_with_exception(attributeRequest))
                attr = r['Items']['DBInstanceAttribute'][0]
                expired_time = attr.get('ExpireTime')
                if not expired_time:
                    expired_time = None
                result.append({
                    'instance_id': attr.get('DBInstanceId'),
                    'region': attr.get('RegionId'),
                    'instance_name': attr.get('DBInstanceDescription'),
                    'network_type': attr.get('InstanceNetworkType'),
                    'engine_version': attr.get('EngineVersion'),
                    'status': attr.get('DBInstanceStatus'),
                    'expired_time': expired_time,
                    'connection_string': attr.get('ConnectionString'),
                    'connections': attr.get('MaxConnections'),
                    'cpu': attr.get('DBInstanceCPU'),
                    'memory': attr.get('DBInstanceMemory'),
                    'iops': attr.get('MaxIOPS'),
                    'storage': attr.get('DBInstanceStorage')
                })
        return result


    def get_oss_instances(self):
        result = []
        auth = oss2.Auth(self.AccessKeyId, self.AccessKeySecret)
        fuc_buckets = oss2.Service(auth, 'oss-cn-hangzhou.aliyuncs.com').list_buckets(max_keys=300)
        for Instance in fuc_buckets.buckets:
            time_local = time.localtime(Instance.creation_date)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            result.append({
                'instance_id': Instance.name,
                'extranet_endpoint': '.'.join([Instance.location]) + '-internal.aliyuncs.com',
                'intranet_endpoint': '.'.join([Instance.location, 'aliyuncs.com']),
                'instance_name': Instance.name,
                'region': Instance.location.strip('oss-'),
                'status': "Running",
                'create_time': dt
            })
        return result
