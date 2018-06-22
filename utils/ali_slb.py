#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "w.z"
# Date: 2018/4/13

from aliyunsdkcore.client import AcsClient
from aliyunsdkslb.request.v20140515 import DescribeVServerGroupAttributeRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515 import DescribeVServerGroupsRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerAttributeRequest
from aliyunsdkslb.request.v20140515 import DescribeLoadBalancerTCPListenerAttributeRequest
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkslb.request.v20140515 import CreateLoadBalancerTCPListenerRequest
from aliyunsdkslb.request.v20140515 import CreateVServerGroupRequest
from aliyunsdkslb.request.v20140515 import StartLoadBalancerListenerRequest

import logging

log = logging.getLogger('django')

# 测试账号 --换成自己的key，此key已经失效
acc_keys_id = "TAIu8r8dk8l"
acc_keys_secret = "IKlYiHb0zhYj2JwFgK0L3kitAF0"


class Slb(object):
    def __init__(self, instance_regionid=None):
        self.instance_regionid = instance_regionid
        self.cli = AcsClient(acc_keys_id, acc_keys_secret, self.instance_regionid)

    def describe_vserver_groups(self, loadbalancerid):
        """
        查询服务器组列表
        :return:
                {
                "VServerGroupId":"rsp-2zecl3ijcewcn",  只能拿到id，还需要 取到所有 服务器组的 id-name
                "VServerGroupName":"80"
                }
        """
        try:
            request = DescribeVServerGroupsRequest.DescribeVServerGroupsRequest()
            request.set_accept_format('json')

            request.add_query_param('RegionId', self.instance_regionid)
            request.add_query_param('LoadBalancerId', loadbalancerid)

            # 发起请求
            response = self.cli.do_action_with_exception(request)
            return response.decode('utf8')
        except Exception as ee:
            log.error('--ds-ad--: {}'.format(ee))

    def describe_vservergroup_attribute(self, vservergroupid):
        """
        查询服务器组的详细信息
        TODO 先拿到服务器组，再查服务器组的详细信息， 需要拿服务器组
        :return:
        """
        try:
            request = DescribeVServerGroupAttributeRequest.DescribeVServerGroupAttributeRequest()
            request.set_accept_format('json')

            request.add_query_param('RegionId', self.instance_regionid)
            request.add_query_param('VServerGroupId', vservergroupid)

            # 发起请求
            response = self.cli.do_action_with_exception(request)
            return response.decode('utf8')
        except Exception as ee:
            log.error(ee)

    def describe_loadbalancers(self, pagenumber=1):
        """
        查询负载均衡实例列表
        :return:
        """
        try:
            request = DescribeLoadBalancersRequest.DescribeLoadBalancersRequest()
            request.set_accept_format('json')
            request.add_query_param('RegionId', self.instance_regionid)
            request.add_query_param('PageSize', 20)
            request.add_query_param('PageNumber', pagenumber)

            # 发起请求
            response = self.cli.do_action_with_exception(request)
            response = response.decode('utf8')
            return response
        except Exception as ee:
            log.error('ali_slb 查询负载均衡实例列表 error: {}'.format(ee))

    def describeloadbalancerattribute(self, loadbalanceid):
        """
        查询负载均衡实例的详细信息 - 来获取端口 --没有分页
        :param loadbalanceid:
        :return:
        """
        try:
            request = DescribeLoadBalancerAttributeRequest.DescribeLoadBalancerAttributeRequest()
            request.set_accept_format('json')
            request.add_query_param('RegionId', self.instance_regionid)
            request.add_query_param('LoadBalancerId', loadbalanceid)

            # 发起请求
            response = self.cli.do_action_with_exception(request)
            return response.decode('utf8')
        except Exception as ee:
            log.error('查询负载均衡接偶错误: {}'.format(ee))

    def describe_lb_tcplisterattribute(self, loadbalancerid, port):
        """
        描述 负载均衡 端口
        :return:
        """
        # 设置参数
        try:
            request = DescribeLoadBalancerTCPListenerAttributeRequest.DescribeLoadBalancerTCPListenerAttributeRequest()
            request.set_accept_format('json')

            request.add_query_param('LoadBalancerId', loadbalancerid)
            request.add_query_param('RegionId', self.instance_regionid)
            request.add_query_param('ListenerPort', port)
            # 发起请求
            response = self.cli.do_action_with_exception(request)
            return response.decode('utf8')
        except ServerException as ee:
            log.error("describe_lb_tcplisterattribute: {}".format(ee))
        except ClientException as ee:
            log.error("describe_lb_tcplisterattribute-: {}".format(ee))

    def add_lb_tcplister(self, loadbalanceid, listenerport, vservergroup):
        try:
            # 设置参数
            request = CreateLoadBalancerTCPListenerRequest.CreateLoadBalancerTCPListenerRequest()
            request.set_accept_format('json')
            request.add_query_param('LoadBalancerId', loadbalanceid)
            request.add_query_param('ListenerPort', listenerport)
            request.add_query_param('Bandwidth', -1)
            request.add_query_param('RegionId', self.instance_regionid)
            request.add_query_param('VServerGroupId', vservergroup)
            # 发起请求
            response = self.cli.do_action_with_exception(request)
            return response.decode('utf8')
        except Exception as ee:
            log.error('创建监听错误{}:'.format(ee))

    def startloadbalancerlistener(self, loadbalanceid, listenerport):
        try:
            request = StartLoadBalancerListenerRequest.StartLoadBalancerListenerRequest()
            request.set_accept_format('json')

            request.add_query_param('RegionId', 'cn-beijing')
            request.add_query_param('LoadBalancerId', loadbalanceid)
            request.add_query_param('ListenerPort', listenerport)
            response = self.cli.do_action_with_exception(request)
            return response.decode('utf8')
        except Exception as ee:
            log.error('启动监听错误: {}'.format(ee))

    def create_slb_vsservergroup(self, loadbalancerid, groupname, serverlist):
        # serverlist = [{'ServerId':'vm-233','Port':'80','Weight':'100'},{'ServerId':'vm-233','Port':'80','Weight':'100'},{'ServerId':'vm-233','Port':'80','Weight':'100'}]
        try:
            request = CreateVServerGroupRequest.CreateVServerGroupRequest()
            request.set_accept_format('json')

            request.add_query_param('RegionId', 'cn-beijing')
            request.add_query_param('LoadBalancerId', loadbalancerid)
            request.add_query_param('VServerGroupName', groupname)
            request.add_query_param('BackendServers', serverlist)
            response = self.cli.do_action_with_exception(request)
            return response.decode('utf8')
        except Exception as ee:
            log.error('创建服务器组错误: {}'.format(ee))


if __name__ == '__main__':
    a = Slb('cn-beijing')
    # b = a.describe_loadbalancers(1)
    # print(b)
    # b = a.describe_vservergroup_attribute('rsp-2ze8uf9y6d7by')
    # print(b)
    # c = a.describe_lb_tcplisterattribute('lb-2zeebyik836gwi3tpmwqt', 80)
    # print(c)
    loadbalanceid = "lb-2zen4z6d9cm8f1bgh3os1"
    groupname = "group1"
    serverlist = [{'ServerId': 'i-2ze5jk243fcqwkdfqe9d', 'Port': '180', 'Weight': '100'},
                  {'ServerId': 'i-2zefi3cw7xre10brcp6y', 'Port': '180', 'Weight': '100'}]
    d = a.create_slb_vsservergroup(loadbalanceid, groupname, serverlist)
    print(d)
