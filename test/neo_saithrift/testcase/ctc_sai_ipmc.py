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
Thrift SAI Mcast tests
"""
import socket
import sys
import pdb
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask

def ip6_to_integer(ip6):
    ip6 = socket.inet_pton(socket.AF_INET6, ip6)
    a, b = unpack(">QQ", ip6)
    return (a << 64) | b

def integer_to_ip6(ip6int):
    a = (ip6int >> 64) & ((1 << 64) - 1)
    b = ip6int & ((1 << 64) - 1)
    return socket.inet_ntop(socket.AF_INET6, pack(">QQ", a, b))

def ip4_to_integer(ip4):
    ip4int = int(socket.inet_aton(ip4).encode('hex'), 16)
    return ip4int

def integer_to_ip4(ip4int):
    return socket.inet_ntoa(hex(ip4int)[2:].zfill(8).decode('hex'))

def sai_thrift_fill_l2mc_entry(addr_family, bv_id, dip_addr, sip_addr, type):
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=dip_addr)
        dipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
        addr = sai_thrift_ip_t(ip4=sip_addr)
        sipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=dip_addr)
        dipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
        addr = sai_thrift_ip_t(ip6=sip_addr)
        sipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
		
    l2mc_entry = sai_thrift_l2mc_entry_t(bv_id=bv_id, type=type, source=sipaddr, destination=dipaddr)
    return l2mc_entry

def sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr, sip_addr, type):
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=dip_addr)
        dipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
        addr = sai_thrift_ip_t(ip4=sip_addr)
        sipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=dip_addr)
        dipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
        addr = sai_thrift_ip_t(ip6=sip_addr)
        sipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
		
    ipmc_entry = sai_thrift_ipmc_entry_t(vr_id=vr_id, type=type, source=sipaddr, destination=dipaddr)
    return ipmc_entry

class fun_01_create_ipmc_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        sys_logging("======create 2 ipmc group======")
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        grp_id1 = self.client.sai_thrift_create_ipmc_group(grp_attr_list)

        warmboot(self.client)
        try:
            sys_logging("ipmc group oid = 0x%x" %grp_id)
            assert (grp_id%0x10000 == 0x33)
            sys_logging("ipmc group oid = 0x%x" %grp_id1)
            assert (grp_id1%0x10000 == 0x33)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            self.client.sai_thrift_remove_ipmc_group(grp_id1)

class fun_02_create_max_ipmc_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        grp_oid_list = []
        grp_num = 8191
        sys_logging("======create 8191 ipmc group======")
        for i in range(grp_num):
            grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
            grp_oid_list.append(grp_id)

        sys_logging("======create a new ipmc group======")
        grp_id1 = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        

        warmboot(self.client)
        try:
            
            sys_logging("ipmc group oid = 0x%x" %grp_id1)
            assert (grp_id1%0x10000 == 0x0)
        finally:
            sys_logging("======clean up======")
            for i in range(grp_num):
                self.client.sai_thrift_remove_ipmc_group(grp_oid_list[i])

class fun_03_remove_ipmc_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        sys_logging("======create 2 ipmc group======")
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        grp_id1 = self.client.sai_thrift_create_ipmc_group(grp_attr_list)

        warmboot(self.client)
        try:
            sys_logging("======remove 2 ipmc group======")
            status = self.client.sai_thrift_remove_ipmc_group(grp_id)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_ipmc_group(grp_id1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("======clean up======")

class fun_04_remove_no_exist_ipmc_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        grp_id1 = 0x10033

        warmboot(self.client)
        try:
            sys_logging("======remove no exist ipmc group======")
            status = self.client.sai_thrift_remove_ipmc_group(grp_id1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            sys_logging("======gey exist ipmc group attribute======")
            attrs = self.client.sai_thrift_get_ipmc_group_attribute(grp_id)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
class fun_05_get_ipmc_group_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)

        warmboot(self.client)
        try:
            sys_logging("======gey ipmc group attribute======")
            attrs = self.client.sai_thrift_get_ipmc_group_attribute(grp_id)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_GROUP_ATTR_IPMC_OUTPUT_COUNT:
                    sys_logging("output count = %d" %a.value.u16)
                    assert (a.value.u16 == 0)
                if a.id == SAI_IPMC_GROUP_ATTR_IPMC_MEMBER_LIST:
                    assert (a.value.objlist.object_id_list == [])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
class fun_06_get_ipmc_group_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 4 member======")
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id4)

        warmboot(self.client)
        try:
            sys_logging("======get ipmc group attribute======")
            attrs = self.client.sai_thrift_get_ipmc_group_attribute(grp_id)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_GROUP_ATTR_IPMC_OUTPUT_COUNT:
                    sys_logging("output count = %d" %a.value.u16)
                    assert (a.value.u16 == 4)
                if a.id == SAI_IPMC_GROUP_ATTR_IPMC_MEMBER_LIST:
                    assert (a.value.objlist.object_id_list != [])
                    n=1
                    for i in a.value.objlist.object_id_list:
                        sys_logging("get the %dth group member oid" %n)
                        sys_logging("the group member oid = 0x%x" %i)
                        n = n+1
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_ipmc_group_member(member_id4)
            self.client.sai_thrift_remove_ipmc_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class fun_07_create_ipmc_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 3 member======")
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)

        warmboot(self.client)
        try:    
            sys_logging("group member1 oid = 0x%x" %member_id1)
            assert (member_id1%0x100000000 == 0x2034)
            sys_logging("group member2 oid = 0x%x" %member_id2)
            assert (member_id2%0x100000000 == 0x8034)
            sys_logging("group member3 oid = 0x%x" %member_id3)
            assert (member_id3%0x100000000 == 0x0034)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


class fun_08_create_exist_ipmc_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 1 member======")
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        sys_logging("group member1 oid = 0x%x" %member_id1)
        sys_logging("======create exist ipmc group member======")
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)

        warmboot(self.client)
        try:    
        
            sys_logging("group member2 oid = 0x%x" %member_id2)
            assert (member_id2 == 0)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
 
            self.client.sai_thrift_remove_ipmc_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class fun_09_remove_ipmc_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 1 member======")
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)

        warmboot(self.client)
        try:  
            sys_logging("======remove ipmc group member======")
            status = self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class fun_10_remove_no_exist_ipmc_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 1 member======")
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        print member_id1
        member_id2 = 0x200000034
        warmboot(self.client)
        try: 
            sys_logging("======remove no exist ipmc group member======")
            status = self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            sys_logging("status = %d" %status)
            #sys_logging("======bug110027======")
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            #assert (status == SAI_STATUS_SUCCESS)
            sys_logging("======remove exist ipmc group member======")
            status = self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class fun_11_get_ipmc_group_member_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 3 group member======")
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)



        warmboot(self.client)
        try:   
            sys_logging("======get ipmc group member member_id1 attribute======")
            attrs = self.client.sai_thrift_get_ipmc_group_member_attribute(member_id1)
            print attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_GROUP_ID:
                    sys_logging("set group id: 0x%x, get group id: 0x%x" %(grp_id,a.value.oid))
                    if grp_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_OUTPUT_ID:
                    sys_logging("set interface id: 0x%x, get interface id: 0x%x" %(rif_id1,a.value.oid))
                    if rif_id1 != a.value.oid:
                        raise NotImplementedError()

            sys_logging("======get ipmc group member member_id2 attribute======")
            attrs = self.client.sai_thrift_get_ipmc_group_member_attribute(member_id2)
            print attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_GROUP_ID:
                    sys_logging("set group id: 0x%x, get group id: 0x%x" %(grp_id,a.value.oid))
                    if grp_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_OUTPUT_ID:
                    sys_logging("set interface id: 0x%x, get interface id: 0x%x" %(rif_id2,a.value.oid))
                    if rif_id2 != a.value.oid:
                        raise NotImplementedError()

            sys_logging("======get ipmc group member member_id3 attribute======")
            attrs = self.client.sai_thrift_get_ipmc_group_member_attribute(member_id3)
            print attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_GROUP_ID:
                    sys_logging("set group id: 0x%x, get group id: 0x%x" %(grp_id,a.value.oid))
                    if grp_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_IPMC_GROUP_MEMBER_ATTR_IPMC_OUTPUT_ID:
                    sys_logging("set interface id: 0x%x, get interface id: 0x%x" %(rif_id3,a.value.oid))
                    if rif_id3 != a.value.oid:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_ipmc_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
           

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class fun_12_create_rpf_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        sys_logging("======create 2 rpf group======")
        grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        grp_id1 = self.client.sai_thrift_create_rpf_group(grp_attr_list)

        warmboot(self.client)
        try:
            sys_logging("rpf group oid = 0x%x" %grp_id)
            assert (grp_id%0x10000 == 0x2f)
            sys_logging("rpf group oid = 0x%x" %grp_id1)
            assert (grp_id1%0x10000 == 0x2f)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_rpf_group(grp_id)
            self.client.sai_thrift_remove_rpf_group(grp_id1)

class fun_13_create_max_rpf_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        grp_oid_list = []
        grp_num = 8191
        sys_logging("======create 8191 rpf group======")
        for i in range(grp_num):
            grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
            grp_oid_list.append(grp_id)
        grp_id1 = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        

        warmboot(self.client)
        try:
            
            sys_logging("rpf group oid = 0x%x" %grp_id1)
            assert (grp_id1%0x10000 == 0x0)
        finally:
            sys_logging("======clean up======")
            for i in range(grp_num):
                self.client.sai_thrift_remove_rpf_group(grp_oid_list[i])

class fun_14_remove_rpf_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        sys_logging("======create 2 rpf group======")
        grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        grp_id1 = self.client.sai_thrift_create_rpf_group(grp_attr_list)

        warmboot(self.client)
        try:
            sys_logging("======remove rpf group======")
            status = self.client.sai_thrift_remove_rpf_group(grp_id)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_rpf_group(grp_id1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("======clean up======")

class fun_15_remove_no_exist_rpf_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        grp_id1 = 0x1002f

        warmboot(self.client)
        try:
            sys_logging("======remove no exist rpf group======")
            status = self.client.sai_thrift_remove_rpf_group(grp_id1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            sys_logging("======gey exist rpf group attribute======")
            attrs = self.client.sai_thrift_get_rpf_group_attribute(grp_id)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_rpf_group(grp_id)

class fun_16_get_rpf_group_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)

        warmboot(self.client)
        try:
            sys_logging("======gey rpf group attribute======")
            attrs = self.client.sai_thrift_get_rpf_group_attribute(grp_id)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_GROUP_ATTR_IPMC_OUTPUT_COUNT:
                    sys_logging("output count = %d" %a.value.u16)
                    assert (a.value.u16 == 0)
                if a.id == SAI_IPMC_GROUP_ATTR_IPMC_MEMBER_LIST:
                    assert (a.value.objlist.object_id_list == [])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_rpf_group(grp_id)

class fun_17_get_rpf_group_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 4 rpf group member======")
        grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        member_id1 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id1)
        member_id2 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id2)
        member_id3 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id3)
        member_id4 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id4)

        warmboot(self.client)
        try:
            sys_logging("======gey rpf group attribute======")
            attrs = self.client.sai_thrift_get_rpf_group_attribute(grp_id)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_GROUP_ATTR_IPMC_OUTPUT_COUNT:
                    sys_logging("output count = %d" %a.value.u16)
                    assert (a.value.u16 == 4)
                if a.id == SAI_IPMC_GROUP_ATTR_IPMC_MEMBER_LIST:
                    assert (a.value.objlist.object_id_list != [])
                    n=1
                    for i in a.value.objlist.object_id_list:
                        sys_logging("get the %dth group member oid" %n)
                        sys_logging("the group member oid = 0x%x" %i)
                        n = n+1
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_rpf_group_member(member_id1)
            self.client.sai_thrift_remove_rpf_group_member(member_id2)
            self.client.sai_thrift_remove_rpf_group_member(member_id3)
            self.client.sai_thrift_remove_rpf_group_member(member_id4)
            self.client.sai_thrift_remove_rpf_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class fun_18_create_rpf_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 3 rpf group member======")
        grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        member_id1 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id1)
        member_id2 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id2)
        member_id3 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id3)
       
        warmboot(self.client)
        try:
            sys_logging("group member1 oid = 0x%x" %member_id1)
            assert (member_id1%0x100000000 == 0x30)
            sys_logging("group member2 oid = 0x%x" %member_id2)
            assert (member_id2%0x100000000 == 0x30)
            sys_logging("group member3 oid = 0x%x" %member_id3)
            assert (member_id3%0x100000000 == 0x30)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_rpf_group_member(member_id1)
            self.client.sai_thrift_remove_rpf_group_member(member_id2)
            self.client.sai_thrift_remove_rpf_group_member(member_id3)
            
            self.client.sai_thrift_remove_rpf_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class fun_19_create_exist_rpf_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 1 rpf group member======")
        grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        member_id1 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id1)
        sys_logging("group member1 oid = 0x%x" %member_id1)
        sys_logging("======create exist rpf group member======")
        member_id2 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id1)
       
        warmboot(self.client)
        try:
            

            sys_logging("group member2 oid = 0x%x" %member_id2)
            assert (member_id2 == 0)
           
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_rpf_group_member(member_id1)
            self.client.sai_thrift_remove_rpf_group_member(member_id2)

            self.client.sai_thrift_remove_rpf_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class fun_20_remove_rpf_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 1 rpf group member======")
        grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        member_id1 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id1)
        sys_logging("======remove ipmc group member======")
        status = self.client.sai_thrift_remove_rpf_group_member(member_id1)
        warmboot(self.client)
        try:
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
           
        finally:
            
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_rpf_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            
class fun_21_remove_no_exist_rpf_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 1 rpf group member======")
        grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        member_id1 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id1)

        member_id2 = 0x300000030
        warmboot(self.client)
        try:
            sys_logging("======remove no exist rpf group member======")
            status = self.client.sai_thrift_remove_rpf_group_member(member_id2)
            sys_logging("status = %d" %status)
            #sys_logging("======bug110027======")
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            #assert (status == SAI_STATUS_SUCCESS)
            sys_logging("======remove exist rpf group member======")
            status = self.client.sai_thrift_remove_rpf_group_member(member_id1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
           
        finally:
            sys_logging("======clean up======")
            

            self.client.sai_thrift_remove_rpf_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class fun_22_get_rpf_group_member_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        vlan_id1 = 10
        vlan_id2 = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======create a ipmc group and add 3 rpf group member======")
        grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        member_id1 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id1)
        member_id2 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id2)
        member_id3 = sai_thrift_create_rpf_group_member(self.client, grp_id, rif_id3)
        warmboot(self.client)
        try:
            sys_logging("======get rpf group member member_id1 attribute======")
            attrs = self.client.sai_thrift_get_rpf_group_member_attribute(member_id1)
            print attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID:
                    sys_logging("set group id: 0x%x, get group id: 0x%x" %(grp_id,a.value.oid))
                    if grp_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID:
                    sys_logging("set interface id: 0x%x, get interface id: 0x%x" %(rif_id1,a.value.oid))
                    if rif_id1 != a.value.oid:
                        raise NotImplementedError()

            sys_logging("======get rpf group member member_id2 attribute======")
            attrs = self.client.sai_thrift_get_rpf_group_member_attribute(member_id2)
            print attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID:
                    sys_logging("set group id: 0x%x, get group id: 0x%x" %(grp_id,a.value.oid))
                    if grp_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID:
                    sys_logging("set interface id: 0x%x, get interface id: 0x%x" %(rif_id2,a.value.oid))
                    if rif_id2 != a.value.oid:
                        raise NotImplementedError()

            sys_logging("======get rpf group member member_id3 attribute======")            
            attrs = self.client.sai_thrift_get_rpf_group_member_attribute(member_id3)
            print attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_RPF_GROUP_MEMBER_ATTR_RPF_GROUP_ID:
                    sys_logging("set group id: 0x%x, get group id: 0x%x" %(grp_id,a.value.oid))
                    if grp_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_RPF_GROUP_MEMBER_ATTR_RPF_INTERFACE_ID:
                    sys_logging("set interface id: 0x%x, get interface id: 0x%x" %(rif_id3,a.value.oid))
                    if rif_id3 != a.value.oid:
                        raise NotImplementedError()
        finally:
            
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_rpf_group(grp_id)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class fun_23_create_v4_ipmc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        

        warmboot(self.client)
        try:
            sys_logging("======create a v4 ipmc entry======")
            status = sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_24_create_v6_ipmc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        

        warmboot(self.client)
        try:
            sys_logging("======create a v6 ipmc entry======")
            status = sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
        finally:    
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)


class fun_25_create_exist_v4_ipmc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sys_logging("======create a v4 ipmc entry======")
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        warmboot(self.client)
        try:
            sys_logging("======create exist v4 ipmc entry======")
            status = sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
           
class fun_26_create_exist_v6_ipmc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sys_logging("======create a v6 ipmc entry======")
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        warmboot(self.client)
        try:
            sys_logging("======create exist v6 ipmc entry======")
            status = sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)


class fun_27_create_max_v4_ipmc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        dip_addr2 = '230.255.1.2'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG
        num = 0
        grp_id_list = []
        ipmc_entry_list = []
        chipname = testutils.test_params_get()['chipname']
        sys_logging("chipname = %s" %chipname)

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        if chipname == "tsingma":
            num = 1024
            sys_logging("======create 1024 XG v4 ipmc entry======")
        elif chipname == "tsingma_mx":
            num = 2048
            sys_logging("======create 2048 XG v4 ipmc entry======")
        else:
            num = 0
            sys_logging("======chipname is error======")
        for i in range(num):
            
            temp = ip4_to_integer(dip_addr2)
            dip_addr = integer_to_ip4(temp+i)
            ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr, default_addr, type)
            ipmc_entry_list.append(ipmc_entry)
            
            sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        warmboot(self.client)
        try:
            sys_logging("======create a new XG v4 ipmc entry======")
            ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
            status = sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_INSUFFICIENT_RESOURCES)
        finally:
            sys_logging("======clean up======")
            for i in range(num):
                self.client.sai_thrift_remove_ipmc_entry(ipmc_entry_list[i])
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)

            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
class fun_28_create_max_v6_ipmc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        dip_addr2 = 'ff06::1:2'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG
        chipname = testutils.test_params_get()['chipname']
        sys_logging("chipname = %s" %chipname)
        if chipname == "tsingma":
            num = 512
            sys_logging("======create 512 XG v6 ipmc entry======")
        elif chipname == "tsingma_mx":
            num = 1024
            sys_logging("======create 1024 XG v6 ipmc entry======")
        else:
            num = 0
            sys_logging("======chipname is error======")
        grp_id_list = []
        ipmc_entry_list = []

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        for i in range(num):
            
            temp = ip6_to_integer(dip_addr2)
            dip_addr = integer_to_ip6(temp+i)
            ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr, default_addr, type)
            ipmc_entry_list.append(ipmc_entry)
            
            sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        warmboot(self.client)
        try:
            sys_logging("======create a new XG v6 ipmc entry======")
            ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
            status = sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_INSUFFICIENT_RESOURCES)
        finally:
            sys_logging("======clean up======")
            for i in range(num):
                self.client.sai_thrift_remove_ipmc_entry(ipmc_entry_list[i])
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)

            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            #pdb.set_trace()

class fun_29_remove_v4_ipmc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sys_logging("======create a v4 ipmc entry======")
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            sys_logging("======remove the v4 ipmc entry======")
            status = self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_30_remove_v6_ipmc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sys_logging("======create a v6 ipmc entry======")
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            sys_logging("======remove the v6 ipmc entry======")
            status = self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_31_remove_no_exist_v4_ipmc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        vr_id1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        dip_addr2 = '230.255.1.2'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sys_logging("======create a v4 ipmc entry======")
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            sys_logging("======remove no exist v4 ipmc entry======")
            ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id1, dip_addr1, default_addr, type)
            status = self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            sys_logging("======remove no exist v4 ipmc entry======")
            ipmc_entry2 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr2, default_addr, type)
            status = self.client.sai_thrift_remove_ipmc_entry(ipmc_entry2)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_virtual_router(vr_id1)

class fun_32_remove_no_exist_v6_ipmc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        vr_id1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        dip_addr2 = 'ff06::1:2'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sys_logging("======create a v6 ipmc entry======")
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            sys_logging("======remove no exist v6 ipmc entry======")
            ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id1, dip_addr1, default_addr, type)
            status = self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            sys_logging("======remove no exist v6 ipmc entry======")
            ipmc_entry2 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr2, default_addr, type)
            status = self.client.sai_thrift_remove_ipmc_entry(ipmc_entry2)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_virtual_router(vr_id1)

class fun_33_set_ipmc_entry_attribute_action_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        sys_logging("======create a v4 ipmc entry======")
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        warmboot(self.client)
        try:
            sys_logging("======get the v4 ipmc entry attribute action======")
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("get packet action = %d" %a.value.s32)
                    if SAI_PACKET_ACTION_TRANSIT != a.value.s32:
                        raise NotImplementedError()
            sys_logging("======set the v4 ipmc entry attribute action======") 
            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_COPY)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)
            sys_logging("======get the v4 ipmc entry attribute action again======")
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("get packet action = %d" %a.value.s32)
                    if SAI_PACKET_ACTION_LOG != a.value.s32:
                        raise NotImplementedError()
            #pdb.set_trace()
            sys_logging("======set the v4 ipmc entry attribute action again======") 
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            sys_logging("======get the v4 ipmc entry attribute action again======")
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("get packet action = %d" %a.value.s32)
                    if SAI_PACKET_ACTION_LOG != a.value.s32:
                        raise NotImplementedError()

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_34_set_ipmc_entry_attribute_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        grp_id1 = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id3)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        warmboot(self.client)
        try:
            sys_logging("======get the v4 ipmc entry attribute output group id======")
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID:
                    sys_logging("get ipmc group id = 0x%x" %a.value.oid)
                    if grp_id != a.value.oid:
                        raise NotImplementedError()

            sys_logging("======set the v4 ipmc entry attribute output group id======")            
            attr_value = sai_thrift_attribute_value_t(oid=grp_id1)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            sys_logging("======get the v4 ipmc entry attribute output group id again======")
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID:
                    sys_logging("get ipmc group id = 0x%x" %a.value.oid)
                    if grp_id1 != a.value.oid:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            self.client.sai_thrift_remove_ipmc_group(grp_id1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_35_set_ipmc_entry_attribute_rpf_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_SG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        rpf_grp_id1 = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id1, rif_id2)
        rpf_grp_id2 = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id2 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id2, rif_id3)
        
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id = grp_id, rpf_grp_id = rpf_grp_id1)

        warmboot(self.client)
        try:
            sys_logging("======get the v4 ipmc entry attribute rpf group id======")
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID:
                    sys_logging("get rpf group id = 0x%x" %a.value.oid)
                    if rpf_grp_id1 != a.value.oid:
                        raise NotImplementedError()
            sys_logging("======set the v4 ipmc entry attribute output group id======")             
            attr_value = sai_thrift_attribute_value_t(oid=rpf_grp_id2)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            sys_logging("======get the v4 ipmc entry attribute rpf group id again======")
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID:
                    sys_logging("get ipmc group id = 0x%x" %a.value.oid)
                    if rpf_grp_id2 != a.value.oid:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id2)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_36_get_ipmc_entry_default_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry)

        warmboot(self.client)
        try:
            sys_logging("======get the v4 ipmc entry attribute(default)======")
            attrs = self.client.sai_thrift_get_ipmc_entry_attribute(ipmc_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_IPMC_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("get packet action = %d" %a.value.s32)
                    if SAI_PACKET_ACTION_TRANSIT != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID:
                    sys_logging("get ipmc group id = 0x%x" %a.value.oid)
                    if 0 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID:
                    sys_logging("get rpf group id = 0x%x" %a.value.oid)
                    if 0 != a.value.oid:
                        raise NotImplementedError()
                        
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_01_v4_XG_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        v4_mcast_enable = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)

        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id4)
        member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)
        #pdb.set_trace()
 


        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_ipmc_group_member(member_id4)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_02_v4_SG_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_SG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id4)
        member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)
 


        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_ipmc_group_member(member_id4)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_03_v4_SG_update_rpf_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_SG
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id2)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)


        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])

            sys_logging("======update rpf group and send packet again======")
            rpf_member_id2 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id3)
            
            attr_value = sai_thrift_attribute_value_t(oid=rpf_grp_id)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])
            sys_logging("======update rpf group and send packet again======")
            rpf_member_id3 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)
            
            attr_value = sai_thrift_attribute_value_t(oid=rpf_grp_id)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id2)
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id3)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_04_v4_XG_update_action_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)


        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            sys_logging("======update action and send packet again======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])

            sys_logging("======update action and send packet again======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_05_v4_SG_update_action_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_SG
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)


        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])

            sys_logging("======update action and send packet again======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])

            sys_logging("======update action and send packet again======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DENY)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])

            sys_logging("======update action and send packet again======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_06_v4_XG_update_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id6 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)

        grp_id1 = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id3)
        member_id5 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id4)
        member_id7 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id1)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src='1.1.1.1',
                                ip_id=106,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src='1.1.1.1',
                                ip_id=106,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])

            sys_logging("======update ipmc group and send packet again======")
            attr_value = sai_thrift_attribute_value_t(oid=grp_id)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])

            sys_logging("======add ipmc group member and send packet again======")
            member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id4)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            sys_logging("======remove ipmc group member and send packet again======")
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,3])
 
            sys_logging("======update ipmc group and send packet again======")
            attr_value = sai_thrift_attribute_value_t(oid=grp_id1)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [2,3])
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)

            self.client.sai_thrift_remove_ipmc_group(grp_id)
            self.client.sai_thrift_remove_ipmc_group(grp_id1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_07_v4_SG_update_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_SG
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id6 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)

        grp_id1 = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id3)
        member_id5 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id4)
        member_id7 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=106,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=106,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])

            sys_logging("======add ipmc group member and send packet again======")
            attr_value = sai_thrift_attribute_value_t(oid=grp_id)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])

            sys_logging("======add ipmc group member and send packet again======")
            member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id4)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            sys_logging("======remove ipmc group member and send packet again======")
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,3])

            sys_logging("======update ipmc group and send packet again======")
            attr_value = sai_thrift_attribute_value_t(oid=grp_id1)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

 
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [2,3])
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)

            self.client.sai_thrift_remove_ipmc_group(grp_id)
            self.client.sai_thrift_remove_ipmc_group(grp_id1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_08_v6_XG_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id4)
        member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src='2001::1',
                                ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src='2001::1',
                                ipv6_hlim=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_ipmc_group_member(member_id4)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_09_v6_SG_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_SG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id4)
        member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)
 


        pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_ipmc_group_member(member_id4)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_10_v6_SG_update_rpf_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_SG
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id2)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)


        pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])

            sys_logging("======update rpf group and send packet again======")
            rpf_member_id2 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id3)
            
            attr_value = sai_thrift_attribute_value_t(oid=rpf_grp_id)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])
            sys_logging("======update rpf group and send packet again======")
            rpf_member_id3 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)
            
            attr_value = sai_thrift_attribute_value_t(oid=rpf_grp_id)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_RPF_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id2)
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id3)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_11_v6_XG_update_action_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)

        pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src='2001::1',
                                ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src='2001::1',
                                ipv6_hlim=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])

            sys_logging("======update action and send packet again======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])

            sys_logging("======update action and send packet again======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_12_v6_SG_update_action_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_SG
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)


        pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])

            sys_logging("======update action and send packet again======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])

            sys_logging("======update action and send packet again======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_13_v6_XG_update_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id6 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)

        grp_id1 = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id3)
        member_id5 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id4)
        member_id7 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id1)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry)

        pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src='2001::1',
                                ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src='2001::1',
                                ipv6_hlim=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])

            sys_logging("======add ipmc group member and send packet again======")
            attr_value = sai_thrift_attribute_value_t(oid=grp_id)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])

            sys_logging("======add ipmc group member and send packet again======")
            member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id4)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            sys_logging("======remove ipmc group member and send packet again======")
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,3])

            sys_logging("======update ipmc group and send packet again======")
            attr_value = sai_thrift_attribute_value_t(oid=grp_id1)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

 
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [2,3])
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)

            self.client.sai_thrift_remove_ipmc_group(grp_id)
            self.client.sai_thrift_remove_ipmc_group(grp_id1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            
            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_14_v6_SG_update_group_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_SG
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        member_id6 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)

        grp_id1 = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id3)
        member_id5 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id4)
        member_id7 = sai_thrift_create_ipmc_group_member(self.client, grp_id1, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry)

        pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any( exp_pkt, [1,2])

            sys_logging("======add ipmc group member and send packet again======")
            attr_value = sai_thrift_attribute_value_t(oid=grp_id)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])

            sys_logging("======add ipmc group member and send packet again======")
            member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id4)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            sys_logging("======remove ipmc group member and send packet again======")
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,3])

            sys_logging("======update ipmc group and send packet again======")
            attr_value = sai_thrift_attribute_value_t(oid=grp_id1)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

 
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [2,3])
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)

            self.client.sai_thrift_remove_ipmc_group(grp_id)
            self.client.sai_thrift_remove_ipmc_group(grp_id1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            
            self.client.sai_thrift_remove_virtual_router(vr_id) 

class scenario_15_fdb_to_l2mc_update_ipmc_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        vlan_id1 = 20
        vlan_id2 = 30
        grp_attr_list = []
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port5, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port5, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id5, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_SG
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)

        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
        sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)

        
        type = SAI_IPMC_ENTRY_TYPE_SG
        grp_id2 = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id2, rif_id2)
        member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id2, rif_id3)
        member_id5 = sai_thrift_create_ipmc_group_member(self.client, grp_id2, rif_id4)
        member_id6 = sai_thrift_create_ipmc_group_member(self.client, grp_id2, rif_id5)
        member_id7 = sai_thrift_create_ipmc_group_member(self.client, grp_id2, rif_id1)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id2)

        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, sip_addr1, type)
        sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id1)
        
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port4)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt2 = simple_tcp_packet(pktlen=104,
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt3 = simple_tcp_packet(pktlen=104,
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt4 = simple_tcp_packet(pktlen=104,
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1,exp_pkt1,exp_pkt2,exp_pkt3,exp_pkt2], [1,2,3,4,4])
           
        finally:
            self.client.sai_thrift_remove_ipmc_group_member(member_id3)
            self.client.sai_thrift_remove_ipmc_group_member(member_id4)
            self.client.sai_thrift_remove_ipmc_group_member(member_id5)
            self.client.sai_thrift_remove_ipmc_group_member(member_id6)
            self.client.sai_thrift_remove_ipmc_group_member(member_id7)
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group(grp_id2)

            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

class scenario_16_v4_SG_test_multi(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
 
        v4_enabled = 1
        v6_enabled = 1
        vlan_id1 = 10
        vlan_id2 = 20
        mac = ''
        grp_attr_list = []

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port4, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port5, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id5, attr)        

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        dip_addr2 = '230.255.2.1'
        dip_addr3 = '230.255.10.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        dmac2 = '01:00:5E:7F:02:01'
        dmac3 = '01:00:5E:7F:0a:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_SG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
   
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id4)
        member_id5 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, grp_id)

        ipmc_entry2 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr2, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry2, grp_id)

        ipmc_entry3 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr3, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry3, grp_id)

        #pdb.set_trace() 


        pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1_1 = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt1_2 = simple_tcp_packet(pktlen=104,
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1_3 = simple_tcp_packet(pktlen=104,
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        pkt2 = simple_tcp_packet(eth_dst=dmac2,
                                eth_src=smac1,
                                ip_dst=dip_addr2,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt2_1 = simple_tcp_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                ip_dst=dip_addr2,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt2_2 = simple_tcp_packet(pktlen=104,
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                ip_dst=dip_addr2,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt2_3 = simple_tcp_packet(pktlen=104,
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                ip_dst=dip_addr2,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)                        
        pkt3 = simple_tcp_packet(eth_dst=dmac3,
                                eth_src=smac1,
                                ip_dst=dip_addr3,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt3_1 = simple_tcp_packet(
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                ip_dst=dip_addr3,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt3_2 = simple_tcp_packet(pktlen=104,
                               eth_dst=dmac3,
                                eth_src=router_mac,
                                ip_dst=dip_addr3,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt3_3 = simple_tcp_packet(pktlen=104,
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                ip_dst=dip_addr3,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1_1,exp_pkt1_2], [1,3])

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2_1,exp_pkt2_2], [1,3])

            self.ctc_send_packet( 0, str(pkt3))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt3_1,exp_pkt3_2], [1,3])
            member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
            member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id5)
            
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1_1,exp_pkt1_1,exp_pkt1_2,exp_pkt1_3], [1,2,3,4])

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2_1,exp_pkt2_1,exp_pkt2_2,exp_pkt2_3], [1,2,3,4])

            self.ctc_send_packet( 0, str(pkt3))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt3_1,exp_pkt3_1,exp_pkt3_2,exp_pkt3_3], [1,2,3,4])
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry2)
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry3)
            
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class scenario_17_v6_SG_test_multi(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
 
        v4_enabled = 1
        v6_enabled = 1
        vlan_id1 = 10
        vlan_id2 = 20
        mac = ''
        grp_attr_list = []

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port4, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port5, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id5, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        dip_addr2 = 'ff06::1:101'
        dip_addr3 = 'ff06::101:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        dmac2 = '33:33:00:01:01:01'
        dmac3 = '33:33:01:01:00:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_SG

        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
   
        member_id3 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id4)
        member_id5 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id1)
        
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, grp_id)

        ipmc_entry2 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr2, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry2, grp_id)

        ipmc_entry3 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr3, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry3, grp_id)

        #pdb.set_trace() 


        pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64)
        exp_pkt1_1 = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63)
        exp_pkt1_2 = simple_tcpv6_packet(pktlen=104,
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1_3 = simple_tcpv6_packet(pktlen=104,
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        pkt2 = simple_tcpv6_packet(eth_dst=dmac2,
                                eth_src=smac1,
                                ipv6_dst=dip_addr2,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64)
        exp_pkt2_1 = simple_tcpv6_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr2,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63)
        exp_pkt2_2 = simple_tcpv6_packet(pktlen=104,
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr2,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt2_3 = simple_tcpv6_packet(pktlen=104,
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr2,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)                       
        pkt3 = simple_tcpv6_packet(eth_dst=dmac3,
                                eth_src=smac1,
                                ipv6_dst=dip_addr3,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64)
        exp_pkt3_1 = simple_tcpv6_packet(
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr3,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63)
        exp_pkt3_2 = simple_tcpv6_packet(pktlen=104,
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr3,
                               ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt3_3 = simple_tcpv6_packet(pktlen=104,
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr3,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1_1,exp_pkt1_2], [1,3])

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2_1,exp_pkt2_2], [1,3])

            self.ctc_send_packet( 0, str(pkt3))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt3_1,exp_pkt3_2], [1,3])
            member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
            member_id4 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id5)
            
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1_1,exp_pkt1_1,exp_pkt1_2,exp_pkt1_3], [1,2,3,4])

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2_1,exp_pkt2_1,exp_pkt2_2,exp_pkt2_3], [1,2,3,4])

            self.ctc_send_packet( 0, str(pkt3))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt3_1,exp_pkt3_1,exp_pkt3_2,exp_pkt3_3], [1,2,3,4])
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry2)
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry3)
            
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

