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


class fun_01_create_nexthop_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        
        warmboot(self.client)
        try:
            sys_logging("======create 2 nexthop group======")
            nhop_group1 = sai_thrift_create_next_hop_group(self.client)
            nhop_group2 = sai_thrift_create_next_hop_group(self.client)
            sys_logging("nexthop group id = 0x%x" %nhop_group1)
            assert (nhop_group1%0x100000000 == 0x5)
            sys_logging("nexthop group id = 0x%x" %nhop_group2)
            assert (nhop_group2%0x100000000 == 0x5)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop_group(nhop_group2)
            
class fun_02_create_max_nexthop_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        num = 1023
        nhop_grp_list = []
        sys_logging("======create 1023 nexthop group======")
        for i in range(num):
            nhop_group = sai_thrift_create_next_hop_group(self.client)
            nhop_grp_list.append(nhop_group)

        warmboot(self.client)
        try:
            sys_logging("======create a new nexthop group======")
            nhop_group1 = sai_thrift_create_next_hop_group(self.client)
            sys_logging("nhop_group1 = 0x%x" %nhop_group1)
            assert (nhop_group1 == SAI_NULL_OBJECT_ID)
        finally:
            sys_logging("======clean up======")
            for i in range(num):
                self.client.sai_thrift_remove_next_hop_group(nhop_grp_list[i])

class fun_03_remove_nexthop_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        sys_logging("======create a nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        warmboot(self.client)
        try:
            sys_logging("======get the nexthop group attribute======")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove the nexthop group======")
            status = self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("======get the nexthop group attribute again======")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            sys_logging("======clean up======")

class fun_04_remove_no_exist_nexthop_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_group2 = 0x500000005
        warmboot(self.client)
        try: 
            sys_logging("======remove not exist nexthop group======")
            status = self.client.sai_thrift_remove_next_hop_group(nhop_group2)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)

            sys_logging("======get the exist nexthop group attribute======")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            assert (attrs.status == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            
class fun_05_get_nexthop_group_attribute_type_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        sys_logging("======create a nexthop group======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        
 
        warmboot(self.client)
        try:
            sys_logging("======get the nexthop group attribute type======")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_TYPE:
                    sys_logging("type = %d" %a.value.s32)
                    if SAI_NEXT_HOP_GROUP_TYPE_ECMP != a.value.s32:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_06_get_nexthop_group_attribute_counterid_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        type = SAI_COUNTER_TYPE_REGULAR
        counter_id1 = sai_thrift_create_counter(self.client, type)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sys_logging("======create 2 nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)

        nhop_group2 = sai_thrift_create_next_hop_group(self.client, counter_id = counter_id1)

        warmboot(self.client)
        try:
            sys_logging("======get the nexthop group attribute counter id======")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID:
                    sys_logging("0x%x" %a.value.oid)
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError()
                        
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group2)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_COUNTER_ID:
                    sys_logging("0x%x" %a.value.oid)
                    if counter_id1 != a.value.oid:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop_group(nhop_group2)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id1)


class fun_07_get_nexthop_group_attribute_count_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)

        sys_logging("======create a nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get the nexthop group attribute count and member list=====")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT:
                    if 0 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST:
                    assert (a.value.objlist.object_id_list == [])
                    
            sys_logging("======add 4 group memeber to the nexthop group======")
            nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
            nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
            nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
            nhop_gmember4 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
            
            nhop_gmember_list = [nhop_gmember3, nhop_gmember2, nhop_gmember1, nhop_gmember4]

            sys_logging("======get the nexthop group attribute count and member list again=====")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT:
                    if 4 != a.value.u32:
                        raise NotImplementedError() 
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST:
                    assert (a.value.objlist.object_id_list != [])
                    n=0
                    for i in a.value.objlist.object_id_list:
                        sys_logging("get the %dth group member oid" %(n+1))
                        sys_logging("the group member oid = 0x%x" %i)
                        assert (nhop_gmember_list[n] == i)
                        n = n+1

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember4)

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)

            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_08_create_nexthop_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr1, dmac2)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif2)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)

        warmboot(self.client)
        try:
            sys_logging("======create three nexthop group member======")
            nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
            nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
            nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
            sys_logging("nhop_gmember1 = 0x%x" %nhop_gmember1)
            sys_logging("nhop_gmember2 = 0x%x" %nhop_gmember2)
            sys_logging("nhop_gmember3 = 0x%x" %nhop_gmember3)
            assert (nhop_gmember1%0x100000000 == 0x2d)
            assert (nhop_gmember2%0x100000000 == 0x1002d)
            assert (nhop_gmember3%0x100000000 == 0x2002d)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)

            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr1, dmac2)

            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_09_create_max_nexthop_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        nhop_list = []
        nhop_gmember_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr4 = '10.10.10.4'
        ip_addr5 = '10.10.10.5'
        ip_addr6 = '10.10.10.6'
        ip_addr7 = '10.10.10.7'
        ip_addr8 = '10.10.10.8'
        ip_addr9 = '10.10.10.9'
        ip_addr10 = '10.10.10.10'
        ip_addr11 = '10.10.10.11'
        ip_addr12 = '10.10.10.12'
        ip_addr13 = '10.10.10.13'
        ip_addr14 = '10.10.10.14'
        ip_addr15 = '10.10.10.15'
        ip_addr16 = '10.10.10.16'
        ip_addr17 = '10.10.10.17'
        
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        ip_addr_list = [ip_addr1, ip_addr2, ip_addr3, ip_addr4, ip_addr5, ip_addr6, ip_addr7, ip_addr8, ip_addr9, ip_addr10, ip_addr11, ip_addr12, ip_addr13, ip_addr14, ip_addr15, ip_addr16]

        for a in ip_addr_list:
            sai_thrift_create_neighbor(self.client, addr_family, rif1, a, dmac1)
            nhop1 = sai_thrift_create_nhop(self.client, addr_family, a, rif1)
            nhop_list.append(nhop1)
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr17, dmac1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr17, rif1)    
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        sys_logging("======create 16 nexthop group member======")
        for i in range(16):
            nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop_list[i])
            sys_logging("nhop_gmember1 = 0x%x" %nhop_gmember1)
            nhop_gmember_list.append(nhop_gmember1)

        warmboot(self.client)
        try:
            sys_logging("======create a new nexthop group member======")
            nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)

            sys_logging("nhop_gmember2 = 0x%x" %nhop_gmember2)
            assert (nhop_gmember2 == SAI_NULL_OBJECT_ID)



        finally:
            sys_logging("======clean up======")
            for i in range(16):
                self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_list[i])

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            for i in range(16):
                self.client.sai_thrift_remove_next_hop(nhop_list[i])
                sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr_list[i], dmac1)
                
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr17, dmac1)

            self.client.sai_thrift_remove_router_interface(rif1)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_10_remove_nexthop_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'

        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        sys_logging("======create a nexthop group member======")
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        
        warmboot(self.client)
        try:
            sys_logging("======get the nexthop group member attribute======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            sys_logging("======remove the nexthop group member======")
            status = self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("======get the nexthop group member attribute again======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")            

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(nhop1)
     
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif1)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_11_remove_no_exist_nexthop_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'

        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        sys_logging("======create a nexthop group member======")
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = 0x40001002d
        nhop_gmember3 = 0x50001002d
        
        warmboot(self.client)
        try:
            sys_logging("======remove not exist nexthop group member======")
            status = self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            sys_logging("======get the nexthop group member attribute======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove another not exist nexthop group member======")
            status = self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            sys_logging("======get the nexthop group member attribute again======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove exist nexthop group member======")
            status = self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            sys_logging("status = %d" %attrs.status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("======get the nexthop group member attribute again======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(nhop1)
     
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif1)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_12_get_nexthop_group_member_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'

        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        sys_logging("======create a nexthop group member======")
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        
        warmboot(self.client)
        try:
            sys_logging("======get the nexthop group member attribute group id and nexthop id======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID:
                    sys_logging("nexthop group id = 0x%x" %a.value.oid)
                    if nhop_group1 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID:
                    sys_logging("nexthop id = 0x%x" %a.value.oid)
                    if nhop1 != a.value.oid:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(nhop1)
     
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif1)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_13_bulk_create_nexthop_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        nhop_list = []
        nhop_group_list = []
        weight_list = []
        nhop_gmember_list = []
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr4 = '10.10.10.4'
        ip_addr5 = '10.10.10.5'
        ip_addr6 = '10.10.10.6'
        ip_addr7 = '10.10.10.7'
        ip_addr8 = '10.10.10.8'
        ip_addr9 = '10.10.10.9'
        ip_addr10 = '10.10.10.10'
        ip_addr11 = '10.10.10.11'
        ip_addr12 = '10.10.10.12'
        ip_addr13 = '10.10.10.13'
        ip_addr14 = '10.10.10.14'
        ip_addr15 = '10.10.10.15'
        ip_addr16 = '10.10.10.16'
        
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        ip_addr_list = [ip_addr1, ip_addr2, ip_addr3, ip_addr4, ip_addr5, ip_addr6, ip_addr7, ip_addr8, ip_addr9, ip_addr10, ip_addr11, ip_addr12, ip_addr13, ip_addr14, ip_addr15, ip_addr16]

        for a in ip_addr_list:
            sai_thrift_create_neighbor(self.client, addr_family, rif1, a, dmac1)
            nhop1 = sai_thrift_create_nhop(self.client, addr_family, a, rif1)
            nhop_list.append(nhop1)
   
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        for i in range(16):
            nhop_group_list.append(nhop_group1)
            weight_list.append(None)

        warmboot(self.client)
        try:
            sys_logging("======bulk create 16 nexthop group member======")
            results = sai_thrift_create_next_hop_group_members(self.client, nhop_group_list, nhop_list, weight_list, mode)

            object_id_list = results[0]
            statuslist = results[1]
            for object_id in object_id_list:
                sys_logging("0x%x" %object_id)
                attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(object_id)
                assert (attrs.status == SAI_STATUS_SUCCESS)
            for status in statuslist:
                assert (status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            for object_id in object_id_list:
                self.client.sai_thrift_remove_next_hop_group_member(object_id)

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            for i in range(16):
                self.client.sai_thrift_remove_next_hop(nhop_list[i])
                sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr_list[i], dmac1)
                
            self.client.sai_thrift_remove_router_interface(rif1)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_14_bulk_create_stop_on_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        nhop_list = []
        nhop_group_list = []
        weight_list = []
        nhop_gmember_list = []
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr4 = '10.10.10.4'
        ip_addr5 = '10.10.10.5'
        ip_addr6 = '10.10.10.6'
        ip_addr7 = '10.10.10.7'
        ip_addr8 = '10.10.10.8'
        ip_addr9 = '10.10.10.9'
        ip_addr10 = '10.10.10.10'
        ip_addr11 = '10.10.10.11'
        ip_addr12 = '10.10.10.12'
        ip_addr13 = '10.10.10.13'
        ip_addr14 = '10.10.10.14'
        ip_addr15 = '10.10.10.15'
        ip_addr16 = '10.10.10.16'

        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        ip_addr_list = [ip_addr1, ip_addr2, ip_addr3, ip_addr4, ip_addr5, ip_addr6, ip_addr7, ip_addr8, ip_addr9, ip_addr10, ip_addr11, ip_addr12, ip_addr13, ip_addr14, ip_addr15, ip_addr16]

        for a in ip_addr_list:
            sai_thrift_create_neighbor(self.client, addr_family, rif1, a, dmac1)
            nhop1 = sai_thrift_create_nhop(self.client, addr_family, a, rif1)
            nhop_list.append(nhop1)
   
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        for i in range(16):
            nhop_group_list.append(nhop_group1)
            weight_list.append(None)
        nhop_group_list[8] = SAI_NULL_OBJECT_ID

        warmboot(self.client)
        try:
            sys_logging("======bulk create 16 nexthop group member with the 9th is error======")
            results = sai_thrift_create_next_hop_group_members(self.client, nhop_group_list, nhop_list, weight_list, mode)
            print results
            object_id_list = results[0]
            statuslist = results[1]
            for i in range(16):
                sys_logging("0x%x" %object_id_list[i])
                if i >= 8:
                    
                    attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(object_id_list[i])
                    print attrs.status
                    assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)       
                   
                else:
                    
                    attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(object_id_list[i])
                    print attrs.status
                    assert (attrs.status == SAI_STATUS_SUCCESS)
                    
        finally:
            sys_logging("======clean up======")
            for object_id in object_id_list:
                self.client.sai_thrift_remove_next_hop_group_member(object_id)

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            for i in range(16):
                self.client.sai_thrift_remove_next_hop(nhop_list[i])
                sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr_list[i], dmac1)
                
            self.client.sai_thrift_remove_router_interface(rif1)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_15_bulk_create_ignore_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        nhop_list = []
        nhop_group_list = []
        weight_list = []
        nhop_gmember_list = []
        mode = SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr4 = '10.10.10.4'
        ip_addr5 = '10.10.10.5'
        ip_addr6 = '10.10.10.6'
        ip_addr7 = '10.10.10.7'
        ip_addr8 = '10.10.10.8'
        ip_addr9 = '10.10.10.9'
        ip_addr10 = '10.10.10.10'
        ip_addr11 = '10.10.10.11'
        ip_addr12 = '10.10.10.12'
        ip_addr13 = '10.10.10.13'
        ip_addr14 = '10.10.10.14'
        ip_addr15 = '10.10.10.15'
        ip_addr16 = '10.10.10.16'
    
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        ip_addr_list = [ip_addr1, ip_addr2, ip_addr3, ip_addr4, ip_addr5, ip_addr6, ip_addr7, ip_addr8, ip_addr9, ip_addr10, ip_addr11, ip_addr12, ip_addr13, ip_addr14, ip_addr15, ip_addr16]

        for a in ip_addr_list:
            sai_thrift_create_neighbor(self.client, addr_family, rif1, a, dmac1)
            nhop1 = sai_thrift_create_nhop(self.client, addr_family, a, rif1)
            nhop_list.append(nhop1)
  
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        for i in range(16):
            nhop_group_list.append(nhop_group1)
            weight_list.append(None)
        nhop_group_list[8] = SAI_NULL_OBJECT_ID

        warmboot(self.client)
        try:
            sys_logging("======bulk create 16 nexthop group member with the 9th is error======")
            results = sai_thrift_create_next_hop_group_members(self.client, nhop_group_list, nhop_list, weight_list, mode)
            print results
            object_id_list = results[0]
            statuslist = results[1]
            for i in range(16):
                sys_logging("0x%x" %object_id_list[i])
                if i == 8:
                    attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(object_id_list[i])
                    print attrs.status
                    assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
                else:
                    attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(object_id_list[i])
                    print attrs.status
                    assert (attrs.status == SAI_STATUS_SUCCESS)
                    
        finally:
            sys_logging("======clean up======")
            for object_id in object_id_list:
                self.client.sai_thrift_remove_next_hop_group_member(object_id)

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            for i in range(16):
                self.client.sai_thrift_remove_next_hop(nhop_list[i])
                sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr_list[i], dmac1)

            self.client.sai_thrift_remove_router_interface(rif1)

            self.client.sai_thrift_remove_virtual_router(vr_id)


class fun_16_bulk_remove_nexthop_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        nhop_list = []
        nhop_group_list = []
        weight_list = []
        nhop_gmember_list = []
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr4 = '10.10.10.4'
        ip_addr5 = '10.10.10.5'
        ip_addr6 = '10.10.10.6'
        ip_addr7 = '10.10.10.7'
        ip_addr8 = '10.10.10.8'
        ip_addr9 = '10.10.10.9'
        ip_addr10 = '10.10.10.10'
        ip_addr11 = '10.10.10.11'
        ip_addr12 = '10.10.10.12'
        ip_addr13 = '10.10.10.13'
        ip_addr14 = '10.10.10.14'
        ip_addr15 = '10.10.10.15'
        ip_addr16 = '10.10.10.16'
 
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        ip_addr_list = [ip_addr1, ip_addr2, ip_addr3, ip_addr4, ip_addr5, ip_addr6, ip_addr7, ip_addr8, ip_addr9, ip_addr10, ip_addr11, ip_addr12, ip_addr13, ip_addr14, ip_addr15, ip_addr16]

        for a in ip_addr_list:
            sai_thrift_create_neighbor(self.client, addr_family, rif1, a, dmac1)
            nhop1 = sai_thrift_create_nhop(self.client, addr_family, a, rif1)
            nhop_list.append(nhop1)
   
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        for i in range(16):
            nhop_group_list.append(nhop_group1)
            weight_list.append(None)
        sys_logging("======bulk create 16 nexthop group member======")
        results = sai_thrift_create_next_hop_group_members(self.client, nhop_group_list, nhop_list, weight_list, mode)
        object_id_list = results[0]
        statuslist = results[1]
  
        warmboot(self.client)
        try:
            sys_logging("======bulk remove 16 nexthop group member======")
            status_list = sai_thrift_remove_next_hop_group_members(self.client, object_id_list, mode)

            sys_logging("======get the 16 nexthop group member attribute======")
            for object_id in object_id_list:
                sys_logging("0x%x" %object_id)
                attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(object_id)
                assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            for i in range(16):
                self.client.sai_thrift_remove_next_hop(nhop_list[i])
                sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr_list[i], dmac1)
                
            self.client.sai_thrift_remove_router_interface(rif1)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_17_bulk_remove_stop_on_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        nhop_list = []
        nhop_group_list = []
        weight_list = []
        nhop_gmember_list = []
        mode = SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr4 = '10.10.10.4'
        ip_addr5 = '10.10.10.5'
        ip_addr6 = '10.10.10.6'
        ip_addr7 = '10.10.10.7'
        ip_addr8 = '10.10.10.8'
        ip_addr9 = '10.10.10.9'
        ip_addr10 = '10.10.10.10'
        ip_addr11 = '10.10.10.11'
        ip_addr12 = '10.10.10.12'
        ip_addr13 = '10.10.10.13'
        ip_addr14 = '10.10.10.14'
        ip_addr15 = '10.10.10.15'
        ip_addr16 = '10.10.10.16'
        
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        ip_addr_list = [ip_addr1, ip_addr2, ip_addr3, ip_addr4, ip_addr5, ip_addr6, ip_addr7, ip_addr8, ip_addr9, ip_addr10, ip_addr11, ip_addr12, ip_addr13, ip_addr14, ip_addr15, ip_addr16]

        for a in ip_addr_list:
            sai_thrift_create_neighbor(self.client, addr_family, rif1, a, dmac1)
            nhop1 = sai_thrift_create_nhop(self.client, addr_family, a, rif1)
            nhop_list.append(nhop1)
   
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        for i in range(16):
            nhop_group_list.append(nhop_group1)
            weight_list.append(None)
        sys_logging("======bulk create 16 nexthop group member======")
        results = sai_thrift_create_next_hop_group_members(self.client, nhop_group_list, nhop_list, weight_list, mode)
        object_id_list = results[0]
        statuslist = results[1]

        member8 = object_id_list[8]

        object_id_list[8] = SAI_NULL_OBJECT_ID
        sys_logging("======bulk remove 16 nexthop group member with the 9th is error======")
        status_list = sai_thrift_remove_next_hop_group_members(self.client, object_id_list, mode)
        print status_list
        warmboot(self.client)
        try:
            object_id_list[8] = member8
            for i in range(16):
                if i < 8:
                    
                    attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(object_id_list[i])
                    print attrs.status
                    assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
                   
                else:
                    attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(object_id_list[i])
                    print attrs.status
                    assert (attrs.status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            for i in range(8,16):
                self.client.sai_thrift_remove_next_hop_group_member(object_id_list[i])
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            for i in range(16):
                self.client.sai_thrift_remove_next_hop(nhop_list[i])
                sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr_list[i], dmac1)

            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_18_bulk_remove_ignore_error_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        nhop_list = []
        nhop_group_list = []
        weight_list = []
        nhop_gmember_list = []
        mode = SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr4 = '10.10.10.4'
        ip_addr5 = '10.10.10.5'
        ip_addr6 = '10.10.10.6'
        ip_addr7 = '10.10.10.7'
        ip_addr8 = '10.10.10.8'
        ip_addr9 = '10.10.10.9'
        ip_addr10 = '10.10.10.10'
        ip_addr11 = '10.10.10.11'
        ip_addr12 = '10.10.10.12'
        ip_addr13 = '10.10.10.13'
        ip_addr14 = '10.10.10.14'
        ip_addr15 = '10.10.10.15'
        ip_addr16 = '10.10.10.16'
        
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        ip_addr_list = [ip_addr1, ip_addr2, ip_addr3, ip_addr4, ip_addr5, ip_addr6, ip_addr7, ip_addr8, ip_addr9, ip_addr10, ip_addr11, ip_addr12, ip_addr13, ip_addr14, ip_addr15, ip_addr16]

        for a in ip_addr_list:
            sai_thrift_create_neighbor(self.client, addr_family, rif1, a, dmac1)
            nhop1 = sai_thrift_create_nhop(self.client, addr_family, a, rif1)
            nhop_list.append(nhop1)
    
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        for i in range(16):
            nhop_group_list.append(nhop_group1)
            weight_list.append(None)
        sys_logging("======bulk create 16 nexthop group member======")
        results = sai_thrift_create_next_hop_group_members(self.client, nhop_group_list, nhop_list, weight_list, mode)
        object_id_list = results[0]
        statuslist = results[1]
        member8 = object_id_list[8]

        object_id_list[8] = SAI_NULL_OBJECT_ID
        sys_logging("======bulk remove 16 nexthop group member with the 9th is error======")
        status_list = sai_thrift_remove_next_hop_group_members(self.client, object_id_list, mode)
        print status_list
        warmboot(self.client)
        try:
            object_id_list[8] = member8
            for i in range(16):
                if i == 8:
                    attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(object_id_list[i])
                    print attrs.status
                    assert (attrs.status == SAI_STATUS_SUCCESS)

                else:
                    attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(object_id_list[i])
                    print attrs.status
                    assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop_group_member(member8)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            for i in range(16):
                self.client.sai_thrift_remove_next_hop(nhop_list[i])
                sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr_list[i], dmac1)

            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_01_ecmp_test(sai_base_test.ThriftInterfaceDataPlane):
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

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)

        hash_id_ecmp = 0x1C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
            
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

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
            port1_pkt_cnt = 0
            port2_pkt_cnt = 0
            src_ip = int(socket.inet_aton('192.168.0.1').encode('hex'),16)
            max_itrs = 20
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip+i)[2:].zfill(8).decode('hex'))
                print src_ip_addr
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:00:11:11:11:11',
                                ip_dst=ip_addr1_subnet,
                                ip_src=src_ip_addr,
                                ip_id=101,
                                ip_ttl=64)

                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src=src_ip_addr,
                                ip_id=101,
                                ip_ttl=63)

                self.ctc_send_packet( 2, str(pkt))
                #self.ctc_verify_packet( (exp_pkt6_1), 6)
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt1], [0, 1])
                if rcv_idx == 0:
                    port1_pkt_cnt = port1_pkt_cnt+1
                elif rcv_idx == 1:
                    port2_pkt_cnt = port2_pkt_cnt+1
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)
            sys_logging("port 2 receive packet conut is %d" %port2_pkt_cnt)
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)


