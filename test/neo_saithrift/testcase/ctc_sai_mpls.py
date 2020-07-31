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
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask

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
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            sai_thrift_remove_bridge_sub_port(self.client, bport2, port3)
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

        label1 = 50
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("======Create 8191 inseg entry(1 exist when init)======")
        for label in range(100,8291):
            sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, rif_id1, packet_action)
        warmboot(self.client)
        try:
            sys_logging("======Create another inseg entry======")
            status = sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id1, packet_action)
            sys_logging("create inseg entry status = %d" %status)
            assert (status == SAI_STATUS_INSUFFICIENT_RESOURCES)

            #pdb.set_trace()
        finally:
            sys_logging("======clean up======")
            for i in range(100,8291):
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
            '''
            attr_value = sai_thrift_attribute_value_t(oid=counter_id1)
            attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_COUNTER_ID, value=attr_value)
            self.client.sai_thrift_set_route_attribute(next_hop, attr)
            attr_value = sai_thrift_attribute_value_t(oid=counter_id2)
            attr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_ATTR_COUNTER_ID, value=attr_value)
            self.client.sai_thrift_set_route_attribute(next_hop1, attr)
            
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_ATTR_COUNTER_ID:
                    print a.value.oid
                    if counter_id1 != a.value.oid:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_next_hop_attribute(next_hop1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_ATTR_COUNTER_ID:
                    if counter_id2 != a.value.oid:
                        raise NotImplementedError()
            '''
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
            assert (es_oid1%0x100000000 == 0x59)
           
            sys_logging("create es oid = 0x%x" %es_oid2)
            assert (es_oid2%0x100000000 == 0x59)
            
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

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)
        

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

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id3, packet_action)


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
                               ip_ttl=99)
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

        label_list = [(label1<<12) | 32]
        pop_nums = 0
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, next_hop2, packet_action)
        
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
                               
        mpls2 = [{'label':100,'tc':0,'ttl':32,'s':1}]
        #sai bug,actually label ttl should be 31 ,ip ttl should be 64
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=31,
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
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_da2, rif_id2)

        #sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, next_hop3, packet_action)

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
                               ip_ttl=99)
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
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
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
                                dl_vlan_pcp_outer=2,
                                dl_vlan_cfi_outer=1,
                                vlan_vid=10,
                                vlan_pcp=2,
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
                                vlan_pcp=2,
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
                                vlan_pcp=2,
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
                                dl_vlan_pcp_outer=2,
                                dl_vlan_cfi_outer=1,
                                vlan_vid=10,
                                vlan_pcp=2,
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
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
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
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
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
                                dl_vlan_pcp_outer=2,
                                dl_vlan_cfi_outer=1,
                                vlan_vid=10,
                                vlan_pcp=2,
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
                                vlan_pcp=2,
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
                                vlan_pcp=2,
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
                                dl_vlan_pcp_outer=2,
                                dl_vlan_cfi_outer=1,
                                vlan_vid=10,
                                vlan_pcp=2,
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
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
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

        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list)
        pdb.set_trace()
        next_hop2 = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, label_list2, next_level_nhop_oid=next_hop1)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask, next_hop2)


        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst=ip_addr1_subnet,
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=20)
                               
        mpls1 = [{'label':label10,'tc':0,'ttl':32,'s':0}, {'label':label9,'tc':0,'ttl':32,'s':0} ,{'label':label8,'tc':0,'ttl':32,'s':0},\
        {'label':label7,'tc':0,'ttl':32,'s':0}, {'label':label6,'tc':0,'ttl':32,'s':0} ,{'label':label5,'tc':0,'ttl':32,'s':0}, {'label':label4,'tc':0,'ttl':32,'s':0},\
        {'label':label3,'tc':0,'ttl':32,'s':0} ,{'label':label2,'tc':0,'ttl':32,'s':0}, {'label':label1,'tc':0,'ttl':32,'s':0}, {'label':label0,'tc':3,'ttl':18,'s':1}]   
        #some problem need test again later
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst=ip_addr1_subnet,
                                ip_ttl=19,
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
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_da2, rif_id2)

        #sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, next_hop3, packet_action)
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

            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2_subnet, ip_mask, next_hop3)
            
            self.client.sai_thrift_remove_next_hop(next_hop3)
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
            sai_thrift_remove_bridge_sub_port(self.client, bport2, port2)
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
            sai_thrift_remove_bridge_sub_port(self.client, bport2, port2)
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
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

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
            assert( 1 == status)
            #assert( 0 == status)   bug110766,should support mpls fdb learning disable 

            #bridge1 ac to pw again
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])

            self.ctc_verify_no_packet( pkt1, 3)
            #self.ctc_verify_packets( pkt1, [3])    bug110766,should support mpls fdb learning disable 

            
        finally:
            sys_logging("======clean up======")
            flush_all_fdb(self.client)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            #sai_thrift_delete_fdb(self.client, bridge_id2, mac1, bport2)
            #sai_thrift_delete_fdb(self.client, bridge_id2, mac2, tunnel_bport2)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port(self.client, bport2, port2)
            sai_thrift_remove_bridge_sub_port(self.client, bport1, port3)
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
        
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port(self.client, bport2, port4)
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


        #pdb.set_trace()
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
        
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port(self.client, bport2, port4)
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
        
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port(self.client, bport2, port4)
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
            
            
            sai_thrift_remove_bridge_sub_port(self.client, bport2, port2)
            
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
            
            
            sai_thrift_remove_bridge_sub_port(self.client, bport2, port2)
            
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
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
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

            
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
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
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
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
        
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
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
        
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
            sai_thrift_remove_bridge_sub_port(self.client, bport2, port4)
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





