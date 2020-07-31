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
Thrift SAI STP interface tests
"""
import socket
from switch import *
import sai_base_test
import pdb
import time
from scapy.config import *
from scapy.layers.all import *


@group('L2')
class func_01_create_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
              
        sys_logging("###create first stpid!###")
        
        switch_init(self.client)
        sys_logging("###first_stp_oid is only for lchip 0 test!###")
        first_stp_oid = 4294967312
        vlan_list = [100]
        
        stp_oid = sai_thrift_create_stp_entry(self.client, vlan_list)

        warmboot(self.client)
        try:
            if stp_oid != first_stp_oid:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_stp_entry(stp_oid)

class func_02_create_same_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
      
        sys_logging("###sdk internal auto alloc id, so do not creat same stpid!###")
        vlan_list = [100]
        
        stp_oid1 = sai_thrift_create_stp_entry(self.client, vlan_list)
        stp_oid2 = sai_thrift_create_stp_entry(self.client, vlan_list)
        warmboot(self.client)
        try:
            if stp_oid1 == stp_oid2:
                raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_stp_entry(stp_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid2)

        
class func_03_create_max_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
              
        sys_logging("###create max stpid!###")
        switch_init(self.client)
        stp_oid = [0 for i in range(1,130)]
        vlan_list = [100]        
        for a in range(1,128):
            sys_logging("###create stpid %d###" %a)
            stp_oid[a] = sai_thrift_create_stp_entry(self.client, vlan_list)
        warmboot(self.client)
        try:
            sys_logging("###create stpid 128 failed###")
            stp_oid[128] = sai_thrift_create_stp_entry(self.client, vlan_list)
            if stp_oid[128] != SAI_NULL_OBJECT_ID:
                raise NotImplementedError()
        finally:
            for a in range(1,128):
                sys_logging("###remove stpid %d###" %a)
                self.client.sai_thrift_remove_stp_entry(stp_oid[a])           
            
class func_04_remove_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
              
        sys_logging("###remove stpid!###")
        sys_logging("###first_stp_oid is only for lchip 0 test!###")
        first_stp_oid = 4294967312
        switch_init(self.client)
        
        vlan_list = [100]
        
        stp_oid = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        warmboot(self.client)
        try:
            if stp_oid != first_stp_oid:
                raise NotImplementedError()
        finally:
            sys_logging("###expect remove success###")
            status = self.client.sai_thrift_remove_stp_entry(stp_oid)            
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()            
            
class func_05_remove_not_exist_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
              
        sys_logging("###remove not exist stpid!###")
        
        switch_init(self.client)
        
        no_exist_stp_oid = 4294967313
        
        warmboot(self.client)
        try:
            sys_logging("###remove failed!###")
            status = self.client.sai_thrift_remove_stp_entry(no_exist_stp_oid)            
            if status == SAI_STATUS_SUCCESS:
                raise NotImplementedError() 
        finally:
            sys_logging("###status=%d###" %status)
           
            
class func_06_set_and_get_stp_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_and_get_stp_attribute###")
        
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        port1 = port_list[0]
        vlan_list = [100]
        stp_oid = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr) 

        state = SAI_STP_PORT_STATE_BLOCKING
        stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)
        
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_stp_attribute(stp_oid)
            for a in attrs.attr_list:
                if a.id == SAI_STP_ATTR_BRIDGE_ID:
                    sys_logging("###SAI_STP_ATTR_BRIDGE_ID  %d###" %a.value.oid)
                    if default_1q_bridge != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_STP_ATTR_VLAN_LIST:
                    sys_logging("###SAI_STP_ATTR_VLAN_LIST count %d###" %a.value.vlanlist.vlan_count)
                    if 1 != a.value.vlanlist.vlan_count:
                        raise NotImplementedError()                    
                    for b in a.value.vlanlist.vlan_list:
                        sys_logging("###SAI_STP_ATTR_VLAN_LIST list %d###" %b)
                        assert( vlan_id == b ) 
                if a.id == SAI_STP_ATTR_PORT_LIST:
                    sys_logging("###SAI_STP_ATTR_PORT_LIST count %d###" %a.value.objlist.count)
                    if 1 != a.value.objlist.count:
                        NotImplementedError() 
                    for b in a.value.objlist.object_id_list:
                        sys_logging("###SAI_STP_ATTR_PORT_LIST list %lx###" %b )
                        assert( stp_port_id == b ) 
        finally:
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)

            
class func_07_create_stp_port_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_stp_port###")
        
        switch_init(self.client)
        vlan_id = 100
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
        
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        vlan_list = [100]
        stp_oid = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr) 

        sys_logging("###state 0 mean learning###")
        state = 0
        stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)

        status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1)
        assert( 0 == status) 
            
        
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        
        warmboot(self.client)
        try:

            sys_logging("###stp port state is learning, should discard packet###")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 1)

            status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1)
            assert( 1 == status) 
            
        finally:
        
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)          
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)       
            
class func_07_create_stp_port_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_stp_port###")
        
        switch_init(self.client)
        vlan_id = 100
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
        
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        vlan_list = [100]
        stp_oid = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr) 

        sys_logging("###state 1 mean forward###")
        state = 1
        stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)

        status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1)
        assert( 0 == status)
        
        
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        
        warmboot(self.client)
        try:
            sys_logging("###stp port state is forward, should forward packet###")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(pkt, [1])

            status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1)
            assert( 1 == status)
        
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)          
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid) 

class func_07_create_stp_port_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_stp_port###")
        
        switch_init(self.client)
        vlan_id = 100
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
        
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        vlan_list = [100]
        stp_oid = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr) 

        sys_logging("###state 2 mean block###")
        state = 2
        stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)

        status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1)
        assert( 0 == status)
        
        
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        
        warmboot(self.client)
        try:
            sys_logging("###stp port state is block, should discard packet###")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 1)

            status = sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1)
            assert( 0 == status)
        
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)          
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)             
            
class func_08_remove_stp_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###remove_stp_port###")
        
        switch_init(self.client)
        vlan_id = 100
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
        
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        vlan_list = [100]
        stp_oid = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr) 

        state = 2
        stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)
        
        
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        
        warmboot(self.client)
        try:
            sys_logging("###stp port state is block, should discard packet###")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 1)
            sys_logging("###remove stp port, the port state will recover to forward###")
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(pkt, [1])          
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)          
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)             
            
            
class func_09_set_stp_port_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###set_stp_port_attr###")
        
        switch_init(self.client)
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        bport1_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
            
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        vlan_list = [100]
        stp_oid = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr) 

        sys_logging("###state 2 mean block###")
        state = 2
        stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)
        
        
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        
        warmboot(self.client)
        try:
            sys_logging("###stp port state is block, should discard packet###")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 1)
       
            sys_logging("###set stp port state to forward###")
            state = 1
            self.client.sai_thrift_set_stp_port_state(stp_port_id, port1, state )
            
            attrs = self.client.sai_thrift_get_stp_port_attribute(stp_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_STP_PORT_ATTR_STP:
                    sys_logging("###SAI_STP_PORT_ATTR_STP  %d###" %a.value.oid)
                    if stp_oid != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_STP_PORT_ATTR_BRIDGE_PORT:
                    sys_logging("###SAI_STP_PORT_ATTR_BRIDGE_PORT  %d###" %a.value.oid)
                    if bport1_oid != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_STP_PORT_ATTR_STATE:
                    sys_logging("###SAI_STP_PORT_ATTR_STATE  %d###" %a.value.s32)
                    if state != a.value.s32:
                        raise NotImplementedError()
            
            sys_logging("###stp port state is forward, should forward packet###")           
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(pkt, [1]) 
            
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)     
            
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)             
            
            
            
class func_10_create_and_remove_stp_ports_fn_mode(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_and_remove_stp_ports###")
        
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        vlan_list = [100]
        stp_oid1 = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        vlan_id1 = 100        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)

        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr) 

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        stp_oid_list = [stp_oid1,stp_oid1,stp_oid1,stp_oid1]
        port_oid_list = [port_list[0],port_list[1],port_list[2],port_list[3]]
        state_list = [0,1,2,1]
       
        sys_logging("###create 4 stp ports###")
        results =  sai_thrift_create_stp_ports(self.client, stp_oid_list, port_oid_list, state_list, 4, 0)
        object_id_list = results[0]
        statuslist = results[1]        
        
        warmboot(self.client)
        try:
            sys_logging("###step1: check 4 stp ports obj-id and status ###")        
            for object_id in object_id_list:
                assert( object_id != SAI_NULL_OBJECT_ID ) 
            for status in statuslist:
                assert( status == SAI_STATUS_SUCCESS )                 
          
            sys_logging("###step2: send packet verify ###") 
            pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
            exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)                                
            sys_logging("###1###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 1)
            self.ctc_verify_no_packet(exp_pkt1, 2)            
            self.ctc_verify_no_packet(exp_pkt1, 3)
            sys_logging("###2###")
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 0)
            self.ctc_verify_no_packet(exp_pkt1, 2)            
            self.ctc_verify_packets(exp_pkt1, [3])             
            sys_logging("###3###")
            self.ctc_send_packet(2, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 0)
            self.ctc_verify_no_packet(exp_pkt1, 1)            
            self.ctc_verify_no_packet(exp_pkt1, 3)
            sys_logging("###4###")           
            self.ctc_send_packet(3, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 0)
            self.ctc_verify_packets(exp_pkt1, [1]) 
            self.ctc_verify_no_packet(exp_pkt1, 2)

            sys_logging("###step3: remove 4 stp ports ###")         
            statuslist1 = sai_thrift_remove_stp_ports(self.client, object_id_list, 0)            
            for status in statuslist1:
                assert( status == SAI_STATUS_SUCCESS )             
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2) 
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid1)
            

class func_10_create_and_remove_stp_ports_fn_mode_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_and_remove_stp_ports###")
        
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        vlan_list = [100]
        stp_oid1 = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        vlan_id1 = 100        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)

        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr) 

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        stp_oid_list = [stp_oid1,stp_oid1,stp_oid1,stp_oid1]
        port_oid_list = [port_list[0],port_list[1],port_list[2],port_list[3]]
        state_list = [0,1,4,2]
       
        sys_logging("###create 4 stp ports and 3rd is fail###")
        results =  sai_thrift_create_stp_ports(self.client, stp_oid_list, port_oid_list, state_list, 4, 0)
        object_id_list = results[0]
        statuslist = results[1]        
        
        warmboot(self.client)
        try:
            sys_logging("###step1: check 4 stp ports obj-id and status ###")        
            assert( object_id_list[0] != SAI_NULL_OBJECT_ID ) 
            assert( object_id_list[1] != SAI_NULL_OBJECT_ID ) 
            assert( object_id_list[2] == SAI_NULL_OBJECT_ID )  
            assert( object_id_list[3] == SAI_NULL_OBJECT_ID ) 
            
            assert( statuslist[0] == SAI_STATUS_SUCCESS )   
            assert( statuslist[1] == SAI_STATUS_SUCCESS ) 
            assert( statuslist[2] != SAI_STATUS_SUCCESS ) 
            assert( statuslist[3] == SAI_STATUS_NOT_EXECUTED )                
          
            sys_logging("###step2: send packet verify ###") 
            pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
            exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)                                
            sys_logging("###1###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 1)
            self.ctc_verify_no_packet(exp_pkt1, 2)           
            self.ctc_verify_no_packet(exp_pkt1, 3)
            sys_logging("###2###")
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 0)
            self.ctc_verify_packets(exp_pkt1, [2])            
            self.ctc_verify_packets(exp_pkt1, [3])             
            sys_logging("###3###")
            self.ctc_send_packet(2, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 0)
            self.ctc_verify_packets(exp_pkt1, [1])            
            self.ctc_verify_packets(exp_pkt1, [3])
            sys_logging("###4###")           
            self.ctc_send_packet(3, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 0)
            self.ctc_verify_packets(exp_pkt1, [1])            
            self.ctc_verify_packets(exp_pkt1, [2])

            sys_logging("###step3: remove 4 stp ports ###")         
            statuslist1 = sai_thrift_remove_stp_ports(self.client, object_id_list, 0)            
            assert( statuslist1[0] == SAI_STATUS_SUCCESS )   
            assert( statuslist1[1] == SAI_STATUS_SUCCESS ) 
            assert( statuslist1[2] == SAI_STATUS_INVALID_OBJECT_ID ) 
            assert( statuslist1[3] == SAI_STATUS_NOT_EXECUTED )             
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2) 
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid1)
            


class func_10_create_and_remove_stp_ports_fn_mode_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###create_and_remove_stp_ports###")
        
        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        vlan_list = [100]
        stp_oid1 = sai_thrift_create_stp_entry(self.client, vlan_list)
        
        vlan_id1 = 100        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)

        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr) 

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        stp_oid_list = [stp_oid1,stp_oid1,stp_oid1,stp_oid1]
        port_oid_list = [port_list[0],port_list[1],port_list[2],port_list[3]]
        state_list = [0,1,4,2]
       
        sys_logging("###create 4 stp ports and 3rd is fail###")
        results =  sai_thrift_create_stp_ports(self.client, stp_oid_list, port_oid_list, state_list, 4, 1)
        object_id_list = results[0]
        statuslist = results[1]        
        
        warmboot(self.client)
        try:
            sys_logging("###step1: check 4 stp ports obj-id and status ###")        
            assert( object_id_list[0] != SAI_NULL_OBJECT_ID ) 
            assert( object_id_list[1] != SAI_NULL_OBJECT_ID ) 
            assert( object_id_list[2] == SAI_NULL_OBJECT_ID )  
            assert( object_id_list[3] != SAI_NULL_OBJECT_ID ) 
            
            assert( statuslist[0] == SAI_STATUS_SUCCESS )   
            assert( statuslist[1] == SAI_STATUS_SUCCESS ) 
            assert( statuslist[2] != SAI_STATUS_SUCCESS ) 
            assert( statuslist[3] == SAI_STATUS_SUCCESS )                
          
            sys_logging("###step2: send packet verify ###") 
            pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
            exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=100,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)                                
            sys_logging("###1###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 1)
            self.ctc_verify_no_packet(exp_pkt1, 2)           
            self.ctc_verify_no_packet(exp_pkt1, 3)
            sys_logging("###2###")
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 0)
            self.ctc_verify_packets(exp_pkt1, [2])            
            self.ctc_verify_no_packet(exp_pkt1, 3)           
            sys_logging("###3###")
            self.ctc_send_packet(2, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 0)
            self.ctc_verify_packets(exp_pkt1, [1])            
            self.ctc_verify_no_packet(exp_pkt1, 3) 
            sys_logging("###4###")           
            self.ctc_send_packet(3, str(pkt1))
            self.ctc_verify_no_packet(exp_pkt1, 0)
            self.ctc_verify_no_packet(exp_pkt1, 1)           
            self.ctc_verify_no_packet(exp_pkt1, 2)

            sys_logging("###step3: remove 4 stp ports ###")         
            statuslist1 = sai_thrift_remove_stp_ports(self.client, object_id_list, 1)            
            assert( statuslist1[0] == SAI_STATUS_SUCCESS )   
            assert( statuslist1[1] == SAI_STATUS_SUCCESS ) 
            assert( statuslist1[2] == SAI_STATUS_INVALID_OBJECT_ID ) 
            assert( statuslist1[3] == SAI_STATUS_SUCCESS )             
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2) 
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid1)
            
class scenario_01_stp_rstp_forward(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###scenario_01_stp_rstp_forward###")
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        sys_logging("###default_stp_oid is only for lchip 0 test!###")
        
        default_stp_oid = 16
        attr_value = sai_thrift_attribute_value_t(oid=default_stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr) 
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)

        sys_logging("###state 1 mean forward###")
        state = 1
        stp_port_id = sai_thrift_create_stp_port(self.client, default_stp_oid, port1, state)
        
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64)
                                
        warmboot(self.client)
        try:
            sys_logging("###stp port state is forwarding, all packets should be forward###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])            
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2)              


class scenario_02_stp_rstp_learning(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###scenario_02_stp_rstp_learning###")
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        sys_logging("###default_stp_oid is only for lchip 0 test!###")
        default_stp_oid = 16
        attr_value = sai_thrift_attribute_value_t(oid=default_stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr) 
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)

        sys_logging("###state 0 mean learning###")
        state = 0
        stp_port_id = sai_thrift_create_stp_port(self.client, default_stp_oid, port1, state)
        
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64)
                                
        warmboot(self.client)
        try:
            sys_logging("###stp port state is learning, all packets should be discard###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 1)                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_no_packet(pkt2, 0)            
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2)    



class scenario_03_stp_rstp_block(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###scenario_03_stp_rstp_block###")
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        sys_logging("###default_stp_oid is only for lchip 0 test!###")
        default_stp_oid = 16
        attr_value = sai_thrift_attribute_value_t(oid=default_stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr) 
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)

        sys_logging("###state 2 mean block###")
        state = 2
        stp_port_id = sai_thrift_create_stp_port(self.client, default_stp_oid, port1, state)
        
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64)
                                
        warmboot(self.client)
        try:
            sys_logging("###stp port state is blocking, all packets should be discard###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 1)                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_no_packet(pkt2, 0)            
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2)  

class scenario_04_mstp_instance_ingress(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###scenario_04_mstp_instance_ingress###")
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_list1 = [10]
        stp_oid1 = sai_thrift_create_stp_entry(self.client, vlan_list1)
        
        vlan_list2 = [20]
        stp_oid2 = sai_thrift_create_stp_entry(self.client, vlan_list2)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid2)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)

        sys_logging("###vlan 10 to stp instance 1 and state is forward###")
        state1 = 1
        stp_port_id1 = sai_thrift_create_stp_port(self.client, stp_oid1, port1, state1)

        sys_logging("###vlan 20 to stp instance 2 and state is block###")
        state2 = 2
        stp_port_id2 = sai_thrift_create_stp_port(self.client, stp_oid2, port1, state2)
        
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64)
                                
        warmboot(self.client)
        try:
            sys_logging("###instance 1 is forward,instance 2 is blocking###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])                       
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_no_packet(pkt2, 0)            
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_stp_port(stp_port_id1)
            self.client.sai_thrift_remove_stp_port(stp_port_id2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2) 
            self.client.sai_thrift_remove_stp_entry(stp_oid1) 
            self.client.sai_thrift_remove_stp_entry(stp_oid2)   


class scenario_05_mstp_instance_egress(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("###scenario_05_mstp_instance_egress###")
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        vlan_list1 = [10]
        stp_oid1 = sai_thrift_create_stp_entry(self.client, vlan_list1)
        
        vlan_list2 = [20]
        stp_oid2 = sai_thrift_create_stp_entry(self.client, vlan_list2)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid2)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)

        sys_logging("###vlan 10 to stp instance 1 and state is block###")
        state1 = 2
        stp_port_id1 = sai_thrift_create_stp_port(self.client, stp_oid1, port1, state1)

        sys_logging("###vlan 20 to stp instance 2 and state is forward###")
        state2 = 1
        stp_port_id2 = sai_thrift_create_stp_port(self.client, stp_oid2, port1, state2)
        
        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03',
                                eth_src='00:00:00:00:00:04',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_ttl=64)
                                
        warmboot(self.client)
        try:     
            sys_logging("###instance 1 is blocking, instance 2 is forward###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 1)
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])             
        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_stp_port(stp_port_id1)
            self.client.sai_thrift_remove_stp_port(stp_port_id2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
            self.client.sai_thrift_remove_vlan(vlan_oid2) 
            self.client.sai_thrift_remove_stp_entry(stp_oid1) 
            self.client.sai_thrift_remove_stp_entry(stp_oid2)   
                

               
class scenario_06_vlan_member_is_lag(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        mac4 = '00:33:33:33:33:34'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        lag_oid = sai_thrift_create_lag(self.client)
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
                
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)

        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [lag_oid,port3])
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        is_lag = 1
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_UNTAGGED,is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)        

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_oid, attr)
                                                
        warmboot(self.client)
        
        try:     

            pkt = simple_tcp_packet(eth_dst=mac2,
                                    eth_src=mac1,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt1 = simple_tcp_packet(eth_dst=mac3,
                                    eth_src=mac2,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt2 = simple_tcp_packet(eth_dst=mac4,
                                    eth_src=mac2,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)
                                    
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            self.ctc_verify_packets( str(pkt), [2], 1)

            self.ctc_send_packet(1, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 0)
            self.ctc_verify_packets( str(pkt), [2], 1)

            port0_pkt_cnt = 0
            port1_pkt_cnt = 0
            
            self.ctc_send_packet(2, str(pkt1))            
            rcv_idx = self.ctc_verify_any_packet_any_port( [pkt1], [0, 1])
            if rcv_idx == 0:
                port0_pkt_cnt = 1
            elif rcv_idx == 1:
                port1_pkt_cnt = 1
            
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)

            port0_pkt_cnt = 0
            port1_pkt_cnt = 0
            
            self.ctc_send_packet(2, str(pkt2))            
            rcv_idx = self.ctc_verify_any_packet_any_port( [pkt2], [0, 1])
            if rcv_idx == 0:
                port0_pkt_cnt = 1
            elif rcv_idx == 1:
                port1_pkt_cnt = 1
            
            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)
            
        finally:
            
            flush_all_fdb(self.client)

            is_lag = 1
            vlan_membera = sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_UNTAGGED,is_lag)
            vlan_memberb = sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED) 
        
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_oid, attr)           

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            
            sai_thrift_remove_lag(self.client, lag_oid)                  

            
class scenario_07_stp_port_is_lag(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        lag_oid = sai_thrift_create_lag(self.client)
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
                
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)

        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [lag_oid,port3])
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        is_lag = 1
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_UNTAGGED,is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)        

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_oid, attr)

        default_stp_oid = 16
        attr_value = sai_thrift_attribute_value_t(oid=default_stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr) 

        stp_port_id = sai_thrift_create_stp_port(self.client, default_stp_oid, lag_bridge_oid, SAI_STP_PORT_STATE_FORWARDING,is_lag)
        
        warmboot(self.client)
        
        try:     

            pkt = simple_tcp_packet(eth_dst=mac2,
                                    eth_src=mac1,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)
                                    
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            self.ctc_verify_packets( str(pkt), [2], 1)

            self.ctc_send_packet(1, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 0)
            self.ctc_verify_packets( str(pkt), [2], 1)
            
            self.client.sai_thrift_set_stp_port_state(stp_port_id, lag_bridge_oid, SAI_STP_PORT_STATE_BLOCKING )
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            self.ctc_verify_no_packet(str(pkt), 2)

            self.ctc_send_packet(1, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 0)
            self.ctc_verify_no_packet(str(pkt), 2)

            self.ctc_send_packet(2, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 0)
            self.ctc_verify_no_packet(str(pkt), 1)
            
        finally:
            
            flush_all_fdb(self.client)

            is_lag = 1
            vlan_membera = sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_UNTAGGED,is_lag)
            vlan_memberb = sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_oid, attr)           

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            
            sai_thrift_remove_lag(self.client, lag_oid)

            
            
            
            
class scenario_08_stp_port_is_lag_and_change_lag_member(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        lag_oid = sai_thrift_create_lag(self.client)
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
                
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)
         
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        is_lag = 1
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_UNTAGGED,is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)        

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_oid, attr)

        default_stp_oid = 16
        attr_value = sai_thrift_attribute_value_t(oid=default_stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr) 

        stp_port_id = sai_thrift_create_stp_port(self.client, default_stp_oid, lag_bridge_oid, SAI_STP_PORT_STATE_FORWARDING,is_lag)

        value = 1
        attr_value = sai_thrift_attribute_value_t(booldata=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
            
        warmboot(self.client)
        
        try:     

            pkt = simple_tcp_packet(eth_dst=mac2,
                                    eth_src=mac1,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt1 = simple_tcp_packet(eth_dst=mac2,
                                    eth_src=mac1,
                                    ip_dst='10.0.0.1',
                                    dl_vlan_enable=True,
                                    vlan_vid=1,                                    
                                    ip_id=101,
                                    ip_ttl=64,
                                    pktlen=104)
                                    
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            self.ctc_verify_packets( str(pkt), [3], 1)

            self.ctc_send_packet(1, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 0)
            self.ctc_verify_packets( str(pkt), [3], 1)

            self.ctc_send_packet(2, str(pkt))
            self.ctc_verify_packets( str(pkt1), [3], 1)            
           
            lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_oid, port3)

            self.ctc_send_packet(2, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 0)
            self.ctc_verify_no_packet(str(pkt), 1)
            self.ctc_verify_packets( str(pkt), [3], 1)

            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            
            self.ctc_send_packet(2, str(pkt))
            self.ctc_verify_packets( str(pkt), [3], 1)  
            
        finally:
            

            flush_all_fdb(self.client)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_oid, attr)           

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            
            sai_thrift_remove_lag(self.client, lag_oid)


            
            
class scenario_09_mstp_port_is_lag(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        vlan_id1 = 100
        vlan_id2 = 200 
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        lag_oid = sai_thrift_create_lag(self.client)
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
                
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)
         
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        is_lag = 1
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_UNTAGGED,is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)        
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_TAGGED,is_lag)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port4, SAI_VLAN_TAGGING_MODE_TAGGED) 
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_oid, attr)

        vlan_list1 = [100]
        stp_oid1 = sai_thrift_create_stp_entry(self.client, vlan_list1)
        
        vlan_list2 = [200]
        stp_oid2 = sai_thrift_create_stp_entry(self.client, vlan_list2)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)
        
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid2)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)

        stp_port_id1 = sai_thrift_create_stp_port(self.client, stp_oid1, lag_bridge_oid, SAI_STP_PORT_STATE_FORWARDING,is_lag)
        stp_port_id2 = sai_thrift_create_stp_port(self.client, stp_oid2, lag_bridge_oid, SAI_STP_PORT_STATE_BLOCKING,is_lag)
        
        warmboot(self.client)
        
        try:     

            pkt = simple_tcp_packet(eth_dst=mac2,
                                    eth_src=mac1,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt1 = simple_tcp_packet(eth_dst=mac2,
                                    eth_src=mac1,
                                    ip_dst='10.0.0.1',
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id2,                                    
                                    ip_id=101,
                                    ip_ttl=64,
                                    pktlen=104)
            pkt2 = simple_tcp_packet(eth_dst=mac2,
                                    eth_src=mac1,
                                    ip_dst='10.0.0.1',
                                    dl_vlan_enable=True,
                                    vlan_vid=1,                                    
                                    ip_id=101,
                                    ip_ttl=64,
                                    pktlen=104)
                                    
            sys_logging("###forward###")
                                    
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            self.ctc_verify_packets( str(pkt), [3], 1)

            self.ctc_send_packet(1, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 0)
            self.ctc_verify_packets( str(pkt), [3], 1)

            sys_logging("###block###")
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt1), 1)
            self.ctc_verify_no_packet(str(pkt1), 3)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(str(pkt1), 0)
            self.ctc_verify_no_packet(str(pkt1), 3)

            sys_logging("### normal port ###")
            
            self.ctc_send_packet(2, str(pkt))
            self.ctc_verify_packets( str(pkt2), [3], 1)            
           
            sys_logging("### add lag member ###")
            lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_oid, port3)

            sys_logging("###forward###")
                                    
            self.ctc_send_packet(2, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 0)            
            self.ctc_verify_no_packet(str(pkt), 1)
            self.ctc_verify_packets( str(pkt), [3], 1)

            sys_logging("###block###")
            
            self.ctc_send_packet(2, str(pkt1))
            self.ctc_verify_no_packet(str(pkt1), 0)            
            self.ctc_verify_no_packet(str(pkt1), 1)
            self.ctc_verify_no_packet(str(pkt1), 3)

            sys_logging("### remove lag member ###")
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [3], 1)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [3], 1)
           
        finally:
            
            flush_all_fdb(self.client)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_oid, attr)           
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            
            self.client.sai_thrift_remove_stp_port(stp_port_id1)
            self.client.sai_thrift_remove_stp_port(stp_port_id2)
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)

            self.client.sai_thrift_remove_stp_entry(stp_oid1) 
            self.client.sai_thrift_remove_stp_entry(stp_oid2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)            
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            
            sai_thrift_remove_lag(self.client, lag_oid)


            
            
                        