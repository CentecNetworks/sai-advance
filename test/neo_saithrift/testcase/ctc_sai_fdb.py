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
Thrift SAI FDB interface tests
"""
import socket
from switch import *
import sai_base_test
import pdb
import time
from scapy.config import *
from scapy.layers.all import *
from ptf.mask import Mask

@group('L2')
class func_01_create_fdb_entry_fn_1q(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)       

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        self.ctc_send_packet(0, str(pkt))
        self.ctc_verify_packets( str(pkt), [1,2], 1)
            
        warmboot(self.client)
        try:
            status = sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
            assert( SAI_STATUS_SUCCESS == status)
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            self.ctc_verify_no_packet(pkt, 2)   
            
        finally:
            status = sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            assert( SAI_STATUS_SUCCESS == status)            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)

        
        
        
        
class func_02_create_fdb_entry_fn_1d_subport(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20    
        vlan_id3 = 30 
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2] 
        
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        sys_logging("###bridge_id1 %d###" %bridge_id1) 
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sys_logging("###sub_port_id1 %d###" %sub_port_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id1, vlan_id3)

        pkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        self.ctc_send_packet(0, str(pkt1))
        self.ctc_verify_packets( str(pkt2), [1], 1)
        self.ctc_verify_packets( str(pkt3), [2], 1)  
           
        warmboot(self.client)
        try:
            type = SAI_FDB_ENTRY_TYPE_STATIC           
            status = sai_thrift_create_fdb_subport(self.client, bridge_id1, mac2, sub_port_id2, mac_action, type)
            assert( SAI_STATUS_SUCCESS == status)   
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            self.ctc_verify_no_packet(pkt3, 2)   

        finally:
            status = sai_thrift_delete_fdb(self.client, bridge_id1, mac2, sub_port_id2)
            assert( SAI_STATUS_SUCCESS == status)
            
            status = sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1) 
            assert( SAI_STATUS_SUCCESS == status)
            
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)            
          
            self.client.sai_thrift_remove_bridge(bridge_id1)  
        
        
        
        
        
    
        
# not support now
#class func_03_create_fdb_entry_fn_tunnel_port(sai_base_test.ThriftInterfaceDataPlane):
#    def runTest(self):
#
#        switch_init(self.client)
#        
#        port0 = port_list[0]
#        port1 = port_list[1]
#        port2 = port_list[2]
#        port3 = port_list[3]
#        
#        v4_enabled = 1
#        v6_enabled = 1
#        
#        mac=router_mac
#        inner_mac_da = '00:00:AA:AA:00:00'
#        inner_mac_sa = '00:00:AA:AA:11:11'
#        
#        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF
#        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI
#        
#        vlan_id = 20
#        vni_id = 1000
#        
#        addr_family = SAI_IP_ADDR_FAMILY_IPV4
#        ip_mask = '255.255.255.0'
#        ip_outer_addr_sa = '30.30.30.30'
#        ip_outer_addr_da = '40.40.40.40'
#        ip_encap_addr_da = '192.168.1.2'
#        ip_decap_addr_da = '192.168.1.1'
#        
#        mac_action = SAI_PACKET_ACTION_FORWARD
#        
#        vr_id = sai_thrift_get_default_router_id(self.client)
#        
#        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
#        
#        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
#        
#        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
#
#        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
#        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
#
#        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, bridge_id)
#        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, bridge_id, vni_id)
#     
#        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
#        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
#        
#        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)
#
#        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_VXLAN)
#      
#        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);
#        
#        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
#
#        type = SAI_FDB_ENTRY_TYPE_STATIC           
#        status = sai_thrift_create_fdb_subport(self.client, bridge_id, inner_mac_da, btunnel_id, mac_action, type)
#        assert( SAI_STATUS_ITEM_NOT_FOUND == status)     
#        
#        status = sai_thrift_create_fdb_tunnel(self.client, bridge_id, inner_mac_da, btunnel_id, mac_action, ip_outer_addr_da)
#        assert( SAI_STATUS_SUCCESS == status)  
#
#        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
#        
#        encap_mac_da = '00:0e:00:0e:00:0e'
#        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
#        
#        sai_thrift_create_fdb_bport(self.client, bridge_id, inner_mac_sa, bport1_id, mac_action)
#        
#
#        pkt1 = simple_tcp_packet(pktlen=100,
#                                eth_dst=inner_mac_da,
#                                eth_src=inner_mac_sa,
#                                dl_vlan_enable=True,
#                                vlan_vid=vlan_id,
#                                vlan_pcp=0,
#                                dl_vlan_cfi=0,
#                                ip_dst=ip_encap_addr_da,
#                                ip_src=ip_decap_addr_da,
#                                ip_id=105,
#                                ip_ttl=64,
#                                ip_ihl=5)
#                                
#        exp_pkt1 = simple_vxlan_packet(pktlen=300,
#                        eth_dst=encap_mac_da,
#                        eth_src=router_mac,
#                        dl_vlan_enable=False,
#                        vlan_vid=0,
#                        vlan_pcp=0,
#                        dl_vlan_cfi=0,
#                        ip_src=ip_outer_addr_sa,
#                        ip_dst=ip_outer_addr_da,
#                        ip_tos=0,
#                        ip_ecn=None,
#                        ip_dscp=None,
#                        ip_ttl=63,
#                        ip_id=0x0000,
#                        ip_flags=0x0,
#                        udp_sport=49180,
#                        udp_dport=4789,
#                        with_udp_chksum=False,
#                        ip_ihl=None,
#                        ip_options=False,
#                        vxlan_reserved1=0x000000,
#                        vxlan_vni = vni_id,
#                        vxlan_reserved2=0x00,
#                        inner_frame = pkt1)
#        m1_exp_pkt1=Mask(exp_pkt1)
#        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
#        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
#        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'chksum')
#        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'sport')
#        inner_pkt2 = simple_tcp_packet(pktlen=100,
#                                eth_dst=inner_mac_sa,
#                                eth_src=inner_mac_da,
#                                dl_vlan_enable=True,
#                                vlan_vid=vlan_id,
#                                vlan_pcp=0,
#                                dl_vlan_cfi=0,
#                                ip_dst=ip_encap_addr_da,
#                                ip_src=ip_decap_addr_da,
#                                ip_id=105,
#                                ip_ttl=64,
#                                ip_ihl=5)
#        pkt2 = simple_vxlan_packet(pktlen=300,
#                        eth_dst=router_mac,
#                        eth_src=encap_mac_da,
#                        dl_vlan_enable=False,
#                        vlan_vid=0,
#                        vlan_pcp=0,
#                        dl_vlan_cfi=0,
#                        ip_src=ip_outer_addr_da,
#                        ip_dst=ip_outer_addr_sa,
#                        ip_tos=0,
#                        ip_ecn=None,
#                        ip_dscp=None,
#                        ip_ttl=63,
#                        ip_id=0x0000,
#                        ip_flags=0x0,
#                        udp_sport=49180,
#                        udp_dport=4789,
#                        with_udp_chksum=False,
#                        ip_ihl=None,
#                        ip_options=False,
#                        vxlan_reserved1=0x000000,
#                        vxlan_vni = vni_id,
#                        vxlan_reserved2=0x00,
#                        inner_frame = inner_pkt2)
#
#        warmboot(self.client)
#        try:
#            self.ctc_send_packet( 1, str(pkt1))
#            self.ctc_verify_packet( m1_exp_pkt1, 2)
#            self.ctc_send_packet( 2, str(pkt2))
#            self.ctc_verify_packet( inner_pkt2, 1)
#        finally:
#            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id)
#            sai_thrift_delete_fdb(self.client, bridge_id, inner_mac_sa, port1)
#            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
#            self.client.sai_thrift_remove_router_interface(rif_encap_id)
#            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)
#            sai_thrift_delete_fdb(self.client, bridge_id, inner_mac_da, tunnel_id)
#            self.client.sai_thrift_remove_bridge_port(btunnel_id)
#            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
#            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
#            self.client.sai_thrift_remove_tunnel(tunnel_id)
#            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
#            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
#            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
#            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
#            self.client.sai_thrift_remove_bridge_port(bport1_id)
#            self.client.sai_thrift_remove_bridge(bridge_id)
#            sai_thrift_create_bridge_port(self.client, port1)
            
        
class func_04_create_same_fdb_entry_fn_1q(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)       

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        self.ctc_send_packet(0, str(pkt))
        self.ctc_verify_packets( str(pkt), [1,2], 1)
            
        warmboot(self.client)
        try:

            status = sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
            assert( SAI_STATUS_SUCCESS == status)
            
            status = sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
            assert( SAI_STATUS_SUCCESS == status)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            self.ctc_verify_no_packet(pkt, 2)   
            
        finally:
        
            status = sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            assert( SAI_STATUS_SUCCESS == status)            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)        
        
        
        
        
        
class func_05_create_error_fdb_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_FORWARD


        not_exist_vlan_oid = 8589934630            
        status = sai_thrift_create_fdb(self.client, not_exist_vlan_oid, mac2, port2, mac_action)
        assert( SAI_STATUS_SUCCESS != status) 
            
        not_exist_bridge_id = 8589942841            
        type = SAI_FDB_ENTRY_TYPE_STATIC           
        status = sai_thrift_create_fdb_subport(self.client, not_exist_bridge_id, mac2, port2, mac_action, type)
        assert( SAI_STATUS_SUCCESS != status)         
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)           
        not_exist_bridge_port = 4294975546            
        type = SAI_FDB_ENTRY_TYPE_STATIC           
        status = sai_thrift_create_fdb_subport(self.client, bridge_id1, mac2, not_exist_bridge_port, mac_action, type)
        assert( SAI_STATUS_SUCCESS != status)         
        
        self.client.sai_thrift_remove_bridge(bridge_id1)
        
        
        
class func_06_remove_fdb_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)       

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
  
        warmboot(self.client)
        try:

            status = sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
            assert( SAI_STATUS_SUCCESS == status)
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            self.ctc_verify_no_packet(pkt, 2)   

            status = sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            assert( SAI_STATUS_SUCCESS == status)                
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1,2], 1)
        
        finally:
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)        
        
        
        
class func_07_remove_not_exist_fdb_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        vlan_id2 = 200
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)       

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
  
        warmboot(self.client)
        try:

            status = sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
            assert( SAI_STATUS_SUCCESS == status)
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            self.ctc_verify_no_packet(pkt, 2)   

            sys_logging("### mac is wrong ###")
            status = sai_thrift_delete_fdb(self.client, vlan_oid, mac3, port2)
            assert( SAI_STATUS_ITEM_NOT_FOUND == status)                
            
            sys_logging("### vlan_oid is wrong ###")
            status = sai_thrift_delete_fdb(self.client, vlan_oid2, mac2, port2)
            assert( SAI_STATUS_ITEM_NOT_FOUND == status)
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            self.ctc_verify_no_packet(pkt, 2)  
        
        finally:
            status = sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            assert( SAI_STATUS_SUCCESS == status) 
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)        
            self.client.sai_thrift_remove_vlan(vlan_oid2)        
        
        
        
        
        
        
class func_08_set_and_get_fdb_entry_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)       

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        status = sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
        assert( SAI_STATUS_SUCCESS == status)
        self.ctc_send_packet(0, str(pkt))
        self.ctc_verify_packets( str(pkt), [1], 1)
        self.ctc_verify_no_packet(pkt, 2) 
            
        warmboot(self.client)
        try:
            
            type = SAI_FDB_ENTRY_TYPE_STATIC
            status = sai_thrift_check_fdb_attribtue_type(self.client, vlan_oid, mac2, type)
            assert( 1 == status) 

            action = SAI_PACKET_ACTION_TRANSIT
            status = sai_thrift_check_fdb_attribtue_action(self.client, vlan_oid, mac2, action)
            assert( 1 == status) 
            
            port = port2
            status = sai_thrift_check_fdb_attribtue_port(self.client, vlan_oid, mac2, port)
            assert( 1 == status) 


            type = SAI_FDB_ENTRY_TYPE_DYNAMIC
            status = sai_thrift_set_fdb_type(self.client, vlan_oid, mac2, type)
            #dynamic cannot rewrite static 
            assert( SAI_STATUS_SUCCESS != status) 

            action = SAI_PACKET_ACTION_LOG
            status = sai_thrift_set_fdb_action(self.client, vlan_oid, mac2, action)
            assert( SAI_STATUS_SUCCESS == status) 
            
            port = port3
            status = sai_thrift_set_fdb_port(self.client, vlan_oid, mac2, port)
            assert( SAI_STATUS_SUCCESS == status)             

            
            type = SAI_FDB_ENTRY_TYPE_STATIC
            status = sai_thrift_check_fdb_attribtue_type(self.client, vlan_oid, mac2, type)
            assert( 1 == status) 

            action = SAI_PACKET_ACTION_LOG
            status = sai_thrift_check_fdb_attribtue_action(self.client, vlan_oid, mac2, action)
            assert( 1 == status) 
            
            port = port3
            status = sai_thrift_check_fdb_attribtue_port(self.client, vlan_oid, mac2, port)
            assert( 1 == status)
            

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [2], 1)
            self.ctc_verify_no_packet(pkt, 1) 
            
        finally:
            status = sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            assert( SAI_STATUS_SUCCESS == status)            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
        
        

        
class func_08_set_and_get_fdb_entry_attribute_fn_metadata(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_TRANSIT
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)       

        status = sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
        assert( SAI_STATUS_SUCCESS == status)
            
        warmboot(self.client)
        try:
            
            fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac2, bv_id=vlan_oid)          
            fdb_attr_list = self.client.sai_thrift_get_fdb_entry_attribute(fdb_entry)
            attr_list = fdb_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_FDB_ENTRY_ATTR_META_DATA:
                    assert ( 0 == attribute.value.u32 )
            
            metadata = 253
            fdb_attribute_value = sai_thrift_attribute_value_t(u32=metadata)
            fdb_attribute = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_META_DATA,value=fdb_attribute_value)
            self.client.sai_thrift_set_fdb_entry_attribute(thrift_fdb_entry=fdb_entry, thrift_attr=fdb_attribute)

            fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac2, bv_id=vlan_oid)          
            fdb_attr_list = self.client.sai_thrift_get_fdb_entry_attribute(fdb_entry)
            attr_list = fdb_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_FDB_ENTRY_ATTR_META_DATA:
                    assert ( metadata == attribute.value.u32 )    
            
        finally:
            status = sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            assert( SAI_STATUS_SUCCESS == status)            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)


            
            
class func_09_flush_fdb_entry_fn_01_by_portid(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_TRANSIT
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)       

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        self.ctc_send_packet(0, str(pkt))
        self.ctc_verify_packets( str(pkt), [1,2], 1)
            
        warmboot(self.client)
        try:
        
            type = SAI_FDB_ENTRY_TYPE_DYNAMIC
            
            status = sai_thrift_create_fdb_new(self.client, vlan_oid, mac2, port2, mac_action, type)
            assert( SAI_STATUS_SUCCESS == status)
            status = sai_thrift_create_fdb_new(self.client, vlan_oid, mac3, port3, mac_action, type)
            assert( SAI_STATUS_SUCCESS == status)            
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            self.ctc_verify_no_packet(pkt, 2)   

            fdb_attr_list = []
            bport_id = sai_thrift_get_bridge_port_by_port(self.client, port2)           
            fdb_attribute1_value = sai_thrift_attribute_value_t(oid=bport_id)
            fdb_attribute1 = sai_thrift_attribute_t(id=SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID, value=fdb_attribute1_value)
            fdb_attr_list.append(fdb_attribute1)
            
            status = self.client.sai_thrift_flush_fdb_entries(fdb_attr_list)
            assert( SAI_STATUS_SUCCESS == status)    
            
            status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac2)
            assert( 0 == status) 

            status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac3)
            assert( 1 == status) 
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1,2], 1)
            
        finally:  
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)



class func_09_flush_fdb_entry_fn_02_by_vlanid(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        vlan_id1 = 200
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_TRANSIT
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)       

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        self.ctc_send_packet(0, str(pkt))
        self.ctc_verify_packets( str(pkt), [1,2], 1)
            
        warmboot(self.client)
        try:
        
            type = SAI_FDB_ENTRY_TYPE_DYNAMIC
            
            status = sai_thrift_create_fdb_new(self.client, vlan_oid, mac2, port2, mac_action, type)
            assert( SAI_STATUS_SUCCESS == status)
            status = sai_thrift_create_fdb_new(self.client, vlan_oid1, mac2, port2, mac_action, type)
            assert( SAI_STATUS_SUCCESS == status)            
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            self.ctc_verify_no_packet(pkt, 2)   

            fdb_attr_list = []       
            fdb_attribute1_value = sai_thrift_attribute_value_t(oid=vlan_oid)
            fdb_attribute1 = sai_thrift_attribute_t(id=SAI_FDB_FLUSH_ATTR_BV_ID, value=fdb_attribute1_value)
            fdb_attr_list.append(fdb_attribute1)
            
            status = self.client.sai_thrift_flush_fdb_entries(fdb_attr_list)
            assert( SAI_STATUS_SUCCESS == status)    
            
            status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac2)
            assert( 0 == status) 

            status = sai_thrift_check_fdb_exist(self.client, vlan_oid1, mac2)
            assert( 1 == status) 
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1,2], 1)
            
        finally:  
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid1)





class func_09_flush_fdb_entry_fn_03_by_entry_type(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        vlan_id1 = 200
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_TRANSIT
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)       

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        self.ctc_send_packet(0, str(pkt))
        self.ctc_verify_packets( str(pkt), [1,2], 1)
            
        warmboot(self.client)
        try:
        
            type = SAI_FDB_ENTRY_TYPE_DYNAMIC            
            status = sai_thrift_create_fdb_new(self.client, vlan_oid, mac2, port2, mac_action, type)
            assert( SAI_STATUS_SUCCESS == status)
            
            type = SAI_FDB_ENTRY_TYPE_STATIC 
            status = sai_thrift_create_fdb_new(self.client, vlan_oid1, mac2, port2, mac_action, type)
            assert( SAI_STATUS_SUCCESS == status)            
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            self.ctc_verify_no_packet(pkt, 2)   

            fdb_attr_list = []       
            fdb_attribute1_value = sai_thrift_attribute_value_t(s32=SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC)
            fdb_attribute1 = sai_thrift_attribute_t(id=SAI_FDB_FLUSH_ATTR_ENTRY_TYPE, value=fdb_attribute1_value)
            fdb_attr_list.append(fdb_attribute1)
            
            status = self.client.sai_thrift_flush_fdb_entries(fdb_attr_list)
            assert( SAI_STATUS_SUCCESS == status)    
            
            status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac2)
            assert( 0 == status) 

            status = sai_thrift_check_fdb_exist(self.client, vlan_oid1, mac2)
            assert( 1 == status) 
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1,2], 1)

            fdb_attr_list = []       
            fdb_attribute1_value = sai_thrift_attribute_value_t(s32=SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            fdb_attribute1 = sai_thrift_attribute_t(id=SAI_FDB_FLUSH_ATTR_ENTRY_TYPE, value=fdb_attribute1_value)
            fdb_attr_list.append(fdb_attribute1)
            
            status = self.client.sai_thrift_flush_fdb_entries(fdb_attr_list)
            status = sai_thrift_check_fdb_exist(self.client, vlan_oid1, mac2)
            assert( 0 == status) 
            
        finally:  
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
                     
      





class scenario_01_fdb_learning_and_aging_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)       

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        self.ctc_send_packet(0, str(pkt))
        self.ctc_verify_packets( str(pkt), [1,2], 1)
            
        warmboot(self.client)
        try:
            
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1)
            assert( 1 == status)

            fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac1, bv_id=vlan_oid)
            bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        
            fdb_attr_list = self.client.sai_thrift_get_fdb_entry_attribute(fdb_entry)
            attr_list = fdb_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID:
                    assert( bport_oid == attribute.value.oid)
            
            #uml do not test
            #time.sleep(310)
            #sys_logging("###fdb aging###")
            #status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1)
            #assert( 0 == status)
            
        finally:         
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)




class scenario_02_fdb_learning_and_aging_sub_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20    
        vlan_id3 = 30 
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2] 
        
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        sys_logging("###bridge_id1 %d###" %bridge_id1) 
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sys_logging("###sub_port_id1 %d###" %sub_port_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id1, vlan_id3)

        pkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        self.ctc_send_packet(0, str(pkt1))
        self.ctc_verify_packets( str(pkt2), [1], 1)
        self.ctc_verify_packets( str(pkt3), [2], 1)  
           
        warmboot(self.client)
        try:
        
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1)
            assert( 1 == status)

            fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac1, bv_id=bridge_id1)
            subport_oid = sai_thrift_get_bridge_port_by_sub_port(self.client, port1, vlan_id1, bridge_id1)
        
            fdb_attr_list = self.client.sai_thrift_get_fdb_entry_attribute(fdb_entry)
            attr_list = fdb_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID:
                    assert( subport_oid == attribute.value.oid)

            #uml do not test
            #time.sleep(310)
            #sys_logging("###fdb aging###")
            #status = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1)
            #assert( 0 == status)
            
        finally:
        
            fdb_attr_list = []       
            fdb_attribute1_value = sai_thrift_attribute_value_t(s32=SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC)
            fdb_attribute1 = sai_thrift_attribute_t(id=SAI_FDB_FLUSH_ATTR_ENTRY_TYPE, value=fdb_attribute1_value)
            fdb_attr_list.append(fdb_attribute1)
            
            status = self.client.sai_thrift_flush_fdb_entries(fdb_attr_list)
            assert( SAI_STATUS_SUCCESS == status) 
            
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)            
          
            self.client.sai_thrift_remove_bridge(bridge_id1)  




# not support now
#class scenario_03_fdb_learning_and_aging_tunnel_port(sai_base_test.ThriftInterfaceDataPlane):
#    def runTest(self):
#
#        switch_init(self.client)
#        
#        port0 = port_list[0]
#        port1 = port_list[1]
#        port2 = port_list[2]
#        port3 = port_list[3]
#        
#        v4_enabled = 1
#        v6_enabled = 1
#        
#        mac=router_mac
#        inner_mac_da = '00:00:00:00:00:01'
#        inner_mac_sa = '00:00:00:00:00:02'
#        
#        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF
#        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI
#        
#        vlan_id = 20
#        vni_id = 1000
#        
#        addr_family = SAI_IP_ADDR_FAMILY_IPV4
#        ip_mask = '255.255.255.0'
#        ip_outer_addr_sa = '30.30.30.30'
#        ip_outer_addr_da = '40.40.40.40'
#        ip_encap_addr_da = '192.168.1.2'
#        ip_decap_addr_da = '192.168.1.1'
#        
#        mac_action = SAI_PACKET_ACTION_FORWARD
#        
#        vr_id = sai_thrift_get_default_router_id(self.client)
#        
#        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
#        
#        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
#        
#        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
#
#        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
#        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
#
#        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, bridge_id)
#        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, bridge_id, vni_id)
#     
#        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
#        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
#        
#        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)
#
#        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_VXLAN)
#      
#        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);
#        
#        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
#        
#        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
#        
#        encap_mac_da = '00:0e:00:0e:00:0e'
#        
#        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
#        
#        type = SAI_FDB_ENTRY_TYPE_STATIC           
#        status = sai_thrift_create_fdb_subport(self.client, bridge_id, inner_mac_sa, bport1_id, mac_action, type)
#        assert( SAI_STATUS_SUCCESS == status) 
#        
#        inner_pkt2 = simple_tcp_packet(pktlen=100,
#                                eth_dst=inner_mac_sa,
#                                eth_src=inner_mac_da,
#                                dl_vlan_enable=True,
#                                vlan_vid=vlan_id,
#                                vlan_pcp=0,
#                                dl_vlan_cfi=0,
#                                ip_dst=ip_encap_addr_da,
#                                ip_src=ip_decap_addr_da,
#                                ip_id=105,
#                                ip_ttl=64,
#                                ip_ihl=5)
#        pkt2 = simple_vxlan_packet(pktlen=300,
#                        eth_dst=router_mac,
#                        eth_src=encap_mac_da,
#                        dl_vlan_enable=False,
#                        vlan_vid=0,
#                        vlan_pcp=0,
#                        dl_vlan_cfi=0,
#                        ip_src=ip_outer_addr_da,
#                        ip_dst=ip_outer_addr_sa,
#                        ip_tos=0,
#                        ip_ecn=None,
#                        ip_dscp=None,
#                        ip_ttl=63,
#                        ip_id=0x0000,
#                        ip_flags=0x0,
#                        udp_sport=49180,
#                        udp_dport=4789,
#                        with_udp_chksum=False,
#                        ip_ihl=None,
#                        ip_options=False,
#                        vxlan_reserved1=0x000000,
#                        vxlan_vni = vni_id,
#                        vxlan_reserved2=0x00,
#                        inner_frame = inner_pkt2)
#
#        warmboot(self.client)
#        try:
#        
#            self.ctc_send_packet( 2, str(pkt2))
#            self.ctc_verify_packet( inner_pkt2, 1)
#            
#            sys_logging("###fdb learning###")
#            status = sai_thrift_check_fdb_exist(self.client, bridge_id, inner_mac_da)
#            assert( 1 == status)
#
#            fdb_entry = sai_thrift_fdb_entry_t(mac_address=inner_mac_da, bv_id=bridge_id)
#       
#            fdb_attr_list = self.client.sai_thrift_get_fdb_entry_attribute(fdb_entry)
#            attr_list = fdb_attr_list.attr_list
#            for attribute in attr_list:
#                if attribute.id == SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID:
#                    sys_logging("### btunnel_id %d ###" %btunnel_id)
#                    sys_logging("### attribute.value.oid %d ###" %attribute.value.oid)
#                    assert( btunnel_id == attribute.value.oid)
#
#            #uml do not test
#            #time.sleep(310)
#            #sys_logging("###fdb aging###")
#            #status = sai_thrift_check_fdb_exist(self.client, bridge_id, inner_mac_da)
#            #assert( 0 == status)            
#            
#                
#        finally:
#            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id)
#            sai_thrift_delete_fdb(self.client, bridge_id, inner_mac_sa, port1)
#            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
#            self.client.sai_thrift_remove_router_interface(rif_encap_id)
#            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)
#            sai_thrift_delete_fdb(self.client, bridge_id, inner_mac_da, tunnel_id)
#            self.client.sai_thrift_remove_bridge_port(btunnel_id)
#            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
#            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
#            self.client.sai_thrift_remove_tunnel(tunnel_id)
#            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
#            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
#            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
#            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
#            self.client.sai_thrift_remove_bridge_port(bport1_id)
#            self.client.sai_thrift_remove_bridge(bridge_id)
#            sai_thrift_create_bridge_port(self.client, port1)
 




            
class scenario_04_fdb_fdb_station_move(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        v4_enabled = 1
        v6_enabled = 1
        
        vlan_id = 10
        rmac = '00:00:00:00:00:01'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, rmac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, rmac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)


        pkt = simple_tcp_packet(eth_dst=rmac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=rmac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet(exp_pkt, 1)

            sai_thrift_create_fdb(self.client, vlan_oid, dmac1, port2, SAI_PACKET_ACTION_FORWARD)
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)
            
            port = port3
            status = sai_thrift_set_fdb_port(self.client, vlan_oid, dmac1, port)
            assert( SAI_STATUS_SUCCESS == status) 
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packet( exp_pkt, 2)

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, dmac1, port)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  




            

class scenario_05_fdb_fdb_entry_cover_01(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)       

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
        self.ctc_send_packet(0, str(pkt))
        self.ctc_verify_packets( str(pkt), [1,2], 1)
            
        warmboot(self.client)
        try:
            
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1)
            assert( 1 == status)

            bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
            
            fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac1, bv_id=vlan_oid)          
            fdb_attr_list = self.client.sai_thrift_get_fdb_entry_attribute(fdb_entry)
            attr_list = fdb_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID:
                    assert( bport_oid == attribute.value.oid)
            
            sys_logging("### send packet for test ###") 
            self.ctc_send_packet(2, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [0], 1)
            
            sys_logging("###create static fdb entry cover dynamic fdb entry###")                    
            status = sai_thrift_create_fdb(self.client, vlan_oid, mac1, port2, mac_action)
            assert( SAI_STATUS_SUCCESS == status)

            status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1)
            assert( 1 == status)

            bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
            
            fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac1, bv_id=vlan_oid)          
            fdb_attr_list = self.client.sai_thrift_get_fdb_entry_attribute(fdb_entry)
            attr_list = fdb_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID:
                    assert( bport_oid == attribute.value.oid)

            sys_logging("### send packet for test ###") 
            self.ctc_send_packet(2, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
                    
        finally:   
            status = sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port2)
            assert( SAI_STATUS_SUCCESS == status)          
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)
 


class scenario_05_fdb_fdb_entry_cover_02(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                       
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20    
        vlan_id3 = 30 
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2] 
        
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        sys_logging("###bridge_id1 %d###" %bridge_id1) 
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sys_logging("###sub_port_id1 %d###" %sub_port_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id1, vlan_id3)

        pkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt4 = simple_tcp_packet(eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt5 = simple_tcp_packet(eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        pkt6 = simple_tcp_packet(eth_dst=mac1,
                                eth_src=mac2,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        self.ctc_send_packet(0, str(pkt1))
        self.ctc_verify_packets( str(pkt2), [1], 1)
        self.ctc_verify_packets( str(pkt3), [2], 1)  
           
        warmboot(self.client)
        try:
        
            sys_logging("###fdb learning###")
            status = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1)
            assert( 1 == status)

            fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac1, bv_id=bridge_id1)
            subport_oid = sai_thrift_get_bridge_port_by_sub_port(self.client, port1, vlan_id1, bridge_id1)
        
            fdb_attr_list = self.client.sai_thrift_get_fdb_entry_attribute(fdb_entry)
            attr_list = fdb_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID:
                    assert( subport_oid == attribute.value.oid)

            sys_logging("### send packet for test ###") 
            self.ctc_send_packet(2, str(pkt4))
            self.ctc_verify_packets( str(pkt5), [0], 1)
            
            sys_logging("###create static fdb entry cover dynamic fdb entry###")                    
        
            type = SAI_FDB_ENTRY_TYPE_STATIC           
            status = sai_thrift_create_fdb_subport(self.client, bridge_id1, mac1, sub_port_id2, mac_action, type)
            assert( SAI_STATUS_SUCCESS == status)   
            
            fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac1, bv_id=bridge_id1)
       
            fdb_attr_list = self.client.sai_thrift_get_fdb_entry_attribute(fdb_entry)
            attr_list = fdb_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID:
                    assert( sub_port_id2 == attribute.value.oid)

            sys_logging("### send packet for test ###") 
            self.ctc_send_packet(2, str(pkt4))
            self.ctc_verify_packets( str(pkt6), [1], 1)            
            
        finally:
            
            status = sai_thrift_delete_fdb(self.client, bridge_id1, mac1, sub_port_id2)
            assert( SAI_STATUS_SUCCESS == status)
        
            fdb_attr_list = []       
            fdb_attribute1_value = sai_thrift_attribute_value_t(s32=SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC)
            fdb_attribute1 = sai_thrift_attribute_t(id=SAI_FDB_FLUSH_ATTR_ENTRY_TYPE, value=fdb_attribute1_value)
            fdb_attr_list.append(fdb_attribute1)
            
            status = self.client.sai_thrift_flush_fdb_entries(fdb_attr_list)
            assert( SAI_STATUS_SUCCESS == status) 
            
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)            
        
            self.client.sai_thrift_remove_bridge(bridge_id1)


class scenario_06_L2AccessTohybridVlanTest(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id2)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
	
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id3)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac4, port3, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)
                                
        warmboot(self.client)
        try:
            sys_logging ("Sending L2 packet port 1 -> port 3 [access vlan=10]), packet from port3 without vlan")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(pkt, [2])
            sys_logging ("Sending L2 packet port 2 -> port 3 [access vlan=20]) packet from port3 with vlan 20")
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(exp_pkt1, [2])
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac4, port3)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)


class scenario_07_L2TrunkTohybridVlanTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        port1 = port_list[0]
        port2 = port_list[1]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member5 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member6 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id3)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)


        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid3, mac2, port2, mac_action)

        pkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=96)
        pkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=100)
        
        pkt3 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        pkt4 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='30.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='30.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=96)
                                
        
        warmboot(self.client)
        try:
            sys_logging ("Sending L2 packet port 1 -> port 2 [without vlan]), packet from port2 with vlan 10")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt2, [1])
            
            sys_logging ("Sending L2 packet port 1 -> port 2 [with vlan 10]) packet from port2 with vlan 10")
            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_packets(pkt2, [1])
            
            sys_logging ("Sending L2 packet port 1 -> port 2 [with vlan 20]) packet from port2 with  vlan 20")
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets(pkt3, [1])
            
            sys_logging ("Sending L2 packet port 1 -> port 2 [with vlan 30]) packet from port2 without vlan")
            self.ctc_send_packet(0, str(pkt4))
            self.ctc_verify_packets(exp_pkt1, [1])
        finally:
            
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid3)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid3, mac2, port2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan_member(vlan_member5)
            self.client.sai_thrift_remove_vlan_member(vlan_member6)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)


class scenario_08_L2FlushStatic(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        fdb_entry_type  = SAI_FDB_FLUSH_ENTRY_TYPE_STATIC

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=107,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=107,
                                ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='10.0.0.1',
                                ip_id=107,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='10.0.0.1',
                                ip_id=107,
                                ip_ttl=64)

        
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            sai_thrift_flush_fdb(self.client, SAI_NULL_OBJECT_ID, SAI_NULL_OBJECT_ID, fdb_entry_type)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1, 2])
            
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [0])
            self.ctc_verify_no_packet( exp_pkt1, 2)
        finally:
            sys_logging ("show fdb entry") 
            time.sleep(5)
            sai_thrift_flush_fdb(self.client, SAI_NULL_OBJECT_ID, SAI_NULL_OBJECT_ID, SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            sai_thrift_flush_fdb(self.client, SAI_NULL_OBJECT_ID, SAI_NULL_OBJECT_ID, SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_09_L2FlushDynamic(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        fdb_entry_type  = SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)


        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=107,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=107,
                                ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='10.0.0.2',
                                ip_id=107,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='10.0.0.2',
                                ip_id=107,
                                ip_ttl=64)

        sys_logging ("start send packet")
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [0])
            sys_logging ("flush dynamic fdb entry")
            sai_thrift_flush_fdb(self.client, SAI_NULL_OBJECT_ID, SAI_NULL_OBJECT_ID, fdb_entry_type)
            
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [0,2])
        finally:
            sys_logging ("show fdb entry") 
            time.sleep(5)
            sai_thrift_flush_fdb(self.client, SAI_NULL_OBJECT_ID, SAI_NULL_OBJECT_ID, SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            sai_thrift_flush_fdb(self.client, SAI_NULL_OBJECT_ID, SAI_NULL_OBJECT_ID, SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)

            

class scenario_10_L2FdbGetSetEntryTypeDynamicToStatic(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac_action = SAI_PACKET_ACTION_FORWARD
        

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb_new(self.client, vlan_oid, mac2, port2, mac_action, SAI_FDB_ENTRY_TYPE_DYNAMIC)
        result = sai_thrift_check_fdb_attribtue_type(self.client, vlan_oid, mac2, SAI_FDB_ENTRY_TYPE_DYNAMIC)
        
        if(1 == result):
            sys_logging ("fdb entry type is right")
        else:
            sys_logging ("fdb entry type is wrong")
        assert(1 == result)
        
        sai_thrift_set_fdb_type(self.client, vlan_oid, mac2,  SAI_FDB_ENTRY_TYPE_STATIC)
        result = sai_thrift_check_fdb_attribtue_type(self.client, vlan_oid, mac2, SAI_FDB_ENTRY_TYPE_STATIC)
        if(1 == result):
            sys_logging ("fdb entry type is right")
        else:
            sys_logging ("fdb entry type is wrong")
        assert(1 == result)
        pkt = simple_tcp_packet(eth_dst= mac2,
                                eth_src= mac1,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_11_L2FdbGetSetEntryActionTransitToTrap(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        result = 0;
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac_action = SAI_PACKET_ACTION_TRANSIT

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb_new(self.client, vlan_oid, mac2, port2, mac_action, SAI_FDB_ENTRY_TYPE_STATIC)
        result = sai_thrift_check_fdb_attribtue_action(self.client, vlan_oid, mac2, SAI_PACKET_ACTION_TRANSIT)
        
        if(1 == result):
            sys_logging ("fdb entry action is right")
        else:
            sys_logging ("fdb entry action is wrong")

        assert(1 == result)

        pkt = simple_tcp_packet(eth_dst= mac2,
                                eth_src= mac1,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)

        
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
        finally:
            sys_logging ("modify action from transit to trap")

        sai_thrift_set_fdb_action(self.client, vlan_oid, mac2, SAI_PACKET_ACTION_TRAP)
        result = sai_thrift_check_fdb_attribtue_action(self.client, vlan_oid, mac2, SAI_PACKET_ACTION_TRAP)
      
        if(1 == result):
            sys_logging ("fdb entry action is right")
        else:
            sys_logging ("fdb entry action is wrong")
        assert(1 == result)

        
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet(exp_pkt, 1)
            sys_logging ("TODO")
            """
            TODO:check packet passed to cpu
            """
        finally:
            sys_logging ("=====test done======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)



class scenario_12_L2FdbGetSetEntryActionTransitToLog(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        result = 0;
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac_action = SAI_PACKET_ACTION_TRANSIT

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb_new(self.client, vlan_oid, mac2, port2, mac_action, SAI_FDB_ENTRY_TYPE_STATIC)
        result = sai_thrift_check_fdb_attribtue_action(self.client, vlan_oid, mac2, SAI_PACKET_ACTION_TRANSIT)
        
        if(1 == result):
            sys_logging ("fdb entry action is right")
        else:
            sys_logging ("fdb entry action is wrong")
        assert(1 == result)
        

        pkt = simple_tcp_packet(eth_dst= mac2,
                                eth_src= mac1,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
        finally:
            sys_logging ("modify action from transit to log")

        sai_thrift_set_fdb_action(self.client, vlan_oid, mac2,  SAI_PACKET_ACTION_LOG)
        result = sai_thrift_check_fdb_attribtue_action(self.client, vlan_oid, mac2, SAI_PACKET_ACTION_LOG)
      
        if(1 == result):
            sys_logging ("fdb entry action is right")
        else:
            sys_logging ("fdb entry action is wrong")
        assert(1 == result)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            """
            TODO:check packet passed to cpu
            """
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_13_L2FdbGetSetEntryActionTransitToDeny(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        result = 0;
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac_action = SAI_PACKET_ACTION_TRANSIT

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb_new(self.client, vlan_oid, mac2, port2, mac_action, SAI_FDB_ENTRY_TYPE_STATIC)
        result = sai_thrift_check_fdb_attribtue_action(self.client, vlan_oid, mac2, SAI_PACKET_ACTION_TRANSIT)
        
        if(1 == result):
            sys_logging ("fdb entry action is right")
        else:
            sys_logging ("fdb entry action is wrong")
        assert(1 == result)
        

        pkt = simple_tcp_packet(eth_dst= mac2,
                                eth_src= mac1,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
        finally:
            sys_logging ("modify action from transit to deny")

        sai_thrift_set_fdb_action(self.client, vlan_oid, mac2, SAI_PACKET_ACTION_DENY)
        result = sai_thrift_check_fdb_attribtue_action(self.client, vlan_oid, mac2, SAI_PACKET_ACTION_DENY)
      
        if(1 == result):
            sys_logging ("fdb entry action is right")
        else:
            sys_logging ("fdb entry action is wrong")
        assert(1 == result)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1, default_time_out)
            """
            TODO:check packet not passed to cpu
            """
        finally:
           
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_14_L2FdbGetSetEntryActionLogToDeny(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        result = 0;
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb_new(self.client, vlan_oid, mac2, port2, SAI_PACKET_ACTION_LOG, SAI_FDB_ENTRY_TYPE_STATIC)
        result = sai_thrift_check_fdb_attribtue_action(self.client, vlan_oid, mac2, SAI_PACKET_ACTION_LOG)
        
        if(1 == result):
            sys_logging ("fdb entry action is right")
        else:
            sys_logging ("fdb entry action is wrong")
        assert(1 == result)
        

        pkt = simple_tcp_packet(eth_dst= mac2,
                                eth_src= mac1,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            """
            TODO:check packet passed to cpu
            """
            
        finally:
            sys_logging ("modify action from log to deny")

        sai_thrift_set_fdb_action(self.client, vlan_oid, mac2,  SAI_PACKET_ACTION_DENY)
        result = sai_thrift_check_fdb_attribtue_action(self.client, vlan_oid, mac2, SAI_PACKET_ACTION_DENY)
      
        if(1 == result):
            sys_logging ("fdb entry action is right")
        else:
            sys_logging ("fdb entry action is wrong")
        assert(1 == result)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet( exp_pkt, 1, default_time_out)
            """
            TODO:check packet not passed to cpu
            """
        finally:
           
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_15_L2FdbGetSetEntryPort(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        result = 0;
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac_action = SAI_PACKET_ACTION_TRANSIT

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb_new(self.client, vlan_oid, mac2, port2, mac_action, SAI_FDB_ENTRY_TYPE_STATIC)
        result = sai_thrift_check_fdb_attribtue_port(self.client, vlan_oid, mac2, port2)
        
        if(1 == result):
            sys_logging ("fdb entry port is right")
        else:
            sys_logging ("fdb entry port is wrong")
        assert(1 == result)
        

        pkt = simple_tcp_packet(eth_dst= mac2,
                                eth_src= mac1,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
        finally:
            sys_logging ("modify port from port2 to port3")

        sai_thrift_set_fdb_port(self.client, vlan_oid, mac2, port3)
        result = sai_thrift_check_fdb_attribtue_port(self.client, vlan_oid, mac2, port3)
      
        if(1 == result):
            sys_logging ("fdb entry port is right")
        else:
            sys_logging ("fdb entry port is wrong")
        assert(1 == result)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [2])
        finally:
           
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port3)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)



class scenario_16_L2VlanGetSetMaxLearnedAddress(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        vlan_id = 10
        limit_num = 1
        result = 0
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging ("vlan_oid:%x" %vlan_oid)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        
        attr_value = sai_thrift_attribute_value_t(u32=limit_num)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        result = sai_thrift_vlan_check_max_learned_address(self.client, vlan_oid, limit_num)
        assert(1 == result)
        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=107,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=107,
                                ip_ttl=64)

        pkt1 = simple_tcp_packet(eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='10.0.0.2',
                                ip_id=107,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='10.0.0.2',
                                ip_id=107,
                                ip_ttl=64)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1, 2])
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [0])
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(1 == result)

            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(0 == result)
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1, 2])
        finally:
            
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)

           
class scenario_18_L2PortTransmitPropertyTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id2)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
	
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id3)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac4, port3, mac_action)
                                
        warmboot(self.client)
        try:
            list = self.client.sai_thrift_get_port_attribute(port1)
            for each in list.attr_list:
                if each.id == SAI_PORT_ATTR_PKT_TX_ENABLE:
                    sys_logging ("SAI_PORT_ATTR_PKT_TX_ENABLE: %s" % ("Ture" if each.value.booldata else "False"))
                    assert (each.value.booldata == True)
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PKT_TX_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            list = self.client.sai_thrift_get_port_attribute(port1)
            for each in list.attr_list:
                if each.id == SAI_PORT_ATTR_PKT_TX_ENABLE:
                    sys_logging ("SAI_PORT_ATTR_PKT_TX_ENABLE: %s" % ("Ture" if each.value.booldata else "False"))
                    assert (each.value.booldata == False)
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PKT_TX_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            list = self.client.sai_thrift_get_port_attribute(port1)
            for each in list.attr_list:
                if each.id == SAI_PORT_ATTR_PKT_TX_ENABLE:
                    sys_logging ("SAI_PORT_ATTR_PKT_TX_ENABLE: %s" % ("Ture" if each.value.booldata else "False"))
                    assert (each.value.booldata == True)
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac4, port3)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            

class scenario_19_L2IsolationGroupTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        vlan_id1 = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac3, port3, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=68)
        pkt1 = simple_tcp_packet(eth_dst=mac3,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='20.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=68)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac3,
                                eth_src=mac1,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
                                
        warmboot(self.client)
        try:
            sys_logging ("Sending L2 packet port 1 -> port 2 [access vlan=10]), packet from port2 with vlan 10")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( pkt, [1])
            sys_logging ("Sending L2 packet port 1 -> port 3 [access vlan=10]) packet from port3 with vlan 10")
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [2])
        finally:
            pass
            
        # set isolation group
        isolation_group_oid = sai_thrift_create_isolation_group(self.client, type = SAI_ISOLATION_GROUP_TYPE_PORT)
        isolation_group_member_oid1 = sai_thrift_create_isolation_group_member(self.client, isolation_group_oid, port2)
        isolation_group_member_oid2 = sai_thrift_create_isolation_group_member(self.client, isolation_group_oid, port3)
        
        bp = sai_thrift_get_bridge_port_by_port(self.client, port1)
        attr_value = sai_thrift_attribute_value_t(oid=isolation_group_oid)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(bp, attr)

        warmboot(self.client)
        try:
            sys_logging ("Sending L2 packet port 1 -> port 2 [access vlan=10]), no packet received")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet( exp_pkt1, 1)
            sys_logging ("Sending L2 packet port 1 -> port 3 [access vlan=10]) no packet received")
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_no_packet( exp_pkt1, 2)
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac3, port3)            
            sai_thrift_remove_isolation_group_member(self.client, isolation_group_member_oid1)
            sai_thrift_remove_isolation_group_member(self.client, isolation_group_member_oid2)
            sai_thrift_remove_isolation_group(self.client, isolation_group_oid)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
        
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid1)


class scenario_20_L2IsolationGroupGetGroupAttributesTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        vlan_id1 = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac3, port3, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=68)
        pkt1 = simple_tcp_packet(eth_dst=mac3,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='20.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=68)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac3,
                                eth_src=mac1,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
                                
        warmboot(self.client)
        try:
            sys_logging ("Sending L2 packet port 1 -> port 2 [access vlan=10]), packet from port2 with vlan 10")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( pkt, [1])
            sys_logging ("Sending L2 packet port 1 -> port 3 [access vlan=10]) packet from port3 with vlan 10")
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [2])
        finally:
            pass
            
        # set isolation group
        
        isolation_group_oid = sai_thrift_create_isolation_group(self.client, type = SAI_ISOLATION_GROUP_TYPE_PORT)
        isolation_group_member_oid1 = sai_thrift_create_isolation_group_member(self.client, isolation_group_oid, port2)
        isolation_group_member_oid2 = sai_thrift_create_isolation_group_member(self.client, isolation_group_oid, port3)
        attr_list = sai_thrift_get_isolation_group_attributes(self.client, isolation_group_oid)
        
        bp = sai_thrift_get_bridge_port_by_port(self.client, port1)
        attr_value = sai_thrift_attribute_value_t(oid=isolation_group_oid)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(bp, attr)
        
        warmboot(self.client)
        try:
            for i in attr_list.attr_list:
                if i.id == SAI_ISOLATION_GROUP_ATTR_TYPE:
                    assert(i.value.s32 == SAI_ISOLATION_GROUP_TYPE_PORT)
                if i.id == SAI_ISOLATION_GROUP_ATTR_ISOLATION_MEMBER_LIST:
                    assert(isolation_group_member_oid1 in i.value.objlist.object_id_list)
                    assert(isolation_group_member_oid2 in i.value.objlist.object_id_list)
            sys_logging ("Sending L2 packet port 1 -> port 2 [access vlan=10]), no packet received")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet( exp_pkt1, 1)
            sys_logging ("Sending L2 packet port 1 -> port 3 [access vlan=10]) no packet received")
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_no_packet( exp_pkt1, 2)
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac3, port3)
            sai_thrift_remove_isolation_group_member(self.client, isolation_group_member_oid1)
            sai_thrift_remove_isolation_group_member(self.client, isolation_group_member_oid2)
            sai_thrift_remove_isolation_group(self.client, isolation_group_oid)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
        
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            

class scenario_21_L2IsolationGroupGetMemberAttributesTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        vlan_id1 = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac3, port3, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=68)
        pkt1 = simple_tcp_packet(eth_dst=mac3,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='20.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=68)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac3,
                                eth_src=mac1,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
                                
        warmboot(self.client)
        try:
            sys_logging ("Sending L2 packet port 1 -> port 2 [access vlan=10]), packet from port2 with vlan 10")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( pkt, [1])
            sys_logging ("Sending L2 packet port 1 -> port 3 [access vlan=10]) packet from port3 with vlan 10")
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [2])
        finally:
            pass
        # set isolation group

        isolation_group_oid = sai_thrift_create_isolation_group(self.client, type = SAI_ISOLATION_GROUP_TYPE_PORT)
        isolation_group_member_oid1 = sai_thrift_create_isolation_group_member(self.client, isolation_group_oid, port2)
        isolation_group_member_oid2 = sai_thrift_create_isolation_group_member(self.client, isolation_group_oid, port3)
               
        attr_list = sai_thrift_get_isolation_group_member_attributes(self.client, isolation_group_member_oid1)
        warmboot(self.client)
        try:
            for i in attr_list.attr_list:
                if i.id == SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_GROUP_ID:
                    assert(i.value.oid == isolation_group_oid)
                if i.id == SAI_ISOLATION_GROUP_MEMBER_ATTR_ISOLATION_OBJECT:
                    assert(port2 == i.value.oid)
        finally:
            pass

        # remove isolation member
        sai_thrift_remove_isolation_group_member(self.client, isolation_group_member_oid1)
        sai_thrift_remove_isolation_group_member(self.client, isolation_group_member_oid2)
        warmboot(self.client)
        try:
            sys_logging ("Sending L2 packet port 1 -> port 2 [access vlan=10]), packet from port2 with vlan 10")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( pkt, [1])
            sys_logging ("Sending L2 packet port 1 -> port 3 [access vlan=10]) packet from port3 with vlan 10")
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [2])
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac3, port3)
            
            sai_thrift_remove_isolation_group(self.client, isolation_group_oid)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid1)



class scenario_22_normal_bridge_port_is_lag(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        mac4 = '00:33:33:33:33:34'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        lag_oid = sai_thrift_create_lag(self.client)
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
                
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        is_lag = 1
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_UNTAGGED,is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)        

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_oid, attr)

        is_lag = 1
        sai_thrift_create_fdb(self.client, vlan_oid, mac1, lag_bridge_oid, mac_action,is_lag)
        
        warmboot(self.client)
        
        try:     

            pkt = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac2,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt1 = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac3,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt2 = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac4,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt3 = simple_tcp_packet(eth_dst=mac2,
                                    eth_src=mac1,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)
                                    
            port0_pkt_cnt = 0
            port1_pkt_cnt = 0
            
            self.ctc_send_packet(2, str(pkt))            
            rcv_idx = self.ctc_verify_any_packet_any_port( [pkt], [0, 1])
            if rcv_idx == 0:
                port0_pkt_cnt = 1
            elif rcv_idx == 1:
                port1_pkt_cnt = 1
            
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)

            self.ctc_send_packet(2, str(pkt1))            
            rcv_idx = self.ctc_verify_any_packet_any_port( [pkt1], [0, 1])
            if rcv_idx == 0:
                port0_pkt_cnt = port0_pkt_cnt + 1
            elif rcv_idx == 1:
                port1_pkt_cnt = port1_pkt_cnt + 1
            
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)

            self.ctc_send_packet(2, str(pkt2))            
            rcv_idx = self.ctc_verify_any_packet_any_port( [pkt2], [0, 1])
            if rcv_idx == 0:
                port0_pkt_cnt = port0_pkt_cnt + 1
            elif rcv_idx == 1:
                port1_pkt_cnt = port1_pkt_cnt + 1
            
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)

            flush_all_fdb(self.client)
            
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_no_packet(str(pkt3), 1)
            self.ctc_verify_packets( str(pkt3), [2], 1)

            self.ctc_send_packet(1, str(pkt3))
            self.ctc_verify_no_packet(str(pkt3), 0)
            self.ctc_verify_packets( str(pkt3), [2], 1)
            
        finally:
             

            flush_all_fdb(self.client)
                        
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_oid, attr)           
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            
            sai_thrift_remove_lag(self.client, lag_oid)   




class scenario_23_bridge_sub_port_is_lag(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 20 
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:22:22:22:22:23'
        mac4 = '00:22:22:22:22:24'
        mac_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        
        lag_oid = sai_thrift_create_lag(self.client)
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
                
        subport1 = sai_thrift_create_bridge_port(self.client, lag_oid, SAI_BRIDGE_PORT_TYPE_SUB_PORT, bridge_id, vlan_id1, None, True, None)
        subport2 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan_id2)
               
        warmboot(self.client)
        
        try:     

            pkt1 = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac2,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id1,                                    
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)
                                    
            pkt2 = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac2,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id2,                                    
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt3 = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac3,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id1,                                    
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt4 = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac3,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id2,                                    
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            sys_logging(" ingress ")

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_verify_packets( str(pkt2), [2], 1)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 0)
            self.ctc_verify_packets( str(pkt2), [2], 1)
            
            sys_logging(" egress ")
            
            flush_all_fdb(self.client)
             
            port0_pkt_cnt = 0
            port1_pkt_cnt = 0
            
            self.ctc_send_packet(2, str(pkt2))            
            rcv_idx = self.ctc_verify_any_packet_any_port( [pkt1], [0, 1])
            if rcv_idx == 0:
                port0_pkt_cnt = 1
            elif rcv_idx == 1:
                port1_pkt_cnt = 1
            
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)

            self.ctc_send_packet(2, str(pkt4))            
            rcv_idx = self.ctc_verify_any_packet_any_port( [pkt3], [0, 1])
            if rcv_idx == 0:
                port0_pkt_cnt = port0_pkt_cnt + 1
            elif rcv_idx == 1:
                port1_pkt_cnt = port1_pkt_cnt + 1
            
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)            

            sys_logging("### remove lag member ###")
            sai_thrift_remove_lag_member(self.client, lag_member_id2)

            sys_logging(" ingress ")

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_verify_packets( str(pkt2), [2], 1)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(str(pkt1), 0)
            self.ctc_verify_no_packet(str(pkt2), 2)

            sys_logging(" egress ")
            
            flush_all_fdb(self.client)            
            
            self.ctc_send_packet(2, str(pkt2))
            self.ctc_verify_packets( str(pkt1), [0], 1)
            self.ctc_verify_no_packet(str(pkt1), 1)
            
            self.ctc_send_packet(2, str(pkt4))
            self.ctc_verify_packets( str(pkt3), [0], 1)
            self.ctc_verify_no_packet(str(pkt3), 1)


            sys_logging("### add lag member ###")   
            
            lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)           
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_verify_packets( str(pkt2), [2], 1)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 0)
            self.ctc_verify_packets( str(pkt2), [2], 1)            
            
        finally:
             
            flush_all_fdb(self.client)
            self.client.sai_thrift_remove_bridge_port(subport1)
            
            self.client.sai_thrift_remove_bridge_port(subport2)
          
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)            
            sai_thrift_remove_lag(self.client, lag_oid)   
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            
            
            
            