# -*- coding: utf-8 -*-

from __future__ import print_function
from django.conf import settings
from common.utils import get_logger
import grpc
import time
from grpc.beta import implementations
from .sdk.compute.v1.common_pb2 import JobResultRequest
from .sdk.bill.v1 import bill_pb2_grpc
from .sdk.compute.v1 import common_pb2_grpc, dc2_pb2_grpc, ebs_pb2_grpc, eip_pb2_grpc, sg_pb2_grpc, snap_pb2_grpc, \
    vpc_pb2_grpc
from .sdk.monitor.v1 import counter_pb2_grpc
import didicloud.sdk.common as c


class DicloudClient(object):
    """简单实现的Client 谨作参考"""

    def __init__(self, oauth2_token=settings.DIDI_ACCESS_TOKEN, addr='open.didiyunapi.com:8080'):

        def oauth2token_credentials(context, callback):
            callback([('authorization', 'Bearer %s' % oauth2_token)], None)

        transport_creds = implementations.ssl_channel_credentials()
        auth_creds = implementations.metadata_call_credentials(oauth2token_credentials)
        channel_creds = implementations.composite_channel_credentials(transport_creds, auth_creds)
        self.channel = grpc.secure_channel(addr, channel_creds)
        self.commonStub = common_pb2_grpc.CommonStub(self.channel)
        self.billStub = bill_pb2_grpc.BillStub(self.channel)
        self.dc2Stub = dc2_pb2_grpc.Dc2Stub(self.channel)
        self.eipStub = eip_pb2_grpc.EipStub(self.channel)
        self.ebsStub = ebs_pb2_grpc.EbsStub(self.channel)
        self.sgStub = sg_pb2_grpc.SgStub(self.channel)
        self.snapStub = snap_pb2_grpc.SnapStub(self.channel)
        self.vpcStub = vpc_pb2_grpc.VpcStub(self.channel)
        self.monitorStub = counter_pb2_grpc.MonitorStub(self.channel)

    def wait_for_job_result(self, regionId, jobUuids):
        allDone = False
        queryTimes = 0
        successResult = []
        if isinstance(jobUuids, unicode):
            jobUuids = [jobUuids]

        while not allDone:  # 轮询异步进度
            queryTimes = queryTimes + 1
            time.sleep(3)
            jobResultResp = self.commonStub.JobResult(JobResultRequest(header=Header(regionId=regionId),
                                                                       jobUuids=jobUuids))
            if jobResultResp.error.errno != 0:
                print("query job uuids", jobUuids, "Result error, errmsg:", jobResultResp.error.errmsg)
                break
            allDone = True
            successResult = []
            for jobResult in jobResultResp.data:
                allDone = allDone and jobResult.done  # 记录任务的进度
                successResult.append(jobResult.success)
                if jobResult.done and (not jobResult.success):
                    print("query job", jobResult.jobUuid, "query times:", queryTimes, "failed, reason:",
                          jobResult.result)
                elif jobResult.done and jobResult.success:
                    print("query job", jobResult.jobUuid, "query times:", queryTimes, "success")
                else:
                    print("query job", jobResult.jobUuid, "query times:", queryTimes, "not done yet")

        return successResult


class DiDiCloudUtil(object):
    def __init__(self):

        self.AccessKeyId = settings.ALY_ACCESS_KEY
        self.AccessKeySecret = settings.ALY_ACCESS_SECRET
        self.clt_conn_list = []
        self.logger = get_logger(__name__)
        self.client = DicloudClient()

    def handle_response_error(self, response):
        error = response.error
        if response.error.errno != 0:
            self.logger.error(
                "request id {} return error, error number:{}, error message:{}".format(error.requestId, error.errno,
                                                                                       error.errmsg))
        else:
            self.logger.info("request id {} is ok".format(error.requestId))

    def get_product_region_and_zone(self, product='dc2'):

        rz_info = {}  # {region:[zone1,zone2]}
        resp = self.client.commonStub.ListRegionAndZone(
            c.ListRegionAndZoneRequest(condition=c.ListRegionAndZoneRequest.Condition(product=product)))
        self.handle_response_error(resp)
        for info in resp.data:
            rz_info[info.id] = [zone.id for zone in info.zone]
        return rz_info

    def format_dc2_instance(self, info, region):
        public_ip = None

        if info.eip:
            public_ip = info.eip.ip
        return {
            'inner_ip': info.ip, 'public_ip': public_ip,
            'instance_name': info.name, 'instance_id': info.dc2Uuid,
            'region': region, 'status': info.status,
            'cpu': 0, 'memory': 0,
        }

    def get_dc2_instances(self, pageSize=100):

        for region in self.get_product_region_and_zone(product='dc2').keys():
            pageNumber = 1
            totalNumber = 0
            while True:
                resp = self.client.dc2Stub.ListDc2(
                    c.ListDc2Request(header=c.Header(regionId=region), start=(pageNumber - 1) * totalNumber,
                                     limit=pageSize))
                self.handle_response_error(resp)
                if len(resp.data) == 0:
                    break
                for info in resp.data:
                    totalNumber += 1
                    yield self.format_dc2_instance(info, region)
                pageNumber += 1
