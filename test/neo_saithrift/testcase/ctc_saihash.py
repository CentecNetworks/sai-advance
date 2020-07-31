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
Thrift SAI interface Mirror tests
"""
import socket
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask

@group('hash')

class HashCreateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Hash Create Test. Verify that Hash is not support create. 
        Steps:
        1. Create Hash.
        2. get attribute and check
        3. clean up.
        """
        print ""
        switch_init(self.client)
        port3 = port_list[3]
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP]
        udf_group_list = [123,456]
        
        # create hash
        print "Create Hash "
        hash_id = sai_thrift_create_hash(self.client, field_list, udf_group_list)
        print "hash_id = %d" %hash_id
        
        warmboot(self.client)
        try:
            print "Check create hash, not support create hash"
            assert (hash_id == 0)
        finally:
            print "Success!"
            
class HashRemoveTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Hash Remove Test. 
        Steps:
        1. create Hash, not support
        2. remove Hash, not support
        3. get attribute and check
        5. clean up.
        """
        print ""
        switch_init(self.client)
        port3 = port_list[3]
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP]
        udf_group_list = [123,456]
        
        # create hash
        print "Create Hash "
        hash_id = sai_thrift_create_hash(self.client, field_list, udf_group_list)
        print "sai_thrift_create_hash; hash_id = %d" %hash_id
        
        # remove hash
        print "Remove Hash"
        status=self.client.sai_thrift_remove_hash(hash_id)
        print "sai_thrift_remove_hash; status = %d" %status
        assert (status == SAI_STATUS_NOT_SUPPORTED)
        
        warmboot(self.client)
        try:
            print "Check create hash, not support create hash"
            assert (hash_id == 0)
        finally:
            print "Success!"
   
@group('l2')
@group('lag')
class HashL2LagDefaultTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0x201C
        hash_id_ecmp = 0x1C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        lag_id1 = sai_thrift_create_lag(self.client, [])
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%u" %lag_id1
        print"lag:%lu" %lag_id1
        print"lag:%lx" %lag_id1
        print"lag:%x" %lag_id1


        """sai_thrift_vlan_remove_all_ports(self.client, switch.default_vlan.oid)"""
        print "port:%lx" %port1
        print "lag_id1:%lx" %lag_id1
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)
        
        # set lag hash: hash field default value to  ip_da
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            # src_mac how to write
            max_itrs = 20
            #src_mac_start = '00:22:22:22:{0}:{1}'
            src_mac_start = '00:22:22:22:22:{0}'
            for i in range(0, max_itrs):
                #src_mac = src_mac_start.format(str(i).zfill(4)[:2], str(i).zfill(4)[2:])
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"count:####################################"
            print count
            for i in range(0, 3):
                #self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)           
           
@group('l2')
@group('lag')
class HashL2LagSetTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0x201C
        hash_id_ecmp = 0x1C
        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_bridged = True
        is_lag = True
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        lag_id1 = sai_thrift_create_lag(self.client, [])
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%u" %lag_id1
        print"lag:%lu" %lag_id1
        print"lag:%lx" %lag_id1
        print"lag:%x" %lag_id1
        print"lag_oid:%lx" %lag_oid1


        """sai_thrift_vlan_remove_all_ports(self.client, switch.default_vlan.oid)"""
        print "port:%lx" %port1
        print "lag_id1:%lx" %lag_id1
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)
        
        # set lag hash: hash field default value to  ip_da
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            dst_ip = int(socket.inet_aton('10.10.10.1').encode('hex'),16)
            max_itrs = 20
            for i in range(0, max_itrs):
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst=dst_ip_addr,
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst=dst_ip_addr,
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                count[rcv_idx] += 1
                dst_ip += 1

            print count
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
            
        finally:
            sai_thrift_flush_fdb_by_bridge_port(self.client, lag_oid1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr)  

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)           

class HashL3IPv4EcmpHostTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print "Sending packet port 1 -> port 2 (192.168.0.1 -> 10.10.10.1 [id = 101])"
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_lag = 0x201C
        hash_id_ecmp = 0x1C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP]

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'

        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)

        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)

        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
        
       ## set lag hash: hash field default value to  ip_sa
       ##Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
       
       # send the test packet(s)
        warmboot(self.client)
        try:
        # step1
            pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=64)

            exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                #ip_tos=3,
                                ip_ttl=63)
            exp_pkt2 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:56',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                #ip_tos=3,
                                ip_ttl=63)

            self.ctc_send_packet( 2, str(pkt))
            #self.ctc_verify_any_packet_any_port( [exp_pkt1, exp_pkt2], [0, 1])
            self.ctc_verify_packets( exp_pkt1, [0])

            # step2
            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)
            
            exp_pkt1 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:55',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    #ip_tos=3,
                                    ip_ttl=63)
            exp_pkt2 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:56',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    #ip_tos=3,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 2, str(pkt))
            #self.ctc_verify_any_packet_any_port( [exp_pkt1, exp_pkt2], [0, 1])
            self.ctc_verify_packets( exp_pkt2, [1])
            
            ## step3
            count = [0, 0]
            src_ip = int(socket.inet_aton('192.168.100.3').encode('hex'),16)
            max_itrs = 20
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.3',
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=64)
            
                exp_pkt1 = simple_tcp_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.3',
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        #ip_tos=3,
                                        ip_ttl=63)
                exp_pkt2 = simple_tcp_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.3',
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        #ip_tos=3,
                                        ip_ttl=63)
            
                self.ctc_send_packet( 2, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2], [0, 1])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx
                src_ip += 1
            
            print count
            for i in range(0, 2):
                self.assertTrue((count[i] >= ((max_itrs / 2) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:

            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)         

class HashMPLSUseLabelECMPSetTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        # create LAG use MPLS Label Stack
        hash_id_lag = 0x201C
        hash_id_ecmp = 0x1C
        field_list = [SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK]

        # set lag hash: hash field default value to  ip_sa
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_mask = '255.255.255.0'   
        ip_da_SWA = '2.2.2.1'
        dmac_SWA = '00:11:11:11:11:11'
        ip_da_SWC = '4.4.4.1'
        dmac_SWC = '00:44:44:44:44:44'
        ip_da_SWD = '3.3.3.1'
        dmac_SWD = '00:33:33:33:33:33'
        
        # create neighbor entries
        # SW_A_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWA, dmac_SWA)
        # SW_D_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da_SWD, dmac_SWD)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da_SWD, dmac_SWD)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id5, ip_da_SWD, dmac_SWD)   
        
        # net hop from SW B via SW A to 1.1.1.0/24   
        # label 100
        label_list1 = [413503]
        # label 50
        label_list2 = [208703]

        #SW_D_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list1)               
        #SW_D_2_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list2)

        nhop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list2)
        nhop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id3, label_list2)
        nhop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id4, label_list2)
        nhop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id5, label_list2)
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)
        nhop_gmember4 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop4)


        # MPLS in segment enrty (egress LER)
        label1 = 200
        pop_nums = 1
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, nhop_group1, None)          
        label2 = 300
        pop_nums = 1
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, nhop_group1, None)
        label3 = 400
        pop_nums = 1
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, nhop_group1, None)
        label4 = 500
        pop_nums = 1
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, nhop_group1, None)
        count = [0, 0, 0, 0, 0]
        # send the test packet(s) with label 200
        mpls1 = [{'label':200,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
         
        exp_mpls1 = [{'label':100,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls1,
                                inner_frame = exp_ip_only_pkt1) 
                                
        # send the test packet(s) with label 300
        mpls2 = [{'label':300,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2) 
         
        exp_mpls2 = [{'label':50,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt2 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls2,
                                inner_frame = exp_ip_only_pkt2) 
                                
        # send the test packet(s) with label 400
        mpls3 = [{'label':400,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt3 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls3,
                                inner_frame = ip_only_pkt3) 
         
        # send the test packet(s) with label 500
        mpls4 = [{'label':500,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt4 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt4 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls4,
                                inner_frame = ip_only_pkt4) 
         
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt1))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt2))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt3))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt4))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2], [1, 2, 3, 4])
            count[rcv_idx] += 1
            print"*********************** rcv_idx:%d" %rcv_idx
            print count
            for i in range(1, 5):
                print"*****************************i:%d" %i
                print"*****************************count:%d" %count[i]
                self.assertTrue((count[i] != 4),
                        "Not all paths are equally balanced by MPLS Label stack")
        finally:
            label = 200
            mpls = sai_thrift_inseg_entry_t(label)   
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            label = 300
            mpls = sai_thrift_inseg_entry_t(label)  
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            label = 400
            mpls = sai_thrift_inseg_entry_t(label)   
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            label = 500
            mpls = sai_thrift_inseg_entry_t(label)  
            self.client.sai_thrift_remove_inseg_entry(mpls)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember4)      
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            self.client.sai_thrift_remove_next_hop(nhop4)
            
            # SW_A_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWA, dmac_SWA)
            # SW_D_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da_SWD, dmac_SWD)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id4, ip_da_SWD, dmac_SWD)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id5, ip_da_SWD, dmac_SWD)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
            
class HashMPLSUseLabelAndInnerHeaderECMPSetTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        # create LAG use MPLS Label Stack
        hash_id_lag = 0x201C
        hash_id_ecmp = 0x1C
        field_list = [SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK, SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC, SAI_NATIVE_HASH_FIELD_INNER_DST_MAC, SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP]
        #field_list = [SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK]

        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port5, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_mask = '255.255.255.0'   
        ip_da_SWA = '2.2.2.1'
        dmac_SWA = '00:11:11:11:11:11'
        ip_da_SWC = '4.4.4.1'
        dmac_SWC = '00:44:44:44:44:44'
        ip_da_SWD = '3.3.3.1'
        dmac_SWD = '00:33:33:33:33:33'
        
        # create neighbor entries
        # SW_A_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWA, dmac_SWA)
        # SW_D_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da_SWD, dmac_SWD) 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_da_SWD, dmac_SWD) 
        sai_thrift_create_neighbor(self.client, addr_family, rif_id5, ip_da_SWD, dmac_SWD)         
        
        # net hop from SW B via SW A to 1.1.1.0/24   
        # label 100
        label_list1 = [413503]
        # label 50
        label_list2 = [208703]
        #SW_D_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list1)               
        #SW_D_2_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list2)   
        nhop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list2)
        nhop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id3, label_list2)
        nhop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id4, label_list2)
        nhop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id5, label_list2)
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)
        nhop_gmember4 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop4)


        # MPLS in segment enrty (egress LER)
        label1 = 200
        pop_nums = 1
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, nhop_group1, None)          
        label2 = 300
        pop_nums = 1
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, nhop_group1, None)
        
        count = [0, 0, 0, 0, 0]
        # send the test packet(s) with label 200 inner SRC IP 192.168.0.1
        mpls1 = [{'label':200,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
         
        exp_mpls1 = [{'label':50,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls1,
                                inner_frame = exp_ip_only_pkt1) 

        # send the test packet(s) with label 200 inner SRC IP 192.168.0.2
        mpls2 = [{'label':200,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.2',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2) 
         
        exp_mpls2 = [{'label':50,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.2',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt2 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls2,
                                inner_frame = exp_ip_only_pkt2)
        
        # send the test packet(s) with label 300 innner SRC IP 192.168.0.1
        mpls3 = [{'label':300,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt3 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls3,
                                inner_frame = ip_only_pkt3) 
         
        exp_mpls3 = [{'label':50,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt3 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt3 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls3,
                                inner_frame = exp_ip_only_pkt3) 
                                
        # send the test packet(s) with label 300 innner SRC IP 192.168.0.2
        mpls4 = [{'label':300,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt4 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.2',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt4 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls4,
                                inner_frame = ip_only_pkt4) 
         
        exp_mpls4 = [{'label':50,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt4 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.2',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt4 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls4,
                                inner_frame = exp_ip_only_pkt4) 
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt1))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3,exp_pkt4], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt2))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3,exp_pkt4], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt3))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3,exp_pkt4], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt4))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3,exp_pkt4], [1, 2, 3, 4])
            count[rcv_idx] += 1
            print"*********************** rcv_idx:%d" %rcv_idx
            print count
            for i in range(1, 5):
                print"*****************************i:%d" %i
                print"*****************************count:%d" %count[i]
                self.assertTrue((count[i] != 4),
                        "Not all paths are equally balanced by MPLS Label stack")
        finally:
            label = 200
            mpls = sai_thrift_inseg_entry_t(label)   
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            label = 300
            mpls = sai_thrift_inseg_entry_t(label)  
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember4)      
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            self.client.sai_thrift_remove_next_hop(nhop4)
            
            # SW_A_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWA, dmac_SWA)
            # SW_D_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da_SWD, dmac_SWD)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id4, ip_da_SWD, dmac_SWD)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id5, ip_da_SWD, dmac_SWD)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

@group('mpls')
@group('lag')
class MPLSLagSetModeTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        # create LAG
        is_bridged = True
        lag_mode = SAI_LAG_MODE_RR
        #lag_id1 = sai_thrift_create_lag(self.client, [], lag_mode)
        lag_id1 = sai_thrift_create_lag(self.client, [])
        print"lag:%u" %lag_id1
        print"lag:%lu" %lag_id1
        print"lag:%lx" %lag_id1
        print"lag:%x" %lag_id1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port4)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id1, port5)

        # set lag hash: hash field default value to  ip_sa
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_mask = '255.255.255.0'   
        ip_da_SWA = '2.2.2.1'
        dmac_SWA = '00:11:11:11:11:11'
        ip_da_SWC = '4.4.4.1'
        dmac_SWC = '00:44:44:44:44:44'
        ip_da_SWD = '3.3.3.1'
        dmac_SWD = '00:33:33:33:33:33'
        
        # create neighbor entries
        # SW_A_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWA, dmac_SWA)
        # SW_D_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)        
        
        # net hop from SW B via SW A to 1.1.1.0/24   
        # label 100
        label_list1 = [413503]

        SW_D_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list1)               
        # MPLS in segment enrty (egress LER)
        label1 = 200
        pop_nums = 1
        nhop1 = SW_D_1_next_hop
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, nhop1, None)          
        count = [0, 0, 0, 0, 0]
        # send the test packet(s) with label 200
        mpls1 = [{'label':200,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
         
        exp_mpls1 = [{'label':100,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls1,
                                inner_frame = exp_ip_only_pkt1) 
         
        warmboot(self.client)
        try:
            for m in range(1, 5):
                self.ctc_send_packet( 0, str(pkt1))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1], [1, 2, 3, 4])
                count[rcv_idx] += 1

            for i in range(1, 5):
                print"*****************************i:%d" %i
                print"*****************************count:%d" %count[i]
                self.assertTrue((count[i] == 1),
                        "Not all paths are equally balanced by MPLS Label stack")
        finally:
            label = 200
            mpls = sai_thrift_inseg_entry_t(label)   
            self.client.sai_thrift_remove_inseg_entry(mpls)  

            self.client.sai_thrift_remove_next_hop(SW_D_1_next_hop)
            
            # SW_A_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWA, dmac_SWA)
            # SW_D_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            sai_thrift_remove_lag(self.client, lag_id1)
            

class HashMPLSUseLabelLagSetTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        # create LAG use MPLS Label Stack
        hash_id_lag = 0x201C
        hash_id_ecmp = 0x1C
        field_list = [SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK]

        lag_id1 = sai_thrift_create_lag(self.client, [])
        print"lag:%u" %lag_id1
        print"lag:%lu" %lag_id1
        print"lag:%lx" %lag_id1
        print"lag:%x" %lag_id1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port4)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id1, port5)

        # set lag hash: hash field default value to  ip_sa
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_mask = '255.255.255.0'   
        ip_da_SWA = '2.2.2.1'
        dmac_SWA = '00:11:11:11:11:11'
        ip_da_SWC = '4.4.4.1'
        dmac_SWC = '00:44:44:44:44:44'
        ip_da_SWD = '3.3.3.1'
        dmac_SWD = '00:33:33:33:33:33'
        
        # create neighbor entries
        # SW_A_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWA, dmac_SWA)
        # SW_D_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)        
        
        # net hop from SW B via SW A to 1.1.1.0/24   
        # label 100
        label_list1 = [413503]
        # label 50
        label_list2 = [208703]

        SW_D_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list1)               
        SW_D_2_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list2)    
        # MPLS in segment enrty (egress LER)
        label1 = 200
        pop_nums = 1
        nhop1 = SW_D_1_next_hop
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, nhop1, None)          
        label2 = 300
        pop_nums = 1
        nhop2 = SW_D_2_next_hop
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, nhop2, None)
        label3 = 400
        pop_nums = 1
        nhop3 = SW_D_2_next_hop
        sai_thrift_create_inseg_entry(self.client, label3, pop_nums, None, nhop3, None)
        label4 = 500
        pop_nums = 1
        nhop4 = SW_D_2_next_hop
        sai_thrift_create_inseg_entry(self.client, label4, pop_nums, None, nhop4, None)
        count = [0, 0, 0, 0, 0]
        # send the test packet(s) with label 200
        mpls1 = [{'label':200,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
         
        exp_mpls1 = [{'label':100,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls1,
                                inner_frame = exp_ip_only_pkt1) 
                                
        # send the test packet(s) with label 300
        mpls2 = [{'label':300,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2) 
         
        exp_mpls2 = [{'label':50,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt2 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls2,
                                inner_frame = exp_ip_only_pkt2) 
                                
        # send the test packet(s) with label 400
        mpls3 = [{'label':400,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt3 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls3,
                                inner_frame = ip_only_pkt3) 
         
        # send the test packet(s) with label 500
        mpls4 = [{'label':500,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt4 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt4 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls4,
                                inner_frame = ip_only_pkt4) 
         
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt1))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt2))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt3))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt4))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2], [1, 2, 3, 4])
            count[rcv_idx] += 1
            print"*********************** rcv_idx:%d" %rcv_idx
            print count
            for i in range(1, 5):
                print"*****************************i:%d" %i
                print"*****************************count:%d" %count[i]
                self.assertTrue((count[i] != 4),
                        "Not all paths are equally balanced by MPLS Label stack")
        finally:
            label = 200
            mpls = sai_thrift_inseg_entry_t(label)   
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            label = 300
            mpls = sai_thrift_inseg_entry_t(label)  
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            label = 400
            mpls = sai_thrift_inseg_entry_t(label)   
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            label = 500
            mpls = sai_thrift_inseg_entry_t(label)  
            self.client.sai_thrift_remove_inseg_entry(mpls)

            self.client.sai_thrift_remove_next_hop(SW_D_2_next_hop)
            self.client.sai_thrift_remove_next_hop(SW_D_1_next_hop)
            
            # SW_A_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWA, dmac_SWA)
            # SW_D_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            sai_thrift_remove_lag(self.client, lag_id1)
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
            
class HashMPLSUseLabelAndInnerHeaderLagSetTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        # create LAG use MPLS Label Stack
        hash_id_lag = 0x201C
        hash_id_ecmp = 0x1C
        field_list = [SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK, SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC, SAI_NATIVE_HASH_FIELD_INNER_DST_MAC, SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP]
        #field_list = [SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK]
        lag_id1 = sai_thrift_create_lag(self.client, [])
        print"lag:%u" %lag_id1
        print"lag:%lu" %lag_id1
        print"lag:%lx" %lag_id1
        print"lag:%x" %lag_id1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port4)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id1, port5)

        # set lag hash: hash field default value to  ip_sa
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_mask = '255.255.255.0'   
        ip_da_SWA = '2.2.2.1'
        dmac_SWA = '00:11:11:11:11:11'
        ip_da_SWC = '4.4.4.1'
        dmac_SWC = '00:44:44:44:44:44'
        ip_da_SWD = '3.3.3.1'
        dmac_SWD = '00:33:33:33:33:33'
        
        # create neighbor entries
        # SW_A_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWA, dmac_SWA)
        # SW_D_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)        
        
        # net hop from SW B via SW A to 1.1.1.0/24   
        # label 100
        label_list1 = [413503]
        # label 50
        label_list2 = [208703]
        SW_D_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list1)               
        SW_D_2_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list2)    
        # MPLS in segment enrty (egress LER)
        label1 = 200
        pop_nums = 1
        nhop1 = SW_D_2_next_hop
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, nhop1, None)          
        label2 = 300
        pop_nums = 1
        nhop2 = SW_D_2_next_hop
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, nhop2, None)
        
        count = [0, 0, 0, 0, 0]
        # send the test packet(s) with label 200 inner SRC IP 192.168.0.1
        mpls1 = [{'label':200,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
         
        exp_mpls1 = [{'label':50,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls1,
                                inner_frame = exp_ip_only_pkt1) 

        # send the test packet(s) with label 200 inner SRC IP 192.168.0.2
        mpls2 = [{'label':200,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.2',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt2 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2) 
         
        exp_mpls2 = [{'label':50,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.2',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt2 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls2,
                                inner_frame = exp_ip_only_pkt2)
        
        # send the test packet(s) with label 300 innner SRC IP 192.168.0.1
        mpls3 = [{'label':300,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt3 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt3 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls3,
                                inner_frame = ip_only_pkt3) 
         
        exp_mpls3 = [{'label':50,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt3 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt3 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls3,
                                inner_frame = exp_ip_only_pkt3) 
                                
        # send the test packet(s) with label 300 innner SRC IP 192.168.0.2
        mpls4 = [{'label':300,'tc':3,'ttl':64,'s':1}]    
        ip_only_pkt4 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.2',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                
        pkt4 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWA,
                                mpls_type=0x8847,
                                mpls_tags= mpls4,
                                inner_frame = ip_only_pkt4) 
         
        exp_mpls4 = [{'label':50,'tc':7,'ttl':63,'s':1}]   
        exp_ip_only_pkt4 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.2',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ttl=63,
                                ip_id=0x0001
                                )  
        
        # something wrong; use mask to not care                                
        exp_pkt4 = simple_mpls_packet(
                                eth_dst=dmac_SWD,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls4,
                                inner_frame = exp_ip_only_pkt4) 
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt1))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3,exp_pkt4], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt2))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3,exp_pkt4], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt3))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3,exp_pkt4], [1, 2, 3, 4])
            count[rcv_idx] += 1
            self.ctc_send_packet( 0, str(pkt4))
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3,exp_pkt4], [1, 2, 3, 4])
            count[rcv_idx] += 1
            print"*********************** rcv_idx:%d" %rcv_idx
            print count
            for i in range(1, 5):
                print"*****************************i:%d" %i
                print"*****************************count:%d" %count[i]
                self.assertTrue((count[i] != 4),
                        "Not all paths are equally balanced by MPLS Label stack")
        finally:
            label = 200
            mpls = sai_thrift_inseg_entry_t(label)   
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            label = 300
            mpls = sai_thrift_inseg_entry_t(label)  
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            
            self.client.sai_thrift_remove_next_hop(SW_D_2_next_hop)
            self.client.sai_thrift_remove_next_hop(SW_D_1_next_hop)
            
            # SW_A_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWA, dmac_SWA)
            # SW_D_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            sai_thrift_remove_lag(self.client, lag_id1)
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class VpwsUseLabelLagTests(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        1.Set provider routing configuration
        2.Set provider mpls lsp configuration
        3.Set provider mpls pw configuration
        4.Set Provider mpls uni port configuration
        9.Send encap and decap traffic packet,check packet receiving
        10.Clear configuration
        11.Repeat 1-10 for 3 times
        """
        sys_logging("1.Set provider routing configuration")
        switch_init(self.client)
        provider_vlan_list = [100]
        provider_vlan_oid_list = [0 for i in range(1)]
        provider_vlan_member_oid_list = [0 for i in range(1)]
        for num in range(1):
            vlan_id = provider_vlan_list[num]
            vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
            provider_vlan_oid_list[num] = vlan_oid
            tmp_port = port_list[num]
            vlan_member = sai_thrift_create_vlan_member(self.client, vlan_oid, tmp_port, SAI_VLAN_TAGGING_MODE_TAGGED)
            provider_vlan_member_oid_list[num] = vlan_member
        v4_enabled = 1
        v6_enabled = 1
        default_vrf_oid = 0x0000000003
        mac=router_mac
        provider_rif_oid_list = [0 for i in range(1)]
        for num in range(1):
            tmp_vlan_oid = provider_vlan_oid_list[num]
            provider_rif_oid = sai_thrift_create_router_interface(self.client, default_vrf_oid, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, tmp_vlan_oid, v4_enabled, v6_enabled, mac)
            provider_rif_oid_list[num] = provider_rif_oid
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask_32 = '255.255.255.255'
        ip_mask_24 = '255.255.255.0'
        provider_rif_ip_addr_list = ['192.168.1.1']
        provider_nexthop_ip_addr_list = ['192.168.1.2']
        provider_nexthop_mac_list = ['00:11:22:33:44:01']
        provider_nhop_oid_list = [0 for i in range(1)]
        mac_action = SAI_PACKET_ACTION_FORWARD
        for num in range(1):
            provider_rif_oid = provider_rif_oid_list[num]
            nexthop_mac = provider_nexthop_mac_list[num]
            provider_rif_ip_addr = provider_rif_ip_addr_list[num]
            ret = sai_thrift_create_route(self.client, default_vrf_oid, addr_family, provider_rif_ip_addr, ip_mask_32, 0, SAI_PACKET_ACTION_TRAP)
            if (ret < 0):
                sys_logging(">>sai_thrift_create_route failed!!! ret = %d" % ret)
            nexthop_ip_addr = provider_nexthop_ip_addr_list[num]
            ret = sai_thrift_create_neighbor(self.client, addr_family, provider_rif_oid, nexthop_ip_addr, nexthop_mac)
            if (ret < 0):
                sys_logging(">>sai_thrift_create_neighbor failed!!! ret = %d" % ret)
            provider_nhop_oid = sai_thrift_create_nhop(self.client, addr_family, nexthop_ip_addr, provider_rif_oid)
            provider_nhop_oid_list[num] = provider_nhop_oid
            ret = sai_thrift_create_route(self.client, default_vrf_oid, addr_family, nexthop_ip_addr, ip_mask_32, provider_nhop_oid)
            if (ret < 0):
                sys_logging(">>sai_thrift_create_route failed!!! ret = %d" % ret)
            tmp_port = port_list[num]
            vlan_oid = provider_vlan_oid_list[num]
            sai_thrift_create_fdb(self.client, vlan_oid, nexthop_mac, tmp_port, mac_action)
        sys_logging("2.Set provider mpls lsp configuration")
        mpls_if_mac = ''
        mpls_rif_oid = sai_thrift_create_router_interface(self.client, default_vrf_oid, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac)
        
        nhp_lsp_label = 200
        nhp_lsp_label_for_nhp = (nhp_lsp_label<<12) | 64
        nhp_lsp_label_list = [nhp_lsp_label_for_nhp]
        nexthop_ip_addr = provider_nexthop_ip_addr_list[0]
        provider_rif_oid = provider_rif_oid_list[0]
        
        nhop_lsp_pe1_to_p = sai_thrift_create_mpls_nhop(self.client, addr_family, nexthop_ip_addr, provider_rif_oid, nhp_lsp_label_list)
        
        inseg_lsp_label = 100
        pop_nums = 1
        inseg_nhop_lsp = mpls_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        
        sai_thrift_create_inseg_entry(self.client, inseg_lsp_label, pop_nums, None, inseg_nhop_lsp, packet_action)
        
        sys_logging("3.Set provider mpls pw configuration")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)
        sys_logging(">>bridge_id = %d" % bridge_id)
        
        pw2_bridge_rif_oid = sai_thrift_create_router_interface(self.client, default_vrf_oid, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac, bridge_id)
        inseg_pw2_label = 102
        nhp_pw2_label = 202
        nhp_pw2_label_for_list = (nhp_pw2_label<<12) | 64
        
        label_list = [nhp_pw2_label_for_list]
        
        #tunnel_id_pw2 = sai_thrift_create_tunnel_mpls(self.client)
        tunnel_id_pw2 = sai_thrift_create_tunnel_mpls(self.client, SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL, SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, True, True, 0, 200)
        nhop_pw_pe1_to_pe2 = sai_thrift_create_tunnel_mpls_nhop(self.client, tunnel_id_pw2, label_list, nhop_lsp_pe1_to_p)
        pop_nums = 1 # cw add to tunnel
        inseg_nhop_pw2 = pw2_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        #pdb.set_trace()
        sai_thrift_create_inseg_entry(self.client, inseg_pw2_label, pop_nums, None, inseg_nhop_pw2, packet_action, tunnel_id_pw2)
        pw2_tunnel_bport_oid = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id_pw2, bridge_id, False)
        
        pw3_bridge_rif_oid = sai_thrift_create_router_interface(self.client, default_vrf_oid, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mpls_if_mac, bridge_id)
        inseg_pw3_label = 103
        nhp_pw3_label = 202
        nhp_pw3_label_for_list = (nhp_pw3_label<<12) | 64
        label_list = [nhp_pw3_label_for_list]
        tunnel_id_pw3 = sai_thrift_create_tunnel_mpls(self.client, SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL, SAI_TUNNEL_TTL_MODE_UNIFORM_MODEL, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, SAI_TUNNEL_MPLS_PW_MODE_TAGGED, True, True, 0, 300)
        nhop_pw_pe1_to_pe3 = sai_thrift_create_tunnel_mpls_nhop(self.client, tunnel_id_pw3, label_list, nhop_lsp_pe1_to_p)
        pop_nums = 1 # cw add to tunnel
        inseg_nhop_pw3 = pw3_bridge_rif_oid
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, inseg_pw3_label, pop_nums, None, inseg_nhop_pw3, packet_action, tunnel_id_pw3)
        pw3_tunnel_bport_oid = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id_pw3, bridge_id, False)
        
        inseg_pw_label_list=[inseg_pw2_label,inseg_pw3_label]
        sys_logging("4.Set Provider mpls uni port configuration")
        
        #Lag configuration
        hash_id_lag = 0x201C
        #pdb.set_trace()
        lag_id1 = sai_thrift_create_lag(self.client, [])
        sys_logging("4.Set Provider mpls uni port configuration")
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port_list[1])
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port_list[2])
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port_list[3])
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id1, port_list[4])

        #Hash configuration
        #field_list = [SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK, SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC, SAI_NATIVE_HASH_FIELD_INNER_DST_MAC, SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP]
        field_list = [SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        uni_vlan_id = 1001
        uni_port_oid = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, uni_vlan_id, False)
        print"*********************** uni_port_oid:%x" %uni_port_oid
        print"*********************** lag_id:%x" %lag_id1
        sys_logging("5.Set Port cross connect")
        mac_action = SAI_PACKET_ACTION_FORWARD

        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=pw2_tunnel_bport_oid)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(uni_port_oid, bport_attr_xcport)

        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=uni_port_oid)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(pw2_tunnel_bport_oid, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(uni_port_oid, bport_attr_xcport)
        self.client.sai_thrift_set_bridge_port_attribute(pw2_tunnel_bport_oid, bport_attr_xcport)


        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=pw3_tunnel_bport_oid)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        
        self.client.sai_thrift_set_bridge_port_attribute(uni_port_oid, bport_attr_xcport)

        bport_attr_xcport_value = sai_thrift_attribute_value_t(oid=uni_port_oid)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(pw3_tunnel_bport_oid, bport_attr_xcport)
        
        bport_attr_xcport_value = sai_thrift_attribute_value_t(booldata=True)
        bport_attr_xcport = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                                    value=bport_attr_xcport_value)
        self.client.sai_thrift_set_bridge_port_attribute(uni_port_oid, bport_attr_xcport)
        self.client.sai_thrift_set_bridge_port_attribute(pw3_tunnel_bport_oid, bport_attr_xcport)

        sys_logging("9.2 Send Vpws Packet and check Lag Hash, first list 0")
        inner_src_mac_list = ['00:88:88:99:01:01', '00:88:88:99:02:02']
        count = [0, 0, 0, 0, 0]
        pdb.set_trace()
        for num1 in range(2):
            uni_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst='00:88:88:88:01:01',
                                eth_src='00:88:88:99:01:01',
                                dl_vlan_enable=True,
                                vlan_vid=1001,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='1.1.1.102',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
            mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                eth_dst='00:88:88:88:01:01',
                                eth_src='00:88:88:99:01:01',
                                dl_vlan_enable=True,
                                vlan_vid=200,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst='1.1.1.1',
                                ip_src='1.1.1.102',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
            mpls_label_stack = [{'label':inseg_lsp_label,'tc':0,'ttl':64,'s':0},{'label':inseg_pw_label_list[num1],'tc':0,'ttl':64,'s':1},{'label':0,'tc':0,'ttl':0,'s':0}]
            pw_pkt = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:11:22:33:44:01',
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                vlan_pcp=0,
                                mpls_type=0x8847,
                                mpls_tags= mpls_label_stack,
                                inner_frame = mpls_inner_pkt)
        
            
            self.ctc_send_packet(0, str(pw_pkt))
            rcv_idx = self.ctc_verify_any_packet_any_port( uni_pkt, [1, 2, 3, 4])
            count[rcv_idx] += 1

        for i in range(5):
                print"*****************************i:%d" %i
                print"*****************************count:%d" %count[i]
                self.assertTrue((count[i] != 2),
                        "Not all paths are equally balanced by MPLS Label stack")

        sys_logging("10.Clear configuration")
        for num in range(2):
            uni_port=port_list[num+1]
            uni_port_oid = uni_port_oid_list[num]
            sai_thrift_remove_bridge_sub_port(self.client, uni_port_oid, uni_port)
        self.client.sai_thrift_remove_bridge_port(pw3_tunnel_bport_oid)
        inseg_entry = sai_thrift_inseg_entry_t(inseg_pw3_label) 
        self.client.sai_thrift_remove_inseg_entry(inseg_entry)
        self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe3)
        self.client.sai_thrift_remove_tunnel(tunnel_id_pw3)
        self.client.sai_thrift_remove_router_interface(pw3_bridge_rif_oid)
        self.client.sai_thrift_remove_bridge_port(pw2_tunnel_bport_oid)
        inseg_entry = sai_thrift_inseg_entry_t(inseg_pw2_label) 
        self.client.sai_thrift_remove_inseg_entry(inseg_entry)
        self.client.sai_thrift_remove_next_hop(nhop_pw_pe1_to_pe2)
        self.client.sai_thrift_remove_tunnel(tunnel_id_pw2)
        self.client.sai_thrift_remove_router_interface(pw2_bridge_rif_oid)
        self.client.sai_thrift_remove_bridge(bridge_id)
        inseg_entry = sai_thrift_inseg_entry_t(inseg_lsp_label) 
        self.client.sai_thrift_remove_inseg_entry(inseg_entry)
        self.client.sai_thrift_remove_next_hop(nhop_lsp_pe1_to_p)
        self.client.sai_thrift_remove_router_interface(mpls_rif_oid)
        for num in range(1):
            provider_rif_oid = provider_rif_oid_list[num]
            nexthop_mac = provider_nexthop_mac_list[num]
            provider_rif_ip_addr = provider_rif_ip_addr_list[num]
            provider_nhop_oid = provider_nhop_oid_list[num]
            tmp_port = port_list[num]
            vlan_oid = provider_vlan_oid_list[num]
            nexthop_ip_addr = provider_nexthop_ip_addr_list[num]
            self.client.sai_thrift_remove_next_hop(provider_nhop_oid)
            sai_thrift_delete_fdb(self.client, vlan_oid, nexthop_mac, tmp_port)
            ret = sai_thrift_remove_route(self.client, default_vrf_oid, addr_family, nexthop_ip_addr, ip_mask_32, provider_nhop_oid)
            if (ret < 0):
                sys_logging(">>sai_thrift_remove_route failed!!! ret = %d" % ret)
            sai_thrift_remove_neighbor(self.client, addr_family, provider_rif_oid, nexthop_ip_addr, nexthop_mac)
            ret = sai_thrift_remove_route(self.client, default_vrf_oid, addr_family, provider_rif_ip_addr, ip_mask_32, 0)
            if (ret < 0):
                sys_logging(">>sai_thrift_remove_route failed!!! ret = %d" % ret)
        for num in range(1):
            provider_rif_oid = provider_rif_oid_list[num]
            self.client.sai_thrift_remove_router_interface(provider_rif_oid)
        for num in range(1):
            vlan_oid = provider_vlan_oid_list[num]
            vlan_id = provider_vlan_list[num]
            sai_thrift_vlan_remove_all_ports(self.client, vlan_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid)
        
        sai_thrift_remove_lag_member(self.client, lag_member_id[0])
        sai_thrift_remove_lag_member(self.client, lag_member_id[1])
        sai_thrift_remove_lag_member(self.client, lag_member_id[2])
        sai_thrift_remove_lag_member(self.client, lag_member_id[3])
        sai_thrift_remove_lag(self.client, lag_id1)
        
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
