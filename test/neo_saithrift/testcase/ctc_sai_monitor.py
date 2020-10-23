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
import time
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
            
class func_05_create_monitor_buffer_and_set_switch_buffer_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print "start test"

        switch_init(self.client)
 
        #Set switch buffer monitor microburst enable
        microburst_enable = True
        attr_value = sai_thrift_attribute_value_t(booldata=microburst_enable)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)
        
        #Set switch buffer monitor microburst min threshold 
        microburst_min_threshold = 150000
        attr_value = sai_thrift_attribute_value_t(u32=microburst_min_threshold)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)
        
        #Set switch buffer monitor microburst max threshold 
        microburst_max_threshold = 300000
        attr_value = sai_thrift_attribute_value_t(u32=microburst_max_threshold)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)
        
        # send the packet to cpu when the usage of buffer over the threshold 
        microburst_event_enable = True
        attr_value = sai_thrift_attribute_value_t(booldata=microburst_event_enable)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)
 
        port = port_list[2]
        sys_logging("port:",port)
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("###the buffer_oid %x ###" %buffer_oid)
        #pdb.set_trace()
        try:
            assert(0 != buffer_oid)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_06_create_monitor_latency_and_set_switch_buffer_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        
        #Set switch latency monitor  min threshold (ns)
        latency_min_threshold = 100
        attr_value = sai_thrift_attribute_value_t(u32=latency_min_threshold)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)
        
        #Set switch latency monitor  max threshold (ns)
        latency_max_threshold = 900
        attr_value = sai_thrift_attribute_value_t(u32=latency_max_threshold)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)
        
        
        port = port_list[2]
        
        microburst_event = [False, True, False, False, False, False, False, False]
        monitor_discard = [False, True, False, False, False, False, False, False]
        sys_logging("port:",port)
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("###the latency_oid %x ###" %latency_oid)
        #pdb.set_trace()
        try:
            assert(SAI_NULL_OBJECT_ID != latency_oid)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid)
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

@group('monitor_new_add')
class func_01_create_one_monitor_buffer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_01_create_one_monitor_buffer")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        warmboot(self.client)
        try:
            assert(SAI_NULL_OBJECT_ID != buffer_oid)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_02_create_two_diff_monitor_buffer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_02_create_two_diff_monitor_buffer")

        switch_init(self.client)

        port1 = port_list[2]
        sys_logging("======port1: %x======" %port1)
        sys_logging("======create monitor buffer======")
        buffer_oid1 = sai_thrift_monitor_create_buffer(self.client, port1)
        sys_logging("======the buffer_oid1: %x ======" %buffer_oid1)

        port2 = port_list[3]
        sys_logging("======port2: %x======" %port2)
        sys_logging("======create monitor buffer again======")
        buffer_oid2 = sai_thrift_monitor_create_buffer(self.client, port2)
        sys_logging("======the buffer_oid2: %x ======" %buffer_oid2)

        warmboot(self.client)
        try:
            assert(SAI_NULL_OBJECT_ID != buffer_oid1)
            assert(SAI_NULL_OBJECT_ID != buffer_oid2)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid1)
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid2)

class func_03_create_two_same_monitor_buffer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_03_create_two_same_monitor_buffer")

        switch_init(self.client)

        port1 = port_list[2]
        sys_logging("======port1: %x======" %port1)
        sys_logging("======create monitor buffer======")
        buffer_oid1 = sai_thrift_monitor_create_buffer(self.client, port1)
        sys_logging("======the buffer_oid1: %x ======" %buffer_oid1)

        port2 = port_list[2]
        sys_logging("======port2: %x======" %port2)
        sys_logging("======create monitor buffer again======")
        buffer_oid2 = sai_thrift_monitor_create_buffer(self.client, port2)
        sys_logging("======the buffer_oid2: %x ======" %buffer_oid2)

        warmboot(self.client)
        try:
            assert(SAI_NULL_OBJECT_ID != buffer_oid1)
            assert(SAI_NULL_OBJECT_ID == buffer_oid2)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid1)

class func_04_remove_exist_monitor_buffer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_04_remove_exist_monitor_buffer")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======remove monitor buffer======")
        status = self.client.sai_thrift_remove_monitor_buffer(buffer_oid)
        sys_logging( "remove monitor buffer status = %d" %status)

        warmboot(self.client)
        try:
            assert(status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            sys_logging("======success======")

class func_05_remove_non_exist_monitor_buffer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging(func_05_remove_non_exist_monitor_buffer)

        switch_init(self.client)

        buffer_oid = 8589934687

        sys_logging("======remove monitor buffer======")
        status = self.client.sai_thrift_remove_monitor_buffer(buffer_oid)
        sys_logging( "remove monitor buffer status = %d" %status)

        warmboot(self.client)
        try:
            assert(status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")
            sys_logging("======success======")

class func_06_set_monitor_buffer_attribute_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_06_set_monitor_buffer_attribute_port")

        switch_init(self.client)

        port = port_list[2]
        port1 = port_list[3]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(oid=port1)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        warmboot(self.client)
        try:
            assert(status == SAI_STATUS_INVALID_ATTRIBUTE_0)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_07_set_monitor_buffer_attribute_threshold_min(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_07_set_monitor_buffer_attribute_threshold_min")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=160000)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                    assert(160000 == a.value.u32)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_08_set_monitor_buffer_attribute_threshold_max(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_08_set_monitor_buffer_attribute_threshold_max")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=320000)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                    assert(320000 == a.value.u32)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_09_set_monitor_buffer_attribute_ingress_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_09_set_monitor_buffer_attribute_ingress_enable")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                    assert(True == a.value.booldata)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_10_set_monitor_buffer_attribute_egress_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_10_set_monitor_buffer_attribute_egress_enable")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                    assert(True == a.value.booldata)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_11_set_monitor_buffer_attribute_egress_total_watermark_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_11_set_monitor_buffer_attribute_egress_total_watermark_zero")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=0)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK:
                    assert(0 == a.value.u32)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_12_set_monitor_buffer_attribute_egress_total_watermark_non_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_12_set_monitor_buffer_attribute_egress_total_watermark_non_zero")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=1)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        warmboot(self.client)
        try:
            assert(SAI_STATUS_FAILURE == status)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_13_set_monitor_buffer_attribute_egress_unicast_watermark_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_13_set_monitor_buffer_attribute_egress_unicast_watermark_zero")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=0)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK:
                    assert(0 == a.value.u32)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_14_set_monitor_buffer_attribute_egress_unicast_watermark_non_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_14_set_monitor_buffer_attribute_egress_unicast_watermark_non_zero")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=1)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        warmboot(self.client)
        try:
            assert(SAI_STATUS_FAILURE == status)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_15_set_monitor_buffer_attribute_egress_multicast_watermark_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_15_set_monitor_buffer_attribute_egress_multicast_watermark_zero")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=0)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK:
                    assert(0 == a.value.u32)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_16_set_monitor_buffer_attribute_egress_multicast_watermark_non_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_16_set_monitor_buffer_attribute_egress_multicast_watermark_non_zero")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=1)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        warmboot(self.client)
        try:
            assert(SAI_STATUS_FAILURE == status)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_17_set_monitor_buffer_attribute_ingress_total_watermark_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_17_set_monitor_buffer_attribute_ingress_total_watermark_zero")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=0)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK:
                    assert(0 == a.value.u32)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_18_set_monitor_buffer_attribute_ingress_total_watermark_non_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_18_set_monitor_buffer_attribute_ingress_total_watermark_non_zero")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=1)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        warmboot(self.client)
        try:
            assert(SAI_STATUS_FAILURE == status)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_19_get_monitor_buffer_attribute(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_19_get_monitor_buffer_attribute")

        switch_init(self.client)

        port = port_list[2]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor buffer======")
        buffer_oid = sai_thrift_monitor_create_buffer(self.client, port)
        sys_logging("======the buffer_oid: %x ======" %buffer_oid)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                assert(150000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                assert(300000 == a.value.u32)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=160000)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(u32=320000)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(u32=0)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(u32=0)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(u32=0)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(u32=0)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK, value=attr_value)
        sys_logging("======set monitor buffer attr======")
        status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid, attr)
        sys_logging( "set monitor buffer status = %d" %status)

        sys_logging("======get monitor buffer attr======")
        attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid)
        sys_logging( "get monitor buffer attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN:
                    assert(160000 == a.value.u32)
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX:
                    assert(320000 == a.value.u32)
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                    assert(True == a.value.booldata)
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE:
                    assert(True == a.value.booldata)
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK:
                    assert(0 == a.value.u32)
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK:
                    assert(0 == a.value.u32)
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK:
                    assert(0 == a.value.u32)
                if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK:
                    assert(0 == a.value.u32)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid)

class func_20_create_one_monitor_latency(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_20_create_one_monitor_latency")

        switch_init(self.client)

        port = port_list[2]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor latency======")
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid %x ======" %latency_oid)
       
        try:
            assert(SAI_NULL_OBJECT_ID != latency_oid)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid)

class func_21_create_two_diff_monitor_latency(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_21_create_two_diff_monitor_latency")

        switch_init(self.client)

        port1 = port_list[2]
        port2 = port_list[3]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port1: %x======" %port1)
        sys_logging("======create monitor latency======")
        latency_oid1 = sai_thrift_monitor_create_latency(self.client, port1, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid1 %x ======" %latency_oid1)

        sys_logging("======port2: %x======" %port2)
        sys_logging("======create monitor latency again======")
        latency_oid2 = sai_thrift_monitor_create_latency(self.client, port2, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid2 %x ======" %latency_oid2)
       
        try:
            assert(SAI_NULL_OBJECT_ID != latency_oid1)
            assert(SAI_NULL_OBJECT_ID != latency_oid2)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid1)
            self.client.sai_thrift_remove_monitor_latency(latency_oid2)

class func_22_create_two_same_monitor_latency(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_22_create_two_same_monitor_latency")

        switch_init(self.client)

        port1 = port_list[2]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port1: %x======" %port1)
        sys_logging("======create monitor latency======")
        latency_oid1 = sai_thrift_monitor_create_latency(self.client, port1, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid1 %x ======" %latency_oid1)

        sys_logging("======create monitor latency again======")
        latency_oid2 = sai_thrift_monitor_create_latency(self.client, port1, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid2 %x ======" %latency_oid2)
       
        try:
            assert(SAI_NULL_OBJECT_ID != latency_oid1)
            assert(SAI_NULL_OBJECT_ID == latency_oid2)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid1)

class func_23_remove_exist_monitor_latency(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_23_remove_exist_monitor_latency")

        switch_init(self.client)

        port = port_list[2]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor latency======")
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid %x ======" %latency_oid)

        sys_logging("======remove monitor latency======")
        status = self.client.sai_thrift_remove_monitor_latency(latency_oid)
        sys_logging( "remove monitor buffer status = %d" %status)

        warmboot(self.client)
        try:
            assert(status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            sys_logging("======success======")

class func_24_remove_non_exist_monitor_latency(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_24_remove_non_exist_monitor_latency")

        switch_init(self.client)

        latency_oid = 8589934688

        sys_logging("======remove monitor latency======")
        status = self.client.sai_thrift_remove_monitor_latency(latency_oid)
        sys_logging( "remove monitor buffer status = %d" %status)

        warmboot(self.client)
        try:
            assert(status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")
            sys_logging("======success======")

class func_25_set_monitor_latency_attribute_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_25_set_monitor_latency_attribute_port")

        switch_init(self.client)

        port = port_list[2]
        port1 = port_list[3]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor latency======")
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid %x ======" %latency_oid)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                for i in range(0, len(microburst_event)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                for i in range(0, len(monitor_discard)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(oid=port1)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        warmboot(self.client)
        try:
            assert(status == SAI_STATUS_INVALID_ATTRIBUTE_0)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid)

class func_26_set_monitor_latency_attribute_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_26_set_monitor_latency_attribute_enable")

        switch_init(self.client)

        port = port_list[2]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor latency======")
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid %x ======" %latency_oid)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                for i in range(0, len(microburst_event)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                for i in range(0, len(monitor_discard)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                    assert(True == a.value.booldata)
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                    assert(False == a.value.booldata)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid)

class func_27_set_monitor_latency_attribute_level_overthrd_event(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_27_set_monitor_latency_attribute_level_overthrd_event")

        switch_init(self.client)

        port = port_list[2]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor latency======")
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid %x ======" %latency_oid)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                for i in range(0, len(microburst_event)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                for i in range(0, len(monitor_discard)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        microburst_event1 = [True, True, True, True, True, True, True, True]
        microburst_event_list = sai_thrift_bool_list_t(count=len(microburst_event1), boollist=microburst_event1)
        attr_value = sai_thrift_attribute_value_t(boollist=microburst_event_list)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                    for i in range(0, len(microburst_event1)):
                        assert(True == a.value.boollist.boollist[i])
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                    for i in range(0, len(monitor_discard)):
                        assert(False == a.value.boollist.boollist[i])

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid)

class func_28_set_monitor_latency_attribute_periodic_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_28_set_monitor_latency_attribute_periodic_enable")

        switch_init(self.client)

        port = port_list[2]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor latency======")
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid %x ======" %latency_oid)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                for i in range(0, len(microburst_event)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                for i in range(0, len(monitor_discard)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        microburst_event1 = [True, True, True, True, True, True, True, True]
        microburst_event_list = sai_thrift_bool_list_t(count=len(microburst_event1), boollist=microburst_event1)
        attr_value = sai_thrift_attribute_value_t(boollist=microburst_event_list)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                    for i in range(0, len(microburst_event1)):
                        assert(True == a.value.boollist.boollist[i])
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                    for i in range(0, len(monitor_discard)):
                        assert(False == a.value.boollist.boollist[i])
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                    assert(True == a.value.booldata)
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                    assert(False == a.value.booldata)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid)

class func_29_set_monitor_latency_attribute_level_discard(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_29_set_monitor_latency_attribute_level_discard")

        switch_init(self.client)

        port = port_list[2]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor latency======")
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid %x ======" %latency_oid)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                for i in range(0, len(microburst_event)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                for i in range(0, len(monitor_discard)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        monitor_discard1 = [True, True, True, True, True, True, True, True]
        monitor_discard_list = sai_thrift_bool_list_t(count=len(monitor_discard1), boollist=monitor_discard1)
        attr_value = sai_thrift_attribute_value_t(boollist=monitor_discard_list)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                    for i in range(0, len(microburst_event)):
                        assert(False == a.value.boollist.boollist[i])
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                    for i in range(0, len(monitor_discard1)):
                        assert(True == a.value.boollist.boollist[i])
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                    assert(True == a.value.booldata)
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                    assert(False == a.value.booldata)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid)

class func_30_set_monitor_latency_attribute_watermark_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_30_set_monitor_latency_attribute_watermark_zero")

        switch_init(self.client)

        port = port_list[2]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor latency======")
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid %x ======" %latency_oid)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                for i in range(0, len(microburst_event)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                for i in range(0, len(monitor_discard)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=0)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK:
                    assert(0 == a.value.u32)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid)

class func_31_set_monitor_latency_attribute_watermark_non_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_31_set_monitor_latency_attribute_watermark_non_zero")

        switch_init(self.client)

        port = port_list[2]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor latency======")
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid %x ======" %latency_oid)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                for i in range(0, len(microburst_event)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                for i in range(0, len(monitor_discard)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        attr_value = sai_thrift_attribute_value_t(u32=1)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK:
                    assert(status == SAI_STATUS_FAILURE)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid)

class func_32_get_monitor_latency_attribute(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_32_get_monitor_latency_attribute")

        switch_init(self.client)

        port = port_list[2]

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port: %x======" %port)
        sys_logging("======create monitor latency======")
        latency_oid = sai_thrift_monitor_create_latency(self.client, port, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid %x ======" %latency_oid)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs
        for a in attrs.attr_list:
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT:
                assert(port == a.value.oid)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                for i in range(0, len(microburst_event)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                for i in range(0, len(monitor_discard)):
                    assert(False == a.value.boollist.boollist[i])
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                assert(False == a.value.booldata)
            if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                assert(False == a.value.booldata)

        microburst_event1 = [True, True, True, True, True, True, True, True]
        microburst_event_list = sai_thrift_bool_list_t(count=len(microburst_event1), boollist=microburst_event1)
        attr_value = sai_thrift_attribute_value_t(boollist=microburst_event_list)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        monitor_discard1 = [True, True, True, True, True, True, True, True]
        monitor_discard_list = sai_thrift_bool_list_t(count=len(monitor_discard1), boollist=monitor_discard1)
        attr_value = sai_thrift_attribute_value_t(boollist=monitor_discard_list)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        attr_value = sai_thrift_attribute_value_t(u32=0)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK, value=attr_value)
        sys_logging("======set monitor latency attr======")
        status = self.client.sai_thrift_set_monitor_latency_attribute(latency_oid, attr)
        sys_logging( "set monitor latency status = %d" %status)

        sys_logging("======get monitor latency attr======")
        attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid)
        sys_logging( "get monitor latency attr status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        print attrs

        warmboot(self.client)
        try:
            for a in attrs.attr_list:
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_OVERTHRD_EVENT:
                    for i in range(0, len(microburst_event)):
                        assert(True == a.value.boollist.boollist[i])
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_LEVEL_DISCARD:
                    for i in range(0, len(monitor_discard1)):
                        assert(True == a.value.boollist.boollist[i])
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE:
                    assert(True == a.value.booldata)
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE:
                    assert(True == a.value.booldata)
                if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK:
                    assert(0 == a.value.u32)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid)

@group('switch_attr')
class func_33_set_switch_buffer_monitor_property_mb_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_33_set_switch_buffer_monitor_property_mb_enable")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_34_set_switch_buffer_monitor_property_mb_total_thrd_min(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_34_set_switch_buffer_monitor_property_mb_total_thrd_min")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(u32=150000)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN = %d======"  %attribute.value.u32)
                    assert ( 150000 == attribute.value.u32 )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_35_set_switch_buffer_monitor_property_mb_total_thrd_max(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_35_set_switch_buffer_monitor_property_mb_total_thrd_max")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(u32=300000)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX = %d======"  %attribute.value.u32)
                    assert ( 300000 == attribute.value.u32 )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_36_set_switch_buffer_monitor_property_mb_level_threshold(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_36_set_switch_buffer_monitor_property_mb_level_threshold")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            value = [0, 2000, 5000, 20000, 400000, 1000000, 5000000, 10000000]
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD:
                    for i in range(0, 8):
                        sys_logging("======index: %d======"  %i)
                        sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD = %d======"  %attribute.value.u32list.u32list[i])
                        assert ( value[i] == attribute.value.u32list.u32list[i] )

            mb_level_threshold = [100, 200, 300, 400, 500, 600, 700, 800]
            mb_level_threshold_list = sai_thrift_u32_list_t(count=len(mb_level_threshold), u32list=mb_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=mb_level_threshold_list)
            sys_logging("======set switch monitor buffer attr======")
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            threshold_value = 100
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD:
                    for i in range(0, 8):
                        sys_logging("======index: %d======"  %i)
                        sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD = %d======"  %attribute.value.u32list.u32list[i])
                        assert ( threshold_value == attribute.value.u32list.u32list[i] )
                        threshold_value += 100

        finally:
            sys_logging("======clean up======")
            mb_level_threshold = [0, 2000, 5000, 20000, 400000, 1000000, 5000000, 10000000]
            mb_level_threshold_list = sai_thrift_u32_list_t(count=len(mb_level_threshold), u32list=mb_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=mb_level_threshold_list)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_37_set_switch_buffer_monitor_property_mb_overthrd_event(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_37_set_switch_buffer_monitor_property_mb_overthrd_event")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT = %d======"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT = %d======"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_38_set_switch_buffer_monitor_property_ingress_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_38_set_switch_buffer_monitor_property_ingress_enable")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_39_set_switch_buffer_monitor_property_egress_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_39_set_switch_buffer_monitor_property_egress_enable")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_40_set_switch_buffer_monitor_property_time_interval(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_40_set_switch_buffer_monitor_property_time_interval")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL = %d======"  %attribute.value.u32)
                    assert ( 1 == attribute.value.u32 )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(u32=100)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL = %d======"  %attribute.value.u32)
                    assert ( 100 == attribute.value.u32 )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u32=1)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_41_set_switch_buffer_monitor_property_ingress_watermark_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_41_set_switch_buffer_monitor_property_ingress_watermark_zero")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_42_set_switch_buffer_monitor_property_ingress_watermark_non_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_42_set_switch_buffer_monitor_property_ingress_watermark_non_zero")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(u32=1)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK , value=attr_value)
            status = self.client.sai_thrift_set_switch_attribute(attr)
            sys_logging( "set switch monitor buffer status = %d" %status)
            assert (status == SAI_STATUS_FAILURE)

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_43_set_switch_buffer_monitor_property_egress_watermark_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_43_set_switch_buffer_monitor_property_egress_watermark_zero")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_44_set_switch_buffer_monitor_property_egress_watermark_non_zero(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_44_set_switch_buffer_monitor_property_egress_watermark_non_zero")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(u32=1)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK , value=attr_value)
            status = self.client.sai_thrift_set_switch_attribute(attr)
            sys_logging( "set switch monitor buffer status = %d" %status)
            assert (status == SAI_STATUS_FAILURE)

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_45_set_switch_latency_monitor_property_threshold_min(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_45_set_switch_latency_monitor_property_threshold_min")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor latency attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

            sys_logging("======set switch monitor latency attr======")
            attr_value = sai_thrift_attribute_value_t(u32=50)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor latency attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN = %d======"  %attribute.value.u32)
                    assert ( 50 == attribute.value.u32 )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_46_set_switch_latency_monitor_property_threshold_max(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_46_set_switch_latency_monitor_property_threshold_max")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor latency attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

            sys_logging("======set switch monitor latency attr======")
            attr_value = sai_thrift_attribute_value_t(u32=100)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor latency attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX = %d======"  %attribute.value.u32)
                    assert ( 100 == attribute.value.u32 )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_47_set_switch_latency_monitor_property_time_interval(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_47_set_switch_latency_monitor_property_time_interval")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor latency attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL = %d======"  %attribute.value.u32)
                    assert ( 1 == attribute.value.u32 )

            sys_logging("======set switch monitor latency attr======")
            attr_value = sai_thrift_attribute_value_t(u32=100)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor latency attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL = %d======"  %attribute.value.u32)
                    assert ( 100 == attribute.value.u32 )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u32=1)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_48_set_switch_latency_monitor_property_level_threshold(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_48_set_switch_latency_monitor_property_level_threshold")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor latency attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            value = [0, 512, 768, 1024, 1280, 1536, 1792, 2048]
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD:
                    for i in range(0, 8):
                        sys_logging("======index: %d======"  %i)
                        sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD = %d======"  %attribute.value.u32list.u32list[i])
                        assert ( value[i] == attribute.value.u32list.u32list[i] )

            #latency_level_threshold = [32, 64, 96, 128, 160, 192, 224, 256]
            latency_level_threshold = [150, 100, 200, 250, 300, 350, 400, 450]
            latency_level_threshold_list = sai_thrift_u32_list_t(count=len(latency_level_threshold), u32list=latency_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=latency_level_threshold_list)
            sys_logging("======set switch monitor latency attr======")
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            latency_level_threshold_value = [128, 96, 192, 224, 288, 320, 384, 448]
            sys_logging("======get switch monitor latency attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD:
                    for i in range(0, 8):
                        sys_logging("======index: %d======"  %i)
                        sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD = %d======"  %attribute.value.u32list.u32list[i])
                        assert ( latency_level_threshold_value[i] == attribute.value.u32list.u32list[i] )

        finally:
            sys_logging("======clean up======")
            mb_level_threshold = [0, 512, 768, 1024, 1280, 1536, 1792, 2048]
            mb_level_threshold_list = sai_thrift_u32_list_t(count=len(mb_level_threshold), u32list=mb_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=mb_level_threshold_list)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_49_get_switch_buffer_monitor_property(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_49_get_switch_buffer_monitor_property")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE, SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN,
                        SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX, SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT,
                        SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD, SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE,
                        SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE, SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL,
                        SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK, SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            value = [0, 2000, 5000, 20000, 400000, 1000000, 5000000, 10000000]
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD:
                    for i in range(0, 8):
                        sys_logging("======index: %d======"  %i)
                        sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD = %d======"  %attribute.value.u32list.u32list[i])
                        assert ( value[i] == attribute.value.u32list.u32list[i] )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT = %d======"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( 0 == attribute.value.booldata )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL = %d======"  %attribute.value.u32)
                    assert ( 1 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=150000)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=300000)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            mb_level_threshold = [100, 200, 300, 400, 500, 600, 700, 800]
            mb_level_threshold_list = sai_thrift_u32_list_t(count=len(mb_level_threshold), u32list=mb_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=mb_level_threshold_list)
            sys_logging("======set switch monitor buffer attr======")
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=100)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging("======get switch monitor buffer attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN = %d======"  %attribute.value.u32)
                    assert ( 150000 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX = %d======"  %attribute.value.u32)
                    assert ( 300000 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD:
                    for i in range(0, 8):
                        sys_logging("======index: %d======"  %i)
                        sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD = %d======"  %attribute.value.u32list.u32list[i])
                        assert ( mb_level_threshold[i] == attribute.value.u32list.u32list[i] )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT = %d======"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE = %d======"  %attribute.value.booldata)
                    assert ( True == attribute.value.booldata )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL = %d======"  %attribute.value.u32)
                    assert ( 100 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            mb_level_threshold = [0, 2000, 5000, 20000, 400000, 1000000, 5000000, 10000000]
            mb_level_threshold_list = sai_thrift_u32_list_t(count=len(mb_level_threshold), u32list=mb_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=mb_level_threshold_list)
            sys_logging("======set switch monitor buffer attr======")
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=1)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

class func_50_get_switch_latency_monitor_property(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("func_50_get_switch_latency_monitor_property")

        switch_init(self.client)

        warmboot(self.client)
        try:
            sys_logging("======get switch monitor latency attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN, SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX, SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL, SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            print attr_list

            value = [0, 512, 768, 1024, 1280, 1536, 1792, 2048]
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX = %d======"  %attribute.value.u32)
                    assert ( 0 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL = %d======"  %attribute.value.u32)
                    assert ( 1 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD:
                    for i in range(0, 8):
                        sys_logging("======index: %d======"  %i)
                        sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD = %d======"  %attribute.value.u32list.u32list[i])
                        assert ( value[i] == attribute.value.u32list.u32list[i] )

            sys_logging("======set switch monitor latency attr======")
            attr_value = sai_thrift_attribute_value_t(u32=50)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=100)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=100)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            latency_level_threshold = [150, 100, 200, 250, 300, 350, 400, 450]
            latency_level_threshold_list = sai_thrift_u32_list_t(count=len(latency_level_threshold), u32list=latency_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=latency_level_threshold_list)
            sys_logging("======set switch monitor latency attr======")
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            latency_level_threshold_value = [128, 96, 192, 224, 288, 320, 384, 448]
            sys_logging("======get switch monitor latency attr======")
            ids_list = [SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN = %d======"  %attribute.value.u32)
                    assert ( 50 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX = %d======"  %attribute.value.u32)
                    assert ( 100 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL:
                    sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL = %d======"  %attribute.value.u32)
                    assert ( 100 == attribute.value.u32 )
                if attribute.id == SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD:
                    for i in range(0, 8):
                        sys_logging("======index: %d======"  %i)
                        sys_logging("======SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD = %d======"  %attribute.value.u32list.u32list[i])
                        assert ( latency_level_threshold_value[i] == attribute.value.u32list.u32list[i] )

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=1)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            mb_level_threshold = [0, 512, 768, 1024, 1280, 1536, 1792, 2048]
            mb_level_threshold_list = sai_thrift_u32_list_t(count=len(mb_level_threshold), u32list=mb_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=mb_level_threshold_list)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

'''
@group('board_test')
class scenario_01_monitor_buffer_stats_and_watermark_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("scenario_01_monitor_buffer_stats_and_watermark_test")
        switch_init(self.client)
        vlan_id = 11
        port1 = port_list[61]
        port2 = port_list[60]
        port3 = port_list[63]
        port4 = port_list[62]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:00:00:00:00:22'
        mac3 = '00:11:11:11:11:12'
        mac4 = '00:11:11:11:11:13'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac3, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac4, port4, mac_action)

        try:
            sys_logging("======port1: %x======" %port1)
            sys_logging("======create monitor buffer======")
            buffer_oid1 = sai_thrift_monitor_create_buffer(self.client, port1)
            sys_logging("======the buffer_oid1: %x ======" %buffer_oid1)

            sys_logging("======port2: %x======" %port2)
            sys_logging("======create monitor buffer======")
            buffer_oid2 = sai_thrift_monitor_create_buffer(self.client, port2)
            sys_logging("======the buffer_oid2: %x ======" %buffer_oid2)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
            sys_logging("======set monitor buffer attr======")
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
            sys_logging("======set monitor buffer attr======")
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
            sys_logging("======set monitor buffer attr======")
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
            sys_logging("======set monitor buffer attr======")
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=5000)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            for i in range(0, 50):
                sys_logging("#################################################################")
                attrs = self.client.sai_thrift_get_monitor_buffer_attribute(buffer_oid2)
                print attrs
                for a in attrs.attr_list:
                    if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_TOTAL_WATERMARK:
                        egress_total_watermark = a.value.u32
                        sys_logging("======egress_total_watermark: %d ======" %egress_total_watermark)
                    if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_UNICAST_WATERMARK:
                        egress_unicast_watermark = a.value.u32
                        sys_logging("======egress_unicast_watermark: %d ======" %egress_unicast_watermark)
                    if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_MULTICAST_WATERMARK:
                        egress_multicast_watermark = a.value.u32
                        sys_logging("======egress_multicast_watermark: %d ======" %egress_multicast_watermark)
                    if a.id == SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_TOTAL_WATERMARK:
                        ingress_total_watermark = a.value.u32
                        sys_logging("======ingress_total_watermark: %d ======" %ingress_total_watermark)

                ids_list = [SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK, SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK]
                switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
                attr_list = switch_attr_list.attr_list
                print attr_list
                for attribute in attr_list:
                    if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_WATERMARK:
                        ingress_watermark = attribute.value.u32
                        sys_logging("======ingress_watermark: %d ======" %ingress_watermark)
                    if attribute.id == SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_WATERMARK:
                        egress_watermark = attribute.value.u32
                        sys_logging("======egress_watermark: %d ======" %egress_watermark)
                sys_logging("#################################################################")
                time.sleep(30)
            pdb.set_trace()
        finally:
            attr_value = sai_thrift_attribute_value_t(u32=1)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_INGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_EGRESS_PORT_PERIODIC_MONITOR_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid2, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_INGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_EGRESS_PERIODIC_MONITOR_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            self.client.sai_thrift_remove_monitor_buffer(buffer_oid1)
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid2)

            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac3, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac4, port4)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_set_port_attribute(port4, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_02_monitor_buffer_mb_monitor_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("scenario_02_monitor_buffer_mb_monitor_test")
        switch_init(self.client)
        vlan_id = 11
        port1 = port_list[61]
        port2 = port_list[60]
        port3 = port_list[63]
        port4 = port_list[62]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:00:00:00:00:22'
        mac3 = '00:11:11:11:11:12'
        mac4 = '00:11:11:11:11:13'
        mac_action = SAI_PACKET_ACTION_FORWARD

        sched_type = SAI_SCHEDULING_TYPE_STRICT
        sched_weight = 10
        sched_oid = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, 0, 0, 10, 0)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac3, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac4, port4, mac_action)

        try:
            sys_logging("======port1: %x======" %port1)
            sys_logging("======create monitor buffer======")
            buffer_oid1 = sai_thrift_monitor_create_buffer(self.client, port1)
            sys_logging("======the buffer_oid1: %x ======" %buffer_oid1)

            sys_logging("======port2: %x======" %port2)
            sys_logging("======create monitor buffer======")
            buffer_oid2 = sai_thrift_monitor_create_buffer(self.client, port2)
            sys_logging("======the buffer_oid2: %x ======" %buffer_oid2)

            sys_logging("======set switch monitor buffer attr======")
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=1000)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid1, attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=2000)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(u32=1000)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid2, attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=2000)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid2, attr)

            attr_value = sai_thrift_attribute_value_t(u32=1000)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=2000)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=5000)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            mb_level_threshold = [0, 2000, 5000, 20000, 400000, 1000000, 5000000, 10000000]
            mb_level_threshold_list = sai_thrift_u32_list_t(count=len(mb_level_threshold), u32list=mb_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=mb_level_threshold_list)
            sys_logging("======set switch monitor buffer attr======")
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            pdb.set_trace()

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            pdb.set_trace()
        finally:
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_ENABLE , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid1, attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MIN, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid2, attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_BUFFER_MONITOR_ATTR_MB_PORT_THRESHOLD_MAX, value=attr_value)
            status = self.client.sai_thrift_set_monitor_buffer_attribute(buffer_oid2, attr)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_TOTAL_THRD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(u32=1)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_TIME_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            mb_level_threshold = [0, 2000, 5000, 20000, 400000, 1000000, 5000000, 10000000]
            mb_level_threshold_list = sai_thrift_u32_list_t(count=len(mb_level_threshold), u32list=mb_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=mb_level_threshold_list)
            sys_logging("======set switch monitor buffer attr======")
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_BUFFER_MONITOR_MB_OVERTHRD_EVENT , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            self.client.sai_thrift_remove_monitor_buffer(buffer_oid1)
            self.client.sai_thrift_remove_monitor_buffer(buffer_oid2)

            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac3, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac4, port4)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_set_port_attribute(port4, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_03_monitor_latency_stats_and_watermark_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_03_monitor_latency_stats_and_watermark_test")

        switch_init(self.client)

        vlan_id = 11
        port1 = port_list[61]
        port2 = port_list[60]
        port3 = port_list[63]
        port4 = port_list[62]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:00:00:00:00:22'
        mac3 = '00:11:11:11:11:12'
        mac4 = '00:11:11:11:11:13'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac3, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac4, port4, mac_action)

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port1: %x======" %port1)
        sys_logging("======create monitor latency======")
        latency_oid1 = sai_thrift_monitor_create_latency(self.client, port1, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid1 %x ======" %latency_oid1)

        sys_logging("======port2: %x======" %port2)
        sys_logging("======create monitor latency again======")
        latency_oid2 = sai_thrift_monitor_create_latency(self.client, port2, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid2 %x ======" %latency_oid2)

        latency_level_threshold = [0, 512, 768, 1024, 1280, 1536, 1792, 2048]
        latency_level_threshold_list = sai_thrift_u32_list_t(count=len(latency_level_threshold), u32list=latency_level_threshold)
        attr_value = sai_thrift_attribute_value_t(u32list=latency_level_threshold_list)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD , value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_PERIODIC_MONITOR_ENABLE, value=attr_value)
        self.client.sai_thrift_set_monitor_latency_attribute(latency_oid2, attr)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE, value=attr_value)
        self.client.sai_thrift_set_monitor_latency_attribute(latency_oid2, attr)

        attr_value = sai_thrift_attribute_value_t(u32=5000)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL , value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        try:
            for i in range(0, 100):
                sys_logging("#################################################################")
                attrs = self.client.sai_thrift_get_monitor_latency_attribute(latency_oid2)
                print attrs
                for a in attrs.attr_list:
                    if a.id == SAI_MONITOR_LATENCY_MONITOR_ATTR_PORT_WATERMARK:
                        latency_watermark = a.value.u32
                        sys_logging("======latency_watermark: %d ======" %latency_watermark)
                sys_logging("#################################################################")
                time.sleep(10)
            pdb.set_trace()

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid1)
            self.client.sai_thrift_remove_monitor_latency(latency_oid2)

            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac3, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac4, port4)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_set_port_attribute(port4, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_04_monitor_latency_mb_monitor_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_04_monitor_latency_mb_monitor_test")

        switch_init(self.client)

        vlan_id = 11
        port1 = port_list[61]
        port2 = port_list[60]
        port3 = port_list[63]
        port4 = port_list[62]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:00:00:00:00:22'
        mac3 = '00:11:11:11:11:12'
        mac4 = '00:11:11:11:11:13'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac3, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac4, port4, mac_action)

        microburst_event = [False, False, False, False, False, False, False, False]
        monitor_discard = [False, False, False, False, False, False, False, False]
        sys_logging("======port1: %x======" %port1)
        sys_logging("======create monitor latency======")
        latency_oid1 = sai_thrift_monitor_create_latency(self.client, port1, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid1 %x ======" %latency_oid1)

        sys_logging("======port2: %x======" %port2)
        sys_logging("======create monitor latency again======")
        latency_oid2 = sai_thrift_monitor_create_latency(self.client, port2, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid2 %x ======" %latency_oid2)

        try:
            latency_level_threshold = [0, 512, 768, 1024, 1280, 1536, 1792, 2048]
            latency_level_threshold_list = sai_thrift_u32_list_t(count=len(latency_level_threshold), u32list=latency_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=latency_level_threshold_list)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE, value=attr_value)
            self.client.sai_thrift_set_monitor_latency_attribute(latency_oid2, attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=512)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=768)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=5000)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            pdb.set_trace()

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid1)
            self.client.sai_thrift_remove_monitor_latency(latency_oid2)

            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac3, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac4, port4)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_set_port_attribute(port4, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class scenario_05_monitor_latency_discard_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_05_monitor_latency_discard_test")

        switch_init(self.client)

        vlan_id = 11
        port1 = port_list[61]
        port2 = port_list[60]
        port3 = port_list[63]
        port4 = port_list[62]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:00:00:00:00:22'
        mac3 = '00:11:11:11:11:12'
        mac4 = '00:11:11:11:11:13'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac3, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac4, port4, mac_action)

        microburst_event = [True, True, True, True, True, True, True, True]
        monitor_discard = [False, False, True, True, False, False, False, False]
        sys_logging("======port1: %x======" %port1)
        sys_logging("======create monitor latency======")
        latency_oid1 = sai_thrift_monitor_create_latency(self.client, port1, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid1 %x ======" %latency_oid1)

        sys_logging("======port2: %x======" %port2)
        sys_logging("======create monitor latency again======")
        latency_oid2 = sai_thrift_monitor_create_latency(self.client, port2, microburst_event = microburst_event, monitor_discard = monitor_discard)
        sys_logging("======the latency_oid2 %x ======" %latency_oid2)

        try:
            latency_level_threshold = [0, 512, 768, 1024, 1280, 1536, 1792, 2048]
            latency_level_threshold_list = sai_thrift_u32_list_t(count=len(latency_level_threshold), u32list=latency_level_threshold)
            attr_value = sai_thrift_attribute_value_t(u32list=latency_level_threshold_list)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_LEVEL_THRESHOLD , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_MONITOR_LATENCY_MONITOR_ATTR_ENABLE, value=attr_value)
            self.client.sai_thrift_set_monitor_latency_attribute(latency_oid2, attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=512)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MIN , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=768)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_THRESHOLD_MAX , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=5000)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_MONITOR_LATENCY_MONITOR_INTERVAL , value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            pdb.set_trace()

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_monitor_latency(latency_oid1)
            self.client.sai_thrift_remove_monitor_latency(latency_oid2)

            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac3, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac4, port4)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_set_port_attribute(port4, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid)
'''