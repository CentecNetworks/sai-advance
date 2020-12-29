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
Thrift SAI MPLS tests
"""
import socket
import ptf
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask
stress = 0
debug = 0


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


class fun_01_create_mpls_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        if debug:
            print ptf.config["test_dir"]
            print ptf.config
            print sys.argv
            pdb.set_trace()
        a = testutils.test_params_get()['chipname']
        print a
        label_list = [150]

        label1 = 100
        label2 = 200
        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        
        warmboot(self.client)
        try:
            sys_logging("======Create 3 type basic mpls inseg entry======")
            status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, next_hop1, packet_action)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            
            status = sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, next_hop2, packet_action)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            status = sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id2, packet_action)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS) 
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 

            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging("get inseg entry attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging("get inseg entry attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging("get inseg entry attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_inseg_entry(mpls3) 
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class fun_02_create_l3vpn_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

        label1 = 100
        label2 = 200
        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        warmboot(self.client)
        try:
            sys_logging("======Create a mpls l3vpn inseg entry======")
            status = sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            mpls3 = sai_thrift_inseg_entry_t(label3) 
 
            self.client.sai_thrift_remove_inseg_entry(mpls3)  

            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class fun_03_create_vpls_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

        label1 = 100
        label2 = 200
        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=201)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        
        warmboot(self.client)
        try:
            sys_logging("======Create 2 vpls inseg entry======")
            status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            status = sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id2)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS) 


            
        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class fun_04_create_vpws_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
   
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

       
        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 64]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=201)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)

        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)


        warmboot(self.client)
        try:
            sys_logging("======Create 2 vpws inseg entry======")
            status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            status = sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id2)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS) 
            

        finally:
            sys_logging("======clean up======")

            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)


class fun_05_create_vpws_inseg_entry_binding_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

       
        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 64]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=201)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)

        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list1, next_level_nhop_oid=next_hop)
        next_hop2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id2, label_list2, next_level_nhop_oid=next_hop)

        warmboot(self.client)
        try:
            sys_logging("======Create 2 vpls inseg entry======")
            status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            status = sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id2)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS) 


            sys_logging("======entry1 bind nexthop to port2======")
            tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)
            bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, False)
        
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                        value=bport_attr_xcport_value)
            
            self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
            
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                        value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)
            
            bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                        value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)

            sys_logging("======entry2 bind nexthop to port3======")
            tunnel_bport2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id2, bridge_id=bridge_id, admin_state=False)
            bport2 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan_id, False)
        
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport2)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                        value=bport_attr_xcport_value)
            
            self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr_xcport)
            
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport2)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                        value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport2, bport_attr_xcport)
            
            bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                        value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport2, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr_xcport)
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2, port3)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport2)
        
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class fun_06_create_exist_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

        label1 = 100
        label2 = 200
        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, next_hop1, packet_action)
        warmboot(self.client)
        try:
            sys_logging("======Create exist inseg entry======")
            status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, next_hop1, packet_action)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS)

            
            status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, next_hop2, packet_action)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS)

            status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id2, packet_action)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS) 
            #pdb.set_trace()
        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)

            self.client.sai_thrift_remove_inseg_entry(mpls1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class fun_07_create_max_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        a = testutils.test_params_get()['chipname']
        if a == 'tsingma':
            lable_cnt=8091
        elif a == 'tsingma_mx':
            lable_cnt=32767
        if stress == 0:
            return
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label1 = 10
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======Create 8191(tm) or 32767(tm2) inseg entry(1 exist when init)======")
        for label in range(20,lable_cnt+20):
            sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, rif_id1, packet_action)
        if debug:
            pdb.set_trace()
        warmboot(self.client)
        try:
            sys_logging("======Create another inseg entry======")
            status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id1, packet_action)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_INSUFFICIENT_RESOURCES)

            #pdb.set_trace()
        finally:
            sys_logging("======clean up======")
            for i in range(20,lable_cnt+20):
                mpls = sai_thrift_inseg_entry_t(i)
                self.client.sai_thrift_remove_inseg_entry(mpls)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_08_remove_mpls_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

        label1 = 100
        label2 = 200
        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        
        sys_logging("======Create 3 basic mpls inseg entry======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, next_hop1, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, next_hop2, packet_action)
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id2, packet_action)

        warmboot(self.client)
        try:
            sys_logging("======remove 3 basic mpls inseg entry======")
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            status = self.client.sai_thrift_remove_inseg_entry(mpls1)
            sys_logging("remove inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_inseg_entry(mpls2)
            sys_logging("remove inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_inseg_entry(mpls3)
            sys_logging("remove inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("======get 3 inseg entry attribute======")
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging("status = %d" %attrs.status) 
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls2)
            sys_logging("status = %d" %attrs.status) 
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls3)
            sys_logging("status = %d" %attrs.status) 
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

            
        finally:
            sys_logging("======clean up======") 
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class fun_09_remove_l3vpn_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

        label1 = 100
        label2 = 200
        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======Create mpls l3vpn inseg entry======")
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)

        warmboot(self.client)
        try:
            sys_logging("======remove the mpls l3vpn inseg entry======")
            mpls3 = sai_thrift_inseg_entry_t(label3)
            status = self.client.sai_thrift_remove_inseg_entry(mpls3)
            sys_logging("remove inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls3)
            sys_logging("status = %d" %attrs.status) 
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class fun_10_remove_vpls_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

        label1 = 100
        label2 = 200
        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=201)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        sys_logging("======Create 2 vpls inseg entry======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id2)
        warmboot(self.client)
        try:
            sys_logging("======remove 2 vpls inseg entry======")
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            
            status = self.client.sai_thrift_remove_inseg_entry(mpls1)
            sys_logging("remove inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_inseg_entry(mpls2)  
            sys_logging("remove inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS) 

            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging("status = %d" %attrs.status) 
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls2)
            sys_logging("status = %d" %attrs.status) 
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            #pdb.set_trace()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class fun_11_remove_vpws_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
   
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

       
        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 64]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=201)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)

        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)

        sys_logging("======Create 2 vpws inseg entry======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id2)
        warmboot(self.client)
        try:
            sys_logging("======remove 2 vpws inseg entry======")
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            
            status = self.client.sai_thrift_remove_inseg_entry(mpls1)
            sys_logging("remove inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_inseg_entry(mpls2) 
            sys_logging("remove inseg entry status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS) 

            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging("status = %d" %attrs.status) 
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls2)
            sys_logging("status = %d" %attrs.status) 
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            #pdb.set_trace()

        finally:
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class fun_12_remove_no_exist_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

        label1 = 100
        label2 = 200
        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)

        sys_logging("======Create 3 basic mpls inseg entry and remove all======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, next_hop1, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, next_hop2, packet_action)
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id2, packet_action)

        mpls1 = sai_thrift_inseg_entry_t(label1)
        mpls2 = sai_thrift_inseg_entry_t(label2) 
        mpls3 = sai_thrift_inseg_entry_t(label3) 
        self.client.sai_thrift_remove_inseg_entry(mpls1)
        self.client.sai_thrift_remove_inseg_entry(mpls2)

        warmboot(self.client)
        try:
            sys_logging("======remove no exist mpls inseg entry======")
            status = self.client.sai_thrift_remove_inseg_entry(mpls1)
            sys_logging("remove inseg entry status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            status = self.client.sai_thrift_remove_inseg_entry(mpls2)
            sys_logging("remove inseg entry status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls3)
            sys_logging("status = %d" %attrs.status) 
            assert (attrs.status == SAI_STATUS_SUCCESS)
                      
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_inseg_entry(mpls3) 
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class fun_13_get_inseg_entry_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

        label1 = 100
        label2 = 200
        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======Create a mpls l3vpn inseg entry======")
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)
        mpls1 = sai_thrift_inseg_entry_t(label3) 
        
        warmboot(self.client)
        try:
            sys_logging("======get the inseg entry attribute======")
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_NUM_OF_POP:
                    sys_logging("set pop_nums = %d" %pop_nums)
                    sys_logging("get pop_nums = %d" %a.value.u8)
                    if pop_nums != a.value.u8:
                        raise NotImplementedError()
                if a.id == SAI_INSEG_ENTRY_ATTR_PACKET_ACTION: 
                    sys_logging("set packet_action = %d" %packet_action)
                    sys_logging("get packet_action = %d" %a.value.s32)
                    if packet_action != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID: 
                    sys_logging("set nhop = %d" %rif_id2)
                    sys_logging("get nhop = %d" %a.value.oid)
                    if rif_id2 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_INSEG_ENTRY_ATTR_DECAP_TUNNEL_ID: 
                    sys_logging("set tunnel_id = %d" %tunnel_id)
                    sys_logging("get tunnel_id = %d" %a.value.oid)
                    if tunnel_id != a.value.oid:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_inseg_entry(mpls1)  

            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)


class fun_14_set_inseg_entry_attr_action_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

        label1 = 100
        label2 = 200
        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)

        sys_logging("======Create a inseg entry======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, next_hop1, packet_action)

        sys_logging("======get the inseg entry attribute======")
        mpls1 = sai_thrift_inseg_entry_t(label1)
        attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
        sys_logging("status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_INSEG_ENTRY_ATTR_PACKET_ACTION: 
                print "get packet_action = %d" %a.value.s32

        warmboot(self.client)
        try:
            sys_logging("======set the inseg entry attribute action======")
            packet_action = SAI_PACKET_ACTION_DROP
            attr_value = sai_thrift_attribute_value_t(s32=packet_action)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr) 

            sys_logging("======get the inseg entry attribute again======")
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_PACKET_ACTION: 
                    sys_logging("set packet_action = %d" %packet_action)
                    sys_logging("get packet_action = %d" %a.value.s32)
                    if packet_action != a.value.s32:
                        raise NotImplementedError()

            sys_logging("======set the inseg entry attribute action======")
            packet_action = SAI_PACKET_ACTION_TRAP
            attr_value = sai_thrift_attribute_value_t(s32=packet_action)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr) 

            sys_logging("======get the inseg entry attribute again======")
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_PACKET_ACTION: 
                    sys_logging("set packet_action = %d" %packet_action)
                    sys_logging("get packet_action = %d" %a.value.s32)
                    if packet_action != a.value.s32:
                        raise NotImplementedError()

            sys_logging("======set the inseg entry attribute action======")
            packet_action = SAI_PACKET_ACTION_FORWARD
            attr_value = sai_thrift_attribute_value_t(s32=packet_action)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr) 

            sys_logging("======get the inseg entry attribute again======")
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_PACKET_ACTION: 
                    sys_logging("set packet_action = %d" %packet_action)
                    sys_logging("get packet_action = %d" %a.value.s32)
                    if packet_action != a.value.s32:
                        raise NotImplementedError()
            #pdb.set_trace()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class fun_15_set_inseg_entry_attr_nhop_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

        label1 = 100

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da2, dmac)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_da2, rif_id1)

        sys_logging("======Create a inseg entry======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, next_hop1, packet_action)

        sys_logging("======get the inseg entry attribute======")
        mpls1 = sai_thrift_inseg_entry_t(label1)
        attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
        sys_logging("status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID: 
                sys_logging( "get next_hop oid = 0x%x" %a.value.oid)
        warmboot(self.client)
        try:
            sys_logging("======set the inseg entry attribute nexthop======")
            attr_value = sai_thrift_attribute_value_t(oid=next_hop2)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID, value=attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr) 

            sys_logging("======get the inseg entry attribute again======")
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID: 
                    sys_logging( "set next_hop oid = 0x%x" %next_hop2)
                    sys_logging( "get next_hop oid = 0x%x" %a.value.oid)
                    if next_hop2 != a.value.oid:
                        raise NotImplementedError()

            sys_logging("======set the inseg entry attribute nexthop======")
            attr_value = sai_thrift_attribute_value_t(oid=next_hop1)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID, value=attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr) 

            sys_logging("======get the inseg entry attribute again======")
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID: 
                    sys_logging( "set next_hop oid = 0x%x" %next_hop1)
                    sys_logging( "get next_hop oid = 0x%x" %a.value.oid)
                    if next_hop1 != a.value.oid:
                        raise NotImplementedError()
            #pdb.set_trace()
        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)
 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da2, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_16_set_inseg_entry_attr_rifnhop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label_list = [150]

        label1 = 100
        label2 = 200
        label3 = 300
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        vr_id2 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======Create a inseg entry======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id1, packet_action, tunnel_id=tunnel_id)
        sys_logging("======get the inseg entry attribute======")
        mpls1 = sai_thrift_inseg_entry_t(label1) 
        attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
        sys_logging( "status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID: 
                sys_logging( "get next_hop oid = 0x%x" %a.value.oid)
                
        warmboot(self.client)
        try:
            sys_logging("======set the inseg entry attribute nexthop(rif)======")
            attr_value = sai_thrift_attribute_value_t(oid=rif_id2)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID, value=attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr) 

            sys_logging("======get the inseg entry attribute again======")
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID: 
                    sys_logging( "set next_hop oid = 0x%x" %rif_id2)
                    sys_logging( "get next_hop oid = 0x%x" %a.value.oid)
                    if rif_id2 != a.value.oid:
                        raise NotImplementedError()

            sys_logging("======set the inseg entry attribute nexthop(rif)======")
            attr_value = sai_thrift_attribute_value_t(oid=rif_id1)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID, value=attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr) 
            
            sys_logging("======get the inseg entry attribute again======")
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls1)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID: 
                    sys_logging("set next_hop oid = 0x%x" %rif_id1)
                    sys_logging("get next_hop oid = 0x%x" %a.value.oid)
                    if rif_id1 != a.value.oid:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_inseg_entry(mpls1)  

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class fun_17_create_mpls_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        label = 100
        label_list1 = [(label<<12) | 64]

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)


        warmboot(self.client)
        try:
            sys_logging("======create a mpls nexthop======")
            next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
            sys_logging("create nhop = 0x%x" %next_hop1)
            assert (next_hop1%0x100000000 == 0x2004)
            #pdb.set_trace()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(next_hop1)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vr_id)


class fun_18_create_l3vpn_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label = 150
        label_list1 = [(label<<12) | 64]

        label = 300
        label_list2 = [(label<<12) | 64]

        label = 450
        label_list3 = [(label<<12) | 64]


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        tunnel_id2 = sai_thrift_create_tunnel_mpls(self.client, decap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, decap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create a mpls nexthop======")
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        
        warmboot(self.client)
        try:
            sys_logging("======create 2 mpls l3vpn nexthop======")
            next_hop2 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_level_nhop_oid=next_hop1)
            sys_logging("create nhop = 0x%x" %next_hop2)
            assert (next_hop1%0x100000000 == 0x2004)
            next_hop3 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id2, label_list3, next_level_nhop_oid=next_hop1)
            sys_logging("create nhop = 0x%x" %next_hop3)
            assert (next_hop1%0x100000000 == 0x2004)
            
        finally:
            sys_logging("======clean up======")
            
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)

class fun_19_create_l2vpn_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label = 150
        label_list = [(label<<12) | 64]

        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 64]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=201)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)

        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        #rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        sys_logging("======create a mpls nexthop======")
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)

        warmboot(self.client)
        try:
            sys_logging("======create 2 l2vpn(tunnel encap) nexthop======")
            next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list1, next_level_nhop_oid=next_hop)
            sys_logging("create nhop = 0x%x" %next_hop1)
            assert (next_hop1%0x100000000 == 0x4004)
            next_hop2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id2, label_list2, next_level_nhop_oid=next_hop)
            sys_logging("create nhop = 0x%x" %next_hop2)
            assert (next_hop1%0x100000000 == 0x4004)
            
            
        finally:
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            #self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class fun_20_create_max_mpls_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        label_list_list = []
        nexthop_list = []

        for i in range(100,1123):
            label_list1 = [(i<<12) | 64]
            label_list_list.append(label_list1)
        label = 50
        label_list = [(label<<12) | 64]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create 1023 mpls nexthop======")
        for i in range(0,1023):
            next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list_list[i])
            nexthop_list.append(next_hop)
        warmboot(self.client)
        try:
            next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
            sys_logging("create nhop = 0x%x" %next_hop1)
            assert (next_hop1 == SAI_NULL_OBJECT_ID)
            
        finally:
            sys_logging("======clean up======")
            for i in range(0,1023):
                self.client.sai_thrift_remove_next_hop(nexthop_list[i])

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            

class fun_21_remove_mpls_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label = 150
        label_list1 = [(label<<12) | 64]

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        sys_logging("======create a mpls nextthop======")
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)

        try:
            sys_logging("======get the mpls nexthop attribute======")
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            
            sys_logging("======remove the mpls nexthop======")
            status = self.client.sai_thrift_remove_next_hop(next_hop1)
            sys_logging("status = %d" %status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======get the mpls nexthop attribute again======")
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("======clean up======")
            #self.client.sai_thrift_remove_next_hop(next_hop1)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vr_id)


class fun_22_remove_l3vpn_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label = 150
        label_list1 = [(label<<12) | 64]

        label = 300
        label_list2 = [(label<<12) | 64]

        label = 450
        label_list3 = [(label<<12) | 64]


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        tunnel_id2 = sai_thrift_create_tunnel_mpls(self.client, decap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, decap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        sys_logging("======create a mpls nexthop======")
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        sys_logging("======create a mpls l3vpn nexthop======")
        next_hop2 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_level_nhop_oid=next_hop1)
        
        warmboot(self.client)
        try:
            sys_logging("======get the mpls l3vpn nexthop attribute======")
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop2)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove the mpls l3vpn nexthop======")
            status = self.client.sai_thrift_remove_next_hop(next_hop2)
            sys_logging("status = %d" %status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======get the mpls l3vpn nexthop attribute again======")
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop2)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(next_hop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)

class fun_23_remove_l2vpn_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label = 150
        label_list = [(label<<12) | 64]

        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 64]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=201)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)

        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        #rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        sys_logging("======create a mpls nexthop======")
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        sys_logging("======create a l2vpn(tunnel encap) nexthop======")
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list1, next_level_nhop_oid=next_hop)
        
        warmboot(self.client)
        try:
            sys_logging("======get the l2vpn(tunnel encap) nexthop attribute======")
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======remove the l2vpn(tunnel encap) nexthop======")
            status = self.client.sai_thrift_remove_next_hop(next_hop1)
            sys_logging("status = %d" %status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("======get the l2vpn(tunnel encap) nexthop attribute again======")
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
            
        finally:
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            #self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class fun_24_remove_no_exist_mpls_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label = 150
        label_list1 = [(label<<12) | 64]

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        sys_logging("======create a mpls nexthop and remove it======")
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        self.client.sai_thrift_remove_next_hop(next_hop1)

        warmboot(self.client)
        try:
            sys_logging("======remove the mpls nexthop again======")
            status = self.client.sai_thrift_remove_next_hop(next_hop1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            #pdb.set_trace()
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_25_get_mpls_nexthop_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label = 150
        label_list1 = [(label<<12) | 64]

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        sys_logging("======create a mpls nexthop======")
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)

        try:
            sys_logging("======get the mpls nexthop attribute======")
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_ATTR_TYPE:
                    if SAI_NEXT_HOP_TYPE_MPLS != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_ATTR_LABELSTACK:
                    if label_list1 != a.value.u32list.u32list:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_ATTR_IP:
                    sys_logging("get ip = %s" %a.value.ipaddr.addr.ip4)
                    if ip_da != a.value.ipaddr.addr.ip4:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID:
                    if rif_id1 != a.value.oid:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
 
            self.client.sai_thrift_remove_next_hop(next_hop1)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_26_get_tunnel_encap_nexthop_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label = 150
        label_list = [(label<<12) | 64]

        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 64]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=201)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        print "0x%x" %tunnel_id1
        print "0x%x" %tunnel_id2
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        #rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        sys_logging("======create a mpls nexthop======")
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        sys_logging("======create a l2vpn(tunnel encap) nexthop======")
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list1, next_level_nhop_oid=next_hop)
        
        warmboot(self.client)
        try:
            sys_logging("======get the l2vpn(tunnel encap) nexthop attribute======")
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_ATTR_TYPE:
                    if SAI_NEXT_HOP_TYPE_TUNNEL_ENCAP != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_ATTR_LABELSTACK:
                    print "get label list =",
                    print a.value.u32list.u32list
                    if label_list1 != a.value.u32list.u32list:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_ATTR_NEXT_LEVEL_NEXT_HOP_ID:
                    sys_logging( "get next level nexthop id = 0x%x" %a.value.oid)
                    if next_hop != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_NEXT_HOP_ATTR_TUNNEL_ID:
                    sys_logging( "get tunnel id = 0x%x" %a.value.oid)
                    if tunnel_id1 != a.value.oid:
                        raise NotImplementedError()
            
        finally:
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            #self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class fun_27_set_and_get_mpls_nexthop_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'

        label = 150
        label_list = [(label<<12) | 64]

        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 64]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        type = SAI_COUNTER_TYPE_REGULAR
        counter_id1 = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = 0x%x" %counter_id1)
        
        counter_id2 = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = 0x%x" %counter_id2)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=201)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        #rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        sys_logging("======create a mpls nexthop======")
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list, counter_oid=counter_id1)
        sys_logging("======create a l2vpn(tunnel encap) nexthop======")
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list1, next_level_nhop_oid=next_hop, counter_oid=counter_id2)
   
        warmboot(self.client)
        try:
            sys_logging("======get the mpls nexthop attribute======")
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_ATTR_COUNTER_ID:
                    if counter_id1 != a.value.oid:
                        raise NotImplementedError()

            sys_logging("======get the l2vpn(tunnel encap) nexthop attribute======")
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_ATTR_COUNTER_ID:
                    if counter_id2 != a.value.oid:
                        raise NotImplementedError()

           #attr_value = sai_thrift_attribute_value_t(oid=counter_id1)
           #attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_COUNTER_ID, value=attr_value)
           #self.client.sai_thrift_set_route_attribute(next_hop, attr)
           #attr_value = sai_thrift_attribute_value_t(oid=counter_id2)
           #attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_COUNTER_ID, value=attr_value)
           #self.client.sai_thrift_set_route_attribute(next_hop1, attr)
           
           #attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop)
           #sys_logging("status = %d" %attrs.status)
           #assert (attrs.status == SAI_STATUS_SUCCESS)
           #for a in attrs.attr_list:
           #    if a.id == SAI_NEXT_HOP_ATTR_COUNTER_ID:
           #        print a.value.oid
           #        if counter_id1 != a.value.oid:
           #            raise NotImplementedError()
           #attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop1)
           #sys_logging("status = %d" %attrs.status)
           #assert (attrs.status == SAI_STATUS_SUCCESS)
           #for a in attrs.attr_list:
           #    if a.id == SAI_NEXT_HOP_ATTR_COUNTER_ID:
           #        if counter_id2 != a.value.oid:
           #            raise NotImplementedError()

        finally:
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            #self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            sai_thrift_remove_counter(self.client, counter_id2)
            sai_thrift_remove_counter(self.client, counter_id1)

class fun_28_create_es_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        label1 = 100
        label2 = 200
        sys_logging("======create 2 es======")
        es_oid1 = sai_thrift_create_es(self.client, label1)
        es_oid2 = sai_thrift_create_es(self.client, label2)

        warmboot(self.client)
        try:
            
            sys_logging("create es oid = 0x%x" %es_oid1)
            assert (es_oid1%0x100000000 == SAI_OBJECT_TYPE_ES)
           
            sys_logging("create es oid = 0x%x" %es_oid2)
            assert (es_oid2%0x100000000 == SAI_OBJECT_TYPE_ES)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_es(es_oid1)
            self.client.sai_thrift_remove_es(es_oid2)

class fun_29_create_exist_es_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        label1 = 100
        label2 = 200
        sys_logging("======create a es======")
        es_oid1 = sai_thrift_create_es(self.client, label1)

        sys_logging("======create a same es======")
        es_oid2 = sai_thrift_create_es(self.client, label1)

        try:
           
            sys_logging("======create es oid = 0x%x======" %es_oid2)
            assert (es_oid2 == SAI_NULL_OBJECT_ID)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_es(es_oid1)

class fun_30_create_same_label_es_and_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        label1 = 100
        label2 = 200
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create a es======")
        es_oid1 = sai_thrift_create_es(self.client, label1)
        sys_logging("======create a mpls inseg entry======")   
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id1, packet_action)

        warmboot(self.client)
        try:
            sys_logging("======create a mpls inseg entry which has same label to es ======")
            status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id1, packet_action)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_ITEM_ALREADY_EXISTS)

            sys_logging("======create a es which has same label to mpls inseg entry ======")
            es_oid2 = sai_thrift_create_es(self.client, label2)
            sys_logging("create es oid = 0x%x" %es_oid2)
            assert (es_oid2 == SAI_NULL_OBJECT_ID)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_es(es_oid1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class fun_31_remove_es_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        label1 = 100
        label2 = 200
        sys_logging("======create a es======")
        es_oid1 = sai_thrift_create_es(self.client, label1)

        sys_logging("======get the es attribute======")
        attrs = self.client.sai_thrift_get_es_attribute(es_oid1)
        sys_logging("status = %d" %attrs.status)

        try:
            sys_logging("======remove the es======")
            status = self.client.sai_thrift_remove_es(es_oid1)
            sys_logging("remove es status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("======get the es attribute again======")
            attrs = self.client.sai_thrift_get_es_attribute(es_oid1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("clean up")

class fun_32_remove_no_exist_es_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        label1 = 100
        label2 = 200
        sys_logging("======create a es and remove it======")
        es_oid1 = sai_thrift_create_es(self.client, label1)
        self.client.sai_thrift_remove_es(es_oid1)

        warmboot(self.client)
        try:
            sys_logging("======remove the no exist es======")
            status = self.client.sai_thrift_remove_es(es_oid1)
            sys_logging("remove es status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("clean up")
            
class fun_33_remove_same_label_es_and_inseg_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        label1 = 100
        label2 = 200
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create a es======")
        es_oid1 = sai_thrift_create_es(self.client, label1)

        warmboot(self.client)
        try:
            sys_logging("======remove the mpls inseg entry which has same label to es ======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            status = self.client.sai_thrift_remove_inseg_entry(mpls1)
            sys_logging("remove inseg entry status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)

            sys_logging("======remove the es======")
            status = self.client.sai_thrift_remove_es(es_oid1)
            sys_logging("remove es oid status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class fun_34_get_es_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        label1 = 100
        label2 = 200
        sys_logging("======create 2 es======")
        es_oid1 = sai_thrift_create_es(self.client, label1)
        es_oid2 = sai_thrift_create_es(self.client, label2)

        warmboot(self.client)
        try:
            sys_logging("======get es1 attribute======")
            attrs = self.client.sai_thrift_get_es_attribute(es_oid1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ES_ATTR_ESI_LABEL:
                    sys_logging("get esi label = %d" %label1)
                    if label1 != a.value.u32:
                        raise NotImplementedError()

            sys_logging("======get es2 attribute======")
            attrs = self.client.sai_thrift_get_es_attribute(es_oid2)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ES_ATTR_ESI_LABEL:
                    sys_logging("get esi label = %d" %label2)
                    if label2 != a.value.u32:
                        raise NotImplementedError()            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_es(es_oid1)
            self.client.sai_thrift_remove_es(es_oid2)

class fun_35_create_mpls_tunnel_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls(self.client) 
        tunnel_id2 = sai_thrift_create_tunnel_mpls(self.client,decap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_val=50, decap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_val=3)

        warmboot(self.client)
        try:
            sys_logging("create mpls tunnel = 0x%x" %tunnel_id1)
            assert (tunnel_id1%0x100000000 == 0x2a) #SAI_OBJECT_TYPE_TUNNEL
           
            sys_logging("create mpls tunnel = 0x%x" %tunnel_id2)
            assert (tunnel_id2%0x100000000 == 0x2a) #SAI_OBJECT_TYPE_TUNNEL
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)

class fun_36_create_mpls_l2_tunnel_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        tunnel_id2= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        warmboot(self.client)
        try:
            sys_logging("create mpls l2 tunnel = 0x%x" %tunnel_id1)
            assert (tunnel_id1%0x100000000 == 0x2a) #SAI_OBJECT_TYPE_TUNNEL
           
            sys_logging("create mpls l2 tunnel = 0x%x" %tunnel_id2)
            assert (tunnel_id2%0x100000000 == 0x2a) #SAI_OBJECT_TYPE_TUNNEL
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)

class fun_37_create_same_mpls_tunnel_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls(self.client) 
        tunnel_id2 = sai_thrift_create_tunnel_mpls(self.client)

        warmboot(self.client)
        try:
            sys_logging("create mpls tunnel = 0x%x" %tunnel_id1)
            assert (tunnel_id1%0x100000000 == 0x2a) #SAI_OBJECT_TYPE_TUNNEL
           
            sys_logging("create mpls tunnel = 0x%x" %tunnel_id2)
            assert (tunnel_id2%0x100000000 == 0x2a) #SAI_OBJECT_TYPE_TUNNEL
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)

class fun_38_remove_mpls_tunnel_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls(self.client) 
        
        ids_list = [SAI_TUNNEL_ATTR_DECAP_TTL_MODE,SAI_TUNNEL_ATTR_ENCAP_TTL_MODE,SAI_TUNNEL_ATTR_ENCAP_TTL_VAL,SAI_TUNNEL_ATTR_DECAP_EXP_MODE,SAI_TUNNEL_ATTR_ENCAP_EXP_MODE,SAI_TUNNEL_ATTR_ENCAP_EXP_VAL]
        attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
        sys_logging("get tunnel attribute status = %d" %attrs.status)

        
        warmboot(self.client)
        try:
            status = self.client.sai_thrift_remove_tunnel(tunnel_id1)
            sys_logging("remove tunnel status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_INVALID_OBJECT_ID)
        finally:
            sys_logging("======clean up======")
            
class fun_39_remove_mpls_l2_tunnel_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)

        ids_list = [SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE,SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW,SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE,SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW,\
        SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN,SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID,SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID,SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID]
        attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
        sys_logging("get tunnel attribute status = %d" %attrs.status)
        
        warmboot(self.client)
        try:
            status = self.client.sai_thrift_remove_tunnel(tunnel_id1)
            sys_logging("remove tunnel status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_INVALID_OBJECT_ID)
        finally:
            sys_logging("======clean up======")

class fun_40_remove_no_exist_mpls_tunnel_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls(self.client) 

        self.client.sai_thrift_remove_tunnel(tunnel_id1)
        
        warmboot(self.client)
        try:
            status = self.client.sai_thrift_remove_tunnel(tunnel_id1)
            sys_logging("remove tunnel status = %d" %status)
            assert (status == SAI_STATUS_INVALID_OBJECT_ID)

        finally:
            sys_logging("======clean up======")

class fun_41_get_mpls_tunnel_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls(self.client,decap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_val=50, decap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_val=3)
        
        ids_list = [SAI_TUNNEL_ATTR_DECAP_TTL_MODE,SAI_TUNNEL_ATTR_ENCAP_TTL_MODE,SAI_TUNNEL_ATTR_ENCAP_TTL_VAL,SAI_TUNNEL_ATTR_DECAP_EXP_MODE,SAI_TUNNEL_ATTR_ENCAP_EXP_MODE,SAI_TUNNEL_ATTR_ENCAP_EXP_VAL,SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID]
        attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
        sys_logging("get tunnel attribute status = %d" %attrs.status)
        
        warmboot(self.client)
        try:
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_TTL_MODE:
                    u8 = ctypes.c_uint8(attribute.value.u8)
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_TTL_MODE = %d ###"  % u8.value)
                    assert ( SAI_TUNNEL_TTL_MODE_PIPE_MODEL == u8.value )
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_TTL_MODE:
                    u8 = ctypes.c_uint8(attribute.value.u8)
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_TTL_MODE = %d ###"  % u8.value)
                    assert ( SAI_TUNNEL_TTL_MODE_PIPE_MODEL == u8.value )
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_TTL_VAL:
                    u8 = ctypes.c_uint8(attribute.value.u8)
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_TTL_VAL = %d ###"  % u8.value)
                    assert ( 50 == u8.value )
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_EXP_MODE:
                    u8 = ctypes.c_uint8(attribute.value.u8)
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_EXP_MODE = %d ###"  % u8.value)
                    assert ( SAI_TUNNEL_EXP_MODE_PIPE_MODEL == u8.value )
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_EXP_MODE:
                    u8 = ctypes.c_uint8(attribute.value.u8)
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_EXP_MODE = %d ###"  % u8.value)
                    assert ( SAI_TUNNEL_EXP_MODE_PIPE_MODEL == u8.value )
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_EXP_VAL:
                    u8 = ctypes.c_uint8(attribute.value.u8)
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_EXP_VAL = %d ###"  % u8.value)
                    assert ( 3 == u8.value )
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID = %x ###"  %attribute.value.oid)
                    assert ( 0 == attribute.value.oid )
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_tunnel(tunnel_id1)

class fun_42_get_mpls_l2_tunnel_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)

        ids_list = [SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE,SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW,SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE,SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW,\
        SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN,SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID,SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID,SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID]
        attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
        sys_logging("get tunnel attribute status = %d" %attrs.status)
        
        warmboot(self.client)
        try:
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN:
                    u16 = ctypes.c_uint16(attribute.value.u16)
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN = %d ###"  % u16.value)
                    assert ( 30 == u16.value )
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE:
                    u8 = ctypes.c_uint8(attribute.value.u8)
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE = %d ###"  % u8.value)
                    assert ( SAI_TUNNEL_MPLS_PW_MODE_TAGGED == u8.value )
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE:
                    u8 = ctypes.c_uint8(attribute.value.u8)
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE = %d ###"  % u8.value)
                    assert ( SAI_TUNNEL_MPLS_PW_MODE_TAGGED == u8.value )
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW:
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW = %d ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW = %g ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID:
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID = %g ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID = %g ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID = %x ###"  %attribute.value.oid)
                    assert ( 0 == attribute.value.oid )
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_tunnel(tunnel_id1)

class fun_43_get_mpls_tunnel_attr_nexthop_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls(self.client,decap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_val=50, decap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_val=3)
        
        ids_list = [SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID]
        attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
        sys_logging("get tunnel attribute status = %d" %attrs.status)
        attr_list = attrs.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID:
                sys_logging("### SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID = %x ###"  %attribute.value.oid)

        port1 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        dmac = '00:55:55:55:55:55'

        label1 = 100
        label2 = 200

        label_list = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        next_hop1 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop2)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_NEXTHOP_ID = %x ###"  %attribute.value.oid)
                    assert ( next_hop1 == attribute.value.oid )
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)

class fun_44_set_mpls_l2_tunnel_attribute_decap_with_cw_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)

        ids_list = [SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW]
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW:
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW = %d ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
                    
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW:
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW = %d ###"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )
                    
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW:
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW = %d ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_tunnel(tunnel_id1)

class fun_45_set_mpls_l2_tunnel_attribute_encap_with_cw_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)

        ids_list = [SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW]
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW = %d ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
                    
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW:
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW = %d ###"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )
                    
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW:
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW = %d ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_tunnel(tunnel_id1)

class fun_46_set_mpls_l2_tunnel_attribute_tagged_vlan_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        vlan_id1 = 30
        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=vlan_id1)

        ids_list = [SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN]
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN = %d ###"  %attribute.value.u16)
                    assert ( vlan_id1 == attribute.value.u16 )

            vlan_id2 = 50        
            attr_value = sai_thrift_attribute_value_t(u16=vlan_id2)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN = %d ###"  %attribute.value.u16)
                    assert ( vlan_id2 == attribute.value.u16 )
                    
            attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN = %d ###"  %attribute.value.u16)
                    assert ( vlan_id1 == attribute.value.u16 )
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_tunnel(tunnel_id1)

class fun_47_set_mpls_l2_tunnel_attribute_decap_esi_valid_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)

        ids_list = [SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID]
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID:
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID = %d ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
                    
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID:
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID = %d ###"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )
                    
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID:
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID = %d ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_tunnel(tunnel_id1)

class fun_48_set_mpls_l2_tunnel_attribute_encap_esi_valid_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)

        ids_list = [SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID]
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID = %d ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
                    
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID = %d ###"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )
                    
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID:
                    sys_logging("### SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID = %d ###"  %attribute.value.booldata)
                    assert ( False == attribute.value.booldata )
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_tunnel(tunnel_id1)


class scenario_01_basic_mpls_ac_to_pw_test(sai_base_test.ThriftInterfaceDataPlane):
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

        label_list = [(label1<<12) | 32]
        #label_list = []
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list, outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_UNIFORM)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
        #pdb.set_trace()
        

        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls1 = [{'label':100,'tc':0,'ttl':63,'s':1}]   
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

        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

        finally:
            sys_logging("======clean up======")

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
            
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_02_basic_mpls_pw_to_ac_test(sai_base_test.ThriftInterfaceDataPlane):
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

        label_list = [(label1<<12) | 64]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_da2, rif_id2)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id3, packet_action ,pop_ttl_mode = SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE)


        mpls2 = [{'label':200,'tc':0,'ttl':100,'s':1}]   
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
                                
        pkt4 = simple_tcp_packet(eth_dst=dmac2,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=62)
        warmboot(self.client)
        try:

            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])
        finally:
            sys_logging("======clean up======")
            mpls2 = sai_thrift_inseg_entry_t(label2) 

            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)
            
            self.client.sai_thrift_remove_next_hop(next_hop3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_03_basic_mpls_swap_test(sai_base_test.ThriftInterfaceDataPlane):
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

        label_list = [(label1<<12) | 60]
        pop_nums = 0
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list, outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_UNIFORM, outseg_type = SAI_OUTSEG_TYPE_SWAP)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, next_hop2, packet_action)
        #pdb.set_trace()
        
        mpls1 = [{'label':200,'tc':0,'ttl':32,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=64,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:33',
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
                               
        mpls2 = [{'label':100,'tc':0,'ttl':31,'s':1}]
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=64,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2) 

        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

        finally:
            sys_logging("======clean up======")
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_04_basic_mpls_php_test(sai_base_test.ThriftInterfaceDataPlane):
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

        label_list = [(label1<<12) | 64]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, [], outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_PIPE, outseg_type = SAI_OUTSEG_TYPE_PHP)

        #sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, next_hop3, packet_action ,pop_ttl_mode = SAI_INSEG_ENTRY_POP_TTL_MODE_PIPE)
        
        mpls2 = [{'label':200,'tc':0,'ttl':100,'s':1}]   
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
                                
        pkt4 = simple_tcp_packet(eth_dst=dmac2,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=63)
        warmboot(self.client)
        try:

            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])
        finally:
            sys_logging("======clean up======")
            mpls2 = sai_thrift_inseg_entry_t(label2) 

            self.client.sai_thrift_remove_inseg_entry(mpls2)

            #sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)
            
            self.client.sai_thrift_remove_next_hop(next_hop3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_05_mpls_l3vpn_ac_to_pw_test(sai_base_test.ThriftInterfaceDataPlane):
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

        label_list = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        next_hop1 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_level_nhop_oid=next_hop2)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop1)


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

        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class scenario_06_l3vpn_ac_to_pw_pipe_mode_test(sai_base_test.ThriftInterfaceDataPlane):
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

        label_list = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 5<<9 | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        #tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client,decap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_val=32, decap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_val=3)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        next_hop1 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_level_nhop_oid=next_hop2)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop1)


        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_dscp=1,
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls1 = [{'label':100,'tc':0,'ttl':32,'s':0}, {'label':200,'tc':3,'ttl':32,'s':1}]
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_dscp=1,
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

        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class scenario_07_mpls_l3vpn_ac_to_pw_per_vrf_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id1 = 10
        vlan_id2 = 20
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

        label_list = [(label1<<12) | 32]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        vr_id2 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        vr_id3 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id3, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id1)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id=vlan_id2)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        next_hop2 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_level_nhop_oid=next_hop1)
        next_hop3 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list3, next_level_nhop_oid=next_hop1)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
        sai_thrift_create_route(self.client, vr_id2, addr_family, ip_addr1_subnet, ip_mask, next_hop3)


        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               dl_vlan_enable=True,
                               vlan_vid=vlan_id1,
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_dscp=0,
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls1 = [{'label':100,'tc':0,'ttl':32,'s':0}, {'label':200,'tc':0,'ttl':63,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=82,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_dscp=0,
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

        pkt3 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               dl_vlan_enable=True,
                               vlan_vid=vlan_id2,
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_dscp=0,
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls2 = [{'label':100,'tc':0,'ttl':32,'s':0}, {'label':300,'tc':0,'ttl':63,'s':1}]   
        ip_only_pkt2 = simple_ip_only_packet(pktlen=82,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_dscp=0,
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt4 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2) 

        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packets( pkt4, [1])

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
            sai_thrift_remove_route(self.client, vr_id2, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id3)
            self.client.sai_thrift_remove_tunnel(tunnel_id)


class scenario_08_mpls_l3vpn_pw_to_ac_test(sai_base_test.ThriftInterfaceDataPlane):
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

        label_list = [(label1<<12) | 64]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        vr_id2 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_da2, rif_id2)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        #pdb.set_trace()

        mpls2 = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]   
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
                                
        pkt4 = simple_tcp_packet(eth_dst=dmac2,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=99)
        warmboot(self.client)
        try:

            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])
        finally:
            sys_logging("======clean up======")
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_inseg_entry(mpls3)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)
            
            self.client.sai_thrift_remove_next_hop(next_hop3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class scenario_09_l3vpn_pw_to_ac_pipe_mode_test(sai_base_test.ThriftInterfaceDataPlane):
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

        label_list = [(label1<<12) | 64]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client, decap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, decap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        vr_id2 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_da2, rif_id2)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        #pdb.set_trace()

        mpls2 = [{'label':200,'tc':0,'ttl':100,'s':0}, {'label':300,'tc':5,'ttl':100,'s':1}]   
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
                                
        pkt4 = simple_tcp_packet(eth_dst=dmac2,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=63)
        warmboot(self.client)
        try:

            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])
        finally:
            sys_logging("======clean up======")
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_inseg_entry(mpls3)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)
            
            self.client.sai_thrift_remove_next_hop(next_hop3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class scenario_10_mpls_l3vpn_pw_to_ac_per_vrf_test(sai_base_test.ThriftInterfaceDataPlane):
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

        label_list = [(label1<<12) | 64]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        vr_id2 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        vr_id3 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id2, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id3, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_da2, rif_id2)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        next_hop4 = sai_thrift_create_nhop(self.client, addr_family, ip_da3, rif_id3)

        sai_thrift_create_route(self.client, vr_id2, addr_family, ip_addr2_subnet, ip_mask, next_hop3)
        sai_thrift_create_route(self.client, vr_id3, addr_family, ip_addr2_subnet, ip_mask, next_hop4)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action)

        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id5, packet_action, tunnel_id=tunnel_id)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id6, packet_action, tunnel_id=tunnel_id)
        #pdb.set_trace()
        
        mpls1 = [{'label':200,'tc':0,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':100,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr2_subnet,
                                ip_ttl=64,
                                ip_id=105,
                                ip_ihl=5
                                )
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:22',
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1)
                                
        pkt2 = simple_tcp_packet(eth_dst=dmac2,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=99)


        mpls2 = [{'label':200,'tc':0,'ttl':100,'s':0}, {'label':100,'tc':3,'ttl':100,'s':1}]   
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
                                
        pkt4 = simple_tcp_packet(eth_dst=dmac3,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=99)
        warmboot(self.client)
        try:
        
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( pkt2, [2])

            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [3])
        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_inseg_entry(mpls3)

            sai_thrift_remove_route(self.client, vr_id2, addr_family, ip_addr2_subnet, ip_mask, next_hop3)
            sai_thrift_remove_route(self.client, vr_id3, addr_family, ip_addr2_subnet, ip_mask, next_hop4)
            
            self.client.sai_thrift_remove_next_hop(next_hop3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            self.client.sai_thrift_remove_next_hop(next_hop4)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_router_interface(rif_id6)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_virtual_router(vr_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id3)
            self.client.sai_thrift_remove_tunnel(tunnel_id)


class scenario_11_mpls_l3vpn_swap_test(sai_base_test.ThriftInterfaceDataPlane):
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

        label_list = [(label1<<12) | 32]
        pop_nums = 0
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, next_hop2, packet_action)
        
        mpls1 = [{'label':200,'tc':0,'ttl':32,'s':0}, {'label':300,'tc':0,'ttl':64,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=64,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:11:11:11:33',
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
                               
        mpls2 = [{'label':100,'tc':0,'ttl':32,'s':0}, {'label':300,'tc':0,'ttl':31,'s':1}]
        #sai bug,actually outer label ttl should be 31 ,inner label and ip ttl should not change
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=64,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2) 

        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

        finally:
            sys_logging("======clean up======")
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_12_vpls_tagged_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[10]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #pdb.set_trace()
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)
        #pdb.set_trace()
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
            self.ctc_send_packet( 10, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [10])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_13_vpls_raw_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_outer=20,
                                dl_vlan_pcp_outer=0,
                                dl_vlan_cfi_outer=1,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)

        pkt4 = simple_qinq_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_outer=20,
                                dl_vlan_pcp_outer=0,
                                dl_vlan_cfi_outer=1,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_ttl=64,
                                ip_ihl=5)
        #pdb.set_trace()
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_14_vpws_tagged_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        
        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

        
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)
        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, False)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_value)

        #pdb.set_trace()
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

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
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
 
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
        
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_15_vpws_raw_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        
        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

        
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)
        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, False)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_value)

        #pdb.set_trace()
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        

        
        pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_outer=20,
                                dl_vlan_pcp_outer=0,
                                dl_vlan_cfi_outer=1,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)

        pkt4 = simple_qinq_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_outer=20,
                                dl_vlan_pcp_outer=0,
                                dl_vlan_cfi_outer=1,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
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
 
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
        
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_16_mpls_sr_ac_to_pw_test(sai_base_test.ThriftInterfaceDataPlane):
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
        label4 = 400
        label5 = 500
        label6 = 150
        label7 = 250
        label8 = 350
        label9 = 450
        label10 = 550

        label_list = [(label1<<12) | 32, (label2<<12) | 32, (label3<<12) | 32, (label4<<12) | 32, (label5<<12) | 32, (label6<<12) | 32,\
        (label7<<12) | 32, (label8<<12) | 32, (label9<<12) | 32, (label10<<12) | 32]

        label0 = 50
        label_list2 = [(label0<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client,decap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_val=50, decap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_mode=SAI_TUNNEL_EXP_MODE_PIPE_MODEL, encap_exp_val=3)
        #tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list, outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_PIPE, outseg_exp_mode= SAI_OUTSEG_EXP_MODE_PIPE, outseg_type=SAI_OUTSEG_TYPE_SWAP)
        next_hop2 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_level_nhop_oid=next_hop1)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
        if debug:
            pdb.set_trace()
        
        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_tos=0,
                               ip_id=105,
                               ip_ttl=20)
                               
        mpls1 = [{'label':label10,'tc':0,'ttl':32,'s':0}, {'label':label9,'tc':0,'ttl':32,'s':0} ,{'label':label8,'tc':0,'ttl':32,'s':0},\
        {'label':label7,'tc':0,'ttl':32,'s':0}, {'label':label6,'tc':0,'ttl':32,'s':0} ,{'label':label5,'tc':0,'ttl':32,'s':0}, {'label':label4,'tc':0,'ttl':32,'s':0},\
        {'label':label3,'tc':0,'ttl':32,'s':0} ,{'label':label2,'tc':0,'ttl':32,'s':0}, {'label':label1,'tc':0,'ttl':32,'s':0}, {'label':label0,'tc':3,'ttl':60,'s':1}]   
        #some problem need test again later
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_tos=0,
                                ip_ttl=19,
                                ip_id=105,
                                ip_ihl=5)
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 

        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

        finally:
            sys_logging("======clean up======")
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)

            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class scenario_17_mpls_sr_transmit_test(sai_base_test.ThriftInterfaceDataPlane):
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

        label_list = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 64]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2, outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_UNIFORM, outseg_type = SAI_OUTSEG_TYPE_SWAP)


        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, next_hop2, packet_action)
        #pdb.set_trace()

        mpls1 = [{'label':100,'tc':3,'ttl':32,'s':0}, {'label':200,'tc':0,'ttl':96,'s':0}, {'label':300,'tc':0,'ttl':100,'s':1}]  
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
                                
        mpls2 = [{'label':200,'tc':0,'ttl':31,'s':0}, {'label':300,'tc':0,'ttl':100,'s':1}]   
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
        pkt4 = simple_tcp_packet(eth_dst=dmac2,
                               eth_src=router_mac,
                               ip_dst=ip_addr2_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=99)

        warmboot(self.client)
        try:
            

            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( pkt2, [2])
        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 

            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

class scenario_18_evpn_ac_to_pw_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 16]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=40)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id2)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        next_hop2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id2, label_list3, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id2) 

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        bport2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id2)
        tunnel_bport2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id2, bridge_id=bridge_id2)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        sai_thrift_create_fdb_bport(self.client, bridge_id2, mac1, bport2, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id2, mac2, tunnel_bport2, mac_action)

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

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        pkt3 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt2 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=40,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack2 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':16,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt4 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack2,
                                inner_frame = mpls_inner_pkt2)


        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packets( pkt4, [1])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id2, mac1, bport2)
            sai_thrift_delete_fdb(self.client, bridge_id2, mac2, tunnel_bport2)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport2)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 
            self.client.sai_thrift_remove_inseg_entry(mpls3)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id2)

class scenario_19_evpn_pw_to_ac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 16]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=40)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id2)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        next_hop2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id2, label_list3, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id2) 

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        bport2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id2)
        tunnel_bport2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id2, bridge_id=bridge_id2)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        sai_thrift_create_fdb_bport(self.client, bridge_id2, mac1, bport2, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id2, mac2, tunnel_bport2, mac_action)

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

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        pkt2 = simple_tcp_packet(pktlen=96,
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


        mpls_inner_pkt2 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=40,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack2 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':16,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack2,
                                inner_frame = mpls_inner_pkt2)
        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #bridge1 pw to ac
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( pkt2, [2])

            #bridge2 pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id2, mac1, bport2)
            sai_thrift_delete_fdb(self.client, bridge_id2, mac2, tunnel_bport2)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport2)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 
            self.client.sai_thrift_remove_inseg_entry(mpls3)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id2)

class scenario_20_evpn_learning_fdb_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 16]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=40)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id2)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        next_hop2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id2, label_list3, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id2) 

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        bport1 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, learn_mode = SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE)

        bport2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id2)
        tunnel_bport2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id2, bridge_id=bridge_id2)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        #sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        #sai_thrift_create_fdb_bport(self.client, bridge_id2, mac1, bport2, mac_action)
        #sai_thrift_create_fdb_bport(self.client, bridge_id2, mac2, tunnel_bport2, mac_action)

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

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
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

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
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
            #bridge1 ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])
            self.ctc_verify_packets( pkt1, [3])
            #self.ctc_verify_each_packet_on_each_port( [pkt2, pkt1], [1, 3])
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id, mac1)
            assert( 1 == status)

            #bridge1 pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id, mac2)
            #pdb.set_trace()
            #assert( 1 == status)
            assert( 0 == status)   #bug110766,should support mpls fdb learning disable 
            #bridge1 ac to pw again
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            #self.ctc_verify_no_packet( pkt1, 3)
            self.ctc_verify_packets( pkt1, [3])    #bug110766,should support mpls fdb learning disable 

            
        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            #sai_thrift_delete_fdb(self.client, bridge_id2, mac1, bport2)
            #sai_thrift_delete_fdb(self.client, bridge_id2, mac2, tunnel_bport2)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2, port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport1, port3)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport2)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 
            self.client.sai_thrift_remove_inseg_entry(mpls3)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id2)

class scenario_21_evpn_unicast_add_es_label_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        dmac2 = '00:55:55:55:55:55'
        dmac = '00:55:55:55:55:66'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'
        mac3 = '00:00:00:03:03:03'


        label1 = 100
        label2 = 200
        label3 = 300
        label4 = 400


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 16]
        label_list4 = [(label4<<12) | 64]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_ttl_val=0, encap_tagged_vlan=30, decap_esi_label_valid=True, encap_esi_label_valid=True)
        tunnel_id2= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=40)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id2)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id5, ip_da2, dmac2)
        next_hop0 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id5, label_list4)
        
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        next_hop2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id2, label_list3, next_level_nhop_oid=next_hop0)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id2) 

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        bport2 = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        tunnel_bport2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id2, bridge_id=bridge_id)

        esi_label=10001
        es_oid = sai_thrift_create_es(self.client, esi_label)

        attr_value = sai_thrift_attribute_value_t(oid=es_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        sai_thrift_create_fdb_bport(self.client, bridge_id, mac3, tunnel_bport2, mac_action)

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

        pkt3 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac3,
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


        mpls_inner_pkt2 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac3,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=40,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack2 = [{'label':label4,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':16,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt4 = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack2,
                                inner_frame = mpls_inner_pkt2)

        warmboot(self.client)
        try:

            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packets( pkt4, [3])

            

        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_es(es_oid)
        
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2, port4)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport2)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 
            self.client.sai_thrift_remove_inseg_entry(mpls3)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop0)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id5, ip_da2, dmac2)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id2)


class scenario_22_evpn_bum_add_es_label_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        dmac2 = '00:55:55:55:55:55'
        dmac = '00:55:55:55:55:66'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'
        mac3 = '00:00:00:03:03:03'


        label1 = 100
        label2 = 200
        label3 = 300
        label4 = 400


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 16]
        label_list4 = [(label4<<12) | 64]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED,decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30, decap_esi_label_valid=True, encap_esi_label_valid=True)
        tunnel_id2= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=40)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id2)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id5, ip_da2, dmac2)
        next_hop0 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id5, label_list4)
        
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        next_hop2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id2, label_list3, next_level_nhop_oid=next_hop0)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id2) 

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        bport2 = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        tunnel_bport2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id2, bridge_id=bridge_id)

        esi_label=10001
        es_oid = sai_thrift_create_es(self.client, esi_label)

        attr_value = sai_thrift_attribute_value_t(oid=es_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

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

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':0},{'label':10001,'tc':0,'ttl':32,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt2 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=40,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack2 = [{'label':label4,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':16,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt3 = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack2,
                                inner_frame = mpls_inner_pkt2)


        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [pkt1, pkt2, pkt3], [4, 1,3])
            #self.ctc_verify_packets( pkt1, [4])
            #self.ctc_verify_packets( pkt2, [1])
            #self.ctc_verify_packets( pkt3, [3])
            

        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_es(es_oid)
        
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2, port4)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport2)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 
            self.client.sai_thrift_remove_inseg_entry(mpls3)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop0)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id5, ip_da2, dmac2)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id2)

class scenario_23_evpn_pw_to_ac_bum_with_es_label_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[0]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        dmac2 = '00:55:55:55:55:55'
        dmac = '00:55:55:55:55:66'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'
        mac3 = '00:00:00:03:03:03'


        label1 = 100
        label2 = 200
        label3 = 300
        label4 = 400


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 16]
        label_list4 = [(label4<<12) | 64]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_ttl_val=0, encap_tagged_vlan=30, decap_esi_label_valid=True, encap_esi_label_valid=True)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id2)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)


        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        bport2 = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        esi_label=10001
        es_oid = sai_thrift_create_es(self.client, esi_label)

        attr_value = sai_thrift_attribute_value_t(oid=es_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

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

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':0},{'label':10001,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


        #pdb.set_trace()
        warmboot(self.client)
        try:

            self.ctc_send_packet( 1, str(pkt2))
            #self.ctc_verify_each_packet_on_each_port( [pkt3, pkt2], [1, 1])
            self.ctc_verify_packets( pkt1, [0])
            self.ctc_verify_no_packet( pkt1, 2)
            

        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_es(es_oid)
        
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2, port4)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)

            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 

            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 


            self.client.sai_thrift_remove_next_hop(next_hop1)

            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id2)


class scenario_24_one_port_two_ac_and_delete_one_ac_to_pw_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 16]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=40)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id2)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        next_hop2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id2, label_list3, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id2) 

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        bport2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id2)
        tunnel_bport2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id2, bridge_id=bridge_id2)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        sai_thrift_create_fdb_bport(self.client, bridge_id2, mac1, bport2, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id2, mac2, tunnel_bport2, mac_action)

        sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
        sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
        sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
        self.client.sai_thrift_remove_bridge_port(tunnel_bport)


        pkt3 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt2 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=40,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack2 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':16,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt4 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack2,
                                inner_frame = mpls_inner_pkt2)


        
        warmboot(self.client)
        try:


            #pw to ac
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packets( pkt4, [1])

            
        finally:
            sys_logging("======clean up======")
            
            sai_thrift_delete_fdb(self.client, bridge_id2, mac1, bport2)
            sai_thrift_delete_fdb(self.client, bridge_id2, mac2, tunnel_bport2)
            
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2, port2)
            
            self.client.sai_thrift_remove_bridge_port(tunnel_bport2)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 
            self.client.sai_thrift_remove_inseg_entry(mpls3)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id2)

class scenario_25_one_port_two_ac_and_delete_one_pw_to_ac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 16]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=40)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id2)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        next_hop2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id2, label_list3, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id2) 

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        bport2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id2)
        tunnel_bport2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id2, bridge_id=bridge_id2)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        sai_thrift_create_fdb_bport(self.client, bridge_id2, mac1, bport2, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id2, mac2, tunnel_bport2, mac_action)

        sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
        sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
        sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
        self.client.sai_thrift_remove_bridge_port(tunnel_bport)


        mpls_inner_pkt2 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=40,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack2 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label3,'tc':0,'ttl':16,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack2,
                                inner_frame = mpls_inner_pkt2)
        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:


            #bridge2 pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])

            
        finally:
            sys_logging("======clean up======")
            
            sai_thrift_delete_fdb(self.client, bridge_id2, mac1, bport2)
            sai_thrift_delete_fdb(self.client, bridge_id2, mac2, tunnel_bport2)
            
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2, port2)
            
            self.client.sai_thrift_remove_bridge_port(tunnel_bport2)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 
            self.client.sai_thrift_remove_inseg_entry(mpls3)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id2)


class scenario_26_vpls_set_tunnel_tagged_vlan_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[10]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

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

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
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

        mpls_inner_pkt2 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=50,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack2 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt5 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack2,
                                inner_frame = mpls_inner_pkt2)

        mpls_inner_pkt3 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=50,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack3 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt6 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack3,
                                inner_frame = mpls_inner_pkt3)
       
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 10, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [10])

            vlan_id2 = 50        
            attr_value = sai_thrift_attribute_value_t(u16=vlan_id2)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_TAGGED_VLAN,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            #ac to pw
            self.ctc_send_packet( 10, str(pkt1))
            self.ctc_verify_packets( pkt5, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt6))
            self.ctc_verify_packets( pkt4, [10])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_27_evpn_set_tunnel_encap_with_cw_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 16]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

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

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt2 = simple_tcp_packet(pktlen=96,
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

        mpls_label_stack2 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack2,
                                inner_frame = mpls_inner_pkt2)


        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt3, [1])

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_WITH_CW,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)

            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)

            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)  
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_28_evpn_set_tunnel_decap_with_cw_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 16]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
       
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

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

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        pkt2 = simple_tcp_packet(pktlen=96,
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

        mpls_label_stack2 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack2,
                                inner_frame = mpls_inner_pkt1)

        warmboot(self.client)
        try:
            #bridge1 pw to ac
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( pkt2, [2])
            
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_MPLS_PW_WITH_CW,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt2, [2])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_29_evpn_bum_set_tunnel_encap_es_label_valid_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'
        mac3 = '00:00:00:03:03:03'

        label1 = 100
        label2 = 200

        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_ttl_val=0, encap_tagged_vlan=30, decap_esi_label_valid=True, encap_esi_label_valid=True)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
       
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        esi_label=10001
        es_oid = sai_thrift_create_es(self.client, esi_label)

        attr_value = sai_thrift_attribute_value_t(oid=es_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

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

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':0},{'label':10001,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_label_stack2 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack2,
                                inner_frame = mpls_inner_pkt)

        #pdb.set_trace()
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])
            
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_ESI_LABEL_VALID,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)
            
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt3, [1])
        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_es(es_oid)
        
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_30_evpn_bum_set_tunnel_decap_es_label_valid_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[0]
        vlan_id = 20
        vlan_id2 = 10
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        ip_da2 = '5.5.5.3'
        dmac2 = '00:55:55:55:55:55'
        dmac = '00:55:55:55:55:66'
        mac1 = '00:00:01:01:01:01'
        mac2 = '00:00:00:02:02:02'
        mac3 = '00:00:00:03:03:03'


        label1 = 100
        label2 = 200
        label3 = 300
        label4 = 400


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3 = [(label3<<12) | 16]
        label_list4 = [(label4<<12) | 64]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_ttl_val=0, encap_tagged_vlan=30, decap_esi_label_valid=True, encap_esi_label_valid=True)
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)


        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        bport2 = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        esi_label=10001
        es_oid = sai_thrift_create_es(self.client, esi_label)

        attr_value = sai_thrift_attribute_value_t(oid=es_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

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

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':0},{'label':10001,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


        #pdb.set_trace()
        warmboot(self.client)
        try:

            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_verify_packets( pkt1, [0])
            self.ctc_verify_no_packet( pkt1, 2)
            
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID,value=attr_value)
            self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)

            ids_list = [SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID]
            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id1, ids_list)
            sys_logging("get tunnel attribute status = %d" %attrs.status)
            attr_list = attrs.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID:
                    sys_logging("### SAI_TUNNEL_ATTR_DECAP_ESI_LABEL_VALID = %d ###"  %attribute.value.booldata)

            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_verify_no_packet( pkt1, 0)
            self.ctc_verify_no_packet( pkt1, 2)
            

        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_es(es_oid)
        
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2, port4)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)

            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 

            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2) 


            self.client.sai_thrift_remove_next_hop(next_hop1)

            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_31_ten_label_sr_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac = '00:55:55:55:55:55'
        dmac2 = '00:55:55:55:55:66'
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
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)


        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop1)
       
        pkt_label1 = [{'label':label1_10,'tc':0,'ttl':32,'s':0}, {'label':label1_9,'tc':0,'ttl':32,'s':0} ,{'label':label1_8,'tc':0,'ttl':32,'s':0},\
        {'label':label1_7,'tc':0,'ttl':32,'s':0}, {'label':label1_6,'tc':0,'ttl':32,'s':0} ,{'label':label1_5,'tc':0,'ttl':32,'s':0}, {'label':label1_4,'tc':0,'ttl':32,'s':0},\
        {'label':label1_3,'tc':0,'ttl':32,'s':0} ,{'label':label1_2,'tc':0,'ttl':32,'s':0}, {'label':label1_1,'tc':0,'ttl':32,'s':1}]   


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
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= pkt_label1,
                                inner_frame = ip_only_pkt1) 

                                
        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [0])



        finally:
            sys_logging("======clean up======")
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_32_mpls_ac_to_pw_update_neighbor_test(sai_base_test.ThriftInterfaceDataPlane):
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
        vlan_id = 20
        
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
        #label_list = []
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        sai_thrift_create_fdb(self.client, vlan_oid, dmac3, port3, SAI_PACKET_ACTION_FORWARD)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, mac)
 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list, outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_UNIFORM)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
        

        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls1 = [{'label':100,'tc':0,'ttl':63,'s':1}]   
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

        pkt3 = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1)

        pkt4 = simple_mpls_packet(
                                eth_dst=dmac3,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1)


        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            
            addr = sai_thrift_ip_t(ip4=ip_da2)
            ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
            attr_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
            attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_IP, value=attr_value)
            status = self.client.sai_thrift_set_next_hop_attribute(next_hop2, attr)
            print 'set port type rif nhop status = %d' %status

            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt3, [1])


            attr_value = sai_thrift_attribute_value_t(oid=rif_id3)
            attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_ROUTER_INTERFACE_ID, value=attr_value)
            status = self.client.sai_thrift_set_next_hop_attribute(next_hop2, attr)
            print 'set port type rif nhop status = %d' %status
            
            addr = sai_thrift_ip_t(ip4=ip_da3)
            ipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
            attr_value = sai_thrift_attribute_value_t(ipaddr=ipaddr)
            attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_IP, value=attr_value)
            status = self.client.sai_thrift_set_next_hop_attribute(next_hop2, attr)
            print 'set port type rif nhop status = %d' %status

            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt4, [3])

        finally:
            sys_logging("======clean up======")

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
            
            self.client.sai_thrift_remove_next_hop(next_hop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
            

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_delete_fdb(self.client, vlan_oid, dmac3, port3)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)



class scenario_33_vpws_ac_to_ac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        vlan_id = 20
        vlan_id2 = 30
        vlan_id3 = 40
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        
        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

        
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)
        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, False)
        bport2 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan_id2, False)
        bport3 = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id, vlan_id3, False)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport2)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_value)

        #pdb.set_trace()
        self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr)
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
  
        pkt4 = simple_tcp_packet(pktlen=96,
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

        warmboot(self.client)
        try:
 
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt4, [3])

            #pw to ac
            self.ctc_send_packet( 3, str(pkt4))
            self.ctc_verify_packets( pkt1, [2])
 
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2, port3)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport3, port4)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
        
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_34_port_ac_vpls_raw_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[10]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #pdb.set_trace()
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)
        #pdb.set_trace()

        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1, 
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        pkt2 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
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
        exp_pkt3 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)



        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt4 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt5 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt5 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 10, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])
            self.ctc_send_packet( 10, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( exp_pkt3, [10])
            self.ctc_send_packet( 1, str(pkt4))
            self.ctc_verify_packets( exp_pkt4, [10])
            self.ctc_send_packet( 1, str(pkt5))
            self.ctc_verify_packets( exp_pkt5, [10])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            self.client.sai_thrift_remove_bridge_port(bport)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_35_port_ac_vpls_tagged_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[10]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #pdb.set_trace()
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)
        #pdb.set_trace()

        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        pkt2 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        pkt3 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=10,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                third_dl_vlan_enable=True,
                                third_vlan_vid=10,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt3 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


        mpls_inner_pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt4 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt5 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt5 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 10, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])
            self.ctc_send_packet( 10, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [1])
            self.ctc_send_packet( 10, str(pkt3))
            self.ctc_verify_packets( exp_pkt3, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt4))
            self.ctc_verify_packets( exp_pkt4, [10])
            self.ctc_send_packet( 1, str(pkt5))
            self.ctc_verify_packets( exp_pkt5, [10])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            self.client.sai_thrift_remove_bridge_port(bport)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_36_qinq_port_ac_vpls_raw_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 10
        cvlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id, cvlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #pdb.set_trace()
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)
        

        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1, 
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)


        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
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
        exp_pkt3 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt4 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt4 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                third_dl_vlan_enable=True,
                                third_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [2])
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( exp_pkt3, [2])

            self.ctc_send_packet( 1, str(pkt4))
            self.ctc_verify_packets( exp_pkt4, [2])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            self.client.sai_thrift_remove_bridge_port(bport) 
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_37_qinq_port_ac_vpls_tagged_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 10
        cvlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id, cvlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #pdb.set_trace()
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1, 
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
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
        exp_pkt3 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [2])
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( exp_pkt3, [2])
   
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            self.client.sai_thrift_remove_bridge_port(bport) 
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_38_port_ac_vpws_tagged_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        
        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

        
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id, admin_state=False)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_value)

        #pdb.set_trace()
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        #pdb.set_trace()
        

        
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
        mpls_inner_pkt = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
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

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
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
        pkt4 = simple_tcp_packet(pktlen=96,
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

        warmboot(self.client)
        try:
 
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])
 
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_bridge_port(bport)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
        
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_39_port_ac_vpws_raw_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        
        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

        
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id, admin_state=False)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_value)

        #pdb.set_trace()
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        

        
        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)

        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
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
 
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_bridge_port(bport)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
        
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_40_qinq_port_ac_vpws_tagged_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 20
        cvlan_id = 40
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        
        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

        
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)
        bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id, cvlan_id, admin_state=False)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_value)

        
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        

        
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=40,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=40,
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

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=40,
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
        pkt4 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=40,
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
 
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_bridge_port(bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
        
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_42_qinq_port_ac_vpws_raw_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 20
        cvlan_id = 40
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        
        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

        
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)
        bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id, cvlan_id, admin_state=False)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_value)

        #pdb.set_trace()
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        
        

        
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=40,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=40,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)

        pkt4 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
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
 
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_bridge_port(bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
        
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_43_port_ac_to_sub_and_qinq_vpws_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 20
        cvlan_id = 40

        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport1 = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id, admin_state=False)
        bport2= sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id, cvlan_id, admin_state=False)
        bport3= sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, svlan_id, admin_state=False)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport2)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(bport1, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport1)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport1, bport_attr)
        #pdb.set_trace()
        

        
        pkt1 = simple_tcp_packet(pktlen=96,
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
        pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt3 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=40,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=40,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt5 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=50,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        
        pkt6 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=50,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        warmboot(self.client)
        try:
 
            #port to qinq
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [2])

            #qinq to port
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])

            bport_attr_value = sai_thrift_attribute_value_t(booldata=False)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport1, bport_attr)

            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport3)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport1, bport_attr_xcport)
            
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport1)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport3, bport_attr_xcport)

            bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport3, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport1, bport_attr)

            #port to sub
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [2])

            #sub to port
            self.ctc_send_packet( 2, str(pkt5))
            self.ctc_verify_packets( pkt6, [2])
                
            bport_attr_value = sai_thrift_attribute_value_t(booldata=False)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport3, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport1, bport_attr)

            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport3)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr_xcport)
            
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport2)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport3, bport_attr_xcport)

            bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport3, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr)

            #qinq to sub
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packets( pkt3, [2])
            
            #sub to qinq
            self.ctc_send_packet( 2, str(pkt5))
            self.ctc_verify_packets( pkt5, [2])
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_bridge_port(bport3)
            self.client.sai_thrift_remove_bridge_port(bport2)
            self.client.sai_thrift_remove_bridge_port(bport1)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            
        

            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_44_port_subport_and_qinq_port_ac_to_ac_vpls_unicast_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 10
        svlan_id2 = 15
        cvlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        mac3 = '00:00:00:03:03:03'
        mac4 = '00:00:00:04:04:04'
        mac5 = '00:00:00:05:05:05'
        mac6 = '00:00:00:06:06:06'
        mac7 = '00:00:00:07:07:07'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)  
        
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport2_1 = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id)
        bport2_2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, svlan_id)
        bport2_3 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id, cvlan_id)
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port3)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport3_1 = sai_thrift_create_bridge_port(self.client, port_id=port3, bridge_id=bridge_id)
        bport3_2 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, svlan_id)
        bport3_3 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port3, bridge_id, svlan_id2, cvlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport2_1, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, bport2_2, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac3, bport2_3, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac4, bport3_1, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac5, bport3_2, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac6, bport3_3, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac7, tunnel_bport, mac_action)

        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac4,
                                eth_src=mac1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        exp_pkt1 = pkt1

        pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac4,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        exp_pkt2 = pkt2
        pkt3 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        exp_pkt3 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        pkt4 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac3,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        exp_pkt4 = simple_tcp_packet(pktlen=104,
                                eth_dst=mac3,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt5 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac5,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        exp_pkt5 = pkt5

        pkt6 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac4,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        exp_pkt6 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac4,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt7 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        exp_pkt7 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        pkt8 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac3,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)        
        exp_pkt8 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac3,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5) 
        pkt9 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac6,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)        
        exp_pkt9 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac6,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=15,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5) 
        pkt10 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac4,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)        
        exp_pkt10 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac4,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5) 
        pkt11 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac5,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=15,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)        
        exp_pkt11 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac5,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5) 

        warmboot(self.client)
        try:
            #port(p) to port(p)
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [3])
            #port(p+c) to port(p+c)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [3])
            #port(p+c) to subport(p+s+c)
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packets( exp_pkt3, [2])
            #port(p+c) to qinq port(p+s+c)
            self.ctc_send_packet( 2, str(pkt4))
            self.ctc_verify_packets( exp_pkt4, [2])

            #subport(p+s+c) to subport(p+s+c)
            self.ctc_send_packet( 2, str(pkt5))
            self.ctc_verify_packets( exp_pkt5, [3])
            #subport(p+s+c) to port(p+c)
            self.ctc_send_packet( 2, str(pkt6))
            self.ctc_verify_packets( exp_pkt6, [3])
            #subport(p+s) to port(p)
            self.ctc_send_packet( 2, str(pkt7))
            self.ctc_verify_packets( exp_pkt7, [2])
            #subport(p+s+c) to qinq port(p+s+c)
            self.ctc_send_packet( 2, str(pkt8))
            self.ctc_verify_packets( exp_pkt8, [2])

            #qinq port(p+s+c) to qinq port(p+s+c)
            self.ctc_send_packet( 2, str(pkt9))
            self.ctc_verify_packets( exp_pkt9, [3])
            #qinq port(p+s+c) to port(p+c)
            self.ctc_send_packet( 2, str(pkt10))
            self.ctc_verify_packets( exp_pkt10, [3])
            #qinq port(p+s+c) to subport(p+s+c)
            self.ctc_send_packet( 3, str(pkt11))
            self.ctc_verify_packets( exp_pkt11, [3])

            
        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)

            self.client.sai_thrift_remove_bridge_port(bport2_1)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2_2, port2)
            self.client.sai_thrift_remove_bridge_port(bport2_3) 
            self.client.sai_thrift_remove_bridge_port(bport3_1)
            sai_thrift_create_bridge_port(self.client, port3, type = SAI_BRIDGE_PORT_TYPE_PORT)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport3_2, port3)
            self.client.sai_thrift_remove_bridge_port(bport3_3) 
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_45_port_subport_and_qinq_port_and_tunnelport_vpls_BUM_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 10
        svlan_id2 = 15
        cvlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        mac3 = '00:00:00:03:03:03'
        mac4 = '00:00:00:04:04:04'
        mac5 = '00:00:00:05:05:05'
        mac6 = '00:00:00:06:06:06'
        mac7 = '00:00:00:07:07:07'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)  
        
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport2_1 = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id)
        bport2_2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, svlan_id)
        bport2_3 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id2, cvlan_id)
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port3)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport3_1 = sai_thrift_create_bridge_port(self.client, port_id=port3, bridge_id=bridge_id)
        bport3_2 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, svlan_id)
        bport3_3 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port3, bridge_id, svlan_id2, cvlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        
   

        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=104,
                                eth_dst=mac2,
                                eth_src=mac1, 
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        pkt2 = simple_tcp_packet(pktlen=104,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        pkt3 = simple_tcp_packet(pktlen=104,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=15,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

       
        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( exp_pkt1, [1])
            #self.ctc_verify_packets( pkt2, [2])
            #self.ctc_verify_packets( pkt2, [3])
            #self.ctc_verify_packets( pkt3, [2])
            #self.ctc_verify_packets( pkt3, [3])
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, pkt2, pkt3, pkt2, pkt3,pkt1], [1, 2, 2, 3, 3,3])
           
            
        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)

            self.client.sai_thrift_remove_bridge_port(bport2_1)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2_2, port2)
            self.client.sai_thrift_remove_bridge_port(bport2_3) 
            self.client.sai_thrift_remove_bridge_port(bport3_1)
            sai_thrift_create_bridge_port(self.client, port3, type = SAI_BRIDGE_PORT_TYPE_PORT)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport3_2, port3)
            self.client.sai_thrift_remove_bridge_port(bport3_3) 
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_46_qinq_port_use_service_vlan_assign_cos_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 10
        cvlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id, cvlan_id, service_vlan_id = 100, service_vlan_cos_mode = SAI_BRIDGE_PORT_OUTGOING_SERVICE_VLAN_COS_MODE_ASSIGN, service_vlan_cos = 7)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #pdb.set_trace()
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1, 
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                vlan_pcp=7,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)


        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
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
        exp_pkt3 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                vlan_pcp=7,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt4 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt4 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                vlan_pcp=7,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                third_dl_vlan_enable=True,
                                third_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [2])
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( exp_pkt3, [2])

            self.ctc_send_packet( 1, str(pkt4))
            self.ctc_verify_packets( exp_pkt4, [2])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            self.client.sai_thrift_remove_bridge_port(bport) 
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_47_qinq_port_use_service_vlan_map_cos_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 10
        cvlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)   
        mpls1 = sai_thrift_inseg_entry_t(label1)
        mpls2 = sai_thrift_inseg_entry_t(label2) 
        attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr)
        self.client.sai_thrift_set_inseg_entry_attribute(mpls2, attr)

        bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id, cvlan_id, service_vlan_id = 100, service_vlan_cos_mode = SAI_BRIDGE_PORT_OUTGOING_SERVICE_VLAN_COS_MODE_MAP, service_vlan_cos = 7)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #pdb.set_trace()
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1, 
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':5,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                vlan_pcp=5,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)


        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':6,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt3 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                vlan_pcp=6,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':4,'ttl':32,'s':1}]
        pkt4 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt4 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                vlan_pcp=4,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                third_dl_vlan_enable=True,
                                third_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [2])
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( exp_pkt3, [2])

            self.ctc_send_packet( 1, str(pkt4))
            self.ctc_verify_packets( exp_pkt4, [2])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            self.client.sai_thrift_remove_bridge_port(bport) 
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_48_sub_port_use_service_vlan_assign_cos_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[10]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, service_vlan_id = 200, service_vlan_cos_mode = SAI_BRIDGE_PORT_OUTGOING_SERVICE_VLAN_COS_MODE_ASSIGN, service_vlan_cos = 6)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #pdb.set_trace()
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)
        #pdb.set_trace()
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
        pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=200,
                                vlan_pcp=6,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 10, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [10])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_49_sub_port_use_service_vlan_map_cos_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        mpls1 = sai_thrift_inseg_entry_t(label1)
        mpls2 = sai_thrift_inseg_entry_t(label2) 
        attr_value = sai_thrift_attribute_value_t(s32 = SAI_INSEG_ENTRY_PSC_TYPE_ELSP)
        attr       = sai_thrift_attribute_t(id = SAI_INSEG_ENTRY_ATTR_PSC_TYPE, value = attr_value)
        self.client.sai_thrift_set_inseg_entry_attribute(mpls1, attr)
        self.client.sai_thrift_set_inseg_entry_attribute(mpls2, attr)

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, service_vlan_id = 200, service_vlan_cos_mode = SAI_BRIDGE_PORT_OUTGOING_SERVICE_VLAN_COS_MODE_MAP)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_outer=20,
                                dl_vlan_pcp_outer=0,
                                dl_vlan_cfi_outer=1,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':5,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)

        pkt4 = simple_qinq_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_outer=200,
                                dl_vlan_pcp_outer=5,
                                dl_vlan_cfi_outer=0,
                                vlan_vid=10,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_ttl=64,
                                ip_ihl=5)
        #pdb.set_trace()
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [2])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_50_port_subport_and_qinq_port_and_tunnelport_need_flood_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 10
        svlan_id2 = 15
        cvlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        mac3 = '00:00:00:03:03:03'
        mac4 = '00:00:00:04:04:04'
        mac5 = '00:00:00:05:05:05'
        mac6 = '00:00:00:06:06:06'
        mac7 = '00:00:00:07:07:07'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)  
        
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport2_1 = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id)
        bport2_2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, svlan_id, need_flood = False)
        bport2_3 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id2, cvlan_id, need_flood = False)
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port3)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport3_1 = sai_thrift_create_bridge_port(self.client, port_id=port3, bridge_id=bridge_id, need_flood = False)
        bport3_2 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, svlan_id)
        bport3_3 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port3, bridge_id, svlan_id2, cvlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        


        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=104,
                                eth_dst=mac2,
                                eth_src=mac1, 
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        pkt2 = simple_tcp_packet(pktlen=104,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        pkt3 = simple_tcp_packet(pktlen=104,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=15,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

       
        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( exp_pkt1, [1])
            #self.ctc_verify_packets( pkt2, [2])
            #self.ctc_verify_packets( pkt2, [3])
            #self.ctc_verify_packets( pkt3, [2])
            #self.ctc_verify_packets( pkt3, [3])
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, pkt2, pkt3], [1, 3, 3])

            bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_NEED_FLOOD, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport2_2, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport2_3, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport3_1, bport_attr)

            bport_attr_value = sai_thrift_attribute_value_t(booldata=False)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_NEED_FLOOD, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport3_2, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport3_3, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)

            self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( exp_pkt1, [1])
            #self.ctc_verify_packets( pkt2, [2])
            #self.ctc_verify_packets( pkt2, [3])
            #self.ctc_verify_packets( pkt3, [2])
            #self.ctc_verify_packets( pkt3, [3])
            self.ctc_verify_each_packet_on_each_port( [pkt2, pkt3, pkt1], [2, 2,3])
           
            
        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)

            self.client.sai_thrift_remove_bridge_port(bport2_1)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2_2, port2)
            self.client.sai_thrift_remove_bridge_port(bport2_3) 
            self.client.sai_thrift_remove_bridge_port(bport3_1)
            sai_thrift_create_bridge_port(self.client, port3, type = SAI_BRIDGE_PORT_TYPE_PORT)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport3_2, port3)
            self.client.sai_thrift_remove_bridge_port(bport3_3) 
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_51_port_use_service_vlan_assign_cos_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id, service_vlan_id = 200, service_vlan_cos_mode = SAI_BRIDGE_PORT_OUTGOING_SERVICE_VLAN_COS_MODE_ASSIGN, service_vlan_cos = 6)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        #pdb.set_trace()
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)
        #pdb.set_trace()

        '''
        pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1, 
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        pkt2 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
        '''
        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
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
        exp_pkt3 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)



        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt4 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt5 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        exp_pkt5 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            #self.ctc_send_packet( 10, str(pkt1))
            #self.ctc_verify_packets( exp_pkt1, [1])
            #self.ctc_send_packet( 10, str(pkt2))
            #self.ctc_verify_packets( exp_pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( exp_pkt3, [2])
            self.ctc_send_packet( 1, str(pkt4))
            self.ctc_verify_packets( exp_pkt4, [2])
            self.ctc_send_packet( 1, str(pkt5))
            self.ctc_verify_packets( exp_pkt5, [2])

            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            self.client.sai_thrift_remove_bridge_port(bport)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_52_vpls_only_encap_and_set_tunnel_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        mac_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        #encap
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

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

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
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
                                ip_ttl=16,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        pkt4 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=16,
                                ip_ihl=5)

        
        warmboot(self.client)
        try:
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            attr_value = sai_thrift_attribute_value_t(u8=SAI_TUNNEL_MPLS_PW_MODE_RAW)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE,value=attr_value)
            status= self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)
            sys_logging("set tunnel attribute encap ttl mode status = %d" %status)
            assert(status == SAI_STATUS_OBJECT_IN_USE)

            attr_value = sai_thrift_attribute_value_t(u8=SAI_TUNNEL_MPLS_PW_MODE_RAW)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE,value=attr_value)
            status = self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)
            sys_logging("set tunnel attribute decap ttl mode status = %d" %status)
            assert(status == SAI_STATUS_SUCCESS)
            #decap
            rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
            rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
            sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
            sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
            sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
            try:
                #ac to pw
                self.ctc_send_packet( 2, str(pkt1))
                self.ctc_verify_packets( pkt2, [1])
                #pw to ac
                self.ctc_send_packet( 1, str(pkt3))
                self.ctc_verify_packets( pkt4, [2])

            finally:
                #decap
                sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
                mpls1 = sai_thrift_inseg_entry_t(label1)
                mpls2 = sai_thrift_inseg_entry_t(label2) 
                self.client.sai_thrift_remove_inseg_entry(mpls1)
                self.client.sai_thrift_remove_inseg_entry(mpls2)
                self.client.sai_thrift_remove_router_interface(rif_id2)
                self.client.sai_thrift_remove_router_interface(rif_id3)

            
        finally:
            sys_logging("======clean up======")
            #encap
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)

class scenario_53_vpls_only_decap_and_set_tunnel_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[10]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        mac_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        #decap
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)
        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)

        
        pkt1 = simple_tcp_packet(pktlen=100,
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
                                dl_vlan_enable=False,
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
            #self.ctc_send_packet( 10, str(pkt1))
            #self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( pkt4, [10])
            
            attr_value = sai_thrift_attribute_value_t(u8=SAI_TUNNEL_MPLS_PW_MODE_RAW)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_ENCAP_MPLS_PW_MODE,value=attr_value)
            status= self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)
            sys_logging("set tunnel attribute encap ttl mode status = %d" %status)
            assert(status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(u8=SAI_TUNNEL_MPLS_PW_MODE_RAW)
            attr = sai_thrift_attribute_t(id=SAI_TUNNEL_ATTR_DECAP_MPLS_PW_MODE,value=attr_value)
            status = self.client.sai_thrift_set_tunnel_attribute(tunnel_id1, attr)
            sys_logging("set tunnel attribute decap ttl mode status = %d" %status)
            assert(status == SAI_STATUS_OBJECT_IN_USE)

            #encap       
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
            next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
            tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
            sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

            try:
                #ac to pw
                self.ctc_send_packet( 10, str(pkt1))
                self.ctc_verify_packets( pkt2, [1])

                #pw to ac
                self.ctc_send_packet( 1, str(pkt3))
                self.ctc_verify_packets( pkt4, [10])

            finally:
                #encap
                sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
                self.client.sai_thrift_remove_bridge_port(tunnel_bport)
                self.client.sai_thrift_remove_next_hop(next_hop1)
                self.client.sai_thrift_remove_next_hop(next_hop)
                sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            
        finally:
            sys_logging("======clean up======")
            


            #decap
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)
            flush_all_fdb(self.client)


class scenario_54_port_subport_and_qinq_port_and_tunnelport_learning_disable_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 10
        svlan_id2 = 15
        cvlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        mac3 = '00:00:00:03:03:03'
        mac4 = '00:00:00:04:04:04'
        mac5 = '00:00:00:05:05:05'
        mac6 = '00:00:00:06:06:06'
        mac7 = '00:00:00:07:07:07'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)  
        
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport2_1 = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id, learn_mode = SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE)
        bport2_2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, svlan_id, learn_mode = SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE)
        bport2_3 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id2, cvlan_id, learn_mode = SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE)
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port3)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport3_1 = sai_thrift_create_bridge_port(self.client, port_id=port3, bridge_id=bridge_id, learn_mode = SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE)
        bport3_2 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, svlan_id, learn_mode = SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE)
        bport3_3 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port3, bridge_id, svlan_id2, cvlan_id, learn_mode = SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, learn_mode = SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE)
        
   

        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        pkt2 = simple_tcp_packet(pktlen=104,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        pkt3 = simple_tcp_packet(pktlen=104,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=15,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
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
        pkt4 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
       
        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id, mac1)
            assert( 0 == status)

            self.ctc_send_packet( 2, str(pkt2))
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id, mac1)
            assert( 0 == status)

            self.ctc_send_packet( 2, str(pkt3))
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id, mac1)
            assert( 0 == status)

            self.ctc_send_packet( 1, str(pkt4))
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id, mac2)
            assert( 0 == status)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_BRIDGE_PORT_FDB_LEARNING_MODE_HW)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE, value=attr_value)
            status = self.client.sai_thrift_set_bridge_port_attribute(bport2_1, thrift_attr=attr)
            print 'set bport2_1 attribute status = %d' %status
            status = self.client.sai_thrift_set_bridge_port_attribute(bport2_2, thrift_attr=attr)
            print 'set bport2_2 attribute status = %d' %status
            status = self.client.sai_thrift_set_bridge_port_attribute(bport2_3, thrift_attr=attr)
            print 'set bport2_3 attribute status = %d' %status
            status = self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, thrift_attr=attr)
            print 'set tunnel_bport attribute status = %d' %status

            self.ctc_send_packet( 2, str(pkt1))
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id, mac1)
            assert( 1 == status)

            self.ctc_send_packet( 2, str(pkt2))
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id, mac1)
            assert( 1 == status)

            self.ctc_send_packet( 2, str(pkt3))
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id, mac1)
            assert( 1 == status)

            self.ctc_send_packet( 1, str(pkt4))
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id, mac2)
            assert( 1 == status)
           
            
        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)

            self.client.sai_thrift_remove_bridge_port(bport2_1)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2_2, port2)
            self.client.sai_thrift_remove_bridge_port(bport2_3) 
            self.client.sai_thrift_remove_bridge_port(bport3_1)
            sai_thrift_create_bridge_port(self.client, port3, type = SAI_BRIDGE_PORT_TYPE_PORT)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport3_2, port3)
            self.client.sai_thrift_remove_bridge_port(bport3_3) 
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_55_port_reflective_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        #1d port reflective enable,1q port reflective disable
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        port5 = port_list[5]
        svlan_id = 10
        svlan_id2 = 15
        cvlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        mac3 = '00:00:00:03:03:03'
        mac4 = '00:00:00:04:04:04'
        mac5 = '00:00:00:05:05:05'
        mac6 = '00:00:00:06:06:06'
        mac7 = '00:00:00:07:07:07'


        label1 = 100
        label2 = 200
        label3 = 300


        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)  
        
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport2_1 = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id)
        bport2_2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, svlan_id)
        bport2_3 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id, svlan_id2, cvlan_id)
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port3)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport3_1 = sai_thrift_create_bridge_port(self.client, port_id=port3, bridge_id=bridge_id)
        bport3_2 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, svlan_id)
        bport3_3 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port3, bridge_id, svlan_id2, cvlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)
        
   

        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt = simple_tcp_packet(pktlen=104,
                                eth_dst=mac2,
                                eth_src=mac1, 
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        pkt2 = simple_tcp_packet(pktlen=104,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        pkt3 = simple_tcp_packet(pktlen=104,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=15,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

       
        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( exp_pkt1, [1])
            #self.ctc_verify_packets( pkt2, [2])
            #self.ctc_verify_packets( pkt2, [3])
            #self.ctc_verify_packets( pkt3, [2])
            #self.ctc_verify_packets( pkt3, [3])
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, pkt2, pkt3, pkt2, pkt3,pkt1], [1, 2, 2, 3, 3,3])

            self.client.sai_thrift_remove_bridge_port(bport2_1)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2_2, port2)
            self.client.sai_thrift_remove_bridge_port(bport2_3) 
            self.client.sai_thrift_remove_bridge_port(bport3_1)
            sai_thrift_create_bridge_port(self.client, port3, type = SAI_BRIDGE_PORT_TYPE_PORT)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport3_2, port3)
            self.client.sai_thrift_remove_bridge_port(bport3_3) 
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)

            vlan = 10
            vlan_id = sai_thrift_create_vlan(self.client, vlan)
            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_id, attr)

            vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
            vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
            vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_id, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
            vlan_member5 = sai_thrift_create_vlan_member(self.client, vlan_id, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

            grp_id = self.client.sai_thrift_create_l2mc_group([])
            member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
            member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
            member_id3 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port4)

            dmac1 = '01:00:5E:7F:01:01'
            smac1 = '00:00:00:00:00:01'
            smac2 = '00:00:00:00:00:02'
            dip_addr1 = '230.255.1.1'
            sip_addr1 = '10.10.10.1'
            sip_addr2 = '10.10.10.2'
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            default_addr = '0.0.0.0'
            type = SAI_L2MC_ENTRY_TYPE_XG
            l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_id, dip_addr1, default_addr, type)

            pkt1 = simple_tcp_packet(eth_dst=dmac1, eth_src=smac1,
                                     ip_dst=dip_addr1, ip_src=sip_addr1,
                                     ip_id=105, ip_ttl=64,
                                     dl_vlan_enable=True, vlan_vid=vlan)
            pkt2 = simple_tcp_packet(eth_dst=dmac1, eth_src=smac2,
                                     ip_dst=dip_addr1, ip_src=sip_addr2,
                                     ip_id=105, ip_ttl=64,
                                     dl_vlan_enable=True, vlan_vid=vlan)

            try:
                sys_logging("### unknown multicast ###")
                self.ctc_send_packet(2, str(pkt1))
                self.ctc_verify_packets(pkt1, [3,4,5])
                self.ctc_verify_no_packet(str(pkt1), 2)

                self.ctc_send_packet(3, str(pkt2))
                self.ctc_verify_packets(pkt2, [2,4,5])
                self.ctc_verify_no_packet(str(pkt2), 3)

                assert(SAI_STATUS_SUCCESS == sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id))
                assert(SAI_STATUS_ITEM_ALREADY_EXISTS == sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id))

                sys_logging("### known multicast ###")
                self.ctc_send_packet(2, str(pkt1))
                self.ctc_verify_packets(pkt1, [3,4])
                self.ctc_verify_no_packet(str(pkt1), 2)
                self.ctc_verify_no_packet(str(pkt1), 5)

                self.ctc_send_packet(3, str(pkt2))
                self.ctc_verify_packets(pkt2, [2,4])
                self.ctc_verify_no_packet(str(pkt2), 3)
                self.ctc_verify_no_packet(str(pkt1), 5)

            finally:
                self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
                self.client.sai_thrift_remove_l2mc_group_member(member_id1)
                self.client.sai_thrift_remove_l2mc_group_member(member_id2)
                self.client.sai_thrift_remove_l2mc_group_member(member_id3)
                self.client.sai_thrift_remove_l2mc_group(grp_id)
                self.client.sai_thrift_remove_vlan_member(vlan_member5)
                self.client.sai_thrift_remove_vlan_member(vlan_member2)
                self.client.sai_thrift_remove_vlan_member(vlan_member3)
                self.client.sai_thrift_remove_vlan_member(vlan_member4)
                self.client.sai_thrift_remove_vlan(vlan_id)
           
            
        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)

            
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_56_ut_sr_vpws_test(sai_base_test.ThriftInterfaceDataPlane):
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
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        
        label1 = 100
        label2 = 200
        label3 = 300
        label4 = 400
        label5 = 500
        label6 = 150
        label7 = 250
        label8 = 350
        label9 = 450
        label10 = 550
        label_list = [(label1<<12) | 32, (label2<<12) | 32, (label3<<12) | 32]
        label11 = 20
        #label_list1 = [(label1<<12) | 64]
        label_list2 = [(label11<<12) | 32]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        a = testutils.test_params_get()['chipname']
        if a == 'tsingma':
            next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list, outseg_type=SAI_OUTSEG_TYPE_SWAP)
        elif a == 'tsingma_mx':
            next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label11, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

        
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)
        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, False)

        
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
        #pdb.set_trace()

        
        pkt1 = simple_tcp_packet(pktlen=100,
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
                                dl_vlan_enable=False,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label3,'tc':0,'ttl':32,'s':0},{'label':label2,'tc':0,'ttl':32,'s':0},{'label':label1,'tc':0,'ttl':32,'s':0},{'label':label11,'tc':0,'ttl':32,'s':1}]
        pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=False,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label11,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
        pkt4 = simple_tcp_packet(pktlen=100,
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
 
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
        
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3)
            mpls11 = sai_thrift_inseg_entry_t(label11) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_inseg_entry(mpls3)
            self.client.sai_thrift_remove_inseg_entry(mpls11)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)


class scenario_57_vpws_set_cross_connect_to_null_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        svlan_id = 20
        cvlan_id = 40
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        
        label1 = 100 
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)

        
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)
        old_port_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        self.client.sai_thrift_remove_bridge_port(old_port_oid)
        bport = sai_thrift_create_bridge_port(self.client, port_id=port2, bridge_id=bridge_id, admin_state=False)
        bport2= sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, svlan_id, admin_state=False)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)

        #pdb.set_trace()
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        
        

        
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)
        pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)
        mpls_inner_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        mpls_inner_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt1)

        exp_pkt2 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt2)
                                
        mpls_inner_pkt3 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt3)

        exp_pkt3 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        exp_pkt4 = simple_tcp_packet(pktlen=96,
                                eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=1,
                                ip_ttl=64,
                                ip_ihl=5)

        warmboot(self.client)
        try:
 
            #ac to pw
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt2, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( exp_pkt4, [2])

            bport_attr_value = sai_thrift_attribute_value_t(booldata=False)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)

            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=0)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)
            
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=0)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)

            #set new cross connect
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr_xcport)
            
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport2)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)

            bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr)

            #ac to pw
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packets( exp_pkt1, [1])

            #pw to ac
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_verify_packets( exp_pkt3, [2])

            bport_attr_value = sai_thrift_attribute_value_t(booldata=False)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr)

            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=0)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr_xcport)
            
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=0)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr_xcport)

            #set new cross connect
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr_xcport)
            
            bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=bport2)
            bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr_xcport)

            bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, bport_attr)

            #sub port to port
            self.ctc_send_packet( 2, str(exp_pkt3))
            self.ctc_verify_packets( exp_pkt4, [2])

            #port to sub port
            self.ctc_send_packet( 2, str(exp_pkt4))
            self.ctc_verify_packets( exp_pkt3, [2])
 
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_bridge_port(bport2)
            self.client.sai_thrift_remove_bridge_port(bport)
            sai_thrift_create_bridge_port(self.client, port2, type = SAI_BRIDGE_PORT_TYPE_PORT)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
        
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)



class scenario_58_vpws_tunnel_port_to_tunnel_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id1 = 10
        vlan_id2 = 20
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

        
        label1 = 102408 
        label2 = 202408
        label3 = 102410 
        label4 = 202410
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        label_list3= [(label3<<12) | 64]
        label_list4 = [(label4<<12) | 32]
        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

        #tunnel port1
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id4, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id3, packet_action, tunnel_id=tunnel_id1)
        tunnel_bport1 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, admin_state=False)

        #tunnel port2
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list3)
        next_hop3 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id2, label_list4, next_level_nhop_oid=next_hop2)
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, rif_id4, packet_action)
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, rif_id3, packet_action, tunnel_id=tunnel_id2)
        tunnel_bport2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id2, bridge_id=bridge_id, admin_state=False)


        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport1)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport2, bport_attr_xcport)
        #pdb.set_trace()
        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=tunnel_bport2)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT, value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport1, bport_attr_xcport)
        
        bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport1, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport2, bport_attr)
        

        mpls_inner_pkt = simple_tcp_packet(pktlen=96,
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

        mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)

        pkt2 = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
        mpls_inner_pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                second_dl_vlan_enable=True,
                                second_vlan_vid=20,
                                ip_dst='1.1.1.1',
                                ip_src='2.2.2.2',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        mpls_label_stack1 = [{'label':label3,'tc':0,'ttl':64,'s':0},{'label':label4,'tc':0,'ttl':32,'s':1}]
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:55:55:55:55:66',
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack1,
                                inner_frame = mpls_inner_pkt1)
                                
        pkt4 = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt1)

        warmboot(self.client)
        try:
 
            #ac to pw
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( pkt4, [2])

            #pw to ac
            self.ctc_send_packet( 2, str(pkt3))
            self.ctc_verify_packets( pkt2, [1])
 
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_bridge_port(tunnel_bport1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport2)
        
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            mpls3 = sai_thrift_inseg_entry_t(label3)
            mpls4 = sai_thrift_inseg_entry_t(label4) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            self.client.sai_thrift_remove_inseg_entry(mpls3)
            self.client.sai_thrift_remove_inseg_entry(mpls4) 
            self.client.sai_thrift_remove_next_hop(next_hop3)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)





