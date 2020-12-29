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
Thrift SAI interface NPM tests
"""

import socket
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask
import pdb

@group('npm')



class func_01_create_npm_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        encap_type = SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port_list[0])
        test_port_oid = bport_oid
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        src_mac = '00:00:00:00:00:01'
        dst_mac = '00:00:00:00:00:02'
        outer_vlanid = 100
        inner_vlan_id = 200
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '5.6.7.8' 
        udp_src_port = 1234 
        udp_dst_port = 5678
        ttl = 100
        tc = 0 
        enable_transmit = 1 
        vrf_oid = 0
        hw_lookup = 1
        pkt_len = 100
        tx_rate = 100
        tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
        tx_period = None
        tx_pkt_cnt = 1
        tx_pkt_duration =None

             
        sys_logging(" step 1 basic data environment")

        vlan_id = outer_vlanid
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[0], SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
 
        
        try:

            sys_logging(" step 2 create npm session on sender ")
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=outer_vlanid,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            #pdb.set_trace()
            #self.ctc_show_packet_twamp(0,str(pkt)) 
            # check packet with not care udpchecksum
            #self.ctc_show_packet_twamp(1,str(pkt),48,2) 
            self.ctc_show_packet_twamp(1,str(pkt)) 
            
            
        finally:
        
            sys_logging("step 3 clear configuration")
            #pdb.set_trace()
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)
            assert (status == SAI_STATUS_SUCCESS)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  




class func_02_create_same_npm_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        encap_type = SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port_list[0])
        test_port_oid = bport_oid
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        src_mac = '00:00:00:00:00:01'
        dst_mac = '00:00:00:00:00:02'
        outer_vlanid = 100
        inner_vlan_id = 200
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '5.6.7.8' 
        udp_src_port = 1234 
        udp_dst_port = 5678
        ttl = 100
        tc = 0 
        enable_transmit = 1 
        vrf_oid = 0
        hw_lookup = 1
        pkt_len = 100
        tx_rate = 100
        tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
        tx_period = None
        tx_pkt_cnt = 1
        tx_pkt_duration =None

             
        sys_logging(" step 1 basic data environment")

        vlan_id = outer_vlanid
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[0], SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
 
        
        try:

            sys_logging(" step 2 create npm session on sender ")
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)

            npm_session_oid_2 = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid_2)
            
            assert (npm_session_oid_2 != SAI_NULL_OBJECT_ID)

            assert (npm_session_oid != npm_session_oid_2)           
            
        finally:
        
            sys_logging("step 3 clear configuration")
            #pdb.set_trace()
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid_2) 
            sys_logging("###remove session status  = %d###" %status)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  





class func_04_create_max_npm_session_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        encap_type = SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port_list[0])
        test_port_oid = bport_oid
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        src_mac = '00:00:00:00:00:01'
        dst_mac = '00:00:00:00:00:02'
        outer_vlanid = 100
        inner_vlan_id = 200
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '5.6.7.8' 
        udp_src_port = 1234 
        udp_dst_port = 5678
        ttl = 100
        tc = 0 
        enable_transmit = 1 
        vrf_oid = 0
        hw_lookup = 1
        pkt_len = 100
        tx_rate = 100
        tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
        tx_period = None
        tx_pkt_cnt = 1
        tx_pkt_duration =None

             
        sys_logging(" step 1 basic data environment")

        vlan_id = outer_vlanid
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[0], SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
 
        
        try:

            sys_logging(" step 2 create npm session on sender ")
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)

            npm_session_oid_2 = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid_2)
            
            assert (npm_session_oid_2 != SAI_NULL_OBJECT_ID)

            npm_session_oid_3 = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid_3)
            
            assert (npm_session_oid_3 != SAI_NULL_OBJECT_ID)

            npm_session_oid_4 = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid_4)
            
            assert (npm_session_oid_4 != SAI_NULL_OBJECT_ID)            

            npm_session_oid_5 = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid_5)
            
            assert (npm_session_oid_5 == SAI_NULL_OBJECT_ID) 
         
            
        finally:
        
            sys_logging("step 3 clear configuration")
            #pdb.set_trace()
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid_2) 
            sys_logging("###remove session status  = %d###" %status)
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid_3) 
            sys_logging("###remove session status  = %d###" %status)
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid_4) 
            sys_logging("###remove session status  = %d###" %status)            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  




class func_06_remove_not_exist_npm_session_fn (sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        encap_type = SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port_list[0])
        test_port_oid = bport_oid
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        src_mac = '00:00:00:00:00:01'
        dst_mac = '00:00:00:00:00:02'
        outer_vlanid = 100
        inner_vlan_id = 200
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '5.6.7.8' 
        udp_src_port = 1234 
        udp_dst_port = 5678
        ttl = 100
        tc = 0 
        enable_transmit = 1 
        vrf_oid = 0
        hw_lookup = 1
        pkt_len = 100
        tx_rate = 100
        tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
        tx_period = None
        tx_pkt_cnt = 1
        tx_pkt_duration =None

             
        sys_logging(" step 1 basic data environment")

        vlan_id = outer_vlanid
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[0], SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
 
        
        try:

            sys_logging(" step 2 create npm session on sender ")
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=outer_vlanid,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            #pdb.set_trace()
            #self.ctc_show_packet_twamp(0,str(pkt)) 
            # check packet with not care udpchecksum
            self.ctc_show_packet_twamp(1,str(pkt)) 
            
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
        
            sys_logging("step 3 clear configuration")
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  




class func_07_set_and_get_npm_session_attr_fn (sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        encap_type = SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port_list[0])
        test_port_oid = bport_oid
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        src_mac = '00:00:00:00:00:01'
        dst_mac = '00:00:00:00:00:02'
        outer_vlanid = 100
        inner_vlan_id = 200
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '5.6.7.8' 
        udp_src_port = 1234 
        udp_dst_port = 5678
        ttl = 100
        tc = 0 
        enable_transmit = 1 
        vrf_oid = 0
        hw_lookup = 1
        pkt_len = 100
        tx_rate = 100
        tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
        tx_period = None
        tx_pkt_cnt = 1
        tx_pkt_duration =None

             
        sys_logging(" step 1 basic data environment")

        vlan_id = outer_vlanid
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[0], SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
 
        
        try:

            sys_logging(" step 2 create npm session on sender ")
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=outer_vlanid,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            #pdb.set_trace()
            #self.ctc_show_packet_twamp(0,str(pkt)) 
            # check packet with not care udpchecksum
            self.ctc_show_packet_twamp(1,str(pkt)) 


            sys_logging(" step 3 get npm session attr ")
            
            attrs = self.client.sai_thrift_get_npm_attribute(npm_session_oid)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
        
            for a in attrs.attr_list:
            
                if a.id == SAI_NPM_SESSION_ATTR_SESSION_ROLE:
                    sys_logging("get SAI_NPM_SESSION_ATTR_SESSION_ROLE = %d" %a.value.s32)
                    assert (a.value.s32 == SAI_NPM_SESSION_ROLE_SENDER)

                if a.id == SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE:
                    sys_logging("get SAI_NPM_SESSION_ATTR_NPM_ENCAPSULATION_TYPE = %d" %a.value.s32)
                    assert (a.value.s32 == encap_type)            

                if a.id == SAI_NPM_SESSION_ATTR_NPM_TEST_PORT:
                    sys_logging("get SAI_NPM_SESSION_ATTR_NPM_TEST_PORT = %d" %a.value.oid)
                    assert (a.value.oid == test_port_oid)

                if a.id == SAI_NPM_SESSION_ATTR_NPM_RECEIVE_PORT:
                    sys_logging("get SAI_NPM_SESSION_ATTR_NPM_RECEIVE_PORT count= %d" %a.value.objlist.count)
                    assert (a.value.objlist.count == len(receive_port_oid))   
                    for b in a.value.objlist.object_id_list:
                        sys_logging("###SAI_NPM_SESSION_ATTR_NPM_RECEIVE_PORT = %d ###" %b)
                        assert (b in receive_port_oid)  

                if a.id == SAI_NPM_SESSION_ATTR_SRC_MAC:
                    sys_logging("get SAI_NPM_SESSION_ATTR_SRC_MAC = %s" %a.value.mac)
                    assert (a.value.mac == src_mac)

                if a.id == SAI_NPM_SESSION_ATTR_DST_MAC:
                    sys_logging("get SAI_NPM_SESSION_ATTR_DST_MAC = %s" %a.value.mac)
                    assert (a.value.mac == dst_mac)

                if a.id == SAI_NPM_SESSION_ATTR_OUTER_VLANID:
                    sys_logging("get SAI_NPM_SESSION_ATTR_OUTER_VLANID = %d" %a.value.u16)
                    assert (a.value.u16 == outer_vlanid) 
            
                if a.id == SAI_NPM_SESSION_ATTR_INNER_VLANID:
                    sys_logging("get SAI_NPM_SESSION_ATTR_INNER_VLANID = %d" %a.value.u16)
                    assert (a.value.u16 == inner_vlan_id) 

                if a.id == SAI_NPM_SESSION_ATTR_SRC_IP:
                    sys_logging("get SAI_NPM_SESSION_ATTR_SRC_IP = %s" %a.value.ipaddr.addr.ip4)
                    assert (a.value.ipaddr.addr.ip4 == src_ip)
                
                if a.id == SAI_NPM_SESSION_ATTR_DST_IP:
                    sys_logging("get SAI_NPM_SESSION_ATTR_DST_IP = %s" %a.value.ipaddr.addr.ip4)
                    assert (a.value.ipaddr.addr.ip4 == dst_ip)
            
                if a.id == SAI_NPM_SESSION_ATTR_UDP_SRC_PORT:
                    sys_logging("get SAI_NPM_SESSION_ATTR_UDP_SRC_PORT = %d" %a.value.u32)
                    assert (a.value.u32 == udp_src_port)

                if a.id == SAI_NPM_SESSION_ATTR_UDP_DST_PORT:
                    sys_logging("get SAI_NPM_SESSION_ATTR_UDP_DST_PORT = %d" %a.value.u32)
                    assert (a.value.u32 == udp_dst_port) 

                if a.id == SAI_NPM_SESSION_ATTR_TTL:
                    sys_logging("get SAI_NPM_SESSION_ATTR_TTL = %d" %a.value.u8)
                    assert (a.value.u8 == ttl)

                if a.id == SAI_NPM_SESSION_ATTR_TC:
                    sys_logging("get SAI_NPM_SESSION_ATTR_TC = %d" %a.value.u8)
                    assert (a.value.u8 == tc)

                if a.id == SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT:
                    sys_logging("get SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT = %d" %a.value.booldata)
                    assert (a.value.booldata == enable_transmit)
                    
                if a.id == SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER:
                    sys_logging("get SAI_NPM_SESSION_ATTR_VPN_VIRTUAL_ROUTER = %d" %a.value.oid)
                    assert (a.value.oid == vrf_oid)
                
                if a.id == SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID:
                    sys_logging("get SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID = %d" %a.value.booldata)
                    assert (a.value.booldata == hw_lookup)
                
                if a.id == SAI_NPM_SESSION_ATTR_PACKET_LENGTH:
                    sys_logging("get SAI_NPM_SESSION_ATTR_PACKET_LENGTH = %d" %a.value.u32)
                    assert (a.value.u32 == pkt_len) 
                
                if a.id == SAI_NPM_SESSION_ATTR_TX_RATE:
                    sys_logging("get SAI_NPM_SESSION_ATTR_TX_RATE = %d" %a.value.u32)
                    assert (a.value.u32 == tx_rate)
                   
                if a.id == SAI_NPM_SESSION_ATTR_PKT_TX_MODE:
                    sys_logging("get SAI_NPM_SESSION_ATTR_PKT_TX_MODE = %d" %a.value.s32)
                    assert (a.value.s32 == tx_mode)

                if a.id == SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD:
                    sys_logging("get SAI_NPM_SESSION_ATTR_TX_PKT_PERIOD = %d" %a.value.u32)
                    assert (a.value.u32 == 0) 
                    
                if a.id == SAI_NPM_SESSION_ATTR_TX_PKT_CNT:
                    sys_logging("get SAI_NPM_SESSION_ATTR_TX_PKT_CNT = %d" %a.value.u32)
                    assert (a.value.u32 == tx_pkt_cnt)

                if a.id == SAI_NPM_SESSION_ATTR_TX_PKT_DURATION:
                    sys_logging("get SAI_NPM_SESSION_ATTR_TX_PKT_DURATION = %d" %a.value.u32)
                    assert (a.value.u32 == 0)

            sys_logging(" step 4 set npm session attr ")

            enable_transmit = 0

            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            sys_logging("set npm attr status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_HW_LOOKUP_VALID, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            sys_logging("set npm attr status = %d" %status)
            assert (status != SAI_STATUS_SUCCESS)
            

            sys_logging(" step 5 get npm session attr ")
            
            attrs = self.client.sai_thrift_get_npm_attribute(npm_session_oid)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
            
                if a.id == SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT:
                    sys_logging("get SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT = %d" %a.value.booldata)
                    assert (a.value.booldata == enable_transmit)

        finally:
        
            sys_logging("step 3 clear configuration")
            #pdb.set_trace()
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)
            assert (status == SAI_STATUS_SUCCESS)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  




class func_08_get_and_clear_npm_session_stats_fn(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        encap_type = SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port_list[0])
        test_port_oid = bport_oid
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        src_mac = '00:00:00:00:00:01'
        dst_mac = '00:00:00:00:00:02'
        outer_vlanid = 100
        inner_vlan_id = 200
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '5.6.7.8' 
        udp_src_port = 1234 
        udp_dst_port = 5678
        ttl = 100
        tc = 0 
        enable_transmit = 1 
        vrf_oid = 0
        hw_lookup = 1
        pkt_len = 100
        tx_rate = 100
        tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
        tx_period = None
        tx_pkt_cnt = 1
        tx_pkt_duration =None

             
        sys_logging(" step 1 basic data environment")

        vlan_id = outer_vlanid
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[0], SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
 
        
        try:

            sys_logging(" step 2 create npm session on sender ")
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=outer_vlanid,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            #pdb.set_trace()
            self.ctc_show_packet_twamp(1,str(pkt)) 
            #check packet with not care udpchecksum
            #self.ctc_show_packet_twamp(1,str(pkt),48,2) 

            sys_logging(" step 3 get npm session stats ")


            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 1)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)



            sys_logging(" step 4 clear npm session stats ")


            status = self.client.sai_thrift_clear_npm_session_stats(npm_session_oid, counter_ids, 8)
            sys_logging("###clear npm stats status = %d###" %status)          
            assert (status == SAI_STATUS_SUCCESS)  

        
            sys_logging(" step 5 get npm session stats again ")


            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)


            
        finally:
        
            sys_logging("step 6 clear configuration")
            #pdb.set_trace()
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)
            assert (status == SAI_STATUS_SUCCESS)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  


class scenario_01_ether_vlan_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        sys_logging(" npm session info ")

        encap_type = SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port_list[1])
        test_port_oid = bport_oid
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        src_mac = '00:00:00:00:00:01'
        dst_mac = '00:00:00:00:00:02'
        outer_vlanid = 100
        inner_vlan_id = 0
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '5.6.7.8' 
        udp_src_port = 1234 
        udp_dst_port = 5678
        ttl = 100
        tc = 0 
        enable_transmit = 0 
        vrf_oid = 0
        hw_lookup = 1
        pkt_len = 100
        tx_rate = 100
        tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
        tx_period = None
        tx_pkt_cnt = 1
        tx_pkt_duration =None

             
        sys_logging(" step 1 basic data environment")

        vlan_id = outer_vlanid
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[2], SAI_VLAN_TAGGING_MODE_TAGGED)
 
        
        try:

            sys_logging(" step 2 create npm session on sender ")
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            #pdb.set_trace()
            warmboot(self.client)
            
            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)

            sys_logging(" step 4 check npm tx packet ") 

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            tx_pkt = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=outer_vlanid,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            #pdb.set_trace()
            self.ctc_show_packet_twamp(2,str(tx_pkt))             

            sys_logging(" step 5 check npm rx packet ") 

            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            rx_pkt = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=outer_vlanid,
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


        
        
        
            self.ctc_send_packet( 2, str(rx_pkt))
            
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)


            sys_logging(" step 7 clear npm session stats ")


            status = self.client.sai_thrift_clear_npm_session_stats(npm_session_oid, counter_ids, 8)
            sys_logging("###clear npm stats status = %d###" %status)          
            assert (status == SAI_STATUS_SUCCESS)  

        
            sys_logging(" step 8 get npm session stats again ")


            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            
        finally:
        
            sys_logging("step 9 clear configuration")
            #pdb.set_trace()
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  


class scenario_02_ether_vlan_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        sys_logging(" npm session info ")
        
        encap_type = SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port_list[1])
        test_port_oid = bport_oid
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        src_mac = '00:00:00:00:00:01'
        dst_mac = '00:00:00:00:00:02'
        outer_vlanid = 100
        inner_vlan_id = 0
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '5.6.7.8' 
        udp_src_port = 1234 
        udp_dst_port = 5678
        tc = 0 
        vrf_oid = 0
        hw_lookup = 1
        pkt_len = 100
             
        sys_logging(" step 1 basic data environment")

        vlan_id = outer_vlanid
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[2], SAI_VLAN_TAGGING_MODE_TAGGED)
         
        try:

            sys_logging(" step 2 create npm session on reflector ")
            
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)

            #pdb.set_trace()
            warmboot(self.client)
            

            sys_logging(" step 3 send packet test ")

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            rx_pkt = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=outer_vlanid,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=255,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


                                      
            tx_pkt = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=outer_vlanid,
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=255,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            self.ctc_send_packet(2, str(rx_pkt))
            self.ctc_verify_packets( str(tx_pkt), [2], 1)

            
        finally:
        
            sys_logging("step 3 clear configuration")
            #spdb.set_trace()
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_03_l2vpn_raw_vpls_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
            
        port1 = port_list[1]
        port2 = port_list[2]
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
            #self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            #self.ctc_send_packet( 1, str(pkt3))
            #self.ctc_verify_packets( pkt4, [2])


            sys_logging(" step 2 create npm session on sender ")

            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 0 
            enable_transmit = 0 
            vrf_oid = 0
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None

            sai_thrift_create_fdb_bport(self.client, bridge_id, dst_mac, tunnel_bport, mac_action)
        
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            #pdb.set_trace()
            warmboot(self.client)

            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)


            sys_logging(" step 4 check npm tx packet ") 

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            tx_mpls_inner_pkt = simple_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)


 
            self.ctc_show_packet_twamp(1,str(tx_pkt)) 

            sys_logging(" step 5 check npm rx packet ") 
            #pdb.set_trace()

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp

            rx_mpls_inner_pkt1 = simple_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)



            self.ctc_send_packet( 1, str(rx_pkt))

            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100+18)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)

            
            
        finally:

            sys_logging("======clean up======")

            #pdb.set_trace()

            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id, dst_mac, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id, src_mac, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)




class scenario_04_l2vpn_raw_vpls_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
            
        port1 = port_list[1]
        port2 = port_list[2]
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
            #self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            #self.ctc_send_packet( 1, str(pkt3))
            #self.ctc_verify_packets( pkt4, [2])


            sys_logging(" step 2 create npm session on reflector ")

            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 0 
            vrf_oid = 0
            hw_lookup = 1

            pkt_len = 100
            ttl = 100
            

            sai_thrift_create_fdb_bport(self.client, bridge_id, dst_mac, bport, mac_action)
                    
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)

            #pdb.set_trace()
            warmboot(self.client)


            sys_logging(" step 3 check npm tx and rx packet ") 

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp

            rx_mpls_inner_pkt1 = simple_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)


            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            tx_mpls_inner_pkt = simple_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)




            self.ctc_send_packet(1, str(rx_pkt))
            self.ctc_verify_packets(tx_pkt, [1])  

            
        finally:

            sys_logging("======clean up======")

            #pdb.set_trace()

            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id, src_mac, tunnel_bport)            
            sai_thrift_delete_fdb(self.client, bridge_id, dst_mac, bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)



class scenario_05_l2vpn_tagged_vpls_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        tag_vlan = 30
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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=tag_vlan)
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


        try:
        
            #ac to pw
            #self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            #self.ctc_send_packet( 1, str(pkt3))
            #self.ctc_verify_packets( pkt4, [2])


            
            sys_logging(" step 2 create npm session on sender ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 0 
            enable_transmit = 0 
            vrf_oid = 0
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None
            
            sai_thrift_create_fdb_bport(self.client, bridge_id, dst_mac, tunnel_bport, mac_action)
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            
            #pdb.set_trace()
            warmboot(self.client)
            
            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            
            
            sys_logging(" step 4 check npm tx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            

            tx_mpls_inner_pkt = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
            
            self.ctc_show_packet_twamp(1,str(tx_pkt)) 
            
            sys_logging(" step 5 check npm rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp

            rx_mpls_inner_pkt1 = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                                                        
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            
            self.ctc_send_packet( 1, str(rx_pkt))
            
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100+22)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)

            
        finally:
        
            sys_logging("======clean up======")
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)

            sai_thrift_delete_fdb(self.client, bridge_id, src_mac, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, dst_mac, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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
            
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)




class scenario_06_l2vpn_tagged_vpls_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        tag_vlan = 30
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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=tag_vlan)
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


        try:
        
            #ac to pw
            #self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            #self.ctc_send_packet( 1, str(pkt3))
            #self.ctc_verify_packets( pkt4, [2])

            
            sys_logging(" step 2 create npm session on reflector ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 0 
            vrf_oid = 0
            hw_lookup = 1
            
            pkt_len = 100
            ttl = 100
            
            
            sai_thrift_create_fdb_bport(self.client, bridge_id, dst_mac, bport, mac_action)
                    
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            #pdb.set_trace()
            warmboot(self.client)
            
            
            sys_logging(" step 3 check npm tx and rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp

            rx_mpls_inner_pkt1 = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            

            tx_mpls_inner_pkt = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
                        
            self.ctc_send_packet(1, str(rx_pkt))
            self.ctc_verify_packets(tx_pkt, [1])  


            
        finally:
        
            sys_logging("======clean up======")
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)

            sai_thrift_delete_fdb(self.client, bridge_id, src_mac, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, dst_mac, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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
            
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)




class scenario_07_l2vpn_raw_vpws_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
                
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

        try:
 
            #ac to pw
            #self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            #self.ctc_send_packet( 1, str(pkt3))
            #self.ctc_verify_packets( pkt4, [2])

            
            sys_logging(" step 2 create npm session on sender ")

            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 0 
            enable_transmit = 0 
            vrf_oid = 0
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None
                        
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            
            #pdb.set_trace()
            warmboot(self.client)

            
            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            
            
            sys_logging(" step 4 check npm tx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            
            tx_mpls_inner_pkt = simple_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
            
            self.ctc_show_packet_twamp(1,str(tx_pkt)) 
            
            
            sys_logging(" step 5 check npm rx packet ") 
            #pdb.set_trace()
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            rx_mpls_inner_pkt1 = simple_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(rx_pkt))
            
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100+18)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
 
        finally:
        
            sys_logging("======clean up======")

            #pdb.set_trace()
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)





class scenario_08_l2vpn_raw_vpws_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
                
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

        try:
 
            #ac to pw
            #self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            #self.ctc_send_packet( 1, str(pkt3))
            #self.ctc_verify_packets( pkt4, [2])

            
            sys_logging(" step 2 create npm session on reflector ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 0 
            vrf_oid = 0
            hw_lookup = 1
            
            pkt_len = 100
            ttl = 100
            
                               
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            #pdb.set_trace()
            warmboot(self.client)
            
            
            sys_logging(" step 3 check npm tx and rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            rx_mpls_inner_pkt1 = simple_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            
            tx_mpls_inner_pkt = simple_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
            
            
            self.ctc_send_packet(1, str(rx_pkt))
            self.ctc_verify_packets(tx_pkt, [1])  

 
        finally:
        
            sys_logging("======clean up======")

            #pdb.set_trace()
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)




class scenario_09_l2vpn_tagged_vpws_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        tag_vlan = 30
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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=tag_vlan)


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

        try:
 
            #ac to pw
            #self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            #self.ctc_send_packet( 1, str(pkt3))
            #self.ctc_verify_packets( pkt4, [2])

            
            sys_logging(" step 2 create npm session on sender ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 0 
            enable_transmit = 0 
            vrf_oid = 0
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None
            
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            
            #pdb.set_trace()
            warmboot(self.client)
            
            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            
            
            sys_logging(" step 4 check npm tx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            
            tx_mpls_inner_pkt = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
            
            self.ctc_show_packet_twamp(1,str(tx_pkt)) 
            
            sys_logging(" step 5 check npm rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            rx_mpls_inner_pkt1 = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                                                        
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            
            self.ctc_send_packet( 1, str(rx_pkt))
            
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100+22)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)



 
        finally:
        
            sys_logging("======clean up======")
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)




class scenario_10_l2vpn_tagged_vpws_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        tag_vlan = 30
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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=tag_vlan)


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

        try:
 
            #ac to pw
            #self.ctc_send_packet( 2, str(pkt1))
            #self.ctc_verify_packets( pkt2, [1])

            #pw to ac
            #self.ctc_send_packet( 1, str(pkt3))
            #self.ctc_verify_packets( pkt4, [2])

            
            sys_logging(" step 2 create npm session on reflector ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 0 
            vrf_oid = 0
            hw_lookup = 1
            
            pkt_len = 100
            ttl = 100
            
                                
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            #pdb.set_trace()
            warmboot(self.client)
            
            
            sys_logging(" step 3 check npm tx and rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            rx_mpls_inner_pkt1 = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            
            tx_mpls_inner_pkt = simple_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
                        
            self.ctc_send_packet(1, str(rx_pkt))
            self.ctc_verify_packets(tx_pkt, [1])  

 
        finally:
        
            sys_logging("======clean up======")
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)



class scenario_11_raw_ip_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        sys_logging(" step 1 basic data environment")

        port1 = port_list[1]
        port2 = port_list[2]

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        vrf_oid = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)           
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vrf_oid, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)               
        rif_id1 = sai_thrift_create_router_interface(self.client, vrf_oid, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        
        dstip = '20.1.1.2'   
        dmac = '00:00:00:00:00:02'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dstip, dmac)
      
        nhop = sai_thrift_create_nhop(self.client, addr_family, dstip, rif_id1)       
         
        dst_ip_subnet = '5.6.7.8'
        ip_mask = '255.255.255.255'        
        sai_thrift_create_route(self.client, vrf_oid, addr_family, dst_ip_subnet, ip_mask, nhop)        
        
        try:

            sys_logging(" step 2 create npm session on sender ")

            encap_type = SAI_NPM_ENCAPSULATION_TYPE_RAW_IP
            test_port_oid = port1
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = 0
            inner_vlan_id = 0
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 0 
            enable_transmit = 0 
            vrf_oid = vrf_oid
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None

            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            
            
            sys_logging(" step 4 check npm tx packet ") 
            

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    dl_vlan_enable=False,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl-1,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            #pdb.set_trace()
            self.ctc_show_packet_twamp(2,str(pkt1)) 


            sys_logging(" step 5 check npm rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt2 = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=router_mac,
                                    eth_src=dmac,
                                    dl_vlan_enable=False,
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl-1,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


                       
            self.ctc_send_packet(2, str(pkt2))
            
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            
        finally:
        
            sys_logging("clear configuration")
            
            sai_thrift_remove_route(self.client, vrf_oid, addr_family, dst_ip_subnet, ip_mask, nhop)
            
            self.client.sai_thrift_remove_next_hop(nhop)            

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dstip, dmac) 

            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vrf_oid)

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)







class scenario_12_raw_ip_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        sys_logging(" step 1 basic data environment")

        port1 = port_list[1]
        port2 = port_list[2]

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        vrf_oid = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)           
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vrf_oid, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)               
        rif_id1 = sai_thrift_create_router_interface(self.client, vrf_oid, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        
        dstip = '20.1.1.1'   
        dmac = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dstip, dmac)
      
        nhop = sai_thrift_create_nhop(self.client, addr_family, dstip, rif_id1)       
         
        dst_ip_subnet = '1.2.3.4'
        ip_mask = '255.255.255.255'        
        sai_thrift_create_route(self.client, vrf_oid, addr_family, dst_ip_subnet, ip_mask, nhop)        


        dstip2 = '5.6.7.8'   
        dmac2 = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dstip2, dmac2)
      
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dstip2, rif_id0)       
         
        dst_ip_subnet2 = '5.6.7.8'
        ip_mask = '255.255.255.255'        
        sai_thrift_create_route(self.client, vrf_oid, addr_family, dst_ip_subnet2, ip_mask, nhop2)   
        
        try:

            sys_logging(" step 2 create npm session on reflector ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_RAW_IP
            test_port_oid = port1
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = 0
            inner_vlan_id = 0
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 0 
            vrf_oid = vrf_oid
            hw_lookup = 1
            
            pkt_len = 100
            ttl = 100
            
                                
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            #pdb.set_trace()
            warmboot(self.client)
            
            
            sys_logging(" step 3 check npm tx and rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=router_mac,
                                    eth_src=dmac,
                                    dl_vlan_enable=False,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl-1,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt2 = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    dl_vlan_enable=False,
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl-2,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            
                        
            self.ctc_send_packet(2, str(pkt1))
            self.ctc_verify_packets(pkt2, [2])  

            
        finally:
        
            sys_logging("clear configuration")

            sai_thrift_remove_route(self.client, vrf_oid, addr_family, dst_ip_subnet2, ip_mask, nhop2)            
            self.client.sai_thrift_remove_next_hop(nhop2)            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dstip2, dmac2) 

            sai_thrift_remove_route(self.client, vrf_oid, addr_family, dst_ip_subnet, ip_mask, nhop)
            self.client.sai_thrift_remove_next_hop(nhop)            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dstip, dmac) 

            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vrf_oid)

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)



           
class scenario_13_l3vpn_mpls_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        send_port_oid = port_list[2]
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 100
        pw_label = 200

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
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

        dst_ip_subnet1 = '5.6.7.0'
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

            sys_logging(" step 2 create npm session on sender ")

            encap_type = SAI_NPM_ENCAPSULATION_TYPE_MPLS_L3VPN
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = 0
            inner_vlan_id = 0
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 0 
            enable_transmit = 0 
            vrf_oid = vr_id
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None

            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            

            sys_logging(" step 4 check npm tx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp
            
            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=tunnel_mac_da,
                                    eth_src=router_mac,
                                    dl_vlan_enable=False,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl-1,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':99,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=tunnel_mac_da,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1) 
                                    
            self.ctc_show_packet_twamp(2,str(pkt2))                    

        
            sys_logging(" step 5 check npm rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp
            
            pkt3 = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=tunnel_mac_da,
                                    eth_src=router_mac,
                                    dl_vlan_enable=False,
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl-1,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label_r,'tc':0,'ttl':253,'s':0}, {'label':pw_label_r,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=router_mac,
                                    eth_src=tunnel_mac_da,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 

            self.ctc_send_packet( 1, str(pkt4))
                                   
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100+8)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            
            
        finally:
        
            sys_logging("clear configuration") 
                        
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

            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)


                       
class scenario_14_l3vpn_mpls_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]     
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        send_port_oid = port_list[2]  
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 300
        pw_label = 400

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        dst_ip0 = '5.6.7.8'   
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

        dst_ip_subnet2 = '5.6.7.0'
        ip_mask2 = '255.255.255.0'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
        
        
        try:

            sys_logging(" step 2 create npm session on reflector ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_MPLS_L3VPN
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = 0
            inner_vlan_id = 0
            addr_family = SAI_IP_ADDR_FAMILY_IPV4
            src_ip = '1.2.3.4' 
            dst_ip = '5.6.7.8' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 7 
            vrf_oid = vr_id
            hw_lookup = 1
            
            pkt_len = 100
            ttl = 100
            
                                
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            #pdb.set_trace()
            warmboot(self.client)
            
            
            sys_logging(" step 3 check npm tx and rx packet ") 
                        
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp

            
            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=dst_mac,
                          eth_src=src_mac,
                          dl_vlan_enable=False,
                          ip_src=src_ip,
                          ip_dst=dst_ip,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=254,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=udp_src_port,
                          udp_dport=udp_dst_port,
                          with_udp_chksum=True,
                          udp_payload=npm_test_pkt,
                          pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label_r,'tc':0,'ttl':32,'s':0}, {'label':pw_label_r,'tc':0,'ttl':99,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=router_mac,
                                    eth_src=tunnel_mac_da,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1)                                    

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt3 = simple_udp_packet(pktlen=pkt_len-4,
                          eth_dst=dst_mac,
                          eth_src=src_mac,
                          dl_vlan_enable=False,
                          ip_src=dst_ip,
                          ip_dst=src_ip,
                          ip_tos=28,
                          ip_ecn=None,
                          ip_dscp=None,
                          ip_ttl=253,
                          ip_ihl=None,
                          ip_options=False,
                          ip_flag=0,
                          ip_id=0,
                          udp_sport=udp_dst_port,
                          udp_dport=udp_src_port,
                          with_udp_chksum=True,
                          udp_payload=npm_test_pkt,
                          pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=tunnel_mac_da,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 
                                    
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt4, [2])      

        finally:
        
            sys_logging("clear configuration") 

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
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)






class scenario_15_ipv6_ether_vlan_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        sys_logging(" npm session info ")

        encap_type = SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port_list[1])
        test_port_oid = bport_oid
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        src_mac = '00:00:00:00:00:01'
        dst_mac = '00:00:00:00:00:02'
        outer_vlanid = 100
        inner_vlan_id = 0
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        src_ip = '2001:11:11:11:11:11:11:11' 
        dst_ip = '2001:22:22:22:22:22:22:22' 
        udp_src_port = 1234 
        udp_dst_port = 5678
        ttl = 100
        tc = 7 
        enable_transmit = 0 
        vrf_oid = 0
        hw_lookup = 1
        pkt_len = 100
        tx_rate = 100
        tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
        tx_period = None
        tx_pkt_cnt = 1
        tx_pkt_duration =None

             
        sys_logging(" step 1 basic data environment")

        vlan_id = outer_vlanid
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[2], SAI_VLAN_TAGGING_MODE_TAGGED)
 
        
        try:

            sys_logging(" step 2 create npm session on sender ")
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            #pdb.set_trace()
            warmboot(self.client)
            
            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)

            sys_logging(" step 4 check npm tx packet ") 

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp

            tx_pkt = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=outer_vlanid,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            #pdb.set_trace()
            self.ctc_show_packet_twamp(2,str(tx_pkt))             

            sys_logging(" step 5 check npm rx packet ") 

            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            rx_pkt = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=outer_vlanid,
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            #pdb.set_trace()   
            self.ctc_send_packet( 2, str(rx_pkt))
            
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            
        finally:
        
            sys_logging("step 3 clear configuration")
            #pdb.set_trace()
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  


class scenario_16_ipv6_ether_vlan_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        sys_logging(" npm session info ")
        
        encap_type = SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port_list[1])
        test_port_oid = bport_oid
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        src_mac = '00:00:00:00:00:01'
        dst_mac = '00:00:00:00:00:02'
        outer_vlanid = 100
        inner_vlan_id = 0
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        src_ip = '2001:11:11:11:11:11:11:11' 
        dst_ip = '2001:22:22:22:22:22:22:22' 
        udp_src_port = 1234 
        udp_dst_port = 5678
        tc = 7 
        vrf_oid = 0
        hw_lookup = 1
        pkt_len = 100
             
        sys_logging(" step 1 basic data environment")

        vlan_id = outer_vlanid
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
         
        try:

            sys_logging(" step 2 create npm session on reflector ")
            
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)

            #pdb.set_trace()
            warmboot(self.client)
            

            sys_logging(" step 3 send packet test ")

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp

                 
            rx_pkt = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=outer_vlanid,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=255,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


                                      
            tx_pkt = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=outer_vlanid,
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=255,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            self.ctc_send_packet(2, str(rx_pkt))
            self.ctc_verify_packets( str(tx_pkt), [2], 1)

            
        finally:
        
            sys_logging("step 3 clear configuration")
            #spdb.set_trace()
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)




class scenario_17_ipv6_l2vpn_raw_vpls_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
            
        port1 = port_list[1]
        port2 = port_list[2]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:0'
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

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
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
        
        try:
        
            sys_logging(" step 2 create npm session on sender ")

            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 7 
            enable_transmit = 0 
            vrf_oid = 0
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None

            sai_thrift_create_fdb_bport(self.client, bridge_id, dst_mac, tunnel_bport, mac_action)
        
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            #pdb.set_trace()
            warmboot(self.client)

            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)


            sys_logging(" step 4 check npm tx packet ") 

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            tx_mpls_inner_pkt = simple_ipv6_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)


 
            self.ctc_show_packet_twamp(1,str(tx_pkt)) 

            sys_logging(" step 5 check npm rx packet ") 
            #pdb.set_trace()

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp

            rx_mpls_inner_pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)



            self.ctc_send_packet( 1, str(rx_pkt))

            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100+18)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)

            
            
        finally:

            sys_logging("======clean up======")

            #pdb.set_trace()

            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id, dst_mac, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id, src_mac, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)




class scenario_18_ipv6_l2vpn_raw_vpls_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
            
        port1 = port_list[1]
        port2 = port_list[2]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:0'
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
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

        
        try:
        
            sys_logging(" step 2 create npm session on reflector ")

            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22'  
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 7 
            vrf_oid = 0
            hw_lookup = 1

            pkt_len = 100
            ttl = 100
            

            sai_thrift_create_fdb_bport(self.client, bridge_id, dst_mac, bport, mac_action)
                    
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)

            #pdb.set_trace()
            warmboot(self.client)


            sys_logging(" step 3 check npm tx and rx packet ") 

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp

                   
            rx_mpls_inner_pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)


            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            tx_mpls_inner_pkt = simple_ipv6_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)




            self.ctc_send_packet(1, str(rx_pkt))
            self.ctc_verify_packets(tx_pkt, [1])  

            
        finally:

            sys_logging("======clean up======")

            #pdb.set_trace()

            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            sai_thrift_delete_fdb(self.client, bridge_id, src_mac, tunnel_bport)            
            sai_thrift_delete_fdb(self.client, bridge_id, dst_mac, bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)



class scenario_19_ipv6_l2vpn_tagged_vpls_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        tag_vlan = 30
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:0'
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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=tag_vlan)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
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

        try:


            sys_logging(" step 2 create npm session on sender ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22'
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 7 
            enable_transmit = 0 
            vrf_oid = 0
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None
            
            sai_thrift_create_fdb_bport(self.client, bridge_id, dst_mac, tunnel_bport, mac_action)
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            
            #pdb.set_trace()
            warmboot(self.client)
            
            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            
            
            sys_logging(" step 4 check npm tx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            

            tx_mpls_inner_pkt = simple_ipv6_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
            
            self.ctc_show_packet_twamp(1,str(tx_pkt)) 
            
            sys_logging(" step 5 check npm rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp

            rx_mpls_inner_pkt1 = simple_ipv6_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                                                        
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            
            self.ctc_send_packet( 1, str(rx_pkt))
            
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100+22)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)

            
        finally:
        
            sys_logging("======clean up======")
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)

            sai_thrift_delete_fdb(self.client, bridge_id, src_mac, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, dst_mac, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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
            
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)




class scenario_20_ipv6_l2vpn_tagged_vpls_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        tag_vlan = 30
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:0'
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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=tag_vlan)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
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

        try:
            
            sys_logging(" step 2 create npm session on reflector ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPLS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 7 
            vrf_oid = 0
            hw_lookup = 1
            
            pkt_len = 100
            ttl = 100
            
            
            sai_thrift_create_fdb_bport(self.client, bridge_id, dst_mac, bport, mac_action)
                    
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            #pdb.set_trace()
            warmboot(self.client)
            
            
            sys_logging(" step 3 check npm tx and rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp

            rx_mpls_inner_pkt1 = simple_ipv6_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            

            tx_mpls_inner_pkt = simple_ipv6_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
                        
            self.ctc_send_packet(1, str(rx_pkt))
            self.ctc_verify_packets(tx_pkt, [1])  


            
        finally:
        
            sys_logging("======clean up======")

            #pdb.set_trace()
            
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)

            sai_thrift_delete_fdb(self.client, bridge_id, src_mac, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, dst_mac, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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
            
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)




class scenario_21_ipv6_l2vpn_raw_vpws_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
                
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:0'
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
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

        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        
        try:
             
            sys_logging(" step 2 create npm session on sender ")

            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 7 
            enable_transmit = 0 
            vrf_oid = 0
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None
                        
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            
            #pdb.set_trace()
            warmboot(self.client)

            
            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            
            
            sys_logging(" step 4 check npm tx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
                                                
            tx_mpls_inner_pkt = simple_ipv6_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
            
            self.ctc_show_packet_twamp(1,str(tx_pkt)) 
            
            
            sys_logging(" step 5 check npm rx packet ") 
            #pdb.set_trace()
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            rx_mpls_inner_pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            
            #pdb.set_trace()
            self.ctc_send_packet( 1, str(rx_pkt))
            
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100+18)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
 
        finally:
        
            sys_logging("======clean up======")

            #pdb.set_trace()
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)





class scenario_22_ipv6_l2vpn_raw_vpws_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
                
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:0'
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
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
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

        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        

        try:

          
            sys_logging(" step 2 create npm session on reflector ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22'
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 7 
            vrf_oid = 0
            hw_lookup = 1
            
            pkt_len = 100
            ttl = 100
            
                               
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            #pdb.set_trace()
            warmboot(self.client)
            
            
            sys_logging(" step 3 check npm tx and rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp

                                    
            rx_mpls_inner_pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            
            tx_mpls_inner_pkt = simple_ipv6_udp_packet(pktlen=pkt_len-4-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=inner_vlan_id,
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
            
            
            self.ctc_send_packet(1, str(rx_pkt))
            self.ctc_verify_packets(tx_pkt, [1])  

 
        finally:
        
            sys_logging("======clean up======")

            #pdb.set_trace()
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)




class scenario_23_ipv6_l2vpn_tagged_vpws_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        tag_vlan = 30
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:0'
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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=tag_vlan)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
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
                                                    
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        

        try:
            
            sys_logging(" step 2 create npm session on sender ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22'
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 7 
            enable_transmit = 0 
            vrf_oid = 0
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None
            
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            
            #pdb.set_trace()
            warmboot(self.client)
            
            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            
            
            sys_logging(" step 4 check npm tx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
                                    
            tx_mpls_inner_pkt = simple_ipv6_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
            
            self.ctc_show_packet_twamp(1,str(tx_pkt)) 
            
            sys_logging(" step 5 check npm rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            rx_mpls_inner_pkt1 = simple_ipv6_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                                                        
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            
            self.ctc_send_packet( 1, str(rx_pkt))
            
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100+22)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)



 
        finally:
        
            sys_logging("======clean up======")
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)




class scenario_24_ipv6_l2vpn_tagged_vpws_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        sys_logging(" step 1 basic data environment")
        
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 20
        tag_vlan = 30
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:0'
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

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=tag_vlan)


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
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
                                                    
        self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
        self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
        
        try:
 

            sys_logging(" step 2 create npm session on reflector ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_L2VPN_VPWS
            test_port_oid = bport
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = vlan_id
            inner_vlan_id = 100
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22'
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 7 
            vrf_oid = 0
            hw_lookup = 1
            
            pkt_len = 100
            ttl = 100
            
                                
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            #pdb.set_trace()
            warmboot(self.client)
            
            
            sys_logging(" step 3 check npm tx and rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
                                    
            rx_mpls_inner_pkt1 = simple_ipv6_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            rx_mpls_label_stack1 = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            rx_pkt = simple_mpls_packet(
                                    eth_dst=router_mac,
                                    eth_src='00:55:55:55:55:66',
                                    mpls_type=0x8847,
                                    mpls_tags= rx_mpls_label_stack1,
                                    inner_frame = rx_mpls_inner_pkt1)
            
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            tx_mpls_inner_pkt = simple_ipv6_qinq_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    outer_vlan_enable=True,
                                    outer_vlan_vid=tag_vlan,
                                    inner_vlan_enable=True,
                                    inner_vlan_vid=inner_vlan_id,                                    
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                                    
            
            tx_mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            tx_pkt = simple_mpls_packet(
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= tx_mpls_label_stack,
                                    inner_frame = tx_mpls_inner_pkt)
            
            
                        
            self.ctc_send_packet(1, str(rx_pkt))
            self.ctc_verify_packets(tx_pkt, [1])  

 
        finally:
        
            sys_logging("======clean up======")
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport, port2)
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

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)




class scenario_25_ipv6_raw_ip_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        sys_logging(" step 1 basic data environment")

        port1 = port_list[1]
        port2 = port_list[2]

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
        vrf_oid = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)           
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vrf_oid, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)               
        rif_id1 = sai_thrift_create_router_interface(self.client, vrf_oid, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        
        dstip = '2012:0:0:0:0:0:0:2'
        dmac = '00:00:00:00:00:02'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dstip, dmac)
      
        nhop = sai_thrift_create_nhop(self.client, addr_family, dstip, rif_id1)       
         
        dst_ip_subnet = '2001:22:22:22:22:22:22:22'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'       
        sai_thrift_create_route(self.client, vrf_oid, addr_family, dst_ip_subnet, ip_mask, nhop)        
        
        try:

            sys_logging(" step 2 create npm session on sender ")

            encap_type = SAI_NPM_ENCAPSULATION_TYPE_RAW_IP
            test_port_oid = port1
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = 0
            inner_vlan_id = 0
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 7 
            enable_transmit = 0 
            vrf_oid = vrf_oid
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None

            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            
            
            sys_logging(" step 4 check npm tx packet ") 
            

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp
                
            pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    dl_vlan_enable=False,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl-1,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            #pdb.set_trace()
            self.ctc_show_packet_twamp(2,str(pkt1)) 


            sys_logging(" step 5 check npm rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt2 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=router_mac,
                                    eth_src=dmac,
                                    dl_vlan_enable=False,
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl-1,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


                       
            self.ctc_send_packet(2, str(pkt2))
            
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            
        finally:
        
            sys_logging("clear configuration")
            
            sai_thrift_remove_route(self.client, vrf_oid, addr_family, dst_ip_subnet, ip_mask, nhop)
            
            self.client.sai_thrift_remove_next_hop(nhop)            

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dstip, dmac) 

            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vrf_oid)

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)







class scenario_26_ipv6_raw_ip_reflector_rx_and_tx_testt(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        sys_logging(" step 1 basic data environment")

        port1 = port_list[1]
        port2 = port_list[2]

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
        vrf_oid = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)           
              
        rif_id0 = sai_thrift_create_router_interface(self.client, vrf_oid, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)               
        rif_id1 = sai_thrift_create_router_interface(self.client, vrf_oid, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        
        dstip = '2012:0:0:0:0:0:0:2'
        dmac = '00:00:00:00:00:02'       
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dstip, dmac)
      
        nhop = sai_thrift_create_nhop(self.client, addr_family, dstip, rif_id1)       
         
        dst_ip_subnet = '2001:11:11:11:11:11:11:11'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'        
        sai_thrift_create_route(self.client, vrf_oid, addr_family, dst_ip_subnet, ip_mask, nhop)        


        dstip2 = '2001:22:22:22:22:22:22:22'   
        dmac2 = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dstip2, dmac2)
      
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, dstip2, rif_id0)       
         
        dst_ip_subnet2 = '2001:22:22:22:22:22:22:22'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'          
        sai_thrift_create_route(self.client, vrf_oid, addr_family, dst_ip_subnet2, ip_mask, nhop2)   
        
        try:

            sys_logging(" step 2 create npm session on reflector ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_RAW_IP
            test_port_oid = port1
            receive_port_oid = [port_list[1],port_list[2],port_list[3]]
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = 0
            inner_vlan_id = 0
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 7 
            vrf_oid = vrf_oid
            hw_lookup = 1
            
            pkt_len = 100
            ttl = 100
            
                                
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            #pdb.set_trace()
            warmboot(self.client)
            
            
            sys_logging(" step 3 check npm tx and rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp

            pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=router_mac,
                                    eth_src=dmac,
                                    dl_vlan_enable=False,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl-1,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt2 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dmac,
                                    eth_src=router_mac,
                                    dl_vlan_enable=False,
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl-2,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            
                        
            self.ctc_send_packet(2, str(pkt1))
            self.ctc_verify_packets(pkt2, [2])  

            
        finally:
        
            sys_logging("clear configuration")

            sai_thrift_remove_route(self.client, vrf_oid, addr_family, dst_ip_subnet2, ip_mask, nhop2)            
            self.client.sai_thrift_remove_next_hop(nhop2)            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id0, dstip2, dmac2) 

            sai_thrift_remove_route(self.client, vrf_oid, addr_family, dst_ip_subnet, ip_mask, nhop)
            self.client.sai_thrift_remove_next_hop(nhop)            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, dstip, dmac) 

            self.client.sai_thrift_remove_router_interface(rif_id0)
            self.client.sai_thrift_remove_router_interface(rif_id1)

            self.client.sai_thrift_remove_virtual_router(vrf_oid)

            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)



          
class scenario_27_ipv6_l3vpn_mpls_sender_tx_and_rx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        send_port_oid = port_list[2]
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 100
        pw_label = 200

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        dst_ip0 = '2001:11:11:11:11:11:11:11'    
        dmac0 = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        dst_ip1 = '2040:11:11:11:11:11:11:11'    
        dmac1 = '00:00:00:00:00:02'         
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        tunnel_ip_da = '2010:11:11:11:11:11:11:11' 
        tunnel_mac_da = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da)                
        lsp_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, tunnel_ip_da, rif_id2, lsp_label_list)
        
        pw_next_hop = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, pw_label_list, next_level_nhop_oid=lsp_next_hop)

        dst_ip_subnet1 = '2001:22:22:22:22:22:22:22'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        lsp_label_r = 300
        pw_label_r = 400
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_inseg_entry(self.client, lsp_label_r, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, pw_label_r, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        dst_ip_subnet2 = '2001:11:11:11:11:11:11:11' 
        ip_mask2 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
                
        try:

            sys_logging(" step 2 create npm session on sender ")

            encap_type = SAI_NPM_ENCAPSULATION_TYPE_MPLS_L3VPN
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = 0
            inner_vlan_id = 0
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22' 
            udp_src_port = 1234 
            udp_dst_port = 5678
            ttl = 100
            tc = 7 
            enable_transmit = 0 
            vrf_oid = vr_id
            hw_lookup = 1
            pkt_len = 100
            tx_rate = 100
            tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
            tx_period = None
            tx_pkt_cnt = 1
            tx_pkt_duration =None

            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)

            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)


            sys_logging(" step 3 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)
            

            sys_logging(" step 4 check npm tx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp
            
            pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=tunnel_mac_da,
                                    eth_src=router_mac,
                                    dl_vlan_enable=False,
                                    ipv6_src=src_ip,
                                    ipv6_dst=dst_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl-1,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':99,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=tunnel_mac_da,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1) 
                                    
            self.ctc_show_packet_twamp(2,str(pkt2))                    

        
            sys_logging(" step 5 check npm rx packet ") 
            
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp
            
            pkt3 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=tunnel_mac_da,
                                    eth_src=router_mac,
                                    dl_vlan_enable=False,
                                    ipv6_src=dst_ip,
                                    ipv6_dst=src_ip,
                                    ipv6_tc=28,
                                    ipv6_ecn=None,
                                    ipv6_dscp=None,
                                    ipv6_hlim=ttl-1,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label_r,'tc':0,'ttl':253,'s':0}, {'label':pw_label_r,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=router_mac,
                                    eth_src=tunnel_mac_da,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 

            self.ctc_send_packet( 1, str(pkt4))
                                   
            sys_logging(" step 6 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100+8)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)
            
            
        finally:
        
            sys_logging("clear configuration") 
                        
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

            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)


                       
class scenario_28_ipv6_l3vpn_mpls_reflector_rx_and_tx_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)

        test_port_oid = port_list[0]     
        receive_port_oid = [port_list[1],port_list[2],port_list[3]]
        send_port_oid = port_list[2]  
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV6

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
       
        lsp_label = 300
        pw_label = 400

        lsp_label_list = [(lsp_label<<12) | 32]
        pw_label_list = [(pw_label<<12) | 32]
                
        sys_logging(" step 1 basic data environment")

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        rif_id0 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, test_port_oid, 0, v4_enabled, v6_enabled, mac)
        dst_ip0 = '2001:22:22:22:22:22:22:22'   
        dmac0 = '00:00:00:00:00:01'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id0, dst_ip0, dmac0)
        nhop0 = sai_thrift_create_nhop(self.client, addr_family, dst_ip0, rif_id0)
        
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port_list[1], 0, v4_enabled, v6_enabled, mac)
        dst_ip1 = '2012:11:11:11:11:11:11:11'
        dmac1 = '00:00:00:00:00:02'         
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, dst_ip1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, dst_ip1, rif_id1)
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, send_port_oid, 0, v4_enabled, v6_enabled, mac)
        tunnel_ip_da = '2013:11:11:11:11:11:11:11'
        tunnel_mac_da = '00:00:00:00:00:03'        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, tunnel_ip_da, tunnel_mac_da)                
        lsp_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, tunnel_ip_da, rif_id2, lsp_label_list)
        
        pw_next_hop = sai_thrift_create_tunnel_mpls_l3vpn_nhop(self.client, tunnel_id, pw_label_list, next_level_nhop_oid=lsp_next_hop)
        
        dst_ip_subnet1 = '2001:11:11:11:11:11:11:11'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'        
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet1, ip_mask1, pw_next_hop)


        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        lsp_label_r = 100
        pw_label_r = 200
        
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sai_thrift_create_inseg_entry(self.client, lsp_label_r, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, pw_label_r, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        dst_ip_subnet2 = '2001:22:22:22:22:22:22:22'
        ip_mask2 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'         
        sai_thrift_create_route(self.client, vr_id, addr_family, dst_ip_subnet2, ip_mask2, nhop0)
        
        
        try:

            sys_logging(" step 2 create npm session on reflector ")
            
            encap_type = SAI_NPM_ENCAPSULATION_TYPE_MPLS_L3VPN
            src_mac = '00:00:00:00:00:01'
            dst_mac = '00:00:00:00:00:02'
            outer_vlanid = 0
            inner_vlan_id = 0
            addr_family = SAI_IP_ADDR_FAMILY_IPV6
            src_ip = '2001:11:11:11:11:11:11:11' 
            dst_ip = '2001:22:22:22:22:22:22:22'
            udp_src_port = 1234 
            udp_dst_port = 5678
            tc = 7 
            vrf_oid = vr_id
            hw_lookup = 1
            
            pkt_len = 100
            ttl = 100
            
                                
            npm_session_oid = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)
            
            #pdb.set_trace()
            warmboot(self.client)
            
            
            sys_logging(" step 3 check npm tx and rx packet ") 
                        
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp

                                    
            pkt1 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=dst_mac,
                          eth_src=src_mac,
                          dl_vlan_enable=False,
                          ipv6_src=src_ip,
                          ipv6_dst=dst_ip,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=254,
                          udp_sport=udp_src_port,
                          udp_dport=udp_dst_port,
                          with_udp_chksum=True,
                          udp_payload=npm_test_pkt,
                          pattern_type=1)

                          
            pkt1 = str(pkt1)[14:]
                          
            mpls1 = [{'label':lsp_label_r,'tc':0,'ttl':32,'s':0}, {'label':pw_label_r,'tc':0,'ttl':99,'s':1}]   
                                               
            pkt2 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=router_mac,
                                    eth_src=tunnel_mac_da,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls1,
                                    inner_frame = pkt1)                                    

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            pkt3 = simple_ipv6_udp_packet(pktlen=pkt_len-4,
                          eth_dst=dst_mac,
                          eth_src=src_mac,
                          dl_vlan_enable=False,
                          ipv6_src=dst_ip,
                          ipv6_dst=src_ip,
                          ipv6_tc=28,
                          ipv6_ecn=None,
                          ipv6_dscp=None,
                          ipv6_hlim=253,
                          udp_sport=udp_dst_port,
                          udp_dport=udp_src_port,
                          with_udp_chksum=True,
                          udp_payload=npm_test_pkt,
                          pattern_type=1)


            pkt3 = str(pkt3)[14:]
                          
            mpls2 = [{'label':lsp_label,'tc':0,'ttl':32,'s':0}, {'label':pw_label,'tc':0,'ttl':253,'s':1}]   
                                               
            pkt4 = simple_mpls_packet(pktlen=pkt_len + 8 - 4,
                                    eth_dst=tunnel_mac_da,
                                    eth_src=router_mac,
                                    mpls_type=0x8847,
                                    mpls_tags= mpls2,
                                    inner_frame = pkt3) 
                                    
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt4, [2])
            

        finally:
        
            sys_logging("clear configuration") 

            #pdb.set_trace()

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
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)





class scenario_29_ether_vlan_sender_and_reflector_coexist(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)

        sys_logging(" npm session info ")

        encap_type = SAI_NPM_ENCAPSULATION_TYPE_ETHER_VLAN
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port_list[1])
        test_port_oid = bport_oid
        receive_port_oid = [port_list[2],port_list[3]]
        src_mac = '00:00:00:00:00:01'
        dst_mac = '00:00:00:00:00:02'
        outer_vlanid = 100
        inner_vlan_id = 0
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '1.2.3.4' 
        dst_ip = '5.6.7.8' 
        udp_src_port = 1234 
        udp_dst_port = 5678
        ttl = 100
        tc = 0 
        enable_transmit = 0 
        vrf_oid = 0
        hw_lookup = 1
        pkt_len = 100
        tx_rate = 100
        tx_mode = SAI_NPM_PKT_TX_MODE_PACKET_NUM
        tx_period = None
        tx_pkt_cnt = 1
        tx_pkt_duration =None

             
        sys_logging(" step 1 basic data environment")

        vlan_id = outer_vlanid
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[1], SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[2], SAI_VLAN_TAGGING_MODE_TAGGED)
 
        
        try:

            sys_logging(" step 2 create npm session on sender ")
            
            npm_session_oid = sai_thrift_create_npm_session_sender(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, ttl, tc, enable_transmit, vrf_oid, hw_lookup, pkt_len, tx_rate , tx_mode, tx_period, tx_pkt_cnt, tx_pkt_duration)
            sys_logging("### npm session oid is = %d###" %npm_session_oid)
            assert (npm_session_oid != SAI_NULL_OBJECT_ID)

            sys_logging(" step 3 create npm session reflector ")
        
            npm_session_oid_2 = sai_thrift_create_npm_session_reflector(self.client, encap_type, test_port_oid, receive_port_oid, src_mac, dst_mac, outer_vlanid, inner_vlan_id, addr_family, src_ip, dst_ip, udp_src_port, udp_dst_port, tc, vrf_oid, hw_lookup)
            sys_logging("### npm session oid is = %d###" %npm_session_oid_2)
            assert (npm_session_oid_2 != SAI_NULL_OBJECT_ID)

            warmboot(self.client)
            
            sys_logging(" step 4 enable npm session send packet ")            
            enable_transmit = 1
            attr_value = sai_thrift_attribute_value_t(booldata=enable_transmit)
            attr = sai_thrift_attribute_t(id=SAI_NPM_SESSION_ATTR_SESSION_ENABLE_TRANSMIT, value=attr_value)
            status = self.client.sai_thrift_set_npm_attribute(npm_session_oid, attr)

            sys_logging(" step 5 check npm tx packet ") 

            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')

            npm_test_pkt = Sequence_Number + Timestamp


            tx_pkt = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=outer_vlanid,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            self.ctc_show_packet_twamp(2,str(tx_pkt))             

            sys_logging(" step 6 check npm rx packet ") 
           
            Sequence_Number = hexstr_to_ascii('00000000')
            Timestamp = hexstr_to_ascii('0000000000445678')
            
            npm_test_pkt = Sequence_Number + Timestamp
            
            rx_pkt = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=src_mac,
                                    eth_src=dst_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=outer_vlanid,
                                    ip_src=dst_ip,
                                    ip_dst=src_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_dst_port,
                                    udp_dport=udp_src_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

        
            self.ctc_send_packet( 2, str(rx_pkt))
            
            sys_logging(" step 7 get npm session stats ")
            
            
            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 1)
            assert (list1[1] == 100)
            assert (list1[2] == 1)
            assert (list1[3] == 100)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)


            sys_logging(" step 8 clear npm session stats ")

            status = self.client.sai_thrift_clear_npm_session_stats(npm_session_oid, counter_ids, 8)
            sys_logging("###clear npm stats status = %d###" %status)          
            assert (status == SAI_STATUS_SUCCESS)  

            sys_logging(" step 9 get npm session stats again ")

            counter_ids = [SAI_NPM_SESSION_STATS_RX_PACKETS, SAI_NPM_SESSION_STATS_RX_BYTE, SAI_NPM_SESSION_STATS_TX_PACKETS, SAI_NPM_SESSION_STATS_TX_BYTE, SAI_NPM_SESSION_STATS_DROP_PACKETS,SAI_NPM_SESSION_STATS_MAX_LATENCY,SAI_NPM_SESSION_STATS_MIN_LATENCY,SAI_NPM_SESSION_STATS_AVG_LATENCY]
            
            list1 = self.client.sai_thrift_get_npm_session_stats(npm_session_oid, counter_ids, 8) 
            
            sys_logging("###list1[0]= %d###" %list1[0])
            sys_logging("###list1[1]= %d###" %list1[1])
            sys_logging("###list1[2]= %d###" %list1[2])
            sys_logging("###list1[3]= %d###" %list1[3])
            sys_logging("###list1[4]= %d###" %list1[4])
            sys_logging("###list1[5]= %d###" %list1[5])
            sys_logging("###list1[6]= %d###" %list1[6])
            sys_logging("###list1[7]= %d###" %list1[7])
            
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)
            assert (list1[4] == 0)
            assert (list1[5] == 0)
            assert (list1[6] == 0)
            assert (list1[7] == 0)


            sys_logging(" step 10 send packet and check reflector swap packet ")

            self.ctc_send_packet(2, str(tx_pkt))
            self.ctc_verify_packets( str(rx_pkt), [2], 1)

            
        finally:
        
            sys_logging("step 11 clear configuration")
            #pdb.set_trace()
            status = self.client.sai_thrift_remove_npm_session(npm_session_oid) 
            sys_logging("###remove session status  = %d###" %status)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  



















