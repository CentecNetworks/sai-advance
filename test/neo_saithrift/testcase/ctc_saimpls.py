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
Thrift SAI MPLS tests
"""
import socket
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask

@group('mpls')         
class Inseg_Entry_CreateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Inseg entry Create Test.  
        Steps:
        1. Create Inseg Entry.
        2. get attribute and check
        3. clean up.
        """
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        print "vr_id = %lx" %vr_id

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        print "rif_id1 = %lx" %rif_id1
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_mask = '255.255.255.0'
        ip_da_SWE = '5.5.5.2'
        dmac_SWE = '00:55:55:55:55:55'
        
        # create neighbor entries
        # SW_E_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)
        

        # MPLS next hop 
        # SW_E_1_next_hop //net hop from SW C via SW E to 7.7.7.0/24  PHP 
        label_list = [150]
        SW_E_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWE, rif_id1, label_list)
        print "SW_E_1_next_hop = %lx" %SW_E_1_next_hop
        
        # setup inseg entry
        label = 100
        pop_nums = 1
        nhop = SW_E_1_next_hop
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, nhop, packet_action)
        
        warmboot(self.client)
        try:
            print "Get inseg entry attribute:  pop_nums = 1, nhop = SW_E_1_next_hop, packet_action = SAI_PACKET_ACTION_FORWARD "
            mpls = sai_thrift_inseg_entry_t(label)            
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls)
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_NUM_OF_POP:
                    print "set pop_nums = %d" %pop_nums
                    print "get pop_nums = %d" %a.value.u8
                    if pop_nums != a.value.u8:
                        raise NotImplementedError()
                if a.id == SAI_INSEG_ENTRY_ATTR_PACKET_ACTION: 
                    print "set packet_action = %d" %SAI_PACKET_ACTION_FORWARD
                    print "get packet_action = %d" %a.value.s32
                    if packet_action != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID: 
                    print "set nhop = %d" %nhop
                    print "get nhop = %d" %a.value.oid
                    if nhop != a.value.oid:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            self.client.sai_thrift_remove_next_hop(SW_E_1_next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
@group('mpls')            
class Inseg_Entry_RemoveTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Inseg Entry Remove Test. 
        Steps:
        1. create inseg entry
        2. remove inseg entry
        3. get attribute and check
        5. clean up.
        """
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        print "vr_id = %lx" %vr_id

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        print "rif_id1 = %lx" %rif_id1
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_mask = '255.255.255.0'
        ip_da_SWE = '5.5.5.2'
        dmac_SWE = '00:55:55:55:55:55'
        
        # create neighbor entries
        # SW_E_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)
        

        # MPLS next hop 
        # SW_E_1_next_hop //net hop from SW C via SW E to 7.7.7.0/24  PHP 
        label_list = [150]
        SW_E_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWE, rif_id1, label_list)
        print "SW_E_1_next_hop = %lx" %SW_E_1_next_hop
        
        # setup inseg entry
        label = 100
        pop_nums = 1
        nhop = SW_E_1_next_hop
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, nhop, packet_action)
              
        warmboot(self.client)
        try:
            print "Get inseg entry attribute:  pop_nums = 1, nhop = SW_E_1_next_hop, packet_action = SAI_PACKET_ACTION_FORWARD "
            mpls = sai_thrift_inseg_entry_t(label)            
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls)
            print "sai_thrift_get_inseg_entry_attribute; status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print "sai_thrift_remove_inseg_entry: pop_nums = 1, nhop = SW_E_1_next_hop, packet_action = SAI_PACKET_ACTION_FORWARD "
            status=self.client.sai_thrift_remove_inseg_entry(mpls)
            print "sai_thrift_remove_inseg_entry; status = %d" %status
            assert (status == SAI_STATUS_SUCCESS)
            print "Get inseg entry attribute:  pop_nums = 1, nhop = SW_E_1_next_hop, packet_action = SAI_PACKET_ACTION_FORWARD "
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls)
            print "sai_thrift_get_inseg_entry_attribute; status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            print "Success!"
            self.client.sai_thrift_remove_next_hop(SW_E_1_next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)

@group('mpls')           
class Inseg_Entry_GetTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Inseg Entry GET Test.  
        Steps:
        1. Create Inseg Entry.
        2. get attribute and check
        3. clean up.
        """
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        print "vr_id = %lx" %vr_id

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        print "rif_id1 = %lx" %rif_id1
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_mask = '255.255.255.0'
        ip_da_SWE = '5.5.5.2'
        dmac_SWE = '00:55:55:55:55:55'
        
        # create neighbor entries
        # SW_E_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)
        

        # MPLS next hop 
        # SW_E_1_next_hop //net hop from SW C via SW E to 7.7.7.0/24  PHP 
        label_list = [150]
        SW_E_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWE, rif_id1, label_list)
        print "SW_E_1_next_hop = %lx" %SW_E_1_next_hop
        
        # setup inseg entry
        label = 100
        pop_nums = 1
        nhop = SW_E_1_next_hop
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, nhop, packet_action)
        
        warmboot(self.client)
        try:
            print "Get inseg entry attribute:  pop_nums = 1, nhop = SW_E_1_next_hop, packet_action = SAI_PACKET_ACTION_FORWARD "
            mpls = sai_thrift_inseg_entry_t(label)            
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls)
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_NUM_OF_POP:
                    print "set pop_nums = %d" %pop_nums
                    print "get pop_nums = %d" %a.value.u8
                    if pop_nums != a.value.u8:
                        raise NotImplementedError()
                if a.id == SAI_INSEG_ENTRY_ATTR_PACKET_ACTION: 
                    print "set packet_action = %d" %SAI_PACKET_ACTION_FORWARD
                    print "get packet_action = %d" %a.value.s32
                    if packet_action != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID: 
                    print "set nhop = %d" %nhop
                    print "get nhop = %d" %a.value.oid
                    if nhop != a.value.oid:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            self.client.sai_thrift_remove_next_hop(SW_E_1_next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id) 
            
@group('mpls')           
class Inseg_Entry_SetTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Inseg Entry SET Test.  
        Steps:
        1. Create Inseg Entry.
        2. get attribute and check.
        3. set inseg entry attribute.
        4. get attribute and check.
        5. clean up.
        """
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        print "vr_id = %lx" %vr_id

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        print "rif_id1 = %lx" %rif_id1
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_mask = '255.255.255.0'
        ip_da_SWE = '5.5.5.2'
        dmac_SWE = '00:55:55:55:55:55'
        
        # create neighbor entries
        # SW_E_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)
        

        # MPLS next hop 
        # SW_E_1_next_hop //net hop from SW C via SW E to 7.7.7.0/24  PHP 
        label_list = [150]
        SW_E_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWE, rif_id1, label_list)
        print "SW_E_1_next_hop = %lx" %SW_E_1_next_hop
        
        # setup inseg entry
        label = 100
        pop_nums = 1
        nhop = SW_E_1_next_hop
        packet_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, nhop, packet_action)
        #return
        warmboot(self.client)
        try:
            print "Get inseg entry attribute:  pop_nums = 1, nhop = SW_E_1_next_hop, packet_action = SAI_PACKET_ACTION_FORWARD "
            mpls = sai_thrift_inseg_entry_t(label)            
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls)
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_NUM_OF_POP:
                    print "set pop_nums = %d" %pop_nums
                    print "get pop_nums = %d" %a.value.u8
                    if pop_nums != a.value.u8:
                        raise NotImplementedError()
                if a.id == SAI_INSEG_ENTRY_ATTR_PACKET_ACTION: 
                    print "set packet_action = %d" %SAI_PACKET_ACTION_FORWARD
                    print "get packet_action = %d" %a.value.s32
                    if packet_action != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID: 
                    print "set nhop = %d" %nhop
                    print "get nhop = %d" %a.value.oid
                    if nhop != a.value.oid:
                        raise NotImplementedError()
            print "Set inseg entry attribute:  pop_nums = 0, nhop = SW_E_1_next_hop, packet_action = SAI_PACKET_ACTION_DENY "          
            pop_nums = 0
            attr_value = sai_thrift_attribute_value_t(u8=pop_nums)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_NUM_OF_POP, value=attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(mpls, attr)
            packet_action = SAI_PACKET_ACTION_DENY
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DENY)
            attr = sai_thrift_attribute_t(id=SAI_INSEG_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_inseg_entry_attribute(mpls, attr)
            print "Get inseg entry attribute:  pop_nums = 0, nhop = SW_E_1_next_hop, packet_action = SAI_PACKET_ACTION_DENY  "         
            attrs = self.client.sai_thrift_get_inseg_entry_attribute(mpls)
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_INSEG_ENTRY_ATTR_NUM_OF_POP:
                    print "set pop_nums = %d" %pop_nums
                    print "get pop_nums = %d" %a.value.u8
                    if pop_nums != a.value.u8:
                        raise NotImplementedError()
                if a.id == SAI_INSEG_ENTRY_ATTR_PACKET_ACTION: 
                    print "set packet_action = %d" %SAI_PACKET_ACTION_DENY
                    print "get packet_action = %d" %a.value.s32
                    if packet_action != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_INSEG_ENTRY_ATTR_NEXT_HOP_ID: 
                    print "set nhop = %d" %nhop
                    print "get nhop = %d" %a.value.oid
                    if nhop != a.value.oid:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            self.client.sai_thrift_remove_next_hop(SW_E_1_next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id) 
            
@group('mpls')
class Ingress_LSR_TEST(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print "Sending packet port 1 -> port 2 (192.168.0.1 -> 10.10.10.1 [id = 101])"
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        print "vr_id = %lx" %vr_id

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        print "rif_id1 = %lx" %rif_id1
        
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
 
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
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
        nhop4 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWB, rif_id1, label_list2)
        
        # route
        ip_da_siteE = '6.6.6.0'
        ip_da_siteD = '7.7.7.0'
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_da_siteE, ip_mask, nhop3)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_da_siteD, ip_mask, nhop4)
        
        # MPLS in segment enrty (egress LER)
        label = 100
        pop_nums = 1
        #nhop = rif_id3
        sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, rif_id3, None) 

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
 
        mpls2 = [{'label':100,'tc':3,'ttl':64,'s':1}]
        
        ip_only_pkt2 = simple_ip_only_packet(pktlen=86,
                                ip_src='192.168.0.1',
                                ip_dst='1.1.1.2',
                                ip_tos=0,
                                ip_ecn=None,
                                ip_dscp=None,
                                ip_ttl=64,
                                ip_id=0x0001
                                )
                                

        pkt2 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src='00:06:07:08:09:0a',
                                mpls_type=0x8847,
                                mpls_tags= mpls2,
                                inner_frame = ip_only_pkt2) 
                                

        # something wrong; use mask to not care 
        exp_pkt2 = simple_tcp_packet(
                                eth_dst=dmac_hostA,
                                eth_src=router_mac,
                                ip_src='192.168.0.1',
                                ip_dst='1.1.1.2',
                                ip_tos=0,
                                ip_ecn=None,
                                ip_dscp=None,
                                ip_ttl=63,
                                ip_id=0x0001
                                )
        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [2])
            
            # with label, lookup ilm to pop and decap, then use innner ip to lookup route 
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [1])
             
        finally:
            label = 100
            mpls = sai_thrift_inseg_entry_t(label) 
            self.client.sai_thrift_remove_inseg_entry(mpls) 
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
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
   
   
@group('mpls')
class Transmit_LSR_TEST(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print "Sending packet port 1 -> port 2 (192.168.0.1 -> 10.10.10.1 [id = 101])"
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        
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
        # SW_C_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_da_SWC, dmac_SWC)
        # SW_D_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)        
        
        # net hop from SW B via SW A to 1.1.1.0/24        
        #label_list = [100]   #wrong
        label_list = [413503] 
        SW_A_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWA, rif_id1, label_list)        
        # net hop from SW B via SW D to 7.7.7.0/24 
        SW_D_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWD, rif_id2, label_list)        
        # net hop from SW B via SW C to 6.6.6.0/24
        SW_C_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWC, rif_id3, label_list)        
        
        # MPLS in segment enrty (egress LER)
        label = 200
        pop_nums = 1
        nhop = SW_D_1_next_hop
        sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, nhop, None)        
        label = 300
        pop_nums = 1
        nhop = SW_C_1_next_hop
        sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, nhop, None)        
        label = 100
        pop_nums = 1
        nhop = SW_A_1_next_hop
        sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, nhop, None)
        
        # send the test packet(s)
        mpls1 = [{'label':300,'tc':3,'ttl':64,'s':1}]    
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
                                eth_dst=dmac_SWC,
                                eth_src=router_mac,
                                mpls_type=0x8847,
                                mpls_tags= exp_mpls1,
                                inner_frame = exp_ip_only_pkt1) 
                                
        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [3])
        finally:
            label = 100
            mpls = sai_thrift_inseg_entry_t(label)   
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            label = 200
            mpls = sai_thrift_inseg_entry_t(label)  
            self.client.sai_thrift_remove_inseg_entry(mpls)  
            label = 300
            mpls = sai_thrift_inseg_entry_t(label)  
            self.client.sai_thrift_remove_inseg_entry(mpls) 
            
            self.client.sai_thrift_remove_next_hop(SW_A_1_next_hop)
            self.client.sai_thrift_remove_next_hop(SW_C_1_next_hop)
            self.client.sai_thrift_remove_next_hop(SW_D_1_next_hop)
            
            # SW_A_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWA, dmac_SWA)
            # SW_C_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_da_SWC, dmac_SWC)
            # SW_D_neigh
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da_SWD, dmac_SWD)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
@group('mpls')
class Egress_LSR_TEST(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print "Sending packet port 1 -> port 2 (192.168.0.1 -> 10.10.10.1 [id = 101])"
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_mask = '255.255.255.0'
        ip_da_SWB = '4.4.4.2'
        dmac_SWB = '00:22:22:22:22:22'
        ip_da_SWE = '5.5.5.2'
        dmac_SWE = '00:55:55:55:55:55'
        
        # create neighbor entries
        # SW_B_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_da_SWB, dmac_SWB)
        # SW_E_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)
        

        # MPLS next hop 
        # SW_B_1_next_hop  //net hop from SW C via SW B to 7.7.7.0/24 
        label_list2 = [823104] # label 200, exp 7, s 1, ttl 64
        SW_B_1_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWB, rif_id2, label_list2)
        # SW_B_2_next_hop  //net hop from SW C via SW B to 1.1.1.0/24 
        label_list1 = [413503]    # label 100, exp 7, s 1, ttl 63
        SW_B_2_next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da_SWB, rif_id2, label_list1)
        
        # SW_E_1_next_hop //net hop from SW C via SW E to 7.7.7.0/24  PHP 
        SW_E_1_next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da_SWE, rif_id1)
        
        
        # MPLS in segment enrty (egress LER)
        label = 100
        pop_nums = 1
        nhop = SW_E_1_next_hop
        sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, nhop, None)
        
        #route
        ip_da_siteA = '1.1.1.0'
        ip_da_siteD = '7.7.7.0'
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_da_siteA, ip_mask, SW_B_2_next_hop)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_da_siteD, ip_mask, SW_B_1_next_hop)
        
        # send the test packet(s)
        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                               eth_src=dmac_SWE,
                               ip_dst='1.1.1.2',
                               ip_src='6.6.6.2',
                               ip_id=105,
                               ip_ttl=64)
                               
        mpls1 = [{'label':100,'tc':7,'ttl':63,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_dst='1.1.1.2',
                                ip_src='6.6.6.2',
                                ip_tos=0,
                                ip_ecn=None,
                                ip_dscp=None,
                                ip_ttl=63,
                                ip_id=105
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
            self.ctc_send_packet( 1, str(pkt1))   #label_list1 = [413503]    # label 100, exp 7, s 1, ttl 63
            self.ctc_verify_packets( exp_pkt1, [2])
            
        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_da_siteA, ip_mask, SW_B_2_next_hop)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_da_siteD, ip_mask, SW_B_1_next_hop)
            
            label = 100
            mpls = sai_thrift_inseg_entry_t(label) 
            self.client.sai_thrift_remove_inseg_entry(mpls) 

            self.client.sai_thrift_remove_next_hop(SW_E_1_next_hop)
            self.client.sai_thrift_remove_next_hop(SW_B_2_next_hop)
            self.client.sai_thrift_remove_next_hop(SW_B_1_next_hop)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_da_SWB, dmac_SWB)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
  

@group('mpls')
class MPLS_PHP_TEST(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print "Sending packet port 1 -> port 2 (192.168.0.1 -> 10.10.10.1 [id = 101])"
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_mask = '255.255.255.0'
        ip_da_SWE = '5.5.5.2'
        dmac_SWE = '00:55:55:55:55:55'
        dmac_SWB = '00:22:22:22:22:22'
        
        # create neighbor entries
        # SW_E_neigh
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)
        

        # MPLS next hop 
        # SW_E_1_next_hop //net hop from SW C via SW E to 7.7.7.0/24  PHP 
        SW_E_1_next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da_SWE, rif_id1)
        
        
        # MPLS in segment enrty (egress LER)
        label = 100
        pop_nums = 1
        nhop = SW_E_1_next_hop
        sai_thrift_create_inseg_entry(self.client, label, pop_nums, None, nhop, None)

        # send the test packet(s)                     
        mpls1 = [{'label':100,'tc':3,'ttl':64,'s':1}]   
        ip_only_pkt1 = simple_ip_only_packet(pktlen=86,
                                ip_src='1.1.1.2',
                                ip_dst='6.6.6.2',
                                ip_tos=0,
                                ip_ecn=None,
                                ip_dscp=None,
                                ip_ttl=64,
                                ip_id=105
                                )                             
        pkt1 = simple_mpls_packet(
                                eth_dst=router_mac,
                                eth_src=dmac_SWB,
                                mpls_type=0x8847,
                                mpls_tags= mpls1,
                                inner_frame = ip_only_pkt1) 
        
        # something wrong; use mask to not care      
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac_SWE,
                                eth_src=router_mac,
                                ip_src='1.1.1.2',
                                ip_dst='6.6.6.2',
                                ip_id=105,
                                ip_ttl=63)
                                
        warmboot(self.client)
        try:
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])
        finally:
            mpls = sai_thrift_inseg_entry_t(label) 
            self.client.sai_thrift_remove_inseg_entry(mpls) 
            
            self.client.sai_thrift_remove_next_hop(SW_E_1_next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da_SWE, dmac_SWE)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            
