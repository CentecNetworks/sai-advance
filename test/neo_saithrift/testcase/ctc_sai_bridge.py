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
Thrift SAI Bridge interface tests
"""
import socket
from switch import *
import sai_base_test
import pdb
import time
from scapy.config import *
from scapy.layers.all import *
from ptf.mask import Mask

class func_01_create_bridge_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("###the first bridge id is just valid for lchip 0!###")        
        first_bridge_id = 8589942841
        warmboot(self.client)
        try:
            assert(first_bridge_id == bridge_id)
        finally:
            self.client.sai_thrift_remove_bridge(bridge_id)

class func_01_create_bridge_fn_1q(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1Q)       
        warmboot(self.client)
        try:
            assert(SAI_NULL_OBJECT_ID == bridge_id)
        finally:
            sys_logging("###only can create 1d bridge !###")
            
class func_02_create_multi_bridge_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        sys_logging("###bridge oid is auto alloc###")
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)        
        warmboot(self.client)
        try:
            assert(bridge_id1 != bridge_id2)
        finally:
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            
            
class func_03_create_max_bridge_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
          
        switch_init(self.client)
        sys_logging("###alloc fid (0k~4k) from opf ###")
        bridge_id = [0 for i in range(0,4096)]
        for a in range(2,4095):
            sys_logging("###creat bridge id %d ###" %a) 
            bridge_id[a] = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
            sys_logging("###bridge_id =%d ###" %bridge_id[a])
        warmboot(self.client)
        try:
            sys_logging("###creat bridge id 4095 ###") 
            bridge_id[4095] = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
            sys_logging("###bridge 4095 oid =%d ###" %bridge_id[4095])
            if bridge_id[4095] != SAI_NULL_OBJECT_ID:
                raise NotImplementedError()
        finally:
            for a in range(2,4095):
                sys_logging("###remove bridge %d###" %a)
                self.client.sai_thrift_remove_bridge(bridge_id[a])             

                
class func_04_remove_bridge_fn (sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        assert(bridge_id != SAI_NULL_OBJECT_ID)
        status = self.client.sai_thrift_remove_bridge(bridge_id)
        warmboot(self.client)
        try:
            assert(status == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("###remove success ###")            
            
            
class func_05_remove_not_exist_bridge_fn (sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        not_exist_bridge_id = 8589942841
        status = self.client.sai_thrift_remove_bridge(not_exist_bridge_id)
        warmboot(self.client)
        try:
            assert(status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            sys_logging("### not found ###")             
            

class func_06_set_and_get_bridge_attribute_fn_0_1d(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_TYPE = %d ###" %a.value.s32)
                    assert(SAI_BRIDGE_TYPE_1D == a.value.s32)
        finally:
            self.client.sai_thrift_remove_bridge(bridge_id)             

            
class func_06_set_and_get_bridge_attribute_fn_0_1q(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_TYPE = %d ###" %a.value.s32)
                    assert(SAI_BRIDGE_TYPE_1Q == a.value.s32)
        finally:
            sys_logging("###1q bridge should not remove###")

            
            
class func_06_set_and_get_bridge_attribute_fn_1_1q(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        sys_logging("###all port is SAI_BRIDGE_PORT_TYPE_PORT by default ###")
        
        warmboot(self.client)
        try:
            ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
            bridge_port_list = ret.data.objlist.object_id_list 
            count = ret.data.objlist.count
            sys_logging("###count = %d ###" %count) 
            assert( 32 == count )
            bport_id = [0 for i in range(0,32)]
            for i in range(0,32):                
                bport_id[i] = sai_thrift_get_bridge_port_by_port(self.client, port_list[i])
                sys_logging("###bridge_port_list %d = %d ###" %(i,bridge_port_list[i]))
                sys_logging("###bport_id %d = %d ###" %(i,bport_id[i]))
                assert( bport_id[i] in bridge_port_list )
        finally:
            sys_logging("###1q bridge should not remove###")

                                
class func_06_set_and_get_bridge_attribute_fn_1_1d(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        
        vlan_id1 = 10
        vlan_id2 = 15
        vlan_id3 = 20
        vlan_id4 = 25
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        
        bport_id = [0 for i in range(0,4)]        
        bport_id[0] = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        bport_id[1] = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id2)
        bport_id[2] = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan_id3)
        bport_id[3] = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id, vlan_id4)
        
        warmboot(self.client)
        try:
        
            default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
            ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
            count = ret.data.objlist.count
            assert( 32 == count ) 
            
            sys_logging("### every port can only be binding to 1q or 1d bridge at same time ###")
            
            ret = self.client.sai_thrift_get_bridge_port_list(bridge_id)
            bridge_port_list = ret.data.objlist.object_id_list 
            count = ret.data.objlist.count
            sys_logging("###count = %d ###" %count) 
            assert( 4 == count )    

            for i in range(0,4):                
                sys_logging("###bridge_port_list %d = %d ###" %(i,bridge_port_list[i]))
                sys_logging("###bport_id %d = %d ###" %(i,bport_id[i]))
                assert( bport_id[i] in bridge_port_list )
                
        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[0], port1)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[1], port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[2], port3)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[3], port4)
            self.client.sai_thrift_remove_bridge(bridge_id)             

'''
#1d port and 1q port can co-exist
class func_06_set_and_get_bridge_attribute_fn_1_1q_and_1d(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        sys_logging("### every port can only be binding to 1q or 1d bridge at same time ###")
        vlan_id1 = 10       
        port1 = port_list[0]
        
        warmboot(self.client)
        try:        
            default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
            ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
            bridge_port_list = ret.data.objlist.object_id_list 
            bport_id0 = sai_thrift_get_bridge_port_by_port(self.client, port_list[0])
            assert( bport_id0 in bridge_port_list )
    
            bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)            
            subport_id0 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
            
            sys_logging("### create sub port will remove bport from default 1q bridge ###")
    
            ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
            bridge_port_list = ret.data.objlist.object_id_list 
            assert( bport_id0 not in bridge_port_list )
    
            ret = self.client.sai_thrift_get_bridge_port_list(bridge_id)
            bridge_subport_list = ret.data.objlist.object_id_list 
            assert( subport_id0 in bridge_subport_list )
        finally:
            sai_thrift_remove_bridge_sub_port(self.client, subport_id0, port1)
            self.client.sai_thrift_remove_bridge(bridge_id)  
'''
           
            
class func_06_set_and_get_bridge_attribute_fn_2_1d(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("###SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    assert(0 == a.value.u32)
            
            value = 100
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("###SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    assert(value == a.value.u32) 

            value = 0
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("###SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    assert(value == a.value.u32) 
                   
        finally:
            self.client.sai_thrift_remove_bridge(bridge_id) 

class func_06_set_and_get_bridge_attribute_fn_2_1q(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("###SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    assert(0 == a.value.u32)
            
            value = 100
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(default_1q_bridge, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("###SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    assert(value == a.value.u32) 

            value = 0
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(default_1q_bridge, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("###SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    assert(value == a.value.u32) 
                   
        finally:
            sys_logging("###test end###")
            
class func_06_set_and_get_bridge_attribute_fn_3_1d(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_LEARN_DISABLE:
                    sys_logging("###SAI_BRIDGE_ATTR_LEARN_DISABLE = %d ###" %a.value.booldata)
                    assert( 0 == a.value.booldata)
            
            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_LEARN_DISABLE:
                    sys_logging("###SAI_BRIDGE_ATTR_LEARN_DISABLE = %d ###" %a.value.booldata)
                    assert( value == a.value.booldata) 

            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_LEARN_DISABLE:
                    sys_logging("###SAI_BRIDGE_ATTR_LEARN_DISABLE = %d ###" %a.value.booldata)
                    assert( value == a.value.booldata) 
                   
        finally:
            self.client.sai_thrift_remove_bridge(bridge_id)

class func_06_set_and_get_bridge_attribute_fn_3_1q(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_LEARN_DISABLE:
                    sys_logging("###SAI_BRIDGE_ATTR_LEARN_DISABLE = %d ###" %a.value.booldata)
                    assert( 0 == a.value.booldata)
            
            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(default_1q_bridge, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_LEARN_DISABLE:
                    sys_logging("###SAI_BRIDGE_ATTR_LEARN_DISABLE = %d ###" %a.value.booldata)
                    assert( value == a.value.booldata) 

            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(default_1q_bridge, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_LEARN_DISABLE:
                    sys_logging("###SAI_BRIDGE_ATTR_LEARN_DISABLE = %d ###" %a.value.booldata)
                    assert( value == a.value.booldata) 
                   
        finally:
            sys_logging("###test end###")
            
class func_06_set_and_get_bridge_attribute_fn_4_1d(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.s32)
            
            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 
                    
        finally:
            self.client.sai_thrift_remove_bridge(bridge_id)


class func_06_set_and_get_bridge_attribute_fn_4_1q(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.s32)
            
            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(default_1q_bridge, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(default_1q_bridge, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 
                    
        finally:
            sys_logging("###test end###")
            
class func_06_set_and_get_bridge_attribute_fn_5_1d(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.s32)
            
            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 
                    
        finally:
            self.client.sai_thrift_remove_bridge(bridge_id)

class func_06_set_and_get_bridge_attribute_fn_5_1q(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.s32)
            
            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(default_1q_bridge, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(default_1q_bridge, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 
                    
        finally:
            sys_logging("###test end###")

class func_06_set_and_get_bridge_attribute_fn_6_1d(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.s32)
            
            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 
                    
        finally:
            self.client.sai_thrift_remove_bridge(bridge_id)


class func_06_set_and_get_bridge_attribute_fn_6_1q(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.s32)
            
            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(default_1q_bridge, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(default_1q_bridge, attr)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    assert( value == a.value.s32) 
                    
        finally:
            sys_logging("###test end###")
            

class func_07_create_bridge_port_fn_sub_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[0]
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)         
        sub_port_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        warmboot(self.client)
        try:
            assert( sub_port_id != SAI_NULL_OBJECT_ID )                                   
        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_port_id, port1)
            self.client.sai_thrift_remove_bridge(bridge_id)    


class func_08_create_same_bridge_port_fn_0_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[0]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        assert (bport_oid != SAI_NULL_OBJECT_ID)
        self.client.sai_thrift_remove_bridge_port(bport_oid)
    
        bport_oid1 = sai_thrift_create_bridge_port(self.client, port1)
        bport_oid2 = sai_thrift_create_bridge_port(self.client, port1)
       
        sys_logging("###bport_oid1 = %ld ###" %bport_oid1)
        sys_logging("###bport_oid2 = %ld ###" %bport_oid2)          
        warmboot(self.client)
        try:
            assert( bport_oid1 == bport_oid2 )
            ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
            bridge_port_list = ret.data.objlist.object_id_list 
            count = ret.data.objlist.count
            sys_logging("###count = %d ###" %count) 
            assert( 32 == count )       
        finally:
            sys_logging("###test end###")  


            
class func_08_create_same_bridge_port_fn_1_sub_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[0]
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_port(self.client, port1, SAI_BRIDGE_PORT_TYPE_SUB_PORT, bridge_id, vlan_id1, None, True)
        sys_logging("###sub_port_id1 = %ld ###" %sub_port_id1)
        sys_logging("###sub_port_id2 = %ld ###" %sub_port_id2) 
        warmboot(self.client)
        try:
            assert( SAI_NULL_OBJECT_ID == sub_port_id2 ) 
        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_port_id1, port1)
            self.client.sai_thrift_remove_bridge(bridge_id)    


            
class func_08_create_same_bridge_port_fn_2_1d_route(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        
        v4_enabled = 1
        v6_enabled = 1
                
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, '')

        bridge_rif_bp1 = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_oid)
        bridge_rif_bp2 = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_oid)
        
  
        sys_logging("###bridge_rif_bp1 = %ld ###" %bridge_rif_bp1)
        sys_logging("###bridge_rif_bp2 = %ld ###" %bridge_rif_bp2) 
       
        warmboot(self.client)
        try:
            assert( SAI_NULL_OBJECT_ID == bridge_rif_bp2 )  
            
        finally:
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp1)          
            self.client.sai_thrift_remove_router_interface(bridge_rif_oid)           
            self.client.sai_thrift_remove_virtual_router(vr_id)           
            self.client.sai_thrift_remove_bridge(bridge_id)

            
class func_08_create_same_bridge_port_fn_3_tunnel(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):                     
        switch_init(self.client)        
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
       
        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
        
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, vlan_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, vlan_id, vni_id)
     
        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        btunnel_id1 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        btunnel_id2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        
        
        sys_logging("###btunnel_id1 = %ld ###" %btunnel_id1)
        sys_logging("###btunnel_id2 = %ld ###" %btunnel_id2) 

        warmboot(self.client)
        try:
        
            assert( SAI_NULL_OBJECT_ID == btunnel_id2 )  
            
        finally:      
            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)        
            self.client.sai_thrift_remove_bridge_port(btunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)  
            


            
class func_09_remove_bridge_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[0]
        
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()

        ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
        count = ret.data.objlist.count
        assert( 32 == count )
            
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)         
        sub_port_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)

        ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
        count = ret.data.objlist.count
        assert( 32 == count )
             
        warmboot(self.client)
        try:
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_port_id, port1)
            ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
            count = ret.data.objlist.count
            assert( 32 == count )            
        finally:
            self.client.sai_thrift_remove_bridge(bridge_id) 


class func_10_remove_not_exist_bridge_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        vlan_id1 = 10        
        port1 = port_list[0]
        
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        assert (bport_oid != SAI_NULL_OBJECT_ID)
        
        not_exist_bport_oid = bport_oid + 1
        status = self.client.sai_thrift_remove_bridge_port(not_exist_bport_oid)
    
        sys_logging("###status = %d ###" %status)  
        warmboot(self.client)
        try:
            assert( SAI_STATUS_INVALID_OBJECT_ID == status )
        finally:
            sys_logging("###test end###")  
            
                
class func_11_set_and_get_bridge_port_attribute_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[0]
                  
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)         
        sub_port_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        
        
        warmboot(self.client)
        try:
        
            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_TYPE:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_TYPE = %d ###" %a.value.s32)
                    assert( SAI_BRIDGE_PORT_TYPE_SUB_PORT == a.value.s32) 
                    
        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_port_id, port1)
            self.client.sai_thrift_remove_bridge(bridge_id) 
            

class func_11_set_and_get_bridge_port_attribute_fn_1_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[1]
                          
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_PORT_ID:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_PORT_ID = %d ###" %a.value.oid)
                    assert( port1 == a.value.oid)                           
        finally:
             sys_logging("###test end###")             
            
            
class func_11_set_and_get_bridge_port_attribute_fn_1_subport(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[1]
                  
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)         
        sub_port_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_PORT_ID:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_PORT_ID = %d ###" %a.value.oid)
                    assert( port1 == a.value.oid)                           
        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_port_id, port1)
            self.client.sai_thrift_remove_bridge(bridge_id)             
            
            
            
class func_11_set_and_get_bridge_port_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[1]
                  
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)         
        sub_port_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        
        
        warmboot(self.client)
        try:
        
            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_TAGGING_MODE:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_TAGGING_MODE = %d ###" %a.value.s32)
                    assert( SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED == a.value.s32)  
                         
            value = SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_TAGGING_MODE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id, attr)
        
            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_TAGGING_MODE:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_TAGGING_MODE = %d ###" %a.value.s32)
                    #assert( SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED == a.value.s32)
                    # do not support update 
                    assert( SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED == a.value.s32)                    
        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_port_id, port1)
            self.client.sai_thrift_remove_bridge(bridge_id)             
            
            
class func_11_set_and_get_bridge_port_attribute_fn_3(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[1]
                  
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)         
        sub_port_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_VLAN_ID:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_VLAN_ID = %d ###" %a.value.u16)
                    assert( vlan_id1 == a.value.u16)                           
        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_port_id, port1)
            self.client.sai_thrift_remove_bridge(bridge_id)             
                        
                      
class func_11_set_and_get_bridge_port_attribute_fn_4(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        
        v4_enabled = 1
        v6_enabled = 1
        
        vlan1_id = 100
        
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, '')

        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_oid)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bridge_rif_bp)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_RIF_ID:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_RIF_ID = %d ###" %a.value.oid)
                    assert( bridge_rif_oid == a.value.oid)                           
        finally:
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)          
            self.client.sai_thrift_remove_router_interface(bridge_rif_oid)           
            self.client.sai_thrift_remove_virtual_router(vr_id)           
            self.client.sai_thrift_remove_bridge(bridge_id)


                     
class func_11_set_and_get_bridge_port_attribute_fn_5(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
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
       
        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
        
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, vlan_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, vlan_id, vni_id)
     
        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(btunnel_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_TUNNEL_ID:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_TUNNEL_ID = %d ###" %a.value.oid)
                    assert( tunnel_id == a.value.oid)                           
        finally:      
            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)        
            self.client.sai_thrift_remove_bridge_port(btunnel_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)        


class func_11_set_and_get_bridge_port_attribute_fn_6_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)

        port1 = port_list[0]
        bport = sai_thrift_get_bridge_port_by_port(self.client, port1)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_ADMIN_STATE:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_ADMIN_STATE = %d ###" %a.value.booldata)
                    assert( 1 == a.value.booldata)  

            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport, attr)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_ADMIN_STATE:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_ADMIN_STATE = %d ###" %a.value.booldata)
                    assert( 0 == a.value.booldata)  
                    
        finally:
                value = 1
                attr_value = sai_thrift_attribute_value_t(booldata=value)
                attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=attr_value)
                self.client.sai_thrift_set_bridge_port_attribute(bport, attr)



class func_11_set_and_get_bridge_port_attribute_fn_6_port_transmit_and_receive(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

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
        
        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)
            
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        
        warmboot(self.client)
        try:
        
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)

            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport1, attr)
    
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 1)  

            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport1, attr)
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, attr)
            
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 1) 
            
            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, attr)
            
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

         
class func_11_set_and_get_bridge_port_attribute_fn_6_sub_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[1]
                  
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        
        sub_port_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        
        
        warmboot(self.client)
        try:

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_BRIDGE_ID:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_BRIDGE_ID = %d ###" %a.value.oid)
                    assert( bridge_id1 == a.value.oid) 

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id, attr)

            sai_thrift_flush_fdb_by_bridge_port(self.client, sub_port_id)
            
            attr_value = sai_thrift_attribute_value_t(oid=bridge_id2)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_BRIDGE_ID, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id, attr)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_BRIDGE_ID:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_BRIDGE_ID = %d ###" %a.value.oid)
                    assert( bridge_id2 == a.value.oid)          
        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_port_id, port1)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            
            
class func_11_set_and_get_bridge_port_attribute_fn_6_1d_route(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        
        v4_enabled = 1
        v6_enabled = 1
        
        vlan1_id = 100
        
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        bridge_rif_oid = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, '')

        bridge_rif_bp = sai_thrift_create_bridge_rif_port(self.client, bridge_id1, bridge_rif_oid)
        
        
        warmboot(self.client)
        try:
        
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bridge_rif_bp)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_BRIDGE_ID:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_BRIDGE_ID = %d ###" %a.value.oid)
                    assert( bridge_id1 == a.value.oid)  

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bridge_rif_bp, attr)

            sai_thrift_flush_fdb_by_bridge_port(self.client, bridge_rif_bp)
            
            attr_value = sai_thrift_attribute_value_t(oid=bridge_id2)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_BRIDGE_ID, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bridge_rif_bp, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bridge_rif_bp, attr)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(bridge_rif_bp)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_BRIDGE_ID:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_BRIDGE_ID = %d ###" %a.value.oid)
                    assert( bridge_id2 == a.value.oid)   
                    
        finally:
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp)          
            self.client.sai_thrift_remove_router_interface(bridge_rif_oid)           
            self.client.sai_thrift_remove_virtual_router(vr_id)           
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)

class func_11_set_and_get_bridge_port_attribute_fn_6_tunnel_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
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
       
        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
        
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, vlan_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, vlan_id, vni_id)
     
        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id1)
        
        
        warmboot(self.client)
        try:
        
            attrs = self.client.sai_thrift_get_bridge_port_attribute(btunnel_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_BRIDGE_ID:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_BRIDGE_ID = %d ###" %a.value.oid)
                    assert( bridge_id1 == a.value.oid)   

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(btunnel_id, attr)

            sai_thrift_flush_fdb_by_bridge_port(self.client, btunnel_id)
            
            attr_value = sai_thrift_attribute_value_t(oid=bridge_id2)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_BRIDGE_ID, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(btunnel_id, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(btunnel_id, attr)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(btunnel_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_BRIDGE_ID:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_BRIDGE_ID = %d ###" %a.value.oid)
                    assert( bridge_id2 == a.value.oid)  
                   
        finally: 
            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)        
            self.client.sai_thrift_remove_bridge_port(btunnel_id)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid) 

            
#SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE            
            
            
class func_11_set_and_get_bridge_port_attribute_fn_7(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[1]
                  
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    assert( 0 == a.value.u32)    
            
            value = 123
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
        
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    assert( 123 == a.value.u32)         
        finally:
            value = 0
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)



class func_11_set_and_get_bridge_port_attribute_fn_8(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[1]
                  
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION = %d ###" %a.value.s32)
                    assert( SAI_PACKET_ACTION_DROP == a.value.s32)    
            
            value = SAI_PACKET_ACTION_COPY
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
        
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION = %d ###" %a.value.s32)
                    assert( value == a.value.s32)         
        finally:
            value = SAI_PACKET_ACTION_DROP
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)




class func_11_set_and_get_bridge_port_attribute_fn_9(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[1]
                  
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)         
        sub_port_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_ADMIN_STATE:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_ADMIN_STATE = %d ###" %a.value.booldata)
                    assert( 1 == a.value.booldata)  

            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id, attr)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_ADMIN_STATE:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_ADMIN_STATE = %d ###" %a.value.booldata)
                    assert( 0 == a.value.booldata)  
                    
        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_port_id, port1)
            self.client.sai_thrift_remove_bridge(bridge_id)



class func_11_set_and_get_bridge_port_attribute_fn_10(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[1]
                  
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING = %d ###" %a.value.booldata)
                    assert( 0 == a.value.booldata)    
            
            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
        
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING = %d ###" %a.value.booldata)
                    assert( value == a.value.booldata)         
        finally:
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
                        
                        
                        

class func_11_set_and_get_bridge_port_attribute_fn_11(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10        
        port1 = port_list[1]
                  
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING = %d ###" %a.value.booldata)
                    assert( 0 == a.value.booldata)    
            
            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
        
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING = %d ###" %a.value.booldata)
                    assert( value == a.value.booldata)         
        finally:
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
                        
                                                
                                                
class func_11_set_and_get_bridge_port_attribute_fn_12(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
               
        port1 = port_list[0]

        isolation_group_oid = sai_thrift_create_isolation_group(self.client, type = SAI_ISOLATION_GROUP_TYPE_BRIDGE_PORT)
        
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP = %d ###" %a.value.oid)
                    assert( SAI_NULL_OBJECT_ID == a.value.oid)    
            
            value = isolation_group_oid
            attr_value = sai_thrift_attribute_value_t(oid=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
        
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP = %d ###" %a.value.oid)
                    assert( value == a.value.oid) 

            value = SAI_NULL_OBJECT_ID
            attr_value = sai_thrift_attribute_value_t(oid=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
        
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP = %d ###" %a.value.oid)
                    assert( value == a.value.oid) 

        finally:
            sai_thrift_remove_isolation_group(self.client, isolation_group_oid)
            
          
# uml port stats is not work
'''            
class func_12_get_bridge_port_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id1 = 10        
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport_oid1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport_oid2 = sai_thrift_get_bridge_port_by_port(self.client, port2)            

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        counter_ids = [SAI_BRIDGE_PORT_STAT_IN_OCTETS, SAI_BRIDGE_PORT_STAT_IN_PACKETS, SAI_BRIDGE_PORT_STAT_OUT_OCTETS, SAI_BRIDGE_PORT_STAT_OUT_PACKETS]
        
        list1 = self.client.sai_thrift_get_bridge_port_stats(bport_oid1, counter_ids, 4) 
        
        sys_logging("###list1[0]= %d###" %list1[0])
        sys_logging("###list1[1]= %d###" %list1[1])
        sys_logging("###list1[2]= %d###" %list1[2])
        sys_logging("###list1[3]= %d###" %list1[3])
        
        assert (list1[0] == 0)
        assert (list1[1] == 0)
        assert (list1[2] == 0)
        assert (list1[3] == 0)
            
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        
        warmboot(self.client)
        try:
        
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)            
                       
            list2 = self.client.sai_thrift_get_bridge_port_stats(bport_oid1, counter_ids, 4) 
            sys_logging("###list2[0]= %d###" %list2[0])
            sys_logging("###list2[1]= %d###" %list2[1])
            sys_logging("###list2[2]= %d###" %list2[2])
            sys_logging("###list2[3]= %d###" %list2[3])
            
            assert (list2[0] == 100)
            assert (list2[1] == 1)
            assert (list2[2] == 0)
            assert (list2[3] == 0)

        finally:    
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)            
'''                
                
                



class scenario_01_bridge_max_learning_limit(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20        
        port1 = port_list[0]
        port2 = port_list[1]                  
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id1)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:04',
                                eth_src='00:00:00:00:00:03',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:04',
                                eth_src='00:00:00:00:00:03',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        
        warmboot(self.client)
        try:

            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("###SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    assert(0 == a.value.u32)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt4), [1], 1)
            
            time.sleep(1)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1)
            assert(1 == result)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2)
            assert(1 == result)
            
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            time.sleep(1)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1)
            assert(0 == result)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2)
            assert(0 == result)

            
            value = 1
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)
        
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            time.sleep(1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt4), [1], 1)
            
            time.sleep(1)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1)
            assert(1 == result)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2)
            assert(0 == result)



        finally:
        

            value = 0
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)
            
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)            
            self.client.sai_thrift_remove_bridge(bridge_id1)          
            self.client.sai_thrift_remove_bridge(bridge_id2)








class scenario_02_bridge_mac_learning_disable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20        
        port1 = port_list[0]
        port2 = port_list[1]                  
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id1)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:04',
                                eth_src='00:00:00:00:00:03',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:04',
                                eth_src='00:00:00:00:00:03',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        
        warmboot(self.client)
        try:

            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_LEARN_DISABLE:
                    sys_logging("###SAI_BRIDGE_ATTR_LEARN_DISABLE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt4), [1], 1)
            
            time.sleep(1)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1)
            assert(1 == result)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2)
            assert(1 == result)
            
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            time.sleep(1)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1)
            assert(0 == result)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2)
            assert(0 == result)

            
            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)
        
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            time.sleep(1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt4), [1], 1)
            
            time.sleep(1)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1)
            assert(0 == result)
            result = sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2)
            assert(0 == result)


        

        finally:

            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)
            
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)            
            self.client.sai_thrift_remove_bridge(bridge_id1)          
            self.client.sai_thrift_remove_bridge(bridge_id2)










class scenario_03_unknown_unicast_flood_control(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20        
        port1 = port_list[0]
        port2 = port_list[1]                  
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id1)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:04',
                                eth_src='00:00:00:00:00:03',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:04',
                                eth_src='00:00:00:00:00:03',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        
        warmboot(self.client)
        try:

            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.booldata)
                    assert(SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.booldata)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt4), [1], 1)
                      
            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)
        
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_no_packet(str(pkt4), 1)
            
        finally:

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)

            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)            
            self.client.sai_thrift_remove_bridge(bridge_id1)          
            self.client.sai_thrift_remove_bridge(bridge_id2)









class scenario_04_unknown_multicast_flood_control(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20        
        port1 = port_list[0]
        port2 = port_list[1]                  
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id1)

        pkt1 = simple_tcp_packet(eth_dst='01:00:5e:01:01:01',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='01:00:5e:01:01:01',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst='01:00:5e:01:01:01',
                                eth_src='00:00:00:00:00:03',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt4 = simple_tcp_packet(eth_dst='01:00:5e:01:01:01',
                                eth_src='00:00:00:00:00:03',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        
        warmboot(self.client)
        try:

            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.booldata)
                    assert(SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.booldata)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt4), [1], 1)
                      
            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)
        
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_no_packet(str(pkt4), 1)
            
        finally:
        
            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)
        
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)            
            self.client.sai_thrift_remove_bridge(bridge_id1)          
            self.client.sai_thrift_remove_bridge(bridge_id2)





class scenario_05_broadcast_flood_control(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20        
        port1 = port_list[0]
        port2 = port_list[1]                  
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id1)

        pkt1 = simple_tcp_packet(eth_dst='ff:ff:ff:ff:ff:ff',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='ff:ff:ff:ff:ff:ff',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst='ff:ff:ff:ff:ff:ff',
                                eth_src='00:00:00:00:00:03',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt4 = simple_tcp_packet(eth_dst='ff:ff:ff:ff:ff:ff',
                                eth_src='00:00:00:00:00:03',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        
        warmboot(self.client)
        try:

            attrs = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
                    sys_logging("###SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.booldata)
                    assert(SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.booldata)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt4), [1], 1)
                      
            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)
        
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_no_packet(str(pkt4), 1)
            
        finally:

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)
            
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)            
            self.client.sai_thrift_remove_bridge(bridge_id1)          
            self.client.sai_thrift_remove_bridge(bridge_id2)  









class scenario_06_sub_port_forward(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]        
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id1, vlan_id1)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id1, vlan_id2)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:01',
                                eth_src='00:00:00:00:00:02',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:01',
                                eth_src='00:00:00:00:00:02',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        
        warmboot(self.client)
        try:

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1,3], 1)
            self.ctc_verify_packets( str(pkt1), [2], 1)                      

            self.ctc_send_packet(2, str(pkt3))
            self.ctc_verify_packets( str(pkt3), [0], 1)
            self.ctc_verify_no_packet(str(pkt4), 1)
            self.ctc_verify_no_packet(str(pkt4), 3)

            
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)                     
            self.client.sai_thrift_remove_bridge(bridge_id1)          








class scenario_07_sub_port_forward_tag_mode(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]        
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id1, vlan_id1)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id1, vlan_id2)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        
        warmboot(self.client)
        try:

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_port_id2)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_TAGGING_MODE:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_TAGGING_MODE = %d ###" %a.value.s32)
                    assert( SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED == a.value.s32)    
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1,3], 1)
            self.ctc_verify_packets( str(pkt1), [2], 1)  

            # do not support update tag mode for sub port
            '''                      
            value = SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_TAGGING_MODE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id2, attr)
  
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt3), [1], 1)
            self.ctc_verify_packets( str(pkt1), [2], 1) 
            self.ctc_verify_packets( str(pkt2), [3], 1)
            '''
                     
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)                     
            self.client.sai_thrift_remove_bridge(bridge_id1)       


class scenario_08_1d_router_forward(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        
        vlan1_id = 10
        vlan2_id = 20
        
        port1 = port_list[1]
        port2 = port_list[2]
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        rmac = '00:00:00:00:00:0a'
        
        mac1 = '00:00:00:00:00:01'
        ip1 = '11.11.11.11'

        mac2 = '00:00:00:00:00:02'
        ip2 = '22.22.22.22'

        mac3 = '00:00:00:00:00:03'
        
        ip_addr_subnet1 = '11.11.11.0'
        ip_mask1 = '255.255.255.0'

        ip_addr_subnet2 = '22.22.22.0'
        ip_mask2 = '255.255.255.0'
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        print "bridge_id1 = %d" %bridge_id1
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)       
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port1, port2])
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan1_id)
        bport2_id = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan2_id)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
                
        bridge_rif_oid1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, rmac)
        bridge_rif_oid2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE, 0, 0, v4_enabled, v6_enabled, rmac)
        
        bridge_rif_bp1 = sai_thrift_create_bridge_rif_port(self.client, bridge_id1, bridge_rif_oid1)
        bridge_rif_bp2 = sai_thrift_create_bridge_rif_port(self.client, bridge_id2, bridge_rif_oid2)
        
        sai_thrift_create_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV4, bridge_rif_oid1, ip1, mac1)
        sai_thrift_create_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV4, bridge_rif_oid2, ip2, mac2)       
        
        sai_thrift_create_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet1, ip_mask1, bridge_rif_oid1)
        sai_thrift_create_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet2, ip_mask2, bridge_rif_oid2)
        
        
        local_pkt = simple_tcp_packet(eth_src=mac1,
                                      eth_dst=mac3,
                                      dl_vlan_enable=True,
                                      vlan_vid=vlan1_id,
                                      ip_src='11.11.11.11',
                                      ip_dst='11.11.11.12',
                                      ip_id=102,
                                      ip_ttl=64)

        L3_pkt = simple_tcp_packet(eth_src=mac2,
                                   eth_dst=rmac,
                                   ip_src=ip2,
                                   ip_dst=ip1,
                                   dl_vlan_enable=True,
                                   vlan_vid=vlan2_id,
                                   ip_id=105,
                                   ip_ttl=64)

        exp_L3_pkt = simple_tcp_packet(eth_src=rmac,
                                   eth_dst=mac1,
                                   ip_src=ip2,
                                   ip_dst=ip1,
                                   dl_vlan_enable=True,
                                   vlan_vid=vlan1_id,
                                   ip_id=105,
                                   ip_ttl=63)                                 

        warmboot(self.client)
        try:

            self.ctc_send_packet( 2, str(L3_pkt))
            self.ctc_verify_no_packet(str(exp_L3_pkt), 0)

            sys_logging("### learn fdb ###")
            self.ctc_send_packet( 1, str(local_pkt))
            time.sleep(2)

            self.ctc_send_packet( 2, str(L3_pkt))
            self.ctc_verify_packets( str(exp_L3_pkt), [1], 1)


        finally:   

            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id2)
            
            sai_thrift_remove_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet1, ip_mask1, bridge_rif_oid1)
            sai_thrift_remove_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet2, ip_mask2, bridge_rif_oid2)
            
            sai_thrift_remove_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV4, bridge_rif_oid1, ip1, mac1)            
            sai_thrift_remove_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV4, bridge_rif_oid2, ip2, mac2)
            
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp1)
            self.client.sai_thrift_remove_bridge_port(bridge_rif_bp2)
            
            self.client.sai_thrift_remove_router_interface(bridge_rif_oid1)
            self.client.sai_thrift_remove_router_interface(bridge_rif_oid2)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_bridge_sub_port_2(self.client, bport1_id, port1)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport2_id, port2)
            
            self.client.sai_thrift_remove_bridge(bridge_id1)           
            self.client.sai_thrift_remove_bridge(bridge_id2)


class scenario_09_tunnel_port_forward(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)
        
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        
        v4_enabled = 1
        v6_enabled = 1
        
        mac=router_mac
        
        inner_mac_da = '00:00:AA:AA:00:00'
        inner_mac_sa = '00:00:AA:AA:11:11'
        
        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF
        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI
        
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
        
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        
        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)
        
        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)

        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)

        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, bridge_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, bridge_id, vni_id)
     
        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_VXLAN)
       
        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);
       
        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        
        sai_thrift_create_fdb_tunnel(self.client, bridge_id, inner_mac_da, btunnel_id, mac_action, ip_outer_addr_da)
        
        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        
        encap_mac_da = '00:0e:00:0e:00:0e'
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
        
        sai_thrift_create_fdb_bport(self.client, bridge_id, inner_mac_sa, bport1_id, mac_action)
        

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
                        ip_ttl=63,
                        ip_id=0x0000,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = pkt1)
        m1_exp_pkt1=Mask(exp_pkt1)
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'chksum')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'sport')
        inner_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=inner_mac_sa,
                                eth_src=inner_mac_da,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        pkt2 = simple_vxlan_packet(pktlen=300,
                        eth_dst=router_mac,
                        eth_src=encap_mac_da,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_da,
                        ip_dst=ip_outer_addr_sa,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=63,
                        ip_id=0x0000,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = inner_pkt2)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m1_exp_pkt1, 2)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( inner_pkt2, 1)
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id)
            sai_thrift_delete_fdb(self.client, bridge_id, inner_mac_sa, port1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            sai_thrift_delete_fdb(self.client, bridge_id, inner_mac_da, tunnel_id)
            self.client.sai_thrift_remove_bridge_port(btunnel_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
            self.client.sai_thrift_remove_bridge_port(bport1_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            

            
            
class scenario_10_update_bridge_port_bridge_id(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
                      
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D) 
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id2, vlan_id3)
        

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id1,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id2,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id3,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        
        warmboot(self.client)
        try:

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            self.ctc_verify_no_packet(str(pkt3), 2)                   

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id1, attr)

            sai_thrift_flush_fdb_by_bridge_port(self.client, sub_port_id1)
            
            attr_value = sai_thrift_attribute_value_t(oid=bridge_id2)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_BRIDGE_ID, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id1, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id1, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1) 
            self.ctc_verify_packets( str(pkt3), [2], 1)
 
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)           
          
            self.client.sai_thrift_remove_bridge(bridge_id1) 
            self.client.sai_thrift_remove_bridge(bridge_id2)            
            

class scenario_11_bridge_port_mac_learn_num_and_violation(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
                 
        pkt1 = simple_tcp_packet(eth_dst=mac3,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac3,
                                eth_src=mac2,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        sys_logging ("step1: no fdb entry")
        
        result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
        assert(0 == result)
        
        result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
        assert(0 == result)
        
        warmboot(self.client)
        try:

            bport_oid1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bport_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    assert(0 == a.value.u32)

            attrs = self.client.sai_thrift_get_bridge_attribute(bport_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION = %d ###" %a.value.s32)
                    assert(SAI_PACKET_ACTION_DROP == a.value.s32)
                    
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)

            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_packets( str(pkt2), [1], 1)            
          
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
            assert(1 == result)
            
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
            assert(1 == result)

            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)  

            value = 1
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
            time.sleep(1)
            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_no_packet(str(pkt2), 1)            

            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
            assert(1 == result)
            
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
            assert(0 == result)
        
        finally:

            value = 0
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)
        
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)            





class scenario_12_bridge_port_ingress_vlan_filter(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id1 = 100
        vlan_id2 = 200
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac_action = SAI_PACKET_ACTION_FORWARD
                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
                 
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
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=100)
       
        warmboot(self.client)
        try:

            bport_oid1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bport_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)
                         
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)

            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)  
            
        finally:

            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)
            
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1) 
            self.client.sai_thrift_remove_vlan(vlan_oid2) 


class scenario_13_bridge_port_egress_vlan_filter(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id1 = 100
        vlan_id2 = 200
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac_action = SAI_PACKET_ACTION_FORWARD
                
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
                 
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
                                vlan_vid=vlan_id2,                                
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=104)
       
        warmboot(self.client)
        try:

            bport_oid1 = sai_thrift_get_bridge_port_by_port(self.client, port2)
            
            attrs = self.client.sai_thrift_get_bridge_attribute(bport_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)
            

            sai_thrift_create_fdb(self.client, vlan_oid2, mac2, port2, mac_action)
                    
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            
            
            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)  
            
        finally:

            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)
            
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac2, port2)            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid1) 
            self.client.sai_thrift_remove_vlan(vlan_oid2) 
            



class scenario_14_normal_bridge_port_is_lag(sai_base_test.ThriftInterfaceDataPlane):
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
        
        value = 1
        attr_value = sai_thrift_attribute_value_t(u32=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)

        value = SAI_PACKET_ACTION_DROP
        attr_value = sai_thrift_attribute_value_t(s32=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
        
        warmboot(self.client)
        
        try:     

            pkt = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac2,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt1 = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac3,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt2 = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac4,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)
                                    
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            self.ctc_verify_packets( str(pkt), [2], 1)

            sys_logging(" exceed mac learning limit num, so discard this packet" )
            
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(str(pkt1), 1)
            self.ctc_verify_no_packet(str(pkt1), 2)

            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_verify_no_packet(str(pkt2), 2)
                       
        finally:
             

            flush_all_fdb(self.client)

            value = 0
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
    
            value = SAI_PACKET_ACTION_DROP
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
        
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
            
            

class scenario_15_normal_bridge_port_with_lag_member_change(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
    
        switch_init(self.client)
        
        vlan_id = 100
        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        mac4 = '00:33:33:33:33:34'
        mac5 = '00:33:33:33:33:35'
        
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        lag_oid = sai_thrift_create_lag(self.client)

        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port1,port2,port3])
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
                
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)
        
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
     
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port3)

        value = 1
        attr_value = sai_thrift_attribute_value_t(booldata=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
        
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)

        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
        
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
                
        value = 2
        attr_value = sai_thrift_attribute_value_t(u32=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)

        value = SAI_PACKET_ACTION_DROP
        attr_value = sai_thrift_attribute_value_t(s32=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
        
        warmboot(self.client)
        
        try:     

            pkt = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac2,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt1 = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac3,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt2 = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac4,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt3 = simple_tcp_packet(eth_dst=mac1,
                                    eth_src=mac5,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)
                                    
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            self.ctc_verify_packets( str(pkt), [2], 1)
            self.ctc_verify_no_packet(str(pkt), 3)
            
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(str(pkt1), 0)
            self.ctc_verify_packets( str(pkt1), [2], 1)
            self.ctc_verify_no_packet(str(pkt1), 3)            
            
            self.ctc_send_packet(3, str(pkt2))
            self.ctc_verify_no_packet(str(pkt2), 0)
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_verify_no_packet(str(pkt2), 2)
            
            sys_logging(" add lag member" )

            lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_oid, port4)

            sys_logging(" exceed mac learning limit num, so discard this packet" )
            self.ctc_send_packet(3, str(pkt3))
            self.ctc_verify_no_packet(str(pkt3), 0)
            self.ctc_verify_no_packet(str(pkt3), 1)
            self.ctc_verify_no_packet(str(pkt3), 2)            
            
            flush_all_fdb(self.client)

            self.ctc_send_packet(3, str(pkt3))
            self.ctc_verify_no_packet(str(pkt3), 0)
            self.ctc_verify_no_packet(str(pkt3), 1)
            self.ctc_verify_packets( str(pkt3), [2], 1)           

            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac5)            
            assert(1 == result)

            sys_logging(" remove lag member" )

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            
            flush_all_fdb(self.client)            
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [2], 1) 

            port0_pkt_cnt = 0
            port1_pkt_cnt = 0

            rcv_idx = self.ctc_verify_any_packet_any_port( [pkt1], [1, 3])
            if rcv_idx == 1:
                port0_pkt_cnt = 1
            elif rcv_idx == 3:
                port1_pkt_cnt = 1

            sys_logging("port 0 receive packet conut is %d" %port0_pkt_cnt)
            sys_logging("port 1 receive packet conut is %d" %port1_pkt_cnt)

            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_packets( str(pkt2), [2], 1)

            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt3), [2], 1)
            
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac3)            
            assert(1 == result)
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac4)            
            assert(1 == result)
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac5)            
            assert(1 == result)
            
        finally:
             
            flush_all_fdb(self.client)
                                   
            value = 0
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
            
            value = SAI_PACKET_ACTION_DROP
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_oid, attr)           
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)            
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            
            sai_thrift_remove_lag(self.client, lag_oid)     
            
            vlan_memberb = sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            vlan_memberb = sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            vlan_memberb = sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)            

            bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)    
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)            
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
    
            bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port3)    
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)            
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
            
            bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port4)    
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)            
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
            

        