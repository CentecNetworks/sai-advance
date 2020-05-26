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
Thrift SAI Tunnel tests
"""
import socket
from switch import *
import sai_base_test
from ptf.mask import Mask

class TunnelCreateTunnelMapEntryTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Bridge Create and Remove test. Verify 1D Bridge. 
        Steps:
        1. create 1D Bridge
        2. Test Bridge
        3. clean up.
        """
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID
        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI
        vlan_id = 20
        vni_id = 1000
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        print "tunnel_map_decap_id = %lx" %tunnel_map_decap_id
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, vlan_id)
         
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_tunnel_map_entry_attribute(tunnel_map_entry_decap_id)

            for a in attrs.attr_list:
                if a.id == SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP_TYPE:
                    print "type %d" %a.value.s32
                    if SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_TUNNEL_MAP_ENTRY_ATTR_TUNNEL_MAP:
                    print "tunnel map id %lx" %a.value.oid
                    if tunnel_map_decap_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_TUNNEL_MAP_ENTRY_ATTR_VNI_ID_KEY:
                    print "vni id %d" %a.value.u32
                    if vni_id != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_TUNNEL_MAP_ENTRY_ATTR_VLAN_ID_VALUE:
                    print "vlan id %d" %a.value.u16
                    if vlan_id != a.value.u16:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id)
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class TunnelCreateTunnelMapTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID
        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI
        vlan_id = 20
        vni_id = 1000
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        print "tunnel_map_decap_id = %lx" %tunnel_map_decap_id
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, vlan_id)
         
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_tunnel_map_attribute(tunnel_map_decap_id)

            for a in attrs.attr_list:
                if a.id == SAI_TUNNEL_MAP_ATTR_TYPE:
                    print "type %d" %a.value.s32
                    if SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_TUNNEL_MAP_ATTR_ENTRY_LIST:
                    for tmp_tunnel_map_id in a.value.objlist.object_id_list:
                        print "tunnel map entry id %lx" %tmp_tunnel_map_id
                        if tmp_tunnel_map_id != tunnel_map_entry_decap_id:
                            raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id)
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
class TunnelCreateTunnelTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Bridge Create and Remove test. Verify 1D Bridge. 
        Steps:
        1. create 1D Bridge
        2. Test Bridge
        3. clean up.
        """
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        ip_addr="40.40.40.40"
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        tunnel_id = sai_thrift_create_tunnel(self.client, underlay_if=rif_id1, overlay_if=rif_id2, ip_addr=ip_addr)
        print "tunnel_id = %lx" %tunnel_id
        
        warmboot(self.client)
        try:
            attr_ids = [SAI_TUNNEL_ATTR_TYPE, SAI_TUNNEL_ATTR_DECAP_TTL_MODE, SAI_TUNNEL_ATTR_DECAP_DSCP_MODE, SAI_TUNNEL_ATTR_ENCAP_SRC_IP]
            attrs = self.client.sai_thrift_get_tunnel_attribute(tunnel_id, attr_ids)

            for a in attrs.attr_list:
                if a.id == SAI_TUNNEL_ATTR_TYPE:
                    print "type %d" %a.value.s32
                    if SAI_TUNNEL_TYPE_IPINIP != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_TUNNEL_ATTR_DECAP_TTL_MODE:
                    print "decap ttl mode %d" %a.value.s32
                    if SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_TUNNEL_ATTR_DECAP_DSCP_MODE:
                    print "decap dscp mode %d" %a.value.s32
                    if SAI_TUNNEL_DSCP_MODE_UNIFORM_MODEL != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_TUNNEL_ATTR_ENCAP_SRC_IP:
                    print "encap addr family %d" %a.value.ipaddr.addr_family
                    print "encap src ip %s" %a.value.ipaddr.addr.ip4
                    if ip_addr != a.value.ipaddr.addr.ip4:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_tunnel(tunnel_id)

class TunnelRemoveTunnelTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        ip_addr="40.40.40.40"
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        tunnel_id = sai_thrift_create_tunnel(self.client, underlay_if=rif_id1, overlay_if=rif_id2, ip_addr=ip_addr)
        print "tunnel_id = %lx" %tunnel_id
        
        warmboot(self.client)
        try:
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            tunnel_id = sai_thrift_create_tunnel(self.client, underlay_if=rif_id1, overlay_if=rif_id2, ip_addr=ip_addr)
            
        finally:
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
class TunnelCreateTunnelTermTableEntryTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        ip_addr="40.40.40.40"
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        tunnel_id = sai_thrift_create_tunnel(self.client, underlay_if=rif_id1, overlay_if=rif_id2, ip_addr=ip_addr)
        print "tunnel_id = %lx" %tunnel_id

        ip_addr_sa = '20.20.20.20'

        ip_addr_da = '40.40.40.40'

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_addr_sa, ip_addr_da, tunnel_id)
        print "tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id
        
        warmboot(self.client)
        try:
            attr_ids = [SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID, SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE, SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP, SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP, SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID]
            attrs = self.client.sai_thrift_get_tunnel_term_table_entry_attribute(tunnel_term_table_entry_id, attr_ids)

            for a in attrs.attr_list:
                if a.id == SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_VR_ID:
                    print "vrf oid %lx" %a.value.oid
                    if vr_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_TYPE:
                    print "term table type %d" %a.value.s32
                    if SAI_TUNNEL_TERM_TABLE_ENTRY_TYPE_P2P != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_DST_IP:
                    print "encap dest ip %s" %a.value.ipaddr.addr.ip4
                    if ip_addr_da != a.value.ipaddr.addr.ip4:
                        raise NotImplementedError()
                if a.id == SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_SRC_IP:
                    print "encap src ip %s" %a.value.ipaddr.addr.ip4
                    if ip_addr_sa != a.value.ipaddr.addr.ip4:
                        raise NotImplementedError()
                if a.id == SAI_TUNNEL_TERM_TABLE_ENTRY_ATTR_ACTION_TUNNEL_ID:
                    print "tunnel oid %lx" %a.value.oid
                    if tunnel_id != a.value.oid:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)

class TunnelCreateIpInIpTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = router_mac
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        vr_id = sai_thrift_get_default_router_id(self.client)
        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        rif_lp_outer_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_decap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        tunnel_id = sai_thrift_create_tunnel(self.client, underlay_if=rif_lp_inner_id, overlay_if=rif_lp_outer_id, ip_addr=ip_outer_addr_sa)
        print "tunnel_id = %lx" %tunnel_id

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id)
        print "tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id
        
        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);
        print "tunnel_nexthop_id = %lx" %tunnel_nexthop_id
        
        encap_mac_da = '00:0e:00:0e:00:0e'
        sai_thrift_create_neighbor(self.client, addr_family, rif_decap_id, ip_outer_addr_da, encap_mac_da)
        
        ip_encap_addr_da = '20.20.20.20'
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_encap_addr_da, ip_mask, tunnel_nexthop_id)  

        ip_decap_addr_da = '192.168.0.1'
        decap_mac_da = '00:0f:00:0f:00:0f'
        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_decap_addr_da, decap_mac_da)
        
        warmboot(self.client)
        # send the test packet(s)
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=router_mac,
                                eth_src=decap_mac_da,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        pkt_only_ip1 = simple_ip_only_packet(pktlen=86,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=63,
                                ip_ihl=5)
        
        exp_pkt1 = simple_ipv4ip_packet(pktlen=106,
                         eth_dst=encap_mac_da,
                         eth_src=router_mac,
                         dl_vlan_enable=False,
                         vlan_vid=0,
                         vlan_pcp=0,
                         dl_vlan_cfi=0,
                         ip_src=ip_outer_addr_sa,
                         ip_dst=ip_outer_addr_da,
                         ip_tos=0,
                         ip_ecn=None,
                         ip_dscp=None,
                         ip_ttl=62,
                         ip_id=0x0000,
                         ip_flags=0x0,
                         ip_ihl=5,
                         ip_options=False,
                         inner_frame=pkt_only_ip1)
        
        pkt_only_ip2 = simple_ip_only_packet(pktlen=86,
                                ip_src=ip_encap_addr_da,
                                ip_dst=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=63,
                                ip_ihl=5)
        pkt2 = simple_ipv4ip_packet(pktlen=106,
                         eth_dst=router_mac,
                         eth_src=encap_mac_da,
                         dl_vlan_enable=False,
                         vlan_vid=0,
                         vlan_pcp=0,
                         dl_vlan_cfi=0,
                         ip_src=ip_outer_addr_da,
                         ip_dst=ip_outer_addr_sa,
                         ip_tos=0,
                         ip_ecn=None,
                         ip_dscp=None,
                         ip_ttl=62,
                         ip_id=0x0000,
                         ip_flags=0x0,
                         ip_ihl=5,
                         ip_options=False,
                         inner_frame=pkt_only_ip2)
        exp_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=decap_mac_da,
                                eth_src=router_mac,
                                ip_dst=ip_decap_addr_da,
                                ip_src=ip_encap_addr_da,
                                ip_id=105,
                                ip_ttl=62,
                                ip_ihl=5)
        m1_exp_pkt1=Mask(exp_pkt1)
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m1_exp_pkt1, 2)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( exp_pkt2, 1)
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_encap_addr_da, ip_mask, tunnel_nexthop_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_decap_addr_da, decap_mac_da)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_decap_id, ip_outer_addr_da, encap_mac_da)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)
            self.client.sai_thrift_remove_router_interface(rif_lp_outer_id)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            self.client.sai_thrift_remove_router_interface(rif_decap_id)

class TunnelCreateIpInIpTtlTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = router_mac
        outer_ttl=20
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        vr_id = sai_thrift_get_default_router_id(self.client)
        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        rif_lp_outer_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_decap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        tunnel_id = sai_thrift_create_tunnel(self.client, underlay_if=rif_lp_inner_id, overlay_if=rif_lp_outer_id, ip_addr=ip_outer_addr_sa, encap_ttl_mode=SAI_TUNNEL_TTL_MODE_PIPE_MODEL, encap_ttl_val=outer_ttl)
        print "tunnel_id = %lx" %tunnel_id

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id)
        print "tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id
        
        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);
        print "tunnel_nexthop_id = %lx" %tunnel_nexthop_id
        
        encap_mac_da = '00:0e:00:0e:00:0e'
        sai_thrift_create_neighbor(self.client, addr_family, rif_decap_id, ip_outer_addr_da, encap_mac_da)
        
        ip_encap_addr_da = '20.20.20.20'
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_encap_addr_da, ip_mask, tunnel_nexthop_id)  

        ip_decap_addr_da = '192.168.0.1'
        decap_mac_da = '00:0f:00:0f:00:0f'
        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_decap_addr_da, decap_mac_da)
        
        warmboot(self.client)
        # send the test packet(s)
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=router_mac,
                                eth_src=decap_mac_da,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        pkt_only_ip1 = simple_ip_only_packet(pktlen=86,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=63,
                                ip_ihl=5)
        
        exp_pkt1 = simple_ipv4ip_packet(pktlen=106,
                         eth_dst=encap_mac_da,
                         eth_src=router_mac,
                         dl_vlan_enable=False,
                         vlan_vid=0,
                         vlan_pcp=0,
                         dl_vlan_cfi=0,
                         ip_src=ip_outer_addr_sa,
                         ip_dst=ip_outer_addr_da,
                         ip_tos=0,
                         ip_ecn=None,
                         ip_dscp=None,
                         ip_ttl=outer_ttl-1,
                         ip_id=0x0000,
                         ip_flags=0x0,
                         ip_ihl=5,
                         ip_options=False,
                         inner_frame=pkt_only_ip1)
        m1_exp_pkt1=Mask(exp_pkt1)
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m1_exp_pkt1, 2)
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_encap_addr_da, ip_mask, tunnel_nexthop_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_decap_addr_da, decap_mac_da)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_decap_id, ip_outer_addr_da, encap_mac_da)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)
            self.client.sai_thrift_remove_router_interface(rif_lp_outer_id)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            self.client.sai_thrift_remove_router_interface(rif_decap_id)

class TunnelCreateIpInIpDscpTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = router_mac
        outer_dscp = 5
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        vr_id = sai_thrift_get_default_router_id(self.client)
        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        rif_lp_outer_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_decap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        tunnel_id = sai_thrift_create_tunnel(self.client, underlay_if=rif_lp_inner_id, overlay_if=rif_lp_outer_id, ip_addr=ip_outer_addr_sa, encap_dscp_mode=SAI_TUNNEL_DSCP_MODE_PIPE_MODEL, encap_dscp_val=outer_dscp)
        print "tunnel_id = %lx" %tunnel_id

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id)
        print "tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id
        
        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);
        print "tunnel_nexthop_id = %lx" %tunnel_nexthop_id
        
        encap_mac_da = '00:0e:00:0e:00:0e'
        sai_thrift_create_neighbor(self.client, addr_family, rif_decap_id, ip_outer_addr_da, encap_mac_da)
        
        ip_encap_addr_da = '20.20.20.20'
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_encap_addr_da, ip_mask, tunnel_nexthop_id)  

        ip_decap_addr_da = '192.168.0.1'
        decap_mac_da = '00:0f:00:0f:00:0f'
        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_decap_addr_da, decap_mac_da)
        
        warmboot(self.client)
        # send the test packet(s)
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=router_mac,
                                eth_src=decap_mac_da,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        pkt_only_ip1 = simple_ip_only_packet(pktlen=86,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=63,
                                ip_ihl=5)
        
        exp_pkt1 = simple_ipv4ip_packet(pktlen=106,
                         eth_dst=encap_mac_da,
                         eth_src=router_mac,
                         dl_vlan_enable=False,
                         vlan_vid=0,
                         vlan_pcp=0,
                         dl_vlan_cfi=0,
                         ip_src=ip_outer_addr_sa,
                         ip_dst=ip_outer_addr_da,
                         ip_tos=0,
                         ip_ecn=None,
                         ip_dscp=outer_dscp,
                         ip_ttl=62,
                         ip_id=0x0000,
                         ip_flags=0x0,
                         ip_ihl=5,
                         ip_options=False,
                         inner_frame=pkt_only_ip1)
        m1_exp_pkt1=Mask(exp_pkt1)
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m1_exp_pkt1, 2)
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_encap_addr_da, ip_mask, tunnel_nexthop_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_decap_addr_da, decap_mac_da)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_decap_id, ip_outer_addr_da, encap_mac_da)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)
            self.client.sai_thrift_remove_router_interface(rif_lp_outer_id)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            self.client.sai_thrift_remove_router_interface(rif_decap_id)
            
class TunnelCreateIpInIpGreTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = router_mac
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        gre_key_value=0x1111;
        vr_id = sai_thrift_get_default_router_id(self.client)
        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        rif_lp_outer_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_decap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        tunnel_id = sai_thrift_create_tunnel_gre(self.client, underlay_if=rif_lp_inner_id, overlay_if=rif_lp_outer_id, ip_addr=ip_outer_addr_sa, gre_key=gre_key_value)
        print "tunnel_id = %lx" %tunnel_id

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_IPINIP_GRE)
        print "tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id
        
        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);
        print "tunnel_nexthop_id = %lx" %tunnel_nexthop_id
        
        encap_mac_da = '00:0e:00:0e:00:0e'
        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
        
        ip_encap_addr_da = '20.20.20.20'
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_encap_addr_da, ip_mask, tunnel_nexthop_id)  

        ip_decap_addr_da = '192.168.0.1'
        decap_mac_da = '00:0f:00:0f:00:0f'
        sai_thrift_create_neighbor(self.client, addr_family, rif_decap_id, ip_decap_addr_da, decap_mac_da)
        
        warmboot(self.client)
        # send the test packet(s)
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=router_mac,
                                eth_src=decap_mac_da,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        pkt_only_ip1 = simple_ip_only_packet(pktlen=86,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=63,
                                ip_ihl=5)

        exp_pkt1 = simple_gre_packet(pktlen=114,
                         eth_dst=encap_mac_da,
                         eth_src=router_mac,
                         dl_vlan_enable=False,
                         vlan_vid=0,
                         vlan_pcp=0,
                         dl_vlan_cfi=0,
                         ip_src=ip_outer_addr_sa,
                         ip_dst=ip_outer_addr_da,
                         ip_tos=0,
                         ip_ecn=None,
                         ip_dscp=None,
                         ip_ttl=62,
                         ip_id=0x0000,
                         ip_flags=0x0,
                         ip_ihl=5,
                         ip_options=False,
                         gre_chksum_present=0,
                         gre_routing_present=0,
                         gre_key_present=1,
                         gre_seqnum_present=0,
                         gre_flags=0,
                         gre_version=0,
                         gre_offset=0,
                         gre_key=gre_key_value,
                         gre_sequence_number=0,
                         inner_frame=pkt_only_ip1)

        m1_exp_pkt1=Mask(exp_pkt1)
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')

        pkt_only_ip2 = simple_ip_only_packet(pktlen=86,
                                ip_src=ip_encap_addr_da,
                                ip_dst=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=63,
                                ip_ihl=5)
        pkt2 = simple_gre_packet(pktlen=114,
                         eth_dst=router_mac,
                         eth_src=encap_mac_da,
                         dl_vlan_enable=False,
                         vlan_vid=0,
                         vlan_pcp=0,
                         dl_vlan_cfi=0,
                         ip_src=ip_outer_addr_da,
                         ip_dst=ip_outer_addr_sa,
                         ip_tos=0,
                         ip_ecn=None,
                         ip_dscp=None,
                         ip_ttl=62,
                         ip_id=0x0000,
                         ip_flags=0x0,
                         ip_ihl=5,
                         ip_options=False,
                         gre_chksum_present=0,
                         gre_routing_present=0,
                         gre_key_present=1,
                         gre_seqnum_present=0,
                         gre_flags=0,
                         gre_version=0,
                         gre_offset=0,
                         gre_key=gre_key_value,
                         gre_sequence_number=0,
                         inner_frame=pkt_only_ip2)
        exp_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=decap_mac_da,
                                eth_src=router_mac,
                                ip_dst=ip_decap_addr_da,
                                ip_src=ip_encap_addr_da,
                                ip_id=105,
                                ip_ttl=62,
                                ip_ihl=5)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m1_exp_pkt1, 2)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( exp_pkt2, 1)
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_encap_addr_da, ip_mask, tunnel_nexthop_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_decap_id, ip_decap_addr_da, decap_mac_da)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)
            self.client.sai_thrift_remove_router_interface(rif_lp_outer_id)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            self.client.sai_thrift_remove_router_interface(rif_decap_id)

class TunnelCreateVxlanVlanMappingTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac=router_mac
        inner_mac_da = '00:00:AA:AA:00:00'
        inner_mac_sa = '00:00:AA:AA:11:11'
        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID
        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI
        vlan_id = 20
        vni_id = 1000
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        ip_encap_addr_da = '192.168.1.2'
        ip_decap_addr_da = '192.168.1.1'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
       
        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        print "tunnel_map_decap_id = %lx" %tunnel_map_decap_id
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
        print "tunnel_map_encap_id = %lx" %tunnel_map_encap_id
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, vlan_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, vlan_id, vni_id)
     
        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)
        print "tunnel_id = %lx" %tunnel_id

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_VXLAN)
        print "tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id
        
        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);
        print "tunnel_nexthop_id = %lx" %tunnel_nexthop_id
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        sai_thrift_create_fdb_tunnel(self.client, vlan_oid, inner_mac_da, btunnel_id, mac_action, ip_outer_addr_da)
        
        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        encap_mac_da = '00:0e:00:0e:00:0e'
        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
        
        sai_thrift_create_fdb(self.client, vlan_oid, inner_mac_sa, port1, mac_action)
        
        warmboot(self.client)
        # send the test packet(s)
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=inner_mac_da,
                                eth_src=inner_mac_sa,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        exp_pkt1 = simple_vxlan_packet(pktlen=300,
                        eth_dst=encap_mac_da,
                        eth_src=router_mac,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_sa,
                        ip_dst=ip_outer_addr_da,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=63,
                        ip_id=0x0001,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = pkt1)
        inner_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=inner_mac_sa,
                                eth_src=inner_mac_da,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        pkt2 = simple_vxlan_packet(pktlen=300,
                        eth_dst=router_mac,
                        eth_src=encap_mac_da,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_da,
                        ip_dst=ip_outer_addr_sa,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=63,
                        ip_id=0x0000,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = inner_pkt2)
        m_exp_pkt1=Mask(exp_pkt1)
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'chksum')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'sport')

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m_exp_pkt1, 2)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( inner_pkt2, 1)
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)
            sai_thrift_delete_fdb(self.client, vlan_oid, inner_mac_sa, port1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            sai_thrift_delete_fdb(self.client, vlan_oid, inner_mac_da, tunnel_id)
            self.client.sai_thrift_remove_bridge_port(btunnel_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class TunnelCreateVxlanBridgeMappingTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac=router_mac
        inner_mac_da = '00:00:AA:AA:00:00'
        inner_mac_sa = '00:00:AA:AA:11:11'
        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF
        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI
        vlan_id = 20
        vni_id = 1000
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        ip_encap_addr_da = '192.168.1.2'
        ip_decap_addr_da = '192.168.1.1'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)

        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        print "tunnel_map_decap_id = %lx" %tunnel_map_decap_id
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
        print "tunnel_map_encap_id = %lx" %tunnel_map_encap_id
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, bridge_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, bridge_id, vni_id)
     
        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)
        print "tunnel_id = %lx" %tunnel_id

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_VXLAN)
        print "tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id
        
        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);
        print "tunnel_nexthop_id = %lx" %tunnel_nexthop_id
        

        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        sai_thrift_create_fdb_tunnel(self.client, bridge_id, inner_mac_da, btunnel_id, mac_action, ip_outer_addr_da)
        
        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        encap_mac_da = '00:0e:00:0e:00:0e'
        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
        
        sai_thrift_create_fdb_bport(self.client, bridge_id, inner_mac_sa, bport1_id, mac_action)
        
        warmboot(self.client)
        # send the test packet(s)
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=inner_mac_da,
                                eth_src=inner_mac_sa,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        exp_pkt1 = simple_vxlan_packet(pktlen=300,
                        eth_dst=encap_mac_da,
                        eth_src=router_mac,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_sa,
                        ip_dst=ip_outer_addr_da,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=63,
                        ip_id=0x0000,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = pkt1)
        m1_exp_pkt1=Mask(exp_pkt1)
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'chksum')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'sport')
        inner_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=inner_mac_sa,
                                eth_src=inner_mac_da,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        pkt2 = simple_vxlan_packet(pktlen=300,
                        eth_dst=router_mac,
                        eth_src=encap_mac_da,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_da,
                        ip_dst=ip_outer_addr_sa,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=63,
                        ip_id=0x0000,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = inner_pkt2)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m1_exp_pkt1, 2)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( inner_pkt2, 1)
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id)
            sai_thrift_delete_fdb(self.client, bridge_id, inner_mac_sa, port1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            sai_thrift_delete_fdb(self.client, bridge_id, inner_mac_da, tunnel_id)
            self.client.sai_thrift_remove_bridge_port(btunnel_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
            self.client.sai_thrift_remove_bridge_port(bport1_id)
            self.client.sai_thrift_remove_bridge(bridge_id)

class TunnelCreateVxlanDefaultVrfMappingTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac=router_mac
        inner_mac_da = '00:00:AA:AA:00:00'
        inner_mac_sa = '00:00:AA:AA:11:11'
        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_VIRTUAL_ROUTER_ID
        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_VIRTUAL_ROUTER_ID_TO_VNI
        vlan_id = 20
        vni_id = 1000
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        ip_encap_addr_da = '192.168.2.2'
        ip_decap_addr_da = '192.168.1.1'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_decap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)

        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        print "tunnel_map_decap_id = %lx" %tunnel_map_decap_id
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
        print "tunnel_map_encap_id = %lx" %tunnel_map_encap_id
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, vr_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, vr_id, vni_id)
     
        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)
        print "tunnel_id = %lx" %tunnel_id

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_VXLAN)
        print "tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id
        
        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);
        print "tunnel_nexthop_id = %lx" %tunnel_nexthop_id
        
        encap_mac_da = '00:0e:00:0e:00:0e'
        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)

        encap_inner_mac_da = '00:0f:00:0f:00:0f'
        sai_thrift_create_neighbor(self.client, addr_family, rif_decap_id, ip_decap_addr_da, encap_inner_mac_da)        
    
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_encap_addr_da, ip_mask, tunnel_nexthop_id)
    
        warmboot(self.client)
        # send the test packet(s)
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=router_mac,
                                eth_src=inner_mac_sa,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
                                
        exp_pkt1 = simple_vxlan_packet(pktlen=300,
                        eth_dst=encap_mac_da,
                        eth_src=router_mac,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_sa,
                        ip_dst=ip_outer_addr_da,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=63,
                        ip_id=0x0000,
                        ip_flags=0x0,
                        udp_sport=49369,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = pkt1)
        m1_exp_pkt1=Mask(exp_pkt1)
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'chksum')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'sport')
        inner_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=router_mac,
                                eth_src=inner_mac_da,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_decap_addr_da,
                                ip_src=ip_encap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        pkt2 = simple_vxlan_packet(pktlen=300,
                        eth_dst=router_mac,
                        eth_src=encap_mac_da,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_da,
                        ip_dst=ip_outer_addr_sa,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=63,
                        ip_id=0x0000,
                        ip_flags=0x0,
                        udp_sport=49369,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = inner_pkt2)

        exp_pkt2 = simple_tcp_packet(pktlen=96,
                        eth_dst=encap_inner_mac_da,
                        eth_src=router_mac,
                        dl_vlan_enable=False,
                        ip_dst=ip_decap_addr_da,
                        ip_src=ip_encap_addr_da,
                        ip_id=105,
                        ip_ttl=63,
                        ip_ihl=5)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m1_exp_pkt1, 2)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( exp_pkt2, 1)
        finally:
            print "success"
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_encap_addr_da, ip_mask, tunnel_nexthop_id)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_decap_id, ip_decap_addr_da, encap_inner_mac_da)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            self.client.sai_thrift_remove_router_interface(rif_decap_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
            
class TunnelSetVxlanDefaultUdpPort(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print "start test"
        print "###################################################"
        print "get default vxlan udp port"
        switch_init(self.client)
        ids_list = [SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        print attr_list
        assert (attr_list[0].id == SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT), "Failed to get default vxlan udp port"
        assert(attr_list[0].value.u16 == 4789), "Get default udp port %d" % attr_list[0].value.u16
        print "###################################################"
        print "set default vxlan default port"
        attr_value = sai_thrift_attribute_value_t(u16=1234)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)
        print "###################################################"
        print "get default vxlan default port"
        ids_list = [SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        assert (attr_list[0].id == SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT), "Failed to get default vxlan udp port"
        assert(attr_list[0].value.u16 == 1234), "Get default udp port %d" % attr_list[0].value.u16
        # reset to default
        attr_value = sai_thrift_attribute_value_t(u16=4789)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)
        
class TunnelCreateVxlanCrossVniTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac=router_mac
        inner_mac_da = '00:00:AA:AA:00:00'
        inner_mac_sa = '00:00:AA:AA:11:11'
        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID
        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI
        vlan_id = 20
        vni_id = 1000
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        ip_encap_addr_da = '192.168.1.2'
        ip_decap_addr_da = '192.168.1.1'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
       
        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        print "tunnel_map_decap_id = %lx" %tunnel_map_decap_id
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
        print "tunnel_map_encap_id = %lx" %tunnel_map_encap_id
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, vlan_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, vlan_id, vni_id)
     
       # encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
       # decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        encap_mapper_list=[tunnel_map_encap_id]
        decap_mapper_list=[tunnel_map_decap_id] 
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)
        print "tunnel_id = %lx" %tunnel_id

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_VXLAN)
        print "tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id
        
        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id, vni_id, '00:11:22:33:44:55');
        print "tunnel_nexthop_id = %lx" %tunnel_nexthop_id
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        sai_thrift_create_fdb_tunnel(self.client, vlan_oid, inner_mac_da, btunnel_id, mac_action, ip_outer_addr_da)
        
        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        encap_mac_da = '00:0e:00:0e:00:0e'
        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
        
        sai_thrift_create_fdb(self.client, vlan_oid, inner_mac_sa, port1, mac_action)
        
        warmboot(self.client)
        # send the test packet(s)
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=inner_mac_da,
                                eth_src=inner_mac_sa,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        replace_da_pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst='00:11:22:33:44:55',
                                eth_src=inner_mac_sa,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=63,
                                ip_ihl=5)
                                
        exp_pkt1 = simple_vxlan_packet(pktlen=300,
                        eth_dst=encap_mac_da,
                        eth_src=router_mac,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_sa,
                        ip_dst=ip_outer_addr_da,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=62,
                        ip_id=0x0001,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = replace_da_pkt1)
        m_exp_pkt1=Mask(exp_pkt1)
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'chksum')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'sport')

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m_exp_pkt1, 2)
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)
            sai_thrift_delete_fdb(self.client, vlan_oid, inner_mac_sa, port1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            sai_thrift_delete_fdb(self.client, vlan_oid, inner_mac_da, tunnel_id)
            self.client.sai_thrift_remove_bridge_port(btunnel_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)            
        
        
        
class TunnelCreateVxlanVlanMappingWithWrongOrderTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ""
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac=router_mac
        inner_mac_da = '00:00:AA:AA:00:00'
        inner_mac_sa = '00:00:AA:AA:11:11'
        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID
        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI
        vlan_id = 20
        vni_id = 1000
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        ip_encap_addr_da = '192.168.1.2'
        ip_decap_addr_da = '192.168.1.1'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vr_id = sai_thrift_get_default_router_id(self.client)
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)
       
        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        print "tunnel_map_decap_id = %lx" %tunnel_map_decap_id
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
        print "tunnel_map_encap_id = %lx" %tunnel_map_encap_id
     
        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)
        print "tunnel_id = %lx" %tunnel_id

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_VXLAN)
        print "tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id
        # create term table entry before create tunnel map entry
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, vlan_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, vlan_id, vni_id)
        
        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);
        print "tunnel_nexthop_id = %lx" %tunnel_nexthop_id
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        sai_thrift_create_fdb_tunnel(self.client, vlan_oid, inner_mac_da, btunnel_id, mac_action, ip_outer_addr_da)
        
        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        encap_mac_da = '00:0e:00:0e:00:0e'
        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
        
        sai_thrift_create_fdb(self.client, vlan_oid, inner_mac_sa, port1, mac_action)
        
        warmboot(self.client)
        # send the test packet(s)
        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=inner_mac_da,
                                eth_src=inner_mac_sa,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        
        exp_pkt1 = simple_vxlan_packet(pktlen=300,
                        eth_dst=encap_mac_da,
                        eth_src=router_mac,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_sa,
                        ip_dst=ip_outer_addr_da,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=63,
                        ip_id=0x0001,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = pkt1)
        inner_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=inner_mac_sa,
                                eth_src=inner_mac_da,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        pkt2 = simple_vxlan_packet(pktlen=300,
                        eth_dst=router_mac,
                        eth_src=encap_mac_da,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_da,
                        ip_dst=ip_outer_addr_sa,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=63,
                        ip_id=0x0000,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = inner_pkt2)
        m_exp_pkt1=Mask(exp_pkt1)
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'chksum')
        m_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'sport')

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m_exp_pkt1, 2)
            print "second pkt"
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( inner_pkt2, 1)
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)
            sai_thrift_delete_fdb(self.client, vlan_oid, inner_mac_sa, port1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            sai_thrift_delete_fdb(self.client, vlan_oid, inner_mac_da, tunnel_id)
            self.client.sai_thrift_remove_bridge_port(btunnel_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)