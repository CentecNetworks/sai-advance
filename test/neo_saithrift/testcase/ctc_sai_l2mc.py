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
Thrift SAI L2MC interface tests
"""
import socket
from switch import *
import sai_base_test
import pdb
import time
from scapy.config import *
from scapy.layers.all import *
from ptf.mask import Mask

def sai_thrift_fill_l2mc_entry(addr_family, bv_id, dip_addr, sip_addr, type):
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=dip_addr)
        dipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
        addr = sai_thrift_ip_t(ip4=sip_addr)
        sipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=dip_addr)
        dipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
        addr = sai_thrift_ip_t(ip6=sip_addr)
        sipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)

    l2mc_entry = sai_thrift_l2mc_entry_t(bv_id=bv_id, type=type, source=sipaddr, destination=dipaddr)
    return l2mc_entry

def sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr, sip_addr, type):
    if addr_family == SAI_IP_ADDR_FAMILY_IPV4:
        addr = sai_thrift_ip_t(ip4=dip_addr)
        dipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
        addr = sai_thrift_ip_t(ip4=sip_addr)
        sipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4, addr=addr)
    else:
        addr = sai_thrift_ip_t(ip6=dip_addr)
        dipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)
        addr = sai_thrift_ip_t(ip6=sip_addr)
        sipaddr = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV6, addr=addr)

    ipmc_entry = sai_thrift_ipmc_entry_t(vr_id=vr_id, type=type, source=sipaddr, destination=dipaddr)
    return ipmc_entry

    
@group('L2MC')
class func_01_create_l2mc_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        sys_logging("###create l2mc group###")
       
        grp_attr_list = []        
        
        warmboot(self.client)
        try:
            grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            sys_logging("###grp_id: %d###" %grp_id)
            assert( SAI_NULL_OBJECT_ID != grp_id)   
        finally:
            self.client.sai_thrift_remove_l2mc_group(grp_id)            

            
class func_02_create_multi_l2mc_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        sys_logging("###create multi l2mc group###")
       
        grp_attr_list = []        
        
        warmboot(self.client)
        try:
            grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            sys_logging("###grp_id1: %d###" %grp_id1)
            sys_logging("###grp_id2: %d###" %grp_id2)            
            assert( SAI_NULL_OBJECT_ID != grp_id1) 
            assert( SAI_NULL_OBJECT_ID != grp_id2)
            assert( grp_id1 != grp_id2)            
        finally:
            self.client.sai_thrift_remove_l2mc_group(grp_id1) 
            self.client.sai_thrift_remove_l2mc_group(grp_id2)             



class func_03_create_max_l2mc_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        sys_logging("###create max l2mc group###")
        sys_logging("###group 0 is reserved###")
        
        grp_attr_list = []
        max_mcast_group_number = 8192   
        grp_id = [0 for i in range(0,max_mcast_group_number)]       

        for a in range(1,max_mcast_group_number):  
            sys_logging("###create l2mc group: %d ###" %a)            
            grp_id[a] = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            sys_logging("###grp_id oid: %d###" %grp_id[a])                        
            assert( SAI_NULL_OBJECT_ID != grp_id[a]) 
            
        warmboot(self.client)
        try:
        
           sys_logging("###create l2mc group: %d ###" %max_mcast_group_number)            
           max_grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
           sys_logging("###grp_id oid: %d###" %max_grp_id)                        
           assert( SAI_NULL_OBJECT_ID == max_grp_id)                 
        
        finally:
            for a in range(1,max_mcast_group_number):         
                self.client.sai_thrift_remove_l2mc_group(grp_id[a]) 


class func_04_remove_l2mc_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        sys_logging("###remove l2mc group###")
       
        grp_attr_list = []        
        
        warmboot(self.client)
        try:
            grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            sys_logging("###grp_id: %d###" %grp_id)
            assert( SAI_NULL_OBJECT_ID != grp_id)
            
            status = self.client.sai_thrift_remove_l2mc_group(grp_id)
            assert( SAI_STATUS_SUCCESS == status)            
            
        finally:
            sys_logging("###test end###")  


class func_05_remove_not_exist_l2mc_group_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        sys_logging("###remove not exist l2mc group###")
       
        grp_attr_list = []        
        
        warmboot(self.client)
        try:
            grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            sys_logging("###grp_id: %d###" %grp_id)
            assert( SAI_NULL_OBJECT_ID != grp_id)
            
            status = self.client.sai_thrift_remove_l2mc_group(grp_id)
            assert( SAI_STATUS_SUCCESS == status)            

            status = self.client.sai_thrift_remove_l2mc_group(grp_id)
            assert( SAI_STATUS_ITEM_NOT_FOUND == status)  
            
        finally:
            sys_logging("###test end###")  


class func_06_get_l2mc_group_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        sys_logging("###member_id1  %d###" %member_id1)
        sys_logging("###member_id2  %d###" %member_id2)
        
        group_member_list = [member_id1,member_id2]
        
        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
        sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id)
            
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_l2mc_group_attribute(grp_id)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT:
                    sys_logging("###SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT = %d ###" %a.value.u32)
                    assert( 2 == a.value.u32)
                if a.id == SAI_L2MC_GROUP_ATTR_L2MC_MEMBER_LIST:
                    for b in a.value.objlist.object_id_list:
                        sys_logging("###SAI_L2MC_GROUP_ATTR_L2MC_MEMBER_LIST group member oid %d###" %b)
                        assert( b in group_member_list )
          
        finally:
        
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)


class func_07_create_l2mc_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        
        warmboot(self.client)
        try:

            sys_logging("### same group , different bridge port ###")        
            member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
            member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)
            assert( member_id1 != SAI_NULL_OBJECT_ID )
            assert( member_id2 != SAI_NULL_OBJECT_ID )            
            assert( member_id1 != member_id2 )

            sys_logging("### same port , different group ###")        
            member_id3 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port2)
            assert( member_id3 != member_id1 ) 
            assert( member_id3 != SAI_NULL_OBJECT_ID )            
            sys_logging("### same group , same bridge port ###")             
            member_id4 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port2)
            assert( member_id4 == SAI_NULL_OBJECT_ID )  

            attrs = self.client.sai_thrift_get_l2mc_group_attribute(grp_id1)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT:
                    sys_logging("###SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT = %d ###" %a.value.u32)
                    assert( 2 == a.value.u32)

            attrs = self.client.sai_thrift_get_l2mc_group_attribute(grp_id2)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT:
                    sys_logging("###SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT = %d ###" %a.value.u32)
                    assert( 1 == a.value.u32)
                        
        finally:
       
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group_member(member_id3)
            self.client.sai_thrift_remove_l2mc_group_member(member_id4)
           
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            self.client.sai_thrift_remove_l2mc_group(grp_id2)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)


class func_08_remove_l2mc_group_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)

        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)    

        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
        sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)
        
        
        warmboot(self.client)
        try:

            status = self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            assert( SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            assert( SAI_STATUS_ITEM_NOT_FOUND == status)
       
            attrs = self.client.sai_thrift_get_l2mc_group_attribute(grp_id1)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT:
                    sys_logging("###SAI_L2MC_GROUP_ATTR_L2MC_OUTPUT_COUNT = %d ###" %a.value.u32)
                    assert( 1 == a.value.u32)

                        
        finally:
                 
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)

            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
                       
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)


class func_09_get_l2mc_group_member_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)

        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        bport2_id = sai_thrift_get_bridge_port_by_port(self.client, port2)
        
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)

        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
        sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)
        
        
        warmboot(self.client)
        try:

            attrs = self.client.sai_thrift_get_l2mc_group_member_attribute(member_id1)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_GROUP_ID:
                    sys_logging("###SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_GROUP_ID = %d ###" %a.value.oid)
                    assert( grp_id1 == a.value.oid)
                if a.id == SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_OUTPUT_ID:
                    sys_logging("###SAI_L2MC_GROUP_MEMBER_ATTR_L2MC_OUTPUT_ID = %d ###" %a.value.oid)
                    assert( bport2_id == a.value.oid)
                        
        finally:

            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
           
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)



class func_10_create_mcast_fdb_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        
        warmboot(self.client)
        try:

            sys_logging("### unknown multicast ###")
        
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            sys_logging("### known multicast ###")

            mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
        finally:

            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)





class func_11_remove_mcast_fdb_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        
        warmboot(self.client)
        try:

            sys_logging("### known multicast ###")

            mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
            status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id)
            assert( SAI_STATUS_SUCCESS == status)

            mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
            status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id)
            assert( SAI_STATUS_ITEM_ALREADY_EXISTS == status)
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            status = self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            assert( SAI_STATUS_SUCCESS == status)    

            status = self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            assert( SAI_STATUS_ITEM_NOT_FOUND == status)   
            
            sys_logging("### unknown multicast ###")        
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])
    
        finally:
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)







class func_12_set_and_get_mcast_fdb_entry_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
        status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id)
        assert( SAI_STATUS_SUCCESS == status)    

        
        warmboot(self.client)
        try:

            sys_logging("### known multicast ###")           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry, attr)
            
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION value %d ###" %a.value.s32 )
                    assert( SAI_PACKET_ACTION_DROP == a.value.s32)
                          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet(str(exp_pkt), 1)
            self.ctc_verify_no_packet(str(exp_pkt), 2)            
            self.ctc_verify_no_packet(str(exp_pkt), 3)
    
        finally:
        
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)




class func_12_set_and_get_mcast_fdb_entry_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
        status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id)
        assert( SAI_STATUS_SUCCESS == status)    

        
        warmboot(self.client)
        try:

            sys_logging("### known multicast ###")           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
            metadata = 123
            attr_value = sai_thrift_attribute_value_t(u32=metadata)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_META_DATA, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry, attr)
            
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_META_DATA:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_META_DATA value %d ###" %a.value.u32 )  
                    assert( metadata == a.value.u32)
                          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
    
        finally:
        
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)






class func_12_set_and_get_mcast_fdb_entry_attribute_fn_3(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)
 
        member_id3 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port3)
        member_id4 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port4)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
        status = sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)    

        
        warmboot(self.client)
        try:

            sys_logging("### known multicast ###")           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            

            attr_value = sai_thrift_attribute_value_t(oid=grp_id2)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry, attr)
            
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID value %d ###" %a.value.oid )  
                    assert( grp_id2 == a.value.oid)
                          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [2,3])
            self.ctc_verify_no_packet(str(exp_pkt), 1)


            attr_value = sai_thrift_attribute_value_t(oid=grp_id3)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry, attr)
            
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID value %d ###" %a.value.oid )  
                    assert( grp_id3 == a.value.oid)
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet(str(exp_pkt), 1)
            self.ctc_verify_no_packet(str(exp_pkt), 2)            
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
        finally:

            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group_member(member_id3)
            self.client.sai_thrift_remove_l2mc_group_member(member_id4)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            self.client.sai_thrift_remove_l2mc_group(grp_id2)
            self.client.sai_thrift_remove_l2mc_group(grp_id3)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)



class func_13_create_l2mc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)

        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
            
        
        warmboot(self.client)
        try:
            
            sys_logging("### unknown multicast ###")      
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            status = sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)
            assert( SAI_STATUS_SUCCESS == status)

            status = sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)
            assert( SAI_STATUS_ITEM_ALREADY_EXISTS == status)
            
            sys_logging("### known multicast ###")           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
        finally:
        
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)

            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)            

            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)


class func_13_create_l2mc_entry_fn_v6(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)


        pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        
        warmboot(self.client)
        try:
        
            sys_logging("### unknown multicast ###")      
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])        

            sys_logging("### known multicast ###")             
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)        
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
                                 
        finally:
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            

class func_14_remove_l2mc_entry_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)

        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
            
        
        warmboot(self.client)
        try:

            status = sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)
            assert( SAI_STATUS_SUCCESS == status)

            sys_logging("### known multicast ###")           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            status = self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            assert( SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            assert( SAI_STATUS_ITEM_NOT_FOUND == status)
            
            sys_logging("### unknown multicast ###")      
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])
      
        finally:
        
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)            

            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)



class func_14_remove_l2mc_entry_fn_v6(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)  

        pkt = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        
        warmboot(self.client)
        try:

            sys_logging("### known multicast ###")                   
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
            sys_logging("### unknown multicast ###")  
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])        
                        
        finally:
        
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)


class func_15_set_and_get_l2mc_entry_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)

        member_id3 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port3)
        member_id4 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port4)
        
        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        status = sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)
            
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
            
        
        warmboot(self.client)
        try:
            
            sys_logging("### known multicast ###")           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
            attr_value = sai_thrift_attribute_value_t(oid=grp_id2)
            attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_l2mc_entry_attribute(l2mc_entry, attr)
           
            attrs = self.client.sai_thrift_get_l2mc_entry_attribute(l2mc_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID:
                    sys_logging("### SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID %d ###" %a.value.oid ) 
                    assert (grp_id2 == a.value.oid)                    

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [2,3])
            self.ctc_verify_no_packet(str(exp_pkt), 1)
                   
        finally:

            status = self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            assert( SAI_STATUS_SUCCESS == status)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id3)
            self.client.sai_thrift_remove_l2mc_group_member(member_id4)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            self.client.sai_thrift_remove_l2mc_group(grp_id2)           
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            
            
            
class func_15_set_and_get_l2mc_entry_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)

        member_id3 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port3)
        member_id4 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port4)
        
        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        status = sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)
            
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
            
        
        warmboot(self.client)
        try:
            
            sys_logging("### known multicast ###")           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP)
            attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_l2mc_entry_attribute(l2mc_entry, attr)
            
            attrs = self.client.sai_thrift_get_l2mc_entry_attribute(l2mc_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("### SAI_L2MC_ENTRY_ATTR_PACKET_ACTION %d ###" %a.value.s32 ) 
                    assert (SAI_PACKET_ACTION_DROP == a.value.s32)                    

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet(str(exp_pkt), 1)
            self.ctc_verify_no_packet(str(exp_pkt), 2)
            self.ctc_verify_no_packet(str(exp_pkt), 3)
                   
        finally:

            status = self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            assert( SAI_STATUS_SUCCESS == status)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id3)
            self.client.sai_thrift_remove_l2mc_group_member(member_id4)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            self.client.sai_thrift_remove_l2mc_group(grp_id2)           
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)    


class func_16_bug_111035_l2mc_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)

        member_id3 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port3)
        member_id4 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port4)
        
        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        status = sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id1)
        assert( SAI_STATUS_SUCCESS == status)
            
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
            
        
        warmboot(self.client)
        try:
            
            sys_logging("### known multicast ###")           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_COPY)
            attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_l2mc_entry_attribute(l2mc_entry, attr)
            
            attrs = self.client.sai_thrift_get_l2mc_entry_attribute(l2mc_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("### SAI_L2MC_ENTRY_ATTR_PACKET_ACTION %d ###" %a.value.s32 ) 
                    assert (SAI_PACKET_ACTION_COPY == a.value.s32)                    

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            
                   
        finally:

            status = self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            assert( SAI_STATUS_SUCCESS == status)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id3)
            self.client.sai_thrift_remove_l2mc_group_member(member_id4)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            self.client.sai_thrift_remove_l2mc_group(grp_id2)           
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)  
            self.client.sai_thrift_clear_cpu_packet_info() 


class func_16_bug_111035_ipmc_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        grp_attr_list = []

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_IPMC_ENTRY_TYPE_XG
        grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id1 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id2)
        member_id2 = sai_thrift_create_ipmc_group_member(self.client, grp_id, rif_id3)
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, default_addr, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id)


        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63)
        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            sys_logging("======update action and send packet again======")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_COPY)
            attr = sai_thrift_attribute_t(id=SAI_IPMC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_ipmc_entry_attribute(ipmc_entry, attr)

            self.ctc_send_packet( 0, str(pkt))
            #self.ctc_verify_no_packet_any( exp_pkt, [1,2])
            self.ctc_verify_packets( exp_pkt, [1,2])
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_clear_cpu_packet_info() 

class scenario_01_update_group_member_for_one_entry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        dmac2 = '01:00:5E:7F:01:02'        
        smac1 = '00:00:00:00:00:01'
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
                                
        
        warmboot(self.client)
        try:

            sys_logging("### unknown multicast ###")
        
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])
           
            sys_logging("### known multicast ###")

            mcast_fdb_entry1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry1, grp_id)
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            sys_logging("### update group member: remove ###")

            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            self.ctc_verify_no_packet(str(exp_pkt), 2)
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            sys_logging("### update group member: add ###")

            member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)          
            
        finally:

            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry1)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            

class scenario_02_update_group_member_for_multi_entry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        dmac2 = '01:00:5E:7F:01:02'        
        smac1 = '00:00:00:00:00:01'
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        pkt1 = simple_tcp_packet(eth_dst=dmac2,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst=dmac2,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        mcast_fdb_entry1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
        mcast_fdb_entry2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac2, bv_id=vlan_oid)
            
        
        warmboot(self.client)
        try:

            sys_logging("### unknown multicast ###")
        
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2,3])
            
            sys_logging("### known multicast ###")

            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry1, grp_id)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry2, grp_id)
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt1), 3)

            sys_logging("### update group member: remove ###")

            self.client.sai_thrift_remove_l2mc_group_member(member_id2)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            self.ctc_verify_no_packet(str(exp_pkt), 2)            
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])
            self.ctc_verify_no_packet(str(exp_pkt1), 2)            
            self.ctc_verify_no_packet(str(exp_pkt1), 3)

            sys_logging("### update group member: add ###")
            
            member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt1), 3)
            
            
        finally:

            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry2)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)


class scenario_03_l2mc_update_group_member_for_one_entry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '224.1.1.1'
        dip_addr2 = '224.129.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)

        l2mc_entry1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
                                
        
        warmboot(self.client)
        try:
            
            sys_logging("### unknown multicast ###")
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])
            
            status = sai_thrift_create_l2mc_entry(self.client, l2mc_entry1, grp_id)
            assert( SAI_STATUS_SUCCESS == status)
         
            sys_logging("### known multicast ###")   
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
            sys_logging("### update member : remove  ###") 

            self.client.sai_thrift_remove_l2mc_group_member(member_id2)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            self.ctc_verify_no_packet(str(exp_pkt), 2)
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
            sys_logging("### update member : add  ###")             
            member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)           
        
        finally:

            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)            
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)

            
class scenario_04_l2mc_update_group_member_for_multi_entry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '224.1.1.1'
        dip_addr2 = '224.129.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)

        l2mc_entry1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        l2mc_entry2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr2, default_addr, type)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr2,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr2,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
                                
        
        warmboot(self.client)
        try:
            
            sys_logging("### unknown multicast ###") 
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2,3])
            
            status = sai_thrift_create_l2mc_entry(self.client, l2mc_entry1, grp_id)
            assert( SAI_STATUS_SUCCESS == status)

            status = sai_thrift_create_l2mc_entry(self.client, l2mc_entry2, grp_id)
            assert( SAI_STATUS_SUCCESS == status)
            
            sys_logging("### known multicast ###")  
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt1), 3)            

            sys_logging("### update member : remove  ###") 
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            self.ctc_verify_no_packet(str(exp_pkt), 2)
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1])
            self.ctc_verify_no_packet(str(exp_pkt1), 2)
            self.ctc_verify_no_packet(str(exp_pkt1), 3)
            
            sys_logging("### update member : add  ###")             
            member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt1), 3)

   
        finally:

            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry2)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)            
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)


            
class scenario_05_update_group_id_for_multi_entry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        dmac2 = '01:00:5E:7F:01:02'        
        smac1 = '00:00:00:00:00:01'
        
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)

        member_id3 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port3)
        member_id4 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port4)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        pkt1 = simple_tcp_packet(eth_dst=dmac2,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst=dmac2,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        mcast_fdb_entry1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
        mcast_fdb_entry2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac2, bv_id=vlan_oid)
            
        
        warmboot(self.client)
        try:

            sys_logging("### unknown multicast ###")
        
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2,3])
            
            sys_logging("### known multicast ###")

            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry1, grp_id1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry2, grp_id2)
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [2,3])
            self.ctc_verify_no_packet(str(exp_pkt1), 1)

            sys_logging("### update mcast_fdb_entry1 group-id ###")

            attr_value = sai_thrift_attribute_value_t(oid=grp_id2)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry1, attr)
           
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry1)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID %d ###" %a.value.oid ) 
                    assert (grp_id2 == a.value.oid)   
                    
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [2,3])
            self.ctc_verify_no_packet(str(exp_pkt), 1)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [2,3])
            self.ctc_verify_no_packet(str(exp_pkt1), 1)


            sys_logging("### update mcast_fdb_entry2 group-id ###")

            attr_value = sai_thrift_attribute_value_t(oid=grp_id1)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry2, attr)
           
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry2)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID %d ###" %a.value.oid ) 
                    assert (grp_id1 == a.value.oid)   
                    
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [2,3])
            self.ctc_verify_no_packet(str(exp_pkt), 1)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt1), 3)
                       
        finally:

            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry2)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group_member(member_id3)
            self.client.sai_thrift_remove_l2mc_group_member(member_id4)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            self.client.sai_thrift_remove_l2mc_group(grp_id2)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            
            
class scenario_06_l2mc_update_group_id_for_multi_entry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '224.1.1.1'
        dip_addr2 = '224.129.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)

        member_id3 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port3)
        member_id4 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port4)
        
        l2mc_entry1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        l2mc_entry2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr2, default_addr, type)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
            
        pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr2,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr2,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        
        warmboot(self.client)
        try:

            sys_logging("### unknown multicast ###")
        
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2,3])
           
            sys_logging("### known multicast ###")   
            
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1, grp_id1)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry2, grp_id2)
        
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [2,3])
            self.ctc_verify_no_packet(str(exp_pkt1), 1)

            sys_logging("### update l2mc_entry1 group-id ###")
            
            attr_value = sai_thrift_attribute_value_t(oid=grp_id2)
            attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_l2mc_entry_attribute(l2mc_entry1, attr)
           
            attrs = self.client.sai_thrift_get_l2mc_entry_attribute(l2mc_entry1)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID:
                    sys_logging("### SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID %d ###" %a.value.oid ) 
                    assert (grp_id2 == a.value.oid)                    
     
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [2,3])
            self.ctc_verify_no_packet(str(exp_pkt), 1)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [2,3])
            self.ctc_verify_no_packet(str(exp_pkt1), 1)

            sys_logging("### update l2mc_entry2 group-id ###")
            
            attr_value = sai_thrift_attribute_value_t(oid=grp_id1)
            attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_l2mc_entry_attribute(l2mc_entry2, attr)
           
            attrs = self.client.sai_thrift_get_l2mc_entry_attribute(l2mc_entry2)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID:
                    sys_logging("### SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID %d ###" %a.value.oid ) 
                    assert (grp_id1 == a.value.oid)                    
     
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [2,3])
            self.ctc_verify_no_packet(str(exp_pkt), 1)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt1), 3)
            
            
        finally:

            status = self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1)
            assert( SAI_STATUS_SUCCESS == status)
            
            status = self.client.sai_thrift_remove_l2mc_entry(l2mc_entry2)
            assert( SAI_STATUS_SUCCESS == status)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id3)
            self.client.sai_thrift_remove_l2mc_group_member(member_id4)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            self.client.sai_thrift_remove_l2mc_group(grp_id2)           
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            


class scenario_07_set_packet_action_per_mcast_fdb_entry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
        
        warmboot(self.client)
        try:

            sys_logging("### unknown multicast ###")
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])
            
            sys_logging("### known multicast ###")             
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id)                      
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            sys_logging("### step 1 : packet action : SAI_PACKET_ACTION_DENY ###")
            
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DENY)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry, attr)           
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION value %d ###" %a.value.s32 )
                    assert( SAI_PACKET_ACTION_DENY == a.value.s32)
                          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet(str(exp_pkt), 1)
            self.ctc_verify_no_packet(str(exp_pkt), 2)            
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            sys_logging("### step 2 : packet action : SAI_PACKET_ACTION_TRANSIT ###")
            
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRANSIT)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry, attr)           
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION value %d ###" %a.value.s32 )
                    assert( SAI_PACKET_ACTION_TRANSIT == a.value.s32)
                          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)


            sys_logging("### step 3 : packet action : SAI_PACKET_ACTION_TRAP ###")

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 0:
                raise NotImplementedError()  
                
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRAP)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry, attr)           
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION value %d ###" %a.value.s32 )
                    assert( SAI_PACKET_ACTION_TRAP == a.value.s32)
                          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet(str(exp_pkt), 1)
            self.ctc_verify_no_packet(str(exp_pkt), 2)            
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError()            
            

            sys_logging("### step 4 : packet action : SAI_PACKET_ACTION_LOG ###")
                
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_LOG)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry, attr)           
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_PACKET_ACTION value %d ###" %a.value.s32 )
                    assert( SAI_PACKET_ACTION_LOG == a.value.s32)
                          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 2:
                raise NotImplementedError() 

            
        finally:
        
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)            
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_clear_cpu_packet_info() 



class scenario_08_set_packet_action_per_l2mc_entry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4   
        default_addr = '0.0.0.0'        
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        type = SAI_L2MC_ENTRY_TYPE_XG                                
        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        
        
        warmboot(self.client)
        try:

            sys_logging("### unknown multicast ###")
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])
            
            sys_logging("### known multicast ###")             
            
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)                    
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            sys_logging("### step 1 : packet action : SAI_PACKET_ACTION_DENY ###")
            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DENY)
            attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_l2mc_entry_attribute(l2mc_entry, attr)           
            attrs = self.client.sai_thrift_get_l2mc_entry_attribute(l2mc_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("### SAI_L2MC_ENTRY_ATTR_PACKET_ACTION value %d ###" %a.value.s32 )
                    assert( SAI_PACKET_ACTION_DENY == a.value.s32)
                          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet(str(exp_pkt), 1)
            self.ctc_verify_no_packet(str(exp_pkt), 2)            
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            sys_logging("### step 2 : packet action : SAI_PACKET_ACTION_TRANSIT ###")
            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)
            attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_l2mc_entry_attribute(l2mc_entry, attr)           
            attrs = self.client.sai_thrift_get_l2mc_entry_attribute(l2mc_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("### SAI_L2MC_ENTRY_ATTR_PACKET_ACTION value %d ###" %a.value.s32 )
                    #assert( SAI_PACKET_ACTION_FORWARD == a.value.s32)
                          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)


            sys_logging("### step 3 : packet action : SAI_PACKET_ACTION_TRAP ###")

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            #if ret.data.u16 != 0:
                #raise NotImplementedError()  
                
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRAP)
            attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_l2mc_entry_attribute(l2mc_entry, attr)           
            attrs = self.client.sai_thrift_get_l2mc_entry_attribute(l2mc_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("### SAI_L2MC_ENTRY_ATTR_PACKET_ACTION value %d ###" %a.value.s32 )
                    assert( SAI_PACKET_ACTION_TRAP == a.value.s32)
                          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            #if ret.data.u16 != 1:
                #raise NotImplementedError()            
            

            sys_logging("### step 4 : packet action : SAI_PACKET_ACTION_LOG ###")
                
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_LOG)
            attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_l2mc_entry_attribute(l2mc_entry, attr)           
            attrs = self.client.sai_thrift_get_l2mc_entry_attribute(l2mc_entry)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_ENTRY_ATTR_PACKET_ACTION:
                    sys_logging("### SAI_L2MC_ENTRY_ATTR_PACKET_ACTION value %d ###" %a.value.s32 )
                    #assert( SAI_PACKET_ACTION_LOG == a.value.s32)
                          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)
            
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            #if ret.data.u16 != 2:
                #raise NotImplementedError() 

            
        finally:
        
             self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
             
             self.client.sai_thrift_remove_l2mc_group_member(member_id1)
             self.client.sai_thrift_remove_l2mc_group_member(member_id2)
             
             self.client.sai_thrift_remove_l2mc_group(grp_id)
             
             self.client.sai_thrift_remove_vlan_member(vlan_member1)
             self.client.sai_thrift_remove_vlan_member(vlan_member2)
             self.client.sai_thrift_remove_vlan_member(vlan_member3)
             self.client.sai_thrift_remove_vlan_member(vlan_member4)
             
             self.client.sai_thrift_remove_vlan(vlan_oid)
             self.client.sai_thrift_clear_cpu_packet_info() 
             
             
class scenario_09_l2mc_lookup_key_type_XG(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE:
                sys_logging("###SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG != a.value.s32:
                    raise NotImplementedError()   
                    
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        sip_addr2 = '10.10.10.2'        
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)

        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr2,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr2,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
                                
        
        warmboot(self.client)
        try:
            
            sys_logging("### unknown multicast ###")      
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2,3])
            
            sys_logging("### known multicast ###") 
            sys_logging("### xg mode do not check sip ###")  
            
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)            

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt1), 3)
            
        finally:
        
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)

            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)            

            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)             
             
             
             
             
             
             
class scenario_09_l2mc_lookup_key_type_SG(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_SG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE:
                sys_logging("###SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_SG != a.value.s32:
                    raise NotImplementedError()   
                    
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '10.10.10.1'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        sip_addr2 = '10.10.10.2'        
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_SG
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)

        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, sip_addr1, type)
        
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr2,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr2,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
                                
        
        warmboot(self.client)
        try:
            
            sys_logging("### unknown multicast ###")      
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2,3])

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2,3])
            
            sys_logging("### known multicast ###") 
            sys_logging("### sg mode will check sip ###")  
            
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)            

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1,2])
            self.ctc_verify_no_packet(str(exp_pkt), 3)

            sys_logging("### not hit will flood ###")  
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [1,2,3])
            
        finally:
        
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)

            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)            

            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)                          
             
             
             
             
class scenario_09_l2mc_lookup_key_type_XG_and_SG(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG_AND_SG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE:
                sys_logging("###SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG_AND_SG != a.value.s32:
                    raise NotImplementedError()   
                    
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '224.1.1.1'
        dip_addr2 = '224.129.1.1'        
        sip_addr1 = '10.10.10.1'
        sip_addr2 = '10.10.10.2'        
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'
        
        type1 = SAI_L2MC_ENTRY_TYPE_XG
        
        type2 = SAI_L2MC_ENTRY_TYPE_SG   
        
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)

        member_id3 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port3)
        member_id4 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port4)
        
        l2mc_entry1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type1)
        
        l2mc_entry2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, sip_addr2, type2)

        sai_thrift_create_l2mc_entry(self.client, l2mc_entry1, grp_id1)  
        sai_thrift_create_l2mc_entry(self.client, l2mc_entry2, grp_id2)  
            
        pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
                                
        pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr2,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
                                
        pk3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr2,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
                                
        
        warmboot(self.client)
        try:
            
            sys_logging("### hit SG  ###")  
            
            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( pkt2, [2,3])
            self.ctc_verify_no_packet(str(pkt2), 1)
            
            sys_logging("### hit XG  ###")
            
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt1, [1,2])
            self.ctc_verify_no_packet(str(pkt1), 3)
            
            sys_logging("### not hit ###")
            
            self.ctc_send_packet( 0, str(pk3))
            self.ctc_verify_packets( pk3, [1,2,3])
            
        finally:

            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry2)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)            
            self.client.sai_thrift_remove_l2mc_group_member(member_id3)
            self.client.sai_thrift_remove_l2mc_group_member(member_id4)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            self.client.sai_thrift_remove_l2mc_group(grp_id2)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)                                       
             
             
             
class scenario_09_l2mc_lookup_key_type_XG_V6(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE:
                sys_logging("###SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG != a.value.s32:
                    raise NotImplementedError()           
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        sip_addr2 = '3001::2'        
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_XG
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)


        pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        pkt2 = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr2,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        
        warmboot(self.client)
        try:
        
            sys_logging("### unknown multicast ###")      

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt1, [1,2,3])        

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( pkt2, [1,2,3]) 
            
            sys_logging("### known multicast ###")  
            sys_logging("### xg mode do not check sip ###") 
            
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)   
            
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt1, [1,2])
            self.ctc_verify_no_packet(str(pkt1), 3)

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( pkt2, [1,2])
            self.ctc_verify_no_packet(str(pkt2), 3)
            
        finally:
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)             
             
             
             
             
             
class scenario_09_l2mc_lookup_key_type_SG_V6(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_SG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE:
                sys_logging("###SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_SG != a.value.s32:
                    raise NotImplementedError()           
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        sip_addr2 = '3001::2'        
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_SG
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        
        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, sip_addr1, type)


        pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        pkt2 = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr2,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
        
        warmboot(self.client)
        try:
        
            sys_logging("### unknown multicast ###")      

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt1, [1,2,3])        

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( pkt2, [1,2,3]) 
            
            sys_logging("### known multicast ###")  
            sys_logging("### sg mode will check sip ###") 
            
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)   
            
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt1, [1,2])
            self.ctc_verify_no_packet(str(pkt1), 3)

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( pkt2, [1,2,3]) 
            
        finally:
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)                     
             
             
             
class scenario_09_l2mc_lookup_key_type_XG_and_SG_V6(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG_AND_SG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
        for a in attrs.attr_list:
            if a.id == SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE:
                sys_logging("###SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG_AND_SG != a.value.s32:
                    raise NotImplementedError()           
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        dip_addr2 = 'ff06::1:2'        
        sip_addr1 = '3001::1'
        sip_addr2 = '3001::2'        
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'
        
        type1 = SAI_L2MC_ENTRY_TYPE_XG
        type2 = SAI_L2MC_ENTRY_TYPE_SG
        
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port3)

        member_id3 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port3)
        member_id4 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port4)
        
        l2mc_entry1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type1)
        l2mc_entry2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, sip_addr1, type2)

        pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr2,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
                                
        pkt2 = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)

        pkt3 = simple_tcpv6_packet(
                                eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr2,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id)
                                
        
        warmboot(self.client)
        try:
        
            sys_logging("### unknown multicast ###")      

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt1, [1,2,3])        

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( pkt2, [1,2,3]) 

            self.ctc_send_packet( 0, str(pkt3))
            self.ctc_verify_packets( pkt3, [1,2,3]) 
            
            sys_logging("### known multicast ###")  
            
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1, grp_id1)   
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry2, grp_id2)

            sys_logging("### hit SG ###")  
            
            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( pkt2, [2,3])
            self.ctc_verify_no_packet(str(pkt2), 1)

            sys_logging("### hit XG ###")  
            
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt1, [1,2])
            self.ctc_verify_no_packet(str(pkt1), 3)            

            sys_logging("### not hit  ###")  
            
            self.ctc_send_packet( 0, str(pkt3))
            self.ctc_verify_packets( pkt3, [1,2,3]) 
            
            
        finally:
        
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry2)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            self.client.sai_thrift_remove_l2mc_group_member(member_id3)
            self.client.sai_thrift_remove_l2mc_group_member(member_id4)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            self.client.sai_thrift_remove_l2mc_group(grp_id2)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)                                  
             
             

class scenario_10_ipmc_entry_bind_l2mc_entry_01(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG           
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            sys_logging("### bind l2mc ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])
           
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)
             


class scenario_10_ipmc_entry_bind_l2mc_entry_01_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'       
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               

        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG           
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            sys_logging("### bind l2mc ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])
           
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)

class scenario_10_ipmc_entry_bind_l2mc_entry_02(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
        
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)
        
        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG           
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            sys_logging("### bind l2mc ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### add l2mc group member ###")   
            l2mc_member_id2_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 1, 2, 3, 4])
            
            sys_logging("### remove l2mc group member ###")   
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 1, 2, 3])            
            self.ctc_verify_no_packet_any(exp_pkt3, [4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)
             


class scenario_10_ipmc_entry_bind_l2mc_entry_02_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'       
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4) 
                                                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG           
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            sys_logging("### bind l2mc ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### add l2mc group member ###")   
            l2mc_member_id2_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 1, 2, 3, 4])
            
            sys_logging("### remove l2mc group member ###")   
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 1, 2, 3])            
            self.ctc_verify_no_packet_any(exp_pkt3, [4])
            
        finally:
            
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)
             
class scenario_10_ipmc_entry_bind_l2mc_entry_03(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                       
            type = SAI_L2MC_ENTRY_TYPE_XG           
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            sys_logging("### bind l2mc ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### remove l2mc entry ###") 
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [ exp_pkt2, exp_pkt2, exp_pkt2], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt3, [4])
            
            sys_logging("### create l2mc entry ###") 
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)    
            


             
class scenario_10_ipmc_entry_bind_l2mc_entry_03_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'         
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                          
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                       
            type = SAI_L2MC_ENTRY_TYPE_XG           
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            sys_logging("### bind l2mc ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### remove l2mc entry ###") 
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [ exp_pkt2, exp_pkt2, exp_pkt2], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt3, [4])
            
            sys_logging("### create l2mc entry ###") 
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)    

class scenario_10_ipmc_entry_bind_l2mc_entry_04(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG           
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            sys_logging("### bind l2mc ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])


            sys_logging("### change l2mc entry group id ###") 
            attr_value = sai_thrift_attribute_value_t(oid=l2mc_grp_id3)
            attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_l2mc_entry_attribute(l2mc_entry1_4, attr)
           
            attrs = self.client.sai_thrift_get_l2mc_entry_attribute(l2mc_entry1_4)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID:
                    sys_logging("### SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID %d ###" %a.value.oid ) 
                    assert (l2mc_grp_id3 == a.value.oid)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt3, [4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)




class scenario_10_ipmc_entry_bind_l2mc_entry_04_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4) 
                                
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG           
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            sys_logging("### bind l2mc ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])


            sys_logging("### change l2mc entry group id ###") 
            attr_value = sai_thrift_attribute_value_t(oid=l2mc_grp_id3)
            attr = sai_thrift_attribute_t(id=SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_l2mc_entry_attribute(l2mc_entry1_4, attr)
           
            attrs = self.client.sai_thrift_get_l2mc_entry_attribute(l2mc_entry1_4)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID:
                    sys_logging("### SAI_L2MC_ENTRY_ATTR_OUTPUT_GROUP_ID %d ###" %a.value.oid ) 
                    assert (l2mc_grp_id3 == a.value.oid)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt3, [4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)

class scenario_11_ipmc_entry_bind_mcast_fdb_entry_01(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, l2mc_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, l2mc_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)
                    
            sys_logging("### bind mcast fdb entry ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])
           
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)
             



class scenario_11_ipmc_entry_bind_mcast_fdb_entry_01_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)
                                
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, l2mc_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, l2mc_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)
                    
            sys_logging("### bind mcast fdb entry ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])
           
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)
             


class scenario_11_ipmc_entry_bind_mcast_fdb_entry_02(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, l2mc_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, l2mc_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)
                    
            sys_logging("### bind mcast fdb entry ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])


            sys_logging("### add group member ###")
            l2mc_member_id2_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port4)           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### remove group member ###")
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt3, [4])

            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_4)            
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)




class scenario_11_ipmc_entry_bind_mcast_fdb_entry_02_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4) 
                                
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, l2mc_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, l2mc_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)
                    
            sys_logging("### bind mcast fdb entry ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])


            sys_logging("### add group member ###")
            l2mc_member_id2_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port4)           
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### remove group member ###")
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)          
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt3, [4])

            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_4)            
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)


class scenario_11_ipmc_entry_bind_mcast_fdb_entry_03(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)        
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, l2mc_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, l2mc_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)
                    
            sys_logging("### bind mcast fdb entry ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])


            sys_logging("### remove mcast fdb entry ###")
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)       
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, exp_pkt2, exp_pkt2], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt3, [4])

            sys_logging("### add mcast fdb entry ###")
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)    
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)



class scenario_11_ipmc_entry_bind_mcast_fdb_entry_03_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'         
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               

        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)
                                
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, l2mc_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, l2mc_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)
                    
            sys_logging("### bind mcast fdb entry ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])


            sys_logging("### remove mcast fdb entry ###")
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)       
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, exp_pkt2, exp_pkt2], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt3, [4])

            sys_logging("### add mcast fdb entry ###")
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)    
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 3, 1, 2, 3, 4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)


class scenario_11_ipmc_entry_bind_mcast_fdb_entry_04(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, l2mc_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, l2mc_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)
                    
            sys_logging("### bind mcast fdb entry ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])


            sys_logging("### change mcast fdb entry group id ###")
            
            attr_value = sai_thrift_attribute_value_t(oid=l2mc_grp_id2)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry_4, attr)
            
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry_4)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID value %d ###" %a.value.oid )  
                    assert( l2mc_grp_id2 == a.value.oid)
                    
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2])
            self.ctc_verify_no_packet_any(exp_pkt3, [4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)
            


class scenario_11_ipmc_entry_bind_mcast_fdb_entry_04_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4) 
                                
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)
            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, l2mc_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, l2mc_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)
                    
            sys_logging("### bind mcast fdb entry ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])


            sys_logging("### change mcast fdb entry group id ###")
            
            attr_value = sai_thrift_attribute_value_t(oid=l2mc_grp_id2)
            attr = sai_thrift_attribute_t(id=SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID, value=attr_value)
            self.client.sai_thrift_set_mcast_fdb_entry_attribute(mcast_fdb_entry_4, attr)
            
            attrs = self.client.sai_thrift_get_mcast_fdb_entry_attribute(mcast_fdb_entry_4)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID:
                    sys_logging("### SAI_MCAST_FDB_ENTRY_ATTR_GROUP_ID value %d ###" %a.value.oid )  
                    assert( l2mc_grp_id2 == a.value.oid)
                    
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2])
            self.ctc_verify_no_packet_any(exp_pkt3, [4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)


class scenario_12_ipmc_entry_auto_bind_01(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)

            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
           
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            #l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            #sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            #l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            #sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)

            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            #mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            #sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, l2mc_grp_id1)
                
            #mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            #sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, l2mc_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)

            sys_logging("### auto bind ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            #self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            #self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            #self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            #self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4) 



class scenario_12_ipmc_entry_auto_bind_01_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)
                                
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)

            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
           
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            #l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            #sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            #l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            #sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)

            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            #mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            #sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, l2mc_grp_id1)
                
            #mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            #sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, l2mc_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, l2mc_grp_id4)

            sys_logging("### auto bind ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            #self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            #self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            #self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            #self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4) 



class scenario_12_ipmc_entry_auto_bind_02(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)


            fdb_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id1 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id1, port1)
            
            fdb_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id2 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id2, port2)
         
            fdb_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id3 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id3, port3)
          
            fdb_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id4 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id4, port4)


            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
           
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, fdb_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, fdb_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, fdb_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, fdb_grp_id4)

            sys_logging("### auto bind but l2mc entry have high priority###")            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### remove l2mc entry and bind mcast fdb entry ###")             
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt2, exp_pkt3], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt1, [4])

            sys_logging("### remove mcast fdb entry ###")  
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)

            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)

            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4) 



class scenario_12_ipmc_entry_auto_bind_02_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'       
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4) 
                                
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)


            fdb_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id1 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id1, port1)
            
            fdb_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id2 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id2, port2)
         
            fdb_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id3 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id3, port3)
          
            fdb_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id4 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id4, port4)


            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
           
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            
            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, fdb_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, fdb_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, fdb_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, fdb_grp_id4)

            sys_logging("### auto bind but l2mc entry have high priority###")            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### remove l2mc entry and bind mcast fdb entry ###")             
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt2, exp_pkt3], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt1, [4])

            sys_logging("### remove mcast fdb entry ###")  
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)

            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)

            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4) 



class scenario_12_ipmc_entry_auto_bind_03(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        #sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)


            fdb_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id1 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id1, port1)
            
            fdb_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id2 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id2, port2)
         
            fdb_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id3 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id3, port3)
          
            fdb_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id4 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id4, port4)

            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, fdb_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, fdb_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, fdb_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, fdb_grp_id4)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
           
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
            
            sys_logging("### auto bind ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### auto bind but l2mc entry have high priority###")            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt2, exp_pkt3], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt1, [4])

            sys_logging("### remove mcast fdb entry ###")  
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)

            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)

            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)



class scenario_12_ipmc_entry_auto_bind_03_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        #sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4) 
                                
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)


            fdb_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id1 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id1, port1)
            
            fdb_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id2 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id2, port2)
         
            fdb_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id3 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id3, port3)
          
            fdb_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id4 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id4, port4)

            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, fdb_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, fdb_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, fdb_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, fdb_grp_id4)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
           
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
            
            sys_logging("### auto bind ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### auto bind but l2mc entry have high priority###")            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt2, exp_pkt3], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt1, [4])

            sys_logging("### remove mcast fdb entry ###")  
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)

            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)

            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)



class scenario_12_ipmc_entry_auto_bind_04(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)


            fdb_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id1 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id1, port1)
            
            fdb_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id2 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id2, port2)
         
            fdb_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id3 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id3, port3)
          
            fdb_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id4 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id4, port4)

            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, fdb_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, fdb_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, fdb_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, fdb_grp_id4)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
           
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            
            sys_logging("### auto bind but l2mc entry have high priority###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### remove l2mc entry and bind mcast fdb entry auto###")             
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt2, exp_pkt3], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt1, [4])
            
            sys_logging("### remove mcast fdb entry ###")  
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)

            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)

            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)



class scenario_12_ipmc_entry_auto_bind_04_V6(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V6_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        default_addr = '0::0'
        dip_addr1 = 'ff06::1:1'
        sip_addr1 = '3001::1'
        dmac1 = '33:33:00:01:00:01'
        smac1 = '00:00:00:00:00:01'       
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt =  simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        exp_pkt3 = simple_tcpv6_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ipv6_dst=dip_addr1,
                                ipv6_src=sip_addr1,
                                ipv6_hlim=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id4)
                                
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, port1)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)


            fdb_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id1 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id1, port1)
            
            fdb_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id2 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id2, port2)
         
            fdb_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id3 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id3, port3)
          
            fdb_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            fdb_member_id4 = sai_thrift_create_l2mc_group_member(self.client, fdb_grp_id4, port4)

            #create ( '01:00:5E:01:01:01' ,Vlan 10/20/30/40) mcast fdb entry
            
            mcast_fdb_entry_1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid1)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_1, fdb_grp_id1)
                
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, fdb_grp_id2)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, fdb_grp_id3)        
            
            mcast_fdb_entry_4 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid4)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_4, fdb_grp_id4)
            
            #create (*,225.1.1.1 ,Vlan 10/20/30/40) L2MC entry
           
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id1) 
            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id2) 
            
            l2mc_entry1_3 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid3, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_3, l2mc_grp_id3)
            
            l2mc_entry1_4 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid4, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_4, l2mc_grp_id4)
            
            
            sys_logging("### auto bind but l2mc entry have high priority###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt2, exp_pkt2, exp_pkt2, exp_pkt3, exp_pkt3, exp_pkt3, exp_pkt3], [1, 2, 1, 2, 3, 1, 2, 3, 4])

            sys_logging("### remove l2mc entry and bind mcast fdb entry auto###")             
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt2, exp_pkt3], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt1, [4])
            
            sys_logging("### remove mcast fdb entry ###")  
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_3)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_4)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_1)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_4)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)

            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(fdb_member_id1)
            
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)

            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id1)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(fdb_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)


class scenario_13_ipmc_entry_bind_order_01(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        def_addr = '0.0.0.0'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_SG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)                                
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
            
            #create L2MC member group
                       
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)

            #create mcast fdb entry                         
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)

            #create SG l2mc entry    
            type = SAI_L2MC_ENTRY_TYPE_SG            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id4) 
            
            #create XG l2mc entry
            type = SAI_L2MC_ENTRY_TYPE_XG
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, def_addr, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id3) 

            sys_logging("### l2mc entry have high priority then mcast fdb ###")
            sys_logging("### xg and sg l2mc entry is same priority ###")
            sys_logging("### the order is fifo ###")
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1, exp_pkt1], [1, 2, 3, 4])
                      
            sys_logging("### remove sg l2mc entry ###")             
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt1, [4])
            
            sys_logging("### remove xg l2mc entry ###")             
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1], [1, 2])
            self.ctc_verify_no_packet_any(exp_pkt1, [3, 4])
            
            sys_logging("### remove mcast fdb entry ###")             
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
                       
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)            

            

class scenario_13_ipmc_entry_bind_order_02(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        def_addr = '0.0.0.0'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_SG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)                                
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
                                           
        
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
            
            #create L2MC member group
                       
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)

            #create mcast fdb entry                         
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)

            #create XG l2mc entry
            type = SAI_L2MC_ENTRY_TYPE_XG
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, def_addr, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id3) 
            
            #create SG l2mc entry    
            type = SAI_L2MC_ENTRY_TYPE_SG            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id4) 
            
            sys_logging("### l2mc entry have high priority then mcast fdb ###")
            sys_logging("### xg and sg l2mc entry is same priority ###")
            sys_logging("### the order is fifo ###")
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt1, [4])
                      
            sys_logging("### remove xg l2mc entry ###")             
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1, exp_pkt1], [1, 2, 3, 4])
            
            sys_logging("### remove sg l2mc entry ###")             
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1], [1, 2])
            self.ctc_verify_no_packet_any(exp_pkt1, [3, 4])
            
            sys_logging("### remove mcast fdb entry ###")             
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
                       
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)            

            
class scenario_13_ipmc_entry_bind_order_03(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        vlan_id4 = 40
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
       
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        # vlan 20 member list
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_4 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port5, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        #vlan 40 member list
        vlan_member4_1 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_2 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_3 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4_4 = sai_thrift_create_vlan_member(self.client, vlan_oid4, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 40
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid4, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        def_addr = '0.0.0.0'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
                
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30/vlanif 40 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        ipmc_member_id3 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id4)
        
        type = SAI_IPMC_ENTRY_TYPE_SG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        #sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)                                
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
                                           
        
        warmboot(self.client)
        try:   
            
            #create L2MC member group
                       
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port2)
            l2mc_member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, port3)
            
            l2mc_grp_id3 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id3_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port2)
            l2mc_member_id3_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port3)
            l2mc_member_id3_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id3, port4)
            
            l2mc_grp_id4 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id4_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port2)
            l2mc_member_id4_2 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port3)
            l2mc_member_id4_3 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port4)
            l2mc_member_id4_4 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id4, port5)

            #create mcast fdb entry                         
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id2)

            #create SG l2mc entry    
            type = SAI_L2MC_ENTRY_TYPE_SG            
            l2mc_entry1_2 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, sip_addr1, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_2, l2mc_grp_id4) 
            
            #create XG l2mc entry
            type = SAI_L2MC_ENTRY_TYPE_XG
            l2mc_entry1_1 = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid2, dip_addr1, def_addr, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry1_1, l2mc_grp_id3) 

            sys_logging("### none ipmc entry ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])            
            
            sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
                                       
            sys_logging("### l2mc entry have high priority then mcast fdb ###")
            sys_logging("### xg and sg l2mc entry is same priority ###")
            sys_logging("### the order is fifo ###")
            
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1, exp_pkt1], [1, 2, 3, 4])
                      
            sys_logging("### remove sg l2mc entry ###")             
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1, exp_pkt1], [1, 2, 3])
            self.ctc_verify_no_packet_any(exp_pkt1, [4])
            
            sys_logging("### remove xg l2mc entry ###")             
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1], [1, 2])
            self.ctc_verify_no_packet_any(exp_pkt1, [3, 4])
            
            sys_logging("### remove mcast fdb entry ###")             
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
            
        finally:

            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
            
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
            self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id3)
            
            self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
            
            self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
            self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
            
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_1)
            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry1_2)
            
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_2)          
                    
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id3_3)
            
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_1)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_2)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_3)
            self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id4_4)
                       
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id3)
            self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id4)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)            
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_4)            
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_4)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4_4) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)




class scenario_14_l2mc_group_member_is_lag_with_mcast_fdb(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  

        lag_oid = sai_thrift_create_lag(self.client)
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port3)
                
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)

        is_lag = 1        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_UNTAGGED,is_lag)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)


        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_oid, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)
        
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        smac2 = '00:00:00:00:00:02'
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, lag_bridge_oid,is_lag)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port4)
        
        pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
                                
        pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac2,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac2,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
                                
        warmboot(self.client)
        
        try:

            sys_logging("### known multicast ###")
            
            mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id)
            
            port0_pkt_cnt = 0
            port1_pkt_cnt = 0
            
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [3], 1)
                       
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1], [1, 2])
            if rcv_idx == 1:
                port0_pkt_cnt = 1
            elif rcv_idx == 2:
                port1_pkt_cnt = 1
            
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [3], 1)
                       
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt2], [1, 2])
            if rcv_idx == 1:
                port0_pkt_cnt = port0_pkt_cnt + 1
            elif rcv_idx == 2:
                port1_pkt_cnt = port1_pkt_cnt + 1
            
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)
            
        finally:
             
            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_oid, attr)
    
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr)
        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)

            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)

            sai_thrift_remove_lag(self.client, lag_oid) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
   



class scenario_15_l2mc_group_member_is_lag_with_l2mc_entry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)  

        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        
        lag_oid = sai_thrift_create_lag(self.client)
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port3)
                
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)

        is_lag = 1        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_UNTAGGED,is_lag)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)


        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_oid, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        smac2 = '00:00:00:00:00:02'
        
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, lag_bridge_oid,is_lag)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port4)
        
        type = SAI_L2MC_ENTRY_TYPE_XG            
        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
            
        pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
                                
        pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac2,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
        
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac2,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64)
                                
        warmboot(self.client)
        
        try:

            sys_logging("### known multicast ###")
            
            status = sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)
            assert( SAI_STATUS_SUCCESS == status)
            
            port0_pkt_cnt = 0
            port1_pkt_cnt = 0
            
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [3], 1)
                       
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1], [1, 2])
            if rcv_idx == 1:
                port0_pkt_cnt = 1
            elif rcv_idx == 2:
                port1_pkt_cnt = 1
            
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( exp_pkt2, [3], 1)
                       
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt2], [1, 2])
            if rcv_idx == 1:
                port0_pkt_cnt = port0_pkt_cnt + 1
            elif rcv_idx == 2:
                port1_pkt_cnt = port1_pkt_cnt + 1
            
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)
            
        finally:
             

            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            
            self.client.sai_thrift_remove_l2mc_group_member(member_id1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2)
            
            self.client.sai_thrift_remove_l2mc_group(grp_id)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_oid, attr)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            
            sai_thrift_remove_lag(self.client, lag_oid) 
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
   


class scenario_16_ipmc_group_member_is_lag(sai_base_test.ThriftInterfaceDataPlane):
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
        
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        
        grp_attr_list = []
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)

        lag_oid1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid1, port2)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid1, port3)               
        lag_bridge_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_oid1)        

        lag_oid2 = sai_thrift_create_lag(self.client)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_oid2, port4)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_oid2, port5)               
        lag_bridge_oid2 = sai_thrift_create_bport_by_lag(self.client, lag_oid2) 
        
        # vlan 10 member list
        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)        
        
        # vlan 20 member list
        is_lag = 1
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, lag_bridge_oid1, SAI_VLAN_TAGGING_MODE_TAGGED, is_lag)
        
        #vlan 30 member list
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, lag_bridge_oid2, SAI_VLAN_TAGGING_MODE_TAGGED, is_lag)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
       
        #create L3if ,vlan if 10
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, mac)

        v4_mcast_enable = 1 
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        
        #create L3if ,vlan if 20
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, mac)
        
        #create L3if ,vlan if 30
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, mac)
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr1 = '224.1.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:01:01:01'
        smac1 = '00:00:00:00:00:01'        
        smac2 = '00:00:00:00:00:02'                 
        #cgreat RPF member group
        rpf_grp_id = self.client.sai_thrift_create_rpf_group(grp_attr_list)
        rpf_member_id1 = sai_thrift_create_rpf_group_member(self.client, rpf_grp_id, rif_id1)  
        
        #create IPMC group ,and add vlanif 20/vlanif 30 to group   
        ipmc_grp_id = self.client.sai_thrift_create_ipmc_group(grp_attr_list) 
        ipmc_member_id1 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id2)
        ipmc_member_id2 = sai_thrift_create_ipmc_group_member(self.client, ipmc_grp_id, rif_id3)
        
        type = SAI_IPMC_ENTRY_TYPE_XG
        
        #create (*,225.1.1.1 VRF1) ipmc entry,and add group5 to entry
        ipmc_entry1 = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr1, sip_addr1, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry1, ipmc_grp_id, SAI_PACKET_ACTION_FORWARD, rpf_grp_id)
               
        pkt = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac1,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=smac2,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=64,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1)
                                
        exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2)
        exp_pkt2 = simple_tcp_packet(eth_dst=dmac1,
                                eth_src=router_mac,
                                ip_dst=dip_addr1,
                                ip_src=sip_addr1,
                                ip_id=105,
                                ip_ttl=63,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3)
        warmboot(self.client)
        try:   

            sys_logging("### bind none ###")             
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet_any(exp_pkt1, [0,1,2,3,4])
                     
            type = SAI_L2MC_ENTRY_TYPE_XG   
            
            #create L2MC member group
            l2mc_grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id1, lag_bridge_oid1, is_lag)
            
            l2mc_grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
            l2mc_member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, l2mc_grp_id2, lag_bridge_oid2, is_lag)

                       
            #create ( '01:00:5E:01:01:01' ,Vlan 20/30) mcast fdb entry
                           
            mcast_fdb_entry_2 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid2)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_2, l2mc_grp_id1)
            
            mcast_fdb_entry_3 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid3)
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry_3, l2mc_grp_id2)        
                               
            sys_logging("### bind mcast fdb entry ###")             

            port0_pkt_cnt = 0
            port1_pkt_cnt = 0
            port2_pkt_cnt = 0
            port3_pkt_cnt = 0
            
            self.ctc_send_packet( 0, str(pkt))
                       
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1], [1, 2])
            if rcv_idx == 1:
                port0_pkt_cnt = port0_pkt_cnt + 1
            elif rcv_idx == 2:
                port1_pkt_cnt = port1_pkt_cnt + 1

            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt2], [3, 4])
            if rcv_idx == 3:
                port2_pkt_cnt = port2_pkt_cnt + 1
            elif rcv_idx == 4:
                port3_pkt_cnt = port3_pkt_cnt + 1
                
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)
            sys_logging("port 2 receive packet conut is %d" %port2_pkt_cnt)
            sys_logging("port 3 receive packet conut is %d" %port3_pkt_cnt)
            

            self.ctc_send_packet( 0, str(pkt2))
                       
            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1], [1, 2])
            if rcv_idx == 1:
                port0_pkt_cnt = port0_pkt_cnt + 1
            elif rcv_idx == 2:
                port1_pkt_cnt = port1_pkt_cnt + 1

            rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt2], [3, 4])
            if rcv_idx == 3:
                port2_pkt_cnt = port2_pkt_cnt + 1
            elif rcv_idx == 4:
                port3_pkt_cnt = port3_pkt_cnt + 1
                
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)
            sys_logging("port 2 receive packet conut is %d" %port2_pkt_cnt)
            sys_logging("port 3 receive packet conut is %d" %port3_pkt_cnt)
            
        finally:
           

           self.client.sai_thrift_remove_ipmc_entry(ipmc_entry1)
           
           self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id1)
           self.client.sai_thrift_remove_ipmc_group_member(ipmc_member_id2)
           
           self.client.sai_thrift_remove_ipmc_group(ipmc_grp_id)
           
           self.client.sai_thrift_remove_rpf_group_member(rpf_member_id1)
           self.client.sai_thrift_remove_rpf_group(rpf_grp_id)
           
           self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_2)
           self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry_3)
           
           self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id1_1)           
           self.client.sai_thrift_remove_l2mc_group_member(l2mc_member_id2_1)
          
           self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id1)
           self.client.sai_thrift_remove_l2mc_group(l2mc_grp_id2)
           
           self.client.sai_thrift_remove_router_interface(rif_id1)
           self.client.sai_thrift_remove_router_interface(rif_id2)
           self.client.sai_thrift_remove_router_interface(rif_id3)
           
           self.client.sai_thrift_remove_virtual_router(vr_id)
            
           self.client.sai_thrift_remove_vlan_member(vlan_member1_1)          
           self.client.sai_thrift_remove_vlan_member(vlan_member2_1)

           sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid1)            
           sai_thrift_remove_lag_member(self.client, lag_member_id1)
           sai_thrift_remove_lag_member(self.client, lag_member_id2)
           sai_thrift_remove_lag(self.client, lag_oid1) 

           sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid2)            
           sai_thrift_remove_lag_member(self.client, lag_member_id3)
           sai_thrift_remove_lag_member(self.client, lag_member_id4)
           sai_thrift_remove_lag(self.client, lag_oid2)
           
           self.client.sai_thrift_remove_vlan(vlan_oid1)
           self.client.sai_thrift_remove_vlan(vlan_oid2)
           self.client.sai_thrift_remove_vlan(vlan_oid3)

            