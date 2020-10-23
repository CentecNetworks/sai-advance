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


class fun_01_create_aps_nexthop_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        
        warmboot(self.client)
        try:
            sys_logging("======create 2 aps nexthop group======")
            nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
            nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
            sys_logging("aps nexthop group id = 0x%x" %nhop_group1)
            assert (nhop_group1%0x100000000 == 0x12005)
            sys_logging("aps nexthop group id = 0x%x" %nhop_group2)
            assert (nhop_group2%0x100000000 == 0x22005)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop_group(nhop_group2)
            
class fun_02_create_max_aps_nexthop_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        num = 1023
        nhop_grp_list = []
        sys_logging("======create 1024 aps nexthop group======")
        for i in range(num):
            nhop_group = sai_thrift_create_next_hop_protection_group(self.client)
            nhop_grp_list.append(nhop_group)
        
        warmboot(self.client)
        try:
            sys_logging("======create a new aps nexthop group======")
            nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
            sys_logging("nhop_group1 = 0x%x" %nhop_group1)
            assert (nhop_group1 == SAI_NULL_OBJECT_ID)
        finally:
            sys_logging("======clean up======")
            for i in range(num):
                self.client.sai_thrift_remove_next_hop_group(nhop_grp_list[i])

class fun_03_remove_aps_nexthop_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        warmboot(self.client)
        try:
            sys_logging("======get the aps nexthop group attribute======")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove the aps nexthop group======")
            status = self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("======get the aps nexthop group attribute again======")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            sys_logging("======clean up======")

class fun_04_remove_no_exist_aps_nexthop_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        self.client.sai_thrift_remove_next_hop_group(nhop_group1)
        warmboot(self.client)
        try: 
            sys_logging("======remove not exist aps nexthop group======")
            status = self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")

            
class fun_05_set_aps_nexthop_group_attribute_switchover_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======get the aps nexthop group attribute switchover======")
        attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                sys_logging("switchover = %d" %a.value.booldata)
 
        warmboot(self.client)
        try:
            sys_logging("======set the aps nexthop group attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            sys_logging("======get the nexthop group attribute switchover again======")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("switchover = %d" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()


            sys_logging("======set the aps nexthop group attribute switchover again======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=0)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            sys_logging("======get the nexthop group attribute switchover again======")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("switchover = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)


class fun_06_get_aps_nexthop_group_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)
        
        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        warmboot(self.client)
        try:

            sys_logging("======get the aps nexthop group attribute switchover again======")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("switchover = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT:
                    sys_logging("count = %d" %a.value.u32)
                    if 0 != a.value.u32:
                        raise NotImplementedError()                
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST:
                    print "switchover = ",
                    print a.value.objlist.object_id_list
                    #sys_logging("switchover = %d" %a.value.booldata)
                    if [] != a.value.objlist.object_id_list:
                        raise NotImplementedError()  
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_TYPE:
                    sys_logging("group type = %d" %a.value.s32)
                    if SAI_NEXT_HOP_GROUP_TYPE_PROTECTION != a.value.s32:
                        raise NotImplementedError()
                        
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)




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

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get the aps nexthop group attribute count and member list=====")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT:
                    if 0 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST:
                    assert (a.value.objlist.object_id_list == [])
                    
            sys_logging("======add 2 aps group memeber to the nexthop group======")
            nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
            nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

            
            nhop_gmember_list = [nhop_gmember_w, nhop_gmember_p]
            print nhop_gmember_list

            sys_logging("======get the aps nexthop group attribute count and member list again=====")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT:
                    if 2 != a.value.u32:
                        raise NotImplementedError() 
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST:
                    assert (a.value.objlist.object_id_list != [])
                    n=0
                    for i in a.value.objlist.object_id_list:
                        sys_logging("get the %dth group member oid" %(n+1))
                        sys_logging("the group member oid = 0x%x" %i)
                        assert (nhop_gmember_list[n] == i)
                        n = n+1

            sys_logging("======remove working group memeber to the nexthop group======")
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            
            sys_logging("======get the aps nexthop group attribute count and member list again=====")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT:
                    if 1 != a.value.u32:
                        raise NotImplementedError() 
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST:
                    assert (a.value.objlist.object_id_list != [])
                    n=0
                    for i in a.value.objlist.object_id_list:
                        sys_logging("get the %dth group member oid" %(n+1))
                        sys_logging("the group member oid = 0x%x" %i)
                        assert (nhop_gmember_p == i)
                        n = n+1

            sys_logging("======remove protection group memeber to the nexthop group======")
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            
            sys_logging("======get the aps nexthop group attribute count and member list again=====")
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_COUNT:
                    if 0 != a.value.u32:
                        raise NotImplementedError() 
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_NEXT_HOP_MEMBER_LIST:
                    assert (a.value.objlist.object_id_list == [])

        finally:
            sys_logging("======clean up======")
            
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
        ip_addr2 = '10.10.10.2'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        warmboot(self.client)
        try:
                    
            sys_logging("======add 2 aps group memeber to the nexthop group======")
            nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
            nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

            sys_logging("aps nexthop group working member id = 0x%x" %nhop_gmember_w)
            assert (nhop_gmember_w%0x100000000 == 0x202d)
            sys_logging("aps nexthop group protection member id = 0x%x" %nhop_gmember_p)
            assert (nhop_gmember_p%0x100000000 == 0x1002d)
            
        finally:
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)

            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)

            self.client.sai_thrift_remove_virtual_router(vr_id)



class fun_09_remove_aps_nexthop_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
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

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        warmboot(self.client)
        try:
            sys_logging("======get the aps nexthop group member attribute======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember_w)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember_p)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            sys_logging("======remove 2 aps nexthop group member======")
            status = self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("======get the nexthop group member attribute again======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember_w)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember_p)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")            

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)

            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            
class fun_10_remove_no_exist_aps_nexthop_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
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

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
        self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
        
        warmboot(self.client)
        try:
            sys_logging("======remove 2 aps nexthop group member======")
            status = self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            status = self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)

            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_11_get_nexthop_aps_group_member_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
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

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        
        warmboot(self.client)
        try:
            sys_logging("======get the aps nexthop group working member attribute======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember_w)
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
                if a.id == SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE:
                    sys_logging("configured role = 0x%x" %a.value.s32)
                    if SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_GROUP_MEMBER_ATTR_OBSERVED_ROLE:
                    sys_logging("observed role = 0x%x" %a.value.s32)
                    if SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_ACTIVE != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("======get the aps nexthop group protection member attribute======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember_p)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_GROUP_ID:
                    sys_logging("nexthop group id = 0x%x" %a.value.oid)
                    if nhop_group1 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_GROUP_MEMBER_ATTR_NEXT_HOP_ID:
                    sys_logging("nexthop id = 0x%x" %a.value.oid)
                    if nhop2 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_GROUP_MEMBER_ATTR_CONFIGURED_ROLE:
                    sys_logging("configured role = 0x%x" %a.value.s32)
                    if SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_GROUP_MEMBER_ATTR_OBSERVED_ROLE:
                    sys_logging("observed role = 0x%x" %a.value.s32)
                    if SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_INACTIVE != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("======set the aps nexthop group attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)       

            sys_logging("======get the aps nexthop group working member attribute again======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember_w)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_MEMBER_ATTR_OBSERVED_ROLE:
                    sys_logging("observed role = 0x%x" %a.value.s32)
                    if SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_INACTIVE != a.value.s32:
                        raise NotImplementedError()
                        
            sys_logging("======get the aps nexthop group protection member attribute again======")
            attrs = self.client.sai_thrift_get_next_hop_group_member_attribute(nhop_gmember_p)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_MEMBER_ATTR_OBSERVED_ROLE:
                    sys_logging("observed role = 0x%x" %a.value.s32)
                    if SAI_NEXT_HOP_GROUP_MEMBER_OBSERVED_ROLE_ACTIVE != a.value.s32:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)

            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)

            self.client.sai_thrift_remove_virtual_router(vr_id)



class scenario_01_route_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 30
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:66'
        dmac3 = '00:11:22:33:44:77'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port2])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        sai_thrift_create_fdb_bport(self.client, bridge_id, dmac1, bport1_id, SAI_PACKET_ACTION_FORWARD)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id2)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_addr2, dmac2)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id3)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

   
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
        exp_pkt2 = simple_tcp_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt3 = simple_tcp_packet(
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                ip_dst='10.10.10.30',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======port type rif send dest ip hit v4 packet to working nexthop======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            sys_logging("======set the aps nexthop group attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr) 

            sys_logging("======port type rif send dest ip hit v4 packet to protection nexthop======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [2])

            sys_logging("======set neighbor dst mac to '00:11:22:33:44:77'======")
            addr = sai_thrift_ip_t(ip4=ip_addr2)
            ipaddr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id3, ip_address=ipaddr)
            attr_value = sai_thrift_attribute_value_t(mac=dmac3)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])
            

            sys_logging("======set the aps nexthop group attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=0)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            sys_logging("======port type rif send dest ip hit v4 packet to working nexthop======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_addr2, dmac2)
            
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            sai_thrift_delete_fdb(self.client, bridge_id, dmac1, bport1_id)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport1_id, port2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_02_basic_mpls_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        ip_da2 = '5.5.5.2'
        ip_da3 = '5.5.5.3'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        dmac3 = '00:55:55:55:55:77'
        
        ip_addr1_subnet = '10.10.10.1'
        ip_addr2_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 100
        label2 = 200
        label3 = 300

        label_list1 = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        #label_list = []
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_da3, rif_id3)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        #pdb.set_trace()
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id4, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True)   
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True) 
        

        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls1 = [{'label':100,'tc':0,'ttl':32,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
                                
        mpls1_p = [{'label':200,'tc':0,'ttl':32,'s':1}] 
        pkt2_p = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1_p,
                                inner_frame = ip_only_pkt1) 
                                
        mpls2 = [{'label':100,'tc':0,'ttl':100,'s':1}]   
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr2_subnet,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2)

        mpls2_p = [{'label':200,'tc':0,'ttl':100,'s':1}]
        pkt3_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls2_p,
                                inner_frame = ip_only_pkt2)

                                
        pkt4 = simple_tcp_packet(eth_dst=dmac3,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=99)

        warmboot(self.client)
        #pdb.set_trace()
        try:
            self.ctc_send_packet( 3, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [3])

            self.ctc_send_packet( 1, str(pkt3_p))
            self.ctc_verify_no_packet( pkt4, 3)

            sys_logging("======set the aps nexthop group attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            self.ctc_send_packet( 3, str(pkt1))
            self.ctc_verify_packets( pkt2_p, [2])

            self.ctc_send_packet( 2, str(pkt3_p))
            self.ctc_verify_packets( pkt4, [3])

            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_no_packet( pkt4, 3)

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            #pdb.set_trace()
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_03_basic_mpls_inactive_not_discard_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        ip_da2 = '5.5.5.2'
        ip_da3 = '5.5.5.3'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        dmac3 = '00:55:55:55:55:77'
        
        ip_addr1_subnet = '10.10.10.1'
        ip_addr2_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 100
        label2 = 200
        label3 = 300

        label_list1 = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        #label_list = []
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_da3, rif_id3)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        #pdb.set_trace()
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id4, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY)   
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY) 
        

        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls1 = [{'label':100,'tc':0,'ttl':32,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
                                
        mpls1_p = [{'label':200,'tc':0,'ttl':32,'s':1}] 
        pkt2_p = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1_p,
                                inner_frame = ip_only_pkt1) 
                                
        mpls2 = [{'label':100,'tc':0,'ttl':100,'s':1}]   
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr2_subnet,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2)

        mpls2_p = [{'label':200,'tc':0,'ttl':100,'s':1}]
        pkt3_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls2_p,
                                inner_frame = ip_only_pkt2)

                                
        pkt4 = simple_tcp_packet(eth_dst=dmac3,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=99)

        warmboot(self.client)
        #pdb.set_trace()
        try:
            self.ctc_send_packet( 3, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [3])

            self.ctc_send_packet( 1, str(pkt3_p))
            self.ctc_verify_packets( pkt4, [3])

            sys_logging("======set the aps nexthop group attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            self.ctc_send_packet( 3, str(pkt1))
            self.ctc_verify_packets( pkt2_p, [2])

            self.ctc_send_packet( 2, str(pkt3_p))
            self.ctc_verify_packets( pkt4, [3])

            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packets( pkt4, [3])

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            #pdb.set_trace()
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_04_vpls_lsp_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop3 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list3, next_level_nhop_oid=nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id4, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id3, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_label_stack_p = [{'label':label2,'tc':0,'ttl':32,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt2_p = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p,
                                inner_frame = mpls_inner_pkt)


        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)

        mpls_label_stack1_p = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt3_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1_p,
                                inner_frame = mpls_inner_pkt1)

                                
        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])
            self.ctc_send_packet( 1, str(pkt3_p))
            self.ctc_verify_no_packet( pkt4, 2)

            sys_logging("======set the aps nexthop group attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2_p, [3])

            #pw to ac
            self.ctc_send_packet( 3, str(pkt3_p))
            self.ctc_verify_packets( pkt4, [2])
            self.ctc_send_packet( 3, str(pkt3))
            self.ctc_verify_no_packet( pkt4, 2)
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_inseg_entry(mpls3) 

            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_05_vpls_pw_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop1)
        next_hop3 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list3, next_level_nhop_oid=next_hop1)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id4, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id3, packet_action, tunnel_id=tunnel_id1, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True)  
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id3, packet_action, tunnel_id=tunnel_id1, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True)

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        frr_bport = sai_thrift_create_bridge_frr_port(self.client, frr_nhp_grp_id=nhop_group1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, frr_bport, mac_action)

        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_label_stack_p = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt2_p = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p,
                                inner_frame = mpls_inner_pkt)


        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)

        mpls_label_stack1_p = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt3_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1_p,
                                inner_frame = mpls_inner_pkt1)

                                
        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])
            self.ctc_send_packet( 1, str(pkt3_p))
            self.ctc_verify_no_packet( pkt4, 2)

            sys_logging("======set the aps nexthop group attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2_p, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3_p))
            self.ctc_verify_packets( pkt4, [2])
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_no_packet( pkt4, 2)
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(frr_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_inseg_entry(mpls3) 
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_06_vpls_2_level_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        ip_da3 = '5.5.5.4'
        ip_da4 = '5.5.5.5'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        dmac3 = '00:55:55:55:55:77'
        dmac4 = '00:55:55:55:55:88'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label3 = 300
        label4 = 400
        label5 = 500
        label6 = 600

        label_list1 = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        label_list4 = [(label4<<12) | 32]
        label_list5 = [(label5<<12) | 32]
        label_list6 = [(label6<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a aps nexthop group======")
        nhop_group3 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember3_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group3, next_hop5, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember3_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group3, next_hop6, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group2, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group2, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label5, pop_nums, None, rif_id5, packet_action, tunnel_id=tunnel_id1, frr_nhp_grp=nhop_group3, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True)  
        sai_thrift_create_inseg_entry(self.client, label6, pop_nums, None, rif_id5, packet_action, tunnel_id=tunnel_id1, frr_nhp_grp=nhop_group3, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True)

        bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        frr_bport = sai_thrift_create_bridge_frr_port(self.client, frr_nhp_grp_id=nhop_group3, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, frr_bport, mac_action)

        pkt_label1 = {'label':label1,'tc':0,'ttl':32,'s':0}
        pkt_label2 = {'label':label2,'tc':0,'ttl':32,'s':0}
        pkt_label3 = {'label':label3,'tc':0,'ttl':32,'s':0}
        pkt_label4 = {'label':label4,'tc':0,'ttl':32,'s':0}
        pkt_label5 = {'label':label5,'tc':0,'ttl':32,'s':1}
        pkt_label6 = {'label':label6,'tc':0,'ttl':32,'s':1}
        mpls_label_stack_w1_w = [pkt_label1, pkt_label5]
        mpls_label_stack_p1_w = [pkt_label2, pkt_label5]
        mpls_label_stack_w2_p = [pkt_label3, pkt_label6]
        mpls_label_stack_p2_p = [pkt_label4, pkt_label6]
        
        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt2_w1_w = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w1_w,
                                inner_frame = mpls_inner_pkt)

        pkt2_p1_w = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p1_w,
                                inner_frame = mpls_inner_pkt)

        pkt2_w2_p = simple_mpls_packet(
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w2_p,
                                inner_frame = mpls_inner_pkt)

        pkt2_p2_p = simple_mpls_packet(
                                eth_dst=dmac4,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p2_p,
                                inner_frame = mpls_inner_pkt)


        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt3_w1_w = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w1_w,
                                inner_frame = mpls_inner_pkt1)

        pkt3_p1_w = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p1_w,
                                inner_frame = mpls_inner_pkt1)

        pkt3_w2_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w2_p,
                                inner_frame = mpls_inner_pkt1)

        pkt3_p2_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p2_p,
                                inner_frame = mpls_inner_pkt1)

                                
        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w1_w, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3_w1_w))
            self.ctc_verify_packets( pkt4, [0])
            self.ctc_send_packet( 1, str(pkt3_p1_w))
            self.ctc_verify_no_packet( pkt4, 0)

            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            #ac to pw
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_p1_w, [2])

            #pw to ac
            self.ctc_send_packet( 2, str(pkt3_p1_w))
            self.ctc_verify_packets( pkt4, [0])
            self.ctc_send_packet( 2, str(pkt3_w1_w))
            self.ctc_verify_no_packet( pkt4, 0)

            sys_logging("======set the pw aps nexthop group3 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group3, nhop_group_atr)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w2_p, [3])

            #pw to ac
            self.ctc_send_packet( 3, str(pkt3_w2_p))
            self.ctc_verify_packets( pkt4, [0])

            sys_logging("======set the lsp aps nexthop group2 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group2, nhop_group_atr)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_p2_p, [4])

            #pw to ac
            self.ctc_send_packet( 4, str(pkt3_p2_p))
            self.ctc_verify_packets( pkt4, [0])

            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=0)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)
            sys_logging("======set the pw aps nexthop group3 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=0)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group3, nhop_group_atr)

            #ac to pw
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w1_w, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3_w1_w))
            self.ctc_verify_packets( pkt4, [0])
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port1)
            self.client.sai_thrift_remove_bridge_port(frr_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            mpls4 = sai_thrift_inseg_entry_t(label4)
            mpls5 = sai_thrift_inseg_entry_t(label5) 
            mpls6 = sai_thrift_inseg_entry_t(label6)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_inseg_entry(mpls3) 
            self.client.sai_thrift_remove_inseg_entry(mpls4)
            self.client.sai_thrift_remove_inseg_entry(mpls5)  
            self.client.sai_thrift_remove_inseg_entry(mpls6) 

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group3)
            
            self.client.sai_thrift_remove_next_hop(next_hop5)
            self.client.sai_thrift_remove_next_hop(next_hop6)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop4)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_router_interface(rif_id6)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_07_vpws_lsp_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop3 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list3, next_level_nhop_oid=nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id4, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id3, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, admin_state=False)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)
        

        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)

        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)

        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_label_stack_p = [{'label':label2,'tc':0,'ttl':32,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt2_p = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p,
                                inner_frame = mpls_inner_pkt)


        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)

        mpls_label_stack1_p = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt3_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1_p,
                                inner_frame = mpls_inner_pkt1)

                                
        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])
            
            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])
            self.ctc_send_packet( 1, str(pkt3_p))
            self.ctc_verify_no_packet( pkt4, 2)

            sys_logging("======set the aps nexthop group attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2_p, [3])

            #pw to ac
            self.ctc_send_packet( 3, str(pkt3_p))
            self.ctc_verify_packets( pkt4, [2])
            self.ctc_send_packet( 3, str(pkt3))
            self.ctc_verify_no_packet( pkt4, 2)
            
        finally:
            sys_logging("======clean up======")
            bport_attr_value = sai_thrift_attribute_value_t(booldata=False)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)

            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_inseg_entry(mpls3) 

            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_08_vpws_pw_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop1)
        next_hop3 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list3, next_level_nhop_oid=next_hop1)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id4, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id3, packet_action, tunnel_id=tunnel_id1, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True)  
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id3, packet_action, tunnel_id=tunnel_id1, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True)

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, admin_state=False)
        frr_bport = sai_thrift_create_bridge_frr_port(self.client, frr_nhp_grp_id=nhop_group1, bridge_id=bridge_id, admin_state=False)
        

        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=frr_bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(frr_bport, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)

        self.client.sai_thrift_set_bridge_port_attribute(frr_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        
        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_label_stack_p = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt2_p = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p,
                                inner_frame = mpls_inner_pkt)


        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)

        mpls_label_stack1_p = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':32,'s':1}]
        pkt3_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1_p,
                                inner_frame = mpls_inner_pkt1)

                                
        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])
            
            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])
            self.ctc_send_packet( 1, str(pkt3_p))
            self.ctc_verify_no_packet( pkt4, 2)

            sys_logging("======set the aps nexthop group attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2_p, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3_p))
            self.ctc_verify_packets( pkt4, [2])
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_no_packet( pkt4, 2)
            
        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(frr_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_inseg_entry(mpls3) 
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_09_vpws_2_level_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        ip_da3 = '5.5.5.4'
        ip_da4 = '5.5.5.5'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        dmac3 = '00:55:55:55:55:77'
        dmac4 = '00:55:55:55:55:88'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label3 = 300
        label4 = 400
        label5 = 500
        label6 = 600

        label_list1 = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        label_list4 = [(label4<<12) | 32]
        label_list5 = [(label5<<12) | 32]
        label_list6 = [(label6<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a aps nexthop group======")
        nhop_group3 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember3_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group3, next_hop5, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember3_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group3, next_hop6, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group2, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group2, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label5, pop_nums, None, rif_id5, packet_action, tunnel_id=tunnel_id1, frr_nhp_grp=nhop_group3, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True)  
        sai_thrift_create_inseg_entry(self.client, label6, pop_nums, None, rif_id5, packet_action, tunnel_id=tunnel_id1, frr_nhp_grp=nhop_group3, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True)

        bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id, admin_state=False)
        frr_bport = sai_thrift_create_bridge_frr_port(self.client, frr_nhp_grp_id=nhop_group3, bridge_id=bridge_id, admin_state=False)
        

        bport_attr_value = sai_thrift_attribute_value_t(oid=frr_bport)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        
        bport_attr_value = sai_thrift_attribute_value_t(oid=bport)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(frr_bport, bport_attr)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)

        self.client.sai_thrift_set_bridge_port_attribute(frr_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)

        pkt_label1 = {'label':label1,'tc':0,'ttl':32,'s':0}
        pkt_label2 = {'label':label2,'tc':0,'ttl':32,'s':0}
        pkt_label3 = {'label':label3,'tc':0,'ttl':32,'s':0}
        pkt_label4 = {'label':label4,'tc':0,'ttl':32,'s':0}
        pkt_label5 = {'label':label5,'tc':0,'ttl':32,'s':1}
        pkt_label6 = {'label':label6,'tc':0,'ttl':32,'s':1}
        mpls_label_stack_w1_w = [pkt_label1, pkt_label5]
        mpls_label_stack_p1_w = [pkt_label2, pkt_label5]
        mpls_label_stack_w2_p = [pkt_label3, pkt_label6]
        mpls_label_stack_p2_p = [pkt_label4, pkt_label6]
        
        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt2_w1_w = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w1_w,
                                inner_frame = mpls_inner_pkt)

        pkt2_p1_w = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p1_w,
                                inner_frame = mpls_inner_pkt)

        pkt2_w2_p = simple_mpls_packet(
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w2_p,
                                inner_frame = mpls_inner_pkt)

        pkt2_p2_p = simple_mpls_packet(
                                eth_dst=dmac4,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p2_p,
                                inner_frame = mpls_inner_pkt)


        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt3_w1_w = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w1_w,
                                inner_frame = mpls_inner_pkt1)

        pkt3_p1_w = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p1_w,
                                inner_frame = mpls_inner_pkt1)

        pkt3_w2_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w2_p,
                                inner_frame = mpls_inner_pkt1)

        pkt3_p2_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p2_p,
                                inner_frame = mpls_inner_pkt1)

                                
        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w1_w, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3_w1_w))
            self.ctc_verify_packets( pkt4, [0])
            self.ctc_send_packet( 1, str(pkt3_p1_w))
            self.ctc_verify_no_packet( pkt4, 0)

            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            #ac to pw
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_p1_w, [2])

            #pw to ac
            self.ctc_send_packet( 2, str(pkt3_p1_w))
            self.ctc_verify_packets( pkt4, [0])
            self.ctc_send_packet( 2, str(pkt3_w1_w))
            self.ctc_verify_no_packet( pkt4, 0)

            sys_logging("======set the pw aps nexthop group3 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group3, nhop_group_atr)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w2_p, [3])

            #pw to ac
            self.ctc_send_packet( 3, str(pkt3_w2_p))
            self.ctc_verify_packets( pkt4, [0])

            sys_logging("======set the lsp aps nexthop group2 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group2, nhop_group_atr)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_p2_p, [4])

            #pw to ac
            self.ctc_send_packet( 4, str(pkt3_p2_p))
            self.ctc_verify_packets( pkt4, [0])

            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=0)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)
            sys_logging("======set the pw aps nexthop group3 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=0)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group3, nhop_group_atr)

            #ac to pw
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w1_w, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3_w1_w))
            self.ctc_verify_packets( pkt4, [0])
            
        finally:
            sys_logging("======clean up======")
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port1)
            self.client.sai_thrift_remove_bridge_port(frr_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            mpls4 = sai_thrift_inseg_entry_t(label4)
            mpls5 = sai_thrift_inseg_entry_t(label5) 
            mpls6 = sai_thrift_inseg_entry_t(label6)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_inseg_entry(mpls3) 
            self.client.sai_thrift_remove_inseg_entry(mpls4)
            self.client.sai_thrift_remove_inseg_entry(mpls5)  
            self.client.sai_thrift_remove_inseg_entry(mpls6) 

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group3)
            
            self.client.sai_thrift_remove_next_hop(next_hop5)
            self.client.sai_thrift_remove_next_hop(next_hop6)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop4)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_router_interface(rif_id6)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_10_l3vpn_lsp_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        ip_da2 = '5.5.5.2'
        ip_da3 = '5.5.5.3'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        dmac3 = '00:55:55:55:55:77'
        ip_addr1_subnet = '10.10.10.1'
        ip_addr2_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 100
        label2 = 200
        label3 = 300

        label_list = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)

        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        next_hop1_p = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        
        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1_p, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop2 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list3, next_level_nhop_oid=nhop_group1)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_da3, rif_id3)
        
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id4, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True)

        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id5, packet_action, tunnel_id=tunnel_id)


        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_dscp=16,
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls1 = [{'label':100,'tc':0,'ttl':32,'s':0}, {'label':300,'tc':0,'ttl':63,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_dscp=16,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
        mpls1_p = [{'label':200,'tc':0,'ttl':32,'s':0}, {'label':300,'tc':0,'ttl':63,'s':1}] 
        pkt2_p = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1_p,
                                inner_frame = ip_only_pkt1) 
                                
        mpls2 = [{'label':100,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]   
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr2_subnet,
                                ip_ttl=64,
                                ip_id=105,
                                ip_ihl=5
                                )
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2)
        mpls2_p = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}] 
        pkt3_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls2_p,
                                inner_frame = ip_only_pkt2)
                                
        pkt4 = simple_tcp_packet(eth_dst=dmac3,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=99)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 3, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [3])
            self.ctc_send_packet( 1, str(pkt3_p))
            self.ctc_verify_no_packet( pkt4, 3)

            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            self.ctc_send_packet( 3, str(pkt1))
            self.ctc_verify_packets( pkt2_p, [2])

            self.ctc_send_packet( 2, str(pkt3_p))
            self.ctc_verify_packets( pkt4, [3])
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_no_packet( pkt4, 3)

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_inseg_entry(mpls3)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(next_hop1_p)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)


class scenario_11_l3vpn_pw_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        ip_da2 = '5.5.5.2'
        ip_da3 = '5.5.5.3'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        dmac3 = '00:55:55:55:55:77'
        ip_addr1_subnet = '10.10.10.1'
        ip_addr2_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 100
        label2 = 200
        label3 = 300

        label_list = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)

        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        next_hop2 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_level_nhop_oid=next_hop1)
        next_hop2_p = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list3, next_level_nhop_oid=next_hop1)
        
        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2_p, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_da3, rif_id3)
        
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id4, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True)

        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id5, packet_action, tunnel_id=tunnel_id, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True)

        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_dscp=16,
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls1 = [{'label':100,'tc':0,'ttl':32,'s':0}, {'label':200,'tc':0,'ttl':63,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_dscp=16,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
        mpls1_p = [{'label':100,'tc':0,'ttl':32,'s':0}, {'label':300,'tc':0,'ttl':63,'s':1}] 
        pkt2_p = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1_p,
                                inner_frame = ip_only_pkt1) 
                                
        mpls2 = [{'label':100,'tc':3,'ttl':100,'s':0}, {'label':200,'tc':3,'ttl':50,'s':1}]   
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr2_subnet,
                                ip_ttl=64,
                                ip_id=105,
                                ip_ihl=5
                                )
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2)
        mpls2_p = [{'label':100,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}] 
        pkt3_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls2_p,
                                inner_frame = ip_only_pkt2)
                                
        pkt4 = simple_tcp_packet(eth_dst=dmac3,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=99)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 3, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [3])
            self.ctc_send_packet( 1, str(pkt3_p))
            self.ctc_verify_no_packet( pkt4, 3)

            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            self.ctc_send_packet( 3, str(pkt1))
            self.ctc_verify_packets( pkt2_p, [1])

            self.ctc_send_packet( 1, str(pkt3_p))
            self.ctc_verify_packets( pkt4, [3])
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_no_packet( pkt4, 3)

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_inseg_entry(mpls3)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop2_p)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)


class scenario_12_l3vpn_two_level_aps_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        ip_da2 = '5.5.5.2'
        ip_da3 = '5.5.5.3'
        ip_da4 = '5.5.5.4'
        ip_da5 = '5.5.5.5'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        dmac3 = '00:55:55:55:55:77'
        dmac4 = '00:55:55:55:55:88'
        dmac5 = '00:55:55:55:55:99'
        ip_addr1_subnet = '10.10.10.1'
        ip_addr2_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 100
        label2 = 200
        label3 = 300
        label4 = 400
        label5 = 500
        label6 = 600

        label_list = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        label_list4 = [(label4<<12) | 32]
        label_list5 = [(label5<<12) | 32]
        label_list6 = [(label6<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id5, ip_da5, dmac5)

        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        next_hop1_p = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        
        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1_p, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop2_p = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)
        
        sys_logging("======create a aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop2_p, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop3 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop3_p = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a aps nexthop group======")
        nhop_group3 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember3_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group3, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember3_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group3, next_hop3_p, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop4 = sai_thrift_create_nhop(self.client, addr_family, ip_da5, rif_id5)
        
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group3)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop4)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True, pop_ttl_mode = SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True, pop_ttl_mode = SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE)

        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group2, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True, pop_ttl_mode = SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE)
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group2, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True, pop_ttl_mode = SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE)
        
        sai_thrift_create_inseg_entry(self.client, label5, pop_nums, None, rif_id6, packet_action, tunnel_id=tunnel_id, frr_nhp_grp=nhop_group3, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True)
        sai_thrift_create_inseg_entry(self.client, label6, pop_nums, None, rif_id6, packet_action, tunnel_id=tunnel_id, frr_nhp_grp=nhop_group3, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True)

        pkt_label1 = {'label':label1,'tc':0,'ttl':32,'s':0}
        pkt_label2 = {'label':label2,'tc':0,'ttl':32,'s':0}
        pkt_label3 = {'label':label3,'tc':0,'ttl':32,'s':0}
        pkt_label4 = {'label':label4,'tc':0,'ttl':32,'s':0}
        pkt_label5 = {'label':label5,'tc':0,'ttl':63,'s':1}
        pkt_label6 = {'label':label6,'tc':0,'ttl':63,'s':1}
        mpls_label_stack_w1_w = [pkt_label1, pkt_label5]
        mpls_label_stack_p1_w = [pkt_label2, pkt_label5]
        mpls_label_stack_w2_p = [pkt_label3, pkt_label6]
        mpls_label_stack_p2_p = [pkt_label4, pkt_label6]

        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_dscp=16,
                               ip_id=105,
                               ip_ttl=64)
                               
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_dscp=16,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2_w1_w = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w1_w,
                                inner_frame = ip_only_pkt1) 
        pkt2_p1_w = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p1_w,
                                inner_frame = ip_only_pkt1) 
        pkt2_w2_p = simple_mpls_packet(
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w2_p,
                                inner_frame = ip_only_pkt1) 
        pkt2_p2_p = simple_mpls_packet(
                                eth_dst=dmac4,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p2_p,
                                inner_frame = ip_only_pkt1) 

                                
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr2_subnet,
                                ip_ttl=64,
                                ip_id=105,
                                ip_ihl=5
                                )
        pkt3_w1_w = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w1_w,
                                inner_frame = ip_only_pkt2)
        pkt3_p1_w = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p1_w,
                                inner_frame = ip_only_pkt2)
        pkt3_w2_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w2_p,
                                inner_frame = ip_only_pkt2)
        pkt3_p2_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p2_p,
                                inner_frame = ip_only_pkt2)                                
        pkt4 = simple_tcp_packet(eth_dst=dmac5,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=63)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 4, str(pkt1))
            self.ctc_verify_packets( pkt2_w1_w, [0])

            self.ctc_send_packet( 0, str(pkt3_w1_w))
            self.ctc_verify_packets( pkt4, [4])
            self.ctc_send_packet( 0, str(pkt3_p1_w))
            self.ctc_verify_no_packet( pkt4, 4)

            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            self.ctc_send_packet( 4, str(pkt1))
            self.ctc_verify_packets( pkt2_p1_w, [1])

            self.ctc_send_packet( 1, str(pkt3_p1_w))
            self.ctc_verify_packets( pkt4, [4])

            sys_logging("======set the lsp aps nexthop group3 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group3, nhop_group_atr)

            self.ctc_send_packet( 4, str(pkt1))
            self.ctc_verify_packets( pkt2_w2_p, [2])

            self.ctc_send_packet( 2, str(pkt3_w2_p))
            self.ctc_verify_packets( pkt4, [4])
            self.ctc_send_packet( 2, str(pkt3_p1_w))
            self.ctc_verify_no_packet( pkt4, 4)

            sys_logging("======set the lsp aps nexthop group2 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group2, nhop_group_atr)

            self.ctc_send_packet( 4, str(pkt1))
            self.ctc_verify_packets( pkt2_p2_p, [3])

            self.ctc_send_packet( 3, str(pkt3_p2_p))
            self.ctc_verify_packets( pkt4, [4])

            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=0)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)
            sys_logging("======set the lsp aps nexthop group3 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=0)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group3, nhop_group_atr)

            self.ctc_send_packet( 4, str(pkt1))
            self.ctc_verify_packets( pkt2_w1_w, [0])

            self.ctc_send_packet( 0, str(pkt3_w1_w))
            self.ctc_verify_packets( pkt4, [4])
            self.ctc_send_packet( 0, str(pkt3_p2_p))
            self.ctc_verify_no_packet( pkt4, 4)
            self.ctc_send_packet( 3, str(pkt3_p2_p))
            self.ctc_verify_no_packet( pkt4, 4)


        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3)
            mpls4 = sai_thrift_inseg_entry_t(label4) 
            mpls5 = sai_thrift_inseg_entry_t(label5) 
            mpls6 = sai_thrift_inseg_entry_t(label6)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_inseg_entry(mpls3)
            self.client.sai_thrift_remove_inseg_entry(mpls4)
            self.client.sai_thrift_remove_inseg_entry(mpls5)
            self.client.sai_thrift_remove_inseg_entry(mpls6)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group3)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop4)
            self.client.sai_thrift_remove_next_hop(next_hop4)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3_p)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3_w)
            self.client.sai_thrift_remove_next_hop_group(nhop_group3)
            self.client.sai_thrift_remove_next_hop(next_hop3_p)
            self.client.sai_thrift_remove_next_hop(next_hop3)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2_p)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2_w)
            self.client.sai_thrift_remove_next_hop_group(nhop_group2)
            self.client.sai_thrift_remove_next_hop(next_hop2_p)
            self.client.sai_thrift_remove_next_hop(next_hop2)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(next_hop1_p)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id5, ip_da5, dmac5)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_router_interface(rif_id6)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)


class scenario_13_sr_aps_group_test1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        ip_da2 = '5.5.5.2'
        ip_da3 = '5.5.5.3'
        ip_da4 = '5.5.5.4'
        ip_da5 = '5.5.5.5'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        dmac3 = '00:55:55:55:55:77'
        dmac4 = '00:55:55:55:55:88'
        dmac5 = '00:55:55:55:55:99'
        ip_addr1_subnet = '10.10.10.1'
        ip_addr2_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1_1 = 100
        label1_2 = 110
        label1_3 = 120
        label1_4 = 130
        label1_5 = 140
        label1_6 = 150
        label1_7 = 160
        label1_8 = 170
        label1_9 = 180
        label1_10 = 190
        label_list1 = [(label1_1<<12) | 32, (label1_2<<12) | 32, (label1_3<<12) | 32, (label1_4<<12) | 32, (label1_5<<12) | 32, (label1_6<<12) | 32,\
        (label1_7<<12) | 32, (label1_8<<12) | 32, (label1_9<<12) | 32, (label1_10<<12) | 32]

        label2_1 = 200
        label2_2 = 210
        label2_3 = 220
        label2_4 = 230
        label2_5 = 240
        label2_6 = 250
        label2_7 = 260
        label2_8 = 270
        label2_9 = 280
        label2_10 = 290
        label_list2 = [(label2_1<<12) | 32, (label2_2<<12) | 32, (label2_3<<12) | 32, (label2_4<<12) | 32, (label2_5<<12) | 32, (label2_6<<12) | 32,\
        (label2_7<<12) | 32, (label2_8<<12) | 32, (label2_9<<12) | 32, (label2_10<<12) | 32]

        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)


        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1_p = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        
        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        #pdb.set_trace()
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1_p, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
       
        
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group1)
       
        pkt_label1 = [{'label':label1_10,'tc':0,'ttl':32,'s':0}, {'label':label1_9,'tc':0,'ttl':32,'s':0} ,{'label':label1_8,'tc':0,'ttl':32,'s':0},\
        {'label':label1_7,'tc':0,'ttl':32,'s':0}, {'label':label1_6,'tc':0,'ttl':32,'s':0} ,{'label':label1_5,'tc':0,'ttl':32,'s':0}, {'label':label1_4,'tc':0,'ttl':32,'s':0},\
        {'label':label1_3,'tc':0,'ttl':32,'s':0} ,{'label':label1_2,'tc':0,'ttl':32,'s':0}, {'label':label1_1,'tc':0,'ttl':32,'s':1}]   
        pkt_label2 = [{'label':label2_10,'tc':0,'ttl':32,'s':0}, {'label':label2_9,'tc':0,'ttl':32,'s':0} ,{'label':label2_8,'tc':0,'ttl':32,'s':0},\
        {'label':label2_7,'tc':0,'ttl':32,'s':0}, {'label':label2_6,'tc':0,'ttl':32,'s':0} ,{'label':label2_5,'tc':0,'ttl':32,'s':0}, {'label':label2_4,'tc':0,'ttl':32,'s':0},\
        {'label':label2_3,'tc':0,'ttl':32,'s':0} ,{'label':label2_2,'tc':0,'ttl':32,'s':0}, {'label':label2_1,'tc':0,'ttl':32,'s':1}]


        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_dscp=16,
                               ip_id=105,
                               ip_ttl=64)
                               
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_dscp=16,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2_w = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= pkt_label1,
                                inner_frame = ip_only_pkt1) 
        pkt2_p = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= pkt_label2,
                                inner_frame = ip_only_pkt1) 

                                
        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2_w, [0])

            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2_p, [1])


            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=0)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2_w, [0])


        finally:
            sys_logging("======clean up======")
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group1)
            

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(next_hop1_p)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_14_sr_aps_group_test2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        ip_da2 = '5.5.5.2'
        ip_da3 = '5.5.5.3'
        ip_da4 = '5.5.5.4'
        ip_da5 = '5.5.5.5'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        dmac3 = '00:55:55:55:55:77'
        dmac4 = '00:55:55:55:55:88'
        dmac5 = '00:55:55:55:55:99'
        ip_addr1_subnet = '10.10.10.1'
        ip_addr2_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1_1 = 100
        label1_2 = 110
        label1_3 = 120
        label1_4 = 130
        label1_5 = 140
        label1_6 = 150
        label1_7 = 160
        label1_8 = 170
        label1_9 = 180
        label1_10 = 190
        label_list1 = [(label1_1<<12) | 32, (label1_2<<12) | 32]

        label2_1 = 200
        label2_2 = 210
        label2_3 = 220
        label2_4 = 230
        label2_5 = 240
        label2_6 = 250
        label2_7 = 260
        label2_8 = 270
        label2_9 = 280
        label2_10 = 290
        label_list2 = [(label1_2<<12) | 32, (label1_1<<12) | 32, (label2_2<<12) | 32, (label2_1<<12) | 32]

        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)


        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1_p = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        
        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        #pdb.set_trace()
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1_p, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
       
        
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group1)
       
        pkt_label1 = [{'label':label1_1,'tc':0,'ttl':32,'s':0}, {'label':label1_2,'tc':0,'ttl':32,'s':1}]   
        pkt_label2 = [ {'label':label2_1,'tc':0,'ttl':32,'s':0}, {'label':label2_2,'tc':0,'ttl':32,'s':0} ,{'label':label1_1,'tc':0,'ttl':32,'s':0}, {'label':label1_2,'tc':0,'ttl':32,'s':1}]


        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_dscp=16,
                               ip_id=105,
                               ip_ttl=64)
                               
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_dscp=16,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2_w = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= pkt_label1,
                                inner_frame = ip_only_pkt1) 
        pkt2_p = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= pkt_label2,
                                inner_frame = ip_only_pkt1) 

                                
        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2_w, [0])

            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2_p, [1])


            sys_logging("======set the lsp aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=0)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2_w, [0])


        finally:
            sys_logging("======clean up======")
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, nhop_group1)
            

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(next_hop1_p)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_15_mpls_sr_transmit_aps_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        ip_da2 = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        ip_addr1_subnet = '10.10.10.1'
        ip_addr2_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 100
        label2 = 200
        label3 = 300

        label2_1 = 210
        label2_2 = 220
        label_list1 = [(label2<<12) | 32, (label2_1<<12) | 32, (label2_2<<12) | 32]
        label_list2 = [(label2<<12) | 64]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da2, dmac2)
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id3, label_list2, outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_UNIFORM, outseg_type = SAI_OUTSEG_TYPE_SWAP)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id2, label_list1, outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_PIPE, outseg_exp_mode= SAI_OUTSEG_EXP_MODE_PIPE)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        #pdb.set_trace()
        nhop_gmember_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

       
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id4, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, nhop_group1, packet_action)
        

        mpls1 = [{'label':100,'tc':3,'ttl':60,'s':0}, {'label':200,'tc':0,'ttl':100,'s':0}, {'label':300,'tc':0,'ttl':100,'s':1}]  
        #mpls1 = [{'label':100,'tc':0,'ttl':64,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1)
                                
        mpls2 = [{'label':200,'tc':0,'ttl':59,'s':0}, {'label':300,'tc':0,'ttl':100,'s':1}]   
        mpls2_p = [{'label':220,'tc':0,'ttl':32,'s':0}, {'label':210,'tc':0,'ttl':32,'s':0}, {'label':200,'tc':0,'ttl':32,'s':0}, {'label':300,'tc':0,'ttl':100,'s':1}] 
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2) 
                                
        pkt2_p = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls2_p,
                                inner_frame = ip_only_pkt2)

        warmboot(self.client)
        try:

            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( pkt2, [3])

            
            sys_logging("======set the sr aps nexthop group1 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( pkt2_p, [2])
        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 

            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_p)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_w)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da2, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)



class scenario_16_vpls_2_level_aps_group_update_member_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        ip_da3 = '5.5.5.4'
        ip_da4 = '5.5.5.5'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        dmac3 = '00:55:55:55:55:77'
        dmac4 = '00:55:55:55:55:88'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label3 = 300
        label4 = 400
        label5 = 500
        label6 = 600

        label_list1 = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        label_list4 = [(label4<<12) | 32]
        label_list5 = [(label5<<12) | 32]
        label_list6 = [(label6<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a aps nexthop group======")
        nhop_group3 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember3_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group3, next_hop5, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember3_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group3, next_hop6, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group1, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group2, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, rif_id6, packet_action, frr_nhp_grp=nhop_group2, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True) 
        sai_thrift_create_inseg_entry(self.client, label5, pop_nums, None, rif_id5, packet_action, tunnel_id=tunnel_id1, frr_nhp_grp=nhop_group3, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_PRIMARY, frr_inactive_discard = True)  
        sai_thrift_create_inseg_entry(self.client, label6, pop_nums, None, rif_id5, packet_action, tunnel_id=tunnel_id1, frr_nhp_grp=nhop_group3, frr_cfg_role=SAI_INSEG_ENTRY_CONFIGURED_ROLE_STANDBY, frr_inactive_discard = True)

        bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        frr_bport = sai_thrift_create_bridge_frr_port(self.client, frr_nhp_grp_id=nhop_group3, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, frr_bport, mac_action, type=SAI_FDB_ENTRY_TYPE_DYNAMIC)

        pkt_label1 = {'label':label1,'tc':0,'ttl':32,'s':0}
        pkt_label2 = {'label':label2,'tc':0,'ttl':32,'s':0}
        pkt_label3 = {'label':label3,'tc':0,'ttl':32,'s':0}
        pkt_label4 = {'label':label4,'tc':0,'ttl':32,'s':0}
        pkt_label5 = {'label':label5,'tc':0,'ttl':32,'s':1}
        pkt_label6 = {'label':label6,'tc':0,'ttl':32,'s':1}
        mpls_label_stack_w1_w = [pkt_label1, pkt_label5]
        mpls_label_stack_p1_w = [pkt_label2, pkt_label5]
        mpls_label_stack_w2_p = [pkt_label3, pkt_label6]
        mpls_label_stack_p2_p = [pkt_label4, pkt_label6]
        
        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt2_w1_w = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w1_w,
                                inner_frame = mpls_inner_pkt)

        pkt2_p1_w = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p1_w,
                                inner_frame = mpls_inner_pkt)

        pkt2_w2_p = simple_mpls_packet(
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w2_p,
                                inner_frame = mpls_inner_pkt)

        pkt2_p2_p = simple_mpls_packet(
                                eth_dst=dmac4,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p2_p,
                                inner_frame = mpls_inner_pkt)


        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt3_w1_w = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w1_w,
                                inner_frame = mpls_inner_pkt1)

        pkt3_p1_w = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p1_w,
                                inner_frame = mpls_inner_pkt1)

        pkt3_w2_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w2_p,
                                inner_frame = mpls_inner_pkt1)

        pkt3_p2_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p2_p,
                                inner_frame = mpls_inner_pkt1)

                                
        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w1_w, [1])
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1_w)

            #ac to pw
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_p1_w, [2])
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3_w)
            
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w2_p, [3])


            sys_logging("======set the lsp aps nexthop group2 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group2, nhop_group_atr)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_p2_p, [4])

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2_p)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w2_p, [3])

            sys_logging("======set the lsp aps nexthop group2 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=0)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group2, nhop_group_atr)

            nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
            nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
            nhop_gmember3_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group3, next_hop5, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)

            #ac to pw
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w1_w, [1])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port1)
            self.client.sai_thrift_remove_bridge_port(frr_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            mpls4 = sai_thrift_inseg_entry_t(label4)
            mpls5 = sai_thrift_inseg_entry_t(label5) 
            mpls6 = sai_thrift_inseg_entry_t(label6)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_inseg_entry(mpls3) 
            self.client.sai_thrift_remove_inseg_entry(mpls4)
            self.client.sai_thrift_remove_inseg_entry(mpls5)  
            self.client.sai_thrift_remove_inseg_entry(mpls6) 

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group3)
            
            self.client.sai_thrift_remove_next_hop(next_hop5)
            self.client.sai_thrift_remove_next_hop(next_hop6)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop4)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_router_interface(rif_id6)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)



class scenario_18_vpls_2_level_aps_group_update_member_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        port7 = port_list[6]
        port8 = port_list[7]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        ip_da3 = '5.5.5.4'
        ip_da4 = '5.5.5.5'
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
        dmac3 = '00:55:55:55:55:77'
        dmac4 = '00:55:55:55:55:88'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label3 = 300
        label4 = 400
        label5 = 500
        label6 = 600
        label7 = 700
        label8 = 800
        label9 = 900
        label10 = 1000
        label11 = 1100

        label_list1 = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        label_list4 = [(label4<<12) | 32]
        label_list5 = [(label5<<12) | 32]
        label_list6 = [(label6<<12) | 32]
        label_list7 = [(label7<<12) | 32]
        label_list8 = [(label8<<12) | 32]
        label_list9 = [(label9<<12) | 32]
        label_list10 = [(label10<<12) | 32]
        label_list11 = [(label11<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)
        next_hop5 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list5)
        next_hop6 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list6)
        next_hop7 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list7)
        

        sys_logging("======create a aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a aps nexthop group======")
        nhop_group3 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember3_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group3, next_hop5, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember3_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group3, next_hop6, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop8 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list8, next_level_nhop_oid=nhop_group1)
        next_hop9 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list9, next_level_nhop_oid=nhop_group2)
        next_hop10 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list10, next_level_nhop_oid=nhop_group3)
        next_hop11 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list11, next_level_nhop_oid=next_hop7)

        sys_logging("======create a aps nexthop group======")
        nhop_group4 = sai_thrift_create_next_hop_protection_group(self.client)
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember4_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group4, next_hop8, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember4_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group4, next_hop9, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        frr_bport = sai_thrift_create_bridge_frr_port(self.client, frr_nhp_grp_id=nhop_group4, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, frr_bport, mac_action, type=SAI_FDB_ENTRY_TYPE_DYNAMIC)

        pkt_label1 = {'label':label1,'tc':0,'ttl':32,'s':0}
        pkt_label2 = {'label':label2,'tc':0,'ttl':32,'s':0}
        pkt_label3 = {'label':label3,'tc':0,'ttl':32,'s':0}
        pkt_label4 = {'label':label4,'tc':0,'ttl':32,'s':0}
        pkt_label5 = {'label':label5,'tc':0,'ttl':32,'s':0}
        pkt_label6 = {'label':label6,'tc':0,'ttl':32,'s':0}
        pkt_label7 = {'label':label7,'tc':0,'ttl':32,'s':0}
        pkt_label8 = {'label':label8,'tc':0,'ttl':32,'s':1}
        pkt_label9 = {'label':label9,'tc':0,'ttl':32,'s':1}
        pkt_label10 = {'label':label10,'tc':0,'ttl':32,'s':1}
        pkt_label11 = {'label':label11,'tc':0,'ttl':32,'s':1}
        mpls_label_stack_w1_w = [pkt_label1, pkt_label8]
        mpls_label_stack_p1_w = [pkt_label2, pkt_label8]
        mpls_label_stack_w3_w = [pkt_label5, pkt_label10]
        mpls_label_stack_p3_w = [pkt_label6, pkt_label10]
        mpls_label_stack_w2_p = [pkt_label3, pkt_label9]
        mpls_label_stack_p2_p = [pkt_label4, pkt_label9]
        mpls_label_stack_4_p = [pkt_label7, pkt_label11]
        
        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt2_w1_w = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w1_w,
                                inner_frame = mpls_inner_pkt)

        pkt2_p1_w = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p1_w,
                                inner_frame = mpls_inner_pkt)

        pkt2_w2_p = simple_mpls_packet(
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w2_p,
                                inner_frame = mpls_inner_pkt)

        pkt2_p2_p = simple_mpls_packet(
                                eth_dst=dmac4,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p2_p,
                                inner_frame = mpls_inner_pkt)
                                
        pkt2_w3_w = simple_mpls_packet(
                                eth_dst=dmac4,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w3_w,
                                inner_frame = mpls_inner_pkt)

        pkt2_p3_w = simple_mpls_packet(
                                eth_dst=dmac4,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p3_w,
                                inner_frame = mpls_inner_pkt)
                                
        pkt2_4_p = simple_mpls_packet(
                                eth_dst=dmac4,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_4_p,
                                inner_frame = mpls_inner_pkt)



        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt3_w1_w = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w1_w,
                                inner_frame = mpls_inner_pkt1)

        pkt3_p1_w = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p1_w,
                                inner_frame = mpls_inner_pkt1)

        pkt3_w2_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_w2_p,
                                inner_frame = mpls_inner_pkt1)

        pkt3_p2_p = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack_p2_p,
                                inner_frame = mpls_inner_pkt1)

                                
        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w1_w, [1])
            
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember4_w)
            
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w2_p, [3])

            nhop_gmember4_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group4, next_hop10, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w3_w, [4])

            sys_logging("======set the lsp aps nexthop group3 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group3, nhop_group_atr)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_p3_w, [4])


            sys_logging("======set the lsp aps nexthop group4 attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group4, nhop_group_atr)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_w2_p, [3])

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember4_p)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_p3_w, [4])
      
            nhop_gmember4_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group4, next_hop11, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2_4_p, [4])


            

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port1)
            self.client.sai_thrift_remove_bridge_port(frr_bport)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember4_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember4_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group4)
            self.client.sai_thrift_remove_next_hop(next_hop8)
            self.client.sai_thrift_remove_next_hop(next_hop9)
            self.client.sai_thrift_remove_next_hop(next_hop10)
            self.client.sai_thrift_remove_next_hop(next_hop11)


            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group3)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1_w)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1_p)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop4)
            self.client.sai_thrift_remove_next_hop(next_hop5)
            self.client.sai_thrift_remove_next_hop(next_hop6)
            self.client.sai_thrift_remove_next_hop(next_hop7)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_router_interface(rif_id6)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)




class scenario_17_create_l2_aps_nexthop_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        bport3 = sai_thrift_get_bridge_port_by_port(self.client, port3)
        bport4 = sai_thrift_get_bridge_port_by_port(self.client, port4)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)  
        self.client.sai_thrift_set_port_attribute(port4, attr) 

        nhop_group = sai_thrift_create_next_hop_group(self.client,type=SAI_NEXT_HOP_GROUP_TYPE_PROTECTION)
        
        nhop_gmember_1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group, bport3,cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember_2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group, bport4,cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        frr_bport_oid = sai_thrift_create_bridge_frr_port(self.client, frr_nhp_grp_id=nhop_group)
        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac2, frr_bport_oid, mac_action)
        

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

            
        warmboot(self.client)
        try:

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [2])

            sys_logging("======set the aps nexthop group attribute switchover======")
            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group, nhop_group_atr) 

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [3])
            
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, frr_bport_oid)
            self.client.sai_thrift_remove_bridge_port(frr_bport_oid)
        
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember_2)
            self.client.sai_thrift_remove_next_hop_group(nhop_group)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_set_port_attribute(port4, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid)



