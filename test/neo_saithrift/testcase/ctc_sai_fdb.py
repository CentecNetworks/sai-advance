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


fdb_attr = ['SAI_FDB_ENTRY_ATTR_TYPE',
            'SAI_FDB_ENTRY_ATTR_PACKET_ACTION',
            'SAI_FDB_ENTRY_ATTR_USER_TRAP_ID',
            'SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID',
            'SAI_FDB_ENTRY_ATTR_META_DATA',
            'SAI_FDB_ENTRY_ATTR_ENDPOINT_IP',
            'SAI_FDB_ENTRY_ATTR_COUNTER_ID',
            'SAI_FDB_ENTRY_ATTR_ALLOW_MAC_MOVE']

fdb_flush_attr = ['SAI_FDB_FLUSH_ATTR_BRIDGE_PORT_ID',
                  'SAI_FDB_FLUSH_ATTR_BV_ID',
                  'SAI_FDB_FLUSH_ATTR_ENTRY_TYPE']


def _set_fdb_attr(client, bv_id, mac, type=None, action=None, bport=None, meta_data=None):
    '''
    only one attribute can be set at the same time
    '''
    fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac, bv_id=bv_id)

    if type is not None:
        attr_value = sai_thrift_attribute_value_t(s32=type)
        attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
        status = client.sai_thrift_set_fdb_entry_attribute(thrift_fdb_entry=fdb_entry, thrift_attr=attr)
        sys_logging("### set %s to %s, status = 0x%x ###" %(fdb_attr[0], type, status))
        return status

    if action is not None:
        attr_value = sai_thrift_attribute_value_t(s32=action)
        attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
        status = client.sai_thrift_set_fdb_entry_attribute(thrift_fdb_entry=fdb_entry, thrift_attr=attr)
        sys_logging("### set %s to %s, status = 0x%x ###" %(fdb_attr[1], action, status))
        return status

    if bport is not None:
        attr_value = sai_thrift_attribute_value_t(oid=bport)
        attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
        status = client.sai_thrift_set_fdb_entry_attribute(thrift_fdb_entry=fdb_entry, thrift_attr=attr)
        sys_logging("### set %s to 0x%09x, status = 0x%x ###" %(fdb_attr[3], bport, status))
        return status

    if meta_data is not None:
        attr_value = sai_thrift_attribute_value_t(u32=meta_data)
        attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_META_DATA, value=attr_value)
        status = client.sai_thrift_set_fdb_entry_attribute(thrift_fdb_entry=fdb_entry, thrift_attr=attr)
        sys_logging("### set %s to %d, status = 0x%x ###" %(fdb_attr[4], meta_data, status))
        return status

def _get_fdb_attr(client, bv_id, mac, type=False, action=False, bport=False, meta_data=False):
    fdb_entry = sai_thrift_fdb_entry_t(mac_address=mac, bv_id=bv_id)
    fdb_attr_list = client.sai_thrift_get_fdb_entry_attribute(fdb_entry)
    if (SAI_STATUS_SUCCESS != fdb_attr_list.status):
        return None

    return_list = []
    attr_count = 0
    if type is True:
        attr_count += 1
    if action is True:
        attr_count += 1
    if bport is True:
        attr_count += 1
    if meta_data is True:
        attr_count += 1

    if type is True:
        for attr in fdb_attr_list.attr_list:
            if attr.id == SAI_FDB_ENTRY_ATTR_TYPE:
                sys_logging("### %s = %s ###" %(fdb_attr[0], attr.value.s32))
                if 1 == attr_count:
                    return attr.value.s32
                else:
                    return_list.append(attr.value.s32)

    if action is True:
        for attr in fdb_attr_list.attr_list:
            if attr.id == SAI_FDB_ENTRY_ATTR_PACKET_ACTION:
                sys_logging("### %s = %s ###" %(fdb_attr[1], attr.value.s32))
                if 1 == attr_count:
                    return attr.value.s32
                else:
                    return_list.append(attr.value.s32)

    if bport is True:
        for attr in fdb_attr_list.attr_list:
            if attr.id == SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID:
                sys_logging("### %s = 0x%09x ###" %(fdb_attr[3], attr.value.oid))
                if 1 == attr_count:
                    return attr.value.oid
                else:
                    return_list.append(attr.value.oid)

    if meta_data is True:
        for attr in fdb_attr_list.attr_list:
            if attr.id == SAI_FDB_ENTRY_ATTR_META_DATA:
                sys_logging("### %s = %d ###" %(fdb_attr[4], attr.value.u32))
                if 1 == attr_count:
                    return attr.value.u32
                else:
                    return_list.append(attr.value.u32)

    return return_list


@group('L2')
class func_01_create_fdb_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        TBD: SAI_BRIDGE_PORT_TYPE_TUNNEL
        '''
        sys_logging("### -----func_01_create_fdb_entry_fn----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### bridge port 1 = 0x%09x ###" %bport1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)
        sys_logging("### bridge port 2 = 0x%09x ###" %bport2)
        bport3 = sai_thrift_get_bridge_port_by_port(self.client, port3)
        sys_logging("### bridge port 3 = 0x%09x ###" %bport3)

        vlan1 = 100
        vlan_id = sai_thrift_create_vlan(self.client, vlan1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan2 = 200
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan2)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan2)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan2)

        attr_value = sai_thrift_attribute_value_t(u16=vlan1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(pkt1, [1,2])

            status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac2, bport2)
            sys_logging("### create fdb entry with bridge port of type PORT, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packets(pkt2, [1,2])

            status = sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_port2)
            sys_logging("### create fdb entry with bridge port of type SUB_PORT, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)
            self.ctc_verify_no_packet(pkt2, 2)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_id)


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


@group('L2')
class func_04_create_same_fdb_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        No exception will happen after creating same fdb entry
        '''
        sys_logging("### -----func_04_create_same_fdb_entry_fn----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### bridge port 1 = 0x%09x ###" %bport1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)
        sys_logging("### bridge port 2 = 0x%09x ###" %bport2)
        bport3 = sai_thrift_get_bridge_port_by_port(self.client, port3)
        sys_logging("### bridge port 3 = 0x%09x ###" %bport3)

        vlan1 = 100
        vlan_id = sai_thrift_create_vlan(self.client, vlan1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan2 = 200
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan2)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan2)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan2)

        attr_value = sai_thrift_attribute_value_t(u16=vlan1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac2, bport2)
            sys_logging("### create FDB entry with bridge port of type PORT, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac2, bport2)
            sys_logging("### create same FDB entry with bridge port of type PORT, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)

            status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac1, bport1, type=SAI_FDB_ENTRY_TYPE_DYNAMIC)
            sys_logging("### create FDB entry with bridge port of type PORT, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            status = sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_port2)
            sys_logging("### create FDB entry with bridge port of type SUB_PORT, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            status = sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_port2)
            sys_logging("### create same FDB entry with bridge port of type SUB_PORT, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)
            self.ctc_verify_no_packet(pkt2, 2)

            status = sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, sub_port1, type=SAI_FDB_ENTRY_TYPE_DYNAMIC)
            sys_logging("### create FDB entry with bridge port of type SUB_PORT, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_05_create_error_fdb_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112533
        '''
        sys_logging("### -----func_05_create_error_fdb_entry_fn----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        mac1 = '00:11:11:11:11:11'
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        try:
            not_exist_vlan_id = 8589934630
            status = sai_thrift_create_fdb(self.client, not_exist_vlan_id, mac1, port1)
            sys_logging("### create FDB entry with invalid vlan_id, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

            not_exist_bridge_id = 8589942841
            status = sai_thrift_create_fdb(self.client, not_exist_bridge_id, mac1, port1)
            sys_logging("### create FDB entry with invalid bridge_id, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

            not_exist_bridge_port = 4294975546
            status = sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, not_exist_bridge_port)
            sys_logging("### create FDB entry with invalid bridge_port_id, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

            status = sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, SAI_NULL_OBJECT_ID)
            sys_logging("### create FDB entry with null bridge_port_id, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

        finally:
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_06_remove_fdb_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_remove_fdb_entry_fn----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        vlan1 = 100
        vlan_id = sai_thrift_create_vlan(self.client, vlan1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan2 = 200
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan2)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan2)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan2)

        attr_value = sai_thrift_attribute_value_t(u16=vlan1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb(self.client, vlan_id, mac2, port2))

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)

            status = sai_thrift_delete_fdb(self.client, vlan_id, mac2)
            sys_logging("### delete FDB entry, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(pkt1, [1,2])

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac1))
            status = sai_thrift_delete_fdb(self.client, vlan_id, mac1)
            sys_logging("### delete learned FDB entry, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_port2))

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)
            self.ctc_verify_no_packet(pkt2, 2)

            status = sai_thrift_delete_fdb(self.client, bridge_id, mac2)
            sys_logging("### delete FDB entry, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packets(pkt2, [1,2])

            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            status = sai_thrift_delete_fdb(self.client, bridge_id, mac1)
            sys_logging("### delete learned FDB entry, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_07_remove_not_exist_fdb_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_07_remove_not_exist_fdb_entry_fn----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        vlan1 = 100
        vlan2 = 200
        vlan_id1 = sai_thrift_create_vlan(self.client, vlan1)
        vlan_id2 = sai_thrift_create_vlan(self.client, vlan2)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id1, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan3 = 300
        vlan4 = 400
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan3)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan3)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id1, vlan3)

        attr_value = sai_thrift_attribute_value_t(u16=vlan1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan3,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb(self.client, vlan_id1, mac2, port2))

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)

            status = sai_thrift_delete_fdb(self.client, vlan_id1, mac3)
            sys_logging("### delete FDB entry with invalid mac, status = 0x%x ###" %status)
            assert(SAI_STATUS_ITEM_NOT_FOUND == status)

            status = sai_thrift_delete_fdb(self.client, vlan_id2, mac2)
            sys_logging("### delete FDB entry with invalid bv_id, status = 0x%x ###" %status)
            assert(SAI_STATUS_ITEM_NOT_FOUND == status)

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id1, mac2, sub_port2))

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)
            self.ctc_verify_no_packet(pkt2, 2)

            status = sai_thrift_delete_fdb(self.client, bridge_id1, mac3)
            sys_logging("### delete FDB entry with invalid mac, status = 0x%x ###" %status)
            assert(SAI_STATUS_ITEM_NOT_FOUND == status)

            status = sai_thrift_delete_fdb(self.client, bridge_id2, mac2)
            sys_logging("### delete FDB entry with invalid bv_id, status = 0x%x ###" %status)
            assert(SAI_STATUS_ITEM_NOT_FOUND == status)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_id1)
            self.client.sai_thrift_remove_vlan(vlan_id2)


@group('L2')
class func_08_set_and_get_fdb_entry_attribute_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112612
        '''
        sys_logging("### -----func_08_set_and_get_fdb_entry_attribute_fn_0----- ###")
        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        vlan1 = 100
        vlan_id = sai_thrift_create_vlan(self.client, vlan1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan2 = 200
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan2)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan2)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan2)

        attr_value = sai_thrift_attribute_value_t(u16=vlan1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb(self.client, vlan_id, mac2, port2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac2))
            assert(type_list[1] == _get_fdb_attr(self.client, vlan_id, mac2, type=True))

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)

            assert(SAI_STATUS_SUCCESS != _set_fdb_attr(self.client, vlan_id, mac2, type=type_list[0]))
            sys_logging("### static FDB entry cannot be changed to dynamic ###")
            assert(type_list[1] == _get_fdb_attr(self.client, vlan_id, mac2, type=True))

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac1))
            assert(type_list[0] == _get_fdb_attr(self.client, vlan_id, mac1, type=True))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac1, type=type_list[1]))
            sys_logging("### dynamic FDB entry can be changed to static ###")
            assert(type_list[1] == _get_fdb_attr(self.client, vlan_id, mac1, type=True))

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_port2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac2))
            assert(type_list[1] == _get_fdb_attr(self.client, bridge_id, mac2, type=True))

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)
            self.ctc_verify_no_packet(pkt2, 2)

            assert(SAI_STATUS_SUCCESS != _set_fdb_attr(self.client, bridge_id, mac2, type=type_list[0]))
            sys_logging("### static FDB entry cannot be changed to dynamic ###")
            assert(type_list[1] == _get_fdb_attr(self.client, bridge_id, mac2, type=True))

            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(type_list[0] == _get_fdb_attr(self.client, bridge_id, mac1, type=True))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac1, type=type_list[1]))
            sys_logging("### dynamic FDB entry can be changed to static ###")
            assert(type_list[1] == _get_fdb_attr(self.client, bridge_id, mac1, type=True))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_08_set_and_get_fdb_entry_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112515, SAI Bug 112612
        '''
        sys_logging("### -----func_08_set_and_get_fdb_entry_attribute_fn_1----- ###")
        action_list = [SAI_PACKET_ACTION_DROP, SAI_PACKET_ACTION_FORWARD,
                       SAI_PACKET_ACTION_COPY, SAI_PACKET_ACTION_COPY_CANCEL,
                       SAI_PACKET_ACTION_TRAP, SAI_PACKET_ACTION_LOG,
                       SAI_PACKET_ACTION_DENY, SAI_PACKET_ACTION_TRANSIT]
        switch_init(self.client)
        #self.client.sai_thrift_clear_cpu_packet_info()

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        vlan = 100
        vlan_id = sai_thrift_create_vlan(self.client, vlan)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan2 = 200
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan2)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan2)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan2)

        attr_value = sai_thrift_attribute_value_t(u16=vlan)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb(self.client, vlan_id, mac2, port2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac2))
            assert(action_list[7] == _get_fdb_attr(self.client, vlan_id, mac2, action=True))

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)
            assert(0 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, action=action_list[2]))
            assert(action_list[5] == _get_fdb_attr(self.client, vlan_id, mac2, action=True))

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)
            assert(1 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, action=action_list[0]))
            assert(action_list[4] == _get_fdb_attr(self.client, vlan_id, mac2, action=True))

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)
            assert(1 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, action=action_list[3]))
            assert(action_list[6] == _get_fdb_attr(self.client, vlan_id, mac2, action=True))

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)
            assert(0 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, action=action_list[1]))
            assert(action_list[7] == _get_fdb_attr(self.client, vlan_id, mac2, action=True))

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)
            assert(0 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_port2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac2))
            assert(action_list[7] == _get_fdb_attr(self.client, bridge_id, mac2, action=True))

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)
            self.ctc_verify_no_packet(pkt2, 2)
            assert(0 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, action=action_list[2]))
            assert(action_list[5] == _get_fdb_attr(self.client, bridge_id, mac2, action=True))

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)
            self.ctc_verify_no_packet(pkt2, 2)
            assert(1 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, action=action_list[0]))
            assert(action_list[4] == _get_fdb_attr(self.client, bridge_id, mac2, action=True))

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_no_packet(pkt2, 1)
            self.ctc_verify_no_packet(pkt2, 2)
            assert(1 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, action=action_list[3]))
            assert(action_list[6] == _get_fdb_attr(self.client, bridge_id, mac2, action=True))

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_no_packet(pkt2, 1)
            self.ctc_verify_no_packet(pkt2, 2)
            assert(0 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, action=action_list[1]))
            assert(action_list[7] == _get_fdb_attr(self.client, bridge_id, mac2, action=True))

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)
            self.ctc_verify_no_packet(pkt2, 2)
            assert(0 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_08_set_and_get_fdb_entry_attribute_fn_3(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112533
        '''
        sys_logging("### -----func_08_set_and_get_fdb_entry_attribute_fn_3----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)
        bport3 = sai_thrift_get_bridge_port_by_port(self.client, port3)

        vlan1 = 100
        vlan_id = sai_thrift_create_vlan(self.client, vlan1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan2 = 200
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan2)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan2)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan2)

        attr_value = sai_thrift_attribute_value_t(u16=vlan1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id, mac2, bport2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac2))
            assert(bport2 == _get_fdb_attr(self.client, vlan_id, mac2, bport=True))

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, bport=bport3))
            assert(bport3 == _get_fdb_attr(self.client, vlan_id, mac2, bport=True))

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 1)
            self.ctc_verify_packet(pkt1, 2)

            assert(SAI_STATUS_SUCCESS != _set_fdb_attr(self.client, vlan_id, mac2, bport=SAI_NULL_OBJECT_ID))
            assert(bport3 == _get_fdb_attr(self.client, vlan_id, mac2, bport=True))

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_port2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac2))
            assert(sub_port2 == _get_fdb_attr(self.client, bridge_id, mac2, bport=True))

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)
            self.ctc_verify_no_packet(pkt2, 2)

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, bport=sub_port3))
            assert(sub_port3 == _get_fdb_attr(self.client, bridge_id, mac2, bport=True))

            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_no_packet(pkt2, 1)
            self.ctc_verify_packet(pkt2, 2)

            assert(SAI_STATUS_SUCCESS != _set_fdb_attr(self.client, bridge_id, mac2, bport=SAI_NULL_OBJECT_ID))
            assert(sub_port3 == _get_fdb_attr(self.client, bridge_id, mac2, bport=True))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_08_set_and_get_fdb_entry_attribute_fn_4(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        valid meta_data: tsingma = 0~253; tsingma_mx = 0~65534
        SAI Bug 112659
        SAI Bug 112612
        '''
        sys_logging("### -----func_08_set_and_get_fdb_entry_attribute_fn_4----- ###")
        switch_init(self.client)

        id_list = [SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(id_list)
        for attribute in switch_attr_list.attr_list:
            if attribute.id == SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE:
                sys_logging("### SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE = %d ~ %d ###"
                            %(attribute.value.u32range.min, attribute.value.u32range.max))
                meta_data_range =[attribute.value.u32range.min, attribute.value.u32range.max]

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)
        bport3 = sai_thrift_get_bridge_port_by_port(self.client, port3)

        vlan1 = 100
        vlan_id = sai_thrift_create_vlan(self.client, vlan1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan2 = 200
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan2)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan2)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan2)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        warmboot(self.client)

        try:
            default_meta_data = 0
            chipname = testutils.test_params_get()['chipname']
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id, mac2, bport2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac2))
            assert(default_meta_data == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))

            meta_data1 = 253
            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data1))
            assert(meta_data1 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))

            meta_data2 = 254
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS != _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data2))
                assert(meta_data1 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data2))
                assert(meta_data2 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))

            meta_data3 = 65534
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS != _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data3))
                assert(meta_data1 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data3))
                assert(meta_data3 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))

            meta_data3 = 65535
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data3))
                assert(0 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data3))
                assert(0 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))

            meta_data3 = 65536
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data3))
                assert(0 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data3))
                assert(0 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))

            meta_data3 = 65537
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data3))
                assert(1 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data3))
                assert(1 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))

            meta_data3 = 66536
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS != _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data3))
                assert(1 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, meta_data=meta_data3))
                assert(1000 == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, meta_data=default_meta_data))
            assert(default_meta_data == _get_fdb_attr(self.client, vlan_id, mac2, meta_data=True))

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_port2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac2))
            assert(0 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))

            meta_data1 = 253
            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data1))
            assert(meta_data1 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))

            meta_data2 = 254
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS != _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data2))
                assert(meta_data1 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data2))
                assert(meta_data2 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))

            meta_data3 = 65534
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS != _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data3))
                assert(meta_data1 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data3))
                assert(meta_data3 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))

            meta_data3 = 65535
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data3))
                assert(0 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data3))
                assert(0 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))

            meta_data3 = 65536
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data3))
                assert(0 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data3))
                assert(0 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))

            meta_data3 = 65537
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data3))
                assert(1 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data3))
                assert(1 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))

            meta_data3 = 66536
            if 'tsingma' == chipname:
                assert(SAI_STATUS_SUCCESS != _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data3))
                assert(1 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))
            elif 'tsingma_mx' == chipname:
                assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, meta_data=meta_data3))
                assert(1000 == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac2, meta_data=default_meta_data))
            assert(default_meta_data == _get_fdb_attr(self.client, bridge_id, mac2, meta_data=True))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_09_flush_fdb_entries_fn_by_bridge_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112614
        '''
        sys_logging("### -----func_09_flush_fdb_entries_fn_by_bridge_port----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan1 = 100
        vlan2 = 200
        vlan_id1 = sai_thrift_create_vlan(self.client, vlan1)
        vlan_id2 = sai_thrift_create_vlan(self.client, vlan2)

        vlan3 = 300
        vlan4 = 400
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan3)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan3)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan4)
        sub_port4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan4)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        mac4 = '00:44:44:44:44:44'
        mac9 = '00:99:99:99:99:99'

        pkt1 = simple_tcp_packet(eth_dst=mac9, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac9, eth_src=mac2,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst=mac9, eth_src=mac3,
                                 dl_vlan_enable=True, vlan_vid=vlan1,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst=mac9, eth_src=mac4,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        pkt5 = simple_tcp_packet(eth_dst=mac9, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan3,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt6 = simple_tcp_packet(eth_dst=mac9, eth_src=mac2,
                                 dl_vlan_enable=True, vlan_vid=vlan4,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt7 = simple_tcp_packet(eth_dst=mac9, eth_src=mac3,
                                 dl_vlan_enable=True, vlan_vid=vlan3,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt8 = simple_tcp_packet(eth_dst=mac9, eth_src=mac4,
                                 dl_vlan_enable=True, vlan_vid=vlan4,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        type1 = 'DYNAMIC'
        type2 = 'STATIC'
        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            sys_logging("********************************************************")
            sys_logging("*        mac            bv_id     bridge port    type  *")
            sys_logging("* -----------------  -----------  -----------  ------- *")
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,vlan_id1,bport1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,vlan_id2,bport1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,vlan_id1,bport1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,vlan_id2,bport1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,vlan_id1,bport2,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,vlan_id2,bport2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,vlan_id1,bport2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,vlan_id2,bport2,type1))
            sys_logging("********************************************************")

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id2, mac1, bport1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id1, mac2, bport1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id2, mac3, bport2))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id1, mac4, bport2))

            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            self.ctc_send_packet(0, pkt1)
            self.ctc_send_packet(0, pkt2)
            self.ctc_send_packet(1, pkt3)
            self.ctc_send_packet(1, pkt4)

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=bport1)
            sys_logging("### flush fdb entries by bridge port 1 and type of default ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=bport1, type=SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            sys_logging("### flush fdb entries by bridge port 1 and type of static ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=bport2, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            sys_logging("### flush fdb entries by bridge port 2 and type of all ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            sys_logging("********************************************************")
            sys_logging("*        mac            bv_id     bridge port    type  *")
            sys_logging("* -----------------  -----------  -----------  ------- *")
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,bridge_id1,sub_port1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,bridge_id2,sub_port3,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,bridge_id1,sub_port1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,bridge_id2,sub_port3,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,bridge_id1,sub_port2,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,bridge_id2,sub_port4,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,bridge_id1,sub_port2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,bridge_id2,sub_port4,type1))
            sys_logging("********************************************************")

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id2, mac1, sub_port3))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id1, mac2, sub_port1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id2, mac3, sub_port4))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id1, mac4, sub_port2))

            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            self.ctc_send_packet(0, pkt5)
            self.ctc_send_packet(0, pkt6)
            self.ctc_send_packet(1, pkt7)
            self.ctc_send_packet(1, pkt8)

            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=sub_port1)
            sys_logging("### flush fdb entries by sub bridge port 1 and type of default ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            sai_thrift_flush_fdb(self.client, bport_id=sub_port3)
            sys_logging("### flush fdb entries by sub bridge port 3 and type of default ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=sub_port1, type=SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            sys_logging("### flush fdb entries by sub bridge port 1 and type of static ###")
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            sai_thrift_flush_fdb(self.client, bport_id=sub_port3, type=SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            sys_logging("### flush fdb entries by sub bridge port 3 and type of static ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=sub_port2, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            sys_logging("### flush fdb entries by sub bridge port 2 and type of all ###")
            sai_thrift_flush_fdb(self.client, bport_id=sub_port4, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            sys_logging("### flush fdb entries by sub bridge port 4 and type of all ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge_port(sub_port4)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            self.client.sai_thrift_remove_vlan(vlan_id1)
            self.client.sai_thrift_remove_vlan(vlan_id2)


@group('L2')
class func_09_flush_fdb_entries_fn_by_bv_id(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112614
        '''
        sys_logging("### -----func_09_flush_fdb_entries_fn_by_bv_id----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan1 = 100
        vlan2 = 200
        vlan_id1 = sai_thrift_create_vlan(self.client, vlan1)
        vlan_id2 = sai_thrift_create_vlan(self.client, vlan2)

        vlan3 = 300
        vlan4 = 400
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan3)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan3)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan4)
        sub_port4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan4)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        mac4 = '00:44:44:44:44:44'
        mac9 = '00:99:99:99:99:99'

        pkt1 = simple_tcp_packet(eth_dst=mac9, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac9, eth_src=mac2,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst=mac9, eth_src=mac3,
                                 dl_vlan_enable=True, vlan_vid=vlan1,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst=mac9, eth_src=mac4,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        pkt5 = simple_tcp_packet(eth_dst=mac9, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan3,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt6 = simple_tcp_packet(eth_dst=mac9, eth_src=mac2,
                                 dl_vlan_enable=True, vlan_vid=vlan4,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt7 = simple_tcp_packet(eth_dst=mac9, eth_src=mac3,
                                 dl_vlan_enable=True, vlan_vid=vlan3,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt8 = simple_tcp_packet(eth_dst=mac9, eth_src=mac4,
                                 dl_vlan_enable=True, vlan_vid=vlan4,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        type1 = 'DYNAMIC'
        type2 = 'STATIC'
        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            sys_logging("********************************************************")
            sys_logging("*        mac            bv_id     bridge port    type  *")
            sys_logging("* -----------------  -----------  -----------  ------- *")
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,vlan_id1,bport1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,vlan_id2,bport1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,vlan_id1,bport1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,vlan_id2,bport1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,vlan_id1,bport2,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,vlan_id2,bport2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,vlan_id1,bport2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,vlan_id2,bport2,type1))
            sys_logging("********************************************************")

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id2, mac1, bport1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id1, mac2, bport1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id2, mac3, bport2))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id1, mac4, bport2))

            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            self.ctc_send_packet(0, pkt1)
            self.ctc_send_packet(0, pkt2)
            self.ctc_send_packet(1, pkt3)
            self.ctc_send_packet(1, pkt4)

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            sai_thrift_flush_fdb(self.client, bv_id=vlan_id1)
            sys_logging("### flush fdb entries by vlan 1 and type of default ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            sai_thrift_flush_fdb(self.client, bv_id=vlan_id1, type=SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            sys_logging("### flush fdb entries by vlan 1 and type of static ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            sai_thrift_flush_fdb(self.client, bv_id=vlan_id2, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            sys_logging("### flush fdb entries by vlan 2 and type of all ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            sys_logging("********************************************************")
            sys_logging("*        mac            bv_id     bridge port    type  *")
            sys_logging("* -----------------  -----------  -----------  ------- *")
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,bridge_id1,sub_port1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,bridge_id2,sub_port3,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,bridge_id1,sub_port1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,bridge_id2,sub_port3,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,bridge_id1,sub_port2,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,bridge_id2,sub_port4,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,bridge_id1,sub_port2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,bridge_id2,sub_port4,type1))
            sys_logging("********************************************************")

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id2, mac1, sub_port3))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id1, mac2, sub_port1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id2, mac3, sub_port4))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id1, mac4, sub_port2))

            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            self.ctc_send_packet(0, pkt5)
            self.ctc_send_packet(0, pkt6)
            self.ctc_send_packet(1, pkt7)
            self.ctc_send_packet(1, pkt8)

            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            sai_thrift_flush_fdb(self.client, bv_id=bridge_id1)
            sys_logging("### flush fdb entries by bridge 1 and type of default ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            sai_thrift_flush_fdb(self.client, bv_id=bridge_id1, type=SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            sys_logging("### flush fdb entries by bridge 1 and type of static ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            sai_thrift_flush_fdb(self.client, bv_id=bridge_id2, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            sys_logging("### flush fdb entries by bridge 2 and type of all ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge_port(sub_port4)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            self.client.sai_thrift_remove_vlan(vlan_id1)
            self.client.sai_thrift_remove_vlan(vlan_id2)


@group('L2')
class func_09_flush_fdb_entries_fn_by_bport_and_bvid(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112614
        '''
        sys_logging("### -----func_09_flush_fdb_entries_fn_by_bport_and_bvid----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan1 = 100
        vlan2 = 200
        vlan_id1 = sai_thrift_create_vlan(self.client, vlan1)
        vlan_id2 = sai_thrift_create_vlan(self.client, vlan2)

        vlan3 = 300
        vlan4 = 400
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan3)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan3)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan4)
        sub_port4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan4)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        mac4 = '00:44:44:44:44:44'
        mac9 = '00:99:99:99:99:99'

        pkt1 = simple_tcp_packet(eth_dst=mac9, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac9, eth_src=mac2,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst=mac9, eth_src=mac3,
                                 dl_vlan_enable=True, vlan_vid=vlan1,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst=mac9, eth_src=mac4,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        pkt5 = simple_tcp_packet(eth_dst=mac9, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan3,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt6 = simple_tcp_packet(eth_dst=mac9, eth_src=mac2,
                                 dl_vlan_enable=True, vlan_vid=vlan4,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt7 = simple_tcp_packet(eth_dst=mac9, eth_src=mac3,
                                 dl_vlan_enable=True, vlan_vid=vlan3,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt8 = simple_tcp_packet(eth_dst=mac9, eth_src=mac4,
                                 dl_vlan_enable=True, vlan_vid=vlan4,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        type1 = 'DYNAMIC'
        type2 = 'STATIC'
        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            sys_logging("********************************************************")
            sys_logging("*        mac            bv_id     bridge port    type  *")
            sys_logging("* -----------------  -----------  -----------  ------- *")
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,vlan_id1,bport1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,vlan_id2,bport1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,vlan_id1,bport1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,vlan_id2,bport1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,vlan_id1,bport2,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,vlan_id2,bport2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,vlan_id1,bport2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,vlan_id2,bport2,type1))
            sys_logging("********************************************************")

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id2, mac1, bport1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id1, mac2, bport1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id2, mac3, bport2))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id1, mac4, bport2))

            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            self.ctc_send_packet(0, pkt1)
            self.ctc_send_packet(0, pkt2)
            self.ctc_send_packet(1, pkt3)
            self.ctc_send_packet(1, pkt4)

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=bport1, bv_id=vlan_id1)
            sys_logging("### flush fdb entries by bridge port 1, vlan 1 and type of default ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=bport1, bv_id=vlan_id1, type=SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            sys_logging("### flush fdb entries by bridge port 1, vlan 1 and type of static ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=bport2, bv_id=vlan_id2, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            sys_logging("### flush fdb entries by bridge port 2, vlan 2 and type of static ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            sys_logging("********************************************************")
            sys_logging("*        mac            bv_id     bridge port    type  *")
            sys_logging("* -----------------  -----------  -----------  ------- *")
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,bridge_id1,sub_port1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,bridge_id2,sub_port3,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,bridge_id1,sub_port1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,bridge_id2,sub_port3,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,bridge_id1,sub_port2,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,bridge_id2,sub_port4,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,bridge_id1,sub_port2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,bridge_id2,sub_port4,type1))
            sys_logging("********************************************************")

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id2, mac1, sub_port3))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id1, mac2, sub_port1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id2, mac3, sub_port4))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id1, mac4, sub_port2))

            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            self.ctc_send_packet(0, pkt5)
            self.ctc_send_packet(0, pkt6)
            self.ctc_send_packet(1, pkt7)
            self.ctc_send_packet(1, pkt8)

            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=sub_port1, bv_id=bridge_id1)
            sys_logging("### flush fdb entries by sub bridge port 1, bridge 1 and type of default ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=sub_port1, bv_id=bridge_id1, type=SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            sys_logging("### flush fdb entries by sub bridge port 1, bridge 1 and type of static ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            sai_thrift_flush_fdb(self.client, bport_id=sub_port4, bv_id=bridge_id2, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            sys_logging("### flush fdb entries by sub bridge port 4, bridge 2 and type of all ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge_port(sub_port4)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            self.client.sai_thrift_remove_vlan(vlan_id1)
            self.client.sai_thrift_remove_vlan(vlan_id2)


@group('L2')
class func_09_flush_fdb_entries_fn_by_type(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112614
        '''
        sys_logging("### -----func_09_flush_fdb_entries_fn_by_type----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan1 = 100
        vlan2 = 200
        vlan_id1 = sai_thrift_create_vlan(self.client, vlan1)
        vlan_id2 = sai_thrift_create_vlan(self.client, vlan2)

        vlan3 = 300
        vlan4 = 400
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan3)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan3)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan4)
        sub_port4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan4)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        mac4 = '00:44:44:44:44:44'
        mac9 = '00:99:99:99:99:99'

        pkt1 = simple_tcp_packet(eth_dst=mac9, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac9, eth_src=mac2,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst=mac9, eth_src=mac3,
                                 dl_vlan_enable=True, vlan_vid=vlan1,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst=mac9, eth_src=mac4,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        pkt5 = simple_tcp_packet(eth_dst=mac9, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan3,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt6 = simple_tcp_packet(eth_dst=mac9, eth_src=mac2,
                                 dl_vlan_enable=True, vlan_vid=vlan4,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt7 = simple_tcp_packet(eth_dst=mac9, eth_src=mac3,
                                 dl_vlan_enable=True, vlan_vid=vlan3,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt8 = simple_tcp_packet(eth_dst=mac9, eth_src=mac4,
                                 dl_vlan_enable=True, vlan_vid=vlan4,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        type1 = 'DYNAMIC'
        type2 = 'STATIC'
        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            sys_logging("********************************************************")
            sys_logging("*        mac            bv_id     bridge port    type  *")
            sys_logging("* -----------------  -----------  -----------  ------- *")
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,vlan_id1,bport1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,vlan_id2,bport1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,vlan_id1,bport1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,vlan_id2,bport1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,vlan_id1,bport2,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,vlan_id2,bport2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,vlan_id1,bport2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,vlan_id2,bport2,type1))
            sys_logging("********************************************************")

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id2, mac1, bport1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id1, mac2, bport1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id2, mac3, bport2))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id1, mac4, bport2))

            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            self.ctc_send_packet(0, pkt1)
            self.ctc_send_packet(0, pkt2)
            self.ctc_send_packet(1, pkt3)
            self.ctc_send_packet(1, pkt4)

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            sai_thrift_flush_fdb(self.client)
            sys_logging("### flush fdb entries by type of default ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            sys_logging("### flush fdb entries by type of static ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id2, mac4))

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            sys_logging("********************************************************")
            sys_logging("*        mac            bv_id     bridge port    type  *")
            sys_logging("* -----------------  -----------  -----------  ------- *")
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,bridge_id1,sub_port1,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac1,bridge_id2,sub_port3,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,bridge_id1,sub_port1,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac2,bridge_id2,sub_port3,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,bridge_id1,sub_port2,type1))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac3,bridge_id2,sub_port4,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,bridge_id1,sub_port2,type2))
            sys_logging("* %s  0x%09x  0x%09x  %7s *" %(mac4,bridge_id2,sub_port4,type1))
            sys_logging("********************************************************")

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id2, mac1, sub_port3))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id1, mac2, sub_port1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id2, mac3, sub_port4))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id1, mac4, sub_port2))

            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            self.ctc_send_packet(0, pkt5)
            self.ctc_send_packet(0, pkt6)
            self.ctc_send_packet(1, pkt7)
            self.ctc_send_packet(1, pkt8)

            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            sai_thrift_flush_fdb(self.client)
            sys_logging("### flush fdb entries by type of default ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_STATIC)
            sys_logging("### flush fdb entries by type of static ###")
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac2))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac3))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac4))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id2, mac4))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge_port(sub_port4)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            self.client.sai_thrift_remove_vlan(vlan_id1)
            self.client.sai_thrift_remove_vlan(vlan_id2)


@group('L2')
class func_10_create_fdb_entries_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112496
        '''
        sys_logging("### -----func_10_create_fdb_entries_fn----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        bulk_attr_list = []
        attr_list = []
        for i in range(0,16):
            bulk_attr_list.append([])
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])
            bulk_attr_list[i] = sai_thrift_attribute_list_t(attr_list=attr_list[i])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            status = self.client.sai_thrift_create_fdb_entries(fdb_entry_list, bulk_attr_list, mode_list[1])
            sys_logging("### create fdb entries, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            for i in range(0,16):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_10_create_fdb_entries_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        status of each fdb entry can be seen in log of saiserver
        SAI Bug 112496
        '''
        sys_logging("### -----func_10_create_fdb_entries_fn_0----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_DENY]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        bulk_attr_list = []
        attr_list = []
        for i in range(0,16):
            bulk_attr_list.append([])
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])
            bulk_attr_list[i] = sai_thrift_attribute_list_t(attr_list=attr_list[i])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            status = self.client.sai_thrift_create_fdb_entries(fdb_entry_list, bulk_attr_list, mode_list[0])
            sys_logging("### create fdb entries, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

            for i in range(0,6):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

            for i in range(6,15):
                assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_10_create_fdb_entries_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        status of each fdb entry can be seen in log of saiserver
        SAI Bug 112496
        '''
        sys_logging("### -----func_10_create_fdb_entries_fn_1----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_DENY]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        bulk_attr_list = []
        attr_list = []
        for i in range(0,16):
            bulk_attr_list.append([])
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])
            bulk_attr_list[i] = sai_thrift_attribute_list_t(attr_list=attr_list[i])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            status = self.client.sai_thrift_create_fdb_entries(fdb_entry_list, bulk_attr_list, mode_list[1])
            sys_logging("### create fdb entries, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

            for i in range(0,6):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

            for i in range(6,8):
                assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))

            for i in range(8,15):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_11_remove_fdb_entries_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112496
        '''
        sys_logging("### -----func_11_remove_fdb_entries_fn----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        attr_list = []
        for i in range(0,16):
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            for i in range(0,16):
                mac = mac_list[i//4]
                vlan_id = vlan_id_list[i%4]
                type = type_list[(i%16)//8]
                action = action_list[(i%8)//2]
                bport = bport_list[i%2]
                status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac, bport, action, type)
                sys_logging("### create fdb entry, status = 0x%x ###" %status)

            for i in range(0,16):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

            status = self.client.sai_thrift_remove_fdb_entries(fdb_entry_list, mode_list[1])
            sys_logging("### remove fdb entries, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_11_remove_fdb_entries_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        status of each fdb entry can be seen in log of saiserver
        '''
        sys_logging("### -----func_11_remove_fdb_entries_fn_0----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_DENY]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        attr_list = []
        for i in range(0,16):
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            for i in range(0,16):
                mac = mac_list[i//4]
                vlan_id = vlan_id_list[i%4]
                type = type_list[(i%16)//8]
                action = action_list[(i%8)//2]
                bport = bport_list[i%2]
                status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac, bport, action, type)
                sys_logging("### create fdb entry, status = 0x%x ###" %status)

            for i in range(0,6):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

            for i in range(6,8):
                assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))

            for i in range(8,15):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

            status = self.client.sai_thrift_remove_fdb_entries(fdb_entry_list, mode_list[0])
            sys_logging("### remove fdb entries, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

            for i in range(0,8):
                assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))

            for i in range(8,15):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_11_remove_fdb_entries_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        status of each fdb entry can be seen in log of saiserver
        SAI Bug 112496
        '''
        sys_logging("### -----func_11_remove_fdb_entries_fn_1----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_DENY]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        attr_list = []
        for i in range(0,16):
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            for i in range(0,16):
                mac = mac_list[i//4]
                vlan_id = vlan_id_list[i%4]
                type = type_list[(i%16)//8]
                action = action_list[(i%8)//2]
                bport = bport_list[i%2]
                status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac, bport, action, type)
                sys_logging("### create fdb entry, status = 0x%x ###" %status)

            for i in range(0,6):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

            for i in range(6,8):
                assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))

            for i in range(8,15):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

            status = self.client.sai_thrift_remove_fdb_entries(fdb_entry_list, mode_list[1])
            sys_logging("### remove fdb entries, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

            for i in range(0,16):
                assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_12_set_fdb_entries_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112496
        '''
        sys_logging("### -----func_12_set_fdb_entries_attribute_fn----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        attr_list = []
        for i in range(0,16):
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            for i in range(0,16):
                mac = mac_list[i//4]
                vlan_id = vlan_id_list[i%4]
                type = type_list[(i%16)//8]
                action = action_list[(i%8)//2]
                bport = bport_list[i%2]
                status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac, bport, action, type)
                sys_logging("### create fdb entry, status = 0x%x ###" %status)

            for i in range(0,16):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

            set_attr_list = []
            for i in range(0,16):
                set_attr_list.append(attr_list3[(i+1)%2])
            status = self.client.sai_thrift_set_fdb_entries_attribute(fdb_entry_list, set_attr_list, mode_list[1])
            sys_logging("### set fdb entries attribute, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            for i in range(0,16):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                bport = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4], bport=True)
                assert(bport_list[(i+1)%2] == bport)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_12_set_fdb_entries_attribute_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        status of each fdb entry can be seen in log of saiserver
        SAI Bug 112496
        '''
        sys_logging("### -----func_12_set_fdb_entries_attribute_fn_0----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        attr_list = []
        for i in range(0,16):
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            for i in range(0,16):
                mac = mac_list[i//4]
                vlan_id = vlan_id_list[i%4]
                type = type_list[(i%16)//8]
                action = action_list[(i%8)//2]
                bport = bport_list[i%2]
                status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac, bport, action, type)
                sys_logging("### create fdb entry, status = 0x%x ###" %status)

            for i in range(0,16):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

            set_attr_list = []
            for i in range(0,16):
                set_attr_list.append(attr_list3[(i+1)%2])
            for i in range(6,8):
                set_attr_list[i] = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID,
                                                          value=sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID))
            status = self.client.sai_thrift_set_fdb_entries_attribute(fdb_entry_list, set_attr_list, mode_list[0])
            sys_logging("### set fdb entries attribute, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

            for i in range(0,6):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                bport = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4], bport=True)
                assert(bport_list[(i+1)%2] == bport)

            for i in range(6,16):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                bport = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4], bport=True)
                assert(bport_list[(i)%2] == bport)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_12_set_fdb_entries_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        status of each fdb entry can be seen in log of saiserver
        SAI Bug 112496
        '''
        sys_logging("### -----func_12_set_fdb_entries_attribute_fn_1----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        attr_list = []
        for i in range(0,16):
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            for i in range(0,16):
                mac = mac_list[i//4]
                vlan_id = vlan_id_list[i%4]
                type = type_list[(i%16)//8]
                action = action_list[(i%8)//2]
                bport = bport_list[i%2]
                status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac, bport, action, type)
                sys_logging("### create fdb entry, status = 0x%x ###" %status)

            for i in range(0,16):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(attr_list[i][0].value.s32 == return_list[0])
                assert(attr_list[i][1].value.s32 == return_list[1])
                assert(attr_list[i][2].value.oid == return_list[2])

            set_attr_list = []
            for i in range(0,16):
                set_attr_list.append(attr_list3[(i+1)%2])
            for i in range(6,8):
                set_attr_list[i] = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID,
                                                          value=sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID))
            status = self.client.sai_thrift_set_fdb_entries_attribute(fdb_entry_list, set_attr_list, mode_list[1])
            sys_logging("### set fdb entries attribute, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

            for i in range(0,6):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                bport = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4], bport=True)
                assert(bport_list[(i+1)%2] == bport)

            for i in range(6,8):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                bport = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4], bport=True)
                assert(bport_list[(i)%2] == bport)

            for i in range(8,16):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                bport = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4], bport=True)
                assert(bport_list[(i+1)%2] == bport)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_13_get_fdb_entries_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112496
        '''
        sys_logging("### -----func_13_set_fdb_entries_attribute_fn----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        attr_list = []
        for i in range(0,16):
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            for i in range(0,16):
                mac = mac_list[i//4]
                vlan_id = vlan_id_list[i%4]
                type = type_list[(i%16)//8]
                action = action_list[(i%8)//2]
                bport = bport_list[i%2]
                status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac, bport, action, type)
                sys_logging("### create fdb entry, status = 0x%x ###" %status)

            for i in range(0,16):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(type_list[(i%16)//8] == return_list[0])
                assert(action_list[(i%8)//2] == return_list[1])
                assert(bport_list[i%2] == return_list[2])

            bulk_attr_list = self.client.sai_thrift_get_fdb_entries_attribute(fdb_entry_list, mode_list[1])
            for i in range(0,16):
                sys_logging("### get fdb entries attribute, status of No.%d = 0x%x ###" %(i,bulk_attr_list[i].status))
                assert(SAI_STATUS_SUCCESS == bulk_attr_list[i].status)
                assert(type_list[(i%16)//8] == bulk_attr_list[i].attr_list[0].value.s32)
                assert(action_list[(i%8)//2] == bulk_attr_list[i].attr_list[1].value.s32)
                assert(bport_list[i%2] == bulk_attr_list[i].attr_list[2].value.oid)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_13_get_fdb_entries_attribute_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112496
        '''
        sys_logging("### -----func_13_set_fdb_entries_attribute_fn_0----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        attr_list = []
        for i in range(0,16):
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            for i in range(0,6):
                mac = mac_list[i//4]
                vlan_id = vlan_id_list[i%4]
                type = type_list[(i%16)//8]
                action = action_list[(i%8)//2]
                bport = bport_list[i%2]
                status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac, bport, action, type)
                sys_logging("### create fdb entry, status = 0x%x ###" %status)

            for i in range(8,16):
                mac = mac_list[i//4]
                vlan_id = vlan_id_list[i%4]
                type = type_list[(i%16)//8]
                action = action_list[(i%8)//2]
                bport = bport_list[i%2]
                status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac, bport, action, type)
                sys_logging("### create fdb entry, status = 0x%x ###" %status)

            for i in range(0,6):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(type_list[(i%16)//8] == return_list[0])
                assert(action_list[(i%8)//2] == return_list[1])
                assert(bport_list[i%2] == return_list[2])

            for i in range(6,8):
                assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))

            for i in range(8,16):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(type_list[(i%16)//8] == return_list[0])
                assert(action_list[(i%8)//2] == return_list[1])
                assert(bport_list[i%2] == return_list[2])

            bulk_attr_list = self.client.sai_thrift_get_fdb_entries_attribute(fdb_entry_list, mode_list[0])
            for i in range(0,6):
                sys_logging("### get fdb entries attribute, status of No.%d = 0x%x ###" %(i,bulk_attr_list[i].status))
                assert(SAI_STATUS_SUCCESS == bulk_attr_list[i].status)
                assert(type_list[(i%16)//8] == bulk_attr_list[i].attr_list[0].value.s32)
                assert(action_list[(i%8)//2] == bulk_attr_list[i].attr_list[1].value.s32)
                assert(bport_list[i%2] == bulk_attr_list[i].attr_list[2].value.oid)
            for i in range(6,16):
                sys_logging("### get fdb entries attribute, status of No.%d = 0x%x ###" %(i,bulk_attr_list[i].status))
                assert(SAI_STATUS_SUCCESS != bulk_attr_list[i].status)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class func_13_get_fdb_entries_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112496
        '''
        sys_logging("### -----func_13_set_fdb_entries_attribute_fn_1----- ###")
        switch_init(self.client)

        mac_list = ['00.11.11.11.11.11','00.22.22.22.22.22',
                    '00.33.33.33.33.33','00.44.44.44.44.44']
        vlan_id_list =[]
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 100))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 200))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 300))
        vlan_id_list.append(sai_thrift_create_vlan(self.client, 400))
        fdb_entry_list = []
        for mac in mac_list:
            for vlan_id in vlan_id_list:
                fdb_entry_list.append(sai_thrift_fdb_entry_t(mac_address=mac, bv_id=vlan_id))

        type_list = [SAI_FDB_ENTRY_TYPE_DYNAMIC, SAI_FDB_ENTRY_TYPE_STATIC]
        attr_list1 = []
        for type in type_list:
            attr_value = sai_thrift_attribute_value_t(s32=type)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_TYPE, value=attr_value)
            attr_list1.append(attr)

        #packet action of dynamic fdb entry cannot be drop
        action_list = [SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT,
                       SAI_PACKET_ACTION_TRANSIT, SAI_PACKET_ACTION_TRANSIT]
        attr_list2 = []
        for action in action_list:
            attr_value = sai_thrift_attribute_value_t(s32=action)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            attr_list2.append(attr)

        port1 = port_list[0]
        port2 = port_list[1]
        bport_list = []
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port1))
        bport_list.append(sai_thrift_get_bridge_port_by_port(self.client, port2))
        attr_list3 = []
        for bport in bport_list:
            attr_value = sai_thrift_attribute_value_t(oid=bport)
            attr = sai_thrift_attribute_t(id=SAI_FDB_ENTRY_ATTR_BRIDGE_PORT_ID, value=attr_value)
            attr_list3.append(attr)

        attr_list = []
        for i in range(0,16):
            attr_list.append([])
            attr_list[i].append(attr_list1[(i%16)//8])
            attr_list[i].append(attr_list2[(i%8)//2])
            attr_list[i].append(attr_list3[i%2])

        mode_list = [SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR]
        warmboot(self.client)

        try:
            for mac in mac_list:
                for vlan_id in vlan_id_list:
                    assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac))

            for i in range(0,6):
                mac = mac_list[i//4]
                vlan_id = vlan_id_list[i%4]
                type = type_list[(i%16)//8]
                action = action_list[(i%8)//2]
                bport = bport_list[i%2]
                status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac, bport, action, type)
                sys_logging("### create fdb entry, status = 0x%x ###" %status)

            for i in range(8,16):
                mac = mac_list[i//4]
                vlan_id = vlan_id_list[i%4]
                type = type_list[(i%16)//8]
                action = action_list[(i%8)//2]
                bport = bport_list[i%2]
                status = sai_thrift_create_fdb_bport(self.client, vlan_id, mac, bport, action, type)
                sys_logging("### create fdb entry, status = 0x%x ###" %status)

            for i in range(0,6):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(type_list[(i%16)//8] == return_list[0])
                assert(action_list[(i%8)//2] == return_list[1])
                assert(bport_list[i%2] == return_list[2])

            for i in range(6,8):
                assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))

            for i in range(8,16):
                assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id_list[i%4], mac_list[i//4]))
                return_list = _get_fdb_attr(self.client, vlan_id_list[i%4], mac_list[i//4],
                                            type=True, action=True, bport=True)
                assert(type_list[(i%16)//8] == return_list[0])
                assert(action_list[(i%8)//2] == return_list[1])
                assert(bport_list[i%2] == return_list[2])

            bulk_attr_list = self.client.sai_thrift_get_fdb_entries_attribute(fdb_entry_list, mode_list[1])
            for i in range(0,6):
                sys_logging("### get fdb entries attribute, status of No.%d = 0x%x ###" %(i,bulk_attr_list[i].status))
                assert(SAI_STATUS_SUCCESS == bulk_attr_list[i].status)
                assert(type_list[(i%16)//8] == bulk_attr_list[i].attr_list[0].value.s32)
                assert(action_list[(i%8)//2] == bulk_attr_list[i].attr_list[1].value.s32)
                assert(bport_list[i%2] == bulk_attr_list[i].attr_list[2].value.oid)
            for i in range(6,8):
                sys_logging("### get fdb entries attribute, status of No.%d = 0x%x ###" %(i,bulk_attr_list[i].status))
                assert(SAI_STATUS_SUCCESS != bulk_attr_list[i].status)
            for i in range(8,16):
                sys_logging("### get fdb entries attribute, status of No.%d = 0x%x ###" %(i,bulk_attr_list[i].status))
                assert(SAI_STATUS_SUCCESS == bulk_attr_list[i].status)
                assert(type_list[(i%16)//8] == bulk_attr_list[i].attr_list[0].value.s32)
                assert(action_list[(i%8)//2] == bulk_attr_list[i].attr_list[1].value.s32)
                assert(bport_list[i%2] == bulk_attr_list[i].attr_list[2].value.oid)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            for vlan_id in vlan_id_list:
                self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class scenario_01_fdb_learning_and_aging(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_01_fdb_learning_and_aging----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)
        bport3 = sai_thrift_get_bridge_port_by_port(self.client, port3)

        vlan1 = 100
        vlan_id = sai_thrift_create_vlan(self.client, vlan1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan2 = 200
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan2)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan2)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan2)

        attr_value = sai_thrift_attribute_value_t(u16=vlan1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac1, eth_src=mac2,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst=mac1, eth_src=mac2,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        warmboot(self.client)

        try:
            aging_time = 10
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_AGING_TIME,
                                          value=sai_thrift_attribute_value_t(u32=aging_time))
            self.client.sai_thrift_set_switch_attribute(attr)

            switch_attr_list = self.client.sai_thrift_get_switch_attribute([SAI_SWITCH_ATTR_FDB_AGING_TIME])
            for attribute in switch_attr_list.attr_list:
                if attribute.id == SAI_SWITCH_ATTR_FDB_AGING_TIME:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_AGING_TIME = %d ###" %attribute.value.u32)
                    assert(aging_time == attribute.value.u32)

            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(
                                         self.client, vlan_id, mac1, bport1, type=SAI_FDB_ENTRY_TYPE_DYNAMIC))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac1))
            assert([SAI_FDB_ENTRY_TYPE_DYNAMIC, bport1] == _get_fdb_attr(self.client, vlan_id, mac1,
                                                                         type=True, bport=True))

            time.sleep(aging_time)
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(pkt1, [1,2])

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac1))
            assert([SAI_FDB_ENTRY_TYPE_DYNAMIC, bport1] == _get_fdb_attr(self.client, vlan_id, mac1,
                                                                         type=True, bport=True))

            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packet(pkt2, 0)
            self.ctc_verify_no_packet(pkt2, 2)

            time.sleep(aging_time)
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac1))

            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packets(pkt2, [0,2])

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(
                                         self.client, bridge_id, mac1, sub_port1, type=SAI_FDB_ENTRY_TYPE_DYNAMIC))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert([SAI_FDB_ENTRY_TYPE_DYNAMIC, sub_port1] == _get_fdb_attr(self.client, bridge_id, mac1,
                                                                            type=True, bport=True))

            time.sleep(aging_time)
            self.ctc_send_packet(0, pkt3)
            self.ctc_verify_packets(pkt3, [1,2])

            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert([SAI_FDB_ENTRY_TYPE_DYNAMIC, sub_port1] == _get_fdb_attr(self.client, bridge_id, mac1,
                                                                            type=True, bport=True))

            self.ctc_send_packet(1, pkt4)
            self.ctc_verify_packet(pkt4, 0)
            self.ctc_verify_no_packet(pkt4, 2)

            time.sleep(aging_time)
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))

            self.ctc_send_packet(1, pkt4)
            self.ctc_verify_packets(pkt4, [0,2])

        finally:
            attr_value = sai_thrift_attribute_value_t(u32=300)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_AGING_TIME, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_id)


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


@group('L2')
class scenario_04_fdb_station_move(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_04_fdb_station_move----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)
        bport3 = sai_thrift_get_bridge_port_by_port(self.client, port3)

        vlan1 = 100
        vlan_id = sai_thrift_create_vlan(self.client, vlan1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan2 = 200
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan2)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan2)

        v4_enabled = 1
        v6_enabled = 1
        rmac = '00:11:22:33:44:55'
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                     port1, 0, v4_enabled, v6_enabled, rmac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN,
                                                     0, vlan_id, v4_enabled, v6_enabled, rmac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                     0, 0, v4_enabled, v6_enabled, rmac, 0, bridge_id)
        rif_port = sai_thrift_create_bridge_rif_port(self.client, bridge_id, rif_id3)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        #default SAI_NEIGHBOR_ENTRY_ATTR_NO_HOST_ROUTE=false, host route will be created
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, mac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_addr2, mac3)

        pkt1 = simple_tcp_packet(eth_dst=rmac, eth_src=mac1,
                                 ip_dst='10.10.10.1', ip_src='192.168.0.1',
                                 ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac2, eth_src=rmac,
                                 ip_dst='10.10.10.1', ip_src='192.168.0.1',
                                 ip_id=101, ip_ttl=63)
        pkt3 = simple_tcp_packet(eth_dst=rmac, eth_src=mac1,
                                 ip_dst='10.10.10.2', ip_src='192.168.0.1',
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_id=102, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst=mac3, eth_src=rmac,
                                 ip_dst='10.10.10.2', ip_src='192.168.0.1',
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_id=102, ip_ttl=63)

        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            self.ctc_send_packet( 0, pkt1)
            self.ctc_verify_no_packet(pkt2, 1)

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb(self.client, vlan_id, mac2, port2))
            assert(bport2 == _get_fdb_attr(self.client, vlan_id, mac2, bport=True))

            self.ctc_send_packet( 0, pkt1)
            self.ctc_verify_packet(pkt2, 1)

            #here uses port_id, but no exception was returned
            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, vlan_id, mac2, bport=port3))
            assert(bport3 == _get_fdb_attr(self.client, vlan_id, mac2, bport=True))

            self.ctc_send_packet( 0, pkt1)
            self.ctc_verify_packet(pkt2, 2)

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            self.ctc_send_packet( 0, pkt3)
            self.ctc_verify_no_packet(pkt4, 1)

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac3, sub_port1))
            assert(sub_port1 == _get_fdb_attr(self.client, bridge_id, mac3, bport=True))

            self.ctc_send_packet( 0, pkt3)
            self.ctc_verify_packet(pkt4, 1)

            assert(SAI_STATUS_SUCCESS == _set_fdb_attr(self.client, bridge_id, mac3, bport=sub_port2))
            assert(sub_port2 == _get_fdb_attr(self.client, bridge_id, mac3, bport=True))

            self.ctc_send_packet( 0, pkt3)
            self.ctc_verify_packet(pkt4, 2)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, mac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_addr2, mac3)
            self.client.sai_thrift_remove_bridge_port(rif_port)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class scenario_05_fdb_entry_cover(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_05_fdb_entry_cover----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)
        bport3 = sai_thrift_get_bridge_port_by_port(self.client, port3)

        vlan1 = 100
        vlan_id = sai_thrift_create_vlan(self.client, vlan1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan2 = 200
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan2)
        sub_port2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan2)
        sub_port3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan2)

        attr_value = sai_thrift_attribute_value_t(u16=vlan1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac1, eth_src=mac2,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst=mac1, eth_src=mac2,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        warmboot(self.client)

        try:
            aging_time = 10
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_AGING_TIME,
                                          value=sai_thrift_attribute_value_t(u32=aging_time))
            self.client.sai_thrift_set_switch_attribute(attr)

            switch_attr_list = self.client.sai_thrift_get_switch_attribute([SAI_SWITCH_ATTR_FDB_AGING_TIME])
            for attribute in switch_attr_list.attr_list:
                if attribute.id == SAI_SWITCH_ATTR_FDB_AGING_TIME:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_AGING_TIME = %d ###" %attribute.value.u32)
                    assert(aging_time == attribute.value.u32)

            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packets(pkt1, [1,2])

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac1))
            assert(SAI_FDB_ENTRY_TYPE_DYNAMIC == _get_fdb_attr(self.client, vlan_id, mac1, type=True))

            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packet(pkt2, 0)
            self.ctc_verify_no_packet(pkt2, 2)

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, vlan_id, mac1,
                                                                     bport1, type=SAI_FDB_ENTRY_TYPE_STATIC))
            assert(SAI_FDB_ENTRY_TYPE_STATIC == _get_fdb_attr(self.client, vlan_id, mac1, type=True))

            time.sleep(aging_time)
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_id, mac1))

            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packet(pkt2, 0)
            self.ctc_verify_no_packet(pkt2, 2)

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            self.ctc_send_packet(0, pkt3)
            self.ctc_verify_packets(pkt3, [1,2])

            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_FDB_ENTRY_TYPE_DYNAMIC == _get_fdb_attr(self.client, bridge_id, mac1, type=True))

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac1,
                                                                     sub_port1, type=SAI_FDB_ENTRY_TYPE_STATIC))
            assert(SAI_FDB_ENTRY_TYPE_STATIC == _get_fdb_attr(self.client, bridge_id, mac1, type=True))

            time.sleep(aging_time)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))

            self.ctc_send_packet(1, pkt4)
            self.ctc_verify_packet(pkt4, 0)
            self.ctc_verify_no_packet(pkt4, 2)

        finally:
            attr_value = sai_thrift_attribute_value_t(u32=300)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_AGING_TIME, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_bridge_port(sub_port1)
            self.client.sai_thrift_remove_bridge_port(sub_port2)
            self.client.sai_thrift_remove_bridge_port(sub_port3)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class scenario_08_L2FlushStatic(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112629
        '''
        sys_logging("### -----scenario_08_L2FlushStatic----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        vlan = 10
        vlan_id = sai_thrift_create_vlan(self.client, vlan)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        pkt = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                ip_dst='10.0.0.1', ip_id=107, ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                    ip_dst='10.0.0.1', ip_id=107, ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac1, eth_src=mac2,
                                 ip_dst='10.0.0.1', ip_id=107, ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac1, eth_src=mac2,
                                     ip_dst='10.0.0.1', ip_id=107, ip_ttl=64)

        warmboot(self.client)

        try:
            sai_thrift_create_fdb(self.client, vlan_id, mac2, port2)

            self.ctc_send_packet(0, pkt)
            self.ctc_verify_packets(exp_pkt, [1])

            fdb_entry_type = SAI_FDB_FLUSH_ENTRY_TYPE_STATIC
            sai_thrift_flush_fdb(self.client, SAI_NULL_OBJECT_ID, SAI_NULL_OBJECT_ID, fdb_entry_type)

            self.ctc_send_packet(0, pkt)
            self.ctc_verify_packets(exp_pkt, [1, 2])

            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_packet(exp_pkt1, 0)
            self.ctc_verify_no_packet(exp_pkt1, 2)

        finally:
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
            self.client.sai_thrift_remove_vlan(vlan_id)


@group('L2')
class scenario_09_L2FlushDynamic(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112629
        '''
        sys_logging("### -----scenario_09_L2FlushDynamic----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        vlan = 10
        vlan_id = sai_thrift_create_vlan(self.client, vlan)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_id, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_id, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_id, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        pkt = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                ip_dst='10.0.0.1', ip_id=107, ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                    ip_dst='10.0.0.1', ip_id=107, ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac1, eth_src=mac2,
                                 ip_dst='10.0.0.2', ip_id=107, ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac1, eth_src=mac2,
                                     ip_dst='10.0.0.2', ip_id=107, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(exp_pkt, [1,2])
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(exp_pkt1, [0])

            fdb_entry_type = SAI_FDB_FLUSH_ENTRY_TYPE_DYNAMIC
            sai_thrift_flush_fdb(self.client, SAI_NULL_OBJECT_ID, SAI_NULL_OBJECT_ID, fdb_entry_type)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(exp_pkt1, [0,2])

        finally:
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
            self.client.sai_thrift_remove_vlan(vlan_id)


class scenario_10_L2FdbGetSetEntryTypeDynamicToStatic(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan_id = 10
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac2, bport2, packet_action, SAI_FDB_ENTRY_TYPE_DYNAMIC)

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
            assert(SAI_FDB_ENTRY_TYPE_DYNAMIC == _get_fdb_attr(self.client, vlan_oid, mac2, type=True))

            _set_fdb_attr(self.client, vlan_oid, mac2, type=SAI_FDB_ENTRY_TYPE_STATIC)
            assert(SAI_FDB_ENTRY_TYPE_STATIC == _get_fdb_attr(self.client, vlan_oid, mac2, type=True))

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(exp_pkt, [1])

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_11_L2FdbGetSetEntryActionTransitToTrap(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan_id = 10
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        packet_action = SAI_PACKET_ACTION_TRANSIT
        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac2, bport2, packet_action, SAI_FDB_ENTRY_TYPE_STATIC)

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
            assert(packet_action == _get_fdb_attr(self.client, vlan_oid, mac2, action=True))
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(exp_pkt, [1])

        finally:
            sys_logging ("modify action from transit to trap")

        _set_fdb_attr(self.client, vlan_oid, mac2, action=SAI_PACKET_ACTION_TRAP)
        assert(SAI_PACKET_ACTION_TRAP == _get_fdb_attr(self.client, vlan_oid, mac2, action=True))

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
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_12_L2FdbGetSetEntryActionTransitToLog(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan_id = 10
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        packet_action = SAI_PACKET_ACTION_TRANSIT
        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac2, bport2, packet_action, SAI_FDB_ENTRY_TYPE_STATIC)

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
            assert(packet_action == _get_fdb_attr(self.client, vlan_oid, mac2, action=True))
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(exp_pkt, [1])

        finally:
            sys_logging ("modify action from transit to log")

        _set_fdb_attr(self.client, vlan_oid, mac2, action=SAI_PACKET_ACTION_LOG)
        assert(SAI_PACKET_ACTION_LOG == _get_fdb_attr(self.client, vlan_oid, mac2, action=True))

        warmboot(self.client)
        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(exp_pkt, [1])
            """
            TODO:check packet passed to cpu
            """

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_13_L2FdbGetSetEntryActionTransitToDeny(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan_id = 10
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        packet_action = SAI_PACKET_ACTION_TRANSIT
        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac2, bport2, packet_action, SAI_FDB_ENTRY_TYPE_STATIC)

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
            assert(packet_action == _get_fdb_attr(self.client, vlan_oid, mac2, action=True))
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(exp_pkt, [1])

        finally:
            sys_logging ("modify action from transit to deny")

        _set_fdb_attr(self.client, vlan_oid, mac2, action=SAI_PACKET_ACTION_DENY)
        assert(SAI_PACKET_ACTION_DENY == _get_fdb_attr(self.client, vlan_oid, mac2, action=True))

        warmboot(self.client)
        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(exp_pkt, 1, default_time_out)
            """
            TODO:check packet not passed to cpu
            """

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_14_L2FdbGetSetEntryActionLogToDeny(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan_id = 10
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        packet_action = SAI_PACKET_ACTION_LOG
        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac2, bport2, packet_action, SAI_FDB_ENTRY_TYPE_STATIC)

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
            assert(packet_action == _get_fdb_attr(self.client, vlan_oid, mac2, action=True))
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            """
            TODO:check packet passed to cpu
            """

        finally:
            sys_logging ("modify action from log to deny")

        _set_fdb_attr(self.client, vlan_oid, mac2, action=SAI_PACKET_ACTION_DENY)
        assert(SAI_PACKET_ACTION_DENY == _get_fdb_attr(self.client, vlan_oid, mac2, action=True))

        warmboot(self.client)
        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(exp_pkt, 1, default_time_out)
            """
            TODO:check packet not passed to cpu
            """

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_15_L2FdbGetSetEntryPort(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)
        bport3 = sai_thrift_get_bridge_port_by_port(self.client, port3)

        vlan_id = 10
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        packet_action = SAI_PACKET_ACTION_TRANSIT
        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac2, bport2, packet_action, SAI_FDB_ENTRY_TYPE_STATIC)

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
            assert(bport2 == _get_fdb_attr(self.client, vlan_oid, mac2, bport=True))
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(exp_pkt, [1])

        finally:
            sys_logging ("modify port from port2 to port3")

        _set_fdb_attr(self.client, vlan_oid, mac2, bport=bport3)
        assert(bport3 == _get_fdb_attr(self.client, vlan_oid, mac2, bport=True))

        warmboot(self.client)
        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(exp_pkt, [2])

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
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

        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port3)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac4, port3)

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
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac4)
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

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port1)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac3, port3)

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
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac3)
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

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port1)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac3, port3)

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
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac3)
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

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port1)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac3, port3)

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
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac3)
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

        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_bridge_oid, mac_action)

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


