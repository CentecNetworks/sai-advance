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
Thrift SAI interface Scheduler tests
"""
import socket
from switch import *
import sai_base_test
import pdb

@group('Scheduler')
class QueueSchedulerTypeSPSchedulingTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler SP Scheduling Test
        step1:Create Scheduler Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_STRICT
        sched_weight = 0
        cir = 2000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        queueId_list = []

        sched_oid = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid 0x%x"%sched_oid)
        assert(0 != sched_oid)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
        

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type:
                        raise NotImplementedError() 
                #if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                #    sys_logging("Get Scheduler Weight: %d"%a.value.u8)
                #    if a.value.u8 != 1:
                #        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("Get queue Scheduler oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid:
                        raise NotImplementedError() 
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
            self.client.sai_thrift_remove_queue(queueId_list[1])
            self.client.sai_thrift_remove_queue(queueId_list[0])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid)


@group('Scheduler')
class QueueSchedulerTypeDWRRSchedulingTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler WDRR Scheduling Test
        step1:Create Scheduler Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        queueId_list = []

        sched_oid_1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid_1)
        assert(0 != sched_oid_1)
        sched_oid_2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight * 2, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid_2)
        assert(0 != sched_oid_2)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid_1)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    sys_logging("Get Scheduler Weight: %d"%a.value.u8)
                    if a.value.u8 != sched_weight:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("Get queue Scheduler1 oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_1:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[1])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("Get queue Scheduler2 oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
            self.client.sai_thrift_remove_queue(queueId_list[1])
            self.client.sai_thrift_remove_queue(queueId_list[0])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)

@group('Scheduler')
class PortSchedulerSchedulingTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler SP Scheduling Test
        step1:Create Scheduler Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_STRICT
        sched_weight = 0
        cir = 2000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]

        sched_oid = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid 0x%x"%sched_oid)
        assert(0 != sched_oid)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:  
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
                    sys_logging("Get port Scheduler oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid:
                        raise NotImplementedError() 
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port, attr)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid)            

@group('Scheduler')
class QueueSchedulerUpdateWeightTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler WDRR Scheduling Test
        step1:Create Scheduler Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        queueId_list = []

        sched_oid_1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid_1)
        assert(0 != sched_oid_1)
        sched_oid_2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight * 2, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid_2)
        assert(0 != sched_oid_2)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        sched_weight = 50
        attr_value = sai_thrift_attribute_value_t(u8=sched_weight)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, value=attr_value)
        self.client.sai_thrift_set_scheduler_attribute(sched_oid_1, attr)

        attr_value = sai_thrift_attribute_value_t(u8=100)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, value=attr_value)
        self.client.sai_thrift_set_scheduler_attribute(sched_oid_2, attr)        

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid_1)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    sys_logging("Get Scheduler Weight: %d"%a.value.u8)
                    if a.value.u8 != sched_weight:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("Get queue Scheduler1 oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_1:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[1])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("Get queue Scheduler2 oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
            self.client.sai_thrift_remove_queue(queueId_list[1])
            self.client.sai_thrift_remove_queue(queueId_list[0])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)            

@group('Scheduler')
class QueueSchedulerUpdateTypeTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler WDRR Scheduling Test
        step1:Create Scheduler Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        queueId_list = []

        sched_oid_1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid_1)
        assert(0 != sched_oid_1)
        sched_oid_2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight * 2, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid_2)
        assert(0 != sched_oid_2)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        sched_type = SAI_SCHEDULING_TYPE_STRICT
        attr_value = sai_thrift_attribute_value_t(s32=sched_type)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_TYPE, value=attr_value)
        self.client.sai_thrift_set_scheduler_attribute(sched_oid_1, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid_1)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    sys_logging("Get Scheduler Weight: %d"%a.value.u8)
                    if a.value.u8 != sched_weight:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("Get queue Scheduler1 oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_1:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[1])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("Get queue Scheduler2 oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
            self.client.sai_thrift_remove_queue(queueId_list[1])
            self.client.sai_thrift_remove_queue(queueId_list[0])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)              

class fun_01_create_2_types_scheduler_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        step1:Create two types Scheduler Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[1]
        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 2000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        queueId_list = []

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, 0, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid1)

        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, 0, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid2)

        sched_oid3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_3 0x%x"%sched_oid3)

        sched_oid4 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_4 0x%x"%sched_oid4)

        warmboot(self.client)
        try:
            assert(0x16 == sched_oid1%0x100000000)
            assert(0x16 == sched_oid2%0x100000000)
            assert(0x16 == sched_oid3%0x100000000)
            assert(0x16 == sched_oid4%0x100000000)
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid1)
            sys_logging("Get sched_oid1 attribute status = %d"%attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid2)
            sys_logging("Get sched_oid2 attribute status = %d"%attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid3)
            sys_logging("Get sched_oid3 attribute status = %d"%attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid4)
            sys_logging("Get sched_oid4 attribute status = %d"%attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)


        finally:
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)


class fun_02_remove_2_types_scheduler_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        step1:Create two types Scheduler Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[1]
        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 2000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        queueId_list = []

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, 0, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid1)

        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid2)

        warmboot(self.client)
        try:            
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid1)
            sys_logging("Get sched_oid1 attribute status = %d"%attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid2)
            sys_logging("Get sched_oid2 attribute status = %d"%attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)

            status=self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            sys_logging("remove sched_oid1 status = %d"%status)
            assert(status == SAI_STATUS_SUCCESS)
            status=self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            sys_logging("remove sched_oid1 status = %d"%status)
            assert(status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid1)
            sys_logging("Get sched_oid1 attribute status = %d"%attrs.status)
            assert(attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid2)
            sys_logging("Get sched_oid2 attribute status = %d"%attrs.status)
            assert(attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            pass


class fun_03_remove_in_use_scheduler_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler SP Scheduling Test
        step1:Create Scheduler Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_STRICT
        sched_weight = 0
        cir = 2000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        queueId_list = []

        sched_oid = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid 0x%x"%sched_oid)
        assert(0 != sched_oid)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
        

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)

        warmboot(self.client)
        try:
            status=self.client.sai_thrift_remove_scheduler_profile(sched_oid)
            sys_logging("remove sched_oid status = %d"%status)
            assert(status == SAI_STATUS_OBJECT_IN_USE)

            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

            status=self.client.sai_thrift_remove_scheduler_profile(sched_oid)
            sys_logging("remove sched_oid status = %d"%status)
            assert(status == SAI_STATUS_OBJECT_IN_USE)

            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)

            status=self.client.sai_thrift_remove_scheduler_profile(sched_oid)
            sys_logging("remove sched_oid status = %d"%status)
            assert(status == SAI_STATUS_SUCCESS)
            
        finally:
            self.client.sai_thrift_remove_queue(queueId_list[1])
            self.client.sai_thrift_remove_queue(queueId_list[0])


class fun_04_set_and_get_scheduler_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight1 = 10
        sched_weight2 = 20
        cir = 2000000
        cir2 = 2500000
        cbs = 256000
        cbs2 = 356000
        pir = 1000000
        pir2 = 1500000
        pbs = 64000
        pbs2 = 74000

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid1)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid1)
            sys_logging('get scheduler attribute status = %d'%attrs.status)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type1:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    sys_logging("Get Scheduler Weight: %d"%a.value.u8)
                    if a.value.u8 != sched_weight1:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_METER_TYPE:
                    sys_logging("Get Scheduler meter type: %d"%a.value.s32)
                    if a.value.s32 != SAI_METER_TYPE_BYTES:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 


            attr_value = sai_thrift_attribute_value_t(s32=sched_type2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_TYPE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(u8=sched_weight2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=cir2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=cbs2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=pir2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=pbs2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)
            
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid1)
            sys_logging('get scheduler attribute status = %d'%attrs.status)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    sys_logging("Get Scheduler Weight: %d"%a.value.u8)
                    if a.value.u8 != sched_weight2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_METER_TYPE:
                    sys_logging("Get Scheduler meter type: %d"%a.value.s32)
                    if a.value.s32 != SAI_METER_TYPE_BYTES:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != cir2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != cbs2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != pir2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != pbs2:
                        raise NotImplementedError() 

        finally:

            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)

class fun_05_set_scheduler_attr_type_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 64, 8]
        sched_group_id_group_node = [None]*8
        queueId_list = []

        
        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        sched_group_id_chan_node = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        
        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)      
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)      
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)

        
        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

        sys_logging("=======set queue parent node profile=======")
        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[0])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[1])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[3])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[3], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[4])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[4], attr)
        
        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[5])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[5], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[6])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[6], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[7])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[7], attr)


        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        sched_weight1 = 20
        cir = 2000000
        cbs = 256000
        pir = 1000000
        pbs = 64000

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, 0, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid1)

        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid2)

        sched_oid3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight1, cir, cbs, pir, pbs)
        sys_logging("sched_oid_3 0x%x"%sched_oid3)

        sys_logging("=======set queue scheduler profile=======")
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid3)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)
        

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[3], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[4], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[5], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[6], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[7], attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid2)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler2 Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type2:
                        raise NotImplementedError() 
            
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid3)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler3 Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type2:
                        raise NotImplementedError() 

            attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[2])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)
            
            attr_value = sai_thrift_attribute_value_t(s32=sched_type1)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_TYPE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid3, attr)

            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid3)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler3 Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type1:
                        raise NotImplementedError() 
                       
            attr_value = sai_thrift_attribute_value_t(s32=sched_type1)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_TYPE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid2, attr)

            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid2)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler2 Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type1:
                        raise NotImplementedError() 
            
            #pdb.set_trace() 
            attr_value = sai_thrift_attribute_value_t(s32=sched_type2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_TYPE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid3, attr)

            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid3)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler3 Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type2:
                        raise NotImplementedError() 
            #pdb.set_trace()            
            attr_value = sai_thrift_attribute_value_t(s32=sched_type2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_TYPE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid2, attr)

            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid2)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    sys_logging("Get Scheduler2 Type: %d"%a.value.s32)
                    if a.value.s32 != sched_type2:
                        raise NotImplementedError() 

            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[1])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)
                        
        finally:
            #pdb.set_trace()
            for i in range(8):
                self.client.sai_thrift_remove_queue(queueId_list[i])
            
            for ii in range(8):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)



class fun_06_set_scheduler_attr_weight_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 64, 8]
        sched_group_id_group_node = [None]*8
        queueId_list = []

        
        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        sched_group_id_chan_node = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        
        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)      
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)      
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0)

        
        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

        sys_logging("=======set queue parent node profile=======")
        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[0])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[1])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[3], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[4], attr)
        
        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[5])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[5], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[6])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[6], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[7])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[7], attr)


        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        sched_weight1 = 20
        sched_weight2 = 15
        cir = 2000000
        cbs = 256000
        pir = 1000000
        pbs = 64000

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, 0, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid1)

        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid2)

        sched_oid3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight1, cir, cbs, pir, pbs)
        sys_logging("sched_oid_3 0x%x"%sched_oid3)

        sched_oid4 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight2, cir, cbs, pir, pbs)
        sys_logging("sched_oid_4 0x%x"%sched_oid4)

        sys_logging("=======set queue scheduler profile=======")
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid3)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[3], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid4)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[4], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[5], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[6], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[7], attr)



        attr_value = sai_thrift_attribute_value_t(oid=sched_oid3)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[0], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[2], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[3], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[4], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[5], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[6], attr)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[7], attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid2)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    sys_logging("Get Scheduler2 Type: %d"%a.value.u8)
                    if a.value.u8 != sched_weight:
                        raise NotImplementedError() 
            
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid3)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    sys_logging("Get Scheduler3 Type: %d"%a.value.u8)
                    if a.value.u8 != sched_weight1:
                        raise NotImplementedError() 

            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(u8=sched_weight)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid3, attr)

            attr_value = sai_thrift_attribute_value_t(u8=sched_weight1)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid2, attr)

            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid2)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    sys_logging("Get Scheduler2 Type: %d"%a.value.u8)
                    if a.value.u8 != sched_weight1:
                        raise NotImplementedError() 
            
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid3)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    sys_logging("Get Scheduler3 Type: %d"%a.value.u8)
                    if a.value.u8 != sched_weight:
                        raise NotImplementedError()

                        
        finally:
            #pdb.set_trace()
            for i in range(8):
                self.client.sai_thrift_remove_queue(queueId_list[i])
          
            for ii in range(8):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)


class fun_07_set_bind_port_scheduler_shape_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]

        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_weight1 = 10
        cir = 2000000
        cbs = 256000
        pir = 900000000
        pir2 = 90000000
        pbs = 64000
        pbs2 = 74000
        

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_port_attribute(port1)
            for a in attrs.attr_list:  
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
                    sys_logging("Get port Scheduler oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_port_attribute(port2)
            for a in attrs.attr_list:  
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
                    sys_logging("Get port Scheduler oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_port_attribute(port3)
            for a in attrs.attr_list:  
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
                    sys_logging("Get port Scheduler oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError() 
                        
            attrs = self.client.sai_thrift_get_port_attribute(port4)
            for a in attrs.attr_list:  
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
                    sys_logging("Get port Scheduler oid: 0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError() 
            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(u64=pir2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=pbs2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)

            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != pir2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != pbs2:
                        raise NotImplementedError() 

            sys_logging('======remove scheduler before remove port scheduler profile======')            
            status =self.client.sai_thrift_remove_scheduler_profile(sched_oid1) 
            sys_logging("remove Scheduler status: %d"%status)
            assert(status==SAI_STATUS_OBJECT_IN_USE)
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_set_port_attribute(port4, attr)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)  



class fun_08_set_bind_queue_scheduler_attr_cir_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 64, 8]
        sched_group_id_group_node = [None]*8
        sched_group_id_group_node1 = [None]*8
        sched_group_id_group_node2 = [None]*8
        sched_group_id_chan_node = [None]*4
        sched_group_service_id = 1
        sched_group_service_id2 = 2
        queueId_list = []
        service_queueId = [None]*8
        service_queueId2 = [None]*8


        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight1 = 10
        sched_weight2 = 20
        cir = 2000000
        cir2 = 2500000
        cbs = 256000
        cbs2 = 356000
        pir = 1000000
        pir2 = 1500000
        pbs = 64000
        pbs2 = 74000

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid1)

        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight2, cir2, cbs2, pir2, pbs2)
        sys_logging("sched_oid_1 0x%x"%sched_oid2)

        
        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        sched_group_id_chan_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        sched_group_id_chan_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        
        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)      
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)      
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)


        sched_group_id_group_node1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id)      
        sched_group_id_group_node1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id)      
        sched_group_id_group_node1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id)


        sched_group_id_group_node2[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id2)      
        sched_group_id_group_node2[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id2)
        sched_group_id_group_node2[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id2)
        sched_group_id_group_node2[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id2)
        sched_group_id_group_node2[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id2)      
        sched_group_id_group_node2[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id2)
        sched_group_id_group_node2[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id2)
        sched_group_id_group_node2[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id2)

        
        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
        sys_logging("=======set queue parent node profile=======")
        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[0])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[1])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[3])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[3], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[4])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[4], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[5], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[6], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[7])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[7], attr)
        
        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=sched_group_id_group_node1[0], service_id=sched_group_service_id)        
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=sched_group_id_group_node1[1], service_id=sched_group_service_id)
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=sched_group_id_group_node1[1], service_id=sched_group_service_id)
        service_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=sched_group_id_group_node1[3], service_id=sched_group_service_id)
        service_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=sched_group_id_group_node1[4], service_id=sched_group_service_id)
        service_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=sched_group_id_group_node1[4], service_id=sched_group_service_id)
        service_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=sched_group_id_group_node1[4], service_id=sched_group_service_id)
        service_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=sched_group_id_group_node1[7], service_id=sched_group_service_id)

        service_queueId2[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=sched_group_id_group_node2[0], service_id=sched_group_service_id2)        
        service_queueId2[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=sched_group_id_group_node2[1], service_id=sched_group_service_id2)
        service_queueId2[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=sched_group_id_group_node2[1], service_id=sched_group_service_id2)
        service_queueId2[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=sched_group_id_group_node2[3], service_id=sched_group_service_id2)
        service_queueId2[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=sched_group_id_group_node2[4], service_id=sched_group_service_id2)
        service_queueId2[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=sched_group_id_group_node2[4], service_id=sched_group_service_id2)
        service_queueId2[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=sched_group_id_group_node2[4], service_id=sched_group_service_id2)
        service_queueId2[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=sched_group_id_group_node2[7], service_id=sched_group_service_id2)

        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(oid=sched_oid2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[4], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[5], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[6], attr)

            self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)

            self.client.sai_thrift_set_queue_attribute(service_queueId2[1], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId2[2], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId2[4], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId2[5], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId2[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_oid1)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[3], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[7], attr)

            self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)

            self.client.sai_thrift_set_queue_attribute(service_queueId2[0], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId2[3], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId2[7], attr)

            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(u64=cir2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=cbs2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=pir2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=pbs2)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid1, attr)



            attr_value = sai_thrift_attribute_value_t(u64=cir)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=cbs)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=pir)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=pbs)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid2, attr)

            
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid1)
            sys_logging('get scheduler attribute status = %d'%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != cir2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != cbs2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != pir2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != pbs2:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid2)
            sys_logging('get scheduler attribute status = %d'%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64)
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    sys_logging("Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64)
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
        finally:
            #pdb.set_trace()
            for i in range(8):
                self.client.sai_thrift_remove_queue(queueId_list[i])
                self.client.sai_thrift_remove_queue(service_queueId[i])
                self.client.sai_thrift_remove_queue(service_queueId2[i])

            for ii in range(8):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node1[ii])
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node2[ii])
            for i in range(4):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[i])
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
            
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)         
                        



