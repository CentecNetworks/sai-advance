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

