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
Thrift SAI interface TWAMP tests
"""
import socket
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask
import pdb

@group('twamp')


class func_01_create_twamp_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
            
        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '1.2.3.4'   
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '3.3.3.3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '2.2.2.2'   
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '2.2.2.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        
        
        try:

            sys_logging(" step 2 create twamp session on sender ")
            #pdb.set_trace()
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            #pdb.set_trace()
            self.ctc_show_packet(2)

            #time.sleep(5)
            
        finally:
        
            sys_logging("step 3 clear configuration")
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)        
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
            

class func_02_create_same_twamp_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
            
        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '1.2.3.4'   
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '3.3.3.3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '2.2.2.2'   
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '2.2.2.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        
        
        try:

            sys_logging(" step 2 create same twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            self.ctc_show_packet(2)
            #time.sleep(5)
          
            twamp_session_oid_1 = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid_1)          
            assert (twamp_session_oid_1 != SAI_NULL_OBJECT_ID)
            
            self.ctc_show_packet(2)
            #time.sleep(5)
            
        finally:
        
            sys_logging("step 3 clear configuration")
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid) 
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid_1)              
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)


class func_03_create_multi_twamp_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
            
        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '1.2.3.4'   
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '3.3.3.3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '2.2.2.2'   
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '2.2.2.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        
        
        try:

            sys_logging(" step 2 create multi twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            self.ctc_show_packet(2)
            #time.sleep(5)
            
            tc = 6
            pkt_len = 87
            twamp_session_oid_1 = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid_1)          
            assert (twamp_session_oid_1 != SAI_NULL_OBJECT_ID)
            
            self.ctc_show_packet(2)
            #time.sleep(5)
            
        finally:
        
            sys_logging("step 3 clear configuration")
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid) 
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid_1)              
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)


class func_04_create_max_twamp_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
            
        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '1.2.3.4'   
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '3.3.3.3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '2.2.2.2'   
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '2.2.2.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        
        
        try:

            sys_logging(" step 2 create max twamp session on sender ")
            
            twamp_session_oid_1 = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid_1)          
            assert (twamp_session_oid_1 != SAI_NULL_OBJECT_ID)
            self.ctc_show_packet(2)
            #time.sleep(5)
            
            tc = 6
            pkt_len = 512
            twamp_session_oid_2 = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid_2)          
            assert (twamp_session_oid_2 != SAI_NULL_OBJECT_ID)            
            self.ctc_show_packet(2)
            #time.sleep(5)

            tc = 5
            pkt_len = 1024
            twamp_session_oid_3 = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid_3)          
            assert (twamp_session_oid_3 != SAI_NULL_OBJECT_ID)            
            self.ctc_show_packet(2)
            #time.sleep(5)           

            tc = 4
            pkt_len = 1518
            twamp_session_oid_4 = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid_4)          
            assert (twamp_session_oid_4 != SAI_NULL_OBJECT_ID)            
            self.ctc_show_packet(2)
            #time.sleep(5)


            tc = 3
            pkt_len = 2000
            twamp_session_oid_5 = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid_5)          
            assert (twamp_session_oid_5 == SAI_NULL_OBJECT_ID)            
            #time.sleep(5)

            
        finally:
        
            sys_logging("step 3 clear configuration")
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid_1) 
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid_2)
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid_3) 
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid_4)            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)


class func_05_remove_twamp_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
            
        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '1.2.3.4'   
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '3.3.3.3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '2.2.2.2'   
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '2.2.2.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        
        
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)
            
            self.ctc_show_packet(2)
            #time.sleep(5)

            sys_logging(" step 3 remove twamp session on sender ")
            
            status = self.client.sai_thrift_remove_twamp_session(twamp_session_oid) 
            sys_logging("###remove session status  = %d###" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
        finally:
        
            sys_logging("step 4 clear configuration")       
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)


class func_06_remove_not_exist_twamp_session_fn (sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
            
        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '1.2.3.4'   
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '3.3.3.3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '2.2.2.2'   
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '2.2.2.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        
        
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)
            
            self.ctc_show_packet(2)
            #time.sleep(5)

            sys_logging(" step 3 remove twamp session on sender ")
            
            status = self.client.sai_thrift_remove_twamp_session(twamp_session_oid) 
            sys_logging("###remove session status  = %d###" %status)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_twamp_session(twamp_session_oid) 
            sys_logging("###remove session status  = %d###" %status)
            assert (status != SAI_STATUS_SUCCESS)           
        
        finally:
        
            sys_logging("step 4 clear configuration")       
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)



class func_07_set_and_get_twamp_session_attr_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
            
        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '1.2.3.4'   
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '3.3.3.3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '2.2.2.2'   
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '2.2.2.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        

        sys_logging(" step 2 create twamp session on sender ")
        
        twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
        sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
        assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

        warmboot(self.client)
        
        try:

            sys_logging(" step 3 get twamp session attr ")

            attrs = self.client.sai_thrift_get_twamp_attribute(twamp_session_oid)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_TWAMP_SESSION_ATTR_TWAMP_PORT:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_TWAMP_PORT = %d" %a.value.oid)
                    assert (a.value.oid == test_port_oid)
                    
                if a.id == SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT count= %d" %a.value.objlist.count)
                    assert (a.value.objlist.count == len(receive_port_oid))   
                    for b in a.value.objlist.object_id_list:
                        sys_logging("###SAI_TWAMP_SESSION_ATTR_RECEIVE_PORT = %d ###" %b)
                        assert (b in receive_port_oid)  
                    
                if a.id == SAI_TWAMP_SESSION_ATTR_SESSION_ROLE:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_SESSION_ROLE = %d" %a.value.s32)
                    assert (a.value.s32 == SAI_TWAMP_SESSION_ROLE_SENDER)

                if a.id == SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_UDP_SRC_PORT = %d" %a.value.u32)
                    assert (a.value.u32 == udp_src_port)

                if a.id == SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_UDP_DST_PORT = %d" %a.value.u32)
                    assert (a.value.u32 == udp_dst_port)                    

                if a.id == SAI_TWAMP_SESSION_ATTR_SRC_IP:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_SRC_IP = %s" %a.value.ipaddr.addr.ip4)
                    assert (a.value.ipaddr.addr.ip4 == src_ip)

                if a.id == SAI_TWAMP_SESSION_ATTR_DST_IP:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_DST_IP = %s" %a.value.ipaddr.addr.ip4)
                    assert (a.value.ipaddr.addr.ip4 == dst_ip)

                if a.id == SAI_TWAMP_SESSION_ATTR_TC:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_TC = %d" %a.value.u8)
                    assert (a.value.u8 == tc)

                if a.id == SAI_TWAMP_SESSION_ATTR_TTL:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_TTL = %d" %a.value.u8)
                    assert (a.value.u8 == 255)

                if a.id == SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTER:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_VPN_VIRTUAL_ROUTER = %d" %a.value.oid)
                    assert (a.value.oid == vrf_oid)

                if a.id == SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_TWAMP_ENCAPSULATION_TYPE = %d" %a.value.s32)
                    assert (a.value.s32 == encap_type)

                if a.id == SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT = %d" %a.value.booldata)
                    assert (a.value.booldata == enable_transmit)

                if a.id == SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_HW_LOOKUP_VALID = %d" %a.value.booldata)
                    assert (a.value.booldata == hw_lookup)

                if a.id == SAI_TWAMP_SESSION_ATTR_PACKET_LENGTH:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_PACKET_LENGTH = %d" %a.value.u32)
                    assert (a.value.u32 == pkt_len) 

                if a.id == SAI_TWAMP_SESSION_ATTR_AUTH_MODE:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_AUTH_MODE = %d" %a.value.s32)
                    assert (a.value.s32 == SAI_TWAMP_SESSION_AUTH_MODE_UNAUTHENTICATED)

                if a.id == SAI_TWAMP_SESSION_ATTR_NEXT_HOP_ID:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_NEXT_HOP_ID = %d" %a.value.oid)
                    assert (a.value.oid == SAI_NULL_OBJECT_ID)

                if a.id == SAI_TWAMP_SESSION_ATTR_TX_RATE:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_TX_RATE = %d" %a.value.u32)
                    assert (a.value.u32 == tx_rate)

                if a.id == SAI_TWAMP_SESSION_ATTR_TWAMP_PKT_TX_MODE:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_TWAMP_PKT_TX_MODE = %d" %a.value.s32)
                    assert (a.value.s32 == tx_mode)

                if a.id == SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_TX_PKT_DURATION = %d" %a.value.u32)
                    assert (a.value.u32 == tx_pkt_duration)
                    
                if a.id == SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_TX_PKT_CNT = %d" %a.value.u32)
                    assert (a.value.u32 == tx_pkt_cnt)

                if a.id == SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_TX_PKT_PERIOD = %d" %a.value.u32)
                    assert (a.value.u32 == tx_period) 

                if a.id == SAI_TWAMP_SESSION_ATTR_TWAMP_MODE:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_TWAMP_MODE = %d" %a.value.s32)
                    assert (a.value.s32 == SAI_TWAMP_MODE_FULL)
            
                if a.id == SAI_TWAMP_SESSION_ATTR_TIMESTAMP_FORMAT:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_TIMESTAMP_FORMAT = %d" %a.value.s32)
                    assert (a.value.s32 == SAI_TWAMP_TIMESTAMP_FORMAT_NTP)
                

            attr_value = sai_thrift_attribute_value_t(u8=6)
            attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_TC, value=attr_value)
            status = self.client.sai_thrift_set_twamp_attribute(twamp_session_oid, attr)
            sys_logging("set twamp attr status = %d" %status)
            assert (status != SAI_STATUS_SUCCESS)
                    
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_twamp_attribute(twamp_session_oid, attr)
            sys_logging("set twamp attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            attrs = self.client.sai_thrift_get_twamp_attribute(twamp_session_oid)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT = %d" %a.value.booldata)
                    assert (a.value.booldata == 0)         
                    
        finally:
        
            sys_logging("step 4 clear configuration")
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)        
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)


class func_08_get_and_clear_twamp_session_stats_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
            
        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '1.2.3.4'   
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '3.3.3.3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '2.2.2.2'   
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '2.2.2.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        
        
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            sys_logging(" step 3 check the send packet ")
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = dmac2
            macsa = router_mac
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port

            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=254,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)

            

            self.ctc_show_packet_twamp(2,str(pkt1))            
            #self.ctc_show_packet_twamp(2,str(pkt1),40,2) 

            warmboot(self.client)
        
            sys_logging("### step 4 check receive packet ###")   
            
            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('3f')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = router_mac
            macsa = dmac1
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt2 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=253,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            self.ctc_send_packet( 1, str(pkt2))
            # sdk cli check show npm session 0 stats flex 

            counter_ids = [SAI_TWAMP_SESSION_STATS_RX_PACKETS, SAI_TWAMP_SESSION_STATS_RX_BYTE, SAI_TWAMP_SESSION_STATS_TX_PACKETS, SAI_TWAMP_SESSION_STATS_TX_BYTE, SAI_TWAMP_SESSION_STATS_DROP_PACKETS,SAI_TWAMP_SESSION_STATS_MAX_LATENCY,SAI_TWAMP_SESSION_STATS_MIN_LATENCY,SAI_TWAMP_SESSION_STATS_AVG_LATENCY,SAI_TWAMP_SESSION_STATS_MAX_JITTER,SAI_TWAMP_SESSION_STATS_MIN_JITTER,SAI_TWAMP_SESSION_STATS_AVG_JITTER,SAI_TWAMP_SESSION_STATS_FIRST_TS,SAI_TWAMP_SESSION_STATS_LAST_TS,SAI_TWAMP_SESSION_STATS_DURATION_TS]
            
            list1 = self.client.sai_thrift_get_twamp_session_stats(twamp_session_oid, counter_ids, 14) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            sys_logging("###list1[8]= %d###" %list1[8])
            sys_logging("###list1[9]= %d###" %list1[9])
            sys_logging("###list1[10]= %d###" %list1[10])
            sys_logging("###list1[11]= %d###" %list1[11])
            sys_logging("###list1[12]= %d###" %list1[12])
            sys_logging("###list1[13]= %d###" %list1[13])
            
            assert (list1[0] == 1)
            assert (list1[1] == 256)
            assert (list1[2] == 1)
            assert (list1[3] == 256)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            assert (list1[8] == 0)
            assert (list1[9] == 0)
            assert (list1[10] == 0)
            assert (list1[11] == 795761)
            assert (list1[12] == 795761)
            assert (list1[13] == 0)
            
            status = self.client.sai_thrift_clear_twamp_session_stats(twamp_session_oid, counter_ids, 14)
            sys_logging("###clear twamp stats status = %d###" %status)          
            assert (status == SAI_STATUS_SUCCESS)            
           
            counter_ids = [SAI_TWAMP_SESSION_STATS_RX_PACKETS, SAI_TWAMP_SESSION_STATS_RX_BYTE, SAI_TWAMP_SESSION_STATS_TX_PACKETS, SAI_TWAMP_SESSION_STATS_TX_BYTE, SAI_TWAMP_SESSION_STATS_DROP_PACKETS,SAI_TWAMP_SESSION_STATS_MAX_LATENCY,SAI_TWAMP_SESSION_STATS_MIN_LATENCY,SAI_TWAMP_SESSION_STATS_AVG_LATENCY,SAI_TWAMP_SESSION_STATS_MAX_JITTER,SAI_TWAMP_SESSION_STATS_MIN_JITTER,SAI_TWAMP_SESSION_STATS_AVG_JITTER,SAI_TWAMP_SESSION_STATS_FIRST_TS,SAI_TWAMP_SESSION_STATS_LAST_TS,SAI_TWAMP_SESSION_STATS_DURATION_TS]
            
            list1 = self.client.sai_thrift_get_twamp_session_stats(twamp_session_oid, counter_ids, 14) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            sys_logging("###list1[8]= %d###" %list1[8])
            sys_logging("###list1[9]= %d###" %list1[9])
            sys_logging("###list1[10]= %d###" %list1[10])
            sys_logging("###list1[11]= %d###" %list1[11])
            sys_logging("###list1[12]= %d###" %list1[12])
            sys_logging("###list1[13]= %d###" %list1[13])
            
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            assert (list1[8] == 0)
            assert (list1[9] == 0)
            assert (list1[10] == 0)
            assert (list1[11] == 0)
            assert (list1[12] == 0)
            assert (list1[13] == 0)
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)        
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)

            
class scenario_01_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 0
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
            
        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '1.2.3.4'   
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '3.3.3.3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '2.2.2.2'   
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '2.2.2.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        
        
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            sys_logging(" step 3 check the send packet ")
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = dmac2
            macsa = router_mac
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port

            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=254,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)
 

            attrs = self.client.sai_thrift_get_twamp_attribute(twamp_session_oid)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT = %d" %a.value.booldata)
                    assert (a.value.booldata == enable_transmit)

            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_twamp_attribute(twamp_session_oid, attr)
            sys_logging("set twamp attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            

            attrs = self.client.sai_thrift_get_twamp_attribute(twamp_session_oid)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT = %d" %a.value.booldata)
                    assert (a.value.booldata == enable_transmit)
                    

            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_twamp_attribute(twamp_session_oid, attr)
            sys_logging("set twamp attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_twamp_attribute(twamp_session_oid)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT:
                    sys_logging("get SAI_TWAMP_SESSION_ATTR_SESSION_ENABLE_TRANSMIT = %d" %a.value.booldata)
                    assert (a.value.booldata == enable_transmit)
                    
            self.ctc_show_packet_twamp(2,str(pkt1))            
            #self.ctc_show_packet_twamp(2,str(pkt1),40,2) 

            warmboot(self.client)
        
            sys_logging("### step 4 check receive packet ###")   
            
            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('3f')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = router_mac
            macsa = dmac1
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt2 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=253,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            self.ctc_send_packet( 1, str(pkt2))
            # sdk cli check show npm session 0 stats flex 

            counter_ids = [SAI_TWAMP_SESSION_STATS_RX_PACKETS, SAI_TWAMP_SESSION_STATS_RX_BYTE, SAI_TWAMP_SESSION_STATS_TX_PACKETS, SAI_TWAMP_SESSION_STATS_TX_BYTE, SAI_TWAMP_SESSION_STATS_DROP_PACKETS,SAI_TWAMP_SESSION_STATS_MAX_LATENCY,SAI_TWAMP_SESSION_STATS_MIN_LATENCY,SAI_TWAMP_SESSION_STATS_AVG_LATENCY,SAI_TWAMP_SESSION_STATS_MAX_JITTER,SAI_TWAMP_SESSION_STATS_MIN_JITTER,SAI_TWAMP_SESSION_STATS_AVG_JITTER,SAI_TWAMP_SESSION_STATS_FIRST_TS,SAI_TWAMP_SESSION_STATS_LAST_TS,SAI_TWAMP_SESSION_STATS_DURATION_TS]
            
            list1 = self.client.sai_thrift_get_twamp_session_stats(twamp_session_oid, counter_ids, 14) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            sys_logging("###list1[8]= %d###" %list1[8])
            sys_logging("###list1[9]= %d###" %list1[9])
            sys_logging("###list1[10]= %d###" %list1[10])
            sys_logging("###list1[11]= %d###" %list1[11])
            sys_logging("###list1[12]= %d###" %list1[12])
            sys_logging("###list1[13]= %d###" %list1[13])
            
            assert (list1[0] == 1)
            assert (list1[1] == 256)
            assert (list1[2] == 1)
            assert (list1[3] == 256)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            assert (list1[8] == 0)
            assert (list1[9] == 0)
            assert (list1[10] == 0)
            assert (list1[11] == 795761)
            assert (list1[12] == 795761)
            assert (list1[13] == 0)
            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)        
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
             
            

class scenario_02_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]       
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)        
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        hw_lookup = 1
        pkt_len = 256
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '2.2.2.2'   
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '3.3.3.3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '1.2.3.4'   
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '1.2.3.0'
        ip_mask1 = '255.255.255.0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        

        try:

            sys_logging(" step 2 create twamp session on reflector ") 
            
            twamp_session_oid = sai_thrift_create_twamp_session_reflector(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, hw_lookup, mode, nexthop=None, port_oid=test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)        
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            warmboot(self.client)
                    
            sys_logging(" step 3 check the receive and send packet ")   
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = router_mac
            macsa = dmac1
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port

            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=254,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('fe')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = dmac2
            macsa = router_mac
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt2 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=253,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)

                          
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(pkt2, [2]) 
            
        finally:

            sys_logging("clear configuration")        
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)        
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
           


           
class scenario_03_UNI_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 100
        pw_label = 200

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")
               
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        dst_ip0 = '1.2.3.4'   
        dmac0 = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        dst_ip1 = '40.40.40.40'   
        dmac1 = '00:00:00:00:00:02'         
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        tunnel_ip_da = '10.10.10.10'
        tunnel_mac_da = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da)                
        lsp_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, tunnel_ip_da, rif_id2, lsp_label_list)
        
        pw_next_hop = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, pw_label_list, next_level_nhop_oid=lsp_next_hop)

        dst_ip_subnet1 = '2.2.2.0'
        ip_mask1 = '255.255.255.0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        lsp_label_r = 300
        pw_label_r = 400
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_inseg_entry(self.client, lsp_label_r, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, pw_label_r, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        dst_ip_subnet2 = '1.2.3.0'
        ip_mask2 = '255.255.255.0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
                
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            sys_logging(" step 3 check the send packet ")
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL
            
            macda = tunnel_mac_da
            macsa = router_mac
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port
            
            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=254,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':254,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1) 
                                    
            self.ctc_show_packet_twamp(2,str(pkt2))                    

            warmboot(self.client)
        
            sys_logging("### step 4 check receive packet ###") 
            
            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('fe')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = router_mac
            macsa = dmac1
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt3 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=253,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label_r,'tc':0,'ttl':253,'s':0}, {'label':pw_label_r,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 

            self.ctc_send_packet( 1, str(pkt4))
            # sdk cli check show npm session 0 stats flex                                     

            counter_ids = [SAI_TWAMP_SESSION_STATS_RX_PACKETS, SAI_TWAMP_SESSION_STATS_RX_BYTE, SAI_TWAMP_SESSION_STATS_TX_PACKETS, SAI_TWAMP_SESSION_STATS_TX_BYTE, SAI_TWAMP_SESSION_STATS_DROP_PACKETS,SAI_TWAMP_SESSION_STATS_MAX_LATENCY,SAI_TWAMP_SESSION_STATS_MIN_LATENCY,SAI_TWAMP_SESSION_STATS_AVG_LATENCY,SAI_TWAMP_SESSION_STATS_MAX_JITTER,SAI_TWAMP_SESSION_STATS_MIN_JITTER,SAI_TWAMP_SESSION_STATS_AVG_JITTER,SAI_TWAMP_SESSION_STATS_FIRST_TS,SAI_TWAMP_SESSION_STATS_LAST_TS,SAI_TWAMP_SESSION_STATS_DURATION_TS]
            
            list1 = self.client.sai_thrift_get_twamp_session_stats(twamp_session_oid, counter_ids, 14) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            sys_logging("###list1[8]= %d###" %list1[8])
            sys_logging("###list1[9]= %d###" %list1[9])
            sys_logging("###list1[10]= %d###" %list1[10])
            sys_logging("###list1[11]= %d###" %list1[11])
            sys_logging("###list1[12]= %d###" %list1[12])
            sys_logging("###list1[13]= %d###" %list1[13])
            
            assert (list1[0] == 1)
            assert (list1[1] == 256+8) 
            assert (list1[2] == 1)
            assert (list1[3] == 256)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            assert (list1[8] == 0)
            assert (list1[9] == 0)
            assert (list1[10] == 0)
            assert (list1[11] == 795761)
            assert (list1[12] == 795761)
            assert (list1[13] == 0)
            
        finally:
        
            sys_logging("clear configuration") 
            
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)  
            
            label1 = sai_thrift_inseg_entry_t(lsp_label_r) 
            label2 = sai_thrift_inseg_entry_t(pw_label_r) 
            self.client.sai_thrift_remove_inseg_entry(label1)
            self.client.sai_thrift_remove_inseg_entry(label2)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
            
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(pw_next_hop)              
            self.client.sai_thrift_remove_next_hop(lsp_next_hop)            
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da) 
            
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3) 
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id) 
            
            
                       
class scenario_04_UNI_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]     
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 300
        pw_label = 400

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")
               
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        dst_ip0 = '2.2.2.2'   
        dmac0 = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        dst_ip1 = '30.30.30.30'   
        dmac1 = '00:00:00:00:00:02'         
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        tunnel_ip_da = '20.20.20.20'
        tunnel_mac_da = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da)                
        lsp_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, tunnel_ip_da, rif_id2, lsp_label_list)
        
        pw_next_hop = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, pw_label_list, next_level_nhop_oid=lsp_next_hop)
        
        dst_ip_subnet1 = '1.2.3.0'
        ip_mask1 = '255.255.255.0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        lsp_label_r = 100
        pw_label_r = 200
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_inseg_entry(self.client, lsp_label_r, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, pw_label_r, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        dst_ip_subnet2 = '2.2.2.0'
        ip_mask2 = '255.255.255.0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
        
        warmboot(self.client)
        
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_reflector(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, hw_lookup, mode, nexthop=None, port_oid=test_port_oid)
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)        
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            warmboot(self.client)
        
            sys_logging(" step 3 check the receive and send packet ")  
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL
            
            macda = router_mac
            macsa = dmac1
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port
            
            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=254,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label_r,'tc':0,'ttl':32,'s':0}, {'label':pw_label_r,'tc':0,'ttl':254,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1)                                    

            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('fe')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = tunnel_mac_da
            macsa = router_mac
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt3 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=253,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 
                                    
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt4, [2])      

        finally:
        
            sys_logging("clear configuration") 
            
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)  

            label1 = sai_thrift_inseg_entry_t(lsp_label_r) 
            label2 = sai_thrift_inseg_entry_t(pw_label_r) 
            self.client.sai_thrift_remove_inseg_entry(label1)
            self.client.sai_thrift_remove_inseg_entry(label2)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
            
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(pw_next_hop)              
            self.client.sai_thrift_remove_next_hop(lsp_next_hop)            

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da) 
            
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3) 
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id)            
            
            

            
            
class scenario_05_NNI_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_NNI
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 100
        pw_label = 200

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")
               
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        dst_ip0 = '1.2.3.4'   
        dmac0 = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        dst_ip1 = '40.40.40.40'   
        dmac1 = '00:00:00:00:00:02'         
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        tunnel_ip_da = '10.10.10.10'
        tunnel_mac_da = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da)                
        lsp_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, tunnel_ip_da, rif_id2, lsp_label_list)
        
        pw_next_hop = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, pw_label_list, next_level_nhop_oid=lsp_next_hop)

        dst_ip_subnet1 = '2.2.2.0'
        ip_mask1 = '255.255.255.0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        lsp_label_r = 300
        pw_label_r = 400
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_inseg_entry(self.client, lsp_label_r, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, pw_label_r, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        dst_ip_subnet2 = '1.2.3.0'
        ip_mask2 = '255.255.255.0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
                
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            sys_logging(" step 3 check the send packet ")
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL
            
            macda = tunnel_mac_da
            macsa = router_mac
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port
            
            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=254,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':254,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1) 
                                    
            self.ctc_show_packet_twamp(2,str(pkt2))                    

            warmboot(self.client)
        
            sys_logging("### step 4 check receive packet ###") 
            
            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('fe')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = router_mac
            macsa = dmac1
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt3 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=253,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label_r,'tc':0,'ttl':253,'s':0}, {'label':pw_label_r,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 

            self.ctc_send_packet( 1, str(pkt4))
            # sdk cli check show npm session 0 stats flex 
            
            counter_ids = [SAI_TWAMP_SESSION_STATS_RX_PACKETS, SAI_TWAMP_SESSION_STATS_RX_BYTE, SAI_TWAMP_SESSION_STATS_TX_PACKETS, SAI_TWAMP_SESSION_STATS_TX_BYTE, SAI_TWAMP_SESSION_STATS_DROP_PACKETS,SAI_TWAMP_SESSION_STATS_MAX_LATENCY,SAI_TWAMP_SESSION_STATS_MIN_LATENCY,SAI_TWAMP_SESSION_STATS_AVG_LATENCY,SAI_TWAMP_SESSION_STATS_MAX_JITTER,SAI_TWAMP_SESSION_STATS_MIN_JITTER,SAI_TWAMP_SESSION_STATS_AVG_JITTER,SAI_TWAMP_SESSION_STATS_FIRST_TS,SAI_TWAMP_SESSION_STATS_LAST_TS,SAI_TWAMP_SESSION_STATS_DURATION_TS]
            
            list1 = self.client.sai_thrift_get_twamp_session_stats(twamp_session_oid, counter_ids, 14) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            sys_logging("###list1[8]= %d###" %list1[8])
            sys_logging("###list1[9]= %d###" %list1[9])
            sys_logging("###list1[10]= %d###" %list1[10])
            sys_logging("###list1[11]= %d###" %list1[11])
            sys_logging("###list1[12]= %d###" %list1[12])
            sys_logging("###list1[13]= %d###" %list1[13])
            
            assert (list1[0] == 1)
            assert (list1[1] == 256+8) 
            assert (list1[2] == 1)
            assert (list1[3] == 256)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            assert (list1[8] == 0)
            assert (list1[9] == 0)
            assert (list1[10] == 0)
            assert (list1[11] == 795761)
            assert (list1[12] == 795761)
            assert (list1[13] == 0)

                                    
        finally:
        
            sys_logging("clear configuration") 
            
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)  
            
            label1 = sai_thrift_inseg_entry_t(lsp_label_r) 
            label2 = sai_thrift_inseg_entry_t(pw_label_r) 
            self.client.sai_thrift_remove_inseg_entry(label1)
            self.client.sai_thrift_remove_inseg_entry(label2)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
            
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(pw_next_hop)              
            self.client.sai_thrift_remove_next_hop(lsp_next_hop)            
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da) 
            
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3) 
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id)  






class scenario_06_NNI_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]      
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '2.2.2.2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_NNI
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 300
        pw_label = 400

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")
               
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        dst_ip0 = '2.2.2.2'   
        dmac0 = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        dst_ip1 = '30.30.30.30'   
        dmac1 = '00:00:00:00:00:02'         
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        tunnel_ip_da = '20.20.20.20'
        tunnel_mac_da = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da)                
        lsp_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, tunnel_ip_da, rif_id2, lsp_label_list)
        
        pw_next_hop = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, pw_label_list, next_level_nhop_oid=lsp_next_hop)
        
        dst_ip_subnet1 = '1.2.3.0'
        ip_mask1 = '255.255.255.0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        lsp_label_r = 100
        pw_label_r = 200
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_inseg_entry(self.client, lsp_label_r, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, pw_label_r, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        dst_ip_subnet2 = '2.2.2.0'
        ip_mask2 = '255.255.255.0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
        
        warmboot(self.client)
        
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_reflector(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, hw_lookup, mode, nexthop=None, port_oid=None )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)        
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            warmboot(self.client)
        
            sys_logging(" step 3 check the receive and send packet ")  
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL
            
            macda = router_mac
            macsa = dmac1
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port
            
            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=254,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label_r,'tc':0,'ttl':254,'s':0}, {'label':pw_label_r,'tc':0,'ttl':254,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1)                                    

            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('fe')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = tunnel_mac_da
            macsa = router_mac
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt3 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ip_src=ipsa,
                          ip_dst=ipda,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=253,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 
                                    
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt4, [2])      

        finally:
        
            sys_logging("clear configuration") 
            
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)  

            label1 = sai_thrift_inseg_entry_t(lsp_label_r) 
            label2 = sai_thrift_inseg_entry_t(pw_label_r) 
            self.client.sai_thrift_remove_inseg_entry(label1)
            self.client.sai_thrift_remove_inseg_entry(label2)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
            
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(pw_next_hop)              
            self.client.sai_thrift_remove_next_hop(lsp_next_hop)            

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da) 
            
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3) 
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id) 




            
class scenario_08_ipv6_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
              
        src_ip = '2001:1:2:3:4:5:6:7' 
        dst_ip = '2001:2:2:2:2:2:2:2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
            
        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '2001:1:2:3:4:5:6:7'   
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '2001:3:3:3:3:3:3:3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '2001:2:2:2:2:2:2:2'   
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '2001:2:2:2:2:2:2:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        
        
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)
            #pdb.set_trace()

            sys_logging(" step 3 check the send packet ")
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = dmac2
            macsa = router_mac
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port

            pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=254,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            self.ctc_show_packet_twamp(2,str(pkt1))            
            #self.ctc_show_packet_twamp(2,str(pkt1),60,2) 

            warmboot(self.client)
        
            sys_logging("### step 4 check receive packet ###")   
            
            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('fe')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = router_mac
            macsa = dmac1
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port
                          
            pkt2 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=253,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            self.ctc_send_packet( 1, str(pkt2))
            # sdk cli check show npm session 0 stats flex 

            counter_ids = [SAI_TWAMP_SESSION_STATS_RX_PACKETS, SAI_TWAMP_SESSION_STATS_RX_BYTE, SAI_TWAMP_SESSION_STATS_TX_PACKETS, SAI_TWAMP_SESSION_STATS_TX_BYTE, SAI_TWAMP_SESSION_STATS_DROP_PACKETS,SAI_TWAMP_SESSION_STATS_MAX_LATENCY,SAI_TWAMP_SESSION_STATS_MIN_LATENCY,SAI_TWAMP_SESSION_STATS_AVG_LATENCY,SAI_TWAMP_SESSION_STATS_MAX_JITTER,SAI_TWAMP_SESSION_STATS_MIN_JITTER,SAI_TWAMP_SESSION_STATS_AVG_JITTER,SAI_TWAMP_SESSION_STATS_FIRST_TS,SAI_TWAMP_SESSION_STATS_LAST_TS,SAI_TWAMP_SESSION_STATS_DURATION_TS]
            
            list1 = self.client.sai_thrift_get_twamp_session_stats(twamp_session_oid, counter_ids, 14) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            sys_logging("###list1[8]= %d###" %list1[8])
            sys_logging("###list1[9]= %d###" %list1[9])
            sys_logging("###list1[10]= %d###" %list1[10])
            sys_logging("###list1[11]= %d###" %list1[11])
            sys_logging("###list1[12]= %d###" %list1[12])
            sys_logging("###list1[13]= %d###" %list1[13])
            
            assert (list1[0] == 1)
            assert (list1[1] == 256) 
            assert (list1[2] == 1)
            assert (list1[3] == 256)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            assert (list1[8] == 0)
            assert (list1[9] == 0)
            assert (list1[10] == 0)
            assert (list1[11] == 795761)
            assert (list1[12] == 795761)
            assert (list1[13] == 0)

            
        finally:
        
            sys_logging("clear configuration")
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)        
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
            
            
            
            


class scenario_09_ipv6_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]       
        udp_src_port = 1111        
        udp_dst_port = 2222
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
              
        src_ip = '2001:1:2:3:4:5:6:7' 
        dst_ip = '2001:2:2:2:2:2:2:2'  
            
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)        
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_IP
        hw_lookup = 1
        pkt_len = 256
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        sys_logging(" step 1 basic data environment")
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id0)        
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id1)

        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        sys_logging("create output route interface = %d" %rif_id2)
        
        dst_ip0 = '2001:2:2:2:2:2:2:2'    
        dmac0 = '00:11:22:33:44:01'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        
        dst_ip1 = '2001:3:3:3:3:3:3:3'   
        dmac1 = '00:11:22:33:44:02'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)

        dst_ip2 = '2001:1:2:3:4:5:6:7'  
        dmac2 = '00:11:22:33:44:03'        
        sys_logging("create neighbor")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)
        
        sys_logging("create nhop to route interface")
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        sys_logging("create nhop to route interface")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)

        sys_logging("create nhop to route interface")
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dst_ip2, rif_id2)
        
        dst_ip_subnet = '2001:1:2:3:4:5:6:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'        
        sys_logging("create route")
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop2)        

        try:

            sys_logging(" step 2 create twamp session on reflector ") 
            
            twamp_session_oid = sai_thrift_create_twamp_session_reflector(self.client , receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, hw_lookup, mode, nexthop=None, port_oid=test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)        
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            warmboot(self.client)
                    
            sys_logging(" step 3 check the receive and send packet ")   
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = router_mac
            macsa = dmac1
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port

            pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=254,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('fe')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = dmac2
            macsa = router_mac
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt2 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=253,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)

                          
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(pkt2, [2]) 
            
        finally:

            sys_logging("clear configuration")        
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)        
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, dst_ip2, dmac2)  
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
           

class scenario_10_ipv6_UNI_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
              
        src_ip = '2001:1:2:3:4:5:6:7' 
        dst_ip = '2001:2:2:2:2:2:2:2'         
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 100
        pw_label = 200

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")
               
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        dst_ip0 = '2001:1:2:3:4:5:6:7'   
        dmac0 = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        dst_ip1 = '2001:40:3:3:3:3:3:3'   
        dmac1 = '00:00:00:00:00:02'         
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        tunnel_ip_da = '2001:10:3:3:3:3:3:3'
        tunnel_mac_da = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da)                
        lsp_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, tunnel_ip_da, rif_id2, lsp_label_list)
        
        pw_next_hop = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, pw_label_list, next_level_nhop_oid=lsp_next_hop)

        dst_ip_subnet1 = '2001:2:2:2:2:2:2:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        lsp_label_r = 300
        pw_label_r = 400
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_inseg_entry(self.client, lsp_label_r, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, pw_label_r, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        dst_ip_subnet2 = '2001:1:2:3:4:5:6:0'
        ip_mask2 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'          
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
                
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration, test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            sys_logging(" step 3 check the send packet ")
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL
            
            macda = tunnel_mac_da
            macsa = router_mac
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port
            
            pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=254,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':254,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1) 
                                    
            self.ctc_show_packet_twamp(2,str(pkt2))                    

            warmboot(self.client)
        
            sys_logging("### step 4 check receive packet ###") 
            
            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('fe')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = router_mac
            macsa = dmac1
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt3 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=253,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label_r,'tc':0,'ttl':253,'s':0}, {'label':pw_label_r,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 

            self.ctc_send_packet( 1, str(pkt4))
            # sdk cli check show npm session 0 stats flex   
            
            counter_ids = [SAI_TWAMP_SESSION_STATS_RX_PACKETS, SAI_TWAMP_SESSION_STATS_RX_BYTE, SAI_TWAMP_SESSION_STATS_TX_PACKETS, SAI_TWAMP_SESSION_STATS_TX_BYTE, SAI_TWAMP_SESSION_STATS_DROP_PACKETS,SAI_TWAMP_SESSION_STATS_MAX_LATENCY,SAI_TWAMP_SESSION_STATS_MIN_LATENCY,SAI_TWAMP_SESSION_STATS_AVG_LATENCY,SAI_TWAMP_SESSION_STATS_MAX_JITTER,SAI_TWAMP_SESSION_STATS_MIN_JITTER,SAI_TWAMP_SESSION_STATS_AVG_JITTER,SAI_TWAMP_SESSION_STATS_FIRST_TS,SAI_TWAMP_SESSION_STATS_LAST_TS,SAI_TWAMP_SESSION_STATS_DURATION_TS]
            
            list1 = self.client.sai_thrift_get_twamp_session_stats(twamp_session_oid, counter_ids, 14) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            sys_logging("###list1[8]= %d###" %list1[8])
            sys_logging("###list1[9]= %d###" %list1[9])
            sys_logging("###list1[10]= %d###" %list1[10])
            sys_logging("###list1[11]= %d###" %list1[11])
            sys_logging("###list1[12]= %d###" %list1[12])
            sys_logging("###list1[13]= %d###" %list1[13])
            
            assert (list1[0] == 1)
            assert (list1[1] == 256+8) 
            assert (list1[2] == 1)
            assert (list1[3] == 256)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            assert (list1[8] == 0)
            assert (list1[9] == 0)
            assert (list1[10] == 0)
            assert (list1[11] == 795761)
            assert (list1[12] == 795761)
            assert (list1[13] == 0)

                                    
        finally:
        
            sys_logging("clear configuration") 
            
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)  
            
            label1 = sai_thrift_inseg_entry_t(lsp_label_r) 
            label2 = sai_thrift_inseg_entry_t(pw_label_r) 
            self.client.sai_thrift_remove_inseg_entry(label1)
            self.client.sai_thrift_remove_inseg_entry(label2)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
            
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(pw_next_hop)              
            self.client.sai_thrift_remove_next_hop(lsp_next_hop)            
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da) 
            
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3) 
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id) 



                       
class scenario_11_ipv6_UNI_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]       
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
              
        src_ip = '2001:1:2:3:4:5:6:7' 
        dst_ip = '2001:2:2:2:2:2:2:2'       
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_UNI
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 300
        pw_label = 400

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")
               
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        dst_ip0 = '2001:2:2:2:2:2:2:2'    
        dmac0 = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        dst_ip1 = '2001:30:3:3:3:3:3:3'   
        dmac1 = '00:00:00:00:00:02'         
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        tunnel_ip_da = '2001:20:3:3:3:3:3:3'
        tunnel_mac_da = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da)                
        lsp_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, tunnel_ip_da, rif_id2, lsp_label_list)
        
        pw_next_hop = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, pw_label_list, next_level_nhop_oid=lsp_next_hop)
        
        dst_ip_subnet1 = '2001:1:2:3:4:5:6:0' 
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'        
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        lsp_label_r = 100
        pw_label_r = 200
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_inseg_entry(self.client, lsp_label_r, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, pw_label_r, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        dst_ip_subnet2 = '2001:2:2:2:2:2:2:0'
        ip_mask2 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
        
        warmboot(self.client)
        
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_reflector(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, hw_lookup, mode, nexthop=None, port_oid=test_port_oid )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)        
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            warmboot(self.client)
        
            sys_logging(" step 3 check the receive and send packet ")  
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL
            
            macda = router_mac
            macsa = dmac1
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port
            
            pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=254,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label_r,'tc':0,'ttl':32,'s':0}, {'label':pw_label_r,'tc':0,'ttl':254,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1)                                    

            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('fe')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = tunnel_mac_da
            macsa = router_mac
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt3 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=253,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 
                                    
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt4, [2])      

        finally:
        
            sys_logging("clear configuration") 
            
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)  

            label1 = sai_thrift_inseg_entry_t(lsp_label_r) 
            label2 = sai_thrift_inseg_entry_t(pw_label_r) 
            self.client.sai_thrift_remove_inseg_entry(label1)
            self.client.sai_thrift_remove_inseg_entry(label2)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
            
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(pw_next_hop)              
            self.client.sai_thrift_remove_next_hop(lsp_next_hop)            

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da) 
            
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3) 
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id)            
            


            
class scenario_12_ipv6_NNI_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]
        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
              
        src_ip = '2001:1:2:3:4:5:6:7' 
        dst_ip = '2001:2:2:2:2:2:2:2'         
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_NNI
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        tx_mode = SAI_TWAMP_PKT_TX_MODE_PACKET_NUM
        tx_period = 0
        tx_rate = 100
        tx_pkt_cnt = 1
        tx_pkt_duration = 0
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 100
        pw_label = 200

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")
               
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        dst_ip0 = '2001:1:2:3:4:5:6:7'  
        dmac0 = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        dst_ip1 = '2001:40:3:3:3:3:3:3'  
        dmac1 = '00:00:00:00:00:02'         
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        tunnel_ip_da = '2001:10:3:3:3:3:3:3'
        tunnel_mac_da = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da)                
        lsp_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, tunnel_ip_da, rif_id2, lsp_label_list)
        
        pw_next_hop = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, pw_label_list, next_level_nhop_oid=lsp_next_hop)

        dst_ip_subnet1 = '2001:2:2:2:2:2:2:2'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'          
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        lsp_label_r = 300
        pw_label_r = 400
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_inseg_entry(self.client, lsp_label_r, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, pw_label_r, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        dst_ip_subnet2 = '2001:1:2:3:4:5:6:0'
        ip_mask2 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'          
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
                
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_sender(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, enable_transmit, hw_lookup, pkt_len, mode, tx_mode, tx_rate,  tx_period, tx_pkt_cnt, tx_pkt_duration )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)          
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            sys_logging(" step 3 check the send packet ")
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL
            
            macda = tunnel_mac_da
            macsa = router_mac
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port
            
            pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=254,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':254,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1) 
                                    
            self.ctc_show_packet_twamp(2,str(pkt2))                    

            warmboot(self.client)
        
            sys_logging("### step 4 check receive packet ###") 
            
            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('fe')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = router_mac
            macsa = dmac1
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt3 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=253,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label_r,'tc':0,'ttl':253,'s':0}, {'label':pw_label_r,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 

            self.ctc_send_packet( 1, str(pkt4))
            # sdk cli check show npm session 0 stats flex                                     

            counter_ids = [SAI_TWAMP_SESSION_STATS_RX_PACKETS, SAI_TWAMP_SESSION_STATS_RX_BYTE, SAI_TWAMP_SESSION_STATS_TX_PACKETS, SAI_TWAMP_SESSION_STATS_TX_BYTE, SAI_TWAMP_SESSION_STATS_DROP_PACKETS,SAI_TWAMP_SESSION_STATS_MAX_LATENCY,SAI_TWAMP_SESSION_STATS_MIN_LATENCY,SAI_TWAMP_SESSION_STATS_AVG_LATENCY,SAI_TWAMP_SESSION_STATS_MAX_JITTER,SAI_TWAMP_SESSION_STATS_MIN_JITTER,SAI_TWAMP_SESSION_STATS_AVG_JITTER,SAI_TWAMP_SESSION_STATS_FIRST_TS,SAI_TWAMP_SESSION_STATS_LAST_TS,SAI_TWAMP_SESSION_STATS_DURATION_TS]
            
            list1 = self.client.sai_thrift_get_twamp_session_stats(twamp_session_oid, counter_ids, 14) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            sys_logging("###list1[8]= %d###" %list1[8])
            sys_logging("###list1[9]= %d###" %list1[9])
            sys_logging("###list1[10]= %d###" %list1[10])
            sys_logging("###list1[11]= %d###" %list1[11])
            sys_logging("###list1[12]= %d###" %list1[12])
            sys_logging("###list1[13]= %d###" %list1[13])
            
            assert (list1[0] == 1)
            assert (list1[1] == 256+8) 
            assert (list1[2] == 1)
            assert (list1[3] == 256)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            assert (list1[8] == 0)
            assert (list1[9] == 0)
            assert (list1[10] == 0)
            assert (list1[11] == 795761)
            assert (list1[12] == 795761)
            assert (list1[13] == 0) 
            
        finally:
        
            sys_logging("clear configuration") 
            
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)  
            
            label1 = sai_thrift_inseg_entry_t(lsp_label_r) 
            label2 = sai_thrift_inseg_entry_t(pw_label_r) 
            self.client.sai_thrift_remove_inseg_entry(label1)
            self.client.sai_thrift_remove_inseg_entry(label2)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
            
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(pw_next_hop)              
            self.client.sai_thrift_remove_next_hop(lsp_next_hop)            
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da) 
            
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3) 
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id)  






class scenario_13_ipv6_NNI_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]     
        receive_port_oid = [port_list[0],port_list[1],port_list[2]]
        send_port_oid = port_list[2]        
        udp_src_port = 1111        
        udp_dst_port = 2222
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
              
        src_ip = '2001:1:2:3:4:5:6:7' 
        dst_ip = '2001:2:2:2:2:2:2:2'        
        tc = 7
        vr_id = sai_thrift_get_default_router_id(self.client)               
        vrf_oid = vr_id
        encap_type = SAI_TWAMP_ENCAPSULATION_TYPE_L3_MPLS_VPN_NNI
        enable_transmit = 1
        hw_lookup = 1
        pkt_len = 256
        mode = SAI_TWAMP_MODE_FULL
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 300
        pw_label = 400

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")
               
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        dst_ip0 = '2001:2:2:2:2:2:2:2'    
        dmac0 = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        dst_ip1 = '2001:30:3:3:3:3:3:3'   
        dmac1 = '00:00:00:00:00:02'         
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        tunnel_ip_da = '2001:20:3:3:3:3:3:3'
        tunnel_mac_da = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da)                
        lsp_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, tunnel_ip_da, rif_id2, lsp_label_list)
        
        pw_next_hop = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, pw_label_list, next_level_nhop_oid=lsp_next_hop)
        
        dst_ip_subnet1 = '2001:1:2:3:4:5:6:0' 
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        lsp_label_r = 100
        pw_label_r = 200
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_inseg_entry(self.client, lsp_label_r, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, pw_label_r, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        dst_ip_subnet2 = '2001:2:2:2:2:2:2:0'
        ip_mask2 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
        
        warmboot(self.client)
        
        try:

            sys_logging(" step 2 create twamp session on sender ")
            
            twamp_session_oid = sai_thrift_create_twamp_session_reflector(self.client, receive_port_oid, udp_src_port, udp_dst_port, addr_family, src_ip, dst_ip, tc, vrf_oid, encap_type, hw_lookup, mode, nexthop=None, port_oid=None )
            sys_logging("###twamp_session_oid = %d###" %twamp_session_oid)        
            assert (twamp_session_oid != SAI_NULL_OBJECT_ID)

            warmboot(self.client)
        
            sys_logging(" step 3 check the receive and send packet ")  
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0000')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000000000')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('00')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL
            
            macda = router_mac
            macsa = dmac1
            ipsa = src_ip
            ipda = dst_ip
            src_port = udp_src_port
            dst_port = udp_dst_port
            
            pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=254,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label_r,'tc':0,'ttl':32,'s':0}, {'label':pw_label_r,'tc':0,'ttl':254,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1)                                    

            Sequence_Number = hexstr_to_ascii('00000001')
            Timestamp = hexstr_to_ascii('0000000000445678')
            Error_Estimate = hexstr_to_ascii('0001')
            MBZ1 = hexstr_to_ascii('0000')
            Receive_Timestamp = hexstr_to_ascii('0000000000345678')
            Sender_Sequence_Number = hexstr_to_ascii('00000000')
            Sender_Timestamp = hexstr_to_ascii('0000000000445678')
            Sender_Error_Estimate = hexstr_to_ascii('0000')
            MBZ2 = hexstr_to_ascii('0000')
            Sender_TTL = hexstr_to_ascii('fe')
            Twamp_test_pkt = Sequence_Number + Timestamp + Error_Estimate + MBZ1 + Receive_Timestamp + Sender_Sequence_Number + Sender_Timestamp + Sender_Error_Estimate + MBZ2 + Sender_TTL

            macda = tunnel_mac_da
            macsa = router_mac
            ipsa = dst_ip
            ipda = src_ip
            src_port = udp_dst_port
            dst_port = udp_src_port

            pkt3 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=macda,
                          eth_src=macsa,
                          dl_vlan_enable=False,
                          ipv6_src=ipsa,
                          ipv6_dst=ipda,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=253,
                          ipv6_fl=0,
                          udp_sport=src_port,
                          udp_dport=dst_port,
                          with_udp_chksum=True,
                          udp_payload=Twamp_test_pkt,
                          pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=macda,
                                    eth_src=macsa,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 
                                    
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt4, [2])  

        finally:
        
            sys_logging("clear configuration") 
            
            self.client.sai_thrift_remove_twamp_session(twamp_session_oid)  

            label1 = sai_thrift_inseg_entry_t(lsp_label_r) 
            label2 = sai_thrift_inseg_entry_t(pw_label_r) 
            self.client.sai_thrift_remove_inseg_entry(label1)
            self.client.sai_thrift_remove_inseg_entry(label2)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)
            sai_thrift_remove_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
            
            self.client.sai_thrift_remove_next_hop(nhop0)            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(pw_next_hop)              
            self.client.sai_thrift_remove_next_hop(lsp_next_hop)            

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0) 
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)             
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da) 
            
            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1) 
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3) 
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_tunnel(tunnel_id) 

