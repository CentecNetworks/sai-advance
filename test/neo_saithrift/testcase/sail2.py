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
Thrift SAI interface L2 tests
"""
import socket
from switch import *
import sai_base_test
import pdb
import time
from scapy.config import *
from scapy.layers.all import *

@group('l2')
class L2AccessToAccessVlanTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        sys_logging ("Sending L2 packet port 1 -> port 2 [access vlan=10])")
        switch_init(self.client)
        vlan_id = 11
        port1 = port_list[0]
        port2 = port_list[1]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
         
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        
        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('l2')
class L2TrunkToTrunkVlanTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        sys_logging ("Sending L2 packet - port 1 -> port 2 [trunk vlan=10])")
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64)

        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(exp_pkt), [1], 1)
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('l2')
class L2TrunkToTrunkVlanTest1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        sys_logging ("Sending L2 packet - port 1 -> port 2 [trunk vlan=10])")
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64)

        try:       
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(exp_pkt), [1], 1)
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)



@group('l2')
class L2AccessToTrunkVlanTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        sys_logging ("Sending L2 packet - port 1 -> port 2 [trunk vlan=10])")
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)

        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(exp_pkt), [1], 1)
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('l2')
class L2TrunkToAccessVlanTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        sys_logging ("Sending L2 packet - port 1 -> port 2 [trunk vlan=10])")
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=96)
        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(exp_pkt), [1], 1)
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)

            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('l2')
class L2FloodTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        sys_logging ('Flood test on ports 1, 2 and 3')
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=107,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=107,
                                ip_ttl=64)

        try:          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets(str(exp_pkt), [1, 2], 1)
            
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('l2')
@group('lag')
class L2LagTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]
        is_lag = True
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        lag_id1 = sai_thrift_create_lag(self.client, [])
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        sys_logging ("lag:%u" %lag_id1)
        sys_logging ("lag:%lu" %lag_id1)
        sys_logging ("lag:%lx" %lag_id1)
        sys_logging ("lag:%x" %lag_id1)


        """sai_thrift_vlan_remove_all_ports(self.client, switch.default_vlan.oid)"""
        sys_logging ("port:%lx" %port1)
        sys_logging ("lag_id1:%lx" %lag_id1)
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
        # Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
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
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt], [0, 1, 2])
                count[rcv_idx] += 1
                dst_ip += 1

            sys_logging ("count = %s " %count)
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
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
            sys_logging ("Sending packet port 1 (lag member) -> port 4")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            sys_logging ("Sending packet port 2 (lag member) -> port 4")
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            sys_logging ("Sending packet port 3 (lag member) -> port 4")
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
        finally:

            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
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
@group('sonic')
class L2VlanBcastUcastTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        For SONiC
        Vlan broadcast and known unicast test. Verify the broacast packet reaches all ports in the vlan and unicast packet reach specific port. 
        Steps:
        1. remove all ports from default vlan
        2. create vlan 10
        3. add n-1 ports to vlan 10
        4. add mac for each port
        5. send untagged broadcast packet from port 1, verify all n-1 ports receive the packet except the last port
        6. send untagged unicast packets from port 1 to the rest of the vlan members ports. Verify only one port at a time receives the packet and port n does not.
        7. clean up.
        """

        switch_init(self.client)
        vlan_id = 10
        mac_list = []
        vlan_member_list = []
        ingress_port = 0

        for i in range (1, len(port_list)):
            mac_list.append("00:00:00:00:00:%02x" %(i+1))
        mac_action = SAI_PACKET_ACTION_FORWARD
        sys_logging ("===========port_list=======")
        sys_logging ("port_list = %s" %port_list)
        sys_logging ("len(port_list) = %d" %len(port_list))

        sai_thrift_vlan_remove_all_ports(self.client, switch.default_vlan.oid)

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        for i in range (0, len(port_list)-1):
            vlan_member_list.append(sai_thrift_create_vlan_member(self.client, vlan_oid, port_list[i], SAI_VLAN_TAGGING_MODE_UNTAGGED))

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        for i in range (0, len(port_list)-1):
            self.client.sai_thrift_set_port_attribute(port_list[i], attr)
            sai_thrift_create_fdb(self.client, vlan_oid, mac_list[i], port_list[i], mac_action)

        bcast_pkt = simple_tcp_packet(eth_dst='ff:ff:ff:ff:ff:ff',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        try:
            expected_ports = []
            for i in range (1, len(port_list)-1):
                expected_ports.append(i)

            self.ctc_send_packet(ingress_port, str(bcast_pkt))
            self.ctc_verify_packets(bcast_pkt, expected_ports)

            for i in range (1, len(port_list)-1):
                ucast_pkt = simple_tcp_packet(eth_dst=mac_list[i],
                                    eth_src='00:00:00:00:00:01',
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)
                self.ctc_send_packet(ingress_port, str(ucast_pkt))
                self.ctc_verify_packets(ucast_pkt, [i])

        finally:
            attr_value = sai_thrift_attribute_value_t(u16=switch.default_vlan.vid)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)

            for i in range (0, len(port_list)-1):
                sai_thrift_delete_fdb(self.client, vlan_oid, mac_list[i], port_list[i])
                self.client.sai_thrift_set_port_attribute(port_list[i], attr)

            for vlan_member in vlan_member_list:
                self.client.sai_thrift_remove_vlan_member(vlan_member)

            self.client.sai_thrift_remove_vlan(vlan_oid)

            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)

@group('l2')
class L2FdbAgingTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        sys_logging ("PTF L2 FDB aging test ...")
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        fdb_aging_time = 10

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        attr_value = sai_thrift_attribute_value_t(u32=fdb_aging_time)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_AGING_TIME, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        pkt1 = simple_tcp_packet(eth_dst=mac1,
                                 eth_src=mac2,
                                 ip_dst='10.0.0.1',
                                 ip_id=101,
                                 ip_ttl=64)

        try:
            sys_logging ("Send packet from port1 to port2 and verify on each of ports")
            sys_logging ('#### Sending 00:11:11:11:11:11| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1 ####')
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [pkt, pkt], [1, 2])
            sys_logging ("Send packet from port2 to port1 and verify only on port1")
            sys_logging ('#### Sending 00:22:22:22:22:22| 00:11:11:11:11:11 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2 ####')
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( pkt1, [0])
            sys_logging ("Wait when the aging time for FDB entries in the FDB table expires, and the entries are removed ...")
            time.sleep(fdb_aging_time*2 + 2)
            sys_logging ("Send packet from port2 to port1 and verify on each of ports")
            sys_logging ('#### Sending 00:22:22:22:22:22| 00:11:11:11:11:11 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2 ####')
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [pkt1, pkt1], [0, 2])
        finally:
            sys_logging ('#### flush fdb by vlan###')
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_AGING_TIME, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            sys_logging ("##aging test end###")

@group('l2')
class L2ARPRequestReplyFDBLearningTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid, v4_enabled, v6_enabled, router_mac)

        try:
            # send the test packet(s)
            sys_logging ("Send ARP request packet from port1 ...")
            arp_req_pkt = simple_arp_packet(eth_dst='ff:ff:ff:ff:ff:ff',
                                            eth_src='00:11:11:11:11:11',
                                            vlan_vid=10,
                                            arp_op=1, #ARP request
                                            ip_snd='10.10.10.1',
                                            ip_tgt='10.10.10.2',
                                            hw_snd='00:11:11:11:11:11')

            self.ctc_send_packet( 0, str(arp_req_pkt))

            time.sleep(1)
            sys_logging ("Send ARP reply packet from port2 ...")
            arp_rpl_pkt = simple_arp_packet(eth_dst=router_mac,
                                            eth_src='00:11:22:33:44:55',
                                            vlan_vid=10,
                                            arp_op=2, #ARP reply
                                            ip_snd='10.10.10.2',
                                            ip_tgt='10.10.10.1',
                                            hw_snd=router_mac,
                                            hw_tgt='00:11:22:33:44:55')

            self.ctc_send_packet( 1, str(arp_rpl_pkt))

            pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                    eth_src='00:11:22:33:44:55',
                                    ip_dst='10.10.10.1',
                                    ip_id=101,
                                    ip_ttl=64)

            time.sleep(1)
            sys_logging ("Send packet from port2 to port1 and verify only on port1 (src_mac and dst_mac addresses are learned)")
            sys_logging ('#### Sending 00:11:11:11:11:11 | 00:11:22:33:44:55 | 10.10.10.1 | 10.10.10.2 | @ ptf_intf 2 ####')
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( pkt, [0])

        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_id)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('l2')
@group('1D')
class L2BridgeSubPortFloodTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 15
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'

        sai_thrift_vlan_remove_all_ports(self.client, switch.default_vlan.oid)

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        bport2_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        bport3_id = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id2, vlan_id1)
        bport4_id = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id2, vlan_id2)

        pkt1 = simple_tcp_packet(eth_dst=mac1,
                                eth_src=mac2,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)

        pkt2 = simple_tcp_packet(eth_dst=mac1,
                                 eth_src=mac2,
                                 ip_dst='10.0.0.1',
                                 ip_id=102,
                                 ip_ttl=64,
                                 dl_vlan_enable=True,
                                 vlan_vid=vlan_id2)

        try:
            sys_logging ("Sending packet to Sub-port [port 1 : vlan {}] (bridge 1)".format(vlan_id1))
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt2, [1])
            sys_logging ("Success")
            sys_logging ("Sending packet to Sub-port [port 3 : vlan {}] (bridge 2)".format(vlan_id1))
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( pkt2, [3])
            sys_logging ("Success")

        finally:
            status = sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)    
            status = sai_thrift_flush_fdb_by_vlan(self.client, bridge_id2)              
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port1)
            sai_thrift_remove_bridge_sub_port(self.client, bport2_id, port2)
            sai_thrift_remove_bridge_sub_port(self.client, bport3_id, port3)
            sai_thrift_remove_bridge_sub_port(self.client, bport4_id, port4)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)

@group('l2')
@group('1D')
class L2BridgeSubPortFDBTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'

        sai_thrift_vlan_remove_all_ports(self.client, switch.default_vlan.oid)

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        bport2_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id)
        bport3_id = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan_id)

        sai_thrift_create_fdb_bport(self.client, bridge_id, mac3, bport3_id, SAI_PACKET_ACTION_FORWARD)

        pkt1 = simple_tcp_packet(eth_dst=mac1,
                                 eth_src=mac2,
                                 ip_dst='10.0.0.1',
                                 ip_id=102,
                                 ip_ttl=64,
                                 dl_vlan_enable=True,
                                 vlan_vid=vlan_id)

        pkt2 = simple_tcp_packet(eth_dst=mac2,
                                 eth_src=mac1,
                                 ip_dst='10.0.0.2',
                                 ip_id=102,
                                 ip_ttl=64,
                                 dl_vlan_enable=True,
                                 vlan_vid=vlan_id)

        pkt3 = simple_tcp_packet(eth_dst=mac3,
                                 eth_src=mac1,
                                 ip_dst='10.0.0.3',
                                 ip_id=102,
                                 ip_ttl=64,
                                 dl_vlan_enable=True,
                                 vlan_vid=vlan_id)

        try:
            sys_logging ("Sending unknown UC [{} -> {}] to port 1".format(mac2, mac1))
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt1, [1, 2])
            sys_logging ("Success")

            sys_logging ("Sending packet [{} -> {}] to port 2 (forwarded via dynamic FDB entry)".format(mac1, mac2))
            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_verify_packets( pkt2, [0])
            sys_logging ("Success")

            sys_logging ("Sending packet [{} -> {}] to port 1 (forwarded via static FDB entry)".format(mac1, mac3))
            self.ctc_send_packet( 0, str(pkt3))
            self.ctc_verify_packets( pkt3, [2])
            sys_logging ("Success")
        finally:
            status = sai_thrift_flush_fdb_by_vlan(self.client, bridge_id) 
            sai_thrift_delete_fdb(self.client, bridge_id, mac3, bport3_id)
            sai_thrift_remove_bridge_sub_port(self.client, bport1_id, port1)
            sai_thrift_remove_bridge_sub_port(self.client, bport2_id, port2)
            sai_thrift_remove_bridge_sub_port(self.client, bport3_id, port3)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)

            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)

