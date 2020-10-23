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
Thrift SAI FDB interface tests
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
    
@group('L2')
class func_01(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
                       
        switch_init(self.client)  
        
        # step1: config vlan
        vlan_oid_list = []
        vlan_oid_list = config_vlan(self.client,32)
        
        # step2: config bridge port
        # already create for saiserver init
        
        # step3: config vlan member
        port_vlan_member_list = range(len(port_list))
        for a in range(0,len(port_list)):
            port_vlan_member_list[a] = config_port_vlan_member(self.client,port_list[a],vlan_oid_list)        
        
        # step4: config fdb entry 
        status = SAI_STATUS_SUCCESS
        macda = '00:00:00:00:00:01'        
        status = config_fdb_test(self.client,vlan_oid_list,macda,port_list,32)
        assert (status == SAI_STATUS_SUCCESS)
        
        warmboot(self.client)        

        # step5: send packet and verify        
        try:
        
            macsa = '00:00:00:00:00:02'        
            vlan_id = range(2,34,1)
            pkt = range(32)
        
            for a in range(0,32):
                pkt[a] = simple_tcp_packet(eth_dst=macda,
                                    eth_src=macsa,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id[a],
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)
                                    
                self.ctc_send_packet(31-a, str(pkt[a]))    
                self.ctc_verify_packets( str(pkt[a]), [a], 1)
            
        finally:

            # step6: delete fdb entry 
            flush_all_fdb(self.client)           
                      
            # step7: delete vlan member
            for a in range(0,len(port_list)):
                delete_port_vlan_member(self.client,port_vlan_member_list[a])             

            # step8: delete vlan
            delete_vlan(self.client,vlan_oid_list)

class casenum(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        #print()
        import os
        import re
        import glob
        print("It's only a test!")
        switch_init(self.client)
        filelist = []
        num_list = []
        s = 0
        allfiles = os.listdir(os.getcwd())
        print allfiles
        for filename in allfiles:
            if re.match(r'.*sai.*.py$',filename):
                filelist.append(filename)
        for file in filelist:
            fobj = open(file, 'r').read()
            words = re.findall('class',fobj)
            num = len(words)
            num_list.append(num)
            #fobj.close()
        for i in range(len(num_list)):
            print "%s case num is %d" %(filelist[i], num_list[i])
            s = s + num_list[i]
        print 'total case num is %d' %s   



class func_02(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
                       
        switch_init(self.client)  
        
        # step1: config vlan
        vlan_oid_list = []
        vlan_oid_list = config_vlan(self.client,32)
        
        # step2: config bridge port
        # already create for saiserver init
        
        # step3: config vlan member
        port_vlan_member_list = range(len(port_list))
        for a in range(0,len(port_list)):
            port_vlan_member_list[a] = config_port_vlan_member(self.client,port_list[a],vlan_oid_list)        
        
        # step4: config stp port 
        vlan_list = []
        stp_oid1 = sai_thrift_create_stp_entry(self.client, vlan_list)
        stp_oid2 = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        a = vlan_oid_list[0:16]
        b = vlan_oid_list[16:32]
        config_stp_instance(self.client,stp_oid1,a)
        config_stp_instance(self.client,stp_oid2,b)

        stp_port_list1 = range(32)   
        stp_port_list2 = range(32)
        
        for c in range(0,len(port_list)):      
            state = SAI_STP_PORT_STATE_FORWARDING
            stp_port_list1[c] = sai_thrift_create_stp_port(self.client, stp_oid1, port_list[c], state)

        for c in range(0,len(port_list)):      
            state = SAI_STP_PORT_STATE_BLOCKING
            stp_port_list2[c] = sai_thrift_create_stp_port(self.client, stp_oid2, port_list[c], state)
            
        # step5: config fdb entry 
        status = SAI_STATUS_SUCCESS
        macda = '00:00:00:00:00:01'        
        status = config_fdb_test(self.client,vlan_oid_list,macda,port_list,32)
        assert (status == SAI_STATUS_SUCCESS)
        
        warmboot(self.client)        

        # step6: send packet and verify        
        try:
        
            macsa = '00:00:00:00:00:02'        
            vlan_id = range(2,34,1)
            pkt = range(32)
        
            for a in range(0,32):
                pkt[a] = simple_tcp_packet(eth_dst=macda,
                                    eth_src=macsa,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id[a],
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)
                if ( a <= 15 ):                   
                    self.ctc_send_packet(31-a, str(pkt[a]))    
                    self.ctc_verify_packets( str(pkt[a]), [a], 1)
                else:
                    self.ctc_send_packet(31-a, str(pkt[a])) 
                    self.ctc_verify_no_packet(str(pkt[a]), a)                                        
            
        finally:

            # step7: delete fdb entry 
            flush_all_fdb(self.client)           
            
            # step8: delete stp port 
            for a in stp_port_list1:
                self.client.sai_thrift_remove_stp_port(a)
            for a in stp_port_list2:
                self.client.sai_thrift_remove_stp_port(a)
            
            # step9: delete vlan member
            for a in range(0,len(port_list)):
                delete_port_vlan_member(self.client,port_vlan_member_list[a])             
            
            # step10: delete vlan
            delete_vlan(self.client,vlan_oid_list)
            
            # step11: delete stp instance
            self.client.sai_thrift_remove_stp_entry(stp_oid1) 
            self.client.sai_thrift_remove_stp_entry(stp_oid2)            



class func_03(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
                       
        switch_init(self.client)  
        
        # step1: config vlan
        vlan_oid_list = []
        vlan_oid_list = config_vlan(self.client,32)
        
        # step2: config bridge port
        # already create for saiserver init
        
        # step3: config vlan member
        port_vlan_member_list = range(len(port_list))
        for a in range(0,len(port_list)):
            port_vlan_member_list[a] = config_port_vlan_member(self.client,port_list[a],vlan_oid_list)        
        
        # step4: config vlanif         
        v4_enabled = 1
        v6_enabled = 1
        mac = ''        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        rif_id_list = range(32)
        for a in range(0,32):
            rif_id_list[a] = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid_list[a], v4_enabled, v6_enabled, mac)

        # step5: config neighbor  
        addr_family=SAI_IP_ADDR_FAMILY_IPV4
        dmac1 =  '00:00:00:00:00:01'                
        for a in range(0,32):
            ip_addr = '10.1.'
            subnet = str(a)
            ip_addr = ip_addr + subnet + '.1'
            sai_thrift_create_neighbor(self.client, addr_family, rif_id_list[a], ip_addr, dmac1)

        # step6: config route
        for a in range(0,32):       
            ip_addr_subnet = '10.1.'
            subnet = str(a)
            ip_addr_subnet = ip_addr_subnet + subnet + '.0'            
            ip_mask = '255.255.255.0'
            sai_thrift_create_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet, ip_mask, rif_id_list[a])

        # step7: config fdb entry 
        macda = dmac1        
        status = config_fdb_test(self.client,vlan_oid_list,macda,port_list,32)
        
        warmboot(self.client)        

        # step8: send packet and verify        
        try:
        
            route_mac = '00:77:66:55:44:00'
            macsa = '00:00:00:00:00:02'        
            vlan_id = range(2,34,1)
            pkt = range(32)
        
            for a in range(0,32,2):
                
                ip_addr = '10.1.'
                subnet = str(a+1)
                ip_addr = ip_addr + subnet + '.1'
            
                pkt[a] = simple_tcp_packet(eth_dst=route_mac,
                                    eth_src=macsa,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id[a],
                                    ip_dst=ip_addr,
                                    ip_id=101,
                                    ip_ttl=64) 

                pkt[a+1] = simple_tcp_packet(eth_dst=dmac1,
                                    eth_src=route_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id[a+1],
                                    ip_dst=ip_addr,
                                    ip_id=101,
                                    ip_ttl=63)
                                    
                self.ctc_send_packet(a, str(pkt[a]))    
                self.ctc_verify_packets( str(pkt[a+1]), [a+1], 1)                                       
           
        finally:

           # step9: delete fdb entry 
           flush_all_fdb(self.client)           

           # step10: delete route
           for a in range(0,32):       
               ip_addr_subnet = '10.1.'
               subnet = str(a)
               ip_addr_subnet = ip_addr_subnet + subnet + '.0'            
               ip_mask = '255.255.255.0'
               sai_thrift_remove_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet, ip_mask, rif_id_list[a])           

           # step11: delete neighbor
           addr_family=SAI_IP_ADDR_FAMILY_IPV4
           dmac1 =  '00:00:00:00:00:01'                
           for a in range(0,32):
               ip_addr = '10.1.'
               subnet = str(a)
               ip_addr = ip_addr + subnet + '.1'
               sai_thrift_remove_neighbor(self.client, addr_family, rif_id_list[a], ip_addr, dmac1)           

           # step12: delete vlanif and vrf 
           for a in range(0,32):              
               self.client.sai_thrift_remove_router_interface(rif_id_list[a])
           
           self.client.sai_thrift_remove_virtual_router(vr_id)
            
           # step13: delete vlan member
           for a in range(0,len(port_list)):
               delete_port_vlan_member(self.client,port_vlan_member_list[a])             
           
           # step14: delete vlan
           delete_vlan(self.client,vlan_oid_list)
        



class func_04(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
                       
        switch_init(self.client)  
        
        # step1: config bridge
        bridge_id_list = range(32)
        for a in bridge_id_list:
            bridge_id_list[a] = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        
        # step2: config sub port
        vlan_id1 = 10
        vlan_id2 = 20
        sub_port1 = range(2)
        sub_port2 = range(2)         
        sub_port_list = range(len(port_list))
        
        for a in range(0,len(port_list),2):   
        
            sub_port1[0] = sai_thrift_create_bridge_sub_port(self.client, port_list[a], bridge_id_list[a], vlan_id1)
            sub_port1[1] = sai_thrift_create_bridge_sub_port(self.client, port_list[a], bridge_id_list[a+1], vlan_id2)
            sub_port_list[a] = copy.deepcopy(sub_port1)
            sub_port2[0] = sai_thrift_create_bridge_sub_port(self.client, port_list[a+1], bridge_id_list[a], vlan_id2)
            sub_port2[1] = sai_thrift_create_bridge_sub_port(self.client, port_list[a+1], bridge_id_list[a+1], vlan_id1)
            sub_port_list[a+1] = copy.deepcopy(sub_port2)            
                
        warmboot(self.client)        

        # step3: send packet and verify        
        try:
        
            macda = '00:00:00:00:00:02'        
            macsa = '00:00:00:00:00:01'        
            pkt = range(2)
            pkt[0] = simple_tcp_packet(eth_dst=macda,
                                eth_src=macsa,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
    
            pkt[1] = simple_tcp_packet(eth_dst=macda,
                                eth_src=macsa,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
            for a in range(0,len(port_list),2):            
                                   
                self.ctc_send_packet(a, str(pkt[0]))    
                self.ctc_verify_packets( str(pkt[1]), [a+1], 1)
                
                self.ctc_send_packet(a+1, str(pkt[1]))    
                self.ctc_verify_packets( str(pkt[0]), [a], 1)
                
        finally:
        
            # step4: delete fdb entry 
            flush_all_fdb(self.client) 
            
            # step5: delete sub port and create bridge port            
            bport_attr_admin_state_value = sai_thrift_attribute_value_t(booldata=False)
            bport_attr_admin_state = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                            value=bport_attr_admin_state_value)                                                    
            for a in sub_port_list:
                for b in a:
                    self.client.sai_thrift_set_bridge_port_attribute(b, bport_attr_admin_state)
                    self.client.sai_thrift_remove_bridge_port(b)
                       
            for a in range(0,len(port_list)): 
                sai_thrift_create_bridge_port(self.client, port_list[a])
                
            # step6: delete brideg
            for a in bridge_id_list:
                self.client.sai_thrift_remove_bridge(a)




class func_05(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
                       
        switch_init(self.client)  
        
        # step1: config bridge
        bridge_id_list = range(32)
        for a in bridge_id_list:
            bridge_id_list[a] = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        
        # step2: config sub port
        vlan_id1 = 10
        vlan_id2 = 20
        sub_port1 = range(2)
        sub_port2 = range(2)         
        sub_port_list = range(len(port_list))
        
        for a in range(0,len(port_list),2):   
        
            sub_port1[0] = sai_thrift_create_bridge_sub_port(self.client, port_list[a], bridge_id_list[a], vlan_id1)
            sub_port1[1] = sai_thrift_create_bridge_sub_port(self.client, port_list[a], bridge_id_list[a+1], vlan_id2)
            sub_port_list[a] = copy.deepcopy(sub_port1)
            sub_port2[0] = sai_thrift_create_bridge_sub_port(self.client, port_list[a+1], bridge_id_list[a], vlan_id2)
            sub_port2[1] = sai_thrift_create_bridge_sub_port(self.client, port_list[a+1], bridge_id_list[a+1], vlan_id1)
            sub_port_list[a+1] = copy.deepcopy(sub_port2)            

        # step3: config vrf
        v4_enabled = 1
        v6_enabled = 1
        mac = ''        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        # step4: config 1d router bridge port and bridge l3if
        bridge_l3if_oid_list = range(len(port_list))
        bridge_port_list_1d = range(len(port_list))        
        for a in range(0,len(port_list)):                        
            bridge_l3if_oid_list[a] = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, mac)        
            bridge_port_list_1d[a] = sai_thrift_create_bridge_rif_port(self.client, bridge_id_list[a], bridge_l3if_oid_list[a])

        # step5: config neighbor  
        addr_family=SAI_IP_ADDR_FAMILY_IPV4
        dmac1 =  '00:00:00:00:00:01'        
        for a in range(0,len(port_list)):
            ip_addr = '10.1.'
            subnet = str(a)
            ip_address_1 = ip_addr + subnet + '.1'              
            sai_thrift_create_neighbor(self.client, addr_family, bridge_l3if_oid_list[a], ip_address_1, dmac1)
            
        # step6: config route
        for a in range(0,len(port_list)):       
            ip_addr_subnet = '10.1.'
            subnet = str(a)
            ip_addr_subnet = ip_addr_subnet + subnet + '.0'            
            ip_mask = '255.255.255.0'
            sai_thrift_create_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet, ip_mask, bridge_l3if_oid_list[a])

        # step7: config fdb entry 
        mac_action = SAI_PACKET_ACTION_FORWARD
        temp_list = range(2)
        type = SAI_FDB_ENTRY_TYPE_STATIC
        for a in range(0,len(port_list),2): 
            temp_list = sub_port_list[a]
            sai_thrift_create_fdb_subport(self.client, bridge_id_list[a],dmac1 ,temp_list[0], mac_action, type)
            sai_thrift_create_fdb_subport(self.client, bridge_id_list[a+1],dmac1 ,temp_list[1], mac_action, type)
            
        warmboot(self.client)        

        # step8: send packet and verify         
        try:
        
            route_mac = '00:77:66:55:44:00'
            macsa = '00:00:00:00:00:01'
            pkt = range(32)
            
            for a in range(0,32,2):
                
                ip_addr = '10.1.'
                subnet = str(a+1)
                ip_addr = ip_addr + subnet + '.1'
            
                pkt[a] = simple_tcp_packet(eth_dst=route_mac,
                                    eth_src=macsa,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id1,
                                    ip_dst=ip_addr,
                                    ip_id=101,
                                    ip_ttl=64) 

                pkt[a+1] = simple_tcp_packet(eth_dst=dmac1,
                                    eth_src=route_mac,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id2,
                                    ip_dst=ip_addr,
                                    ip_id=101,
                                    ip_ttl=63)
                                    
                self.ctc_send_packet(a, str(pkt[a]))    
                self.ctc_verify_packets( str(pkt[a+1]), [a], 1)


                
        finally:

            # step9: delete fdb entry 
            flush_all_fdb(self.client) 

            # step10: delete route
            for a in range(0,len(port_list)):       
                ip_addr_subnet = '10.1.'
                subnet = str(a)
                ip_addr_subnet = ip_addr_subnet + subnet + '.0'            
                ip_mask = '255.255.255.0'
                sai_thrift_remove_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet, ip_mask, bridge_l3if_oid_list[a])         
            
            # step11: delete neighbor             
            for a in range(0,len(port_list)):
                ip_addr = '10.1.'
                subnet = str(a)
                ip_address_1 = ip_addr + subnet + '.1'              
                sai_thrift_remove_neighbor(self.client, addr_family, bridge_l3if_oid_list[a], ip_address_1, dmac1)          
            
            # step12: delete l3if and 1d route bridge port and vrf 
                        
            for a in range(0,len(port_list)): 
                self.client.sai_thrift_remove_bridge_port(bridge_port_list_1d[a])            
                self.client.sai_thrift_remove_router_interface(bridge_l3if_oid_list[a])
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            # step13: delete sub port and create bridge port            
            bport_attr_admin_state_value = sai_thrift_attribute_value_t(booldata=False)
            bport_attr_admin_state = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,
                                            value=bport_attr_admin_state_value)                                                    
            for a in sub_port_list:
                for b in a:
                    self.client.sai_thrift_set_bridge_port_attribute(b, bport_attr_admin_state)
                    self.client.sai_thrift_remove_bridge_port(b)
                       
            for a in range(0,len(port_list)): 
                sai_thrift_create_bridge_port(self.client, port_list[a])
                
            # step14: delete brideg
            for a in bridge_id_list:
                self.client.sai_thrift_remove_bridge(a)


class func_06(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
                       
        switch_init(self.client)  
        
        # step1: config vlan
        vlan_oid_list = []
        vlan_oid_list = config_vlan(self.client,32)
        
        # step2: config bridge port
        # already create for saiserver init
        
        # step3: config vlan member
        port_vlan_member_list = range(len(port_list))
        for a in range(0,len(port_list)):
            port_vlan_member_list[a] = config_port_vlan_member(self.client,port_list[a],vlan_oid_list)        

        # step4: config l2mc group and member            
        grp_attr_list = []
        grp_id_list = range(len(port_list)) 
        for a in range(0,len(port_list)):        
            grp_id_list[a] = self.client.sai_thrift_create_l2mc_group(grp_attr_list)

        grp_member_list = range(0,len(port_list))        
        for a in range(0,len(port_list)):
                grp_member_list[a] = sai_thrift_create_l2mc_group_member(self.client, grp_id_list[a], port_list[len(port_list)-a-1])

        # step5: config mcast fdb entry
        dmac1 = '01:00:5E:7F:01:01'       
        for a in range(0,len(port_list)):        
            mcast_fdb_entry1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid_list[a])
            sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry1, grp_id_list[a])
       
        warmboot(self.client)        

        # step6: send packet and verify        
        try:
        
            macsa = '00:00:00:00:00:01' 
            
            vlan_id = range(2,34,1)
            pkt = range(32)
        
            for a in range(0,32):
                pkt[a] = simple_tcp_packet(eth_dst=dmac1,
                                    eth_src=macsa,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id[a],
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)
                                    
                self.ctc_send_packet(0, str(pkt[a]))
                if ( a != 31):
                    self.ctc_verify_packets( str(pkt[a]), [31-a], 1)
                else:
                    self.ctc_verify_no_packet(str(pkt[a]), 31-a)                     
            
        finally:

            # step7: delete fdb entry 
            flush_all_fdb(self.client)           
            
            # step8: delete mcast fdb entry
            for a in range(0,len(port_list)):        
                mcast_fdb_entry1 = sai_thrift_mcast_fdb_entry_t(mac_address=dmac1, bv_id=vlan_oid_list[a])          
                self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry1)
            
            # step9: delete l2mc group and member
            for a in range(0,len(port_list)):        
                self.client.sai_thrift_remove_l2mc_group_member(grp_member_list[a])
                self.client.sai_thrift_remove_l2mc_group(grp_id_list[a])
            
            # step10: delete vlan member
            for a in range(0,len(port_list)):
                delete_port_vlan_member(self.client,port_vlan_member_list[a])             
            
            # step11: delete vlan
            delete_vlan(self.client,vlan_oid_list)



class func_07(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
                       
        switch_init(self.client)  
        
        # step1: config vlan
        vlan_oid_list = []
        vlan_oid_list = config_vlan(self.client,32)

        attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)        
        for a in vlan_oid_list:
            self.client.sai_thrift_set_vlan_attribute(a, attr)
        
        # step2: config bridge port
        # already create for saiserver init
        
        # step3: config vlan member
        port_vlan_member_list = range(len(port_list))
        for a in range(0,len(port_list)):
            port_vlan_member_list[a] = config_port_vlan_member(self.client,port_list[a],vlan_oid_list)        

        # step4: config l2mc group and member            
        grp_attr_list = []
        grp_id_list = range(len(port_list)) 
        for a in range(0,len(port_list)):        
            grp_id_list[a] = self.client.sai_thrift_create_l2mc_group(grp_attr_list)

        grp_member_list = range(0,len(port_list))        
        for a in range(0,len(port_list)):
                grp_member_list[a] = sai_thrift_create_l2mc_group_member(self.client, grp_id_list[a], port_list[len(port_list)-a-1])

        # step5: config l2mc entry
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1' 
        sip_addr1 = '10.1.1.1'        
        dmac1 = '01:00:5E:7F:01:01'
        type = SAI_L2MC_ENTRY_TYPE_XG
        for a in range(0,len(port_list)):         
            l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid_list[a], dip_addr1, default_addr, type)
            sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id_list[a]) 
       
        warmboot(self.client)        

        # step6: send packet and verify        
        try:
        
            macsa = '00:00:00:00:00:01'            
            vlan_id = range(2,34,1)
            pkt = range(32)
        
            for a in range(0,32):
                pkt[a] = simple_tcp_packet(eth_dst=dmac1,
                                        eth_src=macsa,
                                        ip_dst=dip_addr1,
                                        ip_src=sip_addr1,
                                        ip_id=105,
                                        ip_ttl=64,
                                        dl_vlan_enable=True,
                                        vlan_vid=vlan_id[a])
                                
                self.ctc_send_packet(0, str(pkt[a]))
                if ( a != 31):
                    self.ctc_verify_packets( str(pkt[a]), [31-a], 1)
                    self.ctc_verify_no_packet(str(pkt[a]), 30-a)
                else:
                    self.ctc_verify_no_packet(str(pkt[a]), 31-a)                     
            
        finally:

            # step7: delete fdb entry 
            flush_all_fdb(self.client)           
            
            # step8: delete l2mc entry
            for a in range(0,len(port_list)):        
                l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid_list[a], dip_addr1, default_addr, type)
                self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
        
            # step9: delete l2mc group and member
            for a in range(0,len(port_list)):        
                self.client.sai_thrift_remove_l2mc_group_member(grp_member_list[a])
                self.client.sai_thrift_remove_l2mc_group(grp_id_list[a])
            
            # step10: delete vlan member
            for a in range(0,len(port_list)):
                delete_port_vlan_member(self.client,port_vlan_member_list[a])             
            
            # step11: delete vlan
            delete_vlan(self.client,vlan_oid_list)



class func_08(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        port7 = port_list[6]
        port8 = port_list[7]
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        v4_enabled = 1
        v6_enabled = 1
        
        
        dmac = ['00:00:11:11:22:01', '00:00:11:11:22:02', '00:00:11:11:22:03', '00:00:11:11:22:04', '00:00:11:11:22:05', '00:00:11:11:22:06', '00:00:11:11:22:07', '00:00:11:11:22:08', '00:00:11:11:22:09', '00:00:11:11:22:10', '00:00:11:11:22:11', '00:00:11:11:22:12']
        l3if_mac = ['00:00:77:77:77:01','00:00:77:77:77:02','00:00:77:77:77:03','00:00:77:77:77:04','00:00:77:77:77:05','00:00:77:77:77:06','00:00:77:77:77:07','00:00:77:77:77:08','00:00:77:77:77:09']
        l3if_dmac = [dmac[0], dmac[4], dmac[8], dmac[10], '00:00:11:11:33:01', '00:00:11:11:33:02', '00:00:11:11:33:03', '00:00:11:11:33:04', '00:00:11:11:33:05']
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        addr_family_v6 = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = ['10.10.10.1', '10.10.10.2', '10.10.10.3', '10.10.10.4', '10.10.10.5', '10.10.10.6', '10.10.10.7', '10.10.10.8', '10.10.10.9']
        ip_addr_v6 = ['::7700:7701', '::7700:7702', '::7700:7703', '::7700:7704', '::7700:7705', '::7700:7706', '::7700:7707', '::7700:7708', '::7700:7709']
        ip_addr1_subnet = ['20.10.10.0', '20.10.20.0', '20.10.30.0', '20.10.40.0', '20.10.50.0', '20.10.60.0', '20.10.70.0', '20.10.80.0', '20.10.90.0', '20.70.10.0']
        ip_mask1 = '255.255.255.0'
        ip_addr_subnet_v6 = ['2001::1100', '2001::2200', '2001::3300', '2001::4400', '2001::5500', '2001::6600', '2001::7700', '2001::8800', '2001::9900']
        ip_mask_v6 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ff00'

        #vlan&vlan member
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)

        vlan_member1_1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member1_2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member1_3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_1 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2_3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_1 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_2 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3_3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        #1d bridge&sub port
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port4])
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port5])
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port5, bridge_id1, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port5, bridge_id1, vlan_id1)

        #fdb(vlan)
        sai_thrift_create_fdb(self.client, vlan_oid1, dmac[0], port1, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oid1, dmac[1], port2, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oid1, dmac[2], port3, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oid2, dmac[3], port1, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oid2, dmac[4], port2, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oid2, dmac[5], port3, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oid3, dmac[6], port1, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oid3, dmac[7], port2, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb(self.client, vlan_oid3, dmac[8], port3, SAI_PACKET_ACTION_FORWARD)

        #fdb(bridge)
        sai_thrift_create_fdb_bport(self.client, bridge_id1, dmac[9], sub_port_id1, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb_bport(self.client, bridge_id1, dmac[10], sub_port_id2, SAI_PACKET_ACTION_FORWARD)
        sai_thrift_create_fdb_bport(self.client, bridge_id1, dmac[11], sub_port_id3, SAI_PACKET_ACTION_FORWARD)

        #virtual router
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        #router interface
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid1, v4_enabled, v6_enabled, l3if_mac[0])
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid2, v4_enabled, v6_enabled, l3if_mac[1])
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid3, v4_enabled, v6_enabled, l3if_mac[2])
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, l3if_mac[3])
        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id1, rif_id4)
        rif_id5 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port6, 0, v4_enabled, v6_enabled, l3if_mac[4], outer_vlan_id=vlan_id1)
        rif_id6 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port6, 0, v4_enabled, v6_enabled, l3if_mac[5], outer_vlan_id=vlan_id2)
        rif_id7 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port6, 0, v4_enabled, v6_enabled, l3if_mac[6], outer_vlan_id=vlan_id3)
        rif_id8 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port7, 0, v4_enabled, v6_enabled, l3if_mac[7])
        rif_id9 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port8, 0, v4_enabled, v6_enabled, l3if_mac[8])

        v4_mcast_enable = 1
        attr_value = sai_thrift_attribute_value_t(booldata=v4_mcast_enable)
        attr = sai_thrift_attribute_t(id=SAI_ROUTER_INTERFACE_ATTR_V4_MCAST_ENABLE, value=attr_value)
        self.client.sai_thrift_set_router_interface_attribute(rif_id1, attr)
        self.client.sai_thrift_set_router_interface_attribute(rif_id2, attr)
        self.client.sai_thrift_set_router_interface_attribute(rif_id3, attr)
        #self.client.sai_thrift_set_router_interface_attribute(rif_id4, attr)
        self.client.sai_thrift_set_router_interface_attribute(rif_id5, attr)
        self.client.sai_thrift_set_router_interface_attribute(rif_id6, attr)
        self.client.sai_thrift_set_router_interface_attribute(rif_id7, attr)
        self.client.sai_thrift_set_router_interface_attribute(rif_id8, attr)
        self.client.sai_thrift_set_router_interface_attribute(rif_id9, attr)

        #neighbor(v4)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1[0], l3if_dmac[0])
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1[1], l3if_dmac[1])
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_addr1[2], l3if_dmac[2])
        sai_thrift_create_neighbor(self.client, addr_family, rif_id4, ip_addr1[3], l3if_dmac[3])
        sai_thrift_create_neighbor(self.client, addr_family, rif_id5, ip_addr1[4], l3if_dmac[4])
        sai_thrift_create_neighbor(self.client, addr_family, rif_id6, ip_addr1[5], l3if_dmac[5])
        sai_thrift_create_neighbor(self.client, addr_family, rif_id7, ip_addr1[6], l3if_dmac[6])
        sai_thrift_create_neighbor(self.client, addr_family, rif_id8, ip_addr1[7], l3if_dmac[7])
        sai_thrift_create_neighbor(self.client, addr_family, rif_id9, ip_addr1[8], l3if_dmac[8])

        #nexthop(v4)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1[0], rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1[1], rif_id2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1[2], rif_id3)
        nhop4 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1[3], rif_id4)
        nhop5 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1[4], rif_id5)
        nhop6 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1[5], rif_id6)
        nhop7 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1[6], rif_id7)
        nhop8 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1[7], rif_id8)
        nhop9 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1[8], rif_id9)

        #nexthop group(ecmp)
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop8)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop9)

        hash_id_ecmp = 0x1C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        #route(v4)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet[0], ip_mask1, nhop1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet[1], ip_mask1, nhop2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet[2], ip_mask1, nhop3)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet[3], ip_mask1, nhop4)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet[4], ip_mask1, nhop5)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet[5], ip_mask1, nhop6)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet[6], ip_mask1, nhop7)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet[7], ip_mask1, nhop8)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet[8], ip_mask1, nhop9)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet[9], ip_mask1, nhop_group1)

        #neighbor(v6)
        sai_thrift_create_neighbor(self.client, addr_family_v6, rif_id1, ip_addr_v6[0], l3if_dmac[0])
        sai_thrift_create_neighbor(self.client, addr_family_v6, rif_id2, ip_addr_v6[1], l3if_dmac[1])
        sai_thrift_create_neighbor(self.client, addr_family_v6, rif_id3, ip_addr_v6[2], l3if_dmac[2])
        sai_thrift_create_neighbor(self.client, addr_family_v6, rif_id4, ip_addr_v6[3], l3if_dmac[3])
        sai_thrift_create_neighbor(self.client, addr_family_v6, rif_id5, ip_addr_v6[4], l3if_dmac[4])
        sai_thrift_create_neighbor(self.client, addr_family_v6, rif_id6, ip_addr_v6[5], l3if_dmac[5])
        sai_thrift_create_neighbor(self.client, addr_family_v6, rif_id7, ip_addr_v6[6], l3if_dmac[6])
        sai_thrift_create_neighbor(self.client, addr_family_v6, rif_id8, ip_addr_v6[7], l3if_dmac[7])
        sai_thrift_create_neighbor(self.client, addr_family_v6, rif_id9, ip_addr_v6[8], l3if_dmac[8])

        #nexthop(v6)
        nhop11 = sai_thrift_create_nhop(self.client, addr_family_v6, ip_addr_v6[0], rif_id1)
        nhop12 = sai_thrift_create_nhop(self.client, addr_family_v6, ip_addr_v6[1], rif_id2)
        nhop13 = sai_thrift_create_nhop(self.client, addr_family_v6, ip_addr_v6[2], rif_id3)
        nhop14 = sai_thrift_create_nhop(self.client, addr_family_v6, ip_addr_v6[3], rif_id4)
        nhop15 = sai_thrift_create_nhop(self.client, addr_family_v6, ip_addr_v6[4], rif_id5)
        nhop16 = sai_thrift_create_nhop(self.client, addr_family_v6, ip_addr_v6[5], rif_id6)
        nhop17 = sai_thrift_create_nhop(self.client, addr_family_v6, ip_addr_v6[6], rif_id7)
        nhop18 = sai_thrift_create_nhop(self.client, addr_family_v6, ip_addr_v6[7], rif_id8)
        nhop19 = sai_thrift_create_nhop(self.client, addr_family_v6, ip_addr_v6[8], rif_id9)

        #route(v6)
        sai_thrift_create_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[0], ip_mask_v6, nhop11)
        sai_thrift_create_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[1], ip_mask_v6, nhop12)
        sai_thrift_create_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[2], ip_mask_v6, nhop13)
        sai_thrift_create_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[3], ip_mask_v6, nhop14)
        sai_thrift_create_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[4], ip_mask_v6, nhop15)
        sai_thrift_create_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[5], ip_mask_v6, nhop16)
        sai_thrift_create_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[6], ip_mask_v6, nhop17)
        sai_thrift_create_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[7], ip_mask_v6, nhop18)
        sai_thrift_create_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[8], ip_mask_v6, nhop19)

        #mission session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        monitor_port_list = []
        port_list_valid = False
        ingress_localmirror_id = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[ingress_localmirror_id]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        #mcast
        grp_attr_list = []
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        dip_addr_mcast = '230.255.1.1'
        sip_addr_mcast = '10.10.10.1'
        dmac_mcast = '01:00:5E:7F:01:01'
        smac_mcast = '00:00:00:00:00:01'
        
        type = SAI_L2MC_ENTRY_TYPE_SG
        grp_id1 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id1_1 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port1)
        member_id1_2 = sai_thrift_create_l2mc_group_member(self.client, grp_id1, port2)
        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid1, dip_addr_mcast, sip_addr_mcast, type)
        sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id1)

        grp_id2 = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id2_1 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port1)
        
        mcast_fdb_entry = sai_thrift_mcast_fdb_entry_t(mac_address=dmac_mcast, bv_id=vlan_oid2)
        sai_thrift_create_mcast_fdb_entry(self.client, mcast_fdb_entry, grp_id2)
        
        type = SAI_IPMC_ENTRY_TYPE_SG
        grp_id3 = self.client.sai_thrift_create_ipmc_group(grp_attr_list)
        member_id3_1 = sai_thrift_create_ipmc_group_member(self.client, grp_id3, rif_id1)
        member_id3_2 = sai_thrift_create_ipmc_group_member(self.client, grp_id3, rif_id2)
        member_id3_3 = sai_thrift_create_ipmc_group_member(self.client, grp_id3, rif_id3)
        member_id3_4 = sai_thrift_create_ipmc_group_member(self.client, grp_id3, rif_id6)
        member_id3_5 = sai_thrift_create_ipmc_group_member(self.client, grp_id3, rif_id7)
        
        ipmc_entry = sai_thrift_fill_ipmc_entry(addr_family, vr_id, dip_addr_mcast, sip_addr_mcast, type)
        sai_thrift_create_ipmc_entry(self.client, ipmc_entry, grp_id3)

        #mcast sync and update
        member_id2_2 = sai_thrift_create_l2mc_group_member(self.client, grp_id2, port3)
        member_id3_6 = sai_thrift_create_ipmc_group_member(self.client, grp_id3, rif_id8)
        member_id3_7 = sai_thrift_create_ipmc_group_member(self.client, grp_id3, rif_id9)
        
        pkt1 = simple_tcp_packet(eth_dst=dmac[1],
                                eth_src='00:00:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
        pkt2 = simple_tcp_packet(eth_dst=dmac[10],
                                eth_src='00:00:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        exp_pkt2 = simple_tcp_packet(eth_dst=dmac[10],
                                eth_src='00:00:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst=l3if_mac[3],
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet[1],
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt3 = simple_tcp_packet(
                                eth_dst=l3if_dmac[1],
                                eth_src=l3if_mac[1],
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst=ip_addr1_subnet[1],
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        pkt4 = simple_tcpv6_packet( eth_dst=l3if_mac[3],
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=10,
                                   ipv6_dst=ip_addr_subnet_v6[1],
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt4 = simple_tcpv6_packet(
                                   eth_dst=l3if_dmac[1],
                                   eth_src=l3if_mac[1],
                                   dl_vlan_enable=True,
                                   vlan_vid=20,
                                   ipv6_dst=ip_addr_subnet_v6[1],
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63)
        pkt5 = simple_tcp_packet(eth_dst=dmac_mcast,
                                eth_src=smac_mcast,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst=dip_addr_mcast,
                                ip_src=sip_addr_mcast,
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt5_1 = simple_tcp_packet(
                                eth_dst=dmac_mcast,
                                eth_src=l3if_mac[0],
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst=dip_addr_mcast,
                                ip_src=sip_addr_mcast,
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt5_2 = simple_tcp_packet(
                                eth_dst=dmac_mcast,
                                eth_src=l3if_mac[1],
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst=dip_addr_mcast,
                                ip_src=sip_addr_mcast,
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt5_3 = simple_tcp_packet(
                                eth_dst=dmac_mcast,
                                eth_src=l3if_mac[5],
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst=dip_addr_mcast,
                                ip_src=sip_addr_mcast,
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt5_4 = simple_tcp_packet(
                                eth_dst=dmac_mcast,
                                eth_src=l3if_mac[6],
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_dst=dip_addr_mcast,
                                ip_src=sip_addr_mcast,
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt5_5 = simple_tcp_packet(pktlen=96,
                                eth_dst=dmac_mcast,
                                eth_src=l3if_mac[7],
                                ip_dst=dip_addr_mcast,
                                ip_src=sip_addr_mcast,
                                ip_id=105,
                                ip_ttl=63)
        exp_pkt5_6 = simple_tcp_packet(pktlen=96,
                                eth_dst=dmac_mcast,
                                eth_src=l3if_mac[8],
                                ip_dst=dip_addr_mcast,
                                ip_src=sip_addr_mcast,
                                ip_id=105,
                                ip_ttl=63)
                                
        warmboot(self.client)
        try:
            sys_logging("======l2 test ======")

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packet( (pkt1), 1)
            self.ctc_verify_each_packet_on_each_port( [pkt1, pkt1], [1, 2])

            self.ctc_send_packet( 3, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, pkt2], [4, 2])

            self.ctc_send_packet( 3, str(pkt3))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt3, pkt3], [1, 2])

            self.ctc_send_packet( 3, str(pkt4))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt4, pkt4], [1, 2])

            self.ctc_send_packet( 5, str(pkt5))
            #self.ctc_verify_each_packet_on_each_port( [exp_pkt5_1, exp_pkt5_1, exp_pkt5_2, exp_pkt5_2, exp_pkt5_3, exp_pkt5_4, exp_pkt5_5, exp_pkt5_6], [0, 1, 0, 2, 5, 5, 6, 7])
            self.ctc_verify_each_packet_on_each_port( [exp_pkt5_1, exp_pkt5_1, exp_pkt5_2, exp_pkt5_3, exp_pkt5_5, exp_pkt5_6], [0, 1, 2, 5, 6, 7])

            port6_pkt_cnt = 0
            port7_pkt_cnt = 0
            src_ip = int(socket.inet_aton('192.168.100.3').encode('hex'),16)
            max_itrs = 20
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip+i)[2:].zfill(8).decode('hex'))
                print src_ip_addr
                pkt6 = simple_tcp_packet(eth_dst=l3if_mac[5],
                                eth_src='00:00:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst=ip_addr1_subnet[9],
                                ip_src=src_ip_addr,
                                ip_id=101,
                                ip_ttl=64)

                exp_pkt6_1 = simple_tcp_packet(eth_dst=l3if_dmac[7],
                                eth_src=l3if_mac[7],
                                ip_dst=ip_addr1_subnet[9],
                                ip_src=src_ip_addr,
                                ip_id=101,
                                ip_ttl=63,
                                pktlen=96)
                exp_pkt6_2 = simple_tcp_packet(eth_dst=l3if_dmac[8],
                                eth_src=l3if_mac[8],
                                ip_dst=ip_addr1_subnet[9],
                                ip_src=src_ip_addr,
                                ip_id=101,
                                ip_ttl=63,
                                pktlen=96)
                self.ctc_send_packet( 5, str(pkt6))
                #self.ctc_verify_packet( (exp_pkt6_1), 6)
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt6_1,exp_pkt6_2], [6, 7])
                if rcv_idx == 6:
                    port6_pkt_cnt = port6_pkt_cnt+1
                elif rcv_idx == 7:
                    port7_pkt_cnt = port7_pkt_cnt+1
            sys_logging("port 6 receive packet conut is %d" %port6_pkt_cnt)
            sys_logging("port 7 receive packet conut is %d" %port7_pkt_cnt)

        
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3_1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3_2)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3_3)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3_4)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3_5)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3_6)
            self.client.sai_thrift_remove_ipmc_group_member(member_id3_7)
            self.client.sai_thrift_remove_ipmc_group(grp_id3)

            self.client.sai_thrift_remove_mcast_fdb_entry(mcast_fdb_entry) 
            self.client.sai_thrift_remove_l2mc_group_member(member_id2_1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id2_2)
            self.client.sai_thrift_remove_l2mc_group(grp_id2)

            self.client.sai_thrift_remove_l2mc_entry(l2mc_entry)
            self.client.sai_thrift_remove_l2mc_group_member(member_id1_1)
            self.client.sai_thrift_remove_l2mc_group_member(member_id1_2)            
            self.client.sai_thrift_remove_l2mc_group(grp_id1)
            
            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port4, attr)
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[0], ip_mask_v6, nhop11)
            sai_thrift_remove_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[1], ip_mask_v6, nhop12)
            sai_thrift_remove_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[2], ip_mask_v6, nhop13)
            sai_thrift_remove_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[3], ip_mask_v6, nhop14)
            sai_thrift_remove_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[4], ip_mask_v6, nhop15)
            sai_thrift_remove_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[5], ip_mask_v6, nhop16)
            sai_thrift_remove_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[6], ip_mask_v6, nhop17)
            sai_thrift_remove_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[7], ip_mask_v6, nhop18)
            sai_thrift_remove_route(self.client, vr_id, addr_family_v6, ip_addr_subnet_v6[8], ip_mask_v6, nhop19)
            
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet[0], ip_mask1, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet[1], ip_mask1, nhop2)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet[2], ip_mask1, nhop3)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet[3], ip_mask1, nhop4)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet[4], ip_mask1, nhop5)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet[5], ip_mask1, nhop6)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet[6], ip_mask1, nhop7)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet[7], ip_mask1, nhop8)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet[8], ip_mask1, nhop9)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet[9], ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            self.client.sai_thrift_remove_next_hop(nhop4)
            self.client.sai_thrift_remove_next_hop(nhop5)
            self.client.sai_thrift_remove_next_hop(nhop6)
            self.client.sai_thrift_remove_next_hop(nhop7)
            self.client.sai_thrift_remove_next_hop(nhop8)
            self.client.sai_thrift_remove_next_hop(nhop9)

            self.client.sai_thrift_remove_next_hop(nhop11)
            self.client.sai_thrift_remove_next_hop(nhop12)
            self.client.sai_thrift_remove_next_hop(nhop13)
            self.client.sai_thrift_remove_next_hop(nhop14)
            self.client.sai_thrift_remove_next_hop(nhop15)
            self.client.sai_thrift_remove_next_hop(nhop16)
            self.client.sai_thrift_remove_next_hop(nhop17)
            self.client.sai_thrift_remove_next_hop(nhop18)
            self.client.sai_thrift_remove_next_hop(nhop19)

            sai_thrift_remove_neighbor(self.client, addr_family_v6, rif_id1, ip_addr_v6[0], l3if_dmac[0])
            sai_thrift_remove_neighbor(self.client, addr_family_v6, rif_id2, ip_addr_v6[1], l3if_dmac[1])
            sai_thrift_remove_neighbor(self.client, addr_family_v6, rif_id3, ip_addr_v6[2], l3if_dmac[2])
            sai_thrift_remove_neighbor(self.client, addr_family_v6, rif_id4, ip_addr_v6[3], l3if_dmac[3])
            sai_thrift_remove_neighbor(self.client, addr_family_v6, rif_id5, ip_addr_v6[4], l3if_dmac[4])
            sai_thrift_remove_neighbor(self.client, addr_family_v6, rif_id6, ip_addr_v6[5], l3if_dmac[5])
            sai_thrift_remove_neighbor(self.client, addr_family_v6, rif_id7, ip_addr_v6[6], l3if_dmac[6])
            sai_thrift_remove_neighbor(self.client, addr_family_v6, rif_id8, ip_addr_v6[7], l3if_dmac[7])
            sai_thrift_remove_neighbor(self.client, addr_family_v6, rif_id9, ip_addr_v6[8], l3if_dmac[8])
        
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1[0], l3if_dmac[0])
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1[1], l3if_dmac[1])
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_addr1[2], l3if_dmac[2])
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id4, ip_addr1[3], l3if_dmac[3])
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id5, ip_addr1[4], l3if_dmac[4])
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id6, ip_addr1[5], l3if_dmac[5])
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id7, ip_addr1[6], l3if_dmac[6])
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id8, ip_addr1[7], l3if_dmac[7])
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id9, ip_addr1[8], l3if_dmac[8])

            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_router_interface(rif_id5)
            self.client.sai_thrift_remove_router_interface(rif_id6)
            self.client.sai_thrift_remove_router_interface(rif_id7)
            self.client.sai_thrift_remove_router_interface(rif_id8)
            self.client.sai_thrift_remove_router_interface(rif_id9)

            self.client.sai_thrift_remove_virtual_router(vr_id)

            sai_thrift_delete_fdb(self.client, bridge_id1, dmac[9], sub_port_id1)
            sai_thrift_delete_fdb(self.client, bridge_id1, dmac[10], sub_port_id2)
            sai_thrift_delete_fdb(self.client, bridge_id1, dmac[11], sub_port_id3)
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid3)

            sai_thrift_delete_fdb(self.client, vlan_oid1, dmac[0], port1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, dmac[1], port2)
            sai_thrift_delete_fdb(self.client, vlan_oid1, dmac[2], port3)
            sai_thrift_delete_fdb(self.client, vlan_oid2, dmac[3], port1)
            sai_thrift_delete_fdb(self.client, vlan_oid2, dmac[4], port2)
            sai_thrift_delete_fdb(self.client, vlan_oid2, dmac[5], port3)
            sai_thrift_delete_fdb(self.client, vlan_oid3, dmac[6], port1)
            sai_thrift_delete_fdb(self.client, vlan_oid3, dmac[7], port2)
            sai_thrift_delete_fdb(self.client, vlan_oid3, dmac[8], port3)

            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3) 
             

            self.client.sai_thrift_remove_vlan_member(vlan_member1_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member2_3)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_1)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3_3)
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)

            self.client.sai_thrift_remove_bridge(bridge_id1)
            
            sai_thrift_create_bridge_port(self.client, port4)
            sai_thrift_create_bridge_port(self.client, port5)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr) 
         
class func_09(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print()
        print("It's only a test!")
        switch_init(self.client)
        #print port_list
        #pdb.set_trace()
        vlan_member_list = []
        vrf_num = 16
        vlan_num =64
        vlanif_num = 64
        arp_num=512
        vlan_oid_list = config_vlan(self.client,vlan_num)
        for i in range(8):
            vlan_member_list1 = config_port_vlan_member(self.client,port_list[i],vlan_oid_list)
            vlan_member_list = vlan_member_list + vlan_member_list1
        port_oid_list = [port_list[0], port_list[1], port_list[2], port_list[3], port_list[4], port_list[5], port_list[6], port_list[7]] *8
        config_fdb(self.client,vlan_oid_list,port_oid_list,vlan_num)
        #pdb.set_trace()
        vrf_oid_list = create_vrfs(self.client, vrf_num)
        vlanif_oid_list = create_vlan_ifs(self.client, vlanif_num,vrf_oid_list,vlan_oid_list)
        create_neighbors(self.client, vlanif_oid_list, arp_num)
        nhop_oid_list = create_nexthops(self.client, vlanif_oid_list, arp_num)
        create_routes(self.client, nhop_oid_list, vrf_oid_list)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.0.20',
                                dl_vlan_enable=True,
                                vlan_vid=4,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:02:03:04:00:00',
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=2,
                                ip_dst='10.10.0.20',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)
        pkt1 = simple_tcpv6_packet( eth_dst=router_mac,
                                   eth_src='00:22:22:22:22:22',
                                   dl_vlan_enable=True,
                                   vlan_vid=5,
                                   ipv6_dst='::10:0:8',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=64)
        exp_pkt1 = simple_tcpv6_packet(
                                   eth_dst='00:02:03:04:00:08',
                                   eth_src=router_mac,
                                   dl_vlan_enable=True,
                                   vlan_vid=4,
                                   ipv6_dst='::10:0:8',
                                   ipv6_src='2000::1',
                                   ipv6_hlim=63)
        try:
            sys_logging("======vlan type rif send dest ip hit v4 packet to vlan type rif======")
            self.ctc_send_packet( 5, str(pkt))
            self.ctc_verify_packet( exp_pkt, 0)
            
            self.ctc_send_packet( 6, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 2)
        finally:
            #pdb.set_trace()
            remove_routes(self.client, nhop_oid_list, vrf_oid_list)
            remove_nexthops(self.client, nhop_oid_list)
            remove_neighbors(self.client, vlanif_oid_list, arp_num)
            remove_vlan_ifs(self.client, vlanif_oid_list)
            remove_vrfs(self.client, vrf_oid_list)
            delete_fdb(self.client,vlan_oid_list,port_oid_list,vlan_num)
            delete_port_vlan_member(self.client,vlan_member_list)
            delete_vlan(self.client, vlan_oid_list)
