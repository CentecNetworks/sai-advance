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
        
        mpls_inner_pkt = ach_header + str(udp_pkt)
                                  
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
            flush_all_fdb(self.client) 
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
        src_mep_id =  hexstr_to_ascii('000100080102030405060708')
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
            flush_all_fdb(self.client)
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




class func_01_create_bfd_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        min_tx = 5
        min_rx = 6
        default_mult = 3
        bfd_id = 0        
        warmboot(self.client)
        
        try:
        
            bfd_id = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
            sys_logging("creat bfd session = %d" %bfd_id)
            assert (bfd_id != SAI_NULL_OBJECT_ID)
        
        finally:
        
            sys_logging("remove bfd session = %d" %bfd_id)
            sai_thrift_remove_bfd(self.client, bfd_id)
            

class func_02_create_same_bfd_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        min_tx = 5
        min_rx = 6
        default_mult = 3
        bfd_id1 = 0 
        bfd_id2 = 0         
        warmboot(self.client)
        
        try:
        
            bfd_id1 = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
            sys_logging("creat bfd session = %d" %bfd_id1)
            assert (bfd_id1 != SAI_NULL_OBJECT_ID)
            bfd_id2 = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
            sys_logging("creat bfd session = %d" %bfd_id2)
            assert (bfd_id2 == SAI_NULL_OBJECT_ID)
            
        finally:
        
            sys_logging("remove bfd session = %d" %bfd_id1)
            sai_thrift_remove_bfd(self.client, bfd_id1)                      
            
            
            
            
class func_03_create_multi_bfd_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        
        l_disc1 = 100
        r_disc1 = 200
        l_disc2 = 300
        r_disc2 = 400        
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip1 = '20.20.20.1'
        dst_ip2 = '20.20.20.2'         
        min_tx = 5
        min_rx = 6
        default_mult = 3
        bfd_id1 = 0 
        bfd_id2 = 0         
        warmboot(self.client)
        
        try:
        
            bfd_id1 = sai_thrift_create_ip_bfd_session(self.client, l_disc1, r_disc1, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip1, min_tx, min_rx, default_mult)
            sys_logging("creat bfd session = %d" %bfd_id1)
            assert (bfd_id1 != SAI_NULL_OBJECT_ID)
            
            bfd_id2 = sai_thrift_create_ip_bfd_session(self.client, l_disc2, r_disc2, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip2, min_tx, min_rx, default_mult)
            sys_logging("creat bfd session = %d" %bfd_id2)
            assert (bfd_id2 != SAI_NULL_OBJECT_ID)

            assert (bfd_id1 != bfd_id2)
            
        finally:
            
            sys_logging("remove bfd session = %d" %bfd_id1)
            sai_thrift_remove_bfd(self.client, bfd_id1)            
            sys_logging("remove bfd session = %d" %bfd_id2)
            sai_thrift_remove_bfd(self.client, bfd_id2)             
            
            
# only test for stress because uml performance is limited 
'''
class func_04_create_max_bfd_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
              
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'       
        min_tx = 5
        min_rx = 6
        default_mult = 3 
        
        warmboot(self.client)
        
        try:
        
            ldisc_list = range(2048)
            rdisc_list = range(2048,4096)
            bfd_oid_list = range(2048)
            
            for i in range(0,2047):
                bfd_oid_list[i] = sai_thrift_create_ip_bfd_session(self.client, ldisc_list[i], rdisc_list[i], udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
                sys_logging("creat bfd session = %d" %bfd_oid_list[i])
                assert (bfd_oid_list[i] != SAI_NULL_OBJECT_ID)
            
            bfd_oid_list[2047] = sai_thrift_create_ip_bfd_session(self.client, ldisc_list[2047], rdisc_list[2047], udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
            sys_logging("creat bfd session = %d" %bfd_oid_list[2047])
            assert (bfd_oid_list[2047] == SAI_NULL_OBJECT_ID)
                
        finally:

            for i in range(0,2047):
                sys_logging("remove bfd session = %d" %bfd_oid_list[i])
                sai_thrift_remove_bfd(self.client, bfd_oid_list[i]) 
'''         
            
            
class func_05_remove_bfd_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        min_tx = 5
        min_rx = 6
        default_mult = 3
        bfd_id = 0        
        warmboot(self.client)
        
        try:
        
            bfd_id = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
            sys_logging("creat bfd session = %d" %bfd_id)
            assert (bfd_id != SAI_NULL_OBJECT_ID)

            sys_logging("remove bfd session = %d" %bfd_id)
            status = sai_thrift_remove_bfd(self.client, bfd_id) 
            assert (status == SAI_STATUS_SUCCESS)
            
        finally:
            sys_logging("Test finally")            
           
            
            
class func_06_remove_not_exist_bfd_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        min_tx = 5
        min_rx = 6
        default_mult = 3
        not_exist_bfd_id = 4294967365        
        warmboot(self.client)
        
        try:
        
            sys_logging("remove bfd session = %d" %not_exist_bfd_id)
            status = sai_thrift_remove_bfd(self.client, not_exist_bfd_id) 
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("Test finally")   

            
# test in other case
# class func_07_set_and_get_bfd_session_attr(sai_base_test.ThriftInterfaceDataPlane):


            
class scenario_01_micro_ipv4_bfd_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
                
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_head_version = 4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        dst_mac = '00:11:22:33:66:77'
        src_mac = '00:11:22:33:66:88'
        min_tx = 4
        min_rx = 4
        default_mult = 3
        micro_bfd_macda = '01:00:5e:90:00:01'  
            
        vr_id = sai_thrift_get_default_router_id(self.client)        
                  
        bfd_id = sai_thrift_create_micro_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, addr_family, src_ip, dst_ip, port1, dst_mac, src_mac, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)

        warmboot(self.client)
        
        try:
       
           sys_logging("get bfd session")
           attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
           sys_logging("get attr status = %d" %attrs.status)
           assert (attrs.status == SAI_STATUS_SUCCESS)
           
           for a in attrs.attr_list:

                if a.id == SAI_BFD_SESSION_ATTR_TYPE:
                    sys_logging("get session type = 0x%x" %a.value.s32)
                    if SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID:
                    sys_logging("get hw_lookup_valid = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_PORT:
                    sys_logging("get port1 = 0x%x" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError() 
                        
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_UDP_SRC_PORT:
                    sys_logging("get udp src port = 0x%x" %a.value.u32)
                    if udp_srcport != a.value.u32:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE:
                    sys_logging("get bfd encap type = 0x%x" %a.value.s32)
                    if SAI_BFD_ENCAPSULATION_TYPE_NONE != a.value.s32:
                        raise NotImplementedError() 
                        
                if a.id == SAI_BFD_SESSION_ATTR_IPHDR_VERSION:
                    sys_logging("get ip_head_version = 0x%x" %a.value.u8)
                    if ip_head_version != a.value.u8:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_TOS:
                    sys_logging("get ip header tos = 0x%x" %a.value.u8)
                    if 0 != a.value.u8:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_TTL:
                    u81 = ctypes.c_uint8(a.value.u8)
                    sys_logging("get ip header ttl = 0x%x" %u81.value)
                    if 255 != u81.value:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS:
                    sys_logging("get src_ip = %s" %a.value.ipaddr.addr.ip4)
                    if src_ip != a.value.ipaddr.addr.ip4:
                        raise NotImplementedError() 
                
                if a.id == SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS:
                    sys_logging("get dst_ip = %s" %a.value.ipaddr.addr.ip4)
                    if dst_ip != a.value.ipaddr.addr.ip4:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS:
                    sys_logging("get src_mac = %s" %a.value.mac)
                    if src_mac != a.value.mac:
                        raise NotImplementedError() 
                        
                if a.id == SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS:
                    sys_logging("get dst_mac = %s" %a.value.mac)
                    if dst_mac != a.value.mac:
                        raise NotImplementedError() 
                        
                if a.id == SAI_BFD_SESSION_ATTR_MULTIHOP:
                    sys_logging("get multihop = 0x%x" %a.value.booldata)
                    if multihop != a.value.booldata:
                        raise NotImplementedError()  
                
                if a.id == SAI_BFD_SESSION_ATTR_MIN_TX:
                    sys_logging("get min_tx = 0x%x" %a.value.u32)
                    if min_tx != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MIN_RX:
                    sys_logging("get min_rx = 0x%x" %a.value.u32)
                    if min_rx != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MULTIPLIER:
                    sys_logging("get default_mult = 0x%x" %a.value.u8)
                    if default_mult != a.value.u8:
                        raise NotImplementedError()    
                        
                if a.id == SAI_BFD_SESSION_ATTR_STATE:
                    sys_logging("get session state= 0x%x" %a.value.s32)
                    if SAI_BFD_SESSION_STATE_DOWN != a.value.s32:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_OFFLOAD_TYPE:
                    sys_logging("get offload type= 0x%x" %a.value.s32)
                    if SAI_BFD_SESSION_OFFLOAD_TYPE_NONE != a.value.s32:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_NEGOTIATED_TX:
                    sys_logging("get negotiated tx = 0x%x" %a.value.u32)
                    if 4 != a.value.u32:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_NEGOTIATED_RX:
                    sys_logging("get negotiated rx = 0x%x" %a.value.u32)
                    if 1000 != a.value.u32:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DIAG:
                    sys_logging("get local diag = 0x%x" %a.value.u8)
                    if 0 != a.value.u8:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DIAG:
                    sys_logging("get remote diag = 0x%x" %a.value.u8)
                    if 0 != a.value.u8:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_MULTIPLIER:
                    sys_logging("get remote multi = 0x%x" %a.value.u8)
                    if 3 != a.value.u8:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nexthop oid = 0x%x" %a.value.oid)
                    if SAI_NULL_OBJECT_ID != a.value.oid:
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

                                  
           pkt = simple_udp_packet(pktlen=66,
                                   eth_dst=micro_bfd_macda,
                                   eth_src=src_mac,
                                   ip_src=src_ip,
                                   ip_dst=dst_ip,
                                   ip_tos=0,
                                   ip_ttl=255,
                                   udp_sport=udp_srcport,
                                   udp_dport=6784,
                                   ip_ihl=None,
                                   ip_options=False,
                                   ip_id=0,
                                   with_udp_chksum=False,
                                   udp_payload=bfd_hdr)

           self.ctc_show_packet_twamp(0,str(pkt))                         
                        
        finally:

                sys_logging("remove bfd session = %d" %bfd_id)
                sai_thrift_remove_bfd(self.client, bfd_id)


class scenario_02_micro_ipv4_bfd_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_head_version = 4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        dst_mac = '00:11:22:33:66:77'
        src_mac = '00:11:22:33:66:88'
        min_tx = 100
        min_rx = 100
        default_mult = 3
        vr_id = sai_thrift_get_default_router_id(self.client) 
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        lag_oid = sai_thrift_create_lag(self.client)        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        bfd_id = sai_thrift_create_micro_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, addr_family, src_ip, dst_ip, port1, dst_mac, src_mac, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)

        warmboot(self.client)
        
        try:
       
            bfd_hdr = simple_bfd_packet(mult=3,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=1,
                                  minrxinterval=1,
                                  sta=2)
                                  
            pkt = simple_udp_packet(pktlen=100,
                                   eth_dst=router_mac,
                                   eth_src=dst_mac,
                                   ip_src=dst_ip,
                                   ip_dst=src_ip,
                                   ip_tos=0,
                                   ip_ttl=255,
                                   udp_sport=10000,
                                   udp_dport=6784,
                                   ip_ihl=None,
                                   ip_options=False,
                                   with_udp_chksum=True,
                                   udp_payload=bfd_hdr)
                        
            self.ctc_show_packet(0)
            
            self.ctc_send_packet(0, str(pkt))
                
            # sdk cli show
            # show oam mep bfd micro my-discr 100
            # local state, 1stPkt
                        
        finally:

            sys_logging("remove bfd session = %d" %bfd_id)
            sai_thrift_remove_bfd(self.client, bfd_id)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag(self.client, lag_oid) 

            


            
class scenario_03_micro_ipv6_bfd_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
                
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_head_version = 6
        src_ip = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dst_ip = '1234:5678:9abc:def0:4422:1133:5577:99ab'
        dst_mac = '00:11:22:33:66:77'
        src_mac = '00:11:22:33:66:88'
        min_tx = 4
        min_rx = 4
        default_mult = 3
        micro_bfd_macda = '01:00:5e:90:00:01'  

        vr_id = sai_thrift_get_default_router_id(self.client)        
                  
        bfd_id = sai_thrift_create_micro_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, addr_family, src_ip, dst_ip, port1, dst_mac, src_mac, min_tx, min_rx, default_mult, tos=24, ttl=100)
        sys_logging("creat bfd session = %d" %bfd_id)

        warmboot(self.client)
        
        try:
       
           sys_logging("get bfd session")
           attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
           sys_logging("get attr status = %d" %attrs.status)
           assert (attrs.status == SAI_STATUS_SUCCESS)
           
           for a in attrs.attr_list:
           
                if a.id == SAI_BFD_SESSION_ATTR_TOS:
                    sys_logging("get ip header tos = 0x%x" %a.value.u8)
                    if 24 != a.value.u8:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_TTL:
                    u81 = ctypes.c_uint8(a.value.u8)
                    sys_logging("get ip header ttl = 0x%x" %u81.value)
                    if 100 != u81.value:
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

                                  
           pkt = simple_ipv6_udp_packet(pktlen=86,
                                   eth_dst=micro_bfd_macda,
                                   eth_src=src_mac,
                                   ipv6_src=src_ip,
                                   ipv6_dst=dst_ip,
                                   ipv6_tc=24<<2,
                                   ipv6_hlim=100,
                                   udp_sport=udp_srcport,
                                   udp_dport=6784,
                                   with_udp_chksum=False,
                                   udp_payload=bfd_hdr)

           self.ctc_show_packet_twamp(0,str(pkt))  
           
        finally:

                sys_logging("remove bfd session = %d" %bfd_id)
                sai_thrift_remove_bfd(self.client, bfd_id)
            

class scenario_04_micro_ipv6_bfd_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_head_version = 6
        src_ip = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dst_ip = '1234:5678:9abc:def0:4422:1133:5577:99ab'
        dst_mac = '00:11:22:33:66:77'
        src_mac = '00:11:22:33:66:88'
        min_tx = 100
        min_rx = 100
        default_mult = 3

        vr_id = sai_thrift_get_default_router_id(self.client) 
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        lag_oid = sai_thrift_create_lag(self.client)        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
                  
        bfd_id = sai_thrift_create_micro_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, addr_family, src_ip, dst_ip, port1, dst_mac, src_mac, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)

        warmboot(self.client)
        
        try:
       
            bfd_hdr = simple_bfd_packet(mult=3,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=1,
                                  minrxinterval=1,
                                  sta=2)
                                  
            pkt = simple_ipv6_udp_packet(pktlen=100,
                                   eth_dst=router_mac,
                                   eth_src=dst_mac,
                                   ipv6_src=dst_ip,
                                   ipv6_dst=src_ip,
                                   udp_sport=10000,
                                   udp_dport=6784,
                                   with_udp_chksum=True,
                                   udp_payload=bfd_hdr)
                        
            self.ctc_show_packet(0)
            
            self.ctc_send_packet( 0, str(pkt))
            
            # sdk cli show
            # show oam mep bfd micro my-discr 100
            # local state, 1stPkt
                        
        finally:

            sys_logging("remove bfd session = %d" %bfd_id)
            sai_thrift_remove_bfd(self.client, bfd_id)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag(self.client, lag_oid) 

            
class scenario_05_ipv4_bfd_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 1
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4 
        ip_head_version = 4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        min_tx = 10
        min_rx = 20
        default_mult = 5
     
        bfd_id = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        dmac1 = '00:11:22:33:44:55'
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)

        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
                
        warmboot(self.client)
        
        try:

           sys_logging("get bfd session")
           attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
           sys_logging("get attr status = %d" %attrs.status)
           assert (attrs.status == SAI_STATUS_SUCCESS)
           
           for a in attrs.attr_list:
               
                if a.id == SAI_BFD_SESSION_ATTR_MULTIHOP:
                    sys_logging("get multihop = 0x%x" %a.value.booldata)
                    if multihop != a.value.booldata:
                        raise NotImplementedError()  
                
                if a.id == SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID:
                    sys_logging("get hw_lookup_valid = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()                         

                if a.id == SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER:
                    sys_logging("get vr_id = 0x%x" %a.value.oid)
                    if vr_id != a.value.oid:
                        raise NotImplementedError() 

           attr_value = sai_thrift_attribute_value_t(booldata=1)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status != SAI_STATUS_SUCCESS)
            
           attr_value = sai_thrift_attribute_value_t(oid=vr_id)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status != SAI_STATUS_SUCCESS)

           attr_value = sai_thrift_attribute_value_t(oid=port1)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_PORT, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status != SAI_STATUS_SUCCESS)

           attr_value = sai_thrift_attribute_value_t(u8=1)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TC, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status != SAI_STATUS_SUCCESS)
           
           attr_value = sai_thrift_attribute_value_t(u8=16)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TOS, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status == SAI_STATUS_SUCCESS)

           attr_value = sai_thrift_attribute_value_t(u8=123)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TTL, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status == SAI_STATUS_SUCCESS)

           tmp_mac='00:00:00:00:00:01'
           attr_value = sai_thrift_attribute_value_t(mac=tmp_mac)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_SRC_MAC_ADDRESS, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status != SAI_STATUS_SUCCESS)

           attr_value = sai_thrift_attribute_value_t(mac=tmp_mac)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_DST_MAC_ADDRESS, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status != SAI_STATUS_SUCCESS)

           attr_value = sai_thrift_attribute_value_t(u32=100)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MIN_TX, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status == SAI_STATUS_SUCCESS)

           attr_value = sai_thrift_attribute_value_t(u32=200)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MIN_RX, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status == SAI_STATUS_SUCCESS)
           
           attr_value = sai_thrift_attribute_value_t(u8=10)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MULTIPLIER, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status == SAI_STATUS_SUCCESS)
           
           attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
           sys_logging("get attr status = %d" %attrs.status)
           assert (attrs.status == SAI_STATUS_SUCCESS)
           
           for a in attrs.attr_list:

                if a.id == SAI_BFD_SESSION_ATTR_TOS:
                    sys_logging("get tos = 0x%x" %a.value.u8)
                    if 16 != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_TTL:
                    sys_logging("get ttl = 0x%x" %a.value.u8)
                    if 123 != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_MIN_TX:
                    sys_logging("get min tx = 0x%x" %a.value.u32)
                    if 100 != a.value.u32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_MIN_RX:
                    sys_logging("get min rx  = 0x%x" %a.value.u32)
                    if 200 != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MULTIPLIER:
                    sys_logging("get local multi = 0x%x" %a.value.u8)
                    if 10 != a.value.u8:
                        raise NotImplementedError()
                        
           self.ctc_show_packet(0)
           
           
        finally:
        
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)            


class scenario_06_ipv4_bfd_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        min_tx = 100
        min_rx = 100
        default_mult = 3
                
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        dst_ip_subnet = '20.20.20.0'
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
                                  minrxinterval=1,
                                  sta=2)
                                  
        pkt = simple_udp_packet(pktlen=100,
                                   eth_dst=router_mac,
                                   eth_src=dmac1,
                                   ip_src=dst_ip,
                                   ip_dst=src_ip,
                                   ip_tos=0,
                                   ip_ttl=255,
                                   udp_sport=10000,
                                   udp_dport=3784,
                                   ip_ihl=None,
                                   ip_options=False,
                                   with_udp_chksum=True,
                                   udp_payload=bfd_hdr)
        
        warmboot(self.client)
        
        try:
            
            self.ctc_show_packet(0)
            
            self.ctc_send_packet( 0, str(pkt))
            # pdb.set_trace()
            # sdk cli show
            # show oam mep bfd ip my-discr 100
            # local state, 1stPkt
            
        finally:
            
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)

            
class scenario_07_ipv4_bfd_tx_test_with_nh(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 1
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4 
        ip_head_version = 4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        min_tx = 5
        min_rx = 6
        default_mult = 3

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        dmac1 = '00:11:22:33:44:55'
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)

        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        bfd_id = sai_thrift_create_ip_bfd_session_with_nh(self.client, l_disc, r_disc, udp_srcport, multihop, nhop1, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
               
        warmboot(self.client)
                
        try:

           sys_logging("get bfd session")
           attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
           sys_logging("get attr status = %d" %attrs.status)
           assert (attrs.status == SAI_STATUS_SUCCESS)
           
           for a in attrs.attr_list:


                if a.id == SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID:
                    sys_logging("get hw_lookup_valid = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()                          

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nexthop oid = 0x%x" %a.value.oid)
                    if nhop1 != a.value.oid:
                        raise NotImplementedError() 

           attr_value = sai_thrift_attribute_value_t(oid=nhop1)
           attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_NEXT_HOP_ID, value=attr_value)
           status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
           sys_logging("set bfd attr status = %d" %status)
           assert (status != SAI_STATUS_SUCCESS)
           
           self.ctc_show_packet(0)
           
        finally:
        
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            

class scenario_08_ipv6_bfd_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV6 
        ip_head_version = 6
        src_ip = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dst_ip = '1234:5678:9abc:def0:4422:1133:5577:99ab'       
        min_tx = 5
        min_rx = 6
        default_mult = 3
     
        bfd_id = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult, tos=16)
        sys_logging("creat bfd session = %d" %bfd_id)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        dmac1 = '00:11:22:33:44:55'
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)

        dst_ip_subnet = '1234:5678:9abc:def0:4422:1133:5577:0000'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'     
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
                
        warmboot(self.client)
        
        try:

           sys_logging("get bfd session")
           attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
           sys_logging("get attr status = %d" %attrs.status)
           assert (attrs.status == SAI_STATUS_SUCCESS)
           
           for a in attrs.attr_list:

                if a.id == SAI_BFD_SESSION_ATTR_TYPE:
                    sys_logging("get bfd session type = 0x%x" %a.value.s32)
                    if SAI_BFD_SESSION_TYPE_ASYNC_ACTIVE != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_LOCAL_DISCRIMINATOR:
                    sys_logging("get l_disc = 0x%x" %a.value.u32)
                    if l_disc != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_REMOTE_DISCRIMINATOR:
                    sys_logging("get r_disc = 0x%x" %a.value.u32)
                    if r_disc != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_UDP_SRC_PORT:
                    sys_logging("get udp src port = 0x%x" %a.value.u32)
                    if udp_srcport != a.value.u32:
                        raise NotImplementedError() 
                
                if a.id == SAI_BFD_SESSION_ATTR_MULTIHOP:
                    sys_logging("get multihop = 0x%x" %a.value.booldata)
                    if multihop != a.value.booldata:
                        raise NotImplementedError()  
                
                if a.id == SAI_BFD_SESSION_ATTR_IPHDR_VERSION:
                    sys_logging("get ip_head_version = 0x%x" %a.value.u8)
                    if ip_head_version != a.value.u8:
                        raise NotImplementedError() 
                
                if a.id == SAI_BFD_SESSION_ATTR_SRC_IP_ADDRESS:
                    sys_logging("get src_ip = %s" %a.value.ipaddr.addr.ip6)
                    if src_ip != a.value.ipaddr.addr.ip6:
                        raise NotImplementedError() 
                
                if a.id == SAI_BFD_SESSION_ATTR_DST_IP_ADDRESS:
                    sys_logging("get dst_ip = %s" %a.value.ipaddr.addr.ip6)
                    if dst_ip != a.value.ipaddr.addr.ip6:
                        raise NotImplementedError() 
                
                if a.id == SAI_BFD_SESSION_ATTR_MIN_TX:
                    sys_logging("get min_tx = 0x%x" %a.value.u32)
                    if min_tx != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MIN_RX:
                    sys_logging("get min_rx = 0x%x" %a.value.u32)
                    if min_rx != a.value.u32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MULTIPLIER:
                    sys_logging("get default_mult = 0x%x" %a.value.u8)
                    if default_mult != a.value.u8:
                        raise NotImplementedError()    

                if a.id == SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID:
                    sys_logging("get hw_lookup_valid = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()                         

                if a.id == SAI_BFD_SESSION_ATTR_VIRTUAL_ROUTER:
                    sys_logging("get vr_id = 0x%x" %a.value.oid)
                    if vr_id != a.value.oid:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_BFD_ENCAPSULATION_TYPE:
                    if SAI_BFD_ENCAPSULATION_TYPE_NONE != a.value.s32:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_TOS:
                    sys_logging("get ip header tos = 0x%x" %a.value.u8)
                    if 16 != a.value.u8:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_TTL:
                    u81 = ctypes.c_uint8(a.value.u8)
                    sys_logging("get ip header ttl = 0x%x" %u81.value)
                    if 255 != u81.value:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_OFFLOAD_TYPE:
                    if SAI_BFD_SESSION_OFFLOAD_TYPE_NONE != a.value.s32:
                        raise NotImplementedError() 

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nexthop oid = 0x%x" %a.value.oid)
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError() 
                       
           self.ctc_show_packet(0)
           
        finally:
        
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)            



class scenario_09_ipv6_bfd_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 1
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV6 
        ip_head_version = 6
        src_ip = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dst_ip = '1234:5678:9abc:def0:4422:1133:5577:99ab'       
        min_tx = 5
        min_rx = 6
        default_mult = 3
     
        bfd_id = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        dmac1 = '00:11:22:33:44:55'
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)

        dst_ip_subnet = '1234:5678:9abc:def0:4422:1133:5577:0000'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'     
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
                
        warmboot(self.client)
        
        try:

            bfd_hdr = simple_bfd_packet(mult=3,
                                  mydisc=r_disc,
                                  yourdisc=l_disc,
                                  mintxinterval=1,
                                  minrxinterval=1,
                                  sta=2)
                                  
            pkt = simple_ipv6_udp_packet(pktlen=100,
                                   eth_dst=router_mac,
                                   eth_src=dmac1,
                                   ipv6_src=dst_ip,
                                   ipv6_dst=src_ip,
                                   udp_sport=10000,
                                   udp_dport=4784,
                                   with_udp_chksum=True,
                                   udp_payload=bfd_hdr)
                        
            self.ctc_show_packet(0)
            
            self.ctc_send_packet( 0, str(pkt))
            
            # sdk cli show
            # show oam mep bfd ip my-discr 100
            # local state, 1stPkt
           
        finally:
        
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)  


# ipv6 bfd must use reroute, can not use nexthop            
'''
class scenario_10_ipv6_bfd_tx_test_with_nh(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 1
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV6 
        ip_head_version = 6
        src_ip = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dst_ip = '1234:5678:9abc:def0:4422:1133:5577:99ab'       
        min_tx = 5
        min_rx = 6
        default_mult = 3

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        dmac1 = '00:11:22:33:44:55'
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)

        dst_ip_subnet = '1234:5678:9abc:def0:4422:1133:5577:0000'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'     
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        bfd_id = sai_thrift_create_ip_bfd_session_with_nh(self.client, l_disc, r_disc, udp_srcport, multihop, nhop1, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
               
        warmboot(self.client)
        
        try:

           sys_logging("get bfd session")
           attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
           sys_logging("get attr status = %d" %attrs.status)
           assert (attrs.status == SAI_STATUS_SUCCESS)
           
           for a in attrs.attr_list:

                if a.id == SAI_BFD_SESSION_ATTR_HW_LOOKUP_VALID:
                    sys_logging("get hw_lookup_valid = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()                         

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nexthop oid = 0x%x" %a.value.oid)
                    if nhop1 != a.value.oid:
                        raise NotImplementedError() 
                       
           self.ctc_show_packet(0)
           
        finally:
        
            sys_logging("clear configuration")
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)            
'''



class scenario_11_mpls_ipv4_lsp_bfd_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        addr_family = SAI_IP_ADDR_FAMILY_IPV4  
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        dst_ip1 = '127.0.0.1'
        min_tx = 100
        min_rx = 100
        default_mult = 3
             
        vr_id = sai_thrift_get_default_router_id(self.client)       
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
               
              
        dmac1 = '00:11:22:33:44:55'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)

        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
        
        inseg_lsp_label = 400
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        
        nhp_lsp_label = 100
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, inseg_lsp_label, nhop_lsp_pe1_to_p, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        
        try:

            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE:
                    sys_logging("get mpls_encap_type = 0x%x" %a.value.s32)
                    if mpls_encap_type != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL:
                    sys_logging("get inseg_lsp_label = 0x%x" %a.value.u32)
                    if inseg_lsp_label != a.value.u32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nhop_lsp_pe1_to_p = 0x%x" %a.value.oid)
                    if nhop_lsp_pe1_to_p != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_MPLS_TTL:
                    sys_logging("get mpls ttl = 0x%x" %a.value.u8)
                    if 64 != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_MPLS_EXP:
                    sys_logging("get mpls exp = 0x%x" %a.value.u8)
                    if 7 != a.value.u8:
                        raise NotImplementedError()
                        
            attr_value = sai_thrift_attribute_value_t(s32=mpls_encap_type)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status != SAI_STATUS_SUCCESS)
 
            attr_value = sai_thrift_attribute_value_t(u8=123)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MPLS_TTL, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
 
            attr_value = sai_thrift_attribute_value_t(u8=5)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_MPLS_EXP, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
           
            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_TTL:
                    sys_logging("get mpls ttl = 0x%x" %a.value.u8)
                    if 123 != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_MPLS_EXP:
                    sys_logging("get mpls exp = 0x%x" %a.value.u8)
                    if 5 != a.value.u8:
                        raise NotImplementedError()
                        
            bfd_hdr = simple_bfd_packet(mult=3,
                                        mydisc=r_disc,
                                        yourdisc=l_disc,
                                        mintxinterval=1,
                                        minrxinterval=1,
                                        sta=2)
                                    
            pkt = simple_udp_packet(pktlen=100,
                                    eth_dst=router_mac,
                                    eth_src=dmac1,
                                    ip_src=dst_ip,
                                    ip_dst=dst_ip1,
                                    ip_tos=0,
                                    ip_ttl=255,
                                    udp_sport=10000,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(pkt)[14:]
            
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':1,'s':1}]
            
            pkt = simple_mpls_packet(eth_dst=router_mac,
                                 eth_src=dmac1,
                                 mpls_type=0x8847,
                                 mpls_tags= mpls_label_stack,
                                 inner_frame = mpls_inner_pkt)
                        
            self.ctc_show_packet(0)
            #pdb.set_trace()
            
            self.ctc_send_packet( 0, str(pkt))
            
            # sdk cli show
            # show oam mep bfd mpls my-discr 100 
            # local state, 1stPkt

            
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


#lsp ipv6

class scenario_12_mpls_pw_vccv_raw_bfd_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        min_tx = 5
        min_rx = 6
        default_mult = 3
                   
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
                
        dmac1 = '00:11:22:33:44:55'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)

        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
               
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(" bridge_id = %d" % bridge_id)
        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        # lsp label    
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        # pw tunnel
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=64, encap_tagged_vlan=200)  
        
        # pw label                
        nhp_pw2_label = 100
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)

        # ILM entry for tunnel label pop       
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)       
        inseg_lsp_label = 300
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)        
        
        # ILM VPLS entry for VC lable       
        pop_nums = 1 
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, nhp_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, nhp_pw2_label, nhop_pw_pe1_to_pe2, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_VCCV_RAW, min_tx=min_tx, min_rx=min_rx, multip=default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        
        try:

            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE:
                    sys_logging("get mpls_encap_type = 0x%x" %a.value.s32)
                    if mpls_encap_type != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL:
                    sys_logging("get nhp_pw2_label = 0x%x" %a.value.u32)
                    if nhp_pw2_label != a.value.u32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nhop_pw_pe1_to_pe2 = 0x%x" %a.value.oid)
                    if nhop_pw_pe1_to_pe2 != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID:
                    sys_logging("get ach header valid = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE:
                    sys_logging("get ach_type = 0x%x" %a.value.s32)
                    if SAI_BFD_ACH_CHANNEL_TYPE_VCCV_RAW != a.value.s32:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status != SAI_STATUS_SUCCESS)
                       
            bfd_hdr = simple_bfd_packet(mult=3,
                                        mydisc=r_disc,
                                        yourdisc=l_disc,
                                        mintxinterval=1,
                                        minrxinterval=1,
                                        sta=2)                                   

            ach_header = hexstr_to_ascii('10000007')
            
            mpls_inner_pkt = ach_header + str(bfd_hdr)
                                    
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':nhp_pw2_label,'tc':0,'ttl':1,'s':1}]
            pkt = simple_mpls_packet(eth_dst=router_mac,
                                    eth_src=dmac1,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls_label_stack,
                                    inner_frame = mpls_inner_pkt)

                            
            self.ctc_show_packet(0)
            #pdb.set_trace()
            self.ctc_send_packet( 0, str(pkt))
            
            # sdk cli show
            # show oam mep bfd mpls my-discr 100 
            # local state, 1stPkt


            
        finally:
        
            sys_logging("clear configuration")
            flush_all_fdb(self.client) 
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(nhp_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)            
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)           
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)




class scenario_13_mpls_pw_vccv_ipv4_bfd_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        dst_ip1 = '127.0.0.1'       
        min_tx = 5
        min_rx = 6
        default_mult = 3
                   
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
                
        dmac1 = '00:11:22:33:44:55'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)

        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
               
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(" bridge_id = %d" % bridge_id)
        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        # lsp label    
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        # pw tunnel
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=64, encap_tagged_vlan=200)  
        
        # pw label                
        nhp_pw2_label = 100
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)

        # ILM entry for tunnel label pop       
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)       
        inseg_lsp_label = 300
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)        
        
        # ILM VPLS entry for VC lable       
        pop_nums = 1 
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, nhp_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip1, mpls_encap_type, nhp_pw2_label, nhop_pw_pe1_to_pe2, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV4, min_tx=min_tx, min_rx=min_rx, multip=default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        
        try:

            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE:
                    sys_logging("get mpls_encap_type = 0x%x" %a.value.s32)
                    if mpls_encap_type != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL:
                    sys_logging("get nhp_pw2_label = 0x%x" %a.value.u32)
                    if nhp_pw2_label != a.value.u32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nhop_pw_pe1_to_pe2 = 0x%x" %a.value.oid)
                    if nhop_pw_pe1_to_pe2 != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID:
                    sys_logging("get ach header valid = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE:
                    sys_logging("get ach_type = 0x%x" %a.value.s32)
                    if SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV4 != a.value.s32:
                        raise NotImplementedError()
                       
            bfd_hdr = simple_bfd_packet(mult=3,
                                        mydisc=r_disc,
                                        yourdisc=l_disc,
                                        mintxinterval=1,
                                        minrxinterval=1,
                                        sta=2)
                                    
            pkt = simple_udp_packet(pktlen=100,
                                    eth_dst=router_mac,
                                    eth_src=dmac1,
                                    ip_src=dst_ip,
                                    ip_dst=dst_ip1,
                                    ip_tos=0,
                                    ip_ttl=255,
                                    udp_sport=10000,
                                    udp_dport=3784,
                                    ip_ihl=None,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=bfd_hdr)
                                    
            mpls_inner_pkt = str(pkt)[14:]
                                            

            ach_header = hexstr_to_ascii('10000021')
            
            mpls_inner_pkt = ach_header + str(mpls_inner_pkt)
                                    
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':nhp_pw2_label,'tc':0,'ttl':1,'s':1}]
            pkt = simple_mpls_packet(eth_dst=router_mac,
                                    eth_src=dmac1,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls_label_stack,
                                    inner_frame = mpls_inner_pkt)

                            
            self.ctc_show_packet(0)
            #pdb.set_trace()
            self.ctc_send_packet( 0, str(pkt))
            
            # sdk cli show
            # show oam mep bfd mpls my-discr 100 
            # local state, 1stPkt


            
        finally:
        
            sys_logging("clear configuration")
            flush_all_fdb(self.client) 
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(nhp_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)            
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)           
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)




class scenario_14_mpls_pw_vccv_ipv6_bfd_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        src_ip = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dst_ip = '1234:5678:9abc:def0:4422:1133:5577:99ab'         
        dst_ip1 = '::FFFF:7f00:0'       
        min_tx = 5
        min_rx = 6
        default_mult = 3
                   
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
                
        dmac1 = '00:11:22:33:44:55'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)

        dst_ip_subnet = '1234:5678:9abc:def0:4422:1133:5577:0000'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'      
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
               
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(" bridge_id = %d" % bridge_id)
        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        # lsp label    
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        # pw tunnel
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=64, encap_tagged_vlan=200)  
        
        # pw label                
        nhp_pw2_label = 100
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)

        # ILM entry for tunnel label pop       
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)       
        inseg_lsp_label = 300
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)        
        
        # ILM VPLS entry for VC lable       
        pop_nums = 1 
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, nhp_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_NORMAL
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip1, mpls_encap_type, nhp_pw2_label, nhop_pw_pe1_to_pe2, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV6, min_tx=min_tx, min_rx=min_rx, multip=default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        
        try:

            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE:
                    sys_logging("get mpls_encap_type = 0x%x" %a.value.s32)
                    if mpls_encap_type != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL:
                    sys_logging("get nhp_pw2_label = 0x%x" %a.value.u32)
                    if nhp_pw2_label != a.value.u32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nhop_pw_pe1_to_pe2 = 0x%x" %a.value.oid)
                    if nhop_pw_pe1_to_pe2 != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID:
                    sys_logging("get ach header valid = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE:
                    sys_logging("get ach_type = 0x%x" %a.value.s32)
                    if SAI_BFD_ACH_CHANNEL_TYPE_VCCV_IPV6 != a.value.s32:
                        raise NotImplementedError()
                       
            bfd_hdr = simple_bfd_packet(mult=3,
                                        mydisc=r_disc,
                                        yourdisc=l_disc,
                                        mintxinterval=1,
                                        minrxinterval=1,
                                        sta=2)
                                    
            pkt = simple_ipv6_udp_packet(pktlen=100,
                                   eth_dst=router_mac,
                                   eth_src=dmac1,
                                   ipv6_src=dst_ip,
                                   ipv6_dst=dst_ip1,
                                   udp_sport=10000,
                                   udp_dport=3784,
                                   with_udp_chksum=True,
                                   udp_payload=bfd_hdr)
                                   
            mpls_inner_pkt = str(pkt)[14:]
                                            

            ach_header = hexstr_to_ascii('10000057')
            
            mpls_inner_pkt = ach_header + str(mpls_inner_pkt)
                                    
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':nhp_pw2_label,'tc':0,'ttl':1,'s':1}]
            pkt = simple_mpls_packet(eth_dst=router_mac,
                                    eth_src=dmac1,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls_label_stack,
                                    inner_frame = mpls_inner_pkt)

                            
            self.ctc_show_packet(0)
            #pdb.set_trace()
            self.ctc_send_packet( 0, str(pkt))
            
            # sdk cli show
            # show oam mep bfd mpls my-discr 100 
            # local state, 1stPkt


            
        finally:
        
            sys_logging("clear configuration")
            flush_all_fdb(self.client) 
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(nhp_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)            
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)           
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)


         
class scenario_15_mpls_tp_pw_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        dst_ip1 = '127.0.0.1'       
        min_tx = 5
        min_rx = 6
        default_mult = 3
                   
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
                
        dmac1 = '00:11:22:33:44:55'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)

        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
               
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(" bridge_id = %d" % bridge_id)
        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        # lsp label    
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        # pw tunnel
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=64, encap_tagged_vlan=200)  
        
        # pw label                
        nhp_pw2_label = 100
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)

        # ILM entry for tunnel label pop       
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)       
        inseg_lsp_label = 300
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)        
        
        # ILM VPLS entry for VC lable       
        pop_nums = 1 
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, nhp_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip1, mpls_encap_type, nhp_pw2_label, nhop_pw_pe1_to_pe2, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=min_rx, multip=default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
               
        try:

            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE:
                    sys_logging("get mpls_encap_type = 0x%x" %a.value.s32)
                    if mpls_encap_type != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL:
                    sys_logging("get nhp_pw2_label = 0x%x" %a.value.u32)
                    if nhp_pw2_label != a.value.u32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nhop_pw_pe1_to_pe2 = 0x%x" %a.value.oid)
                    if nhop_pw_pe1_to_pe2 != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID:
                    sys_logging("get ach header valid = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE:
                    sys_logging("get ach_type = 0x%x" %a.value.s32)
                    if SAI_BFD_ACH_CHANNEL_TYPE_TP != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL:
                    sys_logging("get without_gal = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_TP_CV_ENABLE:
                    sys_logging("get cv enable = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

     
            bfd_hdr = simple_bfd_packet(mult=3,
                                        mydisc=r_disc,
                                        yourdisc=l_disc,
                                        mintxinterval=1,
                                        minrxinterval=1,
                                        sta=2)
                                                                              
            ach_header = hexstr_to_ascii('10000022')
            
            mpls_inner_pkt = ach_header + str(bfd_hdr)
                                    
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':nhp_pw2_label,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]         
            pkt = simple_mpls_packet(eth_dst=router_mac,
                                    eth_src=dmac1,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls_label_stack,
                                    inner_frame = mpls_inner_pkt)

                            
            self.ctc_show_packet(0)
            #pdb.set_trace()
            self.ctc_send_packet( 0, str(pkt))
            
            # sdk cli show
            # show oam mep bfd tp-oam label 100 
            # local state, 1stPkt


        finally:
        
            sys_logging("clear configuration")
            flush_all_fdb(self.client) 
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(nhp_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)            
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)           
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)            
            
            
            
class scenario_16_mpls_tp_pw_tx_and_rx_test_without_gal(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        dst_ip1 = '127.0.0.1'       
        min_tx = 5
        min_rx = 6
        default_mult = 3
                   
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
                
        dmac1 = '00:11:22:33:44:55'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id1)

        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
               
        sys_logging("Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging(" bridge_id = %d" % bridge_id)
        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        
        # lsp label    
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id1, nhp_lsp_label_list)
        
        # pw tunnel
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_RAW, decap_cw_en=True, encap_cw_en=True, encap_ttl_val=64, encap_tagged_vlan=200)  
        
        # pw label                
        nhp_pw2_label = 100
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        label_list = [nhp_pw2_label_for_list]
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)

        # ILM entry for tunnel label pop       
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)       
        inseg_lsp_label = 300
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)        
        
        # ILM VPLS entry for VC lable       
        pop_nums = 1 
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, nhp_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip1, mpls_encap_type, nhp_pw2_label, nhop_pw_pe1_to_pe2, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=min_rx, multip=default_mult, cv_en=0, src_mepid=None, without_gal=1)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        
        try:

            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE:
                    sys_logging("get mpls_encap_type = 0x%x" %a.value.s32)
                    if mpls_encap_type != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL:
                    sys_logging("get nhp_pw2_label = 0x%x" %a.value.u32)
                    if nhp_pw2_label != a.value.u32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nhop_pw_pe1_to_pe2 = 0x%x" %a.value.oid)
                    if nhop_pw_pe1_to_pe2 != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID:
                    sys_logging("get ach header valid = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE:
                    sys_logging("get ach_type = 0x%x" %a.value.s32)
                    if SAI_BFD_ACH_CHANNEL_TYPE_TP != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL:
                    sys_logging("get without_gal = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

            bfd_hdr = simple_bfd_packet(mult=3,
                                        mydisc=r_disc,
                                        yourdisc=l_disc,
                                        mintxinterval=1,
                                        minrxinterval=1,
                                        sta=2)
                                                                              
            ach_header = hexstr_to_ascii('10000022')
            
            mpls_inner_pkt = ach_header + str(bfd_hdr)
                                    
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':nhp_pw2_label,'tc':0,'ttl':64,'s':1}]         
            pkt = simple_mpls_packet(eth_dst=router_mac,
                                    eth_src=dmac1,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls_label_stack,
                                    inner_frame = mpls_inner_pkt)

                            
            self.ctc_show_packet(0)
            #pdb.set_trace()
            self.ctc_send_packet( 0, str(pkt))
            
            # sdk cli show
            # show oam mep bfd tp-oam label 100 
            # local state, 1stPkt


            
        finally:
        
            sys_logging("clear configuration")
            flush_all_fdb(self.client) 
            sai_thrift_remove_bfd(self.client, bfd_id)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
            self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip, dmac1)            
            inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)
            inseg_entry = sai_thrift_inseg_entry_t(nhp_pw2_label) 
            self.client.sai_thrift_remove_inseg_entry(inseg_entry)            
            self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)           
            self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
            self.client.sai_thrift_remove_bridge(bridge_id)            
                        


class scenario_17_mpls_tp_lsp_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0] 
        port2 = port_list[1]           
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        dst_ip1 = '127.0.0.1'       
        min_tx = 5
        min_rx = 6
        default_mult = 3
                   
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dmac1 = '00:00:00:00:00:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, src_ip, dmac1)

        dmac2 = '00:00:00:00:00:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, src_ip, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id2)

        src_ip_subnet = '10.10.10.0'        
        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, src_ip_subnet, ip_mask1, nhop1)
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)
      
        # lsp label    
        nhp_lsp_label = 100
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p1 = sai_thrift_create_mpls_nhop(self.client, addr_family, src_ip, rif_id1, nhp_lsp_label_list)
        
        nhp_lsp_label = 300
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p2 = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id2, nhp_lsp_label_list)
        
        # ILM entry for lsp label              
        inseg_lsp_label1 = 200
        inseg_lsp_label2 = 400        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label1, pop_nums, None, nhop_lsp_pe1_to_p1, packet_action)          
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label2, pop_nums, None, nhop_lsp_pe1_to_p2, packet_action)          
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, inseg_lsp_label2, nhop_lsp_pe1_to_p1, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=min_rx, multip=default_mult, cv_en=0, src_mepid=None, without_gal=0)
        sys_logging("creat bfd session = %d" %bfd_id)    
        
        warmboot(self.client)
        
        try:

            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE:
                    sys_logging("get mpls_encap_type = 0x%x" %a.value.s32)
                    if mpls_encap_type != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL:
                    sys_logging("get inseg_lsp_label2 = 0x%x" %a.value.u32)
                    if inseg_lsp_label2 != a.value.u32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nhop_lsp_pe1_to_p1 = 0x%x" %a.value.oid)
                    if nhop_lsp_pe1_to_p1 != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID:
                    sys_logging("get ach header valid = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE:
                    sys_logging("get ach_type = 0x%x" %a.value.s32)
                    if SAI_BFD_ACH_CHANNEL_TYPE_TP != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL:
                    sys_logging("get without_gal = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_TP_CV_ENABLE:
                    sys_logging("get tp cv enable = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()                        

            
            bfd_hdr = simple_bfd_packet(mult=3,
                                        mydisc=r_disc,
                                        yourdisc=l_disc,
                                        mintxinterval=1,
                                        minrxinterval=1,
                                        sta=2)
                                                                              
            ach_header = hexstr_to_ascii('10000022')
            
            mpls_inner_pkt = ach_header + str(bfd_hdr)
                                    
            mpls_label_stack = [{'label':inseg_lsp_label2,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]         
            pkt = simple_mpls_packet(eth_dst=router_mac,
                                    eth_src=dmac1,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls_label_stack,
                                    inner_frame = mpls_inner_pkt)

                            
            self.ctc_show_packet(0)
            #pdb.set_trace()
            self.ctc_send_packet( 0, str(pkt))
            
            # sdk cli show
            # show oam mep bfd tp-oam label 400 
            # local state, 1stPkt


            
        finally:
        
           sys_logging("clear configuration")
           flush_all_fdb(self.client) 
           sai_thrift_remove_bfd(self.client, bfd_id)

           inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label1) 
           self.client.sai_thrift_remove_inseg_entry(inseg_entry)
           inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label2)
           self.client.sai_thrift_remove_inseg_entry(inseg_entry)   

           self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p1)
           self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p2)
       
           sai_thrift_remove_route(self.client, vr_id, addr_family, src_ip_subnet, ip_mask1, nhop1)
           sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)

           self.client.sai_thrift_remove_next_hop(nhop1)
           self.client.sai_thrift_remove_next_hop(nhop2)           
       
           sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, src_ip, dmac1)            
           sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip, dmac2)  
         
           self.client.sai_thrift_remove_router_interface(rif_id1)
           self.client.sai_thrift_remove_router_interface(rif_id2)


           
class scenario_18_mpls_tp_lsp_bfd_cv_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0] 
        port2 = port_list[1]           
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        dst_ip1 = '127.0.0.1'       
        min_tx = 5
        min_rx = 6
        default_mult = 3
                   
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        dmac1 = '00:00:00:00:00:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, src_ip, dmac1)

        dmac2 = '00:00:00:00:00:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, src_ip, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip, rif_id2)

        src_ip_subnet = '10.10.10.0'        
        dst_ip_subnet = '20.20.20.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, src_ip_subnet, ip_mask1, nhop1)
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)
      
        # lsp label    
        nhp_lsp_label = 100
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p1 = sai_thrift_create_mpls_nhop(self.client, addr_family, src_ip, rif_id1, nhp_lsp_label_list)
        
        nhp_lsp_label = 300
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nhop_lsp_pe1_to_p2 = sai_thrift_create_mpls_nhop(self.client, addr_family, dst_ip, rif_id2, nhp_lsp_label_list)
        
        # ILM entry for lsp label              
        inseg_lsp_label1 = 200
        inseg_lsp_label2 = 400        
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label1, pop_nums, None, nhop_lsp_pe1_to_p1, packet_action)          
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label2, pop_nums, None, nhop_lsp_pe1_to_p2, packet_action)          
        
        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP
        
        src_mep_id =  hexstr_to_ascii('000100080102030405060708')     
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, inseg_lsp_label2, nhop_lsp_pe1_to_p1, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=min_rx, multip=default_mult, cv_en=1, src_mepid=src_mep_id)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        
        try:

            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE:
                    sys_logging("get mpls_encap_type = 0x%x" %a.value.s32)
                    if mpls_encap_type != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_IN_LABEL:
                    sys_logging("get inseg_lsp_label2 = 0x%x" %a.value.u32)
                    if inseg_lsp_label2 != a.value.u32:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nhop_lsp_pe1_to_p1 = 0x%x" %a.value.oid)
                    if nhop_lsp_pe1_to_p1 != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID:
                    sys_logging("get ach header valid = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE:
                    sys_logging("get ach_type = 0x%x" %a.value.s32)
                    if SAI_BFD_ACH_CHANNEL_TYPE_TP != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL:
                    sys_logging("get without_gal = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()

                if a.id == SAI_BFD_SESSION_ATTR_TP_CV_ENABLE:
                    sys_logging("get tp cv enable = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()                        

                if a.id == SAI_BFD_SESSION_ATTR_TP_CV_SRC_MEP_ID:
                    sys_logging("get src_mep_id = %s" %a.value.chardata)                 
                    if src_mep_id != a.value.chardata:
                        print "TBD"
                        #raise NotImplementedError()          
                        
            bfd_hdr = simple_bfd_packet(mult=3,
                                        mydisc=r_disc,
                                        yourdisc=l_disc,
                                        mintxinterval=1,
                                        minrxinterval=1,
                                        sta=2)
            
            mep_tlv =  hexstr_to_ascii('000100080102030405060708') 

            ach_header_cc = hexstr_to_ascii('10000022')            
            ach_header_cv = hexstr_to_ascii('10000023')
            
            mpls_inner_pkt1 = ach_header_cc + str(bfd_hdr) 
            mpls_inner_pkt2 = ach_header_cv + str(bfd_hdr) + mep_tlv
            
            mpls_label_stack = [{'label':inseg_lsp_label2,'tc':0,'ttl':64,'s':0},{'label':13,'tc':0,'ttl':1,'s':1}]   
            
            pkt0 = simple_mpls_packet(eth_dst=router_mac,
                                    eth_src=dmac1,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls_label_stack,
                                    inner_frame = mpls_inner_pkt1)


            pkt1 = simple_mpls_packet(pktlen=98,
                                    eth_dst=router_mac,
                                    eth_src=dmac1,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls_label_stack,
                                    inner_frame = mpls_inner_pkt2)
                                    
            self.ctc_show_packet(0)

            self.ctc_send_packet( 0, str(pkt0))
            

            # sdk cli show
            # show oam mep bfd tp-oam label 400 
            # local state, 1stPkt

            
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TP_CV_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_BFD_SESSION_ATTR_TP_CV_ENABLE:
                    sys_logging("get cv enable = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError() 

            self.ctc_send_packet( 0, str(pkt1))

            # sdk cli show
            # show packet stats  
            # TP_BFD_CV_PDU(ID:109): 1 
            
            
        finally:
        
           sys_logging("clear configuration")
           flush_all_fdb(self.client) 
           sai_thrift_remove_bfd(self.client, bfd_id)

           inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label1) 
           self.client.sai_thrift_remove_inseg_entry(inseg_entry)
           inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label2)
           self.client.sai_thrift_remove_inseg_entry(inseg_entry)   

           self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p1)
           self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p2)
       
           sai_thrift_remove_route(self.client, vr_id, addr_family, src_ip_subnet, ip_mask1, nhop1)
           sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)

           self.client.sai_thrift_remove_next_hop(nhop1)
           self.client.sai_thrift_remove_next_hop(nhop2)           
       
           sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, src_ip, dmac1)            
           sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip, dmac2)  
         
           self.client.sai_thrift_remove_router_interface(rif_id1)
           self.client.sai_thrift_remove_router_interface(rif_id2)



class scenario_19_mpls_tp_section_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0] 
        port2 = port_list[1]           
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'        
        dst_ip1 = '127.0.0.1'       
        min_tx = 5
        min_rx = 6
        default_mult = 3
                   
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)
        
        dmac1 = '00:00:00:00:00:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, src_ip, dmac1)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, src_ip, rif_id1)

        mpls_encap_type = SAI_BFD_MPLS_TYPE_TP
        bfd_id = sai_thrift_create_mpls_bfd_session(self.client, l_disc, r_disc, udp_srcport, addr_family, src_ip, dst_ip, mpls_encap_type, None, nhop1, ach_type=SAI_BFD_ACH_CHANNEL_TYPE_TP, min_tx=min_tx, min_rx=min_rx, multip=default_mult, cv_en=0, src_mepid=None, without_gal=0, l3if_oid=rif_id1)
        sys_logging("creat bfd session = %d" %bfd_id)                
             
        warmboot(self.client)
        
        try:

            sys_logging("get bfd session")
            attrs = self.client.sai_thrift_get_bfd_attribute(bfd_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_BFD_SESSION_ATTR_MPLS_ENCAP_BFD_TYPE:
                    sys_logging("get mpls_encap_type = 0x%x" %a.value.s32)
                    if mpls_encap_type != a.value.s32:
                        raise NotImplementedError()
                                   
                if a.id == SAI_BFD_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get nhop1 = 0x%x" %a.value.oid)
                    if nhop1 != a.value.oid:
                        raise NotImplementedError()
            
                if a.id == SAI_BFD_SESSION_ATTR_ACH_HEADER_VALID:
                    sys_logging("get ach header valid = 0x%x" %a.value.booldata)
                    if 1 != a.value.booldata:
                        raise NotImplementedError()
            
                if a.id == SAI_BFD_SESSION_ATTR_ACH_CHANNEL_TYPE:
                    sys_logging("get ach_type = 0x%x" %a.value.s32)
                    if SAI_BFD_ACH_CHANNEL_TYPE_TP != a.value.s32:
                        raise NotImplementedError()
                        
                if a.id == SAI_BFD_SESSION_ATTR_TP_WITHOUT_GAL:
                    sys_logging("get without_gal = 0x%x" %a.value.booldata)
                    if 0 != a.value.booldata:
                        raise NotImplementedError()
            
                if a.id == SAI_BFD_SESSION_ATTR_TP_ROUTER_INTERFACE_ID:
                    sys_logging("get rif_od = 0x%x" %a.value.oid)
                    if rif_id1 != a.value.oid:
                        raise NotImplementedError()                        

            attr_value = sai_thrift_attribute_value_t(oid=rif_id1)
            attr = sai_thrift_attribute_t(id=SAI_BFD_SESSION_ATTR_TP_ROUTER_INTERFACE_ID, value=attr_value)
            status = self.client.sai_thrift_set_bfd_attribute(bfd_id, attr)
            sys_logging("set bfd attr status = %d" %status)
            assert (status != SAI_STATUS_SUCCESS)
            
            
            bfd_hdr = simple_bfd_packet(mult=3,
                                        mydisc=r_disc,
                                        yourdisc=l_disc,
                                        mintxinterval=1,
                                        minrxinterval=1,
                                        sta=2)
                                                                              
            ach_header = hexstr_to_ascii('10000022')
            
            mpls_inner_pkt = ach_header + str(bfd_hdr)
                                    
            mpls_label_stack = [{'label':13,'tc':0,'ttl':1,'s':1}]  
            
            pkt = simple_mpls_packet(eth_dst=router_mac,
                                    eth_src=dmac1,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls_label_stack,
                                    inner_frame = mpls_inner_pkt)

                            
            self.ctc_show_packet(0)
            
            self.ctc_send_packet( 0, str(pkt))
            
            # sdk cli show
            # show oam mep bfd tp-oam section-oam ifid 2 
            # local state, 1stPkt

            
        finally:
        
           sys_logging("clear configuration")
           sai_thrift_remove_bfd(self.client, bfd_id)
           self.client.sai_thrift_remove_next_hop(nhop1)
           sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, src_ip, dmac1)            
           self.client.sai_thrift_remove_router_interface(rif_id1)

                       