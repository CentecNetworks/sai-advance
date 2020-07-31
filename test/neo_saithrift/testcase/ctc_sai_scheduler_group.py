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
Thrift SAI interface Buffer tests
"""
import socket
from switch import *
import sai_base_test
import pdb

@group('Scheduler Group')
class QueueSchedulerGroupBindTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
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
        level = [0,1,2]
        max_childs = [4, 64, 8]
        parent_id = [port, None, None, None]
        sched_group_id_root = [None]*1
        sched_group_id_chan_node = [None]*2
        sched_group_id_group_node = [None]*3

        #port level
        sched_group_id_root[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        sys_logging("sched_group_id_root[0]=0x%x"%sched_group_id_root[0])
        assert(0 != sched_group_id_root[0])
        
        #channel node level
        parent_id[1] = sched_group_id_root[0]
        
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        assert(0 != sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])
        assert(0 != sched_group_id_chan_node[1])
        
        #group node level
        parent_id[2] = sched_group_id_chan_node[0]
        
        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[0], 0)
        sys_logging("sched_group_id_group_node[0]=0x%x"%sched_group_id_group_node[0])
        assert(0 != sched_group_id_group_node[0])
        
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0)
        sys_logging("sched_group_id_group_node[1]=0x%x"%sched_group_id_group_node[1])
        assert(0 != sched_group_id_group_node[1])
        
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0)
        sys_logging("sched_group_id_group_node[2]=0x%x"%sched_group_id_group_node[2])
        assert(0 != sched_group_id_group_node[2])        
        

        queueId_list = []
        sched_oid_1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid_1)
        assert(0 != sched_oid_1)
        
        sched_weight2 = 20
        sched_oid_2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight2, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid_2)
        assert(0 != sched_oid_2)
        
        sched_weight3 = 30
        sched_oid_3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight3, cir, cbs, pir, pbs)
        sys_logging("sched_oid_3 0x%x"%sched_oid_3)
        assert(0 != sched_oid_3)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                    attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                    
                    attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[i%3])
                    sys_logging("bind sched group:0x%X"%sched_group_id_group_node[i%3])
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
        
        #chan node weight
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_chan_node[0], attr)  
        
        #group node weight
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_3)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[0], attr)          

        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                        sys_logging("Get queue[0x%x] Scheduler Group oid: 0x%x"%(queueId_list[ii], a.value.oid))
                        if a.value.oid != sched_group_id_group_node[ii%3]:
                            raise NotImplementedError() 

            sys_logging("Verfy Sched Group[0x%x] Attrs!"%sched_group_id_chan_node[0])
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id_chan_node[0])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    sys_logging("#Get Levle:", a.value.u8)
                    if a.value.u8 != level[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    sys_logging("#Get Max Childs:", a.value.u8)
                    if a.value.u8 != max_childs[1]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                    if a.value.oid != parent_id[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        if a.value.objlist.object_id_list[o_i] != sched_group_id_group_node[o_i%1]:
                            raise NotImplementedError()       
        finally:
            for ii in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                self.client.sai_thrift_remove_queue(queueId_list[ii])
                
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_chan_node[0], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[0], attr)
            
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_3)

@group('Scheduler Group')
class QueueSchedulerGroupUpdateParentTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue & Update Parent Node Test
        step1:Create Scheduler Group Id
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
        level = [0,1,2]
        max_childs = [4, 64, 8]
        parent_id = [port, None, None, None]
        sched_group_id_root = [None]*1
        sched_group_id_chan_node = [None]*2
        sched_group_id_group_node = [None]*3

        #port level
        sched_group_id_root[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        sys_logging("sched_group_id_root[0]=0x%x"%sched_group_id_root[0])
        assert(0 != sched_group_id_root[0])
        
        #channel node level
        parent_id[1] = sched_group_id_root[0]
        
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        assert(0 != sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])
        assert(0 != sched_group_id_chan_node[1])
        
        #group node level
        parent_id[2] = sched_group_id_chan_node[0]
        
        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[0], 0)
        sys_logging("sched_group_id_group_node[0]=0x%x"%sched_group_id_group_node[0])
        assert(0 != sched_group_id_group_node[0])
        
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0)
        sys_logging("sched_group_id_group_node[1]=0x%x"%sched_group_id_group_node[1])
        assert(0 != sched_group_id_group_node[1])
        
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0)
        sys_logging("sched_group_id_group_node[2]=0x%x"%sched_group_id_group_node[2])
        assert(0 != sched_group_id_group_node[2])        
        

        queueId_list = []
        sched_oid_1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid_1)
        assert(0 != sched_oid_1)
        
        sched_weight2 = 20
        sched_oid_2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight2, cir, cbs, pir, pbs)
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
                    attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                    
                    attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[i%3])
                    sys_logging("bind sched group:0x%X"%sched_group_id_group_node[i%3])
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
        
        #group node weight
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[0], attr)
        
        sys_logging("update sched_group_id_group_node[0] parent node, from sched_group_id_chan_node[0] to sched_group_id_chan_node[1]")
        #update sched_group_id_group_node[0] parent node, from sched_group_id_chan_node[0] to sched_group_id_chan_node[1]
        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_chan_node[1])
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[0], attr)
        
        warmboot(self.client)
        try:
            sys_logging("Verfy Sched Group[0x%x] Attrs!"%sched_group_id_group_node[0])
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id_group_node[0])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_chan_node[1]:
                        raise NotImplementedError()

            sys_logging("Verfy Sched Group[0x%x] Attrs!"%sched_group_id_chan_node[1])
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id_chan_node[1])
            for a in attrs.attr_list:        
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 3:
                        raise NotImplementedError()       
        finally:
            for ii in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                self.client.sai_thrift_remove_queue(queueId_list[ii])
                
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[0], attr)
            
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)


@group('Scheduler Group')
class PortGetSchedulerGroupListTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue & Get Port Sched Group List Test
        step1:Create Scheduler Group Id
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
        level = [0,1,2]
        max_childs = [4, 64, 8]
        parent_id = [port, None, None, None]
        sched_group_id_root = [None]*1
        sched_group_id_chan_node = [None]*2
        sched_group_id_group_node = [None]*3

        #port level
        sched_group_id_root[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        sys_logging("sched_group_id_root[0]=0x%x"%sched_group_id_root[0])
        assert(0 != sched_group_id_root[0])
        
        #channel node level
        parent_id[1] = sched_group_id_root[0]
        
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        assert(0 != sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])
        assert(0 != sched_group_id_chan_node[1])
        
        #group node level
        parent_id[2] = sched_group_id_chan_node[0]
        
        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[0], 0)
        sys_logging("sched_group_id_group_node[0]=0x%x"%sched_group_id_group_node[0])
        assert(0 != sched_group_id_group_node[0])
        
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0)
        sys_logging("sched_group_id_group_node[1]=0x%x"%sched_group_id_group_node[1])
        assert(0 != sched_group_id_group_node[1])
        
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0)
        sys_logging("sched_group_id_group_node[2]=0x%x"%sched_group_id_group_node[2])
        assert(0 != sched_group_id_group_node[2])        
        

        queueId_list = []
        sched_oid_1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid_1)
        assert(0 != sched_oid_1)
        
        sched_weight2 = 20
        sched_oid_2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight2, cir, cbs, pir, pbs)
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
                    attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                    
                    attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[i%3])
                    sys_logging("bind sched group:0x%X"%sched_group_id_group_node[i%3])
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)

        #chan node weight
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_chan_node[0], attr)

        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                        sys_logging("Get queue[0x%x] Scheduler Group oid: 0x%x"%(queueId_list[ii], a.value.oid))
                        if a.value.oid != sched_group_id_group_node[ii%3]:
                            raise NotImplementedError() 

            sys_logging("Verfy Sched Group[0x%x] Attrs!"%sched_group_id_chan_node[0])
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id_chan_node[0])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    sys_logging("#Get Levle:", a.value.u8)
                    if a.value.u8 != level[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    sys_logging("#Get Max Childs:", a.value.u8)
                    if a.value.u8 != max_childs[1]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                    if a.value.oid != parent_id[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        if a.value.objlist.object_id_list[o_i] != sched_group_id_group_node[o_i%1]:
                            raise NotImplementedError()

            sys_logging("Get Port[0x%x] Sched Group List!"%port)
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:           
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST:
                    for i in range(a.value.objlist.count):
                        sys_logging(">> Sched Group List[%d]:0x%x"%(i, a.value.objlist.object_id_list[i]))
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS:
                    sys_logging("Sched Group Count:", a.value.u32)
                    if 6 != a.value.u32:
                        raise NotImplementedError()         
        finally:
            for ii in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                self.client.sai_thrift_remove_queue(queueId_list[ii])
                
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_chan_node[0], attr)
            
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1) 
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2) 


@group('Scheduler Group')
class QueueSchedulerGroupUpdateSchedulerWeightTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue & Bind Scheduler & Update Weight
        step1:Create Scheduler Group Id & Bind Scheduler & Update Weight
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
        level = [0,1,2]
        max_childs = [4, 64, 8]
        parent_id = [port, None, None, None]
        sched_group_id_root = [None]*1
        sched_group_id_chan_node = [None]*2
        sched_group_id_group_node = [None]*3

        #port level
        sched_group_id_root[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        sys_logging("sched_group_id_root[0]=0x%x"%sched_group_id_root[0])
        assert(0 != sched_group_id_root[0])
        
        #channel node level
        parent_id[1] = sched_group_id_root[0]
        
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        assert(0 != sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])
        assert(0 != sched_group_id_chan_node[1])
        
        #group node level
        parent_id[2] = sched_group_id_chan_node[0]
        
        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[0], 0)
        sys_logging("sched_group_id_group_node[0]=0x%x"%sched_group_id_group_node[0])
        assert(0 != sched_group_id_group_node[0])
        
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0)
        sys_logging("sched_group_id_group_node[1]=0x%x"%sched_group_id_group_node[1])
        assert(0 != sched_group_id_group_node[1])
        
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0)
        sys_logging("sched_group_id_group_node[2]=0x%x"%sched_group_id_group_node[2])
        assert(0 != sched_group_id_group_node[2])        
        

        queueId_list = []
        sched_oid_1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid_1)
        assert(0 != sched_oid_1)
        
        sched_weight2 = 20
        sched_oid_2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight2, cir, cbs, pir, pbs)
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
                    attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                    
                    attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[i%3])
                    sys_logging("bind sched group:0x%X"%sched_group_id_group_node[i%3])
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)

        #group node weight
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)     
        
        sched_weight = 50
        attr_value = sai_thrift_attribute_value_t(u8=sched_weight)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, value=attr_value)
        self.client.sai_thrift_set_scheduler_attribute(sched_oid_2, attr)  

        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                        sys_logging("Get queue[0x%x] Scheduler Group oid: 0x%x"%(queueId_list[ii], a.value.oid))
                        if a.value.oid != sched_group_id_group_node[ii%3]:
                            raise NotImplementedError() 

            sys_logging("Verfy Sched Group[0x%x] Attrs!"%sched_group_id_group_node[1])
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id_group_node[1])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    sys_logging("#Get Levle:", a.value.u8)
                    if a.value.u8 != level[2]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    sys_logging("#Get Max Childs:", a.value.u8)
                    if a.value.u8 != max_childs[2]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_chan_node[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 3:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        #if a.value.objlist.object_id_list[o_i] != sched_group_id_group_node[o_i%1]:
                        #    raise NotImplementedError()

            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid_2)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    sys_logging("Get Scheduler Weight: %d"%a.value.u8)
                    if a.value.u8 != sched_weight:
                        raise NotImplementedError() 
        finally:
            for ii in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                self.client.sai_thrift_remove_queue(queueId_list[ii])
                
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)
            
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1) 
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2) 
         

class QueueSchedulerGroupServiceGroupBindTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
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
        level = [0,1,2]
        max_childs = [4, 64, 8]
        parent_id = [port, None, None, None]
        sched_group_id_root = [None]*1
        sched_group_id_chan_node = [None]*2
        sched_group_id_group_node = [None]*3
        sched_group_service_id = 1
        service_queueId = [None]*3

        #port level
        sched_group_id_root[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        sys_logging("sched_group_id_root[0]=0x%x"%sched_group_id_root[0])
        assert(0 != sched_group_id_root[0])
        
        #channel node level
        parent_id[1] = sched_group_id_root[0]
        
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        assert(0 != sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])
        assert(0 != sched_group_id_chan_node[1])
        
        #service group node level
        parent_id[2] = sched_group_id_chan_node[0]

        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[0], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[0]=0x%x"%sched_group_id_group_node[0])
        assert(0 != sched_group_id_group_node[0])
        
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[1]=0x%x"%sched_group_id_group_node[1])
        assert(0 != sched_group_id_group_node[1])
        
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[2]=0x%x"%sched_group_id_group_node[2])
        assert(0 != sched_group_id_group_node[2])
        
        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = 0
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[0], service_id=sched_group_service_id)
        sys_logging("service_queueId[0]=0x%x"%service_queueId[0])
        
        queue_index = 1
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id)
        sys_logging("service_queueId[1]=0x%x"%service_queueId[1])
        
        queue_index = 2
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[2], service_id=sched_group_service_id)
        sys_logging("service_queueId[2]=0x%x"%service_queueId[2])
        

        queueId_list = []
        sched_oid_1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid_1)
        assert(0 != sched_oid_1)
        
        sched_weight2 = 20
        sched_oid_2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight2, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid_2)
        assert(0 != sched_oid_2)
        
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)        

        
        #service group node weight
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)          

        warmboot(self.client)
        try:
            for ii in range(3):
                attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                        sys_logging("Get queue[0x%x] Scheduler Group oid: 0x%x"%(service_queueId[ii], a.value.oid))
                        if a.value.oid != sched_group_id_group_node[ii]:
                            raise NotImplementedError()             

            sys_logging("Verfy Sched Group[0x%x] Attrs!"%sched_group_id_group_node[1])
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id_group_node[1])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    sys_logging("#Get Levle:", a.value.u8)
                    if a.value.u8 != level[2]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    sys_logging("#Get Max Childs:", a.value.u8)
                    if a.value.u8 != max_childs[2]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_chan_node[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        if a.value.objlist.object_id_list[o_i] != service_queueId[1]:
                            raise NotImplementedError()       
        finally:
            for ii in range(3):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)
                self.client.sai_thrift_remove_queue(service_queueId[ii])
                
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)
            
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)
            
class QueueSchedulerGroupServiceGroupGetQueueListAndGroupOnPort(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
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
        level = [0,1,2]
        max_childs = [4, 64, 8]
        parent_id = [port, None, None, None]
        sched_group_id_root = [None]*1
        sched_group_id_chan_node = [None]*2
        sched_group_id_group_node = [None]*3
        sched_group_service_id = 1
        service_queueId = [None]*3

        #port level
        sched_group_id_root[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        sys_logging("sched_group_id_root[0]=0x%x"%sched_group_id_root[0])
        assert(0 != sched_group_id_root[0])
        
        #channel node level
        parent_id[1] = sched_group_id_root[0]
        
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        assert(0 != sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])
        assert(0 != sched_group_id_chan_node[1])
        
        #service group node level
        parent_id[2] = sched_group_id_chan_node[0]

        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[0], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[0]=0x%x"%sched_group_id_group_node[0])
        assert(0 != sched_group_id_group_node[0])
        
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[1]=0x%x"%sched_group_id_group_node[1])
        assert(0 != sched_group_id_group_node[1])
        
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[2]=0x%x"%sched_group_id_group_node[2])
        assert(0 != sched_group_id_group_node[2])
        
        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = 0
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[0], service_id=sched_group_service_id)
        sys_logging("service_queueId[0]=0x%x"%service_queueId[0])
        
        queue_index = 1
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id)
        sys_logging("service_queueId[1]=0x%x"%service_queueId[1])
        
        queue_index = 2
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[2], service_id=sched_group_service_id)
        sys_logging("service_queueId[2]=0x%x"%service_queueId[2])
        

        queueId_list = []
        sched_oid_1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid_1)
        assert(0 != sched_oid_1)
        
        sched_weight2 = 20
        sched_oid_2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight2, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid_2)
        assert(0 != sched_oid_2)
        
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)        

        
        #service group node weight
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)          

        warmboot(self.client)
        try:
            for ii in range(3):
                attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                        sys_logging("Get queue[0x%x] Scheduler Group oid: 0x%x"%(service_queueId[ii], a.value.oid))
                        if a.value.oid != sched_group_id_group_node[ii]:
                            raise NotImplementedError()             

            sys_logging("Verfy Sched Group[0x%x] Attrs!"%sched_group_id_group_node[1])
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id_group_node[1])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    sys_logging("#Get Levle:", a.value.u8)
                    if a.value.u8 != level[2]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    sys_logging("#Get Max Childs:", a.value.u8)
                    if a.value.u8 != max_childs[2]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_chan_node[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        if a.value.objlist.object_id_list[o_i] != service_queueId[1]:
                            raise NotImplementedError()
                            
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:  
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    if a.value.u32 != (8+8):
                        raise NotImplementedError()
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                        
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS:
                    sys_logging("queue number:%d"%a.value.u32)
                    if a.value.u32 != 6:
                        raise NotImplementedError()
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST:
                    for i in range(a.value.objlist.count):
                        sys_logging("sched_group_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
            
            
        finally:
            for ii in range(3):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)
                self.client.sai_thrift_remove_queue(service_queueId[ii])
                
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)
            
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)
            
class QueueSchedulerGroupServiceGroupUpdateParentTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
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
        level = [0,1,2]
        max_childs = [4, 64, 8]
        parent_id = [port, None, None, None]
        sched_group_id_root = [None]*1
        sched_group_id_chan_node = [None]*2
        sched_group_id_group_node = [None]*3
        sched_group_service_id = 1
        service_queueId = [None]*3

        #port level
        sched_group_id_root[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        sys_logging("sched_group_id_root[0]=0x%x"%sched_group_id_root[0])
        assert(0 != sched_group_id_root[0])
        
        #channel node level
        parent_id[1] = sched_group_id_root[0]
        
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        assert(0 != sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])
        assert(0 != sched_group_id_chan_node[1])
        
        #service group node level
        parent_id[2] = sched_group_id_chan_node[0]

        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[0], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[0]=0x%x"%sched_group_id_group_node[0])
        assert(0 != sched_group_id_group_node[0])
        
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[1]=0x%x"%sched_group_id_group_node[1])
        assert(0 != sched_group_id_group_node[1])
        
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[2]=0x%x"%sched_group_id_group_node[2])
        assert(0 != sched_group_id_group_node[2])
        
        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = 0
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[0], service_id=sched_group_service_id)
        sys_logging("service_queueId[0]=0x%x"%service_queueId[0])
        
        queue_index = 1
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id)
        sys_logging("service_queueId[1]=0x%x"%service_queueId[1])
        
        queue_index = 2
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[2], service_id=sched_group_service_id)
        sys_logging("service_queueId[2]=0x%x"%service_queueId[2])
        

        queueId_list = []
        sched_oid_1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid_1)
        assert(0 != sched_oid_1)
        
        sched_weight2 = 20
        sched_oid_2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight2, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid_2)
        assert(0 != sched_oid_2)
        
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)        

        #service group node weight
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)        
        
        sys_logging("update sched_group_id_group_node[1] parent node, from sched_group_id_chan_node[1] to sched_group_id_chan_node[0]")
        #update sched_group_id_group_node[1] parent node, from sched_group_id_chan_node[1] to sched_group_id_chan_node[0]
        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_chan_node[0])
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)

        warmboot(self.client)
        try:
            for ii in range(3):
                attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                        sys_logging("Get queue[0x%x] Scheduler Group oid: 0x%x"%(service_queueId[ii], a.value.oid))
                        if a.value.oid != sched_group_id_group_node[ii]:
                            raise NotImplementedError()             

            sys_logging("Verfy Sched Group[0x%x] Attrs!"%sched_group_id_group_node[1])
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id_group_node[1])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    sys_logging("#Get Levle:", a.value.u8)
                    if a.value.u8 != level[2]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    sys_logging("#Get Max Childs:", a.value.u8)
                    if a.value.u8 != max_childs[2]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_chan_node[0]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        if a.value.objlist.object_id_list[o_i] != service_queueId[1]:
                            raise NotImplementedError()       
        finally:
            for ii in range(3):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)
                self.client.sai_thrift_remove_queue(service_queueId[ii])
                
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)
            
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)
            
class QueueSchedulerGroupServiceGroupBridgePortBindTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
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
        level = [0,1,2]
        max_childs = [4, 64, 8]
        parent_id = [port, None, None, None]
        sched_group_id_root = [None]*1
        sched_group_id_chan_node = [None]*2
        sched_group_id_group_node = [None]*3
        sched_group_service_id = 1
        service_queueId = [None]*3

        #port level
        sched_group_id_root[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        sys_logging("sched_group_id_root[0]=0x%x"%sched_group_id_root[0])
        assert(0 != sched_group_id_root[0])
        
        #channel node level
        parent_id[1] = sched_group_id_root[0]
        
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        assert(0 != sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])
        assert(0 != sched_group_id_chan_node[1])
        
        #service group node level
        parent_id[2] = sched_group_id_chan_node[0]
        
        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[0], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[0]=0x%x"%sched_group_id_group_node[0])
        assert(0 != sched_group_id_group_node[0])
        
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[1]=0x%x"%sched_group_id_group_node[1])
        assert(0 != sched_group_id_group_node[1])
        
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node[2]=0x%x"%sched_group_id_group_node[2])
        assert(0 != sched_group_id_group_node[2])
        
        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = 0
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[0], service_id=sched_group_service_id)
        sys_logging("service_queueId[0]=0x%x"%service_queueId[0])
        
        queue_index = 1
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id)
        sys_logging("service_queueId[1]=0x%x"%service_queueId[1])
        
        queue_index = 2
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[2], service_id=sched_group_service_id)
        sys_logging("service_queueId[2]=0x%x"%service_queueId[2])
        

        queueId_list = []
        sched_oid_1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid_1)
        assert(0 != sched_oid_1)
        
        sched_weight2 = 20
        sched_oid_2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight2, cir, cbs, pir, pbs)
        sys_logging("sched_oid_2 0x%x"%sched_oid_2)
        assert(0 != sched_oid_2)
        
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)        

        
        #service group node weight
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)  

        #vpls config
        port1 = port
        port2 = port_list[2]
        
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label3 = 300
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)  
        
        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, service_id = sched_group_service_id)
        
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, service_id=sched_group_service_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_SERVICE_ID:
                    sys_logging("SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_SERVICE_ID = %d " %a.value.u16)
                    assert( sched_group_service_id == a.value.u16) 
                    
            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_SERVICE_ID:
                    sys_logging("SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_SERVICE_ID = %d " %a.value.u16)
                    assert( sched_group_service_id == a.value.u16) 
                    
            for ii in range(3):
                attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                        sys_logging("Get queue[0x%x] Scheduler Group oid: 0x%x"%(service_queueId[ii], a.value.oid))
                        if a.value.oid != sched_group_id_group_node[ii]:
                            raise NotImplementedError()             

            sys_logging("Verfy Sched Group[0x%x] Attrs!"%sched_group_id_group_node[1])
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id_group_node[1])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    sys_logging("#Get Levle:", a.value.u8)
                    if a.value.u8 != level[2]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    sys_logging("#Get Max Childs:", a.value.u8)
                    if a.value.u8 != max_childs[2]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    sys_logging("#Get Parent Node:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_chan_node[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        if a.value.objlist.object_id_list[o_i] != service_queueId[1]:
                            raise NotImplementedError()       
        finally:
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            for ii in range(3):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)
                self.client.sai_thrift_remove_queue(service_queueId[ii])
                
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)
            
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)
            
            