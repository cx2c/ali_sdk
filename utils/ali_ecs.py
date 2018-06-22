#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "w.z"
# Date: 2018/3/21
from aliyunsdkcore import client
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceAttributeRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceStatusRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkecs.request.v20140526 import DescribeVSwitchesRequest
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupsRequest
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
import json
import time


# 测试账号 --换成自己的key，此key已经失效
acc_keys_id = "TAIu8r8dk8l"
acc_keys_secret = "IKlYiHb0zhYj2JwFgK0L3kitAF0"


class Instancex(object):
    def __init__(self, instance_regionx=None, instance_idx=None):
        """
        :param instance_idx: 阿里云实例id
        :param instance_regionx: 阿里云可用地区
        """
        self.instance_idx = instance_idx
        self.instance_regionx = instance_regionx
        self.cli = AcsClient(acc_keys_id, acc_keys_secret, self.instance_regionx)
        # self.cli = AcsClient(acc_keys_id, acc_keys_secret, 'cn-hangzhou')

    def describe_instances(self, pagenumber=1):
        """
        返回 可用区 满足筛选条件所有实例 信息
        :param self:
        :param pagenumber: 默认取第一页
        :return:
        """
        pnum = pagenumber
        if self.instance_regionx:
            try:
                req = DescribeInstancesRequest.DescribeInstancesRequest()
                req.set_accept_format('json')
                req.set_PageSize(20)
                req.add_query_param('regionId', self.instance_regionx)
                # req.add_query_param('InstanceNetworkType', 'vpc')
                # req.add_query_param('VpcId', 'vpc-2zex4tsyueo18kxg61xd9')
                req.add_query_param('PageNumber', pnum)
                req.add_query_param('PageSize', 20)
                response = self.cli.do_action_with_exception(req)
                return response.decode('utf8')
            except Exception as ee:
                print("ee: ", ee)
        else:
            print("instance_region is necessary")

    def describe_instance_attribute(self, instance_id=None):
        if instance_id:
            try:
                request = DescribeInstanceAttributeRequest.DescribeInstanceAttributeRequest()
                request.set_accept_format('json')
                request.add_query_param('InstanceId', instance_id)
                response = self.cli.do_action_with_exception(request)
                return response
            except Exception as ee:
                print(ee)
        else:
            print("instance_id is necessary")

    def describe_instance_status(self, pagenumber=1, pagesize=20):
        """
        批量获取当前用户所有实例的状态信息。
        status: Running or stopped
        :return:
        """
        try:
            request = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
            request.set_accept_format('json')
            request.add_query_param('RegionId', 'cn-beijing')
            request.add_query_param('PageNumber', pagenumber)
            request.add_query_param('PageSize', pagesize)
            response = self.cli.do_action_with_exception(request)
            return response
        except Exception as ee:
            print(ee)

    def create_instance(self, regionid, imageid, instancetype, securitygroupid, instancename, vswitchid,
                        datadisk1size, datadisk1category):
        """
        创建机器 ---
        :return:
        """
        # 设置参数
        request = CreateInstanceRequest.CreateInstanceRequest()
        request.set_accept_format('json')
        request.add_query_param('RegionId', regionid)
        request.add_query_param('ImageId', imageid)
        request.add_query_param('SystemDisk.Category', 'cloud_efficiency')
        # request.add_query_param('ZoneId', 'cn-beijing-c') # follow vswitch
        request.add_query_param('InstanceType', instancetype)
        request.add_query_param('SecurityGroupId', securitygroupid)
        request.add_query_param('InstanceName', instancename)
        request.add_query_param('InternetChargeType', 'PayByTraffic')
        request.add_query_param('AutoRenew', True)
        request.add_query_param('AutoRenewPeriod', 1)
        request.add_query_param('InternetMaxBandwidthIn', 100)
        request.add_query_param('InternetMaxBandwidthOut', 50)
        request.add_query_param('Password', '8ql6,yhY')
        request.add_query_param('SystemDisk.Size', 40)
        request.add_query_param('DataDisk.1.Size', datadisk1size)
        request.add_query_param('DataDisk.1.Category', datadisk1category)
        request.add_query_param('VSwitchId', vswitchid)
        request.add_query_param('Period', 1)
        request.add_query_param('InstanceChargeType', 'PrePaid')

        # TODO 发起请求 创建机器 先注释掉
        response = self.cli.do_action_with_exception(request)
        return response
        # return b'{"InstanceId":"i-2zeiz2rcx33nt7yv3yqs","RequestId":"F220AE39-4AFC-493A-A263-8CECD273ECF8"}'

    def start_instance(self, instanceid):
        request = StartInstanceRequest.StartInstanceRequest()
        try:
            request.set_accept_format('json')
            request.add_query_param('InstanceId', instanceid)
            response = self.cli.do_action_with_exception(request)
            return response
        except Exception as ee:
            print("start instance error ", instanceid, ee)

    # def describe_switch(self):
    #     from aliyunsdkcore import client
    #     from aliyunsdkecs.request.v20140526 import DescribeVSwitchesRequest
    #
    #     clt = client.AcsClient('<accessKeyId>', '<accessSecret>', 'cn-hangzhou')
    #
    #     # 设置参数
    #     request = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
    #     request.set_accept_format('json')
    #
    #     request.add_query_param('RegionId', 'cn-beijing')
    #     request.add_query_param('PageNumber', 1)
    #     request.add_query_param('PageSize', 20)
    #     request.add_query_param('ZoneId', 'cn-beijing-a')
    #
    #     # 发起请求
    #     # response = clt.do_action(request)
    #
    #     # print(response)

    def describe_vswitch(self, pagenumber=1):
        pnum = pagenumber
        if self.instance_regionx:
            try:
                request = DescribeVSwitchesRequest.DescribeVSwitchesRequest()
                request.set_accept_format('json')
                request.add_query_param('PageNumber', pnum)
                request.add_query_param('PageSize', 20)

                # 发起请求
                switchinfos = self.cli.do_action_with_exception(request)

                # 封装交换机信息
                switch_dict = json.loads(switchinfos.decode('utf-8'))
                return switch_dict
            except Exception as ee:
                print(ee)
        else:
            print("instance_region is necessary")

    def describre_securitygroup(self, pagenumber=1):
        pnum = pagenumber
        try:
            request = DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
            request.set_accept_format('json')
            request.add_query_param('PageNumber', pnum)
            request.add_query_param('PageSize', 20)

            # 发起请求
            responses = self.cli.do_action_with_exception(request)

            # 封装交安全组信息
            securitygroup = json.loads(responses.decode('utf-8'))
            return securitygroup
        except Exception as ee:
            print(ee)


class Eip(object):
    pass


class Disk(object):
    pass


class Images(object):
    pass


if __name__ == '__main__':

    # 获取满足条件的所有实例详情-含分页
    # 取第一次，拿到TotalCount
    a = Instancex("cn-beijing")
    # try:
    #     res = a.describe_vswitch()
    #     totalaccount = res.get("TotalCount")
    #     total_page = totalaccount // 20 + 1
    #     for pn in range(1, total_page + 1):
    #         res = a.describe_vswitch(pn)
    #         print("可用区域内的交换机为：", res)
    #         time.sleep(2)
    # except Exception as e:
    #     print(e)
    # try:
    #     res = a.describre_securitygroup()
    #     print('res-----:', res)
    #     totalaccount = res.get("TotalCount")
    #     total_page = totalaccount // 20 + 1
    #     for pn in range(1, total_page + 1):
    #         res = a.describre_securitygroup(pn)
    #         print("可用区域内的安全组为：", res)
    #         time.sleep(2)
    # except Exception as e:
    #     print(e)
    a.start_instance("i-2ze5jk243fcqwkdfqe9d")