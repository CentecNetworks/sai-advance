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
from struct import pack, unpack

from switch import *

import sai_base_test
import ctc_sai_qos_map
from ptf.mask import Mask
'''
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
'''

class fun_01_create_rif_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        port1 = port_list[0]
        port2 = port_list[1]
        vlan_id1 = 10
        vlan_id2 = 20
        mac = ''
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        sys_logging("======create 6 type router interface======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, '')
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, 0, 0, v4_enabled, v6_enabled, '')
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, '')
        
        sys_logging("rif_id1 = 0x%x" %rif_id1)
        sys_logging("rif_id2 = 0x%x" %rif_id2)
        sys_logging("rif_id3 = 0x%x" %rif_id3)
        sys_logging("rif_id4 = 0x%x" %rif_id4)
        sys_logging("rif_id5 = 0x%x" %rif_id5)
        sys_logging("rif_id6 = 0x%x" %rif_id6)

        
       
        warmboot(self.client)
        try:
            assert (rif_id1%0x100000000 == 0x8006)
            assert (rif_id2%0x100000000 == 0x2006)
            assert (rif_id3%0x100000000 == 0x0006)
            assert (rif_id4%0x100000000 == 0xa006)
            assert (rif_id5%0x100000000 == 0x4006)
            assert (rif_id6%0x100000000 == 0x6006)
            
            sys_logging("======get sub type router interface attribute======")
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id1)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID:
                    if vr_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_TYPE:
                    if SAI_ROUTER_INTERFACE_TYPE_SUB_PORT != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_PORT_ID:
                    if port1 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_OUTER_VLAN_ID:
                    sys_logging("get vlan_id = 0x%x" %a.value.u16)
                    if vlan_id1 != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE:
                    if v4_enabled != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE:
                    if v6_enabled != a.value.booldata:
                        raise NotImplementedError()

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_router_interface(rif_id6)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

class fun_02_create_exist_rif_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        port1 = port_list[0]
        port2 = port_list[1]
        vlan_id1 = 10
        vlan_id2 = 20
        mac = ''

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        sys_logging("======create 3 types router interface======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("rif_id1 = 0x%x" %rif_id1)
        sys_logging("rif_id2 = 0x%x" %rif_id2)
        sys_logging("rif_id3 = 0x%x" %rif_id3)

        sys_logging("======create 3 same atribute router interface======")
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("rif_id4 = 0x%x" %rif_id4)
        sys_logging("rif_id5 = 0x%x" %rif_id5)
        sys_logging("rif_id6 = 0x%x" %rif_id6)

        
       
        warmboot(self.client)
        try:
            assert (rif_id1%0x100000000 == 0x8006)
            assert (rif_id2%0x100000000 == 0x2006)
            assert (rif_id3%0x100000000 == 0x0006)
            assert (rif_id4%0x100000000 == 0x0)
            assert (rif_id5%0x100000000 == 0x0)
            assert (rif_id6%0x100000000 == 0x0)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


class fun_03_create_same_attr_rif_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1

        mac = ''
        

        sys_logging("======create 3 type router interface======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, '')
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, 0, 0, v4_enabled, v6_enabled, '')
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, '')
        sys_logging("rif_id1 = 0x%x" %rif_id1)
        sys_logging("rif_id2 = 0x%x" %rif_id2)
        sys_logging("rif_id3 = 0x%x" %rif_id3)

        sys_logging("======create 3 same attribute router interface======")
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, '')
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, 0, 0, v4_enabled, v6_enabled, '')
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, '')
        sys_logging("rif_id4 = 0x%x" %rif_id4)
        sys_logging("rif_id5 = 0x%x" %rif_id5)
        sys_logging("rif_id6 = 0x%x" %rif_id6)
    
        warmboot(self.client)
        try:
            assert (rif_id1%0x100000000 == 0xa006)
            assert (rif_id2%0x100000000 == 0x4006)
            assert (rif_id3%0x100000000 == 0x6006)
            assert (rif_id4%0x100000000 == 0xa006)
            assert (rif_id5%0x100000000 == 0x4006)
            assert (rif_id6%0x100000000 == 0x6006)


        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_router_interface(rif_id6)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_04_max_rif_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        rif_id_list = []
        vlan_oid_list = []
        vr_id1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        port1 = port_list[0]
        chipname = testutils.test_params_get()['chipname']
        sys_logging("chipname = %s" %chipname)

        if chipname == "tsingma_mx":
            sys_logging("======create 8187 router interface======")
            for i in range(10,275):
                vlan_id = i
                vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
                vlan_oid_list.append(vlan_oid)
                for j in range(31):
                    if (i == 274)&(j > 2):
                        continue
                    rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port_list[j], 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id, stats_state = False)
                    rif_id_list.append(rif_id1)
        elif chipname == "tsingma":
            sys_logging("======create 4091 router interface======")
            for i in range(10,142):
                vlan_id = i
                vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
                vlan_oid_list.append(vlan_oid)
                for j in range(31):
                    if (i == 141)&(j == 30):
                        continue
                    rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port_list[j], 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id, stats_state = False)
                    rif_id_list.append(rif_id1)
        else:
            sys_logging("======chipname is error======")

        vlan_id1 = 5
        vlan_id2 = 6
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)

        warmboot(self.client)
        try:
            sys_logging("======create one port type router interface======")
            rif_id = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
            sys_logging("rif_id = 0x%x" %rif_id)
            assert (rif_id%0x100000000 == 0x0)

            sys_logging("======create one sub type router interface======")
            rif_id = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id)
            sys_logging("rif_id = 0x%x" %rif_id)
            assert (rif_id%0x100000000 == 0x0)

            sys_logging("======create one vlan type router interface======")
            rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
            sys_logging("rif_id = 0x%x" %rif_id1)
            assert (rif_id1%0x100000000 == 0x0)

            sys_logging("======create another vlan type router interface======")
            rif_id2 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
            sys_logging("rif_id1 = 0x%x" %rif_id2)
            assert (rif_id2%0x100000000 == 0x0)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            if chipname == "tsingma_mx":
                for i in range(0,8187):
                    self.client.sai_thrift_remove_router_interface(rif_id_list[i])
                for i in range(0,265):
                    self.client.sai_thrift_remove_vlan(vlan_oid_list[i])
            elif chipname == "tsingma":
                for i in range(0,4091):
                    self.client.sai_thrift_remove_router_interface(rif_id_list[i])
                for i in range(0,132):
                    self.client.sai_thrift_remove_vlan(vlan_oid_list[i])
            else:
                sys_logging("======chipname is error======")
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_virtual_router(vr_id1)

class fun_05_create_stats_enable_rif_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        rif_id_list = []
        vlan_oid_list = []
        vr_id1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        port1 = port_list[0]
        chipname = testutils.test_params_get()['chipname']
        sys_logging("chipname = %s" %chipname)

        if chipname == "tsingma_mx":
            sys_logging("======create 273 vlan and 7917 router interface(273+7917+1=8191)======")
            for i in range(10,283):
                vlan_id = i
                vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
                vlan_oid_list.append(vlan_oid)
                for j in range(29):
                    rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port_list[j], 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)
                    rif_id_list.append(rif_id1)
        elif chipname == "tsingma":
            sys_logging("======create 66 vlan and 1980 router interface(66+1980+1=2047)======")
            for i in range(10,76):
                vlan_id = i
                vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
                vlan_oid_list.append(vlan_oid)
                for j in range(30):
                    rif_id1 = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port_list[j], 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id)
                    rif_id_list.append(rif_id1)
        else:
            sys_logging("======chipname is error======")
        vlan_id1 = 300
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)

        warmboot(self.client)
        try:
            sys_logging("======create another sub type router interface======")
            rif_id = sai_thrift_create_router_interface(self.client, vr_id1, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
            sys_logging("rif_id = 0x%x" %rif_id)
            assert (rif_id == 0x0)

        finally:
            sys_logging("======clean up======")
            if chipname == "tsingma_mx":
                for i in range(0,7917):
                    self.client.sai_thrift_remove_router_interface(rif_id_list[i])
                for i in range(0,273):
                    self.client.sai_thrift_remove_vlan(vlan_oid_list[i])
            elif chipname == "tsingma":
                for i in range(0,1980):
                    self.client.sai_thrift_remove_router_interface(rif_id_list[i])
                for i in range(0,66):
                    self.client.sai_thrift_remove_vlan(vlan_oid_list[i])
            else:
                sys_logging("======chipname is error======")
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_virtual_router(vr_id1)

class fun_06_remove_rif_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        port1 = port_list[0]
        port2 = port_list[1]
        vlan_id1 = 10
        vlan_id2 = 20
        mac = ''
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        sys_logging("======create 6 type router interface======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, '')
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, 0, 0, v4_enabled, v6_enabled, '')
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, '')
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id2)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id3)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id4)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id5)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id6)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove 6 type router interface======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id2)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id3)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id4)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id5)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            self.client.sai_thrift_remove_router_interface(rif_id6)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id6)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)


        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


class fun_07_remove_no_exist_rif_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        port1 = port_list[0]
        vlan_id1 = 10
        mac = ''        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        sys_logging("======create 6 type router interface======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, vlan_oid1, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove no exist router interface======")
            status = self.client.sai_thrift_remove_router_interface(0x300008006)
            sys_logging("status = %d" %status)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove no exist router interface======")
            status = self.client.sai_thrift_remove_router_interface(0x0)
            sys_logging("status = %d" %status)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove correct router interface======")
            status = self.client.sai_thrift_remove_router_interface(rif_id1)
            sys_logging("status = %d" %status)
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
           

class fun_08_set_and_get_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        v4_mcast_enable = 0
        v6_mcast_enable = 0
        port1 = port_list[0]
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        warmboot(self.client)
        try:
            sys_logging("=======first get attribute=======")
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID:
                    if vr_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE:
                    if v4_enabled != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE:
                    if v6_enabled != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE:
                    if v4_mcast_enable != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE:
                    if v6_mcast_enable != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS:
                    print "get router_mac = %s" %a.value.mac
                    if router_mac != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_MTU:
                    print "get mtu = %d" %a.value.u32
                    if 1514 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION:
                    print "get action = %d" %a.value.s32
                    if SAI_PACKET_ACTION_TRAP != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                    if False != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL:
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_EGRESS_ACL:
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError()

         
            sys_logging("=======set all support attribute=======")
            v4_enabled = 0
            v6_enabled = 0
            v4_mcast_enable = 1
            v6_mcast_enable = 1
            vr_id1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
            vr_router_mac = "aa:bb:cc:dd:ee:ff"
            mtu = 9600
            action = SAI_PACKET_ACTION_TRANSIT

            attr_value = sai_thrift_attribute_value_t(oid=vr_id1)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            attr_value = sai_thrift_attribute_value_t(booldata=v4_enabled)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            attr_value = sai_thrift_attribute_value_t(booldata=v6_enabled)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            attr_value = sai_thrift_attribute_value_t(booldata=v6_mcast_enable)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            attr_value = sai_thrift_attribute_value_t(mac=vr_router_mac)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            attr_value = sai_thrift_attribute_value_t(u32=mtu)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_MTU, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)

            attr_value = sai_thrift_attribute_value_t(booldata = True)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            status = self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            sys_logging("### set router interface: status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            key_list   = [0, 1, 2, 3, 4, 5, 6, 7]
            value_list  = [1, 1, 1, 3, 3, 3, 5, 5]
            map_id = ctc_sai_qos_map._QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list, [], value_list)
            attr_value = sai_thrift_attribute_value_t(oid = map_id)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            status = self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            sys_logging("### set router interface: status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            key_list   = [0, 1, 2, 3, 4, 5, 6, 7]
            value_list  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                           SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                           SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
            map_id_dscp_color = ctc_sai_qos_map._QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list, [], value_list)
            attr_value = sai_thrift_attribute_value_t(oid = map_id_dscp_color)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            sys_logging("### set router interface: status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            key_list1  = [1, 1, 1, 3, 3, 3, 5, 5, 5]
            key_list2  = [SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                          SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN, 
                          SAI_PACKET_COLOR_RED, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_GREEN]
            value_list = [7, 6, 5, 4, 3, 2, 1, 0, 0]
            map_id_tc_and_color_dscp2 = ctc_sai_qos_map._QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, key_list1, key_list2 , value_list)
            print map_id_tc_and_color_dscp2
            attr_value = sai_thrift_attribute_value_t(oid = map_id_tc_and_color_dscp2)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            status = self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            sys_logging("### set router interface: status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            sys_logging("=======get attribute again=======")
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTER_INTERFACE_ATTR_VIRTUAL_ROUTER_ID:
                    if vr_id1 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE:
                    if v4_enabled != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE:
                    if v6_enabled != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE:
                    if v4_mcast_enable != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE:
                    if v6_mcast_enable != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS:
                    print "get router_mac = %s" %a.value.mac
                    if vr_router_mac != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_MTU:
                    print "get mtu = %d" %a.value.u32
                    if mtu != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION:
                    print "get action = %d" %a.value.s32
                    if action != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP:
                    if map_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    if map_id_dscp_color != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    if map_id_tc_and_color_dscp2 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP:
                    if True != a.value.booldata:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value = attr_value)
            status = self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            status = self.client.sai_thrift_remove_qos_map(map_id_tc_and_color_dscp2)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_COLOR_MAP, value = attr_value)
            status = self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            status = self.client.sai_thrift_remove_qos_map(map_id_dscp_color)
            attr_value = sai_thrift_attribute_value_t(oid = SAI_NULL_OBJECT_ID)
            attr       = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_QOS_DSCP_TO_TC_MAP, value = attr_value)
            status = self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            status = self.client.sai_thrift_remove_qos_map(map_id)
            attr_value = sai_thrift_attribute_value_t(booldata = False)
            attr = sai_thrift_attribute_t(id = SAI_ROUTER_INTERFACE_ATTR_UPDATE_DSCP, value = attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id, attr)
            self.client.sai_thrift_remove_router_interface(rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_virtual_router(vr_id1)

class fun_09_rif_set_stats_state_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
   
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = "aa:bb:cc:dd:ee:ff"

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac, stats_state = False)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        
        
       
        warmboot(self.client)
        try:
            sys_logging("=======first get attribute stats state=======")
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id1)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE:
                    sys_logging("rif_id1 stats state =%s" %a.value.booldata)
                    assert (a.value.booldata == False)

            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id2)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE:
                    sys_logging("rif_id2 stats state =%s" %a.value.booldata)
                    assert (a.value.booldata == True)

            sys_logging("=======set attribute stats state=======")
            attr_value = sai_thrift_attribute_value_t(booldata=1)        
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("=======get attribute stats state again=======")
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id1)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE:
                    sys_logging("rif_id1 stats state =%s" %a.value.booldata)
                    assert (a.value.booldata == True)

            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id2)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE:
                    sys_logging("rif_id2 stats state =%s" %a.value.booldata)
                    assert (a.value.booldata == False)
        finally:
            sys_logging("======clean up======")
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class fun_10_rif_default_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        port1 = port_list[0]
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        warmboot(self.client)
        try:
            sys_logging("======get default attribute======")
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS:
                    sys_logging("set router_mac = %s" %router_mac)
                    sys_logging("get router_mac = %s" %a.value.mac)
                    if router_mac != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_MTU:
                    sys_logging("get mtu = %d" %a.value.u32)
                    if 1514 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_NEIGHBOR_MISS_PACKET_ACTION:
                    sys_logging("get action = %d" %a.value.s32)
                    if SAI_PACKET_ACTION_TRAP != a.value.s32:
                        raise NotImplementedError()

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class fun_11_rif_get_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
   
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = "aa:bb:cc:dd:ee:ff"

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
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("=======first get stats=======")
            counter_ids = [SAI_ROUTER_INTERFACE_STAT_IN_OCTETS, SAI_ROUTER_INTERFACE_STAT_IN_PACKETS, SAI_ROUTER_INTERFACE_STAT_OUT_OCTETS, SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS]
            list1 = self.client.sai_thrift_router_interface_get_stats(rif_id1, counter_ids, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            list2 = self.client.sai_thrift_router_interface_get_stats(rif_id2, counter_ids, 4)
            assert (list2[0] == 0)
            assert (list2[1] == 0)
            assert (list2[2] == 0)
            assert (list2[3] == 0)

            sys_logging("=======send three packets and get stats=======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            list1 = self.client.sai_thrift_router_interface_get_stats(rif_id1, counter_ids, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 312)
            assert (list1[3] == 3)
            list2 = self.client.sai_thrift_router_interface_get_stats(rif_id2, counter_ids, 4)
            assert (list2[0] == 312)
            assert (list2[1] == 3)
            assert (list2[2] == 0)
            assert (list2[3] == 0)
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_12_rif_clear_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
   
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = "aa:bb:cc:dd:ee:ff"

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
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("=======first get stats=======")
            counter_ids = [SAI_ROUTER_INTERFACE_STAT_IN_OCTETS, SAI_ROUTER_INTERFACE_STAT_IN_PACKETS, SAI_ROUTER_INTERFACE_STAT_OUT_OCTETS, SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS]
            list1 = self.client.sai_thrift_router_interface_get_stats(rif_id1, counter_ids, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            list2 = self.client.sai_thrift_router_interface_get_stats(rif_id2, counter_ids, 4)
            assert (list2[0] == 0)
            assert (list2[1] == 0)
            assert (list2[2] == 0)
            assert (list2[3] == 0)

            sys_logging("=======send three packets and get stats=======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            
            sys_logging("=======fclear stats=======")
            self.client.sai_thrift_router_interface_clear_stats(rif_id1, counter_ids, 4)
            self.client.sai_thrift_router_interface_clear_stats(rif_id2, counter_ids, 4)
            list1 = self.client.sai_thrift_router_interface_get_stats(rif_id1, counter_ids, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            list2 = self.client.sai_thrift_router_interface_get_stats(rif_id2, counter_ids, 4)
            assert (list2[0] == 0)
            assert (list2[1] == 0)
            assert (list2[2] == 0)
            assert (list2[3] == 0)
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class fun_13_rif_get_and_clear_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
   
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = "aa:bb:cc:dd:ee:ff"

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
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("=======first get stats=======")
            counter_ids = [SAI_ROUTER_INTERFACE_STAT_IN_OCTETS, SAI_ROUTER_INTERFACE_STAT_IN_PACKETS, SAI_ROUTER_INTERFACE_STAT_OUT_OCTETS, SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS]
            list1 = self.client.sai_thrift_router_interface_get_stats(rif_id1, counter_ids, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            list2 = self.client.sai_thrift_router_interface_get_stats(rif_id2, counter_ids, 4)
            assert (list2[0] == 0)
            assert (list2[1] == 0)
            assert (list2[2] == 0)
            assert (list2[3] == 0)
            
            sys_logging("=======send one packets and get stats=======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            list1 = self.client.sai_thrift_router_interface_get_stats_ext(rif_id1, counter_ids, 0, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 104)
            assert (list1[3] == 1)
            list2 = self.client.sai_thrift_router_interface_get_stats_ext(rif_id2, counter_ids, 0, 4)
            assert (list2[0] == 104)
            assert (list2[1] == 1)
            assert (list2[2] == 0)
            assert (list2[3] == 0)

            sys_logging("=======send two packets,get and clear stats=======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            list1 = self.client.sai_thrift_router_interface_get_stats_ext(rif_id1, counter_ids, 1, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 312)
            assert (list1[3] == 3)
            list2 = self.client.sai_thrift_router_interface_get_stats_ext(rif_id2, counter_ids, 1, 4)
            assert (list2[0] == 312)
            assert (list2[1] == 3)
            assert (list2[2] == 0)
            assert (list2[3] == 0)

            sys_logging("=======get stats again=======")
            list1 = self.client.sai_thrift_router_interface_get_stats(rif_id1, counter_ids, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            list2 = self.client.sai_thrift_router_interface_get_stats(rif_id2, counter_ids, 4)
            assert (list2[0] == 0)
            assert (list2[1] == 0)
            assert (list2[2] == 0)
            assert (list2[3] == 0)
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_01_rif_routermac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
 
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac1 = "aa:bb:cc:dd:ee:ff"
        mac2 = "aa:bb:cc:dd:ee:fe"
        dmac1 = '00:11:22:33:44:55'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        pkt1 = simple_tcp_packet(eth_dst=mac1,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac1,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        pkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac1,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======receive packet with routermac mac1======")
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 1)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_no_packet( exp_pkt2, 1)

            sys_logging("======set attribute routermac======")
            attr_value = sai_thrift_attribute_value_t(mac=mac2)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("======receive packet with routermac mac2======")
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_no_packet( exp_pkt1, 1)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( exp_pkt2, 1)
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_02_rif_MTU_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        dmac1 = '00:11:22:33:44:55'
        mtu = 80
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send and receive packet when MTU is 1514======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

            sys_logging("======change MTU to 80======")
            attr_value = sai_thrift_attribute_value_t(u32=mtu)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_MTU, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            attr_value = sai_thrift_attribute_value_t(u32=mtu)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_MTU, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("======send packet again======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_03_bridge_rif_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        vlan1_id = 10
        vlan2_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac1 = '00:01:01:01:01:01'
        ip1 = '11.11.11.1'

        mac2 = '00:02:02:02:02:02'
        ip2 = '10.10.10.2'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        mac3 = '00:22:22:22:22:22'
        ip3 = '10.0.0.1'
        
        vlan1_oid = sai_thrift_create_vlan(self.client, vlan1_id)
        vlan2_oid = sai_thrift_create_vlan(self.client, vlan2_id)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port2, port3, port4])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan2_id)
        bport2_id = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan2_id)
        bport3_id = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id, vlan2_id)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, bport1_id, SAI_PACKET_ACTION_FORWARD)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        sub_port_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, vlan1_oid, v4_enabled, v6_enabled, '', outer_vlan_id=vlan1_id)
        sys_logging("======create bridge type rif======")
        bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, '')        
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_oid)

        sai_thrift_create_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV4, bridge_rif_oid, ip2, mac2)
        
        local_pkt = simple_tcp_packet(eth_src=mac2,
                                      eth_dst=mac3,
                                      dl_vlan_enable=True,
                                      vlan_vid=vlan2_id,
                                      ip_src=ip2,
                                      ip_dst=ip3,
                                      ip_id=102,
                                      ip_ttl=64)

        L3_pkt = simple_tcp_packet(eth_src=mac1,
                                   eth_dst=router_mac,
                                   ip_src=ip1,
                                   ip_dst=ip2,
                                   dl_vlan_enable=True,
                                   vlan_vid=vlan1_id,
                                   ip_id=105,
                                   ip_ttl=64)

        exp_pkt = simple_tcp_packet(eth_src=router_mac,
                                    eth_dst=mac2,
                                    ip_src=ip1,
                                    ip_dst=ip2,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan2_id,
                                    ip_id=105,
                                    ip_ttl=63)

        warmboot(self.client)
        try:
            sys_logging("======send packet and learning fdb======")
            print "Sending unknown L2 packet [{} -> {}] to learn FDB and flood within a .1D bridge".format(mac1, mac3)
            self.ctc_send_packet( 1, str(local_pkt))
            self.ctc_verify_packets( local_pkt, [2, 3])
            sys_logging("Success")

            print "Sending packet ({} -> {}) : Sub-port rif (port 1 : vlan {}) -> Bridge rif".format(ip1, ip2, vlan1_id)
            self.ctc_send_packet( 0, str(L3_pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            sys_logging("Success")

        finally:

            sai_thrift_remove_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV4, bridge_rif_oid, ip2, mac2)
            self.client.sai_thrift_remove_router_interface(sub_port_rif_oid)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(bridge_rif_oid)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, bport1_id)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport1_id, port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2_id, port3)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport3_id, port4)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            self.client.sai_thrift_remove_vlan(vlan1_oid)
            self.client.sai_thrift_remove_vlan(vlan2_oid)

class scenario_04_rif_v4_enabled_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        dmac1 = '00:11:22:33:44:55'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
       
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send and receive packet when v4_statu is enable======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

            sys_logging("======change v4_statu to disable======")
            v4_enabled = 0
            attr_value = sai_thrift_attribute_value_t(booldata=v4_enabled)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("======send packet again======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_05_rif_v6_enabled_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        dmac1 = '00:11:22:33:44:55'
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
   

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
       
        pkt = simple_tcpv6_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ipv6_dst=ip_addr1,
                                ipv6_src='2000::1:1',
                                ipv6_hlim=64)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ipv6_dst=ip_addr1,
                                ipv6_src='2000::1:1',
                                ipv6_hlim=63)
        warmboot(self.client)
        try:
            sys_logging("======send and receive packet when v6_statu is enable======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

            sys_logging("======change v6_statu to disable======")
            v6_enabled = 0
            attr_value = sai_thrift_attribute_value_t(booldata=v6_enabled)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_ADMIN_V6_STATE, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            sys_logging("======send packet again======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_06_virtual_rif_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Virtual Router Interface Test
        Step:
        1. Create router interface and virtual router interface
        2. Send packets to real interface and virtual router interface 
        3. Verify if packets received by correct port
        """
        
        #GoldenGate do not support virtual interface
        if 'goldengate' == testutils.test_params_get()['chipname']:
            return
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = "aa:bb:cc:dd:ee:ff"
        mac2 = "aa:aa:aa:aa:aa:aa"
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac2, is_virtual = True)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)
        sys_logging()
        pkt = simple_tcp_packet(eth_dst=mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        
        pkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send packet with macda:aa:bb:cc:dd:ee:ff======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

            sys_logging("======send packet with macda:aa:aa:aa:aa:aa:aa======")
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( exp_pkt2, 1)
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_07_stats_state_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
   
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = "aa:bb:cc:dd:ee:ff"

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac, stats_state = False)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac, stats_state = False)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("=======first get stats=======")
            counter_ids = [SAI_ROUTER_INTERFACE_STAT_IN_OCTETS, SAI_ROUTER_INTERFACE_STAT_IN_PACKETS, SAI_ROUTER_INTERFACE_STAT_OUT_OCTETS, SAI_ROUTER_INTERFACE_STAT_OUT_PACKETS]
            sys_logging("=======send one packets and get stats=======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            
            list1 = self.client.sai_thrift_router_interface_get_stats(rif_id1, counter_ids, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            list2 = self.client.sai_thrift_router_interface_get_stats(rif_id2, counter_ids, 4)
            assert (list2[0] == 0)
            assert (list2[1] == 0)
            assert (list2[2] == 0)
            assert (list2[3] == 0)

            sys_logging("=======set rif_id1 attribute stats state=======")
            attr_value = sai_thrift_attribute_value_t(booldata=1)        
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            
            sys_logging("=======send two packets and get stats=======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            list1 = self.client.sai_thrift_router_interface_get_stats(rif_id1, counter_ids, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 208)
            assert (list1[3] == 2)
            list2 = self.client.sai_thrift_router_interface_get_stats(rif_id2, counter_ids, 4)
            assert (list2[0] == 0)
            assert (list2[1] == 0)
            assert (list2[2] == 0)
            assert (list2[3] == 0)

            sys_logging("=======set rif_id2 attribute stats state=======")
            attr_value = sai_thrift_attribute_value_t(booldata=1)        
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_CUSTOM_STATS_STATE, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            
            sys_logging("=======send three packets and get stats=======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            list1 = self.client.sai_thrift_router_interface_get_stats(rif_id1, counter_ids, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 520)
            assert (list1[3] == 5)
            list2 = self.client.sai_thrift_router_interface_get_stats(rif_id2, counter_ids, 4)
            assert (list2[0] == 312)
            assert (list2[1] == 3)
            assert (list2[2] == 0)
            assert (list2[3] == 0)

            sys_logging("=======finally clear stats=======")
            self.client.sai_thrift_router_interface_clear_stats(rif_id1, counter_ids, 4)
            self.client.sai_thrift_router_interface_clear_stats(rif_id2, counter_ids, 4)
            list1 = self.client.sai_thrift_router_interface_get_stats(rif_id1, counter_ids, 4)
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            list2 = self.client.sai_thrift_router_interface_get_stats(rif_id2, counter_ids, 4)
            assert (list2[0] == 0)
            assert (list2[1] == 0)
            assert (list2[2] == 0)
            assert (list2[3] == 0)
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_08_stress_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 2
        mac = ''
        vlanid_list = []
        vlan_list = []
        rif_list = []
        chipname = testutils.test_params_get()['chipname']
        sys_logging("chipname = %s" %chipname)
        if chipname == "tsingma":
            rf_num1 = 4091
        elif chipname == "tsingma_mx":
            rf_num1 = 2047
        else:
            rf_num1 = 0
            sys_logging("======chipname is error======")
        rf_num2 = 4092
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        sys_logging("======create 4092 vlan======")
        for i in range(rf_num2):
            vlanid_list.append(vlan_id+i)
            vlan_list.append(sai_thrift_create_vlan(self.client, vlan_id+i))

        if chipname == "tsingma":
            sys_logging("======create %d sub router interface======" %rf_num1)
            for i in range(rf_num1):
                rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlanid_list[i], stats_state = False))
                #attrs = self.client.sai_thrift_get_router_interface_attribute(rif_list[i])
                #assert (attrs.status == SAI_STATUS_SUCCESS)
            sys_logging("======remove all router interface======")
            for i in range(rf_num1):
                self.client.sai_thrift_remove_router_interface(rif_list[i])
                #attrs = self.client.sai_thrift_get_router_interface_attribute(rif_list[i])
                #assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
            rif_list = []
            sys_logging("======create %d sub router interface again======" %rf_num1)
            for i in range(rf_num1):
                rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlanid_list[i], stats_state = False))
                #attrs = self.client.sai_thrift_get_router_interface_attribute(rif_list[i])
                #assert (attrs.status == SAI_STATUS_SUCCESS)
            sys_logging("======remove all router interface======")
            for i in range(rf_num1):
                self.client.sai_thrift_remove_router_interface(rif_list[i])
        elif chipname == "tsingma_mx":
            sys_logging("======create %d sub router interface======" %(rf_num1 * 4 - 1))
            for i in range(rf_num1):
                rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlanid_list[i], stats_state = False))
                rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlanid_list[i], stats_state = False))
                rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port3, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlanid_list[i], stats_state = False))
                if i == 2046:
                    continue
                else:
                    rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port4, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlanid_list[i], stats_state = False))
                #attrs = self.client.sai_thrift_get_router_interface_attribute(rif_list[i])
                #assert (attrs.status == SAI_STATUS_SUCCESS)
            sys_logging("======remove all router interface======")
            for i in range(rf_num1 * 4 - 1):
                self.client.sai_thrift_remove_router_interface(rif_list[i])
                #attrs = self.client.sai_thrift_get_router_interface_attribute(rif_list[i])
                #assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
            rif_list = []
            sys_logging("======create %d sub router interface again======" %(rf_num1 * 4 - 1))
            for i in range(rf_num1):
                rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlanid_list[i], stats_state = False))
                rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlanid_list[i], stats_state = False))
                rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port3, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlanid_list[i], stats_state = False))
                if i == 2046:
                    continue
                else:
                    rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port4, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlanid_list[i], stats_state = False))
                #attrs = self.client.sai_thrift_get_router_interface_attribute(rif_list[i])
                #assert (attrs.status == SAI_STATUS_SUCCESS)
            sys_logging("======remove all router interface======")
            for i in range(rf_num1 * 4 - 1):
                self.client.sai_thrift_remove_router_interface(rif_list[i])
        else:
            sys_logging("======chipname is error======")

        rif_list = []
        sys_logging("======create 4092 vlan router interface======")
        for i in range(rf_num2):
            rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, port1, vlan_list[i], v4_enabled, v6_enabled, mac, stats_state = False))
            #attrs = self.client.sai_thrift_get_router_interface_attribute(rif_list[i])
            #assert (attrs.status == SAI_STATUS_SUCCESS)

        sys_logging("======remove all router interface======")
        for i in range(rf_num2):
            self.client.sai_thrift_remove_router_interface(rif_list[i])

        rif_list = []
        sys_logging("======create 4092 vlan router interface again======")
        for i in range(rf_num2):
            rif_list.append(sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, port1, vlan_list[i], v4_enabled, v6_enabled, mac, stats_state = False))
            #attrs = self.client.sai_thrift_get_router_interface_attribute(rif_list[i])
            #assert (attrs.status == SAI_STATUS_SUCCESS)

        sys_logging("======remove all router interface======")
        for i in range(rf_num2):
            self.client.sai_thrift_remove_router_interface(rif_list[i])
            #attrs = self.client.sai_thrift_get_router_interface_attribute(rif_list[i])
            #assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

        for i in range(rf_num2):
            self.client.sai_thrift_remove_vlan(vlan_list[i])
        sys_logging("======clean up======")
        self.client.sai_thrift_remove_virtual_router(vr_id)

##bug110526
class scenario_09_create_multi_sub_if_then_del_one_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
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

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id1)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port3, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port3, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id1)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port4, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id1)
        self.client.sai_thrift_remove_router_interface(rif_id2)
        self.client.sai_thrift_remove_router_interface(rif_id3)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id5, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id5)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=20,
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
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 3)

        finally:
            sys_logging("======clean up======")
            #pdb.set_trace()
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id5, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)

            self.client.sai_thrift_remove_virtual_router(vr_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag(self.client, lag_id1)


class scenario_10_set_system_vrf_routermac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
 
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac1 = "00:01:00:01:00:01"
        mac2 = "00:01:00:01:00:02"
        mac3 = "00:01:00:01:00:03"
        mac4 = "00:01:00:01:00:04"
        mac5 = "00:01:00:01:00:05"
        new_sys_mac = "00:10:00:01:00:01"
        dmac1 = '00:11:22:33:44:55'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        vr_id = sai_thrift_get_default_router_id(self.client)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

        vr_id2 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        attr_value = sai_thrift_attribute_value_t(mac=mac2)
        attr = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS, value=attr_value)
        #pdb.set_trace()
        self.client.sai_thrift_set_virtual_router_attribute(vr_id2, attr)
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac3)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_addr2, dmac1)
        

        pkt1 = simple_tcp_packet(eth_dst=mac1,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst=mac4,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        pkt7 = simple_tcp_packet(eth_dst=mac2,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac1,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)                                
                                
        pkt4 = simple_tcp_packet(eth_dst=mac2,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        pkt5 = simple_tcp_packet(
                                eth_dst=mac3,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        pkt6 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        pkt8 = simple_tcp_packet(eth_dst=mac5,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac3,
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======receive packet with routermac mac1======")
            
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 1)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( exp_pkt1, 1)
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_no_packet( exp_pkt1, 1)

            self.ctc_send_packet( 4, str(pkt4))
            self.ctc_verify_packet( exp_pkt2, 3)
            self.ctc_send_packet( 4, str(pkt5))
            self.ctc_verify_packet( exp_pkt2, 3)
            self.ctc_send_packet( 4, str(pkt6))
            self.ctc_verify_no_packet( exp_pkt2, 3)
            

            sys_logging("======set switch routermac======")
            attr_value = sai_thrift_attribute_value_t(mac=mac4)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            #pdb.set_trace()
            
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 1)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_no_packet( exp_pkt1, 1)
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packet( exp_pkt1, 1)

            self.ctc_send_packet( 4, str(pkt4))
            self.ctc_verify_packet( exp_pkt2, 3)
            self.ctc_send_packet( 4, str(pkt5))
            self.ctc_verify_packet( exp_pkt2, 3)
            self.ctc_send_packet( 4, str(pkt6))
            self.ctc_verify_no_packet( exp_pkt2, 3)
            
            
            sys_logging("======set vrf routermac======")
            attr_value = sai_thrift_attribute_value_t(mac=mac2)
            attr = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_virtual_router_attribute(vr_id, attr)
            attr_value = sai_thrift_attribute_value_t(mac=mac5)
            attr = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_virtual_router_attribute(vr_id2, attr)
            #pdb.set_trace()

            sys_logging("======receive packet with routermac mac2======")
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 1)
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_no_packet( exp_pkt1, 1)
            self.ctc_send_packet( 2, str(pkt7))
            self.ctc_verify_packet( exp_pkt1, 1)

            self.ctc_send_packet( 4, str(pkt8))
            self.ctc_verify_packet( exp_pkt2, 3)
            self.ctc_send_packet( 4, str(pkt5))
            self.ctc_verify_packet( exp_pkt2, 3)
            self.ctc_send_packet( 4, str(pkt4))
            self.ctc_verify_no_packet( exp_pkt2, 3)
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            #self.client.sai_thrift_remove_virtual_router(vr_id)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_addr2, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id2)

            attr_value = sai_thrift_attribute_value_t(mac=router_mac)
            attr = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_virtual_router_attribute(vr_id, attr)

            attr_value = sai_thrift_attribute_value_t(mac=router_mac)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class scenario_11_set_rif_routermac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
 
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac1 = "00:01:00:01:00:01"
        mac2 = "00:01:00:01:00:02"
        mac3 = "00:01:00:01:00:03"
        mac4 = "00:01:00:01:00:04"
        mac5 = "00:01:00:01:00:05"
        new_sys_mac = "00:10:00:01:00:01"
        dmac1 = '00:11:22:33:44:55'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        vr_id = sai_thrift_get_default_router_id(self.client)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

        vr_id2 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        attr_value = sai_thrift_attribute_value_t(mac=mac2)
        attr = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS, value=attr_value)
        #pdb.set_trace()
        self.client.sai_thrift_set_virtual_router_attribute(vr_id2, attr)
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac3)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_addr2, dmac1)
        

        pkt1 = simple_tcp_packet(eth_dst=mac1,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst=mac3,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac1,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)                                
        exp_pkt2 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac3,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)                                 
        pkt4 = simple_tcp_packet(eth_dst=mac2,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        pkt5 = simple_tcp_packet(
                                eth_dst=mac3,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        pkt6 = simple_tcp_packet(eth_dst=mac1,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt3 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac3,
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt4 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=mac1,
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======receive packet with routermac mac1======")
            
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 1)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( exp_pkt1, 1)
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_no_packet( exp_pkt1, 1)

            self.ctc_send_packet( 4, str(pkt4))
            self.ctc_verify_packet( exp_pkt3, 3)
            self.ctc_send_packet( 4, str(pkt5))
            self.ctc_verify_packet( exp_pkt3, 3)
            self.ctc_send_packet( 4, str(pkt6))
            self.ctc_verify_no_packet( exp_pkt3, 3)
            

            sys_logging("======set rif routermac======")
            attr_value = sai_thrift_attribute_value_t(mac=mac3)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)

            attr_value = sai_thrift_attribute_value_t(mac=mac1)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
            self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)
            #pdb.set_trace()
            
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_no_packet( exp_pkt2, 1)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( exp_pkt2, 1)
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packet( exp_pkt2, 1)

            self.ctc_send_packet( 4, str(pkt4))
            self.ctc_verify_packet( exp_pkt4, 3)
            self.ctc_send_packet( 4, str(pkt5))
            self.ctc_verify_no_packet( exp_pkt4, 3)
            self.ctc_send_packet( 4, str(pkt6))
            self.ctc_verify_packet( exp_pkt4, 3)
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            #self.client.sai_thrift_remove_virtual_router(vr_id)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_addr2, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id2)

            attr_value = sai_thrift_attribute_value_t(mac=router_mac)
            attr = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_virtual_router_attribute(vr_id, attr)

            attr_value = sai_thrift_attribute_value_t(mac=router_mac)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)


