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

class fun_01_create_v4_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        
        sys_logging("======create a v4 route entry======")
        warmboot(self.client)
        try:
            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            sys_logging("create route status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS) 
   
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_02_create_v6_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create a v6 route entry======")
        warmboot(self.client)
        try:
            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            sys_logging("create route status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS) 

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)


class fun_03_create_exist_v4_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        
        sys_logging("======create a v4 route entry======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        warmboot(self.client)
        try:
            sys_logging("======create exist v4 route entry again======")
            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            sys_logging("create route status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS) 

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_04_create_exist_v6_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create a v6 route entry======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        warmboot(self.client)
        try:
            sys_logging("======create exist v6 route entry again======")
            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            sys_logging("create route status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS) 
   
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

'''
class fun_05_max_v4_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask1 = '255.255.255.255'
        mac = ''
        route_num1 = 16383

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sys_logging("======create max v4 route entry======")
        for i in range(route_num1):
            ip_addr_subnet.append(integer_to_ip4(1+i*256))            
            sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask1, nhop1)

        warmboot(self.client)
        try:
            sys_logging("======create another v4 route entry======")
            ip_addr = integer_to_ip4(1+route_num1*256)
            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr, ip_mask1, nhop1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_INSUFFICIENT_RESOURCES)
            

        finally:
            sys_logging("======clean up======")
            for i in range(route_num1):
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_06_max_v6_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        ip_addr_subnet = []
        route_num1 = 8191


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create max v6 route entry======")
        for i in range(route_num1):
            ip_addr_subnet.append(integer_to_ip6(1+i*256))            
            sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask1, nhop1)

        warmboot(self.client)
        try:
            sys_logging("======create another v4 route entry======")
            status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_INSUFFICIENT_RESOURCES) 
   
        finally:
            sys_logging("======clean up======")
            for i in range(route_num1):           
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

'''
class fun_07_remove_v4_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
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
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create a v4 route entry======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        
        warmboot(self.client)
        try:
            sys_logging("======remove the v4 route entry======")
            status = sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            addr = sai_thrift_ip_t(ip4=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            sys_logging("======get the v4 route entry attribute======")
            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
   
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_08_remove_v6_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create a v6 route entry======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        
        warmboot(self.client)
        try:
            sys_logging("======remove the v6 route entry======")
            status = sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            addr = sai_thrift_ip_t(ip6=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip6=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)   
            sys_logging("======get the v6 route entry attribute======")
            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
   
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_09_remove_no_exist_v4_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
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
        ip_addr1_subnet1 = '10.10.20.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create a v4 route entry======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        
        warmboot(self.client)
        try:
            sys_logging("======remove a no exist v4 route entry======")
            status = sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet1, ip_mask1, nhop1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            addr = sai_thrift_ip_t(ip4=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix) 
            sys_logging("======get the exist v4 route entry attribute======")
            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
   
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_10_remove_no_exist_v6_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_addr1_subnet1 = '1234:5678:9abc:def0:4422:1133:5588:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create a v6 route entry======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        
        warmboot(self.client)
        try:
            sys_logging("======remove a no exist v6 route entry======")
            status = sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            addr = sai_thrift_ip_t(ip6=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip6=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix) 
            sys_logging("======get the exist v6 route entry attribute======")
            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
   
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_11_set_and_get_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sys_logging("======create a v4 route entry======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip4=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)  
            sys_logging("======get the v4 route entry attribute======")
            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("get action = %d" %a.value.s32)
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID:
                    sys_logging("get next hop = 0x%x" %a.value.oid)
                    if nhop1 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("get count id = 0x%x" %a.value.oid)
                    if 0 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTE_ENTRY_ATTR_META_DATA:
                    sys_logging("get cid = %d" %a.value.u32)
                    if 0 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_ROUTE_ENTRY_ATTR_IP_ADDR_FAMILY:
                    sys_logging("get ip version = %d" %a.value.u32)
                    if 0 != a.value.u32:
                        raise NotImplementedError()
            sys_logging("======set the v4 route entry action======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DENY)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            sys_logging("======set the v4 route entry counter oid======")
            type = SAI_COUNTER_TYPE_REGULAR
            counter_id = sai_thrift_create_counter(self.client, type)
            sys_logging("creat counter_id = 0x%x" %counter_id)
            attr_value = sai_thrift_attribute_value_t(oid=counter_id)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_COUNTER_ID, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            sys_logging("======set the v4 route entry nexthop======")
            attr_value = sai_thrift_attribute_value_t(oid=nhop2)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            sys_logging("======set the v4 route entry cid======")
            cid = 100
            attr_value = sai_thrift_attribute_value_t(u32=cid)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_META_DATA, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            sys_logging("======get the v4 route entry attribute again======")
            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("get action = %d" %a.value.s32)
                    if SAI_PACKET_ACTION_DENY != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID:
                    sys_logging("get next hop = 0x%x" %a.value.oid)
                    if nhop2 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("get count id = 0x%x" %a.value.oid)
                    if counter_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTE_ENTRY_ATTR_META_DATA:
                    sys_logging("get cid = %d" %a.value.u32)
                    if cid != a.value.u32:
                        raise NotImplementedError()

   
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)

class fun_12_set_unsupported_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        trap_id = 50

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
       
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)  
        sys_logging("======create a v4 route entry======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip4=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)  
            
            attr_value = sai_thrift_attribute_value_t(u32=trap_id)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_USER_TRAP_ID, value=attr_value)
            sys_logging("======set v4 route entry unsupported attribute======")
            status = self.client.sai_thrift_set_route_attribute(route, attr)
            
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_NOT_SUPPORTED)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)           
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_13_get_default_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
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
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create a v4 route entry======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip4=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix) 
            sys_logging("======get the v4 route entry attribute default======")
            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("get default action = %d" %a.value.s32)
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("get default count id = 0x%x" %a.value.oid)
                    if 0 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTE_ENTRY_ATTR_META_DATA:
                    sys_logging("get default cid = %d" %a.value.u32)
                    if 0 != a.value.u32:
                        raise NotImplementedError()   
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_14_bulk_create_v4_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR   
 
        warmboot(self.client)
        try:
            sys_logging("======create 100 v4 route entry======")
            status = sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_15_bulk_create_v6_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:fff0'

        dmac1 = '00:11:22:33:44:55'
        ip_addr_subnet = []

        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        ip6 = ip6_to_integer(ip_addr2)
        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip6(ip6+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR   
 
        warmboot(self.client)
        try:
            sys_logging("======create 100 v6 route entry======")
            status = sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_16_bulk_create_route_stop_on_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create 100 v4 route entry with the 51th is exist======")
        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        ip_addr_subnet[50] = integer_to_ip4(1+49*256)
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR   
        status = sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
            
        warmboot(self.client)
        try:
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS)
            sys_logging("======the 1-50 v4 route entries successfully create======")
            for i in range(50):
                attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                sys_logging("status = %d" %attrs.status)
                assert (attrs.status == SAI_STATUS_SUCCESS)
            sys_logging("======the 51-100 v4 route entries successfully create======")
            for i in range(50,100):
                attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                sys_logging("status = %d" %attrs.status)
                assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_17_bulk_create_route_ignore_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create 100 v4 route entries with the 51th is exist======")
        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        ip_addr_subnet[50] = integer_to_ip4(1+49*256)
        mode = SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR   
        status = sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
            
        warmboot(self.client)
        try:
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("======the 1-50 and 52-100 v4 route entries successfully create,the 51 unsuccessfully create======")
            for i in range(route_num):
                if 50 == i:
                    attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                    sys_logging("status = %d" %attrs.status)
                    assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
                    continue
                attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                sys_logging("status = %d" %attrs.status)
                assert (attrs.status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_18_bulk_remove_v4_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR 
        sys_logging("======create 100 v4 route entries======")
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        warmboot(self.client)
        try:
            sys_logging("======remove the 100 v4 route entries======")
            status = sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            for i in range(route_num):
                addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
                mask = sai_thrift_ip_t(ip4=ip_mask)
                ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
                route = sai_thrift_route_entry_t(vr_id, ip_prefix)
                routes.append(route)
                sys_logging("======get the 100 v4 route entries attribute======")
            for i in range(route_num):
                attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                sys_logging("status = %d" %attrs.status)
                assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_19_bulk_remove_v6_route_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:fff0'

        dmac1 = '00:11:22:33:44:55'
        ip_addr_subnet = []

        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        ipaddr2 = ip6_to_integer(ip_addr2)
        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip6(ipaddr2+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR  
        sys_logging("======create 100 v6 route entries======")
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        warmboot(self.client)
        try:
            sys_logging("======remove the 100 v6 route entries======")
            status = sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            for i in range(route_num):
                addr = sai_thrift_ip_t(ip6=integer_to_ip6(ipaddr2+i*256))
                mask = sai_thrift_ip_t(ip6=ip_mask)
                ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr, mask=mask)
                route = sai_thrift_route_entry_t(vr_id, ip_prefix)
                routes.append(route)
                sys_logging("======get the 100 v6 route entries attribute======")
            for i in range(route_num):
                attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                sys_logging("status = %d" %attrs.status)
                assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_20_bulk_remove_route_stop_on_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
   
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR 
        sys_logging("======create 100 v4 route entries======")
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
        ip_addr_subnet[50] = integer_to_ip4(1+49*256)    
        warmboot(self.client)
        try:
            sys_logging("======remove 100 v4 route entries with the 51th is error======")
            status = sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            sys_logging("======the 1-50 v4 route entries successfully remove======")
            for i in range(50):
                attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                sys_logging("status = %d" %attrs.status)
                assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            sys_logging("======the 51-100 v4 route entries unsuccessfully remove======")
            for i in range(50,route_num):
                attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                sys_logging("status = %d" %attrs.status)
                assert (attrs.status == SAI_STATUS_SUCCESS)
            
            
        finally:
            sys_logging("======clean up======")
            ip_addr_subnet[50] = integer_to_ip4(1+50*256)
            
            for ip_addr in ip_addr_subnet[50:100]:
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr, ip_mask, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_21_bulk_remove_route_ignore_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
   
        mode = SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR 
        sys_logging("======create 100 v4 route entries======")
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
        ip_addr_subnet[50] = integer_to_ip4(1+49*256)    
        warmboot(self.client)
        try:
            sys_logging("======remove 100 v4 route entries with the 51th is error======")
            status = sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("======the 1-50 and 52-100 v4 route entries successfully remove,the 51 unsuccessfully remove======")
            for i in range(route_num):
                if 50 == i :
                    attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                    sys_logging("status = %d" %attrs.status)
                    assert (attrs.status == SAI_STATUS_SUCCESS)
                    continue
                attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                sys_logging("status = %d" %attrs.status)
                assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
            
        finally:
            sys_logging("======clean up======")
            ip_addr_subnet[50] = integer_to_ip4(1+50*256)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[50], ip_mask, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_22_bulk_set_route_attr_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        attr_list = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR 
        sys_logging("======create 100 route entries======")
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
            
        warmboot(self.client)
        try:
            sys_logging("======get the 100 route entries attribute nexthop======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID:
                    sys_logging("get next hop = 0x%x" %a.value.oid)
                    assert (a.value.oid == nhop1)
            sys_logging("======set the 100 route entries attribute nexthop======")
            for i in range(route_num):
                attr_value = sai_thrift_attribute_value_t(oid=nhop2)
                attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID, value=attr_value)
                attr_list.append(attr)
            status = self.client.sai_thrift_set_routes_attribute(routes, attr_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("======get the 100 route entries attribute nexthop again======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID:
                    sys_logging("get next hop = 0x%x" %a.value.oid)
                    assert (a.value.oid == nhop2)
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_22_bulk_set_route_attr_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        attr_list = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR 
        sys_logging("======create 100 route entries======")
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
            
        warmboot(self.client)
        try:
            sys_logging("======get the 100 route entries attribute action======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("get packet action = %d" %a.value.s32)
            sys_logging("======set the 100 route entries attribute action======")
            for i in range(route_num):
                attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DENY)
                attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
                attr_list.append(attr)
            status = self.client.sai_thrift_set_routes_attribute(routes, attr_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("======get the 100 route entries attribute action again======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("get packet action = %d" %a.value.s32)
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_22_bulk_set_route_attr_fn_3(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        attr_list = []
        counter_id_list = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR   
        sys_logging("======create 100 route entries======")
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
            
        warmboot(self.client)
        try:
            sys_logging("======get the 100 route entries attribute counter id======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("get counter id = 0x%x" %a.value.s32)
            sys_logging("======set the 100 route entries attribute counter id======")
            for i in range(route_num):
                type = SAI_COUNTER_TYPE_REGULAR
                counter_id = sai_thrift_create_counter(self.client, type)
                sys_logging("creat counter_id = 0x%x" %counter_id)
                attr_value = sai_thrift_attribute_value_t(oid=counter_id)
                attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_COUNTER_ID, value=attr_value)
                counter_id_list.append(counter_id)
                attr_list.append(attr)
            status = self.client.sai_thrift_set_routes_attribute(routes, attr_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("======get the 100 route entries attribute counter id again======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("get counter id = 0x%x" %a.value.oid)
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            for i in range(route_num):
                sai_thrift_remove_counter(self.client, counter_id_list[i])

class fun_22_bulk_set_route_attr_fn_4(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        cid = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        attr_list = []
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR
        sys_logging("======create 100 route entries======")
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
            
        warmboot(self.client)
        try:
            sys_logging("======get the 100 route entries attribute cid======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_META_DATA:
                    sys_logging("get route cid = %d" %a.value.u32)
            sys_logging("======set the 100 route entries attribute cid======")
            for i in range(route_num):
                attr_value = sai_thrift_attribute_value_t(u32=cid)
                attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_META_DATA, value=attr_value)
                attr_list.append(attr)
                cid = cid + 1
            status = self.client.sai_thrift_set_routes_attribute(routes, attr_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("======get the 100 route entries attribute cid again======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_META_DATA:
                    sys_logging("get route cid = %d" %a.value.u32)
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_23_bulk_set_route_attr_stp_on_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        attr_list = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR
        sys_logging("======create 100 route entries======")
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
            
        warmboot(self.client)
        try:
            sys_logging("======set 100 route entries attribute with the 51th is error======")
            for i in range(route_num):
                if 50 == i :
                    attr_value = sai_thrift_attribute_value_t(s32=8)
                    attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
                    attr_list.append(attr)
                    continue
                attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DENY)
                attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
                attr_list.append(attr)
            status = self.client.sai_thrift_set_routes_attribute(routes, attr_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_NOT_SUPPORTED)
            sys_logging("======get 100 route entries attribute======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            j = 0
            sys_logging("======the 1-50 v4 route entries attrbute successfully set and the 51-100 v4 route entries attrbute unsuccessfully set======")
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
                    if j < 50:
                        sys_logging("get packet action = %d" %a.value.s32)
                        assert (a.value.s32 == SAI_PACKET_ACTION_DENY)
                        j = j+1
                    else:
                    
                        sys_logging("get packet action = %d" %a.value.s32)
                        assert (a.value.s32 == SAI_PACKET_ACTION_FORWARD)
                        j = j+1
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_24_bulk_set_route_attr_ignore_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        attr_list = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create 100 route entries======")
        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR   
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
            
        warmboot(self.client)
        try:
            sys_logging("======get the 100 route entries attribute packet action======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("get packet action = %d" %a.value.s32)
            sys_logging("======set 100 route entries attribute with the 51th is error======")
            for i in range(route_num):
                if 50 == i :
                    attr_value = sai_thrift_attribute_value_t(s32=8)
                    attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
                    attr_list.append(attr)
                    continue
                attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DENY)
                attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
                attr_list.append(attr)
            status = self.client.sai_thrift_set_routes_attribute(routes, attr_list, mode)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("======get the 100 route entries attribute packet action again======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            sys_logging("======the 51th v4 route entries attrbute unsuccessfully set and other v4 route entries attrbute successfully set======")
            j = 0
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
                    if j == 50:
                        sys_logging("get packet action = %d" %a.value.s32)
                        assert (a.value.s32 == SAI_PACKET_ACTION_FORWARD)
                        j = j+1
                        continue
                    sys_logging("get packet action = %d" %a.value.s32)
                    assert (a.value.s32 == SAI_PACKET_ACTION_DENY)
                    j = j+1
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_25_bulk_get_route_attr_stop_on_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        attr_list = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create 100 route entries======")
        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR   
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
        addr = sai_thrift_ip_t(ip4=integer_to_ip4(2+50*256))
        mask = sai_thrift_ip_t(ip4=ip_mask)
        ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
        routes[50] = sai_thrift_route_entry_t(vr_id, ip_prefix)    
        warmboot(self.client)
        try:    
            sys_logging("======get 100 route entries attribute with the 51th is error======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

            sys_logging("======get 100 route entries attribute one by one======")
            for i in range(route_num):
                if 50 == i:
                    attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                    sys_logging("get the %d th route entry status" %(i+1))
                    sys_logging("status = %d" %attrs.status)
                    assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
                    continue
                attrs = self.client.sai_thrift_get_route_attribute(routes[i])
                sys_logging("get the %d th route entry status" %(i+1))
                sys_logging("status = %d" %attrs.status)
                assert (attrs.status == SAI_STATUS_SUCCESS)

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_26_bulk_get_route_attr_ignore_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0

        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 100
        vr_id_list = []
        addr_family_list = []
        ip_mask_list = []
        nhop_list = []
        pkt_action_list =[]
        counter_oid_list =[]
        cid_list = []
        routes = []
        attr_list = []
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create 100 route entries======")
        for i in range(route_num):
            vr_id_list.append(vr_id)
            addr_family_list.append(addr_family)
            ip_addr_subnet.append(integer_to_ip4(1+i*256))
            ip_mask_list.append(ip_mask)
            nhop_list.append(nhop1)
            pkt_action_list.append(None)
            counter_oid_list.append(None)
            cid_list.append(None)
        mode = SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR   
        sai_thrift_create_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, pkt_action_list, counter_oid_list, cid_list, mode)
        for i in range(route_num):
            addr = sai_thrift_ip_t(ip4=integer_to_ip4(1+i*256))
            mask = sai_thrift_ip_t(ip4=ip_mask)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)
            routes.append(route)
        addr = sai_thrift_ip_t(ip4=integer_to_ip4(2+50*256))
        mask = sai_thrift_ip_t(ip4=ip_mask)
        ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
        routes[50] = sai_thrift_route_entry_t(vr_id, ip_prefix)    
        warmboot(self.client)
        try:
            sys_logging("======get 100 route entries attribute with the 51th is error======")
            attrs = self.client.sai_thrift_get_routes_attribute(routes, mode)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            j = 0
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION:
                    if j == 50:
                        sys_logging("get the %d th route entry packet action" %(j+1))
                        sys_logging("packet action = %d" %a.value.s32)
                        assert (a.value.s32 != SAI_PACKET_ACTION_FORWARD)
                        j = j+1
                        continue
                    sys_logging("get the %d th route entry packet action" %(j+1))
                    sys_logging("packet action = %d" %a.value.s32)
                    assert (a.value.s32 == SAI_PACKET_ACTION_FORWARD)
                    j = j+1

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_routes(self.client, vr_id_list, addr_family_list, ip_addr_subnet, ip_mask_list, nhop_list, mode)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_01_v4_route_dest_ip_match_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        pkt2 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.20.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.20.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send dst ip(v4) hit packet======")
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [0])
            sys_logging("======send dst ip(v4) not hit packet======")
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_no_packet( exp_pkt2, 0)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_02_v6_route_dest_ip_match_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:99ab'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt1 = simple_tcpv6_packet( eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                ipv6_src='2000::1',
                                ipv6_hlim=64)
        exp_pkt1 = simple_tcpv6_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                ipv6_src='2000::1',
                                ipv6_hlim=63)

        pkt2 = simple_tcpv6_packet( eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ipv6_dst='1234:5678:9abc:def0:4422:1133:6688:1111',
                                ipv6_src='2000::1',
                                ipv6_hlim=64)
        exp_pkt2 = simple_tcpv6_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ipv6_dst='1234:5678:9abc:def0:4422:1133:6688:1111',
                                ipv6_src='2000::1',
                                ipv6_hlim=63)
        warmboot(self.client)
        try:
            sys_logging("======send dst ip(v6) hit packet======")
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [0])
            sys_logging("======send dst ip(v6) not hit packet======")
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_no_packet( exp_pkt2, 0)
   
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)


            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_03_v4_route_action_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:    
            sys_logging("======send packet when action is default(forward)======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])

            addr = sai_thrift_ip_t(ip4=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)       
            sys_logging("======set action to deny and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DENY)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 0)
            sys_logging("======set action to forward and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            sys_logging("======set action to drop and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 0)
            sys_logging("======set action to forward and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            sys_logging("======set action to copy and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_COPY)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            sys_logging("======set action to transit and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRANSIT)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            sys_logging("======set action to log and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_LOG)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            sys_logging("======set action to trap and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRAP)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 0)
           
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_04_v6_route_action_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:99ab'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ipv6_dst=ip_addr1_subnet,
                                ipv6_src='2000::1',
                                ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ipv6_dst=ip_addr1_subnet,
                                ipv6_src='2000::1',
                                ipv6_hlim=63)
        warmboot(self.client)
        try:
            sys_logging("======send packet when action is default(forward)======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])

            addr = sai_thrift_ip_t(ip6=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip6=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)       
            sys_logging("======set action to deny and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DENY)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 0)
            sys_logging("======set action to forward and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            sys_logging("======set action to drop and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 0)
            sys_logging("======set action to forward and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            sys_logging("======set action to copy and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_COPY)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            sys_logging("======set action to transit and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRANSIT)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            sys_logging("======set action to log and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_LOG)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            sys_logging("======set action to trap and send packet======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRAP)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 0)
   
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_05_v4_route_nexthop_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send packet======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            self.ctc_verify_no_packet( exp_pkt, 1)
            sys_logging("======set v4 route entry attribute nexthop======")
            addr = sai_thrift_ip_t(ip4=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)      
            attr_value = sai_thrift_attribute_value_t(oid=nhop2)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            sys_logging("======send packet again======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            self.ctc_verify_no_packet( exp_pkt, 0)

   
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_06_v6_route_nexthop_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:99ab'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ipv6_dst=ip_addr1_subnet,
                                ipv6_src='2000::1',
                                ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ipv6_dst=ip_addr1_subnet,
                                ipv6_src='2000::1',
                                ipv6_hlim=63)
        warmboot(self.client)
        try:
            sys_logging("======send packet======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            self.ctc_verify_no_packet( exp_pkt, 1)
            sys_logging("======set v6 route entry attribute nexthop======")
            addr = sai_thrift_ip_t(ip6=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip6=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)             
            attr_value = sai_thrift_attribute_value_t(oid=nhop2)
            attr = sai_thrift_attribute_t(id=SAI_ROUTE_ENTRY_ATTR_NEXT_HOP_ID, value=attr_value)
            self.client.sai_thrift_set_route_attribute(route, attr)
            sys_logging("======send packet again======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            self.ctc_verify_no_packet( exp_pkt, 0)

   
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_07_v4_route_phy_to_phy_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
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
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======port type rif send dest ip hit v4 packet to port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
'''
class test11(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        lag_id1 = sai_thrift_create_lag(self.client, [])
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port4)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        #pdb.set_trace()
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======port type rif send dest ip hit v4 packet to port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            #sai_thrift_remove_lag_member(self.client, lag_member_id1)
            #sai_thrift_remove_lag_member(self.client, lag_member_id2)
            #sai_thrift_remove_lag_member(self.client, lag_member_id3)
            #sai_thrift_remove_lag(self.client, lag_id1)

class test22(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        lag_id1 = sai_thrift_create_lag(self.client, [])
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port4)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)


        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=96)

        warmboot(self.client)
        try:
            sys_logging("======sub port type rif send dest ip hit v4 packet to port type rif======")
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
'''
            
class scenario_08_v6_route_phy_to_phy_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        
        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63)
        warmboot(self.client)
        try:
            sys_logging("======port type rif send dest ip hit v6 packet to port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_09_v4_route_phy_to_vlan_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sai_thrift_create_fdb(self.client, vlan_oid, dmac1, port2, SAI_PACKET_ACTION_FORWARD)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)


        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======port type rif send dest ip hit v4 packet to vlan type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, vlan_oid, dmac1, port2)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_10_v6_route_phy_to_vlan_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sai_thrift_create_fdb(self.client, vlan_oid, dmac1, port2, SAI_PACKET_ACTION_FORWARD)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63)

        warmboot(self.client)
        try:
            sys_logging("======port type rif send dest ip hit v6 packet to vlan type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, vlan_oid, dmac1, port2)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_11_v4_route_phy_to_sub_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=104)

        warmboot(self.client)
        try:
            sys_logging("======port type rif send dest ip hit v4 packet to sub port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_12_v6_route_phy_to_sub_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   dl_vlan_enable=True,
                                   vlan_vid=20,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63,
                                   pktlen=104)
        

        warmboot(self.client)
        try:
            sys_logging("======port type rif send dest ip hit v6 packet to sub port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            

class scenario_13_v4_route_phy_to_bridge_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 30
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port2])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport1_id, SAI_PACKET_ACTION_FORWARD)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id2)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        #pdb.set_trace()
   
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=104)

        warmboot(self.client)
        try:
            sys_logging("======port type rif send dest ip hit v4 packet to bridge type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)




class scenario_14_v6_route_phy_to_bridge_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 30
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port2])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport1_id, SAI_PACKET_ACTION_FORWARD)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id2)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   dl_vlan_enable=True,
                                   vlan_vid=30,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63,
                                   pktlen=104)

        warmboot(self.client)
        try:
            sys_logging("======port type rif send dest ip hit v6 packet to bridge type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_15_v4_route_vlan_to_phy_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)


        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.20',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.20',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=96)

        warmboot(self.client)
        try:
            sys_logging("======vlan type rif send dest ip hit v4 packet to port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
class scenario_16_v6_route_vlan_to_phy_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=10,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63,
                                   pktlen=96)

        warmboot(self.client)
        try:
            sys_logging("======vlan type rif send dest ip hit v6 packet to port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_17_v4_route_vlan_to_vlan_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
   

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, dmac1, port2, SAI_PACKET_ACTION_FORWARD)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.20',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.20',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======vlan type rif send dest ip hit v4 packet to vlan type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, vlan_oid1, dmac1, port2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

class scenario_18_v6_route_vlan_to_vlan_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
   

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, dmac1, port2, SAI_PACKET_ACTION_FORWARD)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63)

        warmboot(self.client)
        try:
            sys_logging("======vlan type rif send dest ip hit v6 packet to vlan type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, vlan_oid1, dmac1, port2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr) 
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid1)


class scenario_19_v4_route_vlan_to_sub_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
  

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
       
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.20',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.10.10.20',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======vlan type rif send dest ip hit v4 packet to sub port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

class scenario_20_v6_route_vlan_to_sub_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
  

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
       
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=10,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   dl_vlan_enable=True,
                                   vlan_vid=20,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63)

        warmboot(self.client)
        try:
            sys_logging("======vlan type rif send dest ip hit v6 packet to sub port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            sys_logging("======clean up======")
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid1)


class scenario_21_v4_route_vlan_to_bridge_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port2])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id1)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport1_id, SAI_PACKET_ACTION_FORWARD)
       
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id2)

        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.20',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.10.10.20',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======vlan type rif send dest ip hit v4 packet to bridge type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
class scenario_22_v6_route_vlan_to_bridge_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        #vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port2])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id1)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport1_id, SAI_PACKET_ACTION_FORWARD)
       
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id2)

        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=10,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   dl_vlan_enable=True,
                                   vlan_vid=20,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63)
        warmboot(self.client)
        try:
            sys_logging("======vlan type rif send dest ip hit v6 packet to bridge type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_23_v4_route_sub_to_phy_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)


        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=96)

        warmboot(self.client)
        try:
            sys_logging("======sub port type rif send dest ip hit v4 packet to port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_24_v6_route_sub_to_phy_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=10,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63,
                                   pktlen=96)

        warmboot(self.client)
        try:
            sys_logging("======sub port type rif send dest ip hit v6 packet to port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_25_v4_route_sub_to_vlan_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
  

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sai_thrift_create_fdb(self.client, vlan_oid1, dmac1, port2, SAI_PACKET_ACTION_FORWARD)
       
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=96)

        warmboot(self.client)
        try:
            sys_logging("======sub port type rif send dest ip hit v4 packet to vlan type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, vlan_oid1, dmac1, port2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

class scenario_26_v6_route_sub_to_vlan_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
  

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sai_thrift_create_fdb(self.client, vlan_oid1, dmac1, port2, SAI_PACKET_ACTION_FORWARD)
       
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=10,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63,
                                   pktlen=96)

        warmboot(self.client)
        try:
            sys_logging("======sub port type rif send dest ip hit v6 packet to vlan type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, vlan_oid1, dmac1, port2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid1)


class scenario_27_v4_route_sub_to_sub_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
  

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
       
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id1)
        
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======sub port type rif send dest ip hit v4 packet to sub port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            sys_logging("======clean up======")
            #pdb.set_trace()
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

class scenario_28_v6_route_sub_to_sub_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
  

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
       
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=10,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   dl_vlan_enable=True,
                                   vlan_vid=20,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63)

        warmboot(self.client)
        try:
            sys_logging("======sub port type rif send dest ip hit v6 packet to sub port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid1)


class scenario_29_v4_route_sub_to_bridge_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port2])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id1)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport1_id, SAI_PACKET_ACTION_FORWARD)
       
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id2)
 
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.20',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.10.10.20',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======sub port type rif send dest ip hit v4 packet to bridge type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_30_v6_route_sub_to_bridge_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port2])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id1)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport1_id, SAI_PACKET_ACTION_FORWARD)
       
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id2)
        #pdb.set_trace()
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=10,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   dl_vlan_enable=True,
                                   vlan_vid=20,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63)

        warmboot(self.client)
        try:
            sys_logging("======sub port type rif send dest ip hit v6 packet to bridge type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_31_v4_route_bridge_to_phy_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 30
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:22:22:22:22:22'
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port1])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id1)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)


        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='10.10.10.40',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.40',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=96)

        warmboot(self.client)
        try:
            sys_logging("======bridge type rif send dest ip hit v4 packet to port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            
            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_32_v6_route_bridge_to_phy_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 30
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:22:22:22:22:22'
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port1])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id1)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=30,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63,
                                   pktlen=96)

        warmboot(self.client)
        try:
            sys_logging("======bridge type rif send dest ip hit v6 packet to port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            
            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port1)
            self.client.sai_thrift_remove_bridge(bridge_id)            

class scenario_33_v4_route_bridge_to_vlan_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:22:22:22:22:22'

       
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sai_thrift_create_fdb(self.client, vlan_oid1, dmac1, port2, SAI_PACKET_ACTION_FORWARD)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port1])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id1)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.40',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.40',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=96)

        warmboot(self.client)
        try:
            sys_logging("======bridge type rif send dest ip hit v4 packet to vlan type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, vlan_oid1, dmac1, port2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_bridge(bridge_id)

            self.client.sai_thrift_remove_vlan(vlan_oid1)

class scenario_34_v6_route_bridge_to_vlan_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:22:22:22:22:22'

       
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sai_thrift_create_fdb(self.client, vlan_oid1, dmac1, port2, SAI_PACKET_ACTION_FORWARD)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port1])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id1)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=10,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63,
                                   pktlen=96)

        warmboot(self.client)
        try:
            sys_logging("======bridge type rif send dest ip hit v6 packet to vlan type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, vlan_oid1, dmac1, port2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_bridge(bridge_id)

            self.client.sai_thrift_remove_vlan(vlan_oid1)


class scenario_35_v4_route_bridge_to_sub_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:22:22:22:22:22'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id1)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port1])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id1)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.40',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.10.10.40',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======bridge type rif send dest ip hit v4 packet to sub port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_36_v6_route_bridge_to_sub_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:22:22:22:22:22'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id1)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port1])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id1)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=10,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   dl_vlan_enable=True,
                                   vlan_vid=20,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63)

        warmboot(self.client)
        try:
            sys_logging("======bridge type rif send dest ip hit v6 packet to sub port type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_37_v4_route_bridge_to_bridge_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:22:22:22:22:22'

        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port1])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port2])
        bport2_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id1)
        sai_thrift_create_fdb_bport(self.client, bridge_id1, dmac1, bport2_id, SAI_PACKET_ACTION_FORWARD)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id1)
        bridge_rif_bp1 = sai_thrift_create_bridge_rif_port(self.client, bridge_id1, rif_id2)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)


        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.40',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.10.10.40',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======bridge type rif send dest ip hit v4 packet to bridge type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, bport1_id)
            sai_thrift_delete_fdb(self.client, bridge_id1, dmac1, bport2_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port1)
            sai_thrift_remove_bridge_sub_port(self.client, bport2_id, port2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id1)

class scenario_38_v6_route_bridge_to_bridge_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:22:22:22:22:22'

        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port1])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port2])
        bport2_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id1)
        sai_thrift_create_fdb_bport(self.client, bridge_id1, dmac1, bport2_id, SAI_PACKET_ACTION_FORWARD)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id1)
        bridge_rif_bp1 = sai_thrift_create_bridge_rif_port(self.client, bridge_id1, rif_id2)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=10,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                   eth_dst=dmac1,
                                   eth_src=router_mac,
                                   dl_vlan_enable=True,
                                   vlan_vid=20,
                                   ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:1111',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63)

        warmboot(self.client)
        try:
            sys_logging("======bridge type rif send dest ip hit v6 packet to bridge type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac2, bport1_id)
            sai_thrift_delete_fdb(self.client, bridge_id1, dmac1, bport2_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port1)
            sai_thrift_remove_bridge_sub_port(self.client, bport2_id, port2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id1)

class scenario_39_v4_stress_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.0'
        mac = ''
        route_num = 10000

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        
        sys_logging("======create 10000 v4 route entries======")
        for i in range(route_num):
            ip_addr_subnet.append(integer_to_ip4(1+i*256))            
            sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop1)
        
        warmboot(self.client)
        try:
            sys_logging("======send 20 different packets======")
            for i in range(4000,4020):
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:00:00:00:00:1',
                                        ip_dst=ip_addr_subnet[i],
                                        ip_src='192.168.8.1',
                                        ip_id=106,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=dmac1,
                                             eth_src=router_mac,
                                             ip_dst=ip_addr_subnet[i],
                                             ip_src='192.168.8.1',
                                             ip_id=106,
                                             ip_ttl=63)
 
                self.ctc_send_packet( 0, str(pkt))
                self.ctc_verify_packet( exp_pkt, 1)
            sys_logging("======remove 10000 v4 route entries======")
            for i in range(route_num):
                          
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop1)
            ip_addr_subnet = []
            sys_logging("======create 10000 v4 route entries again======")
            for i in range(route_num):
                ip_addr_subnet.append(integer_to_ip4(1+i*512))            
                sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop1)
            sys_logging("======send 20 different packets======")
            for i in range(6000,6020):
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:00:00:00:00:1',
                                        ip_dst=ip_addr_subnet[i],
                                        ip_src='192.168.8.1',
                                        ip_id=106,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=dmac1,
                                             eth_src=router_mac,
                                             ip_dst=ip_addr_subnet[i],
                                             ip_src='192.168.8.1',
                                             ip_id=106,
                                             ip_ttl=63)

                self.ctc_send_packet( 0, str(pkt))
                self.ctc_verify_packet( exp_pkt, 1)
            sys_logging("======remove 10000 v4 route entries======")
            for i in range(route_num):              
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop1)
            ip_addr_subnet = []
            sys_logging("======create 10000 v4 route entries again======")
            for i in range(route_num):
                ip_addr_subnet.append(integer_to_ip4(1+i*1024))            
                sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop1)
            sys_logging("======send 20 different packets======")
            for i in range(8000,8020):
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:00:00:00:00:1',
                                        ip_dst=ip_addr_subnet[i],
                                        ip_src='192.168.8.1',
                                        ip_id=106,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=dmac1,
                                             eth_src=router_mac,
                                             ip_dst=ip_addr_subnet[i],
                                             ip_src='192.168.8.1',
                                             ip_id=106,
                                             ip_ttl=63)

                self.ctc_send_packet( 0, str(pkt))
                self.ctc_verify_packet( exp_pkt, 1)
        finally:
            sys_logging("======clean up======")
            for i in range(route_num):
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop1)

            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)



class scenario_40_v6_stress_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac1 = '00:11:22:33:44:55'
        ip_addr_subnet = []
        mac = ''
        route_num = 4000

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)

        dest_ip = '0000:5678:9abc:def0:4422:1133:5577:0000'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ff00'
        dest_int = ip6_to_integer(dest_ip)
        sys_logging("======create 4000 v6 route entries======")
        for i in range(route_num):
            ip_addr_subnet.append(integer_to_ip6(dest_int+i*256))
            sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop)            

        warmboot(self.client)
        try:
            sys_logging("======send 20 different packets======")
            for i in range(1000,1020):
                pkt = simple_tcpv6_packet(eth_dst=router_mac,
                                          eth_src='00:00:00:00:00:1',
                                          ipv6_dst=ip_addr_subnet[i],
                                          ipv6_src='2000:bbbb::1',
                                          ipv6_hlim=64)
                exp_pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                              eth_src=router_mac,
                                              ipv6_dst=ip_addr_subnet[i],
                                              ipv6_src='2000:bbbb::1',
                                              ipv6_hlim=63)

                self.ctc_send_packet( 0, str(pkt))
                self.ctc_verify_packet( exp_pkt, 1)
            sys_logging("======remove 4000 v6 route entries======")    
            for i in range(route_num):
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop)
            sys_logging("======create 4000 v6 route entries again======")
            ip_addr_subnet = []
            for i in range(route_num):
                ip_addr_subnet.append(integer_to_ip6(dest_int+i*1024))
                sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop)
            sys_logging("======send 20 different packets======")
            for i in range(2000,2020):
                pkt = simple_tcpv6_packet(eth_dst=router_mac,
                                          eth_src='00:00:00:00:00:1',
                                          ipv6_dst=ip_addr_subnet[i],
                                          ipv6_src='2000:bbbb::1',
                                          ipv6_hlim=64)
                exp_pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                              eth_src=router_mac,
                                              ipv6_dst=ip_addr_subnet[i],
                                              ipv6_src='2000:bbbb::1',
                                              ipv6_hlim=63)

                print "send ip_addr = %s" %ip_addr_subnet[i]
                self.ctc_send_packet( 0, str(pkt))
                self.ctc_verify_packet( exp_pkt, 1)
            sys_logging("======remove 4000 v6 route entries======")
            for i in range(route_num):
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop)
            sys_logging("======create 4000 v6 route entries again======")
            ip_addr_subnet = []
            for i in range(route_num):
                ip_addr_subnet.append(integer_to_ip6(dest_int+i*4096))
                sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop)
            sys_logging("======send 20 different packets======")
            for i in range(3000,3020):
                pkt = simple_tcpv6_packet(eth_dst=router_mac,
                                          eth_src='00:00:00:00:00:1',
                                          ipv6_dst=ip_addr_subnet[i],
                                          ipv6_src='2000:bbbb::1',
                                          ipv6_hlim=64)
                exp_pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                              eth_src=router_mac,
                                              ipv6_dst=ip_addr_subnet[i],
                                              ipv6_src='2000:bbbb::1',
                                              ipv6_hlim=63)

                print "send ip_addr = %s" %ip_addr_subnet[i]
                self.ctc_send_packet( 0, str(pkt))
                self.ctc_verify_packet( exp_pkt, 1)
            
        finally:
            sys_logging("======clean up======")
            for i in range(route_num):
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop)
            
            self.client.sai_thrift_remove_next_hop(nhop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class route_shake_update_nexthop_attribute_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 30
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr4 = '10.10.10.4'
        ip_addr1_subnet = '10.10.10.0'
        ip_addr2_subnet = '10.10.20.0'
        ip_addr3_subnet = '10.10.30.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        dmac4 = '00:11:22:33:44:58'
        

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port2])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport1_id, SAI_PACKET_ACTION_FORWARD)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id2)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_addr3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_addr4, dmac4)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id3)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id3)
        nhop4 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id3)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask1, nhop2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr3_subnet, ip_mask1, nhop3)



        
        
   
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=104)


        pkt2 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.20.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                ip_dst='10.10.20.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        exp_pkt2_2 = simple_tcp_packet(
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                ip_dst='10.10.20.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        pkt3 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.30.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt3 = simple_tcp_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                ip_dst='10.10.30.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        exp_pkt3_2 = simple_tcp_packet(
                                eth_dst=dmac4,
                                eth_src=router_mac,
                                ip_dst='10.10.30.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)


        warmboot(self.client)
        try:
            sys_logging("======port type rif send dest ip hit v4 packet to bridge type rif======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [2])

            self.ctc_send_packet( 0, str(pkt3))
            self.ctc_verify_packets( exp_pkt3, [2])


            
            sys_logging('=====set bridge type rif bind nexthop attribute,and return not support=====')
            attr_value = sai_thrift_attribute_value_t(oid=rif_id3)
            attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID, value=attr_value)
            status = self.client.sai_thrift_set_next_hop_attribute(nhop1, attr)
            print 'set bridge type rif nhop status = %d' %status
            
            addr = sai_thrift_ip_t(ip4=ip_addr2)
            ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
            attr_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
            attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_IP, value=attr_value)
            status = self.client.sai_thrift_set_next_hop_attribute(nhop1, attr)
            print 'set bridge type rif nhop status = %d' %status



            sys_logging('=====set port type rif bind nexthop attribute,and return success=====')
            addr = sai_thrift_ip_t(ip4=ip_addr3)
            ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
            attr_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
            attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_IP, value=attr_value)
            status = self.client.sai_thrift_set_next_hop_attribute(nhop2, attr)
            print 'set port type rif nhop status = %d' %status


            sys_logging('=====set port type rif bind nexthop attribute,and return success=====')
            attr_value = sai_thrift_attribute_value_t(oid=rif_id4)
            attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID, value=attr_value)
            status = self.client.sai_thrift_set_next_hop_attribute(nhop3, attr)
            print 'set port type rif nhop status = %d' %status
            
            addr = sai_thrift_ip_t(ip4=ip_addr4)
            ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
            attr_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
            attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_IP, value=attr_value)
            status = self.client.sai_thrift_set_next_hop_attribute(nhop3, attr)
            print 'set port type rif nhop status = %d' %status



            attr_value = sai_thrift_attribute_value_t(oid=rif_id2)
            attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID, value=attr_value)
            status = self.client.sai_thrift_set_next_hop_attribute(nhop4, attr)
            print 'set bridge type rif nhop status = %d' %status


            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( exp_pkt2_2, [2])

            self.ctc_send_packet( 0, str(pkt3))
            self.ctc_verify_packets( exp_pkt3_2, [3])


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask1, nhop2)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr3_subnet, ip_mask1, nhop3)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            self.client.sai_thrift_remove_next_hop(nhop4)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_addr2, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_addr3, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id4, ip_addr4, dmac1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport1_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)




