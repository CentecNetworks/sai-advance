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
Thrift SAI interface synceE tests
"""
import socket
from switch import *
import sai_base_test
from ptf.mask import Mask
import pdb

@group('synce')

class func_01_create_synce_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        recovered_port = 1
        clock_divider = 1
        syncE_oid = sai_thrift_create_syncE(self.client, recovered_port, clock_divider)
        sys_logging("###the syncE_oid %x ###" %syncE_oid)
        try:
            assert(syncE_oid==0x10000005e)
            
        finally:
            self.client.sai_thrift_remove_synce(syncE_oid)

class func_02_create_another_synce_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        recovered_port = 1
        clock_divider = 1
        syncE_oid = sai_thrift_create_syncE(self.client, recovered_port, clock_divider)

        syncE_oid_new = sai_thrift_create_syncE(self.client, recovered_port, clock_divider)
        sys_logging("###the syncE_oid %x ###" %syncE_oid_new)
        try:
            assert(syncE_oid_new==SAI_NULL_OBJECT_ID)
            
        finally:
            self.client.sai_thrift_remove_synce(syncE_oid)

class func_03_remove_synce_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        recovered_port = 1
        clock_divider = 1
        syncE_oid = sai_thrift_create_syncE(self.client, recovered_port, clock_divider)
        
        attrs = self.client.sai_thrift_get_synce_attribute(syncE_oid)
        sys_logging("get synce attribute status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        try:
            status = self.client.sai_thrift_remove_synce(syncE_oid)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_synce_attribute(syncE_oid)
            sys_logging("get synce attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("======clean up======") 

class func_04_remove_no_exist_synce_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        recovered_port = 1
        clock_divider = 1
        syncE_oid = sai_thrift_create_syncE(self.client, recovered_port, clock_divider)
        
        self.client.sai_thrift_remove_synce(syncE_oid)
        try:
            status = self.client.sai_thrift_remove_synce(syncE_oid)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
            
        finally:
            sys_logging("======clean up======") 

class func_05_set_synce_attr_clock_divider_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        recovered_port = 1
        clock_divider = 1
        syncE_oid = sai_thrift_create_syncE(self.client, recovered_port, clock_divider)
        clock_divider1 =7
        sys_logging("###the syncE_oid %x ###" %syncE_oid)
        
        attrs = self.client.sai_thrift_get_synce_attribute(syncE_oid)
        sys_logging("get synce attribute status = %d" %attrs.status)
        for a in attrs.attr_list:
            if a.id == SAI_SYNCE_ATTR_CLOCK_DIVIDER:
                print " SyncE divider = 0x%x" %a.value.u16

        try:
            attr_value = sai_thrift_attribute_value_t(u16=clock_divider1)
            attr = sai_thrift_attribute_t(id=SAI_SYNCE_ATTR_CLOCK_DIVIDER, value=attr_value)
            status = self.client.sai_thrift_set_synce_attribute(syncE_oid, attr)
            sys_logging("set synce attribute status = %d" %status)

            attrs = self.client.sai_thrift_get_synce_attribute(syncE_oid)
            sys_logging("get synce attribute status = %d" %attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SYNCE_ATTR_CLOCK_DIVIDER:
                    print " SyncE divider = 0x%x" %a.value.u16
                    if a.value.u16 != clock_divider1:
                        raise NotImplementedError()
            
        finally:
            self.client.sai_thrift_remove_synce(syncE_oid)

class func_06_set_synce_attr_recovered_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        recovered_port = 1
        clock_divider = 1
        syncE_oid = sai_thrift_create_syncE(self.client, recovered_port, clock_divider)
        recovered_port1 = 5
        sys_logging("###the syncE_oid %x ###" %syncE_oid)
        
        attrs = self.client.sai_thrift_get_synce_attribute(syncE_oid)
        sys_logging("get synce attribute status = %d" %attrs.status)
        for a in attrs.attr_list:
            if a.id == SAI_SYNCE_ATTR_RECOVERED_PORT:
                print " SyncE recovered port = 0x%x" %a.value.u16

        try:
            attr_value = sai_thrift_attribute_value_t(u16=recovered_port1)
            attr = sai_thrift_attribute_t(id=SAI_SYNCE_ATTR_RECOVERED_PORT, value=attr_value)
            status = self.client.sai_thrift_set_synce_attribute(syncE_oid, attr)
            sys_logging("set synce attribute status = %d" %status)

            attrs = self.client.sai_thrift_get_synce_attribute(syncE_oid)
            sys_logging("get synce attribute status = %d" %attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SYNCE_ATTR_RECOVERED_PORT:
                    print " SyncE recovered port = 0x%x" %a.value.u16
                    if a.value.u16 != recovered_port1:
                        raise NotImplementedError()
            
        finally:
            self.client.sai_thrift_remove_synce(syncE_oid)


class func_07_get_synce_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        recovered_port = 3
        clock_divider = 4
        syncE_oid = sai_thrift_create_syncE(self.client, recovered_port, clock_divider)
        sys_logging("###the syncE_oid %x ###" %syncE_oid)

        try:
            attrs = self.client.sai_thrift_get_synce_attribute(syncE_oid)
            sys_logging("get synce attribute status = %d" %attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SYNCE_ATTR_CLOCK_DIVIDER:
                    print " SyncE divider = 0x%x" %a.value.u16
                    if a.value.u16 != clock_divider:
                        raise NotImplementedError()
                if a.id == SAI_SYNCE_ATTR_RECOVERED_PORT:
                    print " SyncE recovered port = 0x%x" %a.value.u16
                    if a.value.u16 != recovered_port:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_synce(syncE_oid)

