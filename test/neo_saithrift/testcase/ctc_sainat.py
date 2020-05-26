# Copyright 2013-present Centec Networks, Inc.
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
Thrift SAI interface NAT tests
"""
import socket
from switch import *
import sai_base_test

@group('nat')
def ip4_to_integer(ip4):
    ip4int = int(socket.inet_aton('10.10.10.1').encode('hex'), 16)
    return ip4int

def integer_to_ip4(ip4int):
    return socket.inet_ntoa(hex(ip4int)[2:].zfill(8).decode('hex'))
    

class SNATCreateTest(sai_base_test.ThriftInterfaceDataPlane):
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
        srcip_addr = '10.10.10.1'
        #dstip_addr = '20.20.20.1'
        proto = 6
        l4_srcport = 1000
        #l4_dstport = 2000
        
        ipmask = '255.255.255.255'
        protomask = 0xff
        l4portmask = 0xffff

        #dmac1 = '00:11:22:33:44:55'
        
        keylist = [srcip_addr, '', proto, l4_srcport, 0]
        masklist = [ipmask, ipmask, protomask, l4portmask, l4portmask]
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        #nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        
        mod_srcip_addr = '100.100.100.1'
        #mod_dstip_addr = '200.200.200.1'
        
        mod_l4_srcport = 1001
        
        nat_type = SAI_NAT_TYPE_SOURCE_NAT
        status = sai_thrift_create_nat(self.client, vr_id, nat_type, keylist, masklist, mod_srcip_addr, None, mod_l4_srcport, None)
        sys_logging("creat status = %d" %status)
        #status = sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
        #print "remove status = %d" %status

        warmboot(self.client)
        try:
            status = sai_thrift_create_nat(self.client, vr_id, nat_type, keylist, masklist, mod_srcip_addr, None, mod_l4_srcport, None)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS) 

            nat = sai_thrift_nat_entry_t(vr_id, keylist[0], keylist[1], keylist[2], keylist[3], keylist[4], masklist[0], masklist[1], masklist[2], masklist[3], masklist[4])
            
            attrs = self.client.sai_thrift_get_nat_attribute(nat)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NAT_ENTRY_ATTR_NAT_TYPE:
                    sys_logging("set nat type = 0x%x" %nat_type)
                    sys_logging("get nat type = 0x%x" %a.value.s32)
                    if nat_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_NAT_ENTRY_ATTR_L4_SRC_PORT:
                    sys_logging("set l4 src port = 0x%x" %mod_l4_srcport)
                    sys_logging("get l4 src port = 0x%x" %a.value.u16)
                    if nat_type != a.value.s32:
                        raise NotImplementedError()
        
        finally:
            sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
            #self.client.sai_thrift_remove_next_hop(nhop1)
            #sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
        
            self.client.sai_thrift_remove_virtual_router(vr_id)

class DNATCreateTest(sai_base_test.ThriftInterfaceDataPlane):
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
        #srcip_addr = '10.10.10.1'
        dstip_addr = '20.20.20.1'
        proto = 6
        #l4_srcport = 1000
        l4_dstport = 2000
        
        ipmask = '255.255.255.255'
        protomask = 0xff
        l4portmask = 0xffff

        
        dmac1 = '00:11:22:33:44:55'
        #ip_addr_subnet = '200.200.200.0'
        ip_mask = '255.255.255.255'
        
        #mod_srcip_addr = '100.100.100.1'
        mod_dstip_addr = '200.200.200.1'
        
        mod_l4_dstport = 2001
        
        keylist = ['', dstip_addr, proto, 0, l4_dstport]
        masklist = [ipmask, ipmask, protomask, l4portmask, l4portmask]
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, mod_dstip_addr, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, mod_dstip_addr, rif_id1)
        
        sai_thrift_create_route(self.client, vr_id, addr_family, mod_dstip_addr, ip_mask, nhop1)
        
        nat_type = SAI_NAT_TYPE_DESTINATION_NAT
        
        status = sai_thrift_create_nat(self.client, vr_id, nat_type, keylist, masklist, None, mod_dstip_addr, None, mod_l4_dstport)
        sys_logging("creat status = %d" %status)
        #status = sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
        #print "remove status = %d" %status

        warmboot(self.client)
        try:
            status = sai_thrift_create_nat(self.client, vr_id, nat_type, keylist, masklist, None, mod_dstip_addr, None, mod_l4_dstport)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS) 

            nat = sai_thrift_nat_entry_t(vr_id, keylist[0], keylist[1], keylist[2], keylist[3], keylist[4], masklist[0], masklist[1], masklist[2], masklist[3], masklist[4])
            attrs = self.client.sai_thrift_get_nat_attribute(nat)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NAT_ENTRY_ATTR_NAT_TYPE:
                    sys_logging("set nat type = 0x%x" %nat_type)
                    sys_logging("get nat type = 0x%x" %a.value.s32)
                    if nat_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_NAT_ENTRY_ATTR_L4_DST_PORT:
                    sys_logging("set l4 src port = 0x%x" %mod_l4_dstport)
                    sys_logging("get l4 src port = 0x%x" %a.value.u16)
                    if nat_type != a.value.s32:
                        raise NotImplementedError()
        
        finally:
            sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
            sai_thrift_remove_route(self.client, vr_id, addr_family, mod_dstip_addr, ip_mask, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, mod_dstip_addr, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
        
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
class SNATRemoveTest(sai_base_test.ThriftInterfaceDataPlane):
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
        srcip_addr = '10.10.10.1'
        #dstip_addr = '20.20.20.1'
        proto = 6
        l4_srcport = 1000
        #l4_dstport = 2000
        
        ipmask = '255.255.255.255'
        protomask = 0xff
        l4portmask = 0xffff

        #dmac1 = '00:11:22:33:44:55'
        
        keylist = [srcip_addr, '', proto, l4_srcport, 0]
        masklist = [ipmask, ipmask, protomask, l4portmask, l4portmask]
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        #nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        
        mod_srcip_addr = '100.100.100.1'
        #mod_dstip_addr = '200.200.200.1'
        
        mod_l4_srcport = 1001
        
        nat_type = SAI_NAT_TYPE_SOURCE_NAT
        status = sai_thrift_create_nat(self.client, vr_id, nat_type, keylist, masklist, mod_srcip_addr, None, mod_l4_srcport, None)
        sys_logging("creat status = %d" %status)
        status = sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
        sys_logging("remove status = %d" %status)

        warmboot(self.client)
        try:
            nat = sai_thrift_nat_entry_t(vr_id, keylist[0], keylist[1], keylist[2], keylist[3], keylist[4], masklist[0], masklist[1], masklist[2], masklist[3], masklist[4])
            
            attrs = self.client.sai_thrift_get_nat_attribute(nat)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        
        finally:
            #sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
            #self.client.sai_thrift_remove_next_hop(nhop1)
            #sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
        
            self.client.sai_thrift_remove_virtual_router(vr_id)

class DNATRemoveTest(sai_base_test.ThriftInterfaceDataPlane):
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
        #srcip_addr = '10.10.10.1'
        dstip_addr = '20.20.20.1'
        proto = 6
        #l4_srcport = 1000
        l4_dstport = 2000
        
        ipmask = '255.255.255.255'
        protomask = 0xff
        l4portmask = 0xffff

        
        dmac1 = '00:11:22:33:44:55'
        #ip_addr_subnet = '200.200.200.0'
        ip_mask = '255.255.255.255'
        
        #mod_srcip_addr = '100.100.100.1'
        mod_dstip_addr = '200.200.200.1'
        
        mod_l4_dstport = 2001
        
        keylist = ['', dstip_addr, proto, 0, l4_dstport]
        masklist = [ipmask, ipmask, protomask, l4portmask, l4portmask]
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, mod_dstip_addr, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, mod_dstip_addr, rif_id1)
        
        sai_thrift_create_route(self.client, vr_id, addr_family, mod_dstip_addr, ip_mask, nhop1)
        
        nat_type = SAI_NAT_TYPE_DESTINATION_NAT
        
        status = sai_thrift_create_nat(self.client, vr_id, nat_type, keylist, masklist, None, mod_dstip_addr, None, mod_l4_dstport)
        sys_logging("creat status = %d" %status)
        status = sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
        sys_logging("remove status = %d" %status)

        warmboot(self.client)
        try:
            nat = sai_thrift_nat_entry_t(vr_id, keylist[0], keylist[1], keylist[2], keylist[3], keylist[4], masklist[0], masklist[1], masklist[2], masklist[3], masklist[4])
            attrs = self.client.sai_thrift_get_nat_attribute(nat)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
        
        finally:
            #sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
            sai_thrift_remove_route(self.client, vr_id, addr_family, mod_dstip_addr, ip_mask, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, mod_dstip_addr, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
        
            self.client.sai_thrift_remove_virtual_router(vr_id)

class SNATPacketTest(sai_base_test.ThriftInterfaceDataPlane):
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
        
        #internal
        attr_value = sai_thrift_attribute_value_t(u8=1)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_NAT_ZONE_ID, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        srcip_addr = '10.10.10.1'
        dstip_addr = '20.20.20.1'
        proto = 6
        l4_srcport = 1000
        #l4_dstport = 2000
        
        ipmask = '255.255.255.255'
        protomask = 0xff
        l4portmask = 0xffff

        dmac1 = '00:11:22:33:44:55'
        
        keylist = [srcip_addr, '', proto, l4_srcport, 0]
        masklist = [ipmask, ipmask, protomask, l4portmask, l4portmask]
        
        ip_addr1_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dstip_addr, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dstip_addr, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        
        mod_srcip_addr = '100.100.100.1'
        #mod_dstip_addr = '200.200.200.1'
        
        mod_l4_srcport = 1001
        
        nat_type = SAI_NAT_TYPE_SOURCE_NAT
        status = sai_thrift_create_nat(self.client, vr_id, nat_type, keylist, masklist, mod_srcip_addr, None, mod_l4_srcport, None)
        sys_logging("creat status = %d" %status)
        #status = sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
        #print "remove status = %d" %status
        
        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='10.10.10.1',
                                ip_id=105,
                                ip_ttl=64,
                                tcp_sport=1000)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='100.100.100.1',
                                ip_id=105,
                                ip_ttl=63,
                                tcp_sport=1001)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            
        
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dstip_addr, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
        
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
class DNATPacketTest(sai_base_test.ThriftInterfaceDataPlane):
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

        #external
        attr_value = sai_thrift_attribute_value_t(u8=0)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_NAT_ZONE_ID, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        #srcip_addr = '10.10.10.1'
        dstip_addr = '20.20.20.1'
        proto = 6
        #l4_srcport = 1000
        l4_dstport = 2000
        
        ipmask = '255.255.255.255'
        protomask = 0xff
        l4portmask = 0xffff

        
        dmac1 = '00:11:22:33:44:55'
        #ip_addr_subnet = '200.200.200.0'
        ip_mask = '255.255.255.255'
        
        #mod_srcip_addr = '100.100.100.1'
        mod_dstip_addr = '200.200.200.1'
        
        mod_l4_dstport = 2001
        
        keylist = ['', dstip_addr, proto, 0, l4_dstport]
        masklist = [ipmask, ipmask, protomask, l4portmask, l4portmask]

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, mod_dstip_addr, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, mod_dstip_addr, rif_id1)
        
        sai_thrift_create_route(self.client, vr_id, addr_family, mod_dstip_addr, ip_mask, nhop1)
        
        nat_type = SAI_NAT_TYPE_DESTINATION_NAT
        
        status = sai_thrift_create_nat(self.client, vr_id, nat_type, keylist, masklist, None, mod_dstip_addr, None, mod_l4_dstport)
        sys_logging("creat status = %d" %status)
        #status = sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
        #print "remove status = %d" %status
        
        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=dstip_addr,
                                ip_src='10.10.10.1',
                                ip_id=105,
                                ip_ttl=64,
                                tcp_dport=2000)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=mod_dstip_addr,
                                ip_src='10.10.10.1',
                                ip_id=105,
                                ip_ttl=63,
                                tcp_dport=2001)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
        
        finally:
            sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
            sai_thrift_remove_route(self.client, vr_id, addr_family, mod_dstip_addr, ip_mask, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, mod_dstip_addr, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
        
            self.client.sai_thrift_remove_virtual_router(vr_id)