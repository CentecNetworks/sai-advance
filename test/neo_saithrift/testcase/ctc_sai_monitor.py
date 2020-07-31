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
Thrift SAI interface Monitor tests
"""
import socket
from switch import *
import sai_base_test
from ptf.mask import Mask
import pdb

@group('monitor')

class func_01_create_monitor_buffer_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        
        port = port_list[2]
        sys_logging("port:",port)
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("###the buffer_oid %x ###" %buffer_oid)
       
        try:
            assert(0 != buffer_oid)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_02_create_monitor_buffer_with_all_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        port = port_list[2]
        
        threshold_min = 160000
        threshold_max =  320000
        ingr_port_perio_monitor_enable = True
        egr_port_perio_monitor_enable = False
        
        sys_logging("port:",port)
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port, threshold_min = threshold_min, threshold_max =  threshold_max, ingr_port_perio_monitor_enable = ingr_port_perio_monitor_enable, egr_port_perio_monitor_enable = egr_port_perio_monitor_enable)
        sys_logging("###the buffer_oid %x ###" %buffer_oid)
       
        try:
            assert(SAI_NULL_OBJECT_ID != buffer_oid)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)
            
class func_03_create_another_monitor_buffer_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        port = port_list[2]
        threshold_min = 160000
        threshold_max =  320000
        ingr_port_perio_monitor_enable = True
        egr_port_perio_monitor_enable = False
        
        sys_logging("port:",port)
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port, threshold_min = threshold_min, threshold_max =  threshold_max, ingr_port_perio_monitor_enable = ingr_port_perio_monitor_enable, egr_port_perio_monitor_enable = egr_port_perio_monitor_enable)
        sys_logging("###the buffer_oid %x ###" %buffer_oid)
        
        port = port_list[5]
        threshold_min = 120000
        threshold_max = 400000
        ingr_port_perio_monitor_enable = True
        egr_port_perio_monitor_enable = True
        
        sys_logging("port:",port)
        buffer_oid_new = sai_thrift_monitor_create_buffer(self.client, port, threshold_min = threshold_min, threshold_max =  threshold_max, ingr_port_perio_monitor_enable = ingr_port_perio_monitor_enable, egr_port_perio_monitor_enable = egr_port_perio_monitor_enable)
        sys_logging("###the buffer_oid_new %x ###" %buffer_oid_new)   
        
        try:
            assert(SAI_NULL_OBJECT_ID != buffer_oid_new)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid_new)
            
class func_04_create_monitor_latency_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        port = port_list[2]
        
        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("port:",port)
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("###the latency_oid %x ###" %latency_oid)
       
        try:
            assert(SAI_NULL_OBJECT_ID != latency_oid)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid)
