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
Thrift SAI interface bfd tests
"""
import socket
from switch import *
import sai_base_test
from ptf.mask import Mask
import pdb

@group('bfd')

class BfdIPBfdCreateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        min_tx = 5
        min_rx = 6
        default_mult = 3
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        bfd_id = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        try:
            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("set l_disc = 0x%x" %l_disc)
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("set r_disc = 0x%x" %r_disc)
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_UDP_SRC_PORT:
                    sys_logging("set udp_srcport = 0x%x" %udp_srcport)
                    sys_logging("get udp_srcport = 0x%x" %a.value.u32)
                    if udp_srcport != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER:
                    sys_logging("set vr_id = 0x%x" %vr_id)
                    sys_logging("get vr_id = 0x%x" %a.value.oid)
                    if vr_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_MIN_TX:
                    sys_logging("set min_tx = 0x%x" %min_tx)
                    sys_logging("get min_tx = 0x%x" %a.value.u32)
                    if min_tx != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_MIN_RX:
                    sys_logging("set min_rx = 0x%x" %min_rx)
                    sys_logging("get min_rx = 0x%x" %a.value.u32)
                    if min_rx != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_MULTIPLIER:
                    sys_logging("set min_rx = 0x%x" %default_mult)
                    sys_logging("get min_rx = 0x%x" %a.value.u8)
                    if default_mult != a.value.u8:
                        raise NotImplementedError()
        finally:
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            
class BfdIPv4BfdRxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        min_tx = 5
        min_rx = 6
        default_mult = 3
        
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        bfd_id = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        bfd_hdr = simple_bfd_packet(mult=3,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=1,
                                  minrxinterval=1)
                                  
        pkt = simple_udp_packet(pktlen=100,
                                   eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   ip_src='6.6.6.6',
                                   ip_dst=src_ip,
                                   ip_tos=0,
                                   ip_ttl=255,
                                   udp_sport=10000,
                                   udp_dport=3784,
                                   ip_ihl=None,
                                   ip_options=False,
                                   with_udp_chksum=True,
                                   udp_payload=bfd_hdr)
        #pdb.set_trace()
        
        warmboot(self.client)
        try:
            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("set l_disc = 0x%x" %l_disc)
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("set r_disc = 0x%x" %r_disc)
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
            
            self.ctc_show_packet(0)
            
            self.ctc_send_packet( 0, str(pkt))
            
            #sdk cli show
            # show oam mep bfd ip my-discr 100
            # local state, 1stPkt
            
        finally:
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            
class BfdIPv4BfdTxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        min_tx = 5
        min_rx = 6
        default_mult = 3
        
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        bfd_id = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        try:
            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("set l_disc = 0x%x" %l_disc)
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("set r_disc = 0x%x" %r_disc)
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
            
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)

class BfdIPv6BfdTxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        min_tx = 5
        min_rx = 6
        default_mult = 3
        
        src_ip = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dst_ip = '1234:5678:9abc:def0:4422:1133:5577:99ab'
        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        dst_ip_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        bfd_id = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        try:
            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("set l_disc = 0x%x" %l_disc)
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("set r_disc = 0x%x" %r_disc)
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
            
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            
class BfdMicroBfdTxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        min_tx = 5
        min_rx = 6
        default_mult = 3
        dst_mac = '00:11:22:33:66:77'
        src_mac = '00:11:22:33:66:88'
        
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        bfd_id = sai_thrift_create_micro_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, addr_family, src_ip, dst_ip, port1, dst_mac, src_mac, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        try:
            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("set l_disc = 0x%x" %l_disc)
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("set r_disc = 0x%x" %r_disc)
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
            
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            
class BfdMicroBfdv6TxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        min_tx = 5
        min_rx = 6
        default_mult = 3
        dst_mac = '00:11:22:33:66:77'
        src_mac = '00:11:22:33:66:88'
        
        src_ip = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dst_ip = '1234:5678:9abc:def0:4422:1133:5577:99ab'
        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        dst_ip_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        bfd_id = sai_thrift_create_micro_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, addr_family, src_ip, dst_ip, port1, dst_mac, src_mac, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        try:
            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("set l_disc = 0x%x" %l_disc)
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("set r_disc = 0x%x" %r_disc)
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
            
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            
class BfdLspBfdTxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        min_tx = 5
        min_rx = 6
        default_mult = 3
        
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        inseg_lsp_label = 200
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        
        nhp_lsp_label = 300
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, inseg_lsp_label, nhop_lsp_pe1_to_p, min_tx=min_tx, min_rx=1, multip=3)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        try:
            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("set l_disc = 0x%x" %l_disc)
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("set r_disc = 0x%x" %r_disc)
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
            
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            
class BfdPwRawBfdTxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        min_tx = 5
        min_rx = 6
        default_mult = 3
        
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(">>bridge_id = %d" % bridge_id)
        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
       
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        inseg_pw2_label = 102
        nhp_pw2_label = 202
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=64, encap_tagged_vlan=200)
        
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        pop_nums = 1 # cw add to tunnel
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, inseg_pw2_label, nhop_pw_pe1_to_pe2, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_VCCV_RAW, min_tx=min_tx, min_rx=1, multip=3)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        try:
            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("set l_disc = 0x%x" %l_disc)
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("set r_disc = 0x%x" %r_disc)
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
            
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
class BfdTpBfdPwCcTxRxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        min_tx = 5
        min_rx = 6
        default_mult = 3
        
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(">>bridge_id = %d" % bridge_id)

        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        inseg_lsp_label = 100
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        inseg_pw2_label = 102
        nhp_pw2_label = 202
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=64, encap_tagged_vlan=200)
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        pop_nums = 1 # cw add to tunnel
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, inseg_pw2_label, nhop_pw_pe1_to_pe2, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=1, multip=3)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        
        srcmac = '00:22:33:44:55:66'
        
        bfd_hdr = simple_bfd_packet(mult=3,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=1,
                                  minrxinterval=1)
                                  
        udp_pkt = simple_ip_only_udp_packet(pktlen=100,
                                   ip_src='6.6.6.6',
                                   ip_dst=src_ip,
                                   ip_tos=0,
                                   ip_ttl=255,
                                   udp_sport=10000,
                                   udp_dport=3784,
                                   ip_ihl=None,
                                   ip_options=False,
                                   with_udp_chksum=False,
                                   udp_payload=bfd_hdr)
        
        ach_header = hexstr_to_ascii('10000022')
        
        mpls_inner_pkt = ach_header + str(bfd_hdr)
                                  
        mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw2_label,'tc':0,'ttl':1,'s':1}]
        pw_pkt = simple_mpls_packet(
                            eth_dst=router_mac,
                            eth_src=srcmac,
                            mpls_type=0x8847,
                            mpls_tags= mpls_label_stack,
                            inner_frame = mpls_inner_pkt)
                                
        warmboot(self.client)
        try:
            #pdb.set_trace()
            self.ctc_send_packet( 0, str(pw_pkt))
            
            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("set l_disc = 0x%x" %l_disc)
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("set r_disc = 0x%x" %r_disc)
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
            
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
class BfdTpBfdPwCvTxTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        min_tx = 5
        min_rx = 6
        default_mult = 3
        
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dst_ip_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)
        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(">>bridge_id = %d" % bridge_id)
        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
       
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        inseg_pw2_label = 102
        nhp_pw2_label = 202
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=64, encap_tagged_vlan=200)
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        
        pop_nums = 1 # cw add to tunnel
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP
        src_mep_id = 'abcdefghijklmnopqrstuvwxyz012345'
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, inseg_pw2_label, nhop_pw_pe1_to_pe2, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=1, multip=3, cv_en=1, src_mepid=src_mep_id)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        try:
            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("set l_disc = 0x%x" %l_disc)
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("set r_disc = 0x%x" %r_disc)
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
            
            self.ctc_show_packet(0)
            
        finally:
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)