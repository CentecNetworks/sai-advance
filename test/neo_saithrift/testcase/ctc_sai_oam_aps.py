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
Thrift SAI interface OAM APS tests
"""

import socket
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask
import pdb

@group('OAM_APS')



class scenario_01_mpls_lsp_bfd_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        #pdb.set_trace()

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label1, next_hop1, min_tx, min_rx, default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 100 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)


            sys_logging(" step 4 check bfd rx packet ")
            
            self.ctc_send_packet( 1, str(pkt2))
            #pdb.set_trace()
 
        finally:

            #pdb.set_trace()
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
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


class scenario_02_mpls_lsp_bfd_ttl1_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        #pdb.set_trace()

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label1, next_hop1, min_tx, min_rx, default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 100 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':1,'s':1}]
             
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)


            sys_logging(" step 4 check bfd rx packet ")
            
            self.ctc_send_packet( 1, str(pkt2))
            #pdb.set_trace()
 
        finally:

            #pdb.set_trace()
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
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


'''
class scenario_02_mpls_lsp_bfd_php_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        #vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        vr_id = sai_thrift_get_default_router_id(self.client)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label1, next_hop1, min_tx, min_rx, default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 100 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    

            sys_logging(" step 4 check bfd rx packet ")
            
            self.ctc_send_packet( 1, str(pkt))
 
        finally:

            #pdb.set_trace()
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, port1)
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
            
            #self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)
'''


class scenario_03_mpls_pw_vccv_raw_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label5, next_hop5, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_VCCV_RAW, min_tx=min_tx, min_rx=min_rx, multip=default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")
            
            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)


            mpls_label_stack2 = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack2,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

            #pdb.set_trace()
            time.sleep(5)
            #IPEDISCARDTYPE_APS_DIS
            self.ctc_send_packet( 2, str(pkt3))


            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=1,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac2,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            
            sys_logging(" step 6 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(2,str(pkt1)) 
            
            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 
            
            sys_logging(" step 7 check bfd rx packet ")
            
            self.ctc_send_packet( 2, str(pkt2))


        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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



class scenario_03_mpls_pw_vccv_raw_ttl1_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label5, next_hop5, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_VCCV_RAW, min_tx=min_tx, min_rx=min_rx, multip=default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")
            
            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)


            mpls_label_stack2 = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack2,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

            #pdb.set_trace()
            time.sleep(5)
            #IPEDISCARDTYPE_APS_DIS
            self.ctc_send_packet( 2, str(pkt3))


            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=1,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac2,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            
            sys_logging(" step 6 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(2,str(pkt1)) 
            
            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 
            
            sys_logging(" step 7 check bfd rx packet ")
            
            self.ctc_send_packet( 2, str(pkt2))


        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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

class scenario_04_mpls_pw_vccv_ipv4_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label5, next_hop5, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV4, min_tx=min_tx, min_rx=min_rx, multip=default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)

            pw_ach = hexstr_to_ascii('10000021')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")

            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)

            pw_ach = hexstr_to_ascii('10000021')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)



            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)

            pw_ach = hexstr_to_ascii('10000021')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]

            mpls_label_stack2 = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack2,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

            #pdb.set_trace()
            time.sleep(5)
            #IPEDISCARDTYPE_APS_DIS
            self.ctc_send_packet( 2, str(pkt3))


            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=1,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
            
            pw_ach = hexstr_to_ascii('10000021')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac2,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            
            sys_logging(" step 6 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(2,str(pkt1)) 
            
            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
            
            pw_ach = hexstr_to_ascii('10000021')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 
            
            sys_logging(" step 7 check bfd rx packet ")
            
            self.ctc_send_packet( 2, str(pkt2))


        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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


class scenario_04_mpls_pw_vccv_ipv4_ttl1_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label5, next_hop5, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV4, min_tx=min_tx, min_rx=min_rx, multip=default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)

            pw_ach = hexstr_to_ascii('10000021')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")

            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)

            pw_ach = hexstr_to_ascii('10000021')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)



            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)

            pw_ach = hexstr_to_ascii('10000021')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]

            mpls_label_stack2 = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack2,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

            #pdb.set_trace()
            time.sleep(5)
            #IPEDISCARDTYPE_APS_DIS
            self.ctc_send_packet( 2, str(pkt3))


            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=1,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
            
            pw_ach = hexstr_to_ascii('10000021')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac2,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            
            sys_logging(" step 6 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(2,str(pkt1)) 
            
            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
            
            pw_ach = hexstr_to_ascii('10000021')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 
            
            sys_logging(" step 7 check bfd rx packet ")
            
            self.ctc_send_packet( 2, str(pkt2))


        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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



class scenario_05_mpls_pw_vccv_ipv6_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        src_ip = '1234:5678:9abc:def0:0:0:0:1'
        #dst_ip = 'ffff:7f00:0:0:0:0:0:1' 
        dst_ip = '::FFFF:7f00:0'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label5, next_hop5, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV6, min_tx=min_tx, min_rx=min_rx, multip=default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_ipv6_udp_packet(pktlen=86,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=7<<5,
                                    ipv6_hlim=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)

            pw_ach = hexstr_to_ascii('10000057')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")

            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_ipv6_udp_packet(pktlen=86,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=7<<5,
                                    ipv6_hlim=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)

            pw_ach = hexstr_to_ascii('10000057')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)



            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      

            inner_pkt = simple_ipv6_udp_packet(pktlen=86,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=7<<5,
                                    ipv6_hlim=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            pw_ach = hexstr_to_ascii('10000057')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]

            mpls_label_stack2 = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack2,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

            #pdb.set_trace()
            time.sleep(5)
            #IPEDISCARDTYPE_APS_DIS
            self.ctc_send_packet( 2, str(pkt3))


            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=1,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)

            inner_pkt = simple_ipv6_udp_packet(pktlen=86,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=7<<5,
                                    ipv6_hlim=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
            
            pw_ach = hexstr_to_ascii('10000057')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac2,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            
            sys_logging(" step 6 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(2,str(pkt1)) 
            
            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)

            inner_pkt = simple_ipv6_udp_packet(pktlen=86,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=7<<5,
                                    ipv6_hlim=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            pw_ach = hexstr_to_ascii('10000057')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 
            
            sys_logging(" step 7 check bfd rx packet ")
            
            self.ctc_send_packet( 2, str(pkt2))


        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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

            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            
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




class scenario_05_mpls_pw_vccv_ipv6_ttl1_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        src_ip = '1234:5678:9abc:def0:0:0:0:1'
        #dst_ip = 'ffff:7f00:0:0:0:0:0:1' 
        dst_ip = '::FFFF:7f00:0'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label5, next_hop5, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV6, min_tx=min_tx, min_rx=min_rx, multip=default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_ipv6_udp_packet(pktlen=86,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=7<<5,
                                    ipv6_hlim=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)

            pw_ach = hexstr_to_ascii('10000057')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")

            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_ipv6_udp_packet(pktlen=86,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=7<<5,
                                    ipv6_hlim=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)

            pw_ach = hexstr_to_ascii('10000057')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)



            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      

            inner_pkt = simple_ipv6_udp_packet(pktlen=86,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=7<<5,
                                    ipv6_hlim=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            pw_ach = hexstr_to_ascii('10000057')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]

            mpls_label_stack2 = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack2,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

            #pdb.set_trace()
            time.sleep(5)
            #IPEDISCARDTYPE_APS_DIS
            self.ctc_send_packet( 2, str(pkt3))


            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=1,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)

            inner_pkt = simple_ipv6_udp_packet(pktlen=86,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=7<<5,
                                    ipv6_hlim=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
            
            pw_ach = hexstr_to_ascii('10000057')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac2,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            
            sys_logging(" step 6 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(2,str(pkt1)) 
            
            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)

            inner_pkt = simple_ipv6_udp_packet(pktlen=86,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=7<<5,
                                    ipv6_hlim=255,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            pw_ach = hexstr_to_ascii('10000057')
                        
            mpls_inner_pkt = pw_ach + str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 
            
            sys_logging(" step 7 check bfd rx packet ")
            
            self.ctc_send_packet( 2, str(pkt2))


        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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

            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            
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


class scenario_06_mpls_tp_lsp_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label1, next_hop1, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=min_rx, multip=default_mult, cv_en=0, src_mepid=None, without_gal=0)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)

            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")

            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

 
        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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



class scenario_06_mpls_tp_lsp_ttl1_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label1, next_hop1, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=min_rx, multip=default_mult, cv_en=0, src_mepid=None, without_gal=0)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)

            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")

            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':1,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

 
        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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


class scenario_07_mpls_tp_pw_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label5, next_hop5, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=min_rx, multip=default_mult, cv_en=0, src_mepid=None, without_gal=0)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)

            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")

            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)



            mpls_label_stack2 = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack2,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

            #pdb.set_trace()
            time.sleep(5)
            #IPEDISCARDTYPE_APS_DIS
            self.ctc_send_packet( 2, str(pkt3))


            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=1,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac2,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            
            sys_logging(" step 6 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(2,str(pkt1)) 
            
            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 
            
            sys_logging(" step 7 check bfd rx packet ")
            
            self.ctc_send_packet( 2, str(pkt2))


 
        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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




class scenario_07_mpls_tp_pw_ttl1_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label5, next_hop5, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=min_rx, multip=default_mult, cv_en=0, src_mepid=None, without_gal=0)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)

            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")

            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)



            mpls_label_stack2 = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack2,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

            #pdb.set_trace()
            time.sleep(5)
            #IPEDISCARDTYPE_APS_DIS
            self.ctc_send_packet( 2, str(pkt3))


            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=1,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac2,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            
            sys_logging(" step 6 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(2,str(pkt1)) 
            
            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':0},{'label':13,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 
            
            sys_logging(" step 7 check bfd rx packet ")
            
            self.ctc_send_packet( 2, str(pkt2))


 
        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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





class scenario_08_mpls_tp_pw_without_gal_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label5, next_hop5, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=min_rx, multip=default_mult, cv_en=0, src_mepid=None, without_gal=1)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)

            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")

            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)



            mpls_label_stack2 = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack2,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

            #pdb.set_trace()
            time.sleep(5)
            #IPEDISCARDTYPE_APS_DIS
            self.ctc_send_packet( 2, str(pkt3))


            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=1,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac2,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            
            sys_logging(" step 6 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(2,str(pkt1)) 
            
            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 
            
            sys_logging(" step 7 check bfd rx packet ")
            
            self.ctc_send_packet( 2, str(pkt2))


 
        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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



class scenario_08_mpls_tp_pw_without_gal_ttl1_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label5, next_hop5, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=min_rx, multip=default_mult, cv_en=0, src_mepid=None, without_gal=1)
            sys_logging("creat bfd session = %d" %bfd_oid1)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)

            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 3 check bfd tx packet ")

            # lsp ttl is map
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)



            mpls_label_stack2 = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack2,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 4 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

            #pdb.set_trace()
            time.sleep(5)
            #IPEDISCARDTYPE_APS_DIS
            self.ctc_send_packet( 2, str(pkt3))


            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=1,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac2,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            
            sys_logging(" step 6 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(2,str(pkt1)) 
            
            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            g_ach = hexstr_to_ascii('10000022')

            mpls_inner_pkt = g_ach + str(bfd_hdr)


            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':1,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 
            
            sys_logging(" step 7 check bfd rx packet ")
            
            self.ctc_send_packet( 2, str(pkt2))


 
        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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

class scenario_09_mpls_tp_lsp_y1731_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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


        sys_logging(" step 2 create mpls tp lsp y1731 session ")

        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = label1
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, next_hop1, nogal=0)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)


        try:


            sys_logging(" step 3 check bfd tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


            self.ctc_show_packet_twamp(1,str(pkt)) 
            #pdb.set_trace()


            sys_logging(" step 4 check bfd rx packet ")


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(1) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
        finally:

            #pdb.set_trace()
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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



class scenario_09_mpls_tp_lsp_y1731_ttl1_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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


        sys_logging(" step 2 create mpls tp lsp y1731 session ")

        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = label1
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, next_hop1, nogal=0)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)


        try:


            sys_logging(" step 3 check bfd tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


            self.ctc_show_packet_twamp(1,str(pkt)) 
            #pdb.set_trace()


            sys_logging(" step 4 check bfd rx packet ")


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':1,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(1) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        
        finally:

            #pdb.set_trace()
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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



class scenario_10_mpls_tp_pw_y1731_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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


        sys_logging(" step 2 create mpls tp lsp y1731 session ")

        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = label5
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, next_hop5, nogal=0)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)


        try:


            sys_logging(" step 3 check bfd tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


            self.ctc_show_packet_twamp(1,str(pkt)) 
            #pdb.set_trace()


            sys_logging(" step 4 check bfd rx packet ")


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':64,'s':0}, {'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(1) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':64,'s':0}, {'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
            # aps discard                    
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(3) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        

            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            sys_logging(" step 6 check bfd tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=1,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
            
            
            self.ctc_show_packet_twamp(2,str(pkt)) 
            #pdb.set_trace()
            
            
            sys_logging(" step 7 check bfd rx packet ")
            
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':64,'s':0}, {'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac2,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 2, str(pkt))
            time.sleep(1) 
            
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
            
        finally:

            #pdb.set_trace()
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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




class scenario_10_mpls_tp_pw_y1731_ttl1_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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


        sys_logging(" step 2 create mpls tp lsp y1731 session ")

        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = label5
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, next_hop5, nogal=0)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)


        try:


            sys_logging(" step 3 check bfd tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


            self.ctc_show_packet_twamp(1,str(pkt)) 
            #pdb.set_trace()


            sys_logging(" step 4 check bfd rx packet ")


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':1,'s':0}, {'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(1) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':1,'s':0}, {'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
            # aps discard                    
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(3) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        

            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            sys_logging(" step 6 check bfd tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=1,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
            
            
            self.ctc_show_packet_twamp(2,str(pkt)) 
            #pdb.set_trace()
            
            
            sys_logging(" step 7 check bfd rx packet ")
            
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':1,'s':0}, {'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac2,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 2, str(pkt))
            time.sleep(1) 
            
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
            
        finally:

            #pdb.set_trace()
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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


class scenario_11_mpls_tp_pw_y1731_without_gal_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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


        sys_logging(" step 2 create mpls tp lsp y1731 session ")

        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = label5
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, next_hop5, nogal=1)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)


        try:


            sys_logging(" step 3 check bfd tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':0,'ttl':64,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


            self.ctc_show_packet_twamp(1,str(pkt)) 
            #pdb.set_trace()


            sys_logging(" step 4 check bfd rx packet ")


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':64,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(1) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':64,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
            # aps discard                    
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(3) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        

            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            sys_logging(" step 6 check bfd tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=1,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':0,'ttl':64,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
            
            
            self.ctc_show_packet_twamp(2,str(pkt)) 
            #pdb.set_trace()
            
            
            sys_logging(" step 7 check bfd rx packet ")
            
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':64,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac2,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 2, str(pkt))
            time.sleep(1) 
            
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
            
        finally:

            #pdb.set_trace()
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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



class scenario_11_mpls_tp_pw_y1731_without_gal_ttl1_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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


        sys_logging(" step 2 create mpls tp lsp y1731 session ")

        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = label5
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, next_hop5, nogal=1)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1)        
        sys_logging("creat rmep id1 = %d" %rmep_id1)


        try:


            sys_logging(" step 3 check bfd tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':0,'ttl':64,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


            self.ctc_show_packet_twamp(1,str(pkt)) 
            #pdb.set_trace()


            sys_logging(" step 4 check bfd rx packet ")


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(1) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
            # aps discard                    
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(3) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
                        

            sys_logging(" step 5 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            sys_logging(" step 6 check bfd tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=1,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':0,'ttl':64,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac2,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
            
            
            self.ctc_show_packet_twamp(2,str(pkt)) 
            #pdb.set_trace()
            
            
            sys_logging(" step 7 check bfd rx packet ")
            
            
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0}, {'label':label5,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 2, str(pkt))
            time.sleep(1) 
            
            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
            
        finally:

            #pdb.set_trace()
            sys_logging("======clean up======")

            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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







class scenario_12_bfd_session_coexist_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 3

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label1, next_hop1, min_tx, min_rx, default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid1)


            bfd_hdr = simple_bfd_packet(vers=1,
                               diag=0,
                               sta=1,
                               pbit=0,
                               fbit=0,
                               cbit=0,
                               abit=0,
                               dbit=0,
                               mbit=0,
                               mult=default_mult,
                               mydisc=l_disc,
                               yourdisc=r_disc,
                               mintxinterval=min_tx,
                               minrxinterval=min_rx,
                               echointerval=0)
                                   
            inner_pkt = simple_udp_packet(pktlen=66,
                                 eth_dst=router_mac,
                                 eth_src=router_mac,
                                 ip_src=src_ip,
                                 ip_dst=dst_ip,
                                 ip_tos=7<<5,
                                 ip_ttl=1,
                                 udp_sport=udp_srcport,
                                 udp_dport=3784,
                                 ip_ihl=None,
                                 ip_id=0,
                                 ip_options=False,
                                 with_udp_chksum=False,
                                 udp_payload=bfd_hdr)
                                 
            mpls_inner_pkt = str(inner_pkt)[14:]

            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]

            pkt1 = simple_mpls_packet(eth_dst=dmac,
                              eth_src=router_mac,
                              mpls_type=0x8847,
                              mpls_tags= mpls_label_stack,
                              inner_frame = mpls_inner_pkt)


            sys_logging(" step 3 check bfd tx packet ")

            self.ctc_show_packet_twamp(1,str(pkt1))
            

            sys_logging(" step 4 create mpls pw bfd session ")

            l_disc = 300
            r_disc = 400

            bfd_oid2 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label5, next_hop5, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_VCCV_RAW, min_tx=min_tx, min_rx=min_rx, multip=default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid2)

 
             

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 5 check bfd tx packet ")
            
            # lsp ttl is map

            # bfd send packet too fast, so check packet always failed 
            #self.ctc_show_packet_twamp(1,str(pkt2)) 

            # pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 500 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)


            mpls_label_stack2 = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack2,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 6 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))

            #pdb.set_trace()
            time.sleep(5)
            #IPEDISCARDTYPE_APS_DIS
            self.ctc_send_packet( 2, str(pkt3))


            sys_logging(" step 7 set aps group switchover ")

            nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
            nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
            self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=1,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt1 = simple_mpls_packet(eth_dst=dmac2,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
            
            sys_logging(" step 8 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(2,str(pkt1)) 
            
            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                     
            pw_ach = hexstr_to_ascii('10000007')

            mpls_inner_pkt = pw_ach + str(bfd_hdr)

            
            mpls_label_stack = [{'label':label2,'tc':0,'ttl':64,'s':0},{'label':label5,'tc':7,'ttl':64,'s':1}]
            
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 
            
            sys_logging(" step 9 check bfd rx packet ")
            
            self.ctc_send_packet( 2, str(pkt2))


        finally:

            #pdb.set_trace()
            
            sys_logging("======clean up======")

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            sai_thrift_remove_bfd(self.client, bfd_oid2)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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





class scenario_13_bfd_updateApsEn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)
        #pdb.set_trace()

        sys_logging("======create a lsp aps nexthop group======")
        #first = sai_thrift_create_next_hop_protection_group(self.client)
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        #pdb.set_trace()

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        #pdb.set_trace()
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        #pdb.set_trace()

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 5
        ach_type=None
        cv_en=0
        src_mepid=None
        without_gal=0
        l3if_oid=None
        aps_group=nhop_group1
        is_protection=False
        protection_en=True

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label1, next_hop1, ach_type, min_tx, min_rx, default_mult, cv_en, src_mepid, without_gal, l3if_oid,  aps_group, is_protection, protection_en)
            #pdb.set_trace()

            sys_logging("step 3 get the nexthop group attribute")

            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError() 

            sys_logging(" step 4 get mpls bfd session attr ")

            
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_oid1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:

                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_STATE:
                    sys_logging("SAI_BFD_SESSION_ATTR_REMOTE_STATE is = %d" %a.value.s32)
                    if SAI_BFD_SESSION_STATE_DOWN != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID is = %d" %a.value.oid)
                    if nhop_group1 != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH is = %d" %a.value.booldata)
                    if is_protection != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN is = %d" %a.value.booldata)
                    if protection_en != a.value.booldata:
                        raise NotImplementedError()   

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 5 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            #pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 100 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)


            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=2,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]

            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)


            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=3,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]                                 
            pkt4 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 6 check bfd rx packet ")
            
            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_send_packet( 1, str(pkt4))           
            #pdb.set_trace()

            time.sleep(5)

            sys_logging(" step 7 get the nexthop group attribute")

            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)                    
                    if 1 != a.value.booldata:
                        raise NotImplementedError() 
        finally:

            
            sys_logging("======clean up======")
            #pdb.set_trace()

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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







class scenario_14_bfd_Repair(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)
        #pdb.set_trace()

        sys_logging("======create a lsp aps nexthop group======")
        #first = sai_thrift_create_next_hop_protection_group(self.client)
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        #pdb.set_trace()

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        #pdb.set_trace()
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        #pdb.set_trace()

        sys_logging(" set aps group switchover ")
        
        nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
        nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
        self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)
        

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 5
        ach_type=None
        cv_en=0
        src_mepid=None
        without_gal=0
        l3if_oid=None
        aps_group=nhop_group1
        is_protection=True
        protection_en=True

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label1, next_hop1, ach_type, min_tx, min_rx, default_mult, cv_en, src_mepid, without_gal, l3if_oid,  aps_group, is_protection, protection_en)
            #pdb.set_trace()

            sys_logging("step 3 get the nexthop group attribute")

            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError() 

            sys_logging(" step 4 get mpls bfd session attr ")

            
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_oid1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:

                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_STATE:
                    sys_logging("SAI_BFD_SESSION_ATTR_REMOTE_STATE is = %d" %a.value.s32)
                    if SAI_BFD_SESSION_STATE_DOWN != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID is = %d" %a.value.oid)
                    if nhop_group1 != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH is = %d" %a.value.booldata)
                    if is_protection != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN is = %d" %a.value.booldata)
                    if protection_en != a.value.booldata:
                        raise NotImplementedError()   

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 5 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            #pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 100 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)


            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=2,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]

            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)


            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=3,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]                                 
            pkt4 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 6 check bfd rx packet ")
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_send_packet( 1, str(pkt4))           
            #pdb.set_trace()

            time.sleep(5)

            sys_logging(" step 7 get the nexthop group attribute")

            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)                    
                    if 0 != a.value.booldata:
                        raise NotImplementedError() 
        finally:

            
            sys_logging("======clean up======")
            #pdb.set_trace()

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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





class scenario_15_bfd_apsgroup_set_and_get(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)
        #pdb.set_trace()

        sys_logging("======create a lsp aps nexthop group======")
        #first = sai_thrift_create_next_hop_protection_group(self.client)
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        #pdb.set_trace()

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        #pdb.set_trace()
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        #pdb.set_trace()

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 5
        ach_type=None
        cv_en=0
        src_mepid=None
        without_gal=0
        l3if_oid=None
        aps_group=None
        is_protection=None
        protection_en=None

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label1, next_hop1, ach_type, min_tx, min_rx, default_mult, cv_en, src_mepid, without_gal, l3if_oid,  aps_group, is_protection, protection_en)
            #pdb.set_trace()

            sys_logging("step 3 get the nexthop group attribute")

            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError() 

            sys_logging(" step 4 get and set mpls bfd session attr ")

            
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_oid1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:

                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_STATE:
                    sys_logging("SAI_BFD_SESSION_ATTR_REMOTE_STATE is = %d" %a.value.s32)
                    if SAI_BFD_SESSION_STATE_DOWN != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID is = %d" %a.value.oid)
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH is = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN is = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()   

            attr_value = sai_thrift_attribute_value_t(oid=nhop_group1)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_oid1, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_oid1, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_oid1, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_oid1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:

                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_STATE:
                    sys_logging("SAI_BFD_SESSION_ATTR_REMOTE_STATE is = %d" %a.value.s32)
                    if SAI_BFD_SESSION_STATE_DOWN != a.value.s32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID is = %d" %a.value.oid)
                    if nhop_group1 != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH is = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN is = %d" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError() 


            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 5 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 

            #pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 100 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)


            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=2,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]

            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)


            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=3,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]                                 
            pkt4 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 6 check bfd rx packet ")
            
            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_send_packet( 1, str(pkt4))           
            #pdb.set_trace()

            time.sleep(5)

            sys_logging(" step 7 get the nexthop group attribute")

            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)                    
                    if 1 != a.value.booldata:
                        raise NotImplementedError() 

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_oid1, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_oid1, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_oid1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                        
                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID is = %d" %a.value.oid)
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError()
            
                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_IS_PROTECTION_PATH is = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
            
                if a.id == SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN:
                    sys_logging("SAI_BFD_SESSION_ATTR_HW_PROTECTION_EN is = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError() 

                        
        finally:

            
            sys_logging("======clean up======")
            #pdb.set_trace()

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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




class scenario_16_bfd_set_state_to_admindown(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)
        #pdb.set_trace()

        sys_logging("======create a lsp aps nexthop group======")
        #first = sai_thrift_create_next_hop_protection_group(self.client)
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)
        #pdb.set_trace()

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        #pdb.set_trace()
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        #pdb.set_trace()

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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
        #pdb.set_trace()


        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        src_ip = '10.0.0.1'      
        dst_ip = '127.0.0.1'
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL        
        min_tx = 4
        min_rx = 3
        default_mult = 5
        ach_type=None
        cv_en=0
        src_mepid=None
        without_gal=0
        l3if_oid=None
        aps_group=nhop_group1
        is_protection=False
        protection_en=True

        try:

            sys_logging(" step 2 create mpls lsp bfd session ")

            bfd_oid1 = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, label1, next_hop1, ach_type, min_tx, min_rx, default_mult, cv_en, src_mepid, without_gal, l3if_oid,  aps_group, is_protection, protection_en)
            #pdb.set_trace()

            sys_logging("step 3 get the nexthop group attribute")

            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError() 

            sys_logging(" step 4 get mpls bfd session attr ")
           
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_oid1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:

                if a.id == SAI_BFD_SESSION_ATTR_STATE:
                    sys_logging("SAI_BFD_SESSION_ATTR_STATE is = %d" %a.value.s32)
                    if SAI_BFD_SESSION_STATE_DOWN != a.value.s32:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(s32=SAI_BFD_SESSION_STATE_ADMIN_DOWN)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_STATE, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_oid1, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_oid1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:

                if a.id == SAI_BFD_SESSION_ATTR_STATE:
                    sys_logging("SAI_BFD_SESSION_ATTR_STATE is = %d" %a.value.s32)
                    if SAI_BFD_SESSION_STATE_ADMIN_DOWN != a.value.s32:
                        raise NotImplementedError()

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=SAI_BFD_SESSION_STATE_ADMIN_DOWN,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 5 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(1,str(pkt1)) 


            attr_value = sai_thrift_attribute_value_t(s32=SAI_BFD_SESSION_STATE_DOWN)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_STATE, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_oid1, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=SAI_BFD_SESSION_STATE_DOWN,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=l_disc,
                                  yourdisc=r_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt1 = simple_mpls_packet(eth_dst=dmac,
                                 eth_src=router_mac,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)

            sys_logging(" step 5 check bfd tx packet ")
            
            self.ctc_show_packet_twamp(1,str(pkt1))             

            #pdb.set_trace()
            # sdk bug
            # mpls ilm space 0 label 100 property oam-mp-chk-type 1

            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=1,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]
             
            pkt2 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)


            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=2,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]

            pkt3 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)


            bfd_hdr = simple_bfd_packet(vers=1,
                                  diag=0,
                                  sta=3,
                                  pbit=0,
                                  fbit=0,
                                  cbit=0,
                                  abit=0,
                                  dbit=0,
                                  mbit=0,
                                  mult=default_mult,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=min_tx,
                                  minrxinterval=min_rx,
                                  echointerval=0)
                                      
            inner_pkt = simple_udp_packet(pktlen=66,
                                    eth_dst=router_mac,
                                    eth_src=router_mac,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=7<<5,
                                    ip_ttl=1,
                                    udp_sport=udp_srcport,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=False,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(inner_pkt)[14:]
            
            mpls_label_stack = [{'label':label1,'tc':7,'ttl':64,'s':1}]                                 
            pkt4 = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src='00:55:55:55:55:66',
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                                 

            sys_logging(" step 6 check bfd rx packet ")
            
            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_send_packet( 1, str(pkt3))
            self.ctc_send_packet( 1, str(pkt4))           
            #pdb.set_trace()

            time.sleep(5)

            sys_logging(" step 7 get the nexthop group attribute")

            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)                    
                    if 1 != a.value.booldata:
                        raise NotImplementedError() 
        finally:

            
            sys_logging("======clean up======")
            #pdb.set_trace()

            sai_thrift_remove_bfd(self.client, bfd_oid1)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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





class scenario_17_y1731_updateApsEn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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


        sys_logging(" step 2 create mpls tp lsp y1731 session ")

        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = label1
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, next_hop1, nogal=0)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac=None
        aps_group=nhop_group1
        is_protection=False
        protection_en=True
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac, aps_group, is_protection, protection_en) 
        sys_logging("creat rmep id1 = %d" %rmep_id1)                    

        try:


            sys_logging(" step 3 check y1731 ccm tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


            self.ctc_show_packet_twamp(1,str(pkt)) 
            #pdb.set_trace()

            sys_logging("step 4 get the nexthop group attribute")
            
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError() 


            sys_logging(" step 5 check y1731 ccm rx packet ")


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(1) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

            #pdb.set_trace()

            time.sleep(1) 

            sys_logging("step 6 get the nexthop group attribute")
            
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError() 
                    
        finally:

            sys_logging("======clean up======")
            #pdb.set_trace()
            
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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




class scenario_18_y1731_Repair(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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


        sys_logging(" step 2 create mpls tp lsp y1731 session ")

        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = label1
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, next_hop1, nogal=0)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac=None
        aps_group=nhop_group1
        is_protection=True
        protection_en=True
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac, aps_group, is_protection, protection_en) 
        sys_logging("creat rmep id1 = %d" %rmep_id1)                    

        sys_logging(" set aps group switchover ")
        
        nhop_group_atr_value = sai_thrift_attribute_value_t(booldata=1)
        nhop_group_atr = sai_thrift_attribute_t(id=SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER, value=nhop_group_atr_value)
        self.client.sai_thrift_set_next_hop_group_attribute(nhop_group1, nhop_group_atr)

        try:


            sys_logging(" step 3 check y1731 ccm tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


            self.ctc_show_packet_twamp(1,str(pkt)) 
            #pdb.set_trace()

            sys_logging("step 4 get the nexthop group attribute")
            
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError() 


            sys_logging(" step 5 check y1731 ccm rx packet ")


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(1) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

            #pdb.set_trace()

            time.sleep(1) 

            sys_logging("step 6 get the nexthop group attribute")
            
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError() 
                    
        finally:

            sys_logging("======clean up======")
            #pdb.set_trace()
            
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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





class scenario_19_y1731_apsgroup_set_and_get(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da3, dmac3)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da4, dmac4)
        
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da2, rif_id2, label_list2)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da3, rif_id3, label_list3)
        next_hop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da4, rif_id4, label_list4)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group1 = sai_thrift_create_next_hop_protection_group(self.client)

        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember1_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember1_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)

        sys_logging("======create a lsp aps nexthop group======")
        nhop_group2 = sai_thrift_create_next_hop_protection_group(self.client)
        
        sys_logging("======add 2 aps group memeber to the nexthop group======")
        nhop_gmember2_w = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop3, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_PRIMARY)
        nhop_gmember2_p = sai_thrift_create_next_hop_group_member(self.client, nhop_group2, next_hop4, cfg_role=SAI_NEXT_HOP_GROUP_MEMBER_CONFIGURED_ROLE_STANDBY)
        
        next_hop5 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list5, next_level_nhop_oid=nhop_group1)
        next_hop6 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list6, next_level_nhop_oid=nhop_group2)

        sys_logging("======create a pw aps nexthop group======")
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


        sys_logging(" step 2 create mpls tp lsp y1731 session ")

        meg_type = SAI_Y1731_MEG_TYPE_MPLS_TP
        meg_name = "abcd"
        level = 7
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mpls_in_label = label1
        mep_id = sai_thrift_create_y1731_tp_session(self.client, mpls_in_label, meg_id, dir, local_mep_id, ccm_period, ccm_en, next_hop1, nogal=0)        
        sys_logging("creat mep id = %d" %mep_id)
        
        remote_mep_id1 = 11
        mac=None
        aps_group=None
        is_protection=None
        protection_en=None
        rmep_id1 = sai_thrift_create_y1731_rmep(self.client, mep_id, remote_mep_id1, mac, aps_group, is_protection, protection_en) 
        sys_logging("creat rmep id1 = %d" %rmep_id1)                    


        sys_logging("get rmep 1 info")
        attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
        
            if a.id == SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID:
                sys_logging("SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID is = %d" %a.value.oid)
                if SAI_NULL_OBJECT_ID != a.value.oid:
                    raise NotImplementedError()
                    
            if a.id == SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_IS_PROTECTION_PATH:
                sys_logging("SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_IS_PROTECTION_PATH is = %d" %a.value.booldata)
                if 0 != a.value.booldata:
                    raise NotImplementedError()
                    
            if a.id == SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_EN:
                sys_logging("SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_EN is = %d" %a.value.booldata)
                if 0 != a.value.booldata:
                    raise NotImplementedError()

        attr_value = sai_thrift_attribute_value_t(oid=nhop_group1)
        attr = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID, value=attr_value)
        status = self.client.sai_thrift_set_y1731_rmep_attribute(rmep_id1, attr)
        sys_logging("set rmep attr status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(booldata=0)
        attr = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_IS_PROTECTION_PATH, value=attr_value)
        status = self.client.sai_thrift_set_y1731_rmep_attribute(rmep_id1, attr)
        sys_logging("set rmep attr status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_EN, value=attr_value)
        status = self.client.sai_thrift_set_y1731_rmep_attribute(rmep_id1, attr)
        sys_logging("set rmep attr status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)
        
        sys_logging("get rmep 1 info")
        attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
        
            if a.id == SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID:
                sys_logging("SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID is = %d" %a.value.oid)
                if nhop_group1 != a.value.oid:
                    raise NotImplementedError()
                    
            if a.id == SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_IS_PROTECTION_PATH:
                sys_logging("SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_IS_PROTECTION_PATH is = %d" %a.value.booldata)
                if 0 != a.value.booldata:
                    raise NotImplementedError()
                    
            if a.id == SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_EN:
                sys_logging("SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_EN is = %d" %a.value.booldata)
                if 1 != a.value.booldata:
                    raise NotImplementedError()
                    

        try:


            sys_logging(" step 3 check y1731 ccm tx packet ")
                
            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=local_mep_id,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=dmac,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)


            self.ctc_show_packet_twamp(1,str(pkt)) 
            #pdb.set_trace()

            sys_logging("step 4 get the nexthop group attribute")
            
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError() 


            sys_logging(" step 5 check y1731 ccm rx packet ")


            ccm_hdr = simple_ccm_packet(mel=level,
                                       rdi=0,
                                       period=ccm_period,
                                       mepid=remote_mep_id1,
                                       megid=meg_name)
                                       
            ach_header = hexstr_to_ascii('10008902')
            
            mpls_inner_pkt = ach_header + str(ccm_hdr)
                                      
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
                                
            self.ctc_send_packet( 1, str(pkt))
            time.sleep(1) 

            sys_logging("get rmep 1 info")
            attrs = self.client.sai_thrift_get_y1731_rmep_attribute(rmep_id1)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_Y1731_REMOTE_MEP_ATTR_CONNECTION_ESTABLISHED:
                    sys_logging("get rmep established = %s" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

            #pdb.set_trace()

            time.sleep(1) 

            sys_logging("step 6 get the nexthop group attribute")
            
            attrs = self.client.sai_thrift_get_next_hop_group_attribute(nhop_group1)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER:
                    sys_logging("SAI_NEXT_HOP_GROUP_ATTR_SET_SWITCHOVER is = %d" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError() 

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_EN, value=attr_value)
            status = self.client.sai_thrift_set_y1731_rmep_attribute(rmep_id1, attr)
            sys_logging("set rmep attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_IS_PROTECTION_PATH, value=attr_value)
            status = self.client.sai_thrift_set_y1731_rmep_attribute(rmep_id1, attr)
            sys_logging("set rmep attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_Y1731_REMOTE_MEP_ATTR_HW_PROTECTION_NEXT_HOP_GROUP_ID, value=attr_value)
            status = self.client.sai_thrift_set_y1731_rmep_attribute(rmep_id1, attr)
            sys_logging("set rmep attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
                    
        finally:

            sys_logging("======clean up======")
            #pdb.set_trace()
            
            self.client.sai_thrift_remove_y1731_rmep(rmep_id1)
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, frr_bport)
            flush_all_fdb(self.client)
            
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


