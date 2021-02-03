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
Thrift SAI interface virtual router tests
"""
import socket
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask

class func_01_create_virtual_router_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)

        sys_logging("======create virtual router======")
        v4_enabled = 0
        v6_enabled = 0
        vr_id1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        
        warmboot(self.client)
        try:
            assert(vr_id1 == 0x100000003)
            attrs = self.client.sai_thrift_get_virtual_router_attribute(vr_id1)
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE:
                    print "set v4_enabled = %d" %v4_enabled
                    print "get v4_enabled = %d" %a.value.booldata
                    if v4_enabled != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE:
                    print "set v6_enabled = %d" %v6_enabled
                    print "get v6_enabled = %d" %a.value.booldata
                    if v6_enabled != a.value.booldata:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_virtual_router(vr_id1)


 
class func_02_create_max_virtual_router_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        vr_num = 255
        vr_id_list = []

        sys_logging("=======create 255 virtual router=======")
        for i in range(vr_num):
            if v4_enabled == 1:
                v4_enabled == 0
                v6_enabled == 0
            else:
                v4_enabled == 1
                v6_enabled == 1
            vr_id_list.append(sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled))
            sys_logging("vr_id = 0x%x" %vr_id_list[i])
            attrs = self.client.sai_thrift_get_virtual_router_attribute(vr_id_list[i])
            assert (attrs.status == SAI_STATUS_SUCCESS)
        try:
            sys_logging("=======create another virtual router=======")
            vr_id1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
            sys_logging("vr_id = 0x%x" %vr_id1)
            assert(vr_id1 == 0x0)
        finally:
            sys_logging("======clean up======")
            for i in range(vr_num):
                self.client.sai_thrift_remove_virtual_router(vr_id_list[i])
                attrs = self.client.sai_thrift_get_virtual_router_attribute(vr_id_list[i])
                assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

            
class func_03_remove_virtual_router_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
      
        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1

        sys_logging("=======create virtual router=======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_virtual_router_attribute(vr_id)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("=======remove virtual router=======")
            status = self.client.sai_thrift_remove_virtual_router(vr_id)
            assert (status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_virtual_router_attribute(vr_id)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            sys_logging("======clean up======")


class func_04_remove_no_exist_virtual_router_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
       
        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        sys_logging("=======create virtual router=======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        vr_id1 = 0
        vr_id2 = 0x200000003
        warmboot(self.client)
        try:
            sys_logging("=======remove no exist virtual router=======")
            statu = self.client.sai_thrift_remove_virtual_router(vr_id1)
            sys_logging("statu = %d"%statu)
            assert (statu == SAI_STATUS_ITEM_NOT_FOUND)
            
            sys_logging("=======remove no exist virtual router again=======")
            statu = self.client.sai_thrift_remove_virtual_router(vr_id2)
            sys_logging("statu = %d"%statu)
            assert (statu == SAI_STATUS_ITEM_NOT_FOUND)

            print "=======remove exist virtual router=======" 
            statu = self.client.sai_thrift_remove_virtual_router(vr_id)
            sys_logging("statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("======clean up======")


class func_05_virtual_router_set_and_get_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        v4_enabled = 0
        v6_enabled = 0
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
                
        warmboot(self.client)
        try:

            sys_logging("======set correct attribute======")
            v4_enabled = 1
            v6_enabled = 1
            vr_router_mac = "aa:bb:cc:dd:ee:ff"
            
            attr_value = sai_thrift_attribute_value_t(booldata=v4_enabled)
            attr = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE, value=attr_value)
            statu = self.client.sai_thrift_set_virtual_router_attribute(vr_id, attr)
            sys_logging("statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)
            
            attr_value = sai_thrift_attribute_value_t(booldata=v6_enabled)
            attr = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE, value=attr_value)
            statu = self.client.sai_thrift_set_virtual_router_attribute(vr_id, attr)
            sys_logging("statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)
            
            attr_value = sai_thrift_attribute_value_t(mac=vr_router_mac)
            attr = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            statu = self.client.sai_thrift_set_virtual_router_attribute(vr_id, attr)
            sys_logging("statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)

            sys_logging("======get attribute======")
            attrs = self.client.sai_thrift_get_virtual_router_attribute(vr_id)
            sys_logging("status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE:
                    print "set v4_enabled = %d" %v4_enabled
                    print "get v4_enabled = %d" %a.value.booldata
                    if v4_enabled != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V6_STATE:
                    print "set v6_enabled = %d" %v6_enabled
                    print "get v6_enabled = %d" %a.value.booldata
                    if v6_enabled != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS:
                    print "set router_mac = %s" %vr_router_mac
                    print "get router_mac = %s" %a.value.mac
                    if vr_router_mac != a.value.mac:
                        raise NotImplementedError()    

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_virtual_router(vr_id)



class scenario_01_vr_change_rif_attr(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        print ""
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        port1 = port_list[0]
        vr_mac = ''


        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, vr_mac)

        warmboot(self.client)

        try:
            sys_logging("======first get rif v4_state and routermac======")
            attrs = self.client.sai_thrift_get_router_interface_attribute(rif_id)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE:
                    sys_logging("set v4_enabled = %d" %v4_enabled)
                    sys_logging("get v4_enabled = %d" %a.value.booldata)
                    if v4_enabled != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS:
                    sys_logging("set router_mac = %s" %router_mac)
                    sys_logging("get router_mac = %s" %a.value.mac)
                    if router_mac != a.value.mac:
                        raise NotImplementedError()  

            sys_logging("=======change virtual router v4_state and routermac=======")
            v4_enabled = 0 
            vr_mac = '12:34:34:56:56:78'
            attr_value = sai_thrift_attribute_value_t(booldata=v4_enabled)
            attr = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_ADMIN_V4_STATE, value=attr_value)
            self.client.sai_thrift_set_virtual_router_attribute(vr_id, attr)
            attr_value = sai_thrift_attribute_value_t(mac=vr_mac)
            attr = sai_thrift_attribute_t(id=SAI_VIRTUAL_ROUTER_ATTR_SRC_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_virtual_router_attribute(vr_id, attr)

            sys_logging("=======get rif v4_state and routermac again=======")
            attrs1 = self.client.sai_thrift_get_router_interface_attribute(rif_id)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs1.attr_list:
                if a.id == SAI_ROUTER_INTERFACE_ATTR_ADMIN_V4_STATE:
                    
                    sys_logging("get new v4_enabled = %d" %a.value.booldata)
                    if v4_enabled != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ROUTER_INTERFACE_ATTR_SRC_MAC_ADDRESS:
                   
                    sys_logging("get new router_mac = %s" %a.value.mac)
                    if router_mac != a.value.mac:
                        raise NotImplementedError()    
        finally:

            sys_logging("======clean up======")
            self.client.sai_thrift_remove_router_interface(rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)


class scenario_02_stress(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        v4_enabled = 1
        v6_enabled = 1
        vr_num = 255
        vr_id_list = []


        sys_logging("=======create 255 virtual router=======")
        for i in range(vr_num):
            if v4_enabled == 1:
                v4_enabled == 0
                v6_enabled == 0
            else:
                v4_enabled == 1

                v6_enabled == 1
            vr_id_list.append(sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled))
            sys_logging("vr_id = 0x%x" %vr_id_list[i])
        try:
            for i in range(vr_num):
                attrs = self.client.sai_thrift_get_virtual_router_attribute(vr_id_list[i])
                assert (attrs.status == SAI_STATUS_SUCCESS)
        finally:
            sys_logging("======clean up======")
            for i in range(vr_num):
                
                self.client.sai_thrift_remove_virtual_router(vr_id_list[i])
                attrs = self.client.sai_thrift_get_virtual_router_attribute(vr_id_list[i])
                assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
    
        




