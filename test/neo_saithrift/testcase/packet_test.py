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
Thrift SAI packet tests
"""
import socket
import sys
import pdb

from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask

@group('packet test')
def ip6_to_integer(ip6):
    ip6 = socket.inet_pton(socket.AF_INET6, ip6)
    a, b = unpack(">QQ", ip6)
    return (a << 64) | b

def integer_to_ip6(ip6int):
    a = (ip6int >> 64) & ((1 << 64) - 1)
    b = ip6int & ((1 << 64) - 1)
    return socket.inet_ntop(socket.AF_INET6, pack(">QQ", a, b))

def ip4_to_integer(ip4):
    ip4int = int(socket.inet_aton('10.10.10.1').encode('hex'), 16)
    return ip4int

def integer_to_ip4(ip4int):
    return socket.inet_ntoa(hex(ip4int)[2:].zfill(8).decode('hex'))

class ptp_packet_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
                       
        ptp_sync = simple_ptp_packet(msgType=0,
                                    msgLen=44,
                                    cfHigh=0x11,
                                    cfLow=0x22334455,
                                    clockId="123",
                                    srcPortId=1,
                                    tsSecHigh=0,
                                    tsSec=0x66,
                                    tsNs=0x778899)
                                    
        ptp_delay_resp = simple_ptp_packet(msgType=9,
                                    msgLen=54,
                                    cfHigh=0x11,
                                    cfLow=0x22334455,
                                    clockId="123",
                                    srcPortId=1,
                                    tsSecHigh=0,
                                    tsSec=0x66,
                                    tsNs=0x778899,
                                    reqClockId='abc',
                                    reqSrcPortId=2)
        
        pkt1 = simple_udp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                udp_dport=319,
                                udp_payload=ptp_delay_resp)
                                
        
        
        
        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            
            #sys_logging("======send dst ip(v4) hit packet======")
            #self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( exp_pkt1, [0])
            #sys_logging("======send dst ip(v4) not hit packet======")
            #self.ctc_send_packet( 2, str(pkt2))
            #self.ctc_verify_no_packet( exp_pkt2, 0)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)