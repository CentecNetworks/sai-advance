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

from switch import *
from ptf.mask import Mask
import sai_base_test

import sys
from struct import pack, unpack

def ip6_to_integer(ip6):
    ip6 = socket.inet_pton(socket.AF_INET6, ip6)
    a, b = unpack(">QQ", ip6)
    return (a << 64) | b

def integer_to_ip6(ip6int):
    a = (ip6int >> 64) & ((1 << 64) - 1)
    b = ip6int & ((1 << 64) - 1)
    return socket.inet_ntop(socket.AF_INET6, pack(">QQ", a, b))

def ip4_to_integer(ip4):
    ip4int = int(socket.inet_aton('10.10.10.1').encode('hex'), 16)
    return ip4int

def integer_to_ip4(ip4int):
    return socket.inet_ntoa(hex(ip4int)[2:].zfill(8).decode('hex'))
    
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
    
@group('switch')

# TBD
#class func_01_create_switch_fn(sai_base_test.ThriftInterfaceDataPlane):

# TBD                  
#class func_02_remove_switch_fn(sai_base_test.ThriftInterfaceDataPlane):


    
class func_03_set_and_get_switch_attribute_01_NUMBER_OF_ACTIVE_PORTS(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        active_port_num = 32
        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS:
                    sys_logging("### SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS = %d ###"  %attribute.value.u32)
                    assert ( active_port_num == attribute.value.u32 ) 
        finally:           
            sys_logging("### TEST END! ###")          

class func_03_set_and_get_switch_attribute_02_MAX_NUMBER_OF_SUPPORTED_PORTS(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        max_port_num = 256

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_MAX_NUMBER_OF_SUPPORTED_PORTS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MAX_NUMBER_OF_SUPPORTED_PORTS:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_NUMBER_OF_SUPPORTED_PORTS = %d ###"  %attribute.value.u32)
                    assert ( max_port_num == attribute.value.u32 ) 
        finally:           
            sys_logging("### TEST END! ###")


class func_03_set_and_get_switch_attribute_03_PORT_LIST(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        port_list = [1,4294967297,8589934593,12884901889,17179869185,21474836481,25769803777,30064771073,34359738369,38654705665,42949672961,47244640257,51539607553,55834574849,60129542145,64424509441,68719476737,73014444033,77309411329,81604378625,85899345921,90194313217,94489280513,98784247809,103079215105,107374182401,111669149697,115964116993,120259084289,124554051585,128849018881,133143986177]
        active_port_num = 32

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_PORT_LIST]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_PORT_LIST:
                    sys_logging("### SAI_SWITCH_ATTR_PORT_LIST = %d ###"  %attribute.value.objlist.count)
                    assert ( active_port_num == attribute.value.objlist.count )
                    for attr in attribute.value.objlist.object_id_list:
                        sys_logging("### SAI_SWITCH_ATTR_PORT_LIST = %d ###"  %attr)
                        assert ( attr in  port_list )                        
        finally:           
            sys_logging("### TEST END! ###")


class func_03_set_and_get_switch_attribute_04_PORT_MAX_MTU(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        max_port_mtu = 16383

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_PORT_MAX_MTU]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_PORT_MAX_MTU:
                    sys_logging("### SAI_SWITCH_ATTR_PORT_MAX_MTU = %d ###"  %attribute.value.u32)
                    assert ( max_port_mtu == attribute.value.u32 ) 
        finally:           
            sys_logging("### TEST END! ###")

#?
class func_03_set_and_get_switch_attribute_05_CPU_PORT(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        cpu_port = 1152921504606855169

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_CPU_PORT]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_CPU_PORT:
                    sys_logging("### SAI_SWITCH_ATTR_CPU_PORT = %d ###"  %attribute.value.oid)
                    assert ( cpu_port == attribute.value.oid ) 
        finally:           
            sys_logging("### TEST END! ###")


class func_03_set_and_get_switch_attribute_06_MAX_VIRTUAL_ROUTERS(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        max_vrf = 255

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_MAX_VIRTUAL_ROUTERS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MAX_VIRTUAL_ROUTERS:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_VIRTUAL_ROUTERS = %d ###"  %attribute.value.u32)
                    assert ( max_vrf == attribute.value.u32 ) 
        finally:           
            sys_logging("### TEST END! ###")
            
            
class func_03_set_and_get_switch_attribute_07_FDB_TABLE_SIZE(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        fdb_size = 131072

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_FDB_TABLE_SIZE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_FDB_TABLE_SIZE:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_TABLE_SIZE = %d ###"  %attribute.value.u32)
                    assert ( fdb_size == attribute.value.u32 ) 
        finally:           
            sys_logging("### TEST END! ###")            
            
            
class func_03_set_and_get_switch_attribute_08_L3_NEIGHBOR_TABLE_SIZE(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        neighbor_size = 16384

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_L3_NEIGHBOR_TABLE_SIZE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_L3_NEIGHBOR_TABLE_SIZE:
                    sys_logging("### SAI_SWITCH_ATTR_L3_NEIGHBOR_TABLE_SIZE = %d ###"  %attribute.value.u32)
                    assert ( neighbor_size == attribute.value.u32 ) 
        finally:           
            sys_logging("### TEST END! ###")             
            
            
            
class func_03_set_and_get_switch_attribute_09_L3_ROUTE_TABLE_SIZE(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        route_size = 8192

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_L3_ROUTE_TABLE_SIZE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_L3_ROUTE_TABLE_SIZE:
                    sys_logging("### SAI_SWITCH_ATTR_L3_ROUTE_TABLE_SIZE = %d ###"  %attribute.value.u32)
                    assert ( route_size == attribute.value.u32 ) 
        finally:           
            sys_logging("### TEST END! ###")            
            
# default mode is flex mode            
class func_03_set_and_get_switch_attribute_10_LAG_MEMBERS(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        lag_member = 256

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_LAG_MEMBERS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_LAG_MEMBERS:
                    sys_logging("### SAI_SWITCH_ATTR_LAG_MEMBERS = %d ###"  %attribute.value.u32)
                    assert ( lag_member == attribute.value.u32 ) 
        finally:           
            sys_logging("### TEST END! ###")              
            
# default mode is flex mode            
class func_03_set_and_get_switch_attribute_11_NUMBER_OF_LAGS(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        lag_num = 256

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_NUMBER_OF_LAGS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_NUMBER_OF_LAGS:
                    sys_logging("### SAI_SWITCH_ATTR_NUMBER_OF_LAGS = %d ###"  %attribute.value.u32)
                    assert ( lag_num == attribute.value.u32 ) 
        finally:           
            sys_logging("### TEST END! ###")             
            
# Default is 64 for SAI            
class func_03_set_and_get_switch_attribute_12_ECMP_MEMBERS(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        #ecmp_member = 64
        ecmp_member = 16

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_ECMP_MEMBERS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_ECMP_MEMBERS:
                    sys_logging("### SAI_SWITCH_ATTR_ECMP_MEMBERS = %d ###"  %attribute.value.u32)
                    assert ( ecmp_member == attribute.value.u32 ) 
        finally:           
            sys_logging("### TEST END! ###")              
            
           
class func_03_set_and_get_switch_attribute_13_NUMBER_OF_ECMP_GROUPS(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        ecmp_group = 1024

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_NUMBER_OF_ECMP_GROUPS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_NUMBER_OF_ECMP_GROUPS:
                    sys_logging("### SAI_SWITCH_ATTR_NUMBER_OF_ECMP_GROUPS = %d ###"  %attribute.value.u32)
                    assert ( ecmp_group == attribute.value.u32 ) 
        finally:           
            sys_logging("### TEST END! ###") 
            
            
# default is 8q mode
class func_03_set_and_get_switch_attribute_14_NUMBER_OF_UNICAST_QUEUES(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        unicast_queue = 8
        multicast_queue = 8
        queue_num = 8
        cpu_queue = 128

        warmboot(self.client)
        try:
        
            ids_list = [SAI_SWITCH_ATTR_NUMBER_OF_UNICAST_QUEUES]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_NUMBER_OF_UNICAST_QUEUES:
                    sys_logging("### SAI_SWITCH_ATTR_NUMBER_OF_UNICAST_QUEUES = %d ###"  %attribute.value.u32)
                    assert ( unicast_queue == attribute.value.u32 ) 

            ids_list = [SAI_SWITCH_ATTR_NUMBER_OF_MULTICAST_QUEUES]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_NUMBER_OF_MULTICAST_QUEUES:
                    sys_logging("### SAI_SWITCH_ATTR_NUMBER_OF_MULTICAST_QUEUES = %d ###"  %attribute.value.u32)
                    assert ( multicast_queue == attribute.value.u32 ) 

            ids_list = [SAI_SWITCH_ATTR_NUMBER_OF_QUEUES]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_NUMBER_OF_QUEUES:
                    sys_logging("### SAI_SWITCH_ATTR_NUMBER_OF_QUEUES = %d ###"  %attribute.value.u32)
                    assert ( queue_num == attribute.value.u32 ) 
            
            ids_list = [SAI_SWITCH_ATTR_NUMBER_OF_CPU_QUEUES]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_NUMBER_OF_CPU_QUEUES:
                    sys_logging("### SAI_SWITCH_ATTR_NUMBER_OF_CPU_QUEUES = %d ###"  %attribute.value.u32)
                    assert ( cpu_queue == attribute.value.u32 )                     
        finally:           
            sys_logging("### TEST END! ###") 
            
            
            
class func_03_set_and_get_switch_attribute_15_ON_LINK_ROUTE_SUPPORTED(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        support = 1

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_ON_LINK_ROUTE_SUPPORTED]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_ON_LINK_ROUTE_SUPPORTED:
                    sys_logging("### SAI_SWITCH_ATTR_ON_LINK_ROUTE_SUPPORTED = %d ###"  %attribute.value.booldata)
                    assert ( support == attribute.value.booldata ) 
        finally:           
            sys_logging("### TEST END! ###")             
            
            
            
class func_03_set_and_get_switch_attribute_16_OPER_STATUS(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        status = SAI_SWITCH_OPER_STATUS_UP

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_OPER_STATUS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_OPER_STATUS:
                    sys_logging("### SAI_SWITCH_ATTR_OPER_STATUS = %d ###"  %attribute.value.s32)
                    assert ( status == attribute.value.s32 ) 
        finally:           
            sys_logging("### TEST END! ###") 
            
            
# only support one sensor
# uml can not work            
class func_03_set_and_get_switch_attribute_17_MAX_NUMBER_OF_TEMP_SENSORS(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        sensor_num = 1
        #temp = x
        #max_temp = x
        #average = x

        warmboot(self.client)
        try:
        
            ids_list = [SAI_SWITCH_ATTR_MAX_NUMBER_OF_TEMP_SENSORS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MAX_NUMBER_OF_TEMP_SENSORS:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_NUMBER_OF_TEMP_SENSORS = %d ###"  %attribute.value.u8)
                    assert ( sensor_num == attribute.value.u8 ) 
                        
            #ids_list = [SAI_SWITCH_ATTR_TEMP_LIST]
            #switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            #attr_list = switch_attr_list.attr_list
            #for attribute in attr_list:
            #    if attribute.id == SAI_SWITCH_ATTR_TEMP_LIST:
            #        sys_logging("### SAI_SWITCH_ATTR_TEMP_LIST = %d ###"  %attribute.value.s32list.count)
            #        assert ( sensor_num == attribute.value.s32list.count )
            #        for attr in attribute.value.s32list.s32list:
            #            sys_logging("### SAI_SWITCH_ATTR_TEMP_LIST = %d ###"  %attr)
            #            assert ( temp == attr )                        
            #
            #ids_list = [SAI_SWITCH_ATTR_MAX_TEMP]
            #switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            #attr_list = switch_attr_list.attr_list
            #for attribute in attr_list:
            #    if attribute.id == SAI_SWITCH_ATTR_MAX_TEMP:
            #        sys_logging("### SAI_SWITCH_ATTR_MAX_TEMP = %d ###"  %attribute.value.s32)
            #        assert ( max_temp == attribute.value.s32 ) 
            #
            #ids_list = [SAI_SWITCH_ATTR_AVERAGE_TEMP]
            #switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            #attr_list = switch_attr_list.attr_list
            #for attribute in attr_list:
            #    if attribute.id == SAI_SWITCH_ATTR_AVERAGE_TEMP:
            #        sys_logging("### SAI_SWITCH_ATTR_AVERAGE_TEMP = %d ###"  %attribute.value.s32)
            #        assert ( average == attribute.value.s32 )
            
        finally:           
            sys_logging("### TEST END! ###") 
                        
            

class func_03_set_and_get_switch_attribute_18_ACL_TABLE_MINIMUM_PRIORITY(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        table_min_priority = 1
        table_max_priority = 32767
        entry_min_priority = 1
        entry_max_priority = 65535        
        group_min_priority = 0
        group_max_priority = 0 
        
        warmboot(self.client)
        try:
        
            ids_list = [SAI_SWITCH_ATTR_ACL_TABLE_MINIMUM_PRIORITY,SAI_SWITCH_ATTR_ACL_TABLE_MAXIMUM_PRIORITY,SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY,SAI_SWITCH_ATTR_ACL_ENTRY_MAXIMUM_PRIORITY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_ACL_TABLE_MINIMUM_PRIORITY:
                    sys_logging("### SAI_SWITCH_ATTR_ACL_TABLE_MINIMUM_PRIORITY = %d ###"  %attribute.value.u32)
                    assert ( table_min_priority == attribute.value.u32 ) 
                if attribute.id == SAI_SWITCH_ATTR_ACL_TABLE_MAXIMUM_PRIORITY:
                    sys_logging("### SAI_SWITCH_ATTR_ACL_TABLE_MAXIMUM_PRIORITY = %d ###"  %attribute.value.u32)
                    assert ( table_max_priority == attribute.value.u32 )                     
                if attribute.id == SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY:
                    sys_logging("### SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY = %d ###"  %attribute.value.u32)
                    assert ( entry_min_priority == attribute.value.u32 ) 
                if attribute.id == SAI_SWITCH_ATTR_ACL_ENTRY_MAXIMUM_PRIORITY:
                    sys_logging("### SAI_SWITCH_ATTR_ACL_ENTRY_MAXIMUM_PRIORITY = %d ###"  %attribute.value.u32)
                    assert ( entry_max_priority == attribute.value.u32 ) 
                    
            ids_list = [SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MINIMUM_PRIORITY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            assert ( switch_attr_list.status == SAI_STATUS_NOT_SUPPORTED )

            ids_list = [SAI_SWITCH_ATTR_ACL_TABLE_GROUP_MAXIMUM_PRIORITY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            assert ( switch_attr_list.status == SAI_STATUS_NOT_SUPPORTED )

                    
        finally:           
            sys_logging("### TEST END! ###")             






class func_03_set_and_get_switch_attribute_19_META_DATA_RANGE(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        fdb_range_min = 0
        fdb_range_max = 253
        route_range_min = 0
        route_range_max = 253
        neighbor_range_min = 0
        neighbor_range_max = 0
        port_range_min = 0
        port_range_max = 254
        vlan_range_min = 0
        vlan_range_max = 254
        acl_range_min = 0
        acl_range_max = 16382
        trap_range_min = 78
        trap_range_max = 128
        
        warmboot(self.client)
        try:
        
            ids_list = [SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE,SAI_SWITCH_ATTR_ROUTE_DST_USER_META_DATA_RANGE,SAI_SWITCH_ATTR_NEIGHBOR_DST_USER_META_DATA_RANGE,SAI_SWITCH_ATTR_PORT_USER_META_DATA_RANGE,SAI_SWITCH_ATTR_VLAN_USER_META_DATA_RANGE,SAI_SWITCH_ATTR_ACL_USER_META_DATA_RANGE,SAI_SWITCH_ATTR_ACL_USER_TRAP_ID_RANGE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
            
                if attribute.id == SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE Min = %d ###"  %attribute.value.u32range.min)
                    sys_logging("### SAI_SWITCH_ATTR_FDB_DST_USER_META_DATA_RANGE MAX = %d ###"  %attribute.value.u32range.max)                    
                    assert ( fdb_range_min == attribute.value.u32range.min ) 
                    assert ( fdb_range_max == attribute.value.u32range.max ) 

                if attribute.id == SAI_SWITCH_ATTR_ROUTE_DST_USER_META_DATA_RANGE:
                    sys_logging("### SAI_SWITCH_ATTR_ROUTE_DST_USER_META_DATA_RANGE Min = %d ###"  %attribute.value.u32range.min)
                    sys_logging("### SAI_SWITCH_ATTR_ROUTE_DST_USER_META_DATA_RANGE MAX = %d ###"  %attribute.value.u32range.max)                    
                    assert ( route_range_min == attribute.value.u32range.min ) 
                    assert ( route_range_max == attribute.value.u32range.max ) 

                if attribute.id == SAI_SWITCH_ATTR_NEIGHBOR_DST_USER_META_DATA_RANGE:
                    sys_logging("### SAI_SWITCH_ATTR_NEIGHBOR_DST_USER_META_DATA_RANGE Min = %d ###"  %attribute.value.u32range.min)
                    sys_logging("### SAI_SWITCH_ATTR_NEIGHBOR_DST_USER_META_DATA_RANGE MAX = %d ###"  %attribute.value.u32range.max)                    
                    assert ( neighbor_range_min == attribute.value.u32range.min ) 
                    assert ( neighbor_range_max == attribute.value.u32range.max ) 

                if attribute.id == SAI_SWITCH_ATTR_PORT_USER_META_DATA_RANGE:
                    sys_logging("### SAI_SWITCH_ATTR_PORT_USER_META_DATA_RANGE Min = %d ###"  %attribute.value.u32range.min)
                    sys_logging("### SAI_SWITCH_ATTR_PORT_USER_META_DATA_RANGE MAX = %d ###"  %attribute.value.u32range.max)                    
                    assert ( port_range_min == attribute.value.u32range.min ) 
                    assert ( port_range_max == attribute.value.u32range.max ) 
                    
                if attribute.id == SAI_SWITCH_ATTR_VLAN_USER_META_DATA_RANGE:
                    sys_logging("### SAI_SWITCH_ATTR_VLAN_USER_META_DATA_RANGE Min = %d ###"  %attribute.value.u32range.min)
                    sys_logging("### SAI_SWITCH_ATTR_VLAN_USER_META_DATA_RANGE MAX = %d ###"  %attribute.value.u32range.max)                    
                    assert ( vlan_range_min == attribute.value.u32range.min ) 
                    assert ( vlan_range_max == attribute.value.u32range.max ) 
                    
                if attribute.id == SAI_SWITCH_ATTR_ACL_USER_META_DATA_RANGE:
                    sys_logging("### SAI_SWITCH_ATTR_ACL_USER_META_DATA_RANGE Min = %d ###"  %attribute.value.u32range.min)
                    sys_logging("### SAI_SWITCH_ATTR_ACL_USER_META_DATA_RANGE MAX = %d ###"  %attribute.value.u32range.max)                    
                    assert ( acl_range_min == attribute.value.u32range.min ) 
                    assert ( acl_range_max == attribute.value.u32range.max ) 

                if attribute.id == SAI_SWITCH_ATTR_ACL_USER_TRAP_ID_RANGE:
                    sys_logging("### SAI_SWITCH_ATTR_ACL_USER_TRAP_ID_RANGE Min = %d ###"  %attribute.value.u32range.min)
                    sys_logging("### SAI_SWITCH_ATTR_ACL_USER_TRAP_ID_RANGE MAX = %d ###"  %attribute.value.u32range.max)                    
                    assert ( trap_range_min == attribute.value.u32range.min ) 
                    assert ( trap_range_max == attribute.value.u32range.max ) 
                    
        finally:           
            sys_logging("### TEST END! ###") 






class func_03_set_and_get_switch_attribute_20_DEFAULT_VLAN_ID(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        default_vlan_oid = 4294967334
        default_stp_oid = 16
        max_stp_ins = 128
        default_vrf = 3
        default_1q_bridge = 4294967353

        warmboot(self.client)
        try:
        
            ids_list = [SAI_SWITCH_ATTR_DEFAULT_VLAN_ID,SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID,SAI_SWITCH_ATTR_MAX_STP_INSTANCE,SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID,SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list            
            for attribute in attr_list:
            
                if attribute.id == SAI_SWITCH_ATTR_DEFAULT_VLAN_ID:
                    sys_logging("### SAI_SWITCH_ATTR_DEFAULT_VLAN_ID = %d ###"  %attribute.value.oid)
                    assert ( default_vlan_oid == attribute.value.oid ) 

                if attribute.id == SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID:
                    sys_logging("### SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID = %d ###"  %attribute.value.oid)
                    assert ( default_stp_oid == attribute.value.oid ) 
                    
                if attribute.id == SAI_SWITCH_ATTR_MAX_STP_INSTANCE:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_STP_INSTANCE = %d ###"  %attribute.value.u32)
                    assert ( max_stp_ins == attribute.value.u32 )                     

                if attribute.id == SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID:
                    sys_logging("### SAI_SWITCH_ATTR_DEFAULT_VIRTUAL_ROUTER_ID = %d ###"  %attribute.value.oid)
                    assert ( default_vrf == attribute.value.oid ) 

                if attribute.id == SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID:
                    sys_logging("### SAI_SWITCH_ATTR_DEFAULT_1Q_BRIDGE_ID = %d ###"  %attribute.value.oid)
                    assert ( default_1q_bridge == attribute.value.oid ) 
                    
                    
        finally:           
            sys_logging("### TEST END! ###") 




# TBD
#class func_03_set_and_get_switch_attribute_21_INGRESS_ACL(sai_base_test.ThriftInterfaceDataPlane):
#class func_03_set_and_get_switch_attribute_21_EGRESS_ACL(sai_base_test.ThriftInterfaceDataPlane):


# for TM
class func_03_set_and_get_switch_attribute_22_TOTAL_BUFFER_SIZE(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        size = 9000

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_TOTAL_BUFFER_SIZE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_TOTAL_BUFFER_SIZE:
                    sys_logging("### SAI_SWITCH_ATTR_TOTAL_BUFFER_SIZE = %d ###"  %attribute.value.u64)
                    assert ( size == attribute.value.u64 ) 
        finally:           
            sys_logging("### TEST END! ###") 


# see scenario test case
class func_03_set_and_get_switch_attribute_23_ENTRY(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        size = 0

        warmboot(self.client)
        try:

            ids_list = [SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY,SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY,]
            
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
            
                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 )

                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 )

                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 )

                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 )

                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 )

                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 )

                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 )

                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 )
                    
                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY:
                    sys_logging("### SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY = %d ###"  %attribute.value.u32)
                    assert ( size == attribute.value.u32 ) 
                  
        finally:           
            sys_logging("### TEST END! ###") 



class func_03_set_and_get_switch_attribute_24_DEFAULT_TRAP_GROUP(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        default_trap_oid = 4294967313

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_DEFAULT_TRAP_GROUP]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_DEFAULT_TRAP_GROUP:
                    sys_logging("### SAI_SWITCH_ATTR_DEFAULT_TRAP_GROUP = %d ###"  %attribute.value.oid)
                    assert ( default_trap_oid == attribute.value.oid ) 
        finally:           
            sys_logging("### TEST END! ###") 


class func_03_set_and_get_switch_attribute_25_HASH(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        ecmp_oid = 28
        lag_oid = 8220

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_ECMP_HASH,SAI_SWITCH_ATTR_LAG_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
            
                if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                    assert ( ecmp_oid == attribute.value.oid ) 

                if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                    assert ( lag_oid == attribute.value.oid ) 
                    
        finally:           
            sys_logging("### TEST END! ###") 




class func_03_set_and_get_switch_attribute_26_RESTART(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        warmboot = 0
        type = SAI_SWITCH_RESTART_TYPE_PLANNED

        warmboot(self.client)
        try:
        
            ids_list = [SAI_SWITCH_ATTR_RESTART_WARM,SAI_SWITCH_ATTR_RESTART_TYPE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
            
                if attribute.id == SAI_SWITCH_ATTR_RESTART_WARM:
                    sys_logging("### SAI_SWITCH_ATTR_RESTART_WARM = %d ###"  %attribute.value.booldata)
                    assert ( warmboot == attribute.value.booldata ) 

                if attribute.id == SAI_SWITCH_ATTR_RESTART_TYPE:
                    sys_logging("### SAI_SWITCH_ATTR_RESTART_TYPE = %d ###"  %attribute.value.s32)
                    assert ( type == attribute.value.s32 ) 

            attr_value = sai_thrift_attribute_value_t(booldata=1) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_RESTART_WARM , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  

            ids_list = [SAI_SWITCH_ATTR_RESTART_WARM,SAI_SWITCH_ATTR_RESTART_TYPE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
            
                if attribute.id == SAI_SWITCH_ATTR_RESTART_WARM:
                    sys_logging("### SAI_SWITCH_ATTR_RESTART_WARM = %d ###"  %attribute.value.booldata)
                    assert ( 1 == attribute.value.booldata ) 


            attr_value = sai_thrift_attribute_value_t(booldata=0) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_RESTART_WARM , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  

            ids_list = [SAI_SWITCH_ATTR_RESTART_WARM,SAI_SWITCH_ATTR_RESTART_TYPE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
            
                if attribute.id == SAI_SWITCH_ATTR_RESTART_WARM:
                    sys_logging("### SAI_SWITCH_ATTR_RESTART_WARM = %d ###"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata )                     
        finally:           
            sys_logging("### TEST END! ###") 




class func_03_set_and_get_switch_attribute_27_MIN_PLANNED_RESTART_INTERVAL(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        interval = 10000
        storage_size = 10240

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL,SAI_SWITCH_ATTR_NV_STORAGE_SIZE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
            
                if attribute.id == SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL:
                    sys_logging("### SAI_SWITCH_ATTR_MIN_PLANNED_RESTART_INTERVAL = %d ###"  %attribute.value.u32)
                    assert ( interval == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_NV_STORAGE_SIZE:
                    sys_logging("### SAI_SWITCH_ATTR_NV_STORAGE_SIZE = %d ###"  %attribute.value.u64)
                    assert ( storage_size == attribute.value.u64 ) 
                    
        finally:           
            sys_logging("### TEST END! ###") 



class func_03_set_and_get_switch_attribute_28_MAX_ACL_ACTION_COUNT(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        action_count = 19
        range_count = 524

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_MAX_ACL_ACTION_COUNT,SAI_SWITCH_ATTR_MAX_ACL_RANGE_COUNT]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
            
                if attribute.id == SAI_SWITCH_ATTR_MAX_ACL_ACTION_COUNT:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_ACL_ACTION_COUNT = %d ###"  %attribute.value.u32)
                    assert ( action_count == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_MAX_ACL_RANGE_COUNT:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_ACL_RANGE_COUNT = %d ###"  %attribute.value.u32)
                    assert ( range_count == attribute.value.u32 ) 
                    
        finally:           
            sys_logging("### TEST END! ###") 


# TBD            
#class func_03_set_and_get_switch_attribute_29_ACL_CAPABILITY(sai_base_test.ThriftInterfaceDataPlane):            


class func_03_set_and_get_switch_attribute_30_MCAST_SNOOPING_CAPABILITY(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        mcast_snooping_capability = SAI_SWITCH_MCAST_SNOOPING_CAPABILITY_XG_AND_SG

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_MCAST_SNOOPING_CAPABILITY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:           
                if attribute.id == SAI_SWITCH_ATTR_MCAST_SNOOPING_CAPABILITY:
                    sys_logging("### SAI_SWITCH_ATTR_MCAST_SNOOPING_CAPABILITY = %d ###"  %attribute.value.s32)
                    assert ( mcast_snooping_capability == attribute.value.s32 ) 
                    
        finally:           
            sys_logging("### TEST END! ###") 



# default is store-and-forward mode
class func_03_set_and_get_switch_attribute_31_SWITCHING_MODE(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        switch_mode = SAI_SWITCH_SWITCHING_MODE_STORE_AND_FORWARD

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_SWITCHING_MODE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:           
                if attribute.id == SAI_SWITCH_ATTR_SWITCHING_MODE:
                    sys_logging("### SAI_SWITCH_ATTR_SWITCHING_MODE = %d ###"  %attribute.value.s32)
                    assert ( switch_mode == attribute.value.s32 ) 
                    
        finally:           
            sys_logging("### TEST END! ###")


class func_03_set_and_get_switch_attribute_32_CPU_FLOOD_ENABLE(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        bool = 0

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_BCAST_CPU_FLOOD_ENABLE,SAI_SWITCH_ATTR_MCAST_CPU_FLOOD_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:  
            
                if attribute.id == SAI_SWITCH_ATTR_BCAST_CPU_FLOOD_ENABLE:
                    sys_logging("### SAI_SWITCH_ATTR_BCAST_CPU_FLOOD_ENABLE = %d ###"  %attribute.value.booldata)
                    assert ( bool == attribute.value.booldata ) 
                if attribute.id == SAI_SWITCH_ATTR_MCAST_CPU_FLOOD_ENABLE:
                    sys_logging("### SAI_SWITCH_ATTR_MCAST_CPU_FLOOD_ENABLE = %d ###"  %attribute.value.booldata)
                    assert ( bool == attribute.value.booldata ) 
                    
        finally:           
            sys_logging("### TEST END! ###")



class func_03_set_and_get_switch_attribute_33_SRC_MAC_ADDRESS(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        mac1 = "00:77:66:55:44:00"
        mac2 = "00:44:55:66:77:00"

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_SRC_MAC_ADDRESS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:              
                if attribute.id == SAI_SWITCH_ATTR_SRC_MAC_ADDRESS:
                    sys_logging("### SAI_SWITCH_ATTR_SRC_MAC_ADDRESS = %s ###"  %attribute.value.mac)
                    assert ( mac1 == attribute.value.mac ) 

            attr_value = sai_thrift_attribute_value_t(mac=mac2) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_SRC_MAC_ADDRESS , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  
            
            ids_list = [SAI_SWITCH_ATTR_SRC_MAC_ADDRESS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:              
                if attribute.id == SAI_SWITCH_ATTR_SRC_MAC_ADDRESS:
                    sys_logging("### SAI_SWITCH_ATTR_SRC_MAC_ADDRESS = %s ###"  %attribute.value.mac)
                    assert ( mac2 == attribute.value.mac )             

            attr_value = sai_thrift_attribute_value_t(mac=mac1) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_SRC_MAC_ADDRESS , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  
            
            ids_list = [SAI_SWITCH_ATTR_SRC_MAC_ADDRESS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:              
                if attribute.id == SAI_SWITCH_ATTR_SRC_MAC_ADDRESS:
                    sys_logging("### SAI_SWITCH_ATTR_SRC_MAC_ADDRESS = %s ###"  %attribute.value.mac)
                    assert ( mac1 == attribute.value.mac )
                    
        finally:           
            sys_logging("### TEST END! ###")



class func_03_set_and_get_switch_attribute_34_MAX_LEARNED_ADDRESSES(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:              
                if attribute.id == SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES = %s ###"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 ) 

            attr_value = sai_thrift_attribute_value_t(u32=1000) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  
            
            ids_list = [SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:              
                if attribute.id == SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES = %s ###"  %attribute.value.u32)
                    assert ( 1000 == attribute.value.u32 )             

            attr_value = sai_thrift_attribute_value_t(u32=0) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  
            
            ids_list = [SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:              
                if attribute.id == SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES = %s ###"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )
                    
        finally:           
            sys_logging("### TEST END! ###")
            





class func_03_set_and_get_switch_attribute_35_FDB(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_FDB_AGING_TIME,SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION,SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION,SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list: 
            
                if attribute.id == SAI_SWITCH_ATTR_FDB_AGING_TIME:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_AGING_TIME = %s ###"  %attribute.value.u32)
                    assert ( 300 == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION = %s ###"  %attribute.value.s32)
                    assert ( SAI_PACKET_ACTION_FORWARD == attribute.value.s32 ) 

                if attribute.id == SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION = %s ###"  %attribute.value.s32)
                    assert ( SAI_PACKET_ACTION_FORWARD == attribute.value.s32 ) 

                if attribute.id == SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION = %s ###"  %attribute.value.s32)
                    assert ( SAI_PACKET_ACTION_FORWARD == attribute.value.s32 ) 

            attr_value = sai_thrift_attribute_value_t(u32=123) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_AGING_TIME , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            ids_list = [SAI_SWITCH_ATTR_FDB_AGING_TIME,SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION,SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION,SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list: 
            
                if attribute.id == SAI_SWITCH_ATTR_FDB_AGING_TIME:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_AGING_TIME = %s ###"  %attribute.value.u32)
                    assert ( 123 == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION = %s ###"  %attribute.value.s32)
                    assert ( SAI_PACKET_ACTION_DROP == attribute.value.s32 ) 

                if attribute.id == SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION = %s ###"  %attribute.value.s32)
                    assert ( SAI_PACKET_ACTION_DROP == attribute.value.s32 ) 

                if attribute.id == SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION = %s ###"  %attribute.value.s32)
                    assert ( SAI_PACKET_ACTION_DROP == attribute.value.s32 ) 

            attr_value = sai_thrift_attribute_value_t(u32=300) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_AGING_TIME , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            ids_list = [SAI_SWITCH_ATTR_FDB_AGING_TIME,SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION,SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION,SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list: 
            
                if attribute.id == SAI_SWITCH_ATTR_FDB_AGING_TIME:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_AGING_TIME = %s ###"  %attribute.value.u32)
                    assert ( 300 == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION = %s ###"  %attribute.value.s32)
                    assert ( SAI_PACKET_ACTION_FORWARD == attribute.value.s32 ) 

                if attribute.id == SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION = %s ###"  %attribute.value.s32)
                    assert ( SAI_PACKET_ACTION_FORWARD == attribute.value.s32 ) 

                if attribute.id == SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION:
                    sys_logging("### SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION = %s ###"  %attribute.value.s32)
                    assert ( SAI_PACKET_ACTION_FORWARD == attribute.value.s32 ) 
                    
        finally:           
            sys_logging("### TEST END! ###")



#sdk bug
#class func_03_set_and_get_switch_attribute_36_ECMP(sai_base_test.ThriftInterfaceDataPlane):
#
#    def runTest(self):
#
#        switch_init(self.client)
#
        warmboot(self.client)
#        try:
#        
#            ids_list = [SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM,SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED,SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH]
#            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
#            attr_list = switch_attr_list.attr_list
#            for attribute in attr_list: 
#            
#                if attribute.id == SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM:
#                    sys_logging("### SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM = %s ###"  %attribute.value.s32)
#                    assert ( SAI_HASH_ALGORITHM_CRC == attribute.value.s32 ) 
#
#                if attribute.id == SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED:
#                    sys_logging("### SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED = %s ###"  %attribute.value.u32)
#                    assert ( 65535 == attribute.value.u32 ) 
#
#                if attribute.id == SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH:
#                    sys_logging("### SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH = %s ###"  %attribute.value.booldata)
#                    assert ( 0 == attribute.value.booldata ) 
#                    
#            attr_value = sai_thrift_attribute_value_t(s32=SAI_HASH_ALGORITHM_XOR) 
#            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM , value=attr_value)
#            self.client.sai_thrift_set_switch_attribute(attr) 
#
#            attr_value = sai_thrift_attribute_value_t(u32=65534) 
#            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED , value=attr_value)
#            self.client.sai_thrift_set_switch_attribute(attr) 
#
#            attr_value = sai_thrift_attribute_value_t(booldata=1) 
#            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH , value=attr_value)
#            self.client.sai_thrift_set_switch_attribute(attr) 
#            
#            ids_list = [SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM,SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED,SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH]
#            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
#            attr_list = switch_attr_list.attr_list
#            for attribute in attr_list: 
#            
#                if attribute.id == SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM:
#                    sys_logging("### SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_ALGORITHM = %s ###"  %attribute.value.s32)
#                    assert ( SAI_HASH_ALGORITHM_XOR == attribute.value.s32 ) 
#
#                if attribute.id == SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED:
#                    sys_logging("### SAI_SWITCH_ATTR_ECMP_DEFAULT_HASH_SEED = %s ###"  %attribute.value.u32)
#                    assert ( 65534 == attribute.value.u32 ) 
#
#                if attribute.id == SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH:
#                    sys_logging("### SAI_SWITCH_ATTR_ECMP_DEFAULT_SYMMETRIC_HASH = %s ###"  %attribute.value.booldata)
#                    assert ( 1 == attribute.value.booldata ) 
#                    
#        finally:           
#            sys_logging("### TEST END! ###")


#sdk bug
#class func_03_set_and_get_switch_attribute_37_LAG(sai_base_test.ThriftInterfaceDataPlane):
#
#    def runTest(self):
#
#        switch_init(self.client)
#
        warmboot(self.client)
#        try:
#        
#            ids_list = [SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM,SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED,SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH]
#            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
#            attr_list = switch_attr_list.attr_list
#            for attribute in attr_list: 
#            
#                if attribute.id == SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM:
#                    sys_logging("### SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM = %s ###"  %attribute.value.s32)
#                    assert ( SAI_HASH_ALGORITHM_CRC == attribute.value.s32 ) 
#
#                if attribute.id == SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED:
#                    sys_logging("### SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED = %s ###"  %attribute.value.u32)
#                    assert ( 65535 == attribute.value.u32 ) 
#
#                if attribute.id == SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH:
#                    sys_logging("### SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH = %s ###"  %attribute.value.booldata)
#                    assert ( 0 == attribute.value.booldata ) 
#                    
#            attr_value = sai_thrift_attribute_value_t(s32=SAI_HASH_ALGORITHM_XOR) 
#            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM , value=attr_value)
#            self.client.sai_thrift_set_switch_attribute(attr) 
#
#            attr_value = sai_thrift_attribute_value_t(u32=65534) 
#            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED , value=attr_value)
#            self.client.sai_thrift_set_switch_attribute(attr) 
#
#            attr_value = sai_thrift_attribute_value_t(booldata=1) 
#            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH , value=attr_value)
#            self.client.sai_thrift_set_switch_attribute(attr) 
#            
#            ids_list = [SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM,SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED,SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH]
#            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
#            attr_list = switch_attr_list.attr_list
#            for attribute in attr_list: 
#            
#                if attribute.id == SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM:
#                    sys_logging("### SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_ALGORITHM = %s ###"  %attribute.value.s32)
#                    assert ( SAI_HASH_ALGORITHM_XOR == attribute.value.s32 ) 
#
#                if attribute.id == SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED:
#                    sys_logging("### SAI_SWITCH_ATTR_LAG_DEFAULT_HASH_SEED = %s ###"  %attribute.value.u32)
#                    assert ( 65534 == attribute.value.u32 ) 
#
#                if attribute.id == SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH:
#                    sys_logging("### SAI_SWITCH_ATTR_LAG_DEFAULT_SYMMETRIC_HASH = %s ###"  %attribute.value.booldata)
#                    assert ( 1 == attribute.value.booldata ) 
#                    
#        finally:           
#            sys_logging("### TEST END! ###")
            
            
            
class func_03_set_and_get_switch_attribute_38_COUNTER_REFRESH_INTERVAL(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:             
                if attribute.id == SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL:
                    sys_logging("### SAI_SWITCH_ATTR_COUNTER_REFRESH_INTERVAL = %d ###"  %attribute.value.u32)
                    assert ( 60 == attribute.value.u32 ) 
                    
        finally:           
            sys_logging("### TEST END! ###")         
            
            
# TBD            
#class func_03_set_and_get_switch_attribute_39_QOS(sai_base_test.ThriftInterfaceDataPlane):   



# TBD          
#class func_03_set_and_get_switch_attribute_40_SWITCH_SHELL_ENABLE(sai_base_test.ThriftInterfaceDataPlane):
#
#    def runTest(self):
#
#        switch_init(self.client)
#
        warmboot(self.client)
#        try:
#            ids_list = [SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE]
#            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
#            attr_list = switch_attr_list.attr_list
#            for attribute in attr_list:             
#                if attribute.id == SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE:
#                    sys_logging("### SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE = %d ###"  %attribute.value.booldata)
#                    assert ( 0 == attribute.value.booldata ) 
#
#            attr_value = sai_thrift_attribute_value_t(booldata=1) 
#            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE , value=attr_value)
#            self.client.sai_thrift_set_switch_attribute(attr) 
#
#            ids_list = [SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE]
#            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
#            attr_list = switch_attr_list.attr_list
#            for attribute in attr_list:             
#                if attribute.id == SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE:
#                    sys_logging("### SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE = %d ###"  %attribute.value.booldata)
#                    assert ( 1 == attribute.value.booldata ) 
#            
#            attr_value = sai_thrift_attribute_value_t(booldata=0) 
#            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE , value=attr_value)
#            self.client.sai_thrift_set_switch_attribute(attr) 
#
#            ids_list = [SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE]
#            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
#            attr_list = switch_attr_list.attr_list
#            for attribute in attr_list:             
#                if attribute.id == SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE:
#                    sys_logging("### SAI_SWITCH_ATTR_SWITCH_SHELL_ENABLE = %d ###"  %attribute.value.booldata)
#                    assert ( 0 == attribute.value.booldata )                     
#        finally:           
#            sys_logging("### TEST END! ###")   
            
            
            
           
class func_03_set_and_get_switch_attribute_41_SWITCH_PROFILE_ID(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_SWITCH_PROFILE_ID,SAI_SWITCH_ATTR_SWITCH_HARDWARE_INFO,SAI_SWITCH_ATTR_INIT_SWITCH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_SWITCH_PROFILE_ID:
                    sys_logging("### SAI_SWITCH_ATTR_SWITCH_PROFILE_ID = %d ###"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_SWITCH_HARDWARE_INFO:
                    sys_logging("### SAI_SWITCH_ATTR_SWITCH_HARDWARE_INFO = %d ###"  %attribute.value.s8list.count)
                    assert ( 0 == attribute.value.s8list.count )                    

                if attribute.id == SAI_SWITCH_ATTR_INIT_SWITCH:
                    sys_logging("### SAI_SWITCH_ATTR_INIT_SWITCH = %d ###"  %attribute.value.booldata)
                    assert ( 1 == attribute.value.booldata )
                    
        finally:           
            sys_logging("### TEST END! ###")   
                        
            
            
class func_03_set_and_get_switch_attribute_42_MAX_TWAMP_SESSION(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_MAX_TWAMP_SESSION]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_MAX_TWAMP_SESSION:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_TWAMP_SESSION = %d ###"  %attribute.value.u32)
                    assert ( 4 == attribute.value.u32 ) 

            attr_value = sai_thrift_attribute_value_t(u32=6) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MAX_TWAMP_SESSION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            ids_list = [SAI_SWITCH_ATTR_MAX_TWAMP_SESSION]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_MAX_TWAMP_SESSION:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_TWAMP_SESSION = %d ###"  %attribute.value.u32)
                    assert ( 6 == attribute.value.u32 ) 
                    
            attr_value = sai_thrift_attribute_value_t(u32=8) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MAX_TWAMP_SESSION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            ids_list = [SAI_SWITCH_ATTR_MAX_TWAMP_SESSION]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_MAX_TWAMP_SESSION:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_TWAMP_SESSION = %d ###"  %attribute.value.u32)
                    assert ( 8 == attribute.value.u32 ) 

            attr_value = sai_thrift_attribute_value_t(u32=4) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MAX_TWAMP_SESSION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            ids_list = [SAI_SWITCH_ATTR_MAX_TWAMP_SESSION]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_MAX_TWAMP_SESSION:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_TWAMP_SESSION = %d ###"  %attribute.value.u32)
                    assert ( 4 == attribute.value.u32 ) 
                    
        finally:           
            sys_logging("### TEST END! ###")            
            
            
            
class func_03_set_and_get_switch_attribute_43_FAST_API_ENABLE(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_FAST_API_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_FAST_API_ENABLE:
                    sys_logging("### SAI_SWITCH_ATTR_FAST_API_ENABLE = %d ###"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata ) 
                    
        finally:           
            sys_logging("### TEST END! ###")   
            

#TBD
#class func_03_set_and_get_switch_attribute_44_ACL_STAGE_INGRESS(sai_base_test.ThriftInterfaceDataPlane):
#class func_03_set_and_get_switch_attribute_44_ACL_STAGE_EGRESS(sai_base_test.ThriftInterfaceDataPlane):


class func_03_set_and_get_switch_attribute_45_QOS_NUM_LOSSLESS_QUEUES(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUES]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUES:
                    sys_logging("### SAI_SWITCH_ATTR_QOS_NUM_LOSSLESS_QUEUES = %d ###"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 ) 
                    
        finally:           
            sys_logging("### TEST END! ###") 


# u16 and s16 is same treat in python by default
class func_03_set_and_get_switch_attribute_46_TPID_OUTER_VLAN(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        tpid = 0x8100
        
        warmboot(self.client)
        try:
        
            ids_list = [SAI_SWITCH_ATTR_TPID_OUTER_VLAN,SAI_SWITCH_ATTR_TPID_INNER_VLAN]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_TPID_OUTER_VLAN:
                    u161 = ctypes.c_uint16(attribute.value.u16) 
                    sys_logging("### SAI_SWITCH_ATTR_TPID_OUTER_VLAN = %d ###"  %u161.value)
                    assert ( tpid == u161.value ) 

                if attribute.id == SAI_SWITCH_ATTR_TPID_INNER_VLAN:
                    u162 = ctypes.c_uint16(attribute.value.u16) 
                    sys_logging("### SAI_SWITCH_ATTR_TPID_INNER_VLAN = %d ###"  %u162.value)
                    assert ( tpid == u162.value ) 

            attr_value = sai_thrift_attribute_value_t(u16=100) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_TPID_OUTER_VLAN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(u16=200) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_TPID_INNER_VLAN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            ids_list = [SAI_SWITCH_ATTR_TPID_OUTER_VLAN,SAI_SWITCH_ATTR_TPID_INNER_VLAN]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_TPID_OUTER_VLAN:
                    sys_logging("### SAI_SWITCH_ATTR_TPID_OUTER_VLAN = %d ###"  %attribute.value.u16)
                    assert ( 100 == attribute.value.u16 ) 

                if attribute.id == SAI_SWITCH_ATTR_TPID_INNER_VLAN:
                    sys_logging("### SAI_SWITCH_ATTR_TPID_INNER_VLAN = %d ###"  %attribute.value.u16)
                    assert ( 200 == attribute.value.u16 ) 


            u16 = ctypes.c_int16(tpid) 
            
            attr_value = sai_thrift_attribute_value_t(u16=u16.value) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_TPID_OUTER_VLAN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(u16=u16.value) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_TPID_INNER_VLAN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            ids_list = [SAI_SWITCH_ATTR_TPID_OUTER_VLAN,SAI_SWITCH_ATTR_TPID_INNER_VLAN]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_TPID_OUTER_VLAN:
                    u161 = ctypes.c_uint16(attribute.value.u16) 
                    sys_logging("### SAI_SWITCH_ATTR_TPID_OUTER_VLAN = %d ###"  %u161.value)
                    assert ( tpid == u161.value ) 

                if attribute.id == SAI_SWITCH_ATTR_TPID_INNER_VLAN:
                    u162 = ctypes.c_uint16(attribute.value.u16) 
                    sys_logging("### SAI_SWITCH_ATTR_TPID_INNER_VLAN = %d ###"  %u162.value)
                    assert ( tpid == u162.value ) 
                                      
        finally:           
            sys_logging("### TEST END! ###") 



            
class func_03_set_and_get_switch_attribute_46_CRC_CHECK_ENABLE(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        
        warmboot(self.client)
        try:
        
            ids_list = [SAI_SWITCH_ATTR_CRC_CHECK_ENABLE,SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_CRC_CHECK_ENABLE:
                    sys_logging("### SAI_SWITCH_ATTR_CRC_CHECK_ENABLE = %d ###"  %attribute.value.booldata)
                    assert ( 1 == attribute.value.booldata ) 

                if attribute.id == SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE:
                    sys_logging("### SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE = %d ###"  %attribute.value.booldata)
                    assert ( 1 == attribute.value.booldata )
                    
            attr_value = sai_thrift_attribute_value_t(booldata=0) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_CRC_CHECK_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(booldata=0) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            
            ids_list = [SAI_SWITCH_ATTR_CRC_CHECK_ENABLE,SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_CRC_CHECK_ENABLE:
                    sys_logging("### SAI_SWITCH_ATTR_CRC_CHECK_ENABLE = %d ###"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata ) 

                if attribute.id == SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE:
                    sys_logging("### SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE = %d ###"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata )

            attr_value = sai_thrift_attribute_value_t(booldata=1) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_CRC_CHECK_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(booldata=1) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            
            ids_list = [SAI_SWITCH_ATTR_CRC_CHECK_ENABLE,SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_CRC_CHECK_ENABLE:
                    sys_logging("### SAI_SWITCH_ATTR_CRC_CHECK_ENABLE = %d ###"  %attribute.value.booldata)
                    assert ( 1 == attribute.value.booldata ) 

                if attribute.id == SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE:
                    sys_logging("### SAI_SWITCH_ATTR_CRC_RECALCULATION_ENABLE = %d ###"  %attribute.value.booldata)
                    assert ( 1 == attribute.value.booldata )
                                     
        finally:           
            sys_logging("### TEST END! ###") 
            
            

class func_03_set_and_get_switch_attribute_47_MAX_BFD_SESSION(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        l_disc = 100
        r_disc = 200
        udp_srcport = 49153
        multihop = 0
        vr_id = sai_thrift_get_default_router_id(self.client)
        min_tx = 5
        min_rx = 6
        default_mult = 3
        
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_ip = '10.10.10.1'
        dst_ip = '20.20.20.1'
        
        bfd_id = sai_thrift_create_ip_bfd_session(self.client, l_disc, r_disc, udp_srcport, multihop, vr_id, addr_family, src_ip, dst_ip, min_tx, min_rx, default_mult)
        sys_logging("creat bfd session = %d" %bfd_id)
        
        warmboot(self.client)
        try:
        
            ids_list = [SAI_SWITCH_ATTR_NUMBER_OF_BFD_SESSION,SAI_SWITCH_ATTR_MAX_BFD_SESSION,SAI_SWITCH_ATTR_SUPPORTED_IPV4_BFD_SESSION_OFFLOAD_TYPE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    

                if attribute.id == SAI_SWITCH_ATTR_NUMBER_OF_BFD_SESSION:
                    sys_logging("### SAI_SWITCH_ATTR_NUMBER_OF_BFD_SESSION = %d ###"  %attribute.value.u32)
                    assert ( 1 == attribute.value.u32 ) 
                    
                if attribute.id == SAI_SWITCH_ATTR_MAX_BFD_SESSION:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_BFD_SESSION = %d ###"  %attribute.value.u32)
                    assert ( 2048 == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_SUPPORTED_IPV4_BFD_SESSION_OFFLOAD_TYPE:
                    sys_logging("### SAI_SWITCH_ATTR_SUPPORTED_IPV4_BFD_SESSION_OFFLOAD_TYPE count = %d ###"  %attribute.value.s32list.count)
                    assert ( 1 == attribute.value.s32list.count )
                    for att1 in attribute.value.s32list.s32list:
                        sys_logging("### SAI_SWITCH_ATTR_SUPPORTED_IPV4_BFD_SESSION_OFFLOAD_TYPE list = %d ###"  %att1)
                        assert ( SAI_BFD_SESSION_OFFLOAD_TYPE_FULL == att1 )                    

            ids_list = [SAI_SWITCH_ATTR_SUPPORTED_IPV6_BFD_SESSION_OFFLOAD_TYPE,SAI_SWITCH_ATTR_MIN_BFD_RX,SAI_SWITCH_ATTR_MIN_BFD_TX]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:  
            
                if attribute.id == SAI_SWITCH_ATTR_SUPPORTED_IPV6_BFD_SESSION_OFFLOAD_TYPE:
                    sys_logging("### SAI_SWITCH_ATTR_SUPPORTED_IPV6_BFD_SESSION_OFFLOAD_TYPE count = %d ###"  %attribute.value.s32list.count)
                    assert ( 1 == attribute.value.s32list.count )
                    for att2 in attribute.value.s32list.s32list:
                        sys_logging("### SAI_SWITCH_ATTR_SUPPORTED_IPV6_BFD_SESSION_OFFLOAD_TYPE list = %d ###"  %att2)
                        assert ( SAI_BFD_SESSION_OFFLOAD_TYPE_FULL == att2 )                       

                if attribute.id == SAI_SWITCH_ATTR_MIN_BFD_RX:
                    sys_logging("### SAI_SWITCH_ATTR_MIN_BFD_RX = %d ###"  %attribute.value.u32)
                    assert ( 1 == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_MIN_BFD_TX:
                    sys_logging("### SAI_SWITCH_ATTR_MIN_BFD_TX = %d ###"  %attribute.value.u32)
                    assert ( 1 == attribute.value.u32 ) 
                    
        finally:   
            sai_thrift_remove_bfd(self.client, bfd_id)        
            sys_logging("### TEST END! ###") 





class func_03_set_and_get_switch_attribute_48_VXLAN_DEFAULT_ROUTER_MAC(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        default_mac = "00:00:00:00:00:00"
        default_port = 4789
        mac1 = "00:00:00:00:00:01"
        port1 = 1234
        
        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC,SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:  
            
                if attribute.id == SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC:
                    sys_logging("### SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC = %s ###"  %attribute.value.mac)
                    assert ( default_mac == attribute.value.mac ) 

                if attribute.id == SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT:
                    sys_logging("### SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT = %d ###"  %attribute.value.u16)
                    assert ( default_port == attribute.value.u16 )
                    
            attr_value = sai_thrift_attribute_value_t(mac=mac1) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(u16=port1) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)             

            ids_list = [SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC,SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:  
            
                if attribute.id == SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC:
                    sys_logging("### SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC = %s ###"  %attribute.value.mac)
                    assert ( mac1 == attribute.value.mac ) 

                if attribute.id == SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT:
                    sys_logging("### SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT = %d ###"  %attribute.value.u16)
                    assert ( port1 == attribute.value.u16 )

            attr_value = sai_thrift_attribute_value_t(mac=default_mac) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(u16=default_port) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)             

            ids_list = [SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC,SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:  
            
                if attribute.id == SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC:
                    sys_logging("### SAI_SWITCH_ATTR_VXLAN_DEFAULT_ROUTER_MAC = %s ###"  %attribute.value.mac)
                    assert ( default_mac == attribute.value.mac ) 

                if attribute.id == SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT:
                    sys_logging("### SAI_SWITCH_ATTR_VXLAN_DEFAULT_PORT = %d ###"  %attribute.value.u16)
                    assert ( default_port == attribute.value.u16 )
                    
        finally:           
            sys_logging("### TEST END! ###")   


class func_03_set_and_get_switch_attribute_48_SUPPORTED_EXTENDED_STATS_MODE(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        stats_mode_list = [SAI_STATS_MODE_READ,SAI_STATS_MODE_READ_AND_CLEAR]
        
        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_SUPPORTED_EXTENDED_STATS_MODE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:           
                if attribute.id == SAI_SWITCH_ATTR_SUPPORTED_EXTENDED_STATS_MODE:
                    sys_logging("### SAI_SWITCH_ATTR_SUPPORTED_EXTENDED_STATS_MODE = %s ###"  %attribute.value.s32list.count)
                    assert ( 2 == attribute.value.s32list.count )
                    for att1 in attribute.value.s32list.s32list:
                        sys_logging("### SAI_SWITCH_ATTR_SUPPORTED_EXTENDED_STATS_MODE list = %d ###"  %att1)
                        assert ( att1 in stats_mode_list )  


        finally:           
            sys_logging("### TEST END! ###")  
            
            
class func_03_set_and_get_switch_attribute_49_UNINIT_DATA_PLANE_ON_REMOVAL(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
      
        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL,SAI_SWITCH_ATTR_PRE_SHUTDOWN]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:  
            
                if attribute.id == SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL:
                    sys_logging("### SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL = %d ###"  %attribute.value.booldata)
                    assert ( 1 == attribute.value.booldata ) 

                if attribute.id == SAI_SWITCH_ATTR_PRE_SHUTDOWN:
                    sys_logging("### SAI_SWITCH_ATTR_PRE_SHUTDOWN = %d ###"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata ) 
                    
            attr_value = sai_thrift_attribute_value_t(booldata=0) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(booldata=1) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_PRE_SHUTDOWN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            
            ids_list = [SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL,SAI_SWITCH_ATTR_PRE_SHUTDOWN]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:  
            
                if attribute.id == SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL:
                    sys_logging("### SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL = %d ###"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata ) 

                if attribute.id == SAI_SWITCH_ATTR_PRE_SHUTDOWN:
                    sys_logging("### SAI_SWITCH_ATTR_PRE_SHUTDOWN = %d ###"  %attribute.value.booldata)
                    assert ( 1 == attribute.value.booldata ) 
                    
            attr_value = sai_thrift_attribute_value_t(booldata=1) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            attr_value = sai_thrift_attribute_value_t(booldata=0) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_PRE_SHUTDOWN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            
            ids_list = [SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL,SAI_SWITCH_ATTR_PRE_SHUTDOWN]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:  
            
                if attribute.id == SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL:
                    sys_logging("### SAI_SWITCH_ATTR_UNINIT_DATA_PLANE_ON_REMOVAL = %d ###"  %attribute.value.booldata)
                    assert ( 1 == attribute.value.booldata ) 

                if attribute.id == SAI_SWITCH_ATTR_PRE_SHUTDOWN:
                    sys_logging("### SAI_SWITCH_ATTR_PRE_SHUTDOWN = %d ###"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata ) 
                    
        finally:           
            sys_logging("### TEST END! ###") 




class func_03_set_and_get_switch_attribute_50_NUMBER_OF_Y1731_SESSION(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        vlan = 10
        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        
        
        meg_type = SAI_Y1731_MEG_TYPE_ETHER_VLAN
        meg_name = "abcd"
        level = 3
        
        meg_id = sai_thrift_create_y1731_meg(self.client, meg_type, meg_name, level)
        sys_logging("creat meg id = %d" %meg_id)
        
        dir = SAI_Y1731_SESSION_DIR_DOWNMEP
        local_mep_id = 10
        ccm_period = 1 
        ccm_en = 1
        mep_id = sai_thrift_create_y1731_eth_session(self.client, meg_id, dir, local_mep_id, ccm_period, ccm_en, port_id=port1, vlan_id = vlan)
        
        sys_logging("creat mep id = %d" %mep_id)
        
        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_NUMBER_OF_Y1731_SESSION,SAI_SWITCH_ATTR_MAX_Y1731_SESSION,SAI_SWITCH_ATTR_SUPPORTED_Y1731_SESSION_PERFORMANCE_MONITOR_OFFLOAD_TYPE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:    
            
                if attribute.id == SAI_SWITCH_ATTR_NUMBER_OF_Y1731_SESSION:
                    sys_logging("### SAI_SWITCH_ATTR_NUMBER_OF_Y1731_SESSION = %d ###"  %attribute.value.u32)
                    assert ( 1 == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_MAX_Y1731_SESSION:
                    sys_logging("### SAI_SWITCH_ATTR_MAX_Y1731_SESSION = %d ###"  %attribute.value.u32)
                    assert ( 2048 == attribute.value.u32 ) 

                if attribute.id == SAI_SWITCH_ATTR_SUPPORTED_Y1731_SESSION_PERFORMANCE_MONITOR_OFFLOAD_TYPE:
                    sys_logging("### SAI_SWITCH_ATTR_SUPPORTED_Y1731_SESSION_PERFORMANCE_MONITOR_OFFLOAD_TYPE count = %d ###"  %attribute.value.s32list.count)
                    assert ( 1 == attribute.value.s32list.count )
                    for att1 in attribute.value.s32list.s32list:
                        sys_logging("### SAI_SWITCH_ATTR_SUPPORTED_Y1731_SESSION_PERFORMANCE_MONITOR_OFFLOAD_TYPE list = %d ###"  %att1)
                        assert ( SAI_Y1731_SESSION_PERF_MONITOR_OFFLOAD_TYPE_PARTIAL == att1 )   
                        
        finally:     
            self.client.sai_thrift_remove_y1731_session(mep_id)
            self.client.sai_thrift_remove_y1731_meg(meg_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)     
            sys_logging("### TEST END! ###") 





class func_04_get_switch_stats_and_clear_switch_stats(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
               
        type = SAI_DEBUG_COUNTER_TYPE_SWITCH_IN_DROP_REASONS
        in_drop_list = [SAI_IN_DROP_REASON_SMAC_MULTICAST]
        sw_counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list)
        sys_logging("creat sw_counter_id = %d" %sw_counter_id)
                       
        attrs = self.client.sai_thrift_get_debug_counter_attribute(sw_counter_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
            if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                sys_logging("get switch debug index = %d" %a.value.u32)
                sw_debug_counter_index = a.value.u32
        
        vlan_id1 = 10
       
        port1 = port_list[0]
        port2 = port_list[1]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mcastmac = 'ff:ff:00:00:00:01'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
	       
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mcastmac,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        exp_pkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mcastmac,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
        warmboot(self.client)
        try:
           
            sys_logging("Sending L2 packet port 1 -> port 2 , mcast src mac, discard by SAI_IN_DROP_REASON_SMAC_MULTICAST")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 1)
                      
            debug_index_list2 = [sw_debug_counter_index+SAI_SWITCH_STAT_IN_DROP_REASON_RANGE_BASE]
            counters_results = self.client.sai_thrift_get_switch_stats(debug_index_list2, len(debug_index_list2))
            sys_logging("switch drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)
            
            status = self.client.sai_thrift_clear_switch_stats(debug_index_list2, len(debug_index_list2))
            sys_logging("switch clear status = %d " %(status))
            assert (status == SAI_STATUS_SUCCESS)
            
            counters_results = self.client.sai_thrift_get_switch_stats(debug_index_list2, len(debug_index_list2))
            sys_logging("switch drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 0)
            
            
        finally:
        
            self.client.sai_thrift_clear_port_all_stats(port1)
            self.client.sai_thrift_clear_port_all_stats(port2)
            
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)
           
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
          
            self.client.sai_thrift_remove_debug_counter(sw_counter_id)




class func_05_get_switch_stats_ext(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
               
        type = SAI_DEBUG_COUNTER_TYPE_SWITCH_OUT_DROP_REASONS
        out_drop_list = [SAI_OUT_DROP_REASON_EGRESS_VLAN_FILTER]
        sw_counter_id = sai_thrift_create_debugcounter(self.client, type, None, out_drop_list)
        sys_logging("creat sw_counter_id = %d" %sw_counter_id)
                       
        attrs = self.client.sai_thrift_get_debug_counter_attribute(sw_counter_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        
        for a in attrs.attr_list:
            if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                sys_logging("get switch debug index = %d" %a.value.u32)
                sw_debug_counter_index = a.value.u32
        
        vlan_id1 = 10
        vlan_id2 = 10 
        
        port1 = port_list[0]
        port2 = port_list[1]
        
        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mcastmac = 'ff:ff:00:00:00:01'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id2)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
	       
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)

        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
        value = 1
        attr_value = sai_thrift_attribute_value_t(booldata=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
        
        
        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        exp_pkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
        warmboot(self.client)
        try:
           
            sys_logging("Sending L2 packet port 1 -> port 2 , port 2 do not allow vlan_id1, discard by SAI_OUT_DROP_REASON_EGRESS_VLAN_FILTER")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 1)
                      
            debug_index_list2 = [sw_debug_counter_index+SAI_SWITCH_STAT_OUT_DROP_REASON_RANGE_BASE]
            
            mode = SAI_STATS_MODE_READ
            counters_results = self.client.sai_thrift_get_switch_stats_ext(debug_index_list2, mode, len(debug_index_list2))
            sys_logging("switch drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)

            mode = SAI_STATS_MODE_READ_AND_CLEAR
            counters_results = self.client.sai_thrift_get_switch_stats_ext(debug_index_list2, mode, len(debug_index_list2))
            sys_logging("switch drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 1)
                        
            counters_results = self.client.sai_thrift_get_switch_stats_ext(debug_index_list2, mode, len(debug_index_list2))
            sys_logging("switch drop stats = %d " %(counters_results[0]))
            assert (counters_results[0] == 0)
            
            
        finally:
        
            self.client.sai_thrift_clear_port_all_stats(port1)
            self.client.sai_thrift_clear_port_all_stats(port2)
            
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port2)
           
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            
            self.client.sai_thrift_remove_debug_counter(sw_counter_id)

            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
            

#TBD
#scenario_01_switch_ingress_and_egrees_acl


class scenario_02_get_available_ip_route_entry_v4(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        dmac1 = '00:11:22:33:44:55'
        ip_addr1 = '10.10.10.1'
        ip_addr_subnet = []
        ip_mask = '255.255.255.254'
        mac = ''
        route_num = 4096

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)


        for i in range(route_num):
            ip_addr_subnet.append(integer_to_ip4(1+i*2))            
            sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop1)

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY, SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY :
                    sys_logging ("ipv4_route_cnt: %d " %attribute.value.u32)
                    if route_num != attribute.value.u32:
                        raise NotImplementedError()
                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY :
                    sys_logging ("ipv6_route_cnt: %d " %attribute.value.u32)
                    if 0 != attribute.value.u32:
                        raise NotImplementedError()

        finally:
            for i in range(route_num):
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop1)

            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)



class scenario_02_get_available_ip_route_entry_v6(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac1 = '00:11:22:33:44:55'
        ip_addr_subnet = []
        mac = ''
        route_num = 4095

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
        nhop = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)

        dest_ip = '0000:5678:9abc:def0:4422:1133:5577:0000'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff'
        dest_int = ip6_to_integer(dest_ip)
        
        for i in range(route_num):
            ip_addr_subnet.append(integer_to_ip6(dest_int+i))
            sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop)            
            
        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY, SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_IPV4_ROUTE_ENTRY :
                    sys_logging ("ipv4_route_cnt: %d " %attribute.value.u32)
                    if 0 != attribute.value.u32:
                        raise NotImplementedError()
                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_IPV6_ROUTE_ENTRY :
                    sys_logging ("ipv6_route_cnt: %d " %attribute.value.u32)
                    if route_num != attribute.value.u32:
                        raise NotImplementedError()
        finally:
            for i in range(route_num):
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop)
            
            self.client.sai_thrift_remove_next_hop(nhop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

                        
class scenario_03_get_available_nexthop_v4(sai_base_test.ThriftInterfaceDataPlane):

 def runTest(self):
 
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        dest_mac = []
        ip_addr = []
        ip_addr_subnet = []
        ip_mask = '255.255.255.255'
        nhop = []
        mac = ''
        next_hop_num = 1023

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_mac_start = ['01:22:33:44:55:', '11:22:33:44:55:', '21:22:33:44:55:', '31:22:33:44:55:', '41:22:33:44:55:', '51:22:33:44:55:', '61:22:33:44:55:', '71:22:33:44:55:', '81:22:33:44:55:', '91:22:33:44:55:', 'a1:22:33:44:55:']

        for i in range(next_hop_num):
            dest_mac.append(src_mac_start[i/99] + str(i%99).zfill(2))
            ip_addr.append(integer_to_ip4(1+i))
            ip_addr_subnet.append(integer_to_ip4(0xff0000+i))
            sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
            nhop.append(sai_thrift_create_nhop(self.client, addr_family, ip_addr[i], rif_id2))
            sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop[i])

        warmboot(self.client)
        try:           
            ids_list = [ SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY,  SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEXTHOP_ENTRY :
                    sys_logging ("ipv4_nexthop_cnt: %d " %attribute.value.u32)
                    if next_hop_num != attribute.value.u32:
                        raise NotImplementedError()
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEXTHOP_ENTRY :
                    sys_logging ("ipv6_nexthop_cnt: %d " %attribute.value.u32)
                    if 0 != attribute.value.u32:
                        raise NotImplementedError()
        finally:
            for i in range(next_hop_num):
                sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet[i], ip_mask, nhop[i])
                self.client.sai_thrift_remove_next_hop(nhop[i])
                sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_04_get_available_neighbor_v4(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        dest_mac = []
        ip_addr = []
        mac = ''
        neighbor_num = 1023

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        src_mac_start = ['01:22:33:44:55:', '11:22:33:44:55:', '21:22:33:44:55:', '31:22:33:44:55:', '41:22:33:44:55:', '51:22:33:44:55:', '61:22:33:44:55:', '71:22:33:44:55:', '81:22:33:44:55:', '91:22:33:44:55:', 'a1:22:33:44:55:']

        for i in range(neighbor_num):
            dest_mac.append(src_mac_start[i/99] + str(i%99).zfill(2))
            ip_addr.append(integer_to_ip4(1+i))
            sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])

        warmboot(self.client)
        try:            
            ids_list = [ SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY,  SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY :
                    sys_logging ("ipv4_neighbor_cnt: %d " %attribute.value.u32)
                    if neighbor_num != attribute.value.u32:
                        raise NotImplementedError()
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY :
                    sys_logging ("ipv6_neighbor_cnt: %d " %attribute.value.u32)
                    if 0 != attribute.value.u32:
                        raise NotImplementedError()
                    
        finally:
            for i in range(neighbor_num):
                sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)




class scenario_04_get_available_neighbor_v6(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        dest_mac = []
        ip_addr = []
        mac = ''
        neighbor_num = 1023

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        src_mac_start = ['01:22:33:44:55:', '11:22:33:44:55:', '21:22:33:44:55:', '31:22:33:44:55:', '41:22:33:44:55:', '51:22:33:44:55:', '61:22:33:44:55:', '71:22:33:44:55:', '81:22:33:44:55:', '91:22:33:44:55:', 'a1:22:33:44:55:']
        dest_ip = '1234:5678:9abc:def0:4422:1133:5577:0000'
        dest_int = ip6_to_integer(dest_ip)
        for i in range(neighbor_num):
            dest_mac.append(src_mac_start[i/99] + str(i%99).zfill(2))
            ip_addr.append(integer_to_ip6(dest_int+i))
            sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])

        warmboot(self.client)
        try:
        
            ids_list = [SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY,  SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_IPV4_NEIGHBOR_ENTRY :
                    sys_logging ("ipv4_neighbor_cnt: %d " %attribute.value.u32)
                    if 0 != attribute.value.u32:
                        raise NotImplementedError()
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_IPV6_NEIGHBOR_ENTRY :
                    sys_logging ("ipv6_neighbor_cnt: %d " %attribute.value.u32)
                    if neighbor_num != attribute.value.u32:
                        raise NotImplementedError()
        finally:
            for i in range(neighbor_num):
                sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr[i], dest_mac[i])
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)



class scenario_05_get_available_nexthop_group(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        print
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)

        warmboot(self.client)
        try:
            ids_list = [ SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_ENTRY :
                    sys_logging ("nexthop_group_cnt: %d " %attribute.value.u32)
                    if 1 != attribute.value.u32:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_virtual_router(vr_id)




class scenario_05_get_available_nexthop_group_member(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr1, dmac2)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif2)
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_NEXT_HOP_GROUP_MEMBER_ENTRY :
                    sys_logging ("nexthop_group_member_cnt: %d" %attribute.value.u32)
                    if 2 != attribute.value.u32:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)

            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)

            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr1, dmac2)

            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)

            self.client.sai_thrift_remove_virtual_router(vr_id)



class scenario_06_get_available_fdb(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        print
        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        mac1='00:00:00:00:00:11'
        mac2='00:00:00:00:00:22'
        mac3='00:00:00:00:00:33'
        mac4='00:00:00:00:00:44'
        mac5='00:00:00:00:00:55'
        mac6='00:00:00:00:00:66'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_id=1
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_LEARN_DISABLE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(switch.default_vlan.oid, attr)
        sai_thrift_flush_fdb_by_vlan(self.client, switch.default_vlan.oid)

        vlan_id1 = 10
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_id2 = 20
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_id3 = 30
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_id4 = 40
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
        vlan_id5 = 50
        vlan_oid5 = sai_thrift_create_vlan(self.client, vlan_id5)
        vlan_id6 = 60
        vlan_oid6 = sai_thrift_create_vlan(self.client, vlan_id6)
        
        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port0, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac2, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid3, mac3, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid4, mac4, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid5, mac5, port0, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid6, mac6, port1, mac_action)

        warmboot(self.client)
        try:
            ids_list = [SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY:
                    sys_logging ("fdb_cnt: %d" %attribute.value.u32)
                    if 6 != attribute.value.u32:
                        raise NotImplementedError()
                    
            sai_thrift_delete_fdb(self.client, vlan_oid5, mac5, port0)
            sai_thrift_delete_fdb(self.client, vlan_oid6, mac6, port1)
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY:
                    sys_logging ("fdb_cnt: %d" %attribute.value.u32)
                    if 4 != attribute.value.u32:
                        raise NotImplementedError()
                    
            sai_thrift_create_fdb(self.client, vlan_oid5, mac5, port0, mac_action)
            sai_thrift_create_fdb(self.client, vlan_oid6, mac6, port1, mac_action)
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_AVAILABLE_FDB_ENTRY:
                    sys_logging ("fdb_cnt: %d" %attribute.value.u32)
                    if 6 != attribute.value.u32:
                        raise NotImplementedError()
        finally: 
        
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1, port0)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac2, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid3, mac3, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid4, mac4, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid5, mac5, port0)
            sai_thrift_delete_fdb(self.client, vlan_oid6, mac6, port1)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)
            self.client.sai_thrift_remove_vlan(vlan_oid5)
            self.client.sai_thrift_remove_vlan(vlan_oid6)
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(switch.default_vlan.oid, attr)


class scenario_07_get_available_l2mc(sai_base_test.ThriftInterfaceDataPlane):

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
        vlan_id = 10
        grp_attr_list = []

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port5, SAI_VLAN_TAGGING_MODE_TAGGED)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        default_addr = '0.0.0.0'
        dip_addr1 = '230.255.1.1'
        sip_addr1 = '10.10.10.1'
        dmac1 = '01:00:5E:7F:01:01'
        smac1 = '00:00:00:00:00:01'
        type = SAI_L2MC_ENTRY_TYPE_SG
        grp_id = self.client.sai_thrift_create_l2mc_group(grp_attr_list)
        member_id1 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port2)
        member_id2 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port3)
        member_id3 = sai_thrift_create_l2mc_group_member(self.client, grp_id, port4)
        l2mc_entry = sai_thrift_fill_l2mc_entry(addr_family, vlan_oid, dip_addr1, default_addr, type)
        sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)
        
        self.client.sai_thrift_remove_l2mc_group_member(member_id2)
        sai_thrift_create_l2mc_entry(self.client, l2mc_entry, grp_id)

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
            
            ids_list = [SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY , SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY  :
                    sys_logging ("l2mc_entry_cnt: %d" %attribute.value.u32)
                    if 1 != attribute.value.u32:
                        raise NotImplementedError()
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY  :
                    sys_logging ("ipmc_entry_cnt: %d" %attribute.value.u32)
                    if 0 != attribute.value.u32:
                        raise NotImplementedError()
                                
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
            
            
            
            
class scenario_08_get_available_ipmc(sai_base_test.ThriftInterfaceDataPlane):

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
            
            ids_list = [SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY , SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_L2MC_ENTRY  :
                    sys_logging ("l2mc_entry_cnt: %d" %attribute.value.u32)
                    if 0 != attribute.value.u32:
                        raise NotImplementedError()
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_IPMC_ENTRY  :
                    sys_logging ("ipmc_entry_cnt: %d" %attribute.value.u32)
                    if 1 != attribute.value.u32:
                        raise NotImplementedError()
        finally:
        
            self.client.sai_thrift_remove_ipmc_entry(ipmc_entry)
            self.client.sai_thrift_remove_ipmc_group_member(member_id1)
            self.client.sai_thrift_remove_ipmc_group_member(member_id2)
            self.client.sai_thrift_remove_ipmc_group(grp_id)
            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            
            self.client.sai_thrift_remove_virtual_router(vr_id)




class scenario_09_get_available_snat(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
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
        srcip_addr = '10.10.10.1'
        proto = 6
        l4_srcport = 1000       
        ipmask = '255.255.255.255'
        protomask = 0xff
        l4portmask = 0xffff       
        keylist = [srcip_addr, '', proto, l4_srcport, 0]
        masklist = [ipmask, ipmask, protomask, l4portmask, l4portmask]       
        mod_srcip_addr = '100.100.100.1'      
        mod_l4_srcport = 1001      
        nat_type = SAI_NAT_TYPE_SOURCE_NAT
        status = sai_thrift_create_nat(self.client, vr_id, nat_type, keylist, masklist, mod_srcip_addr, None, mod_l4_srcport, None)
        sys_logging("creat status = %d" %status)

        warmboot(self.client)
        try:

            ids_list = [SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY , SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY  :
                    sys_logging ("snat_entry_cnt: %d" %attribute.value.u32)
                    if 1 != attribute.value.u32:
                        raise NotImplementedError()
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY  :
                    sys_logging ("dnat_entry_cnt: %d" %attribute.value.u32)
                    if 0 != attribute.value.u32:
                        raise NotImplementedError()
                        
        finally:
        
            sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)           
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)        
            self.client.sai_thrift_remove_virtual_router(vr_id)    




class scenario_10_get_available_dnat(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
    
        switch_init(self.client)
        
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
        dstip_addr = '20.20.20.1'
        proto = 6
        l4_dstport = 2000       
        ipmask = '255.255.255.255'
        protomask = 0xff
        l4portmask = 0xffff
        dmac1 = '00:11:22:33:44:55'
        ip_mask = '255.255.255.255'
        mod_dstip_addr = '200.200.200.1'  
        mod_l4_dstport = 2001       
        keylist = ['', dstip_addr, proto, 0, l4_dstport]
        masklist = [ipmask, ipmask, protomask, l4portmask, l4portmask]
       
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, mod_dstip_addr, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, mod_dstip_addr, rif_id1)
        
        sai_thrift_create_route(self.client, vr_id, addr_family, mod_dstip_addr, ip_mask, nhop1)
        
        nat_type = SAI_NAT_TYPE_DESTINATION_NAT
        
        status = sai_thrift_create_nat(self.client, vr_id, nat_type, keylist, masklist, None, mod_dstip_addr, None, mod_l4_dstport)
        sys_logging("creat status = %d" %status)

        warmboot(self.client)
        try:

            ids_list = [SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY , SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_SNAT_ENTRY  :
                    sys_logging ("snat_entry_cnt: %d" %attribute.value.u32)
                    if 0 != attribute.value.u32:
                        raise NotImplementedError()
                if attribute.id ==  SAI_SWITCH_ATTR_AVAILABLE_DNAT_ENTRY  :
                    sys_logging ("dnat_entry_cnt: %d" %attribute.value.u32)
                    if 1 != attribute.value.u32:
                        raise NotImplementedError()
                        
        finally:
        
            sai_thrift_remove_nat(self.client, vr_id, keylist, masklist)
            sai_thrift_remove_route(self.client, vr_id, addr_family, mod_dstip_addr, ip_mask, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, mod_dstip_addr, dmac1)          
            self.client.sai_thrift_remove_router_interface(rif_id1)  
            self.client.sai_thrift_remove_router_interface(rif_id2)            
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            

class scenario_11_set_route_mac(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        
        port1 = port_list[1]
        port2 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        router_mac='00:77:66:55:44:00'
        
        default_vrf = 3
                   
        rif_id1 = sai_thrift_create_router_interface(self.client, default_vrf, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, None)
        rif_id2 = sai_thrift_create_router_interface(self.client, default_vrf, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, None)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, default_vrf, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)                             
                                
        warmboot(self.client)
        try:
        
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packet( exp_pkt, 1)

            ids_list = [SAI_SWITCH_ATTR_SRC_MAC_ADDRESS]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:              
                if attribute.id == SAI_SWITCH_ATTR_SRC_MAC_ADDRESS:
                    sys_logging("### SAI_SWITCH_ATTR_SRC_MAC_ADDRESS = %s ###"  %attribute.value.mac)
                    assert ( router_mac == attribute.value.mac )
                   
            
        finally:
          
            sai_thrift_remove_route(self.client, default_vrf, addr_family, ip_addr1_subnet, ip_mask1, rif_id1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)            
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)


            
class scenario_12_set_max_learning_address(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
                 
        pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        sys_logging ("step1: no fdb entry")
        
        result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
        if(1 == result):
            sys_logging ("fdb entry exist")
        else:
            sys_logging ("fdb entry not exist")
        assert(0 == result)
        
        result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
        if(1 == result):
            sys_logging ("fdb entry exist")
        else:
            sys_logging ("fdb entry not exist")
        assert(0 == result)
        
        warmboot(self.client)
        try:
        
            sys_logging ("step2: mac learnning address num is 1, so only can learning one fdb entry")
            limit_num = 1
            
            attr_value = sai_thrift_attribute_value_t(u32=limit_num)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
            time.sleep(3)
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets( str(pkt2), [0], 1)            
            
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(1 == result)            
                
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(0 == result)            
            
            sys_logging ("step3: flush all fdb entry")
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)
            time.sleep(3)
            sys_logging ("step4: mac learnning address num is 0 means disable ")
            limit_num = 0
            attr_value = sai_thrift_attribute_value_t(u32=limit_num)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)             

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
            time.sleep(3)
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets( str(pkt2), [0], 1)            
            
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(1 == result)            
                
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2)
            if(1 == result):
                sys_logging ("fdb entry exist")
            else:
                sys_logging ("fdb entry not exist")
            assert(1 == result)              
            
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)






class scenario_13_fdb_unicast_miss_packet_action(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:22:22:22:22:33'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
        
        self.client.sai_thrift_clear_cpu_packet_info()

        pkt1 = simple_tcp_packet(eth_dst=mac2,
            eth_src=mac1,
            ip_dst='10.0.0.1',
            ip_src='192.168.0.1',
            ip_id=102,
            ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac2,
            eth_src=mac1,
            ip_dst='10.0.0.1',
            ip_src='192.168.0.1',
            dl_vlan_enable=True,
            vlan_vid=10,
            ip_id=102,
            ip_ttl=64,
            pktlen=104)
            
        pkt2 = simple_tcp_packet(eth_dst=mac3,
            eth_src=mac1,
            ip_dst='10.0.0.1',
            ip_src='192.168.0.1',
            ip_id=102,
            ip_ttl=64)
        exp_pkt2 = simple_tcp_packet(eth_dst=mac3,
            eth_src=mac1,
            ip_dst='10.0.0.1',
            ip_src='192.168.0.1',
            dl_vlan_enable=True,
            vlan_vid=10,
            ip_id=102,
            ip_ttl=64,
            pktlen=104)
                
        warmboot(self.client)
        try:
            # step 1
            sys_logging ('#### Sending 00:22:22:22:22:22 | 00:11:11:11:11:11 | 10.0.0.1 | 192.168.0.1 | @ ptf_intf 1 ####')
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packets( exp_pkt1, [2])   
            
            time.sleep(1)            
            # step 2
            sys_logging ('#### Sending 00:22:22:22:22:22 | 00:11:11:11:11:11 | 10.0.0.1 | 192.168.0.1 | @ ptf_intf 1 ####')
            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, exp_pkt2], [2, 3])  

            time.sleep(1)
            # step 3
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRAP) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  

            sys_logging ('#### Sending 00:22:22:22:22:22 | 00:11:11:11:11:11 | 10.0.0.1 | 192.168.0.1 | @ ptf_intf 1 ####')
            self.ctc_send_packet( 1, str(pkt2))
            self.ctc_verify_no_packet( exp_pkt2, 2)   
            self.ctc_verify_no_packet( exp_pkt2, 3)
            
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet: %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError()
                
            attrs = self.client.sai_thrift_get_cpu_packet_attribute(0)
            sys_logging ("success to get packet attribute")
            for a in attrs.attr_list:
                if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                    sys_logging ("ingress port: 0x%lx" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError()
            
        finally:
        
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2) 
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)   
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)  
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_UNICAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 

            
            
class scenario_14_fdb_multicast_miss_packet_action(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:22:22:22:22:33'
        mcast_mac = '01:00:5e:7f:01:01'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        self.client.sai_thrift_clear_cpu_packet_info()

        pkt1 = simple_tcp_packet(eth_dst=mcast_mac,
            eth_src=mac1,
            ip_dst='10.0.0.1',
            ip_src='192.168.0.1',
            ip_id=102,
            ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst=mcast_mac,
            eth_src=mac1,
            ip_dst='10.0.0.1',
            ip_src='192.168.0.1',
            dl_vlan_enable=True,
            vlan_vid=10,
            ip_id=102,
            ip_ttl=64,
            pktlen=104)

                
        warmboot(self.client)
        try:
            # step 1
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1], [2, 3])  
            time.sleep(1)
            # step 2
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRAP) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  

            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_no_packet( exp_pkt1, 2)   
            self.ctc_verify_no_packet( exp_pkt1, 3)
            
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet: %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError()
                
            attrs = self.client.sai_thrift_get_cpu_packet_attribute(0)
            sys_logging ("success to get packet attribute")
            for a in attrs.attr_list:
                if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                    sys_logging ("ingress port: 0x%lx" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError()
            
        finally:
        
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)   
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)  
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_MULTICAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 




           
class scenario_15_fdb_broadcast_miss_packet_action(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:22:22:22:22:33'
        mcast_mac = '01:00:5e:7f:01:01'
        broadcast_mac = 'ff:ff:ff:ff:ff:ff'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        
        self.client.sai_thrift_clear_cpu_packet_info()

        pkt1 = simple_tcp_packet(eth_dst=broadcast_mac,
            eth_src=mac1,
            ip_dst='10.0.0.1',
            ip_src='192.168.0.1',
            ip_id=102,
            ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(eth_dst=broadcast_mac,
            eth_src=mac1,
            ip_dst='10.0.0.1',
            ip_src='192.168.0.1',
            dl_vlan_enable=True,
            vlan_vid=10,
            ip_id=102,
            ip_ttl=64,
            pktlen=104)

                
        warmboot(self.client)
        try:
            # step 1
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1], [2, 3])  
            time.sleep(1)
            # step 2
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_TRAP) 
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  

            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_no_packet( exp_pkt1, 2)   
            self.ctc_verify_no_packet( exp_pkt1, 3)
            
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet: %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError()
                
            attrs = self.client.sai_thrift_get_cpu_packet_attribute(0)
            sys_logging ("success to get packet attribute")
            for a in attrs.attr_list:
                if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                    sys_logging ("ingress port: 0x%lx" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError()
            
        finally:
        
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)   
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_FORWARD)  
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_FDB_BROADCAST_MISS_PACKET_ACTION , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 



















            