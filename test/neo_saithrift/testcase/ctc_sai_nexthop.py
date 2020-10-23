# Copyright 2013-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Thrift SAI interface L3 tests
"""
import socket
import sys
import pdb
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask

@group('l3')
def ip6_to_integer(ip6):
    ip6 = socket.inet_pton(socket.AF_INET6, ip6)
    a, b = unpack(">QQ", ip6)
    return (a << 64) | b

def integer_to_ip6(ip6int):
    a = (ip6int >> 64) & ((1 << 64) - 1)
    b = ip6int & ((1 << 64) - 1)
    return socket.inet_ntop(socket.AF_INET6, pack(">QQ", a, b))

def ip4_to_integer(ip4):
    ip4int = int(socket.inet_aton('10.10.10.1').encode('hex'), 16)
    return ip4int

def integer_to_ip4(ip4int):
    return socket.inet_ntoa(hex(ip4int)[2:].zfill(8).decode('hex'))

class fun_01_create_v4_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

        warmboot(self.client)
        try:
            sys_logging("======create a v4 nexthop======")
            nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
            sys_logging("nhop = 0x%x" %nhop)
            assert (nhop%0x100000000 == 0x4)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_02_create_v6_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '2001::1:1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

        warmboot(self.client)
        try:
            sys_logging("======create a v6 nexthop======")
            nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
            sys_logging("nhop = 0x%x" %nhop)
            assert (nhop%0x100000000 == 0x4)
            #pdb.set_trace()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_03_create_same_neighbor_v4_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sys_logging("======create a v4 nexthop======")
        nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        warmboot(self.client)
        try:
            sys_logging("======create same neighbor v4 nexthop======")
            nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
            sys_logging("nhop1 = 0x%x" %nhop1)
            assert (nhop1 != SAI_NULL_OBJECT_ID)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_04_create_same_neighbor_v6_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '2001::1:1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sys_logging("======create a v6 nexthop======")
        nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        warmboot(self.client)
        try:
            sys_logging("======create same neighbor v6 nexthop======")
            nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
            sys_logging("nhop1 = 0x%x" %nhop1)
            assert (nhop1 != SAI_NULL_OBJECT_ID)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_05_create_nexthop_multi_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        dest_mac = []
        ip_addr4 = []
        ip_addr6 = []
        nhop4_list=[]
        nhop6_list=[]
        mac = ''
        neighbor_num = 500

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family1 = SAI_IP_ADDR_FAMILY_IPV4
        addr_family2 = SAI_IP_ADDR_FAMILY_IPV6
        src_mac_start = ['01:22:33:44:55:', '11:22:33:44:55:', '21:22:33:44:55:', '31:22:33:44:55:', '41:22:33:44:55:', '51:22:33:44:55:', '61:22:33:44:55:', '71:22:33:44:55:', '81:22:33:44:55:', '91:22:33:44:55:', 'a1:22:33:44:55:']

        sys_logging("======create 50 v4 and 500 neighbor first======")
        for i in range(neighbor_num):
            dest_mac.append(src_mac_start[i/99] + str(i%99).zfill(2))
            ip_addr4.append(integer_to_ip4(1+i))
            ip_addr6.append(integer_to_ip6(10000+i))
            if i%2 == 0:
                sai_thrift_create_neighbor(self.client, addr_family1, rif_id1, ip_addr4[i], dest_mac[i])
                sai_thrift_create_neighbor(self.client, addr_family2, rif_id1, ip_addr6[i], dest_mac[i])
            else:
                sai_thrift_create_neighbor(self.client, addr_family1, rif_id2, ip_addr4[i], dest_mac[i])
                sai_thrift_create_neighbor(self.client, addr_family2, rif_id2, ip_addr6[i], dest_mac[i])

        #pdb.set_trace()

        warmboot(self.client)
        try:
            sys_logging("======create 500 v4 and 500 v6 nexthop======")
            for i in range(neighbor_num):
                if i%2 == 0:
                    nhop4 = sai_thrift_create_nhop(self.client, addr_family1, ip_addr4[i], rif_id1)
                    nhop4_list.append(nhop4)
                    nhop6 = sai_thrift_create_nhop(self.client, addr_family2, ip_addr6[i], rif_id1)
                    nhop6_list.append(nhop6)
                else:
                    nhop4 = sai_thrift_create_nhop(self.client, addr_family1, ip_addr4[i], rif_id2)
                    nhop4_list.append(nhop4)
                    nhop6 = sai_thrift_create_nhop(self.client, addr_family2, ip_addr6[i], rif_id2)
                    nhop6_list.append(nhop6)
        finally:
            sys_logging("======clean up======")
            for i in range(neighbor_num):
                self.client.sai_thrift_remove_next_hop(nhop4_list[i])
                self.client.sai_thrift_remove_next_hop(nhop6_list[i])
                if i%2 == 0:
                    sai_thrift_remove_neighbor(self.client, addr_family1, rif_id1, ip_addr4[i], dest_mac[i])
                    sai_thrift_remove_neighbor(self.client, addr_family2, rif_id1, ip_addr6[i], dest_mac[i])
                else:
                    sai_thrift_remove_neighbor(self.client, addr_family1, rif_id2, ip_addr4[i], dest_mac[i])
                    sai_thrift_remove_neighbor(self.client, addr_family2, rif_id2, ip_addr6[i], dest_mac[i])
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_06_remove_v4_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sys_logging("======create a v4 nexthop======")
        nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        warmboot(self.client)
        try:
            
            attrs = self.client.sai_thrift_get_next_hop_attribute(nhop)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove the v4 nexthop======")
            self.client.sai_thrift_remove_next_hop(nhop)
            attrs = self.client.sai_thrift_get_next_hop_attribute(nhop)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("======clean up======")
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_07_remove_v6_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '2001::1:1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sys_logging("======create a v6 nexthop======")
        nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        warmboot(self.client)
        try:
            
            attrs = self.client.sai_thrift_get_next_hop_attribute(nhop)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove the v6 nexthop======")
            status = self.client.sai_thrift_remove_next_hop(nhop)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            attrs = self.client.sai_thrift_get_next_hop_attribute(nhop)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("======clean up======")
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_08_remove_no_exist_v4_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sys_logging("======create a v4 nexthop======")
        nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #print "0x%x" %nhop
        nhop1 = 0x600000004
        warmboot(self.client)
        try:
            sys_logging("======remove no exist v4 nexthop======")
            status = self.client.sai_thrift_remove_next_hop(nhop1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            
            attrs = self.client.sai_thrift_get_next_hop_attribute(nhop)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_09_remove_no_exist_v6_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '2001::1:1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sys_logging("======create a v6 nexthop======")
        nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #print "0x%x" %nhop
        nhop1 = 0x600000004
        warmboot(self.client)
        try:
            sys_logging("======remove no exist v6 nexthop======")
            status = self.client.sai_thrift_remove_next_hop(nhop1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            
            attrs = self.client.sai_thrift_get_next_hop_attribute(nhop)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_10_get_nexthop_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sys_logging("======create a v4 nexthop======")
        nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        warmboot(self.client)
        try:

            attrs = self.client.sai_thrift_get_next_hop_attribute(nhop)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_ATTR_TYPE:
                    if SAI_NEXT_HOP_TYPE_IP != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_ATTR_IP:
                    print "get ip = %s" %a.value.ipaddr.addr.ip4
                    if ip_addr1 != a.value.ipaddr.addr.ip4:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID:
                    if rif_id1 != a.value.oid:
                        raise NotImplementedError()
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_01_nhop_neighbor_share_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        # create next hop first
        #import pdb
        #pdb.set_trace()
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #self.client.sai_thrift_remove_next_hop(nhop1)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst=ip_addr1,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_02_nhop_bind_multi_route_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '20.20.20.0'
        ip_addr3_subnet = '30.30.30.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'

        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask1, nhop1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr3_subnet, ip_mask1, nhop1)

        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        pkt2 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr2_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst=ip_addr2_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        pkt3 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr3_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt3 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst=ip_addr3_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:

            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [1])
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packets( exp_pkt3, [1])
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask1, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr3_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)


