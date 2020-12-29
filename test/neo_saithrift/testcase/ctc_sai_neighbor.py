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

class fun_01_neighbor_v4_create_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family=SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'  
        warmboot(self.client)
        try:
            sys_logging("======create a v4 neighbor======")
            status = sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)   
           
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_02_neighbor_v6_create_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family=SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac1 = '00:11:22:33:44:55'
        warmboot(self.client)
        try:
            sys_logging("======create a v6 neighbor======")
            status = sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)  
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_03_neighbor_v4_create_exist_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family=SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sys_logging("======create a v4 neighbor first======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        warmboot(self.client)
        try:
            sys_logging("======create a same v4 neighbor======")
            status = sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS)   
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_04_neighbor_v6_create_exist_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family=SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac1 = '00:11:22:33:44:55'
        sys_logging("======create a v6 neighbor first======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        warmboot(self.client)
        try:
            sys_logging("======create a same v6 neighbor======")
            status = sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS)  
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_05_neighbor_v4_max_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        dest_mac = []
        ip_addr = []
        mac = ''

        neighbor_num = 65535

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_mac_start = '00:22:22:{0}:{0}:{0}'

        for i in range(0, 7):
            for j in range(0, 100):
                for m in range(0, 100):
                    src_mac = src_mac_start.format(str(i).zfill(4)[2:],str(j).zfill(4)[2:],str(m).zfill(4)[2:])
                    dest_mac.append(src_mac)

        sys_logging("======create %d(max) v4 neighbor first======" %neighbor_num)
        for i in range(neighbor_num):
            ip_addr.append(integer_to_ip4(1+i))
            sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i], no_host_route = True)

        addr_family=SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        warmboot(self.client)
        try:
            sys_logging("======create another v4 neighbor======")
            status = sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1, no_host_route = True)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_INSUFFICIENT_RESOURCES)
        finally:
            sys_logging("======clean up======")
            for i in range(neighbor_num):
                sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_06_neighbor_v6_max_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        dest_mac = []
        ip_addr = []
        mac = ''

        neighbor_num = 65535

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        src_mac_start = '00:22:22:{0}:{0}:{0}'

        for i in range(0, 7):
            for j in range(0, 100):
                for m in range(0, 100):
                    src_mac = src_mac_start.format(str(i).zfill(4)[2:],str(j).zfill(4)[2:],str(m).zfill(4)[2:])
                    dest_mac.append(src_mac)

        sys_logging("======create %d(max) v6 neighbor first======" %neighbor_num)
        for i in range(neighbor_num):
            ip_addr.append(integer_to_ip6(1+i))
            sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i], no_host_route = True)
        addr_family=SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac1 = '00:11:22:33:44:55'
        warmboot(self.client)
        try:
            sys_logging("======create another v6 neighbor======")
            status = sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1, no_host_route = True)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_INSUFFICIENT_RESOURCES)
        finally:
            sys_logging("======clean up======")
            for i in range(neighbor_num):
                sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_07_neighbor_v4_remove_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family=SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.11.1'
        dmac1 = '00:11:22:33:44:55'

        sys_logging("======create a v4 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip4=ip_addr1)
            ipaddr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove the v4 neighbor======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_08_neighbor_v6_remove_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family=SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("======create a v4 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip6=ip_addr1)
            ipaddr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove the v4 neighbor======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_09_neighbor_v4_remove_no_exist_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family=SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.11.1'
        ip_addr2 = '10.10.11.2'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'

        sys_logging("======create a v4 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip4=ip_addr1)
            ipaddr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove no exist v4 neighbor======")
            status = sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove no exist v4 neighbor======")
            status = sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr2, dmac1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_10_neighbor_v6_remove_no_exist_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family=SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:99ab'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'

        sys_logging("======create a v6 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip6=ip_addr1)
            ipaddr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove no exist v6 neighbor======")
            status = sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove no exist v6 neighbor======")
            status = sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr2, dmac1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class fun_11_neighbor_set_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family=SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'

        sys_logging("======create a v4 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip4=ip_addr1)
            ipaddr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)
           
            sys_logging("======get all support attribute======")
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS:
                    sys_logging("set dest mac = %s" %dmac1)
                    sys_logging("get dest mac = %s" %a.value.mac)
                    if dmac1 != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE:
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
                        
            sys_logging("======set all support attribute======")
            dmac2 = 'aa:bb:cc:dd:ee:ff'
            attr_value = sai_thrift_attribute_value_t(mac=dmac2)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRANSIT)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)
            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)

            sys_logging("======get all support attribute again======")
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS:
                    sys_logging("set dest mac = %s" %dmac1)
                    sys_logging("get dest mac = %s" %a.value.mac)
                    if dmac2 != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION:
                    if SAI_PACKET_ACTION_TRANSIT != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE:
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_12_neighbor_set_unsupported_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family=SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'

        sys_logging("======create a v4 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip4=ip_addr1)
            ipaddr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)
           
            sys_logging("======get all not support attribute======")
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_COUNTER_ID, value=attr_value)
            status = self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_INVALID_ATTRIBUTE_0)
            
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_USER_TRAP_ID, value=attr_value)
            status = self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_INVALID_ATTRIBUTE_0)
            
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_META_DATA, value=attr_value)
            status = self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_INVALID_ATTRIBUTE_0)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
class fun_13_neighbor_get_default_attribute(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family=SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("======create a v4 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip4=ip_addr1)
            ipaddr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)

            sys_logging("======set all support attribute default value======")
            attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE:
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_14_neighbor_remove_all_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        cnt = 256;

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        dmac1 = '00:11:22:33:44:55'
        ipv4_addr = '10.10.10.1'
        ipv6_addr = '1234:5678:9abc:def0:4422:1133:5577:99aa'

        sys_logging("======create 256 v4 neighbor and v6 neighbor======")
        for i in range(cnt):
            ipv4_int = ip4_to_integer(ipv4_addr)+i
            ip_addr1 = integer_to_ip4(ipv4_int)
            sai_thrift_create_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV4, rif_id1, ip_addr1, dmac1)
            
            ipv6_int = ip6_to_integer(ipv6_addr)+i
            ip_addr2 = integer_to_ip6(ipv6_int)
            sai_thrift_create_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV6, rif_id1, ip_addr2, dmac1)

        sys_logging("======remove all neighbor======")
        self.client.sai_thrift_remove_all_neighbor_entry()

        warmboot(self.client)
        try:
            sys_logging("======get all neighbor attribute======")
            for i in range(cnt):
                ipv4_int = ip4_to_integer(ipv4_addr)+i
                ip_addr1 = integer_to_ip4(ipv4_int)
                addr = sai_thrift_ip_t(ip4=ip_addr1)
                ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
                neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)
                attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
                sys_logging("status = %d" %attrs.status)
                assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
                
                ipv6_int = ip6_to_integer(ipv6_addr)+i
                ip_addr2 = integer_to_ip6(ipv6_int)
                addr = sai_thrift_ip_t(ip6=ip_addr2)
                ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
                neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)
                attrs = self.client.sai_thrift_get_neighbor_entry_attribute(neighbor_entry)
                sys_logging("status = %d" %attrs.status)
                assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_01_neighbor_v4_receive_packet_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac1 = '00:11:22:33:44:55'
        sys_logging("======create a v4 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

        pkt1 = simple_tcp_packet(eth_dst=mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        pkt2 = simple_tcp_packet(eth_dst=mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=mac,
                                ip_dst='10.10.10.2',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send ipv4 hit packet======")
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 1)

            sys_logging("======send ipv4 not hit packet======")
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_no_packet( exp_pkt2, 1)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_02_neighbor_v6_receive_packet_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = "aa:bb:cc:dd:ee:ff"

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '2000::1:1'
        dmac1 = '00:11:22:33:44:55'
        sys_logging("======create a v6 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

        pkt1 = simple_tcpv6_packet(eth_dst=mac,
                                  eth_src='00:22:22:22:22:22',
                                  ipv6_dst='2000::1:1',
                                  ipv6_src='2000::0:1',
                                  ipv6_hlim=64)
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                      eth_src=mac,
                                      ipv6_dst='2000::1:1',
                                      ipv6_src='2000::0:1',
                                      ipv6_hlim=63)

        pkt2 = simple_tcpv6_packet(eth_dst=mac,
                                  eth_src='00:22:22:22:22:22',
                                  ipv6_dst='2000::1:2',
                                  ipv6_src='2000::0:1',
                                  ipv6_hlim=64)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                      eth_src=mac,
                                      ipv6_dst='2000::1:2',
                                      ipv6_src='2000::0:1',
                                      ipv6_hlim=63)
        warmboot(self.client)
        try:
            sys_logging("======send ipv6 hit packet======")
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 1)

            sys_logging("======send ipv6 not hit packet======")
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_no_packet( exp_pkt2, 1)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_03_neighbor_macda_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:66'
        sys_logging("======create a v4 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

        pkt = simple_tcp_packet(eth_dst=mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt2 = simple_tcp_packet(
                                eth_dst=dmac2,
                                eth_src=mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send packet and receive packet with macda='00:11:22:33:44:55' ======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt1, 1)

            sys_logging("======set neighbor dst mac to '00:11:22:33:44:66'======")
            addr = sai_thrift_ip_t(ip4=ip_addr1)
            ipaddr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)
            attr_value = sai_thrift_attribute_value_t(mac=dmac2)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_DST_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)

            sys_logging("======send packet and receive packet with macda='00:11:22:33:44:66' ======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt2, 1)            

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_04_neighbor_no_host_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac1 = '00:11:22:33:44:55'
        sys_logging("======create a v4 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

        pkt = simple_tcp_packet(eth_dst=mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send packet,no_host_route state is disabled ======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

            addr = sai_thrift_ip_t(ip4=ip_addr1)
            ipaddr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)

            sys_logging("======set neighbor no_host_route state to enabled======")   
            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)

            sys_logging("======send packet again ======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1)

            sys_logging("======set neighbor no_host_route state to disabled======")
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)

            sys_logging("======send packet again ======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_05_neighbor_packet_action_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac1 = '00:11:22:33:44:55'
        sys_logging("======create a v4 neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

        pkt = simple_tcp_packet(eth_dst=mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send packet======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

            addr = sai_thrift_ip_t(ip4=ip_addr1)
            ipaddr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            neighbor_entry = sai_thrift_neighbor_entry_t(rif_id=rif_id1, ip_address=ipaddr)

            sys_logging("======set neighbor packet action to DENY======") 
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DENY)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)

            sys_logging("======send packet again======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1)

            sys_logging("======set neighbor packet action to TRANSIT======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRANSIT)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

            sys_logging("======set neighbor packet action to DROP======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)

            sys_logging("======send packet again======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1)

            sys_logging("======set neighbor packet action to FORWARD======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)

            sys_logging("======send packet again======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

            sys_logging("======set neighbor packet action to COPY======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_COPY)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)

            sys_logging("======send packet again======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1)

            sys_logging("======set neighbor packet action to FORWARD======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)

            sys_logging("======send packet again======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

            sys_logging("======set neighbor packet action to TRAP======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRAP)
            attr = sai_thrift_attribute_t(id=SAI_NEIGHBOR_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_neighbor_entry_attribute(neighbor_entry, attr)

            sys_logging("======send packet again======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_06_neighbor_update_by_FDB_Test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        mac = ''

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sys_logging("======create a v4 neighbor with vlan router interface======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send packet when have not dst port======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1)
            
            sys_logging("======add a fdb entry======") 
            sai_thrift_create_fdb(self.client, vlan_oid, dmac1, port2, SAI_PACKET_ACTION_FORWARD)

            sys_logging("======send packet again======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            sys_logging("======delete the fdb entry======")
            sai_thrift_delete_fdb(self.client, vlan_oid, dmac1, port2)

            sys_logging("======send packet again======")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1)


        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_07_neighbor_add_by_nexthop_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
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
        
        sys_logging("======create next hop first======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        sys_logging("======create neighbor and route======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

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
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            sys_logging("======send packet======")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_08_neighbor_create_nexthop_first(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'

        sys_logging("======for bug 109805======")
        sys_logging("======create next hop first======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        sys_logging("======create and remove a neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
       
        warmboot(self.client)
        try:
            sys_logging("======create the neighbor again======")
            status = sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            assert (status == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_09_neighbor_v4_stress_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        dest_mac = []
        ip_addr = []
        mac = ''
        neighbor_num = 1023
        loop_num = 2
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_mac_start = ['01:22:33:44:55:', '11:22:33:44:55:', '21:22:33:44:55:', '31:22:33:44:55:', '41:22:33:44:55:', '51:22:33:44:55:', '61:22:33:44:55:', '71:22:33:44:55:', '81:22:33:44:55:', '91:22:33:44:55:', 'a1:22:33:44:55:']
        try:
            sys_logging("======create and remove v4 neighbor======")
            for j in range(loop_num):
                for i in range(neighbor_num):
                    dest_mac.append(src_mac_start[i/99] + str(i%99).zfill(2))
                    ip_addr.append(integer_to_ip4(1+i))
                    sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
                for i in range(neighbor_num):
                    sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
                    
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_10_v4_stress_send_packet_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        dest_mac = []
        ip_addr = []
        mac = ''
        neighbor_num = 128
        loop_num = 2
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_mac_start = ['01:22:33:44:55:', '11:22:33:44:55:', '21:22:33:44:55:', '31:22:33:44:55:', '41:22:33:44:55:', '51:22:33:44:55:', '61:22:33:44:55:', '71:22:33:44:55:', '81:22:33:44:55:', '91:22:33:44:55:', 'a1:22:33:44:55:']
        try:
            sys_logging("======create and remove v4 neighbor======")

            for i in range(neighbor_num):
                dest_mac.append(src_mac_start[i/99] + str(i%99).zfill(2))
                ip_addr.append(integer_to_ip4(1+i))
                sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
            #pdb.set_trace()
            for k in range(neighbor_num):
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr[k],
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
                exp_pkt = simple_tcp_packet(
                                eth_dst=dest_mac[k],
                                eth_src=router_mac,
                                ip_dst=ip_addr[k],
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
                self.ctc_send_packet( 0, str(pkt))
                self.ctc_verify_packets( exp_pkt, [1])
        finally:
            sys_logging("======clean up======")
            
            for i in range(neighbor_num):
                sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_11_neighbor_v6_stress_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        dest_mac = []
        ip_addr = []
        mac = ''
        neighbor_num = 1023
        loop_num = 2

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        dest_ip = '1234:5678:9abc:def0:4422:1133:5577:0000'
        dest_int = ip6_to_integer(dest_ip)
        src_mac_start = ['01:22:33:44:55:', '11:22:33:44:55:', '21:22:33:44:55:', '31:22:33:44:55:', '41:22:33:44:55:', '51:22:33:44:55:', '61:22:33:44:55:', '71:22:33:44:55:', '81:22:33:44:55:', '91:22:33:44:55:', 'a1:22:33:44:55:']
        try:
            sys_logging("======create and remove v6 neighbor======")
            for j in range(loop_num):
                for i in range(neighbor_num):
                    dest_mac.append(src_mac_start[i/99] + str(i%99).zfill(2))
                    ip_addr.append(integer_to_ip6(dest_int+i))
                    sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
                for i in range(neighbor_num):
                    sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
                    
        finally:     
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_12_v6_stress_send_packet_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        dest_mac = []
        ip_addr = []
        mac = ''
        neighbor_num = 128
        loop_num = 2

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        dest_ip = '1234:5678:9abc:def0:4422:1133:5577:0000'
        dest_int = ip6_to_integer(dest_ip)
        src_mac_start = ['01:22:33:44:55:', '11:22:33:44:55:', '21:22:33:44:55:', '31:22:33:44:55:', '41:22:33:44:55:', '51:22:33:44:55:', '61:22:33:44:55:', '71:22:33:44:55:', '81:22:33:44:55:', '91:22:33:44:55:', 'a1:22:33:44:55:']
        try:
            sys_logging("======create and remove v6 neighbor======")
            for i in range(neighbor_num):
                dest_mac.append(src_mac_start[i/99] + str(i%99).zfill(2))
                ip_addr.append(integer_to_ip6(dest_int+i))
                sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
            for k in range(neighbor_num):
                pkt = simple_tcpv6_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ipv6_dst=ip_addr[k],
                                ipv6_src='2000::0:1',
                                ipv6_hlim=64)
                exp_pkt = simple_tcpv6_packet(eth_dst=dest_mac[k],
                                  eth_src=router_mac,
                                  ipv6_dst=ip_addr[k],
                                  ipv6_src='2000::0:1',
                                  ipv6_hlim=63)
                
                self.ctc_send_packet( 0, str(pkt))
                self.ctc_verify_packets( exp_pkt, [1])
                
        finally:   
            for i in range(neighbor_num):
                    sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
                    
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)




