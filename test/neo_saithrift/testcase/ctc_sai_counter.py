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
Thrift SAI interface Counter tests
"""
import socket
from switch import *
import sai_base_test
from ptf.mask import Mask
import pdb

@group('counter')    

class CounterCreateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        
        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            
            for a in attrs.attr_list:
                if a.id == SAI_COUNTER_ATTR_TYPE:
                    sys_logging("set type = 0x%x" %type)
                    sys_logging("get type = 0x%x" %a.value.s32)
                    if type != a.value.s32:
                        raise NotImplementedError()
        
        finally:
            sai_thrift_remove_counter(self.client, counter_id)

class CounterRemoveTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        
        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)
        status = sai_thrift_remove_counter(self.client, counter_id)
        sys_logging("remove status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_counter_attribute(counter_id)
            sys_logging("get attr status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        
        finally:
            sys_logging("CounterRemoveTest finally.")
            #sai_thrift_remove_counter(self.client, counter_id)
            
class RouterCounterSetTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)
        
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        #rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        
        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        warmboot(self.client)
        try:
            addr = sai_thrift_ip_t(ip4=ip_addr1_subnet)
            mask = sai_thrift_ip_t(ip4=ip_mask1)
            ip_prefix = sai_thrift_ip_prefix_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr, mask=mask)
            route = sai_thrift_route_entry_t(vr_id, ip_prefix)            
            
            attrs = self.client.sai_thrift_get_route_attribute(route)
            sys_logging("get status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTE_ENTRY_ATTR_COUNTER_ID:
                    sys_logging("set counterid = 0x%x" %counter_id)
                    sys_logging("get counterid = 0x%x" %a.value.oid)
                    if counter_id != a.value.oid:
                        raise NotImplementedError()
        
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)
            

class RouterCounterPacketTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)
        
        
        port1 = port_list[0]
        port2 = port_list[1]

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)


        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        
        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                pktlen=120)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            
            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 124)
            
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 2)
            assert (counters_results[1] == 248)
            
        
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)
            
class RouterCounterExtPacketTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)
        
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                pktlen=120)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [0])
            
            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            mode = SAI_STATS_MODE_READ_AND_CLEAR
            counters_results = self.client.sai_thrift_get_counter_stats_ext(counter_id,cnt_ids, mode, len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 124)
            
            self.ctc_send_packet( 1, str(pkt), count=2)
            self.ctc_verify_packets( exp_pkt, [0], cmpSeq=1)
            self.ctc_verify_packets( exp_pkt, [0], cmpSeq=2)
            
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 2)
            assert (counters_results[1] == 248)
            
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)
            
class RouterCounterClearTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)
        
        
        port1 = port_list[0]
        port2 = port_list[1]

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)


        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD, counter_oid = counter_id)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                pktlen=120)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt), count=10)
            self.ctc_verify_packets( exp_pkt, [0])
            
            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 10)
            assert (counters_results[1] == 1240)
            
            status = self.client.sai_thrift_clear_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("clear status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)
            
        
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)
            
class NexthopMplsCounterPacketTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)
        
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        sys_logging("vr_id = %lx" %vr_id)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        sys_logging("rif_id1 = %lx" %rif_id1)
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
 
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4     
        
        ip_mask = '255.255.255.0'
        ip_da_hostA = '1.1.1.2'
        dmac_hostA = '00:11:11:11:11:11'   
        
        ip_da_SWB = '2.2.2.2'
        dmac_SWB = '00:22:22:22:22:22'
        
        # create neighbor entries
        # Host_A_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da_hostA, dmac_hostA)
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da_hostA, dmac_hostA)
        # SW_B_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWB, dmac_SWB)
        
        
        # router 
        # local route   
        ip_da_SWA_rif1 = '2.2.2.0'
        ip_da_SWA_rif2 = '1.1.1.0'

        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_da_SWB, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_da_SWA_rif1, ip_mask, nhop1)
        
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_da_hostA, rif_id2)
        #nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_da_hostA, rif_id3)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_da_SWA_rif2, ip_mask, nhop2)
        
        
        # remote routes (ingress LER)
        # route to host B network 
        # MPLS next hop 
        # SW_B2_1 next hop  //net hop from SW A via SW B to 7.7.7.0/24
        
        label_list3 = [300]
        nhop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWB, rif_id1, label_list3)
        
        # SW_B2_2 next hop  //net hop from SW A via SW B to 6.6.6.0/24 
        #label_list2 = [200]
        #label_list2 = [1089470664]
        label_list2 = [823104]
        nhop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWB, rif_id1, label_list2, counter_oid=counter_id)
        
        # route
        ip_da_siteE = '6.6.6.0'
        ip_da_siteD = '7.7.7.0'
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_da_siteE, ip_mask, nhop3)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_da_siteD, ip_mask, nhop4)

        # send the test packet(s)
        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src='00:11:11:11:11:11',
                               ip_dst='7.7.7.2',
                               ip_src='1.1.1.2',
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls1 = [{'label':200,'tc':7,'ttl':64,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst='7.7.7.2',
                                ip_ttl=63,
                                ip_id=105,
                                ip_ihl=5
                                )
                                
        # something wrong; use mask to not care 
        exp_pkt1 = simple_mpls_packet(
                                eth_dst=dmac_SWB,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1)
                                
        

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1), count=3)
            self.ctc_verify_packets( exp_pkt1, [2])
            
            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 3)
            assert (counters_results[1] == 324)
            
            status = self.client.sai_thrift_clear_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("clear status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)
            
        
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_da_siteE, ip_mask, nhop3)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_da_siteD, ip_mask, nhop4)
            self.client.sai_thrift_remove_next_hop(nhop3)
            self.client.sai_thrift_remove_next_hop(nhop4)
        
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_da_SWA_rif1, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_da_SWA_rif2, ip_mask, nhop2)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)

            # Host_A_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da_hostA, dmac_hostA)
            # SW_B_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWB, dmac_SWB)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_counter(self.client, counter_id)
            
class NexthopTunnelVxlanCounterTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        type = SAI_COUNTER_TYPE_REGULAR
        counter_id = sai_thrift_create_counter(self.client, type)
        sys_logging("creat counter_id = %d" %counter_id)
        
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
        
        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
       
        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        sys_logging("tunnel_map_decap_id = %lx" %tunnel_map_decap_id)
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
        sys_logging("tunnel_map_encap_id = %lx" %tunnel_map_encap_id)
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, vlan_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, vlan_id, vni_id)
     
       # encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
       # decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        encap_mapper_list=[tunnel_map_encap_id]
        decap_mapper_list=[tunnel_map_decap_id] 
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_encap_id)
        sys_logging("tunnel_id = %lx" %tunnel_id)

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_VXLAN)
        sys_logging("tunnel_term_table_entry_id = %lx" %tunnel_term_table_entry_id)
        
        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id, vni_id, '00:11:22:33:44:55', counter_id);
        sys_logging("tunnel_nexthop_id = %lx" %tunnel_nexthop_id)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        sai_thrift_create_fdb_tunnel(self.client, vlan_oid, inner_mac_da, btunnel_id, mac_action, ip_outer_addr_da)
        
        
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
            
            cnt_ids=[]
            cnt_ids.append(SAI_COUNTER_STAT_PACKETS)
            cnt_ids.append(SAI_COUNTER_STAT_BYTES)
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 154)
            
            status = self.client.sai_thrift_clear_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("clear status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            counters_results = self.client.sai_thrift_get_counter_stats(counter_id,cnt_ids,len(cnt_ids))
            sys_logging("packets = %d " %(counters_results[0]))
            sys_logging("bytes = %d " %(counters_results[1]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)
            
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
