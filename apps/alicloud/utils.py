# -*- coding: utf-8 -*-

import json
import time
from datetime import datetime, timedelta

import oss2
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkrds.request.v20140815 import DescribeDBInstancesRequest, DescribeDBInstanceAttributeRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkr_kvstore.request.v20150101 import DescribeInstancesRequest as kvInstancesRequest
from aliyunsdkr_kvstore.request.v20150101 import DescribeInstanceAttributeRequest
from aliyunsdkbssopenapi.request.v20171214.QueryOrdersRequest import QueryOrdersRequest
from aliyunsdkbssopenapi.request.v20171214.GetOrderDetailRequest import GetOrderDetailRequest
from aliyunsdkbssopenapi.request.v20171214.QueryInstanceBillRequest import QueryInstanceBillRequest
from aliyunsdkbssopenapi.request.v20171214.QueryBillOverviewRequest import QueryBillOverviewRequest
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
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        for clt in self.clt_conn_list:
            pageNumber = 1
            while True:
                request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
                clt_result = json.loads(clt.do_action_with_exception(request))
                result = clt_result['Instances']['Instance']
                pageNumber += 1
                if len(result) == 0:
                    print(pageNumber, clt_result['TotalCount'])
                    break
                for info in self.get_ecs_result(result):
                    yield info

    def get_slb_instances(self, pageSize=100):
        request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
        request.set_accept_format('json')
        for clt in self.clt_conn_list:
            pageNumber = 1
            while True:
                request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
                clt_result = json.loads(clt.do_action_with_exception(request), encoding='utf-8')
                result = clt_result['LoadBalancers']['LoadBalancer']
                if len(result) == 0:
                    print(pageNumber, clt_result['TotalCount'])
                    break
                pageNumber += 1
                for Instance in result:
                    yield {
                        'address_type': Instance['AddressType'],
                        'instance_id': Instance['LoadBalancerId'],
                        'instance_name': Instance.get('LoadBalancerName', ''),
                        'address_ip_version': Instance.get('AddressIPVersion'),
                        'network_type': Instance.get('NetworkType'),
                        'address': Instance['Address'],
                        'region': Instance['RegionId'],
                        'status': Instance['LoadBalancerStatus'],
                        'create_time': Instance['CreateTime']
                    }

    def get_kvstore_instances(self, pageSize=50):
        request = kvInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        attributeRequest = DescribeInstanceAttributeRequest.DescribeInstanceAttributeRequest()
        attributeRequest.set_accept_format('json')
        for clt in self.clt_conn_list:
            pageNumber = 1
            while True:
                request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
                clt_result = json.loads(clt.do_action_with_exception(request))
                region_result = clt_result['Instances']['KVStoreInstance']
                pageNumber += 1
                if len(region_result) == 0:
                    print(pageNumber, clt_result['TotalCount'])
                    break
                for Instance in region_result:
                    yield {
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
                    }

    def get_rds_instances(self, pageSize=100):
        request = DescribeDBInstancesRequest.DescribeDBInstancesRequest()
        request.set_accept_format('json')
        attributeRequest = DescribeDBInstanceAttributeRequest.DescribeDBInstanceAttributeRequest()
        attributeRequest.set_accept_format('json')
        for clt in self.clt_conn_list:
            pageNumber = 1
            while True:
                request.set_query_params(dict(PageNumber=pageNumber, PageSize=pageSize))
                clt_result = json.loads(clt.do_action_with_exception(request), encoding='utf-8')
                region_result = clt_result['Items']['DBInstance']
                pageNumber += 1
                if len(region_result) == 0:
                    print(pageNumber, clt_result['PageRecordCount'])
                    break
                for Instance in region_result:
                    attributeRequest.add_query_param("action_name", "DescribeDBInstanceAttribute")
                    attributeRequest.add_query_param("DBInstanceId", Instance['DBInstanceId'])
                    r = json.loads(clt.do_action_with_exception(attributeRequest))
                    attr = r['Items']['DBInstanceAttribute'][0]
                    expired_time = attr.get('ExpireTime')
                    if not expired_time:
                        expired_time = None
                    yield {
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
                    }

    def get_oss_instances(self):
        auth = oss2.Auth(self.AccessKeyId, self.AccessKeySecret)
        fuc_buckets = oss2.Service(auth, 'oss-cn-hangzhou.aliyuncs.com').list_buckets(max_keys=300)
        for Instance in fuc_buckets.buckets:
            time_local = time.localtime(Instance.creation_date)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            yield {
                'instance_id': Instance.name,
                'extranet_endpoint': '.'.join([Instance.location]) + '-internal.aliyuncs.com',
                'intranet_endpoint': '.'.join([Instance.location, 'aliyuncs.com']),
                'instance_name': Instance.name,
                'region': Instance.location.strip('oss-'),
                'status': "Running",
                'create_time': dt
            }

    def get_bill_instances(self, billing_cycle, page_size=None, page_num=None):
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, 'cn-hangzhou')
        request = QueryInstanceBillRequest()
        request.set_accept_format('json')
        request.set_BillingCycle(billing_cycle)
        if page_num: request.set_PageNum(page_num)
        if page_size: request.set_PageSize(page_size)
        response = client.do_action_with_exception(request)
        return json.loads(str(response, encoding='utf-8'))

    def get_bill_overview(self, billing_cycle, product_code=None):
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, 'cn-hangzhou')
        request = QueryBillOverviewRequest()
        request.set_accept_format('json')
        request.set_BillingCycle(billing_cycle)
        if product_code:
            request.set_ProductCode(product_code)
        response = client.do_action_with_exception(request)
        return json.loads(str(response, encoding='utf-8'))

    def get_order_result(self, request):
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, 'cn-hangzhou')
        response = client.do_action_with_exception(request)
        return json.loads(str(response, encoding='utf-8'))

    def get_orders_list(self, begin_time=None, end_time=None, page_size=100):
        """
        查询指定时间内的所有订单
        :param begin_time: 开始时间 标准ISO时间 (例: 2016-05-23T12:00:00Z) 默认为昨天一天的账单数据
        :param end_time: 结束时间 同上
        :param page_size: 每页大小
        :return:
        """
        if not begin_time:
            today = datetime.now()
            yesterday = today - timedelta(days=1)
            begin_time = yesterday.strftime("%Y-%m-%dT00:00:00Z")
            end_time = today.strftime("%Y-%m-%dT00:00:00Z")
        request = QueryOrdersRequest()
        request.set_PageSize(page_size)
        request.set_accept_format('json')
        request.set_CreateTimeEnd(end_time)
        request.set_CreateTimeStart(begin_time)
        page_num = 0
        while True:
            page_num += 1
            request.set_PageNum(page_num)
            data = self.get_order_result(request)
            if len(data['Data']['OrderList']['Order']) != 0:
                yield data
            else:
                break

    def get_orders_details(self, order_id):
        """
        查询订单详情
        :param order_id: 订单id
        :return:
        """
        request = GetOrderDetailRequest()
        request.set_accept_format('json')
        request.set_OrderId(order_id)
        return self.get_order_result(request)
