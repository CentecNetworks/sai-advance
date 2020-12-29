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
import pdb
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask


@group('mirror')
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

class fun_01_create_local_mirror_session(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        
        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        monitor_port_list = [port1, port2, port3]
        port_list_valid = False
        port_list_valid1 = True 
        sys_logging("======Create 2 mirror session: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
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
        ingress_localmirror_id1 = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid1,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        
        warmboot(self.client)
        try:
            sys_logging("ingress_localmirror_id = 0x%x" %ingress_localmirror_id)
            sys_logging("ingress_localmirror_id = 0x%x" %ingress_localmirror_id1)
            assert (ingress_localmirror_id%0x100000000 == 0xe)
            assert (ingress_localmirror_id1%0x100000000 == 0xe)
            
            sys_logging( "======Get 2 mirror session attribute======")            
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_localmirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_localmirror_id1)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id1)

class fun_02_create_rspan_mirror_session(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10
        
        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_REMOTE
        monitor_port = port3
        monitor_port_list = []
        port_list_valid = False 
        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_SESSION_TYPE_REMOTE======")
        ingress_remotemirror_id = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            vlan_id, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        
        warmboot(self.client)
        try:
            sys_logging("ingress_localmirror_id = 0x%x" %ingress_remotemirror_id)
            assert (ingress_remotemirror_id%0x100000000 == 0x200e)
            
            sys_logging( "======Get the mirror session attribute======")            
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_remotemirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_mirror_session(ingress_remotemirror_id)

class fun_03_create_erspan_mirror_session(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
     
        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10

        mirror_type = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE
        monitor_port = port3
        monitor_port_list = []
        port_list_valid = False 
        
        src_mac='00:00:00:00:11:22'
        dst_mac='00:00:00:00:11:33'
        src_ip='17.18.19.0'
        dst_ip='33.19.20.0'
        encap_type=SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL
        ip_version=0x4
        ttl=0x20
        tos=0x3c
        gre_type=0x22eb

        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE======")
        ingress_enhanced_remotemirror_id = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            None, None, None, None, 
            src_mac=src_mac,dst_mac=dst_mac,src_ip=src_ip,
            dst_ip=dst_ip,encap_type=encap_type,iphdr_version=ip_version,
            ttl=ttl,tos=tos,gre_type=gre_type)     
        
        
        warmboot(self.client)
        try:
            sys_logging("ingress_localmirror_id = 0x%x" %ingress_enhanced_remotemirror_id)
            assert (ingress_enhanced_remotemirror_id%0x100000000 == 0x400e)
            
            sys_logging( "======Get the mirror session attribute======")            
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_enhanced_remotemirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_mirror_session(ingress_enhanced_remotemirror_id)

class fun_04_remove_mirror_session(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_id = 10
        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        monitor_port_list = [port1, port2, port3]
        port_list_valid = False
        port_list_valid1 = True 

        
        src_mac='00:00:00:00:11:22'
        dst_mac='00:00:00:00:11:33'
        src_ip='17.18.19.0'
        dst_ip='33.19.20.0'
        encap_type=SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL
        ip_version=0x4
        ttl=0x20
        tos=0x3c
        gre_type=0x22eb
        
        sys_logging("======Create 4 mirror session======")
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
        ingress_localmirror_id1 = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid1,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
            
        mirror_type = SAI_MIRROR_SESSION_TYPE_REMOTE
        ingress_remotemirror_id = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            vlan_id, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        mirror_type = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE
        ingress_enhanced_remotemirror_id = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            None, None, None, None, 
            src_mac=src_mac,dst_mac=dst_mac,src_ip=src_ip,
            dst_ip=dst_ip,encap_type=encap_type,iphdr_version=ip_version,
            ttl=ttl,tos=tos,gre_type=gre_type)
       
        warmboot(self.client)
        try:
            sys_logging( "======remove 4 mirror session attribute======") 
            status = self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id1)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_mirror_session(ingress_remotemirror_id)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_mirror_session(ingress_enhanced_remotemirror_id)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            sys_logging( "======Get 4 mirror session attribute======")            
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_localmirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_localmirror_id1)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_remotemirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_enhanced_remotemirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")

class fun_05_remove_no_exist_mirror_session(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        
        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        monitor_port_list = [port1, port2, port3]
        port_list_valid = False
        port_list_valid1 = True 
        sys_logging("======Create 2 mirror session======")
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
        ingress_localmirror_id1 = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid1,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        ingress_localmirror_id2 = ingress_localmirror_id1+0x100000000
        warmboot(self.client)
        try:
            sys_logging("ingress_localmirror_id = 0x%x" %ingress_localmirror_id)
            sys_logging("ingress_localmirror_id = 0x%x" %ingress_localmirror_id1)
            sys_logging("ingress_localmirror_id = 0x%x" %ingress_localmirror_id2)

            sys_logging( "======remove no exist mirror session attribute======") 
            status = self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id2)
            sys_logging( "status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            sys_logging( "======Get 2 mirror session attribute======")            
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_localmirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_localmirror_id1)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id1)

class fun_06_set_local_mirror_session_attribute(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
     
        print ""
        switch_init(self.client)
        port3 = port_list[3]
        port2 = port_list[2]
        
        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        port_list_valid = 0
        monitor_port_list = []
        truncate_size = 100 
        sample_rate = 7 
        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
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
        sys_logging("ingress_localmirror_id = 0x%lx" %ingress_localmirror_id)
        
        warmboot(self.client)
        try:
            sys_logging("======get the mirror session attribute: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_localmirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MIRROR_SESSION_ATTR_TYPE:
                    sys_logging("create mirror_type = %d" %mirror_type)
                    sys_logging("get mirror_type = %d" %a.value.s32)
                    if mirror_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID:
                    sys_logging("create mirror port_list_valid = %d" %port_list_valid)
                    sys_logging("get mirror port_list_valid = %d" %a.value.booldata)
                    if port_list_valid!= a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_MONITOR_PORT: 
                    sys_logging("create monitor_port = 0x%lx" %monitor_port)
                    sys_logging("get monitor_port = 0x%lx" %a.value.oid)
                    if monitor_port != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE: 
                    sys_logging("set sample_rate = %d" %sample_rate)
                    sys_logging("get sample_rate = %d" %a.value.u32)
            sys_logging("======set the mirror session attribute: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
            sys_logging("Set mirror session: monitor_port = 2")
            attr_value = sai_thrift_attribute_value_t(oid=port2)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_MONITOR_PORT, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_localmirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("Set mirror session: truncate_size = 100")
            attr_value = sai_thrift_attribute_value_t(u16=truncate_size)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_localmirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("Set mirror session: sample_rate = 1/8")
            attr_value = sai_thrift_attribute_value_t(u32=sample_rate)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_localmirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("======get the mirror session attribute again======")
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_localmirror_id)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MIRROR_SESSION_ATTR_TYPE:
                    sys_logging("set mirror_type = %d" %mirror_type)
                    sys_logging("get mirror_type = %d" %a.value.s32)
                    if mirror_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_MONITOR_PORT: 
                    sys_logging("set monitor_port = 0x%x" %port2)
                    sys_logging("get monitor_port = 0x%x" %a.value.oid)
                    if port2 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE: 
                    sys_logging("set truncate_size = %d" %truncate_size)
                    sys_logging("get truncate_size = %d" %a.value.u16)
                    if truncate_size != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE: 
                    sys_logging("set sample_rate = %d" %sample_rate)
                    sys_logging("get sample_rate = %d" %a.value.u32)
                    if sample_rate != a.value.u32:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)

class fun_07_set_portlist_mirror_session_attribute(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        port5 = port_list[5]
        
        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        port_list_valid = 1
        monitor_port_list = [port1,port2,port3]
        monitor_port_list1 = [port2,port3,port4,port5]
        truncate_size = 100 
        sample_rate = 7 
        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
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
        sys_logging("ingress_localmirror_id = 0x%lx" %ingress_localmirror_id)
        
        warmboot(self.client)
        try:

            sys_logging("======get the mirror session attribute: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_localmirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MIRROR_SESSION_ATTR_TYPE:
                    sys_logging("create mirror_type = %d" %mirror_type)
                    sys_logging("get mirror_type = %d" %a.value.s32)
                    if mirror_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE: 
                    sys_logging("create truncate_size = %d" %truncate_size)
                    sys_logging("get truncate_size = %d" %a.value.u16)
                    if 0 != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE: 
                    sys_logging("create truncate_size = %d" %truncate_size)
                    sys_logging("get truncate_size = %d" %a.value.u16)
                    if 1 != a.value.u32:
                        raise NotImplementedError()
                    
                if a.id == SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST_VALID:
                    sys_logging("create mirror port_list_valid = %d" %port_list_valid)
                    sys_logging("get mirror port_list_valid = %d" %a.value.booldata)
                    if port_list_valid!= a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST:
                    assert (a.value.objlist.object_id_list != [])
                    n=0
                    for i in a.value.objlist.object_id_list:
                        sys_logging("get the %dth mirror port oid" %(n+1))
                        sys_logging("the mirror port oid = 0x%x" %i)
                        assert (monitor_port_list[n] == i)
                        n = n+1
                

            
            sys_logging("======set the mirror session attribute: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
            sys_logging("Set mirror session: port_list = monitor_port_list1")
            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=len(monitor_port_list1),object_id_list=monitor_port_list1))
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_localmirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            print "Set mirror session: truncate_size = 100"
            attr_value = sai_thrift_attribute_value_t(u16=truncate_size)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_localmirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            print "Set mirror session: sample_rate = 1/8"
            attr_value = sai_thrift_attribute_value_t(u32=sample_rate)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_localmirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            sys_logging("======get the mirror session attribute again======")
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_localmirror_id)
            sys_logging( "status = %d" %attrs.status)
            
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MIRROR_SESSION_ATTR_TYPE:
                    sys_logging("set mirror_type = %d" %mirror_type)
                    sys_logging("get mirror_type = %d" %a.value.s32)
                    if mirror_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE: 
                    sys_logging("set truncate_size = %d" %truncate_size)
                    sys_logging("get truncate_size = %d" %a.value.u16)
                    if truncate_size != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_SAMPLE_RATE: 
                    sys_logging("settruncate_size = %d" %truncate_size)
                    sys_logging("get truncate_size = %d" %a.value.u16)
                    if sample_rate != a.value.u32:
                        raise NotImplementedError()                    
                if a.id == SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST:
                    assert (a.value.objlist.object_id_list != [])
                    n=0
                    for i in a.value.objlist.object_id_list:
                        sys_logging("get the %dth mirror port oid" %(n+1))
                        sys_logging("the mirror port oid = 0x%x" %i)
   
                        assert (monitor_port_list1[n] == i)
                        n = n+1
                
                     
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)

class fun_08_set_rspan_mirror_session_attribute(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port3 = port_list[3]
        port2 = port_list[2]
        
        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_REMOTE
        monitor_port = port3
        port_list_valid = 0
        monitor_port_list = []
        truncate_size = 100 
        vlan_id_create = 10
        vlan_id_set = 20
        
        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_SESSION_TYPE_REMOTE======")
        ingress_remotemirror_id = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            vlan_id_create, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        sys_logging("ingress_localmirror_id = 0x%lx" %ingress_remotemirror_id)
        
        warmboot(self.client)
        try:
            sys_logging("======get the mirror session attribute: mirror_type = SAI_MIRROR_SESSION_TYPE_REMOTE======")
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_remotemirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MIRROR_SESSION_ATTR_TYPE:
                    sys_logging("set mirror_type = %d" %mirror_type)
                    sys_logging("get mirror_type = %d" %a.value.s32)
                    if mirror_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_MONITOR_PORT: 
                    sys_logging("create monitor_port = 0x%x" %monitor_port)
                    sys_logging("get monitor_port = 0x%x" %a.value.oid)
                    if monitor_port != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_VLAN_ID: 
                    sys_logging("create vlan_id_create = %d" %vlan_id_create)
                    sys_logging("get vlan_id_create = %d" %a.value.u16)
                    if vlan_id_create != a.value.u16:
                        raise NotImplementedError()

            sys_logging("======set the mirror session attribute: mirror_type = SAI_MIRROR_SESSION_TYPE_REMOTE======")
            sys_logging("Set mirror session: monitor_port = 2")
            attr_value = sai_thrift_attribute_value_t(oid=port2)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_MONITOR_PORT, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("Set mirror session: truncate_size = 100")
            attr_value = sai_thrift_attribute_value_t(u16=truncate_size)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("Set mirror session: vlan_id = 20")
            attr_value = sai_thrift_attribute_value_t(u16=vlan_id_set)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_VLAN_ID, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            sys_logging("======get the mirror session attribute again======")
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_remotemirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MIRROR_SESSION_ATTR_TYPE:
                    sys_logging("set mirror_type = %d" %mirror_type)
                    sys_logging("get mirror_type = %d" %a.value.s32)
                    if mirror_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_MONITOR_PORT: 
                    sys_logging("set monitor_port = 0x%lx" %port2)
                    sys_logging("get monitor_port = 0x%lx" %a.value.oid)
                    if port2 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE: 
                    sys_logging("set truncate_size = %d" %truncate_size)
                    sys_logging("get truncate_size = %d" %a.value.u16)
                    if truncate_size != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_VLAN_ID: 
                    sys_logging("set vlan_id_set = %d" %vlan_id_set)
                    sys_logging("get vlan_id_set = %d" %a.value.u16)
                    if vlan_id_set != a.value.u16:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_mirror_session(ingress_remotemirror_id)

class fun_09_set_erspan_mirror_session_attribute(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        src_mac_set='00:00:00:00:00:33'
        dst_mac_set='00:00:00:00:00:22'
        monitor_port=port1
        port_list_valid = 0
        monitor_port_list = []
        source_port=port2
        truncate_size = 100 
        mirror_type=SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE
        src_mac='00:00:00:00:11:22'
        dst_mac='00:00:00:00:11:33'
        encap_type=SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL
        ip_version=0x4
        ip_version_set=0x4
        tos=0x3c
        ttl=0x20
        tos_set=0x3d
        ttl_set=0x2d
        #gre_type=0x88be  buff = pack("!h", i16) error: 'h' format requires -32768 <= number <= 32767
        gre_type=0x22eb
        gre_type_set=0x2222
        src_ip='17.18.19.0'
        dst_ip='33.19.20.0'
        src_ip_set='11.12.13.14'
        dst_ip_set='21.22.23.24'
        addr_family=0
        vlan_id_create = 10
        vlan_id_set = 20
        
        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE======")
        ingress_enhanced_remotemirror_id = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            vlan_id_create, None, None, None, 
            src_mac=src_mac,dst_mac=dst_mac,src_ip=src_ip,dst_ip=dst_ip,encap_type=encap_type,iphdr_version=ip_version,ttl=ttl,tos=tos,gre_type=gre_type)
        sys_logging("ingress_localmirror_id = 0x%lx" %ingress_enhanced_remotemirror_id)  
        
        warmboot(self.client)
        try:
            sys_logging("======get the mirror session attribute: mirror_type = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE======")
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_enhanced_remotemirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MIRROR_SESSION_ATTR_TYPE:
                    sys_logging("set mirror_type = %d" %mirror_type)
                    sys_logging("get mirror_type = %d" %a.value.s32)
                    if mirror_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_MONITOR_PORT: 
                    sys_logging("create monitor_port = 0x%x" %monitor_port)
                    sys_logging("get monitor_port = 0x%x" %a.value.oid)
                    if monitor_port != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_VLAN_ID: 
                    sys_logging("create vlan_id_create = %d" %vlan_id_create)
                    sys_logging("get vlan_id_create = %d" %a.value.u16)
                    if vlan_id_create != a.value.u16:
                        raise NotImplementedError()

            sys_logging("======set the mirror session attribute: mirror_type = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE======")
            sys_logging("Set mirror session: monitor_port = 2")
            attr_value = sai_thrift_attribute_value_t(oid=port2)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_MONITOR_PORT, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_enhanced_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("Set mirror session: truncate_size = %d" %truncate_size)
            attr_value = sai_thrift_attribute_value_t(u16=truncate_size)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_enhanced_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            sys_logging("Set mirror session: vlan_id = %d" %vlan_id_set)
            attr_value = sai_thrift_attribute_value_t(u16=vlan_id_set)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_VLAN_ID, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_enhanced_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            sys_logging("Set mirror session: src_mac_set = %s" %src_mac_set)
            attr_value = sai_thrift_attribute_value_t(mac=src_mac_set)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_enhanced_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("Set mirror session: dst_mac_set = %s" %dst_mac_set)
            attr_value = sai_thrift_attribute_value_t(mac=dst_mac_set)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_enhanced_remotemirror_id, attr)
            #source ip
            sys_logging("Set mirror session: src_ip_set = %s" %src_ip_set)
            addr = sai_thrift_ip_t(ip4=src_ip_set)
            src_ip_addr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            attribute5_value = sai_thrift_attribute_value_t(ipaddr=src_ip_addr)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS,
                                            value=attribute5_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_enhanced_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            #dst ip
            sys_logging("Set mirror session: dst_ip_set = %s" %dst_ip_set)
            addr = sai_thrift_ip_t(ip4=dst_ip_set)
            dst_ip_addr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
            attribute6_value = sai_thrift_attribute_value_t(ipaddr=dst_ip_addr)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS,
                                            value=attribute6_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_enhanced_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("Set mirror session: ip_version_set = %s" %ip_version_set)
            attr_value = sai_thrift_attribute_value_t(u8=ip_version_set)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_enhanced_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("Set mirror session: tos_set = %s" %tos_set)
            attr_value = sai_thrift_attribute_value_t(u8=tos_set)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_TOS, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_enhanced_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("Set mirror session: ttl_set = %s" %ttl_set)
            attr_value = sai_thrift_attribute_value_t(u8=ttl_set)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_TTL, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_enhanced_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            sys_logging("Set mirror session: gre_type_set = %s" %gre_type_set)
            attr_value = sai_thrift_attribute_value_t(u16=gre_type_set)
            attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE, value=attr_value)
            status=self.client.sai_thrift_set_mirror_attribute(ingress_enhanced_remotemirror_id, attr)
            sys_logging("status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)
            
            sys_logging("======get the mirror session attribute again======")
            attrs = self.client.sai_thrift_get_mirror_attribute(ingress_enhanced_remotemirror_id)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_MIRROR_SESSION_ATTR_TYPE:
                    sys_logging("set mirror_type = %d" %mirror_type)
                    sys_logging("get mirror_type = %d" %a.value.s32)
                    if mirror_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_MONITOR_PORT: 
                    sys_logging("set monitor_port = 0x%lx" %port2)
                    sys_logging("get monitor_port = 0x%lx" %a.value.oid)
                    if port2 != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_TRUNCATE_SIZE: 
                    sys_logging("set truncate_size = %d" %truncate_size)
                    sys_logging("get truncate_size = %d" %a.value.u16)
                    if truncate_size != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_VLAN_ID: 
                    sys_logging("set vlan_id_set = %d" %vlan_id_set)
                    sys_logging("get vlan_id_set = %d" %a.value.u16)
                    if vlan_id_set != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS: 
                    sys_logging("set src_mac_set = %s" %src_mac_set)
                    sys_logging("get src_mac_set = %s" %a.value.mac)
                    if src_mac_set != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS: 
                    sys_logging("set dst_mac_set = %s" %dst_mac_set)
                    sys_logging("get dst_mac_set = %s" %a.value.mac)
                    if dst_mac_set != a.value.mac:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS: 
                    sys_logging("set src_ip_set = %s" %src_ip_set)
                    sys_logging("get src_ip_set = %s" %a.value.ipaddr.addr.ip4)
                    if src_ip_set != a.value.ipaddr.addr.ip4:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS: 
                    sys_logging("set dst_ip_set = %s" %dst_ip_set)
                    sys_logging("get dst_ip_set = %s" %a.value.ipaddr.addr.ip4)
                    if dst_ip_set != a.value.ipaddr.addr.ip4:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_IPHDR_VERSION: 
                    sys_logging("set ip_version_set = %d" %ip_version_set)
                    sys_logging("get ip_version_set = %d" %a.value.u8)
                    if ip_version_set != a.value.u8:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_TOS: 
                    sys_logging("set tos_set = %d" %tos_set)
                    sys_logging("get tos_set = %d" %a.value.u8)
                    if tos_set != a.value.u8:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_TTL: 
                    sys_logging("set ttl_set = %d" %ttl_set)
                    sys_logging("get ttl_set = %d" %a.value.u8)
                    if ttl_set != a.value.u8:
                        raise NotImplementedError()
                if a.id == SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE: 
                    sys_logging("set gre_type_set = %d" %gre_type_set)
                    sys_logging("get gre_type_set = %d" %a.value.u16)
                    if gre_type_set != a.value.u16:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_mirror_session(ingress_enhanced_remotemirror_id)

class fun_10_create_max_mirror_session(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        switch_init(self.client)

        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]

        mirror_type1 = SAI_MIRROR_SESSION_TYPE_LOCAL
        mirror_type2 = SAI_MIRROR_SESSION_TYPE_REMOTE
        mirror_type3 = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE

        port_list_valid = 0
        port_list_valid1 = 1
        monitor_port1=port1
        monitor_port2=port2
        monitor_port3=port3
        monitor_port_list = [port0, port1]

        src_mac='00:00:00:00:11:22'
        dst_mac='00:00:00:00:11:33'
        encap_type=SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL
        ip_version=0x4
        tos=0x3c
        ttl=0x22
        gre_type=0x22eb
        src_ip='17.18.19.0'
        dst_ip='33.19.20.0'
        vlan_id_remote = 20

        sys_logging("======Create 4 mirror session======")
        localmirror1 = sai_thrift_create_mirror_session(self.client,
            mirror_type1,
            monitor_port1,
            monitor_port_list,
            port_list_valid,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        localmirror2 = sai_thrift_create_mirror_session(self.client,
            mirror_type1,
            monitor_port1,
            monitor_port_list,
            port_list_valid1,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        remotemirror = sai_thrift_create_mirror_session(self.client,
            mirror_type2,
            monitor_port2,
            monitor_port_list,
            port_list_valid,
            vlan_id_remote, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)    
        erspanid = sai_thrift_create_mirror_session(self.client,
            mirror_type3,
            monitor_port3,
            monitor_port_list,
            port_list_valid,
            None, None, None, None, 
            src_mac=src_mac,dst_mac=dst_mac,src_ip=src_ip,dst_ip=dst_ip,encap_type=encap_type,iphdr_version=ip_version,ttl=ttl,tos=tos,gre_type=gre_type)

        attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[localmirror1]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
        status = self.client.sai_thrift_set_port_attribute(port0, attr)
        sys_logging( "status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[localmirror2]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
        status = self.client.sai_thrift_set_port_attribute(port1, attr)
        sys_logging( "status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[remotemirror]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
        status = self.client.sai_thrift_set_port_attribute(port2, attr)
        sys_logging( "status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[erspanid]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
        status = self.client.sai_thrift_set_port_attribute(port3, attr)
        sys_logging( "status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        warmboot(self.client)
        try:
            attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=2,object_id_list=[localmirror1,localmirror2]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
            status = self.client.sai_thrift_set_port_attribute(port4, attr)
            sys_logging( "status = %d" %status)
            assert (status == SAI_STATUS_INSUFFICIENT_RESOURCES)
        finally:
            sys_logging("======clean up======")
            attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
            self.client.sai_thrift_set_port_attribute(port0, attr)

            self.client.sai_thrift_remove_mirror_session(localmirror1)
            self.client.sai_thrift_remove_mirror_session(localmirror2)
            self.client.sai_thrift_remove_mirror_session(remotemirror)
            self.client.sai_thrift_remove_mirror_session(erspanid)

class scenario_01_ingress_local_mirror_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''
        switch_init(self.client)
        vlan_id = 10
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
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

        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        monitor_port_list = []
        port_list_valid = False
        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
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
        sys_logging("======bind the mirror session to port1 and port2 ingress======")
        attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[ingress_localmirror_id]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        warmboot(self.client)
        
        try:

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

            sys_logging("======send packet from port1 to port2,mirror to port3======")
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, pkt1], [2, 3])

            pkt2 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                vlan_vid=10,
                dl_vlan_enable=True,
                ip_id=102,
                ip_ttl=64,
                pktlen=104)
            exp_pkt2 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                ip_id=102,
                ip_ttl=64,
                pktlen=100)

            sys_logging("======send packet from port2 to port1,mirror to port3======")
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, pkt2], [1, 3])
            
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)
            #attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_MIRROR_SESSION, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_02_egress_local_mirror_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        vlan_id = 10
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
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

        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        monitor_port_list = []
        port_list_valid = False
        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
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

        sys_logging("======bind the mirror session to port1 and port2 egress======")
        attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[ingress_localmirror_id]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_MIRROR_SESSION, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        warmboot(self.client)
        
        try:

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

            sys_logging("======send packet from port1 to port2,mirror to port3======")
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, exp_pkt1], [2, 3])


            pkt2 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                vlan_vid=10,
                dl_vlan_enable=True,
                ip_id=102,
                ip_ttl=64,
                pktlen=104)
            exp_pkt2 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                ip_id=102,
                ip_ttl=64,
                pktlen=100)

            sys_logging("======send packet from port2 to port1,mirror to port3======")
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, exp_pkt2], [1, 3])
            
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_MIRROR_SESSION, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_03_flow_mirror_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_id = 20
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sai_thrift_create_fdb(self.client, vlan_oid, mac_dst, port2, mac_action)
        
        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        monitor_port_list = []
        port_list_valid = False
        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
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

        pkt = simple_qinq_tcp_packet(pktlen=100,
            eth_dst=mac_dst,
            eth_src=mac_src,
            dl_vlan_outer=20,
            dl_vlan_pcp_outer=4,
            dl_vlan_cfi_outer=1,
            vlan_vid=10,
            vlan_pcp=2,
            dl_vlan_cfi=1,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=64,
            tcp_sport=1234,
            tcp_dport=80)

        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_FORWARD
        in_ports = [port1, port2]
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=None
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=None
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.255"
        ip_dst = '10.10.10.1'
        ip_dst_mask = "255.255.255.255"
        is_ipv6 = False
        ip_tos=None 
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        ip_type = SAI_ACL_IP_TYPE_IPV4ANY
        ip_protocol = 6
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id_list=[ingress_localmirror_id]
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        addr_family = None

        acl_table_id = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            in_ports,
            out_ports,
            in_port,
            out_port,
            svlan_id, 
            svlan_pri,
            svlan_cfi, 
            cvlan_id,
            cvlan_pri, 
            cvlan_cfi,
            ip_type,
            None,None,None,None,None,None,None,None,None,None,
            None,None,None,None,None,None,None,None,None,None,
            ip_protocol,
            src_l4_port,
            dst_l4_port)

        sys_logging("======bind the mirror session to acl entry======")
        acl_entry_id = sai_thrift_create_acl_entry(self.client,
            acl_table_id,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_type,
            None,None,None,None,None,None,None,None,None,None,
            None,None,None,None,None,None,None,None,None,None,
            ip_src, ip_src_mask,
            ip_dst, ip_dst_mask,
            ip_protocol,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id_list,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn)

        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
        self.client.sai_thrift_clear_cpu_packet_info()
        #pdb.set_trace()
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(enable = True, parameter = sai_thrift_acl_parameter_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[ingress_localmirror_id]))))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS, value=attribute_value)
        self.client.sai_thrift_set_acl_entry_attribute(acl_entry_id, attribute)

        warmboot(self.client)

        try:

            sys_logging("======send packet from port1 to port2,mirror to port3======")

            self.ctc_send_packet( 0, str(pkt))

            self.ctc_verify_each_packet_on_each_port( [pkt, pkt], [1, 2])

        finally:
            sys_logging("======clean up======")

            attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(enable = True, parameter = sai_thrift_acl_parameter_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))))
            attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_MIRROR_INGRESS, value=attribute_value)
            self.client.sai_thrift_set_acl_entry_attribute(acl_entry_id, attribute)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # remove ingress_localmirror_id
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac_dst, port2)

            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_04_portlist_local_mirror_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print''
        
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        port5 = port_list[5]
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

        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        monitor_port_list = [port3, port4, port5]
        port_list_valid = True

        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
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

        sys_logging("======bind the mirror session to port1 and port2 ingress======")
        attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[ingress_localmirror_id]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)

        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        warmboot(self.client)
        
        try:

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

            sys_logging("======send packet from port1 to port2,mirror to port3,port4,port5======")
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, pkt1, pkt1, pkt1], [2, 3, 4, 5])


            pkt2 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                vlan_vid=10,
                dl_vlan_enable=True,
                ip_id=102,
                ip_ttl=64,
                pktlen=104)
            exp_pkt2 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                ip_id=102,
                ip_ttl=64,
                pktlen=100)
            sys_logging("======send packet from port2 to port1,mirror to port3,port4,port5======")
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, pkt2, pkt2, pkt2], [1, 3, 4, 5])
            
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_05_rspan_mirror_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 1 -> ptf_intf 2, ptf_intf 3 (local mirror)"
        print "Sending packet ptf_intf 2 -> ptf_intf 1, ptf_intf 3 (local mirror)"

        switch_init(self.client)
        vlan_id = 10
        vlan_id1 = 20
        vlan_pri = 5
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
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

        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_REMOTE
        monitor_port = port3
        monitor_port_list = []
        port_list_valid = False 
        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_SESSION_TYPE_REMOTE======")
        ingress_remotemirror_id = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            vlan_id1, vlan_pri, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)

        sys_logging("======bind the mirror session to port1 and port2 ingress======")
        attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[ingress_remotemirror_id]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        warmboot(self.client)
        
        try:
            

            pkt1 = simple_tcp_packet(eth_dst=mac2,
                eth_src=mac1,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                ip_id=102,
                ip_ttl=64)
            exp_pkt11 = simple_tcp_packet(pktlen=104,
                eth_dst=mac2,
                eth_src=mac1,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                vlan_vid=10,
                dl_vlan_enable=True,
                ip_id=102,
                ip_ttl=64)
            exp_pkt12 = simple_tcp_packet(pktlen=104,
                eth_dst=mac2,
                eth_src=mac1,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                vlan_vid=20,
                vlan_pcp=5,
                dl_vlan_enable=True,
                ip_id=102,
                ip_ttl=64)


            sys_logging("======send packet from port1 to port2,mirror to port3======")
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt11, exp_pkt12], [2, 3])


            pkt2 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                vlan_vid=10,
                dl_vlan_enable=True,
                ip_id=1,
                ip_ttl=64,
                pktlen=104)
            exp_pkt21 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                ip_id=1,
                ip_ttl=64)
            exp_pkt22 = simple_qinq_tcp_packet(pktlen=108,
                eth_dst=mac1,
                eth_src=mac2,
                dl_vlan_outer=20,
                dl_vlan_pcp_outer=5,
                vlan_vid=10,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1', 
                ip_ttl=64)

            sys_logging("======send packet from port2 to port1,mirror to port3======")
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt21, exp_pkt22], [1, 3])       
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_mirror_session(ingress_remotemirror_id)
            
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_06_erspan_mirror_test(sai_base_test.ThriftInterfaceDataPlane):
    
    def runTest(self):
        print       
        switch_init(self.client)

        
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        mac3='00:00:00:00:00:33'
        mac2='00:00:00:00:00:22'
        monitor_port=port1
        port_list_valid = 0
        monitor_port_list = []
        source_port=port2
        mirror_type=SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE
        src_mac='00:00:00:00:11:22'
        dst_mac='00:00:00:00:11:33'
        encap_type=SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL
        ip_version=0x4
        tos=0x3c
        ttl=0x22
        gre_type=0x22eb
        src_ip='17.18.19.0'
        dst_ip='33.19.20.0'
        addr_family=0
        vlan_remote_id = 3
        mac_action = SAI_PACKET_ACTION_FORWARD  
        
        src_mac_set='00:00:00:00:34:56'
        dst_mac_set='00:00:00:00:67:89'
        tos_set=0x3d
        ttl_set=0x2d
        gre_type_set=0x2222
        src_ip_set='11.12.13.14'
        dst_ip_set='21.22.23.24'        

        vlan_remote_oid = sai_thrift_create_vlan(self.client, vlan_remote_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_remote_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_remote_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_remote_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_remote_oid, mac3, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_remote_oid, mac2, port2, mac_action)

        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE======")
        erspanid = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            None, None, None, None, 
            src_mac=src_mac,dst_mac=dst_mac,src_ip=src_ip,dst_ip=dst_ip,encap_type=encap_type,iphdr_version=ip_version,ttl=ttl,tos=tos,gre_type=gre_type)

        sys_logging("======bind the mirror session to port2 ingress and egress======")
        attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[erspanid]))

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_MIRROR_SESSION, value=attrb_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:33',
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=3,
                                ip_id=101,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:22',
                                eth_src='00:33:33:33:33:33',
                                dl_vlan_enable=True,
                                vlan_vid=3,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        exp_pkt1= ipv4_erspan_platform_pkt(pktlen=142,
                                    eth_dst='00:00:00:00:11:33',
                                    eth_src='00:00:00:00:11:22',
                                    ip_id=0,
                                    ip_ttl=0x22,
                                    ip_tos=0xF0,
                                    ip_ihl=5,
                                    ip_src='17.18.19.0',
                                    ip_dst='33.19.20.0',
                                    version=2,
                                    mirror_id=(erspanid & 0x3FFFFFFF),
                                    inner_frame=pkt1
                                    )

        exp_pkt2= ipv4_erspan_platform_pkt(pktlen=142,
                                    eth_dst='00:00:00:00:11:33',
                                    eth_src='00:00:00:00:11:22',
                                    ip_id=0,
                                    ip_ttl=0x22,
                                    ip_tos=0xF0,
                                    ip_ihl=5,
                                    ip_src='17.18.19.0',
                                    ip_dst='33.19.20.0',
                                    version=2,
                                    mirror_id=(erspanid & 0x3FFFFFFF),
                                    inner_frame=pkt2
                                    )
                                   
        m1=Mask(exp_pkt1)
        m1.set_do_not_care_scapy(ptf.packet.IP,'frag')
        m1.set_do_not_care_scapy(ptf.packet.IP,'flags')
        m1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'platf_id')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info1')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info2')
            
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'span_id')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'timestamp')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'sgt_other')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'direction')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'version')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'vlan')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'priority')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'truncated')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'unknown2')
        
        m2=Mask(exp_pkt2)
        m2.set_do_not_care_scapy(ptf.packet.IP,'frag')
        m2.set_do_not_care_scapy(ptf.packet.IP,'flags')
        m2.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m2.set_do_not_care_scapy(ptf.packet.IP,'id')
        m2.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'platf_id')
        m2.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info1')
        m2.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info2')
            
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'span_id')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'timestamp')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'sgt_other')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'direction')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'version')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'vlan')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'priority')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'truncated')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'unknown2')
        
        warmboot(self.client)
        try:
            sys_logging("======send packet from port2 to port3,mirror to port1======")
            self.ctc_send_packet( 2, pkt1)
            self.ctc_verify_each_packet_on_each_port( [m1,pkt1], ports=[1,3])
            
            sys_logging("======send packet from port3 to port2,mirror to port1======")
            self.ctc_send_packet( 3, pkt2)            
            self.ctc_verify_each_packet_on_each_port( [pkt2,m2], ports=[2,1])
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_remote_oid, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_remote_oid, mac3, port3)
            
            attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_MIRROR_SESSION, value=attrb_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
 
            self.client.sai_thrift_remove_mirror_session(erspanid)
 
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_remote_oid)
           
class scenario_07_local_mirror_set_attribute_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        vlan_id = 10
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
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

        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        monitor_port_list = []
        port_list_valid = False
        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
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
    
        sys_logging("======bind the mirror session to port1 and port2 ingress======")
        attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[ingress_localmirror_id]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)

        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)


        sys_logging("======set the mirror session attribute======")
        sys_logging("Set mirror session: monitor_port = port0")
        attr_value = sai_thrift_attribute_value_t(oid=port0)
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_MONITOR_PORT, value=attr_value)
        self.client.sai_thrift_set_mirror_attribute(ingress_localmirror_id, attr)
        warmboot(self.client)
        
        try:


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

            sys_logging("======send packet from port1 to port2,mirror to port0======")
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, pkt1], [2, 0])

            time.sleep(1)

            pkt2 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                vlan_vid=10,
                dl_vlan_enable=True,
                ip_id=102,
                ip_ttl=64,
                pktlen=104)
            exp_pkt2 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                ip_id=102,
                ip_ttl=64,
                pktlen=100)

            sys_logging("======send packet from port2 to port1,mirror to port0======")
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, pkt2], [1, 0])
            
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_08_portlist_local_mirror_set_attribute_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print''
        
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        port5 = port_list[5]
        port6 = port_list[6]
        port7 = port_list[7]
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

        # setup local mirror session
        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port3
        monitor_port_list = [port3, port4, port5]
        monitor_port_list1 = [port4, port5, port6, port7]
        port_list_valid = True

        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_TYPE_LOCAL======")
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

        sys_logging("======bind the mirror session to port1 and port2 ingress======")
        attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[ingress_localmirror_id]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)

        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sys_logging("======set the mirror session attribute======")
        sys_logging("Set mirror session: port_list = monitor_port_list1")
        attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=len(monitor_port_list1),object_id_list=monitor_port_list1))
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_MONITOR_PORTLIST, value=attr_value)
        self.client.sai_thrift_set_mirror_attribute(ingress_localmirror_id, attr)
        warmboot(self.client)
        
        try:

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

            sys_logging("======send packet from port1 to port2,mirror to port4,port5,port6,port7======")
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1, pkt1, pkt1, pkt1, pkt1], [2, 4, 5, 6, 7])


            pkt2 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                vlan_vid=10,
                dl_vlan_enable=True,
                ip_id=102,
                ip_ttl=64,
                pktlen=104)
            exp_pkt2 = simple_tcp_packet(eth_dst=mac1,
                eth_src=mac2,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1',
                ip_id=102,
                ip_ttl=64,
                pktlen=100)

            sys_logging("======send packet from port2 to port1,mirror to port4,port5,port6,port7======")
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_each_packet_on_each_port( [exp_pkt2, pkt2, pkt2, pkt2, pkt2], [1, 4, 5, 6, 7])
            
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_09_erspan_mirror_set_attribute_test(sai_base_test.ThriftInterfaceDataPlane):
    
    def runTest(self):
        print       
        switch_init(self.client)

        
        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        mac3='00:00:00:00:00:33'
        mac2='00:00:00:00:00:22'
        monitor_port=port1
        port_list_valid = 0
        monitor_port_list = []

        mirror_type=SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE
        src_mac='00:00:00:00:11:22'
        dst_mac='00:00:00:00:11:33'
        encap_type=SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL
        ip_version=0x4
        tos=0x3c
        ttl=0x22
        gre_type=0x22eb
        src_ip='17.18.19.0'
        dst_ip='33.19.20.0'
        addr_family=0
        vlan_remote_id = 3
        mac_action = SAI_PACKET_ACTION_FORWARD  
        
        src_mac_set='00:00:00:00:34:56'
        dst_mac_set='00:00:00:00:67:89'
        tos_set=0x3d
        ttl_set=0x2d
        gre_type_set=0x2222
        src_ip_set='11.12.13.14'
        dst_ip_set='21.22.23.24'  

        vlan_header_valid = True
        vlan_id_set = 10

        vlan_remote_oid = sai_thrift_create_vlan(self.client, vlan_remote_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_remote_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_remote_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_remote_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_remote_oid, mac3, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_remote_oid, mac2, port2, mac_action)

        sys_logging("======Create 1 mirror session: mirror_type = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE======")
        erspanid = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            None, None, None, None, 
            src_mac=src_mac,dst_mac=dst_mac,src_ip=src_ip,dst_ip=dst_ip,encap_type=encap_type,iphdr_version=ip_version,ttl=ttl,tos=tos,gre_type=gre_type)

        sys_logging("======bind the mirror session to  port2 ingress and egress======")
        attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[erspanid]))

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_MIRROR_SESSION, value=attrb_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)


        sys_logging("======set the mirror session attribute======")
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id_set)
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_mirror_attribute(erspanid, attr)
        attr_value = sai_thrift_attribute_value_t(booldata=vlan_header_valid)
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_VLAN_HEADER_VALID,value=attr_value)
        self.client.sai_thrift_set_mirror_attribute(erspanid, attr)
        
            
        attr_value = sai_thrift_attribute_value_t(oid=port0)
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_MONITOR_PORT, value=attr_value)
        self.client.sai_thrift_set_mirror_attribute(erspanid, attr)
        
        attr_value = sai_thrift_attribute_value_t(mac=src_mac_set)
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_SRC_MAC_ADDRESS, value=attr_value)
        status=self.client.sai_thrift_set_mirror_attribute(erspanid, attr)

        attr_value = sai_thrift_attribute_value_t(mac=dst_mac_set)
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_DST_MAC_ADDRESS, value=attr_value)
        self.client.sai_thrift_set_mirror_attribute(erspanid, attr)

        addr = sai_thrift_ip_t(ip4=src_ip_set)
        src_ip_addr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
        attribute5_value = sai_thrift_attribute_value_t(ipaddr=src_ip_addr)
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_SRC_IP_ADDRESS, value=attribute5_value)
        self.client.sai_thrift_set_mirror_attribute(erspanid, attr)

        addr = sai_thrift_ip_t(ip4=dst_ip_set)
        dst_ip_addr = sai_thrift_ip_address_t(addr_family=addr_family, addr=addr)
        attribute6_value = sai_thrift_attribute_value_t(ipaddr=dst_ip_addr)
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_DST_IP_ADDRESS, value=attribute6_value)
        self.client.sai_thrift_set_mirror_attribute(erspanid, attr)

        attr_value = sai_thrift_attribute_value_t(u8=tos_set)
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_TOS, value=attr_value)
        self.client.sai_thrift_set_mirror_attribute(erspanid, attr)

        attr_value = sai_thrift_attribute_value_t(u8=ttl_set)
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_TTL, value=attr_value)
        self.client.sai_thrift_set_mirror_attribute(erspanid, attr)

        attr_value = sai_thrift_attribute_value_t(u16=gre_type_set)
        attr = sai_thrift_attribute_t(id=SAI_MIRROR_SESSION_ATTR_GRE_PROTOCOL_TYPE, value=attr_value)
        self.client.sai_thrift_set_mirror_attribute(erspanid, attr)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:33',
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=3,
                                ip_id=101,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:22',
                                eth_src='00:33:33:33:33:33',
                                dl_vlan_enable=True,
                                vlan_vid=3,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        exp_pkt1= ipv4_erspan_platform_pkt(pktlen=146,
                                    eth_dst='00:00:00:00:67:89',
                                    eth_src='00:00:00:00:34:56',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_id=0,
                                    ip_ttl=0x2d,
                                    ip_tos=0x3d,
                                    ip_ihl=5,
                                    ip_src='11.12.13.14',
                                    ip_dst='21.22.23.24',
                                    version=2,
                                    mirror_id=(erspanid & 0x3FFFFFFF),
                                    inner_frame=pkt1
                                    )

        exp_pkt2= ipv4_erspan_platform_pkt(pktlen=146,
                                    eth_dst='00:00:00:00:67:89',
                                    eth_src='00:00:00:00:34:56',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_id=0,
                                    ip_ttl=0x2d,
                                    ip_tos=0x3d,
                                    ip_ihl=5,
                                    ip_src='11.12.13.14',
                                    ip_dst='21.22.23.24',
                                    version=2,
                                    mirror_id=(erspanid & 0x3FFFFFFF),
                                    inner_frame=pkt2
                                    )
        m1=Mask(exp_pkt1)
        m1.set_do_not_care_scapy(ptf.packet.IP,'tos')
        m1.set_do_not_care_scapy(ptf.packet.IP,'frag')
        m1.set_do_not_care_scapy(ptf.packet.IP,'flags')
        m1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1.set_do_not_care_scapy(ptf.packet.GRE,'proto')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'platf_id')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info1')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info2')
            
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'span_id')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'timestamp')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'sgt_other')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'direction')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'version')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'vlan')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'priority')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'truncated')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'unknown2')
        
        m2=Mask(exp_pkt2)
        m2.set_do_not_care_scapy(ptf.packet.IP,'tos')
        m2.set_do_not_care_scapy(ptf.packet.IP,'frag')
        m2.set_do_not_care_scapy(ptf.packet.IP,'flags')
        m2.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m2.set_do_not_care_scapy(ptf.packet.IP,'id')
        m2.set_do_not_care_scapy(ptf.packet.GRE,'proto')
        m2.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'platf_id')
        m2.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info1')
        m2.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info2')
            
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'span_id')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'timestamp')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'sgt_other')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'direction')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'version')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'vlan')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'priority')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'truncated')
        m2.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'unknown2')
        
        warmboot(self.client)
        try:
            sys_logging("======send packet from port2 to port3,mirror to port0======")
            self.ctc_send_packet( 2, pkt1)
            self.ctc_verify_each_packet_on_each_port( [m1,pkt1], ports=[0,3])
            
            sys_logging("======send packet from port3 to port2,mirror to port0======")
            self.ctc_send_packet( 3, pkt2)            
            self.ctc_verify_each_packet_on_each_port( [pkt2,m2], ports=[2,0])
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_remote_oid, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_remote_oid, mac3, port3)
           
            attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_MIRROR_SESSION, value=attrb_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
           

            self.client.sai_thrift_remove_mirror_session(erspanid)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_remote_oid)

class scenario_10_one_port_to_multi_mirror_set_attribute_test(sai_base_test.ThriftInterfaceDataPlane):
    
    def runTest(self):
        print       
        switch_init(self.client)

        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        port5 = port_list[5]
        port6 = port_list[6]
        port7 = port_list[7]

        mirror_type1 = SAI_MIRROR_SESSION_TYPE_LOCAL
        mirror_type2 = SAI_MIRROR_SESSION_TYPE_REMOTE
        mirror_type3 = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE
        
        mac1='00:00:00:00:00:33'
        mac2='00:00:00:00:00:22'
        
        port_list_valid = 0
        port_list_valid1 = 1
        monitor_port1=port2
        monitor_port_list = [port3, port4, port5]
        monitor_port2=port6
        monitor_port3=port7
        
        src_mac='00:00:00:00:11:22'
        dst_mac='00:00:00:00:11:33'
        encap_type=SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL
        ip_version=0x4
        tos=0x3c
        ttl=0x22
        gre_type=0x22eb
        src_ip='17.18.19.0'
        dst_ip='33.19.20.0'
        addr_family=0
        vlan_remote_id = 3
        mac_action = SAI_PACKET_ACTION_FORWARD  
        
        src_mac_set='00:00:00:00:34:56'
        dst_mac_set='00:00:00:00:67:89'
        tos_set=0x3d
        ttl_set=0x2d
        gre_type_set=0x2222
        src_ip_set='11.12.13.14'
        dst_ip_set='21.22.23.24'

        vlan_header_valid = True
        vlan_id_set = 10
        vlan_id_remote = 20

        vlan_remote_oid = sai_thrift_create_vlan(self.client, vlan_remote_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_remote_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_remote_oid, port0, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_remote_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_remote_oid, mac2, port0, mac_action)

        sys_logging("======Create 4 mirror session======")
        localmirror1 = sai_thrift_create_mirror_session(self.client,
            mirror_type1,
            monitor_port1,
            monitor_port_list,
            port_list_valid,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        localmirror2 = sai_thrift_create_mirror_session(self.client,
            mirror_type1,
            monitor_port1,
            monitor_port_list,
            port_list_valid1,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        remotemirror = sai_thrift_create_mirror_session(self.client,
            mirror_type2,
            monitor_port2,
            monitor_port_list,
            port_list_valid,
            vlan_id_remote, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)    
        erspanid = sai_thrift_create_mirror_session(self.client,
            mirror_type3,
            monitor_port3,
            monitor_port_list,
            port_list_valid,
            None, None, None, None, 
            src_mac=src_mac,dst_mac=dst_mac,src_ip=src_ip,dst_ip=dst_ip,encap_type=encap_type,iphdr_version=ip_version,ttl=ttl,tos=tos,gre_type=gre_type)

        sys_logging("======bind 4 mirror session to port1 ingress======")
        attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=4,object_id_list=[localmirror1, localmirror2, remotemirror, erspanid]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        pkt = simple_tcp_packet(eth_dst='00:00:00:00:00:22',
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.0.0.1',
                                ip_src='192.168.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=3,
                                ip_id=1,
                                ip_ttl=64)

        exp_pkt1 = pkt
        
        exp_pkt2 =  simple_qinq_tcp_packet(pktlen=104,
                eth_dst='00:00:00:00:00:22',
                eth_src='00:22:22:22:22:22',
                dl_vlan_outer=20,
                vlan_vid=3,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1', 
                ip_ttl=64)

        exp_pkt3= ipv4_erspan_platform_pkt(pktlen=158,
                                    eth_dst='00:00:00:00:11:33',
                                    eth_src='00:00:00:00:11:22',
                                    ip_id=0,
                                    ip_ttl=0x22,
                                    ip_tos=0xF0,
                                    ip_ihl=5,
                                    ip_src='17.18.19.0',
                                    ip_dst='33.19.20.0',
                                    version=2,
                                    mirror_id=(erspanid & 0x3FFFFFFF),
                                    inner_frame=pkt
                                    )
        #print exp_pkt3.show()
        m1=Mask(exp_pkt3)
        m1.set_do_not_care_scapy(ptf.packet.IP,'tos')
        m1.set_do_not_care_scapy(ptf.packet.IP,'frag')
        m1.set_do_not_care_scapy(ptf.packet.IP,'flags')
        m1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1.set_do_not_care_scapy(ptf.packet.GRE,'proto')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'platf_id')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info1')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info2')
            
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'span_id')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'timestamp')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'sgt_other')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'direction')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'version')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'vlan')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'priority')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'truncated')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'unknown2')
        
        
        warmboot(self.client)
        try:
            sys_logging("======send packet from port1 to port0,mirror to port2,port3,port4,port5,port6,port7======")
            self.ctc_send_packet( 1, pkt)
            self.ctc_verify_each_packet_on_each_port( [exp_pkt1,exp_pkt1,exp_pkt1,exp_pkt1,exp_pkt1,exp_pkt2,m1], ports=[0,2,3,4,5,6,7])
            
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_remote_oid, mac2, port0)
            sai_thrift_delete_fdb(self.client, vlan_remote_oid, mac1, port1)
            
            attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
 
            self.client.sai_thrift_remove_mirror_session(localmirror1)
            self.client.sai_thrift_remove_mirror_session(localmirror2)
            self.client.sai_thrift_remove_mirror_session(remotemirror)
            self.client.sai_thrift_remove_mirror_session(erspanid)
 
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
 
            self.client.sai_thrift_remove_vlan(vlan_remote_oid)
 
class scenario_11_one_port_to_multi_mirror_broadcast_set_attribute_test(sai_base_test.ThriftInterfaceDataPlane):
    
    def runTest(self):
        print       
        switch_init(self.client)

        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        port5 = port_list[5]
        port6 = port_list[6]
        port7 = port_list[7]

        mirror_type1 = SAI_MIRROR_SESSION_TYPE_LOCAL
        mirror_type2 = SAI_MIRROR_SESSION_TYPE_REMOTE
        mirror_type3 = SAI_MIRROR_SESSION_TYPE_ENHANCED_REMOTE
        
        mac1='00:00:00:00:00:33'
        mac2='00:00:00:00:00:22'
        
        port_list_valid = 0
        port_list_valid1 = 1
        monitor_port1=port2
        monitor_port_list = [port4, port5]
        monitor_port2=port6
        monitor_port3=port7
        
        src_mac='00:00:00:00:11:22'
        dst_mac='00:00:00:00:11:33'
        encap_type=SAI_ERSPAN_ENCAPSULATION_TYPE_MIRROR_L3_GRE_TUNNEL
        ip_version=0x4
        tos=0x3c
        ttl=0x22
        gre_type=0x22eb
        src_ip='17.18.19.0'
        dst_ip='33.19.20.0'
        addr_family=0
        vlan_remote_id = 3
        mac_action = SAI_PACKET_ACTION_FORWARD  
        
        src_mac_set='00:00:00:00:34:56'
        dst_mac_set='00:00:00:00:67:89'
        tos_set=0x3d
        ttl_set=0x2d
        gre_type_set=0x2222
        src_ip_set='11.12.13.14'
        dst_ip_set='21.22.23.24'  

        vlan_header_valid = True
        vlan_id_set = 10
        vlan_id_remote = 20

        vlan_remote_oid = sai_thrift_create_vlan(self.client, vlan_remote_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_remote_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_remote_oid, port0, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_remote_oid, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        #sai_thrift_create_fdb(self.client, vlan_remote_oid, mac1, port1, mac_action)
        #sai_thrift_create_fdb(self.client, vlan_remote_oid, mac2, port0, mac_action)

        sys_logging("======Create 4 mirror session======")
        localmirror1 = sai_thrift_create_mirror_session(self.client,
            mirror_type1,
            monitor_port1,
            monitor_port_list,
            port_list_valid,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        localmirror2 = sai_thrift_create_mirror_session(self.client,
            mirror_type1,
            monitor_port1,
            monitor_port_list,
            port_list_valid1,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)
        remotemirror = sai_thrift_create_mirror_session(self.client,
            mirror_type2,
            monitor_port2,
            monitor_port_list,
            port_list_valid,
            vlan_id_remote, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)    
        erspanid = sai_thrift_create_mirror_session(self.client,
            mirror_type3,
            monitor_port3,
            monitor_port_list,
            port_list_valid,
            None, None, None, None, 
            src_mac=src_mac,dst_mac=dst_mac,src_ip=src_ip,dst_ip=dst_ip,encap_type=encap_type,iphdr_version=ip_version,ttl=ttl,tos=tos,gre_type=gre_type)

        sys_logging("======bind 4 mirror session to port1 ingress======")
        attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=4,object_id_list=[localmirror1, localmirror2, remotemirror, erspanid]))
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        pkt = simple_tcp_packet(eth_dst='00:00:00:00:00:22',
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.0.0.1',
                                ip_src='192.168.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=3,
                                ip_id=1,
                                ip_ttl=64)

        exp_pkt1 = pkt
        
        exp_pkt2 =  simple_qinq_tcp_packet(pktlen=104,
                eth_dst='00:00:00:00:00:22',
                eth_src='00:22:22:22:22:22',
                dl_vlan_outer=20,
                vlan_vid=3,
                ip_dst='10.0.0.1',
                ip_src='192.168.0.1', 
                ip_ttl=64)

        exp_pkt3= ipv4_erspan_platform_pkt(pktlen=158,
                                    eth_dst='00:00:00:00:11:33',
                                    eth_src='00:00:00:00:11:22',
                                    ip_id=0,
                                    ip_ttl=0x22,
                                    ip_tos=0xF0,
                                    ip_ihl=5,
                                    ip_src='17.18.19.0',
                                    ip_dst='33.19.20.0',
                                    version=2,
                                    mirror_id=(erspanid & 0x3FFFFFFF),
                                    inner_frame=pkt
                                    )
        #print exp_pkt3.show()
        m1=Mask(exp_pkt3)
        m1.set_do_not_care_scapy(ptf.packet.IP,'tos')
        m1.set_do_not_care_scapy(ptf.packet.IP,'frag')
        m1.set_do_not_care_scapy(ptf.packet.IP,'flags')
        m1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1.set_do_not_care_scapy(ptf.packet.GRE,'proto')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'platf_id')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info1')
        m1.set_do_not_care_scapy(ptf.packet.PlatformSpecific, 'info2')
            
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'span_id')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'timestamp')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'sgt_other')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'direction')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'version')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'vlan')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'priority')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'truncated')
        m1.set_do_not_care_scapy(ptf.packet.ERSPAN_III, 'unknown2')
        
        
        warmboot(self.client)
        try:
            sys_logging("======send packet from port1 to port0,mirror to port2,port3,port4,port5,port6,port7======")
            self.ctc_send_packet( 1, pkt)
            self.ctc_verify_packet( exp_pkt2, 6)
            #self.ctc_verify_each_packet_on_each_port( [exp_pkt1,exp_pkt1,exp_pkt1,exp_pkt1,exp_pkt1,exp_pkt2,m1], ports=[0,2,3,4,5,6,7])
            
        finally:
            sys_logging("======clean up======")
            #sai_thrift_delete_fdb(self.client, vlan_remote_oid, mac2, port0)
            #sai_thrift_delete_fdb(self.client, vlan_remote_oid, mac1, port1)
            
            attrb_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attrb_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
 
            self.client.sai_thrift_remove_mirror_session(localmirror1)
            self.client.sai_thrift_remove_mirror_session(localmirror2)
            self.client.sai_thrift_remove_mirror_session(remotemirror)
            self.client.sai_thrift_remove_mirror_session(erspanid)
 
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
 
            self.client.sai_thrift_remove_vlan(vlan_remote_oid)