# Copyright 2013-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Thrift SAI interface ACL tests
"""

from switch import *
import sai_base_test

@group('acl')
class IPAclTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_mask1 = '255.255.255.255'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

        # send the test packet(s)
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
        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( exp_pkt, [0])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = None
        mac_dst = None
        mac_src_mask = None
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        is_ipv6 = False
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        ip_proto = None
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None

        acl_table_id = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            ip_proto,
            in_ports,
            out_ports,
            in_port,
            out_port,
            src_l4_port,
            dst_l4_port)
        acl_entry_id = sai_thrift_create_acl_entry(self.client,
            acl_table_id,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_src, ip_src_mask,
            ip_dst, ip_dst_mask,
            is_ipv6,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            ip_proto,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        warmboot(self.client)
        
        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 1, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( exp_pkt, 0, default_time_out)
        finally:
            # unbind this ACL table from port2s object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

@group('acl')
class MACSrcAclTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_mask1 = '255.255.255.255'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

        # send the test packet(s)
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
        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( exp_pkt, [0])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source MAC
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = 1
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = '00:22:22:22:22:22'
        mac_dst = None
        mac_src_mask = 'ff:ff:ff:ff:ff:ff'
        mac_dst_mask = None
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
        ip_src = None
        ip_src_mask = None
        ip_dst = None
        ip_dst_mask = None
        is_ipv6 = False
        #ip qos info
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        ip_proto = None
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None

        acl_table_id = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            ip_proto,
            in_ports,
            out_ports,
            in_port,
            out_port,
            src_l4_port,
            dst_l4_port)
        acl_entry_id = sai_thrift_create_acl_entry(self.client,
            acl_table_id,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_src, ip_src_mask,
            ip_dst, ip_dst_mask,
            is_ipv6,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            ip_proto,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        warmboot(self.client)

        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src mac 00:22:22:22:22:22, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 1, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( exp_pkt, 0, default_time_out)
        finally:
            # unbind this ACL table from port2s object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

@group('acl')
class L3AclTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.100.100 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        L4_SRC_PORT = 1000
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_mask1 = '255.255.255.255'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
            eth_src='00:22:22:22:22:22',
            ip_dst='10.10.10.1',
            ip_src='192.168.100.100',
            tcp_sport = L4_SRC_PORT,
            ip_id=105,
            ip_ttl=64)
        exp_pkt = simple_tcp_packet(
            eth_dst='00:11:22:33:44:55',
            eth_src=router_mac,
            ip_dst='10.10.10.1',
            ip_src='192.168.100.100',
            tcp_sport = L4_SRC_PORT,
            ip_id=105,
            ip_ttl=63)
        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.100.100 | SPORT 1000 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.100.100 | SPORT 1000 | @ ptf_intf 1'
            self.ctc_verify_packets( exp_pkt, [0])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP and SPORT
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_ROUTER_INTF]
        entry_priority = 1
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = None
        mac_dst = None
        mac_src_mask = None
        mac_dst_mask = None
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
        ip_src = "192.168.100.1"
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        is_ipv6 = False
        #ip qos info
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        ip_proto = None
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = L4_SRC_PORT
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None

        acl_table_id = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            ip_proto,
            in_ports,
            out_ports,
            in_port,
            out_port,
            src_l4_port,
            dst_l4_port)
        acl_entry_id = sai_thrift_create_acl_entry(self.client,
            acl_table_id,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_src, ip_src_mask,
            ip_dst, ip_dst_mask,
            is_ipv6,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            ip_proto,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn)

        # bind this ACL table to rif_id2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        
        warmboot(self.client)

        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src ip 192.168.100.1/255.255.255.0, SPORT 1000, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.100.100 | SPORT 1000 | @ ptf_intf 1'
            # send the same packet
            self.ctc_send_packet( 1, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.100.100 | SPORT 1000 | @ ptf_intf 0'
            self.ctc_verify_no_packet( exp_pkt, 0, default_time_out)
        finally:
            # unbind this ACL table from rif_id2s object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

@group('acl')
class SeqAclTableGroupTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_mask1 = '255.255.255.255'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

        # send the test packet(s)
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
        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( exp_pkt, [0])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
            group_stage,
            group_bind_point_list,
            group_type)

        # setup ACL tables to block based on Source MAC
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = 1
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = '00:22:22:22:22:22'
        mac_dst = None
        mac_src_mask = 'ff:ff:ff:ff:ff:ff'
        mac_dst_mask = None
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
        ip_src = None
        ip_src_mask = None
        ip_src1 = "192.168.0.1"
        ip_src1_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        is_ipv6 = False
        #ip qos info
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        ip_proto = None
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None

        # create ACL table #1
        acl_table_id1 = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            ip_proto,
            in_ports,
            out_ports,
            in_port,
            out_port,
            src_l4_port,
            dst_l4_port)
        acl_entry_id1 = sai_thrift_create_acl_entry(self.client,
            acl_table_id1,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_src, ip_src_mask,
            ip_dst, ip_dst_mask,
            is_ipv6,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            ip_proto,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn)

        # create ACL table #2
        acl_table_id2 = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            ip_proto,
            in_ports,
            out_ports,
            in_port,
            out_port,
            src_l4_port,
            dst_l4_port)
        acl_entry_id2 = sai_thrift_create_acl_entry(self.client,
            acl_table_id2,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_src1, ip_src1_mask,
            ip_dst, ip_dst_mask,
            is_ipv6,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            ip_proto,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn)

        # setup ACL table group members
        group_member_priority1 = 1
        group_member_priority2 = 100

        # create ACL table group members
        acl_table_group_member_id1 = sai_thrift_create_acl_table_group_member(self.client,
            acl_table_group_id,
            acl_table_id1,
            group_member_priority1)
        acl_table_group_member_id2 = sai_thrift_create_acl_table_group_member(self.client,
            acl_table_group_id,
            acl_table_id2,
            group_member_priority2)

        # bind this ACL table group to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_group_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        warmboot(self.client)
        
        try:
            assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'
            assert acl_table_id1 > 0, 'acl_entry_id1 is <= 0'
            assert acl_entry_id1 > 0, 'acl_entry_id1 is <= 0'
            assert acl_table_id2 > 0, 'acl_entry_id2 is <= 0'
            assert acl_entry_id2 > 0, 'acl_entry_id2 is <= 0'
            assert acl_table_group_member_id1 > 0, 'acl_table_group_member_id1 is <= 0'
            assert acl_table_group_member_id2 > 0, 'acl_table_group_member_id2 is <= 0'

            print '#### ACL \'DROP, src mac 00:22:22:22:22:22, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 1, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( exp_pkt, 0, default_time_out)
        finally:
            # unbind this ACL table from port2s object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            # cleanup ACL
            self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id1)
            self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id2)
            self.client.sai_thrift_remove_acl_entry(acl_entry_id1)
            self.client.sai_thrift_remove_acl_table(acl_table_id1)
            self.client.sai_thrift_remove_acl_entry(acl_entry_id2)
            self.client.sai_thrift_remove_acl_table(acl_table_id2)
            self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

@group('acl')
class MultBindAclTableGroupTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 4 -> [ptf_intf 1, ptf_intf 2, ptf_intf 3] (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_mask1 = '255.255.255.255'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id4)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

        # send the test packet(s)
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
        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_send_packet( 0, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 4'
            self.ctc_verify_packet( exp_pkt, 3)
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 4'
            self.ctc_verify_packet( exp_pkt, 3)
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 3'
            self.ctc_send_packet( 2, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 4'
            self.ctc_verify_packet( exp_pkt, 3)
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet [ptf_intf 1, ptf_intf 2, ptf_intf 3] - [acl]-> ptf_intf 4 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
            group_stage,
            group_bind_point_list,
            group_type)

        # setup ACL tables to block based on Source MAC
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = 1
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = '00:22:22:22:22:22'
        mac_dst = None
        mac_src_mask = 'ff:ff:ff:ff:ff:ff'
        mac_dst_mask = None
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
        ip_src = None
        ip_src_mask = None
        ip_src1 = "192.168.0.1"
        ip_src1_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        is_ipv6 = False
        #ip qos info
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        ip_proto = None
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None

        # create ACL table #1
        acl_table_id1 = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            ip_proto,
            in_ports,
            out_ports,
            in_port,
            out_port,
            src_l4_port,
            dst_l4_port)
        acl_entry_id1 = sai_thrift_create_acl_entry(self.client,
            acl_table_id1,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_src, ip_src_mask,
            ip_dst, ip_dst_mask,
            is_ipv6,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            ip_proto,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn)

        # create ACL table #2
        acl_table_id2 = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            ip_proto,
            in_ports,
            out_ports,
            in_port,
            out_port,
            src_l4_port,
            dst_l4_port)
        acl_entry_id2 = sai_thrift_create_acl_entry(self.client,
            acl_table_id2,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_src1, ip_src1_mask,
            ip_dst, ip_dst_mask,
            is_ipv6,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            ip_proto,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn)

        # setup ACL table group members
        group_member_priority1 = 1
        group_member_priority2 = 100

        # create ACL table group members
        acl_table_group_member_id1 = sai_thrift_create_acl_table_group_member(self.client,
            acl_table_group_id,
            acl_table_id1,
            group_member_priority1)
        acl_table_group_member_id2 = sai_thrift_create_acl_table_group_member(self.client,
            acl_table_group_id,
            acl_table_id2,
            group_member_priority2)

        # bind this ACL table group to port1, port2, port3 object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_group_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        warmboot(self.client)
        
        try:
            assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'
            assert acl_table_id1 > 0, 'acl_entry_id1 is <= 0'
            assert acl_entry_id1 > 0, 'acl_entry_id1 is <= 0'
            assert acl_table_id2 > 0, 'acl_entry_id2 is <= 0'
            assert acl_entry_id2 > 0, 'acl_entry_id2 is <= 0'
            assert acl_table_group_member_id1 > 0, 'acl_table_group_member_id1 is <= 0'
            assert acl_table_group_member_id2 > 0, 'acl_table_group_member_id2 is <= 0'

            print '#### ACL \'DROP, src mac 00:22:22:22:22:22, in_ports[ptf_intf_1,2,3,4]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_send_packet( 0, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 4'
            self.ctc_verify_no_packet( exp_pkt, 3, default_time_out)
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 4'
            self.ctc_verify_no_packet( exp_pkt, 3, default_time_out)
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 3'
            self.ctc_send_packet( 2, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 4'
            self.ctc_verify_no_packet( exp_pkt, 3, default_time_out)
        finally:
            # unbind this ACL table from port1, port2, port3 object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            # cleanup ACL
            self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id1)
            self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id2)
            self.client.sai_thrift_remove_acl_entry(acl_entry_id1)
            self.client.sai_thrift_remove_acl_table(acl_table_id1)
            self.client.sai_thrift_remove_acl_entry(acl_entry_id2)
            self.client.sai_thrift_remove_acl_table(acl_table_id2)
            self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id4, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)

@group('acl')
class BindAclTableInGroupTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet [ptf_intf 1, ptf_intf 2, ptf_intf 3, ptf_intf 4] -> ptf_intf 5 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        port5 = port_list[5]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)


        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id5, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id4)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

        # send the test packet(s)
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
        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_send_packet( 1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 5'
            self.ctc_verify_packet( exp_pkt, 5)
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 2, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 5'
            self.ctc_verify_packet( exp_pkt, 5)
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 3'
            self.ctc_send_packet( 3, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 5'
            self.ctc_verify_packet( exp_pkt, 5)
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 4'
            self.ctc_send_packet( 4, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 5'
            self.ctc_verify_packet( exp_pkt, 5)
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet [ptf_intf 1, ptf_intf 2, ptf_intf 3, ptf_intf 4] -> ptf_intf 5 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
            group_stage,
            group_bind_point_list,
            group_type)

        # setup ACL tables to block based on Source MAC
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = 1
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = '00:22:22:22:22:22'
        mac_dst = None
        mac_src_mask = 'ff:ff:ff:ff:ff:ff'
        mac_dst_mask = None
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
        ip_src = None
        ip_src_mask = None
        ip_src1 = "192.168.0.1"
        ip_src1_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        is_ipv6 = False
        #ip qos info
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        ip_proto = None
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None

        # create ACL table #1
        acl_table_id1 = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            ip_proto,
            in_ports,
            out_ports,
            in_port,
            out_port,
            src_l4_port,
            dst_l4_port)
        acl_entry_id1 = sai_thrift_create_acl_entry(self.client,
            acl_table_id1,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_src, ip_src_mask,
            ip_dst, ip_dst_mask,
            is_ipv6,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            ip_proto,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn)

        # create ACL table #2
        acl_table_id2 = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            ip_proto,
            in_ports,
            out_ports,
            in_port,
            out_port,
            src_l4_port,
            dst_l4_port)
        acl_entry_id2 = sai_thrift_create_acl_entry(self.client,
            acl_table_id2,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_src1, ip_src1_mask,
            ip_dst, ip_dst_mask,
            is_ipv6,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            ip_proto,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn)

        # setup ACL table group members
        group_member_priority1 = 1
        group_member_priority2 = 100

        # create ACL table group members
        acl_table_group_member_id1 = sai_thrift_create_acl_table_group_member(self.client,
            acl_table_group_id,
            acl_table_id1,
            group_member_priority1)
        acl_table_group_member_id2 = sai_thrift_create_acl_table_group_member(self.client,
            acl_table_group_id,
            acl_table_id2,
            group_member_priority2)

        # bind this ACL table group to port1, port2, port3, port4 object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_group_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        attr_value1 = sai_thrift_attribute_value_t(oid=acl_table_id2)
        attr1 = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value1)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        self.client.sai_thrift_set_port_attribute(port4, attr1)

        warmboot(self.client)
        
        try:
            assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'
            assert acl_table_id1 > 0, 'acl_entry_id1 is <= 0'
            assert acl_entry_id1 > 0, 'acl_entry_id1 is <= 0'
            assert acl_table_id2 > 0, 'acl_entry_id2 is <= 0'
            assert acl_entry_id2 > 0, 'acl_entry_id2 is <= 0'
            assert acl_table_group_member_id1 > 0, 'acl_table_group_member_id1 is <= 0'
            assert acl_table_group_member_id2 > 0, 'acl_table_group_member_id2 is <= 0'

            print '#### ACL \'DROP, src mac 00:22:22:22:22:22, in_ports[ptf_intf_1,2,3,4]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_send_packet( 1, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 5'
            self.ctc_verify_no_packet( exp_pkt, 5, default_time_out)
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 2, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 5'
            self.ctc_verify_no_packet( exp_pkt, 5, default_time_out)
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 3'
            self.ctc_send_packet( 3, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 5'
            self.ctc_verify_no_packet( exp_pkt, 5, default_time_out)
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 4'
            self.ctc_send_packet( 4, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 5'
            self.ctc_verify_no_packet( exp_pkt, 5, default_time_out)
        finally:
            # unbind this ACL table from port1, port2, port3, port4 object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_set_port_attribute(port4, attr)
            # cleanup ACL
            self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id1)
            self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id2)
            self.client.sai_thrift_remove_acl_entry(acl_entry_id1)
            self.client.sai_thrift_remove_acl_table(acl_table_id1)
            self.client.sai_thrift_remove_acl_entry(acl_entry_id2)
            self.client.sai_thrift_remove_acl_table(acl_table_id2)
            self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id5, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_virtual_router(vr_id)
