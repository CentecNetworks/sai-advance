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
        #pdb.set_trace()
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
            
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
                
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
            
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
                
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
            
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
                
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
            
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
                
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
        #pdb.set_trace()
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
            
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
                
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
            
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
                
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
            
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
                
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

            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])

            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)


class fun_01_create_level0_scheduler_group_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        parent_id = port

        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id, 0)
        sys_logging("sched_group_id_root=0x%x"%sched_group_id_root)

        warmboot(self.client)
        try:
            assert(SAI_NULL_OBJECT_ID != sched_group_id_root)
            sched_group_id_root1 = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id, 0)
            sys_logging("sched_group_id_root1=0x%x"%sched_group_id_root1)
            assert(SAI_NULL_OBJECT_ID == sched_group_id_root1)
        finally:
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
        

class fun_02_create_level1_scheduler_group_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        parent_id = port
        sched_group_id_chan_node = [None]*4

        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id, 0)
        sys_logging("sched_group_id_root=0x%x"%sched_group_id_root)

        parent_id = sched_group_id_root
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])

        sched_group_id_chan_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[2]=0x%x"%sched_group_id_chan_node[2])
        
        sched_group_id_chan_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[3]=0x%x"%sched_group_id_chan_node[3])

        warmboot(self.client)
        try:
            assert(SAI_NULL_OBJECT_ID != sched_group_id_chan_node[0])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_chan_node[1])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_chan_node[2])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_chan_node[3])
            sched_group_id_chan_node_4 = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
            sys_logging("sched_group_id_chan_node_4=0x%x"%sched_group_id_chan_node_4)
            assert(SAI_NULL_OBJECT_ID == sched_group_id_chan_node_4)
        finally:
            for i in sched_group_id_chan_node:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)


class fun_03_create_level2_scheduler_group_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        parent_id = port
        sched_group_id_chan_node = [None]*4
        sched_group_id_group_node = [None]*8
        sched_group_id_group_node1 = [None]*8
        sched_group_service_id = 10 

        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id, 0)
        sys_logging("sched_group_id_root=0x%x"%sched_group_id_root)

        parent_id = sched_group_id_root
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])

        sched_group_id_chan_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[2]=0x%x"%sched_group_id_chan_node[2])
        
        sched_group_id_chan_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[3]=0x%x"%sched_group_id_chan_node[3])

        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)      
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)      
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)   
        sys_logging("sched_group_id_group_node[0]=0x%x"%sched_group_id_group_node[0])
        sys_logging("sched_group_id_group_node[1]=0x%x"%sched_group_id_group_node[1])
        sys_logging("sched_group_id_group_node[2]=0x%x"%sched_group_id_group_node[2])
        sys_logging("sched_group_id_group_node[3]=0x%x"%sched_group_id_group_node[3])
        sys_logging("sched_group_id_group_node[4]=0x%x"%sched_group_id_group_node[4])
        sys_logging("sched_group_id_group_node[5]=0x%x"%sched_group_id_group_node[5])
        sys_logging("sched_group_id_group_node[6]=0x%x"%sched_group_id_group_node[6])
        sys_logging("sched_group_id_group_node[7]=0x%x"%sched_group_id_group_node[7])

        sched_group_id_group_node1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)      
        sched_group_id_group_node1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)      
        sched_group_id_group_node1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node1[0]=0x%x"%sched_group_id_group_node1[0])
        sys_logging("sched_group_id_group_node1[1]=0x%x"%sched_group_id_group_node1[1])
        sys_logging("sched_group_id_group_node1[2]=0x%x"%sched_group_id_group_node1[2])
        sys_logging("sched_group_id_group_node1[3]=0x%x"%sched_group_id_group_node1[3])
        sys_logging("sched_group_id_group_node1[4]=0x%x"%sched_group_id_group_node1[4])
        sys_logging("sched_group_id_group_node1[5]=0x%x"%sched_group_id_group_node1[5])
        sys_logging("sched_group_id_group_node1[6]=0x%x"%sched_group_id_group_node1[6])
        sys_logging("sched_group_id_group_node1[7]=0x%x"%sched_group_id_group_node1[7])

        warmboot(self.client)
        try:
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node[0])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node[1])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node[2])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node[3])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node[4])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node[5])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node[6])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node[7])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node1[0])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node1[1])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node1[2])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node1[3])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node1[4])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node1[5])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node1[6])
            assert(SAI_NULL_OBJECT_ID != sched_group_id_group_node1[7])
            sched_group_id_group_node_8 = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0) 
            sys_logging("sched_group_id_group_node_8=0x%x"%sched_group_id_group_node_8)
            assert(SAI_NULL_OBJECT_ID == sched_group_id_group_node_8)
            sched_group_id_group_node1_8 = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id) 
            sys_logging("sched_group_id_group_node1_8=0x%x"%sched_group_id_group_node1_8)
            assert(SAI_NULL_OBJECT_ID == sched_group_id_group_node1_8)
        finally:
            for i in sched_group_id_group_node:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in sched_group_id_group_node1:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in sched_group_id_chan_node:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)


class fun_04_remove_scheduler_group_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        parent_id = port
        sched_group_id_chan_node = [None]*4
        sched_group_id_group_node = [None]*8
        sched_group_id_group_node1 = [None]*8
        sched_group_service_id = 10 

        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id, 0)
        sys_logging("sched_group_id_root=0x%x"%sched_group_id_root)

        parent_id = sched_group_id_root
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])

        sched_group_id_chan_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[2]=0x%x"%sched_group_id_chan_node[2])
        
        sched_group_id_chan_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[3]=0x%x"%sched_group_id_chan_node[3])

        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)      
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)      
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0)   
        sys_logging("sched_group_id_group_node[0]=0x%x"%sched_group_id_group_node[0])
        sys_logging("sched_group_id_group_node[1]=0x%x"%sched_group_id_group_node[1])
        sys_logging("sched_group_id_group_node[2]=0x%x"%sched_group_id_group_node[2])
        sys_logging("sched_group_id_group_node[3]=0x%x"%sched_group_id_group_node[3])
        sys_logging("sched_group_id_group_node[4]=0x%x"%sched_group_id_group_node[4])
        sys_logging("sched_group_id_group_node[5]=0x%x"%sched_group_id_group_node[5])
        sys_logging("sched_group_id_group_node[6]=0x%x"%sched_group_id_group_node[6])
        sys_logging("sched_group_id_group_node[7]=0x%x"%sched_group_id_group_node[7])

        sched_group_id_group_node1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)      
        sched_group_id_group_node1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)      
        sched_group_id_group_node1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node1[0]=0x%x"%sched_group_id_group_node1[0])
        sys_logging("sched_group_id_group_node1[1]=0x%x"%sched_group_id_group_node1[1])
        sys_logging("sched_group_id_group_node1[2]=0x%x"%sched_group_id_group_node1[2])
        sys_logging("sched_group_id_group_node1[3]=0x%x"%sched_group_id_group_node1[3])
        sys_logging("sched_group_id_group_node1[4]=0x%x"%sched_group_id_group_node1[4])
        sys_logging("sched_group_id_group_node1[5]=0x%x"%sched_group_id_group_node1[5])
        sys_logging("sched_group_id_group_node1[6]=0x%x"%sched_group_id_group_node1[6])
        sys_logging("sched_group_id_group_node1[7]=0x%x"%sched_group_id_group_node1[7])

        warmboot(self.client)
        try:
            for i in sched_group_id_group_node:
                attrs = self.client.sai_thrift_get_scheduler_group_attribute(i)
                sys_logging("get sched_group attribute status=%d"%attrs.status)
                assert(SAI_STATUS_SUCCESS == attrs.status)
                status = self.client.sai_thrift_remove_scheduler_group(i)
                sys_logging("remove sched_group status=%d"%status)
                assert(SAI_STATUS_SUCCESS == status)
                attrs = self.client.sai_thrift_get_scheduler_group_attribute(i)
                sys_logging("get removed sched_group attribute status=%d"%attrs.status)
                assert(SAI_STATUS_ITEM_NOT_FOUND == attrs.status)
            for i in sched_group_id_group_node1:
                attrs = self.client.sai_thrift_get_scheduler_group_attribute(i)
                sys_logging("get sched_group attribute status=%d"%attrs.status)
                assert(SAI_STATUS_SUCCESS == attrs.status)
                status = self.client.sai_thrift_remove_scheduler_group(i)
                sys_logging("remove sched_group status=%d"%status)
                assert(SAI_STATUS_SUCCESS == status)
                attrs = self.client.sai_thrift_get_scheduler_group_attribute(i)
                sys_logging("get removed sched_group attribute status=%d"%attrs.status)
                assert(SAI_STATUS_ITEM_NOT_FOUND == attrs.status)
            for i in sched_group_id_chan_node:
                attrs = self.client.sai_thrift_get_scheduler_group_attribute(i)
                sys_logging("get sched_group attribute status=%d"%attrs.status)
                assert(SAI_STATUS_SUCCESS == attrs.status)
                status = self.client.sai_thrift_remove_scheduler_group(i)
                sys_logging("remove sched_group status=%d"%status)
                assert(SAI_STATUS_SUCCESS == status)
                attrs = self.client.sai_thrift_get_scheduler_group_attribute(i)
                sys_logging("get removed sched_group attribute status=%d"%attrs.status)
                assert(SAI_STATUS_ITEM_NOT_FOUND == attrs.status)
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id_root)
            sys_logging("get sched_group attribute status=%d"%attrs.status)
            assert(SAI_STATUS_SUCCESS == attrs.status)
            status = self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
            sys_logging("remove sched_group status=%d"%status)
            assert(SAI_STATUS_SUCCESS == status)
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id_root)
            sys_logging("get removed sched_group attribute status=%d"%attrs.status)
            assert(SAI_STATUS_ITEM_NOT_FOUND == attrs.status)
        finally:
            pass



class fun_05_create_and_remove_serviceid_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        parent_id = port
        sched_group_id_chan_node = [None]*4
        sched_group_id_group_node1 = [None]*8
        sched_group_id_group_node2 = [None]*8
        sched_group_id_group_node3 = [None]*8
        sched_group_service_id = 10 
        sched_group_service_id2 = 20
        sched_group_service_id3 = 30

        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id, 0)
        sys_logging("sched_group_id_root=0x%x"%sched_group_id_root)

        parent_id = sched_group_id_root
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])

        sched_group_id_chan_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[2]=0x%x"%sched_group_id_chan_node[2])
        
        sched_group_id_chan_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id, 0)
        sys_logging("sched_group_id_chan_node[3]=0x%x"%sched_group_id_chan_node[3])


        sched_group_id_group_node1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)      
        sched_group_id_group_node1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)      
        sched_group_id_group_node1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sys_logging("sched_group_id_group_node1[0]=0x%x"%sched_group_id_group_node1[0])
        sys_logging("sched_group_id_group_node1[1]=0x%x"%sched_group_id_group_node1[1])
        sys_logging("sched_group_id_group_node1[2]=0x%x"%sched_group_id_group_node1[2])
        sys_logging("sched_group_id_group_node1[3]=0x%x"%sched_group_id_group_node1[3])
        sys_logging("sched_group_id_group_node1[4]=0x%x"%sched_group_id_group_node1[4])
        sys_logging("sched_group_id_group_node1[5]=0x%x"%sched_group_id_group_node1[5])
        sys_logging("sched_group_id_group_node1[6]=0x%x"%sched_group_id_group_node1[6])
        sys_logging("sched_group_id_group_node1[7]=0x%x"%sched_group_id_group_node1[7])

        sched_group_id_group_node2[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)      
        sched_group_id_group_node2[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)
        sched_group_id_group_node2[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)
        sched_group_id_group_node2[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)
        sched_group_id_group_node2[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)      
        sched_group_id_group_node2[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)
        sched_group_id_group_node2[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)
        sched_group_id_group_node2[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)
        sys_logging("sched_group_id_group_node2[0]=0x%x"%sched_group_id_group_node2[0])
        sys_logging("sched_group_id_group_node2[1]=0x%x"%sched_group_id_group_node2[1])
        sys_logging("sched_group_id_group_node2[2]=0x%x"%sched_group_id_group_node2[2])
        sys_logging("sched_group_id_group_node2[3]=0x%x"%sched_group_id_group_node2[3])
        sys_logging("sched_group_id_group_node2[4]=0x%x"%sched_group_id_group_node2[4])
        sys_logging("sched_group_id_group_node2[5]=0x%x"%sched_group_id_group_node2[5])
        sys_logging("sched_group_id_group_node2[6]=0x%x"%sched_group_id_group_node2[6])
        sys_logging("sched_group_id_group_node2[7]=0x%x"%sched_group_id_group_node2[7])

        

        sched_group_id_group_node3[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)      
        sched_group_id_group_node3[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
        sched_group_id_group_node3[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
        sched_group_id_group_node3[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
        sched_group_id_group_node3[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)      
        sched_group_id_group_node3[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
        sched_group_id_group_node3[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
        sched_group_id_group_node3[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
        sys_logging("sched_group_id_group_node3[0]=0x%x"%sched_group_id_group_node3[0])
        sys_logging("sched_group_id_group_node3[1]=0x%x"%sched_group_id_group_node3[1])
        sys_logging("sched_group_id_group_node3[2]=0x%x"%sched_group_id_group_node3[2])
        sys_logging("sched_group_id_group_node3[3]=0x%x"%sched_group_id_group_node3[3])
        sys_logging("sched_group_id_group_node3[4]=0x%x"%sched_group_id_group_node3[4])
        sys_logging("sched_group_id_group_node3[5]=0x%x"%sched_group_id_group_node3[5])
        sys_logging("sched_group_id_group_node3[6]=0x%x"%sched_group_id_group_node3[6])
        sys_logging("sched_group_id_group_node3[7]=0x%x"%sched_group_id_group_node3[7])
        #pdb.set_trace()

        warmboot(self.client)
        try:
            for i in sched_group_id_group_node1:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in sched_group_id_group_node2:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in sched_group_id_group_node3:
                self.client.sai_thrift_remove_scheduler_group(i)
            #pdb.set_trace()
            sched_group_id_group_node1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)      
            sched_group_id_group_node1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
            sched_group_id_group_node1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
            sched_group_id_group_node1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
            sched_group_id_group_node1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)      
            sched_group_id_group_node1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
            sched_group_id_group_node1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
            sched_group_id_group_node1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)

            sched_group_id_group_node2[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)      
            sched_group_id_group_node2[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)
            sched_group_id_group_node2[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)
            sched_group_id_group_node2[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)
            sched_group_id_group_node2[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)      
            sched_group_id_group_node2[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)
            sched_group_id_group_node2[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)
            sched_group_id_group_node2[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], 0, service_id=sched_group_service_id2)

            sched_group_id_group_node3[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)      
            sched_group_id_group_node3[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
            sched_group_id_group_node3[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
            sched_group_id_group_node3[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
            sched_group_id_group_node3[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)      
            sched_group_id_group_node3[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
            sched_group_id_group_node3[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
            sched_group_id_group_node3[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id3)
            #pdb.set_trace()
        finally:
            for i in sched_group_id_group_node1:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in sched_group_id_group_node2:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in sched_group_id_group_node3:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in sched_group_id_chan_node:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)


class fun_06_set_normal_type_scheduler_group_attribute_scheduler_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        parent_id = port
        sched_group_id_chan_node = [None]*4
        sched_group_id_group_node = [None]*8

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
        sys_logging("sched_oid_2 0x%x"%sched_oid2)

        sched_oid3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight1, cir, cbs, pir, pbs)
        sys_logging("sched_oid_3 0x%x"%sched_oid3)

        sched_oid4 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight2, cir, cbs, pir, pbs)
        sys_logging("sched_oid_4 0x%x"%sched_oid4)



        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id, 0)
        sys_logging("sched_group_id_root=0x%x"%sched_group_id_root)

        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])

        sched_group_id_chan_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        sys_logging("sched_group_id_chan_node[2]=0x%x"%sched_group_id_chan_node[2])
        
        sched_group_id_chan_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        sys_logging("sched_group_id_chan_node[3]=0x%x"%sched_group_id_chan_node[3])

        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3)      
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3)      
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3)   
        sys_logging("sched_group_id_group_node[0]=0x%x"%sched_group_id_group_node[0])
        sys_logging("sched_group_id_group_node[1]=0x%x"%sched_group_id_group_node[1])
        sys_logging("sched_group_id_group_node[2]=0x%x"%sched_group_id_group_node[2])
        sys_logging("sched_group_id_group_node[3]=0x%x"%sched_group_id_group_node[3])
        sys_logging("sched_group_id_group_node[4]=0x%x"%sched_group_id_group_node[4])
        sys_logging("sched_group_id_group_node[5]=0x%x"%sched_group_id_group_node[5])
        sys_logging("sched_group_id_group_node[6]=0x%x"%sched_group_id_group_node[6])
        sys_logging("sched_group_id_group_node[7]=0x%x"%sched_group_id_group_node[7])

        queueId_list = []
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
        
        
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[4], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[5], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[6], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[3], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[7], attr)

        warmboot(self.client)
        try:
            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(oid=sched_oid4)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[0], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[1], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[2], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[3], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[4], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[5], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[6], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node[7], attr)
        finally:
            #pdb.set_trace()
            for i in queueId_list:
                self.client.sai_thrift_remove_queue(i)
            for i in sched_group_id_group_node:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in sched_group_id_chan_node:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)


class fun_07_set_service_type_scheduler_group_attribute_scheduler_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        parent_id = port
        sched_group_id_chan_node = [None]*4
        sched_group_id_group_node1 = [None]*8
        service_queueId = [None]*8
        sched_group_service_id = 10

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
        sys_logging("sched_oid_2 0x%x"%sched_oid2)

        sched_oid3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight1, cir, cbs, pir, pbs)
        sys_logging("sched_oid_3 0x%x"%sched_oid3)

        sched_oid4 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight2, cir, cbs, pir, pbs)
        sys_logging("sched_oid_4 0x%x"%sched_oid4)



        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id, 0)
        sys_logging("sched_group_id_root=0x%x"%sched_group_id_root)

        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        sys_logging("sched_group_id_chan_node[0]=0x%x"%sched_group_id_chan_node[0])
        
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        sys_logging("sched_group_id_chan_node[1]=0x%x"%sched_group_id_chan_node[1])

        sched_group_id_chan_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        sys_logging("sched_group_id_chan_node[2]=0x%x"%sched_group_id_chan_node[2])
        
        sched_group_id_chan_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        sys_logging("sched_group_id_chan_node[3]=0x%x"%sched_group_id_chan_node[3])

        sched_group_id_group_node1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3, service_id=sched_group_service_id)      
        sched_group_id_group_node1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3, service_id=sched_group_service_id)
        sched_group_id_group_node1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3, service_id=sched_group_service_id)
        sched_group_id_group_node1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3, service_id=sched_group_service_id)
        sched_group_id_group_node1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3, service_id=sched_group_service_id)      
        sched_group_id_group_node1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3, service_id=sched_group_service_id)
        sched_group_id_group_node1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3, service_id=sched_group_service_id)
        sched_group_id_group_node1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[2], sched_oid3, service_id=sched_group_service_id)
        #pdb.set_trace()
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
        
        #pdb.set_trace()
        attr_value = sai_thrift_attribute_value_t(oid=sched_oid2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)
        self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)

        warmboot(self.client)
        try:
            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(oid=sched_oid4)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node1[0], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node1[1], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node1[2], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node1[3], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node1[4], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node1[5], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node1[6], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id_group_node1[7], attr)
        finally:
            #pdb.set_trace()
            for i in service_queueId:
                self.client.sai_thrift_remove_queue(i)
            for i in sched_group_id_group_node1:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in sched_group_id_chan_node:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)


class fun_08_set_normal_type_scheduler_group_attribute_parent_node_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)


        #create scheduler profile
        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight1 = 10
        sched_weight2 = 15
        sched_weight3 = 20
        cir = 2000000
        cir2 = 2500000
        cbs = 256000
        cbs2 = 356000
        pir = 1000000
        pir2 = 1500000
        pbs = 64000
        pbs2 = 74000

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid4 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight1, cir2, cbs2, pir2, pbs2)
        sched_oid5 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight2, cir2, cbs2, pir2, pbs2)
        sched_oid6 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight3, cir2, cbs2, pir2, pbs2)



        #create scheduler group and queue
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 100, 8]
        root_sched_group = [None]*1
        channel_sched_group = [None]*4
        node_sched_group = [None]*8
        basic_queueId = [None]*8


        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        channel_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        
        node_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)      
        node_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)      
        node_sched_group[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        sys_logging("node_sched_group[0]=0x%x"%node_sched_group[0])
        sys_logging("node_sched_group[1]=0x%x"%node_sched_group[1])
        sys_logging("node_sched_group[2]=0x%x"%node_sched_group[2])
        sys_logging("node_sched_group[3]=0x%x"%node_sched_group[3])
        sys_logging("node_sched_group[4]=0x%x"%node_sched_group[4])
        sys_logging("node_sched_group[5]=0x%x"%node_sched_group[5])
        sys_logging("node_sched_group[6]=0x%x"%node_sched_group[6])
        sys_logging("node_sched_group[7]=0x%x"%node_sched_group[7])
        queue_type = SAI_QUEUE_TYPE_ALL
        queue_index = [0,1,2,3,4,5,6,7]
        basic_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=node_sched_group[0], sche_id=sched_oid1)        
        basic_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=node_sched_group[1], sche_id=sched_oid5)
        basic_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=node_sched_group[1], sche_id=sched_oid6)
        basic_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=node_sched_group[3], sche_id=sched_oid2)
        basic_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=node_sched_group[4], sche_id=sched_oid6)
        basic_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=node_sched_group[4], sche_id=sched_oid5)
        basic_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=node_sched_group[4], sche_id=sched_oid6)
        basic_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=node_sched_group[7], sche_id=sched_oid3)
        #pdb.set_trace()

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(channel_sched_group[2])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
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
                    if a.value.oid != root_sched_group[0]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 8:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        #if a.value.objlist.object_id_list[o_i] != sched_group_id_group_node[o_i%1]:
                        #    raise NotImplementedError()
            #pdb.set_trace()
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(channel_sched_group[1])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
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
                    if a.value.oid != root_sched_group[0]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        #if a.value.objlist.object_id_list[o_i] != sched_group_id_group_node[o_i%1]:
                        #    raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(oid=channel_sched_group[1])
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[0], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[1], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[2], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[3], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[4], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[5], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[6], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[7], attr)
            #pdb.set_trace()

            attrs = self.client.sai_thrift_get_scheduler_group_attribute(channel_sched_group[1])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
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
                    if a.value.oid != root_sched_group[0]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 8:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        #if a.value.objlist.object_id_list[o_i] != sched_group_id_group_node[o_i%1]:
                        #    raise NotImplementedError()

            attrs = self.client.sai_thrift_get_scheduler_group_attribute(channel_sched_group[2])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
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
                    if a.value.oid != root_sched_group[0]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        #if a.value.objlist.object_id_list[o_i] != sched_group_id_group_node[o_i%1]:
                        #    raise NotImplementedError()



            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[0])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid4:
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
                    if a.value.oid != channel_sched_group[1]:
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
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[1])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid4:
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
                    if a.value.oid != channel_sched_group[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 2:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))   
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[2])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[3])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[4])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 3:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[5])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[6])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[7])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            #update queue attribure parent scheduler group and scheduler profile
            attr_value = sai_thrift_attribute_value_t(oid=node_sched_group[3])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(basic_queueId[4], attr)
            self.client.sai_thrift_set_queue_attribute(basic_queueId[5], attr)
            attr_value = sai_thrift_attribute_value_t(oid=node_sched_group[6])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(basic_queueId[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_oid4)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(basic_queueId[3], attr)
            attr_value = sai_thrift_attribute_value_t(oid=sched_oid2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(basic_queueId[6], attr)
            #pdb.set_trace()
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[3])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 3:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[4])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[5])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[6])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))


        finally:
            #remove all
            for i in basic_queueId:
                self.client.sai_thrift_remove_queue(i)
            for i in node_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in channel_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in root_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid5)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid6)


class fun_09_set_service_type_scheduler_group_attribute_parent_node_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)


        #create scheduler profile
        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight1 = 10
        sched_weight2 = 15
        sched_weight3 = 20
        cir = 2000000
        cir2 = 2500000
        cbs = 256000
        cbs2 = 356000
        pir = 1000000
        pir2 = 1500000
        pbs = 64000
        pbs2 = 74000

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid4 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight1, cir2, cbs2, pir2, pbs2)
        sched_oid5 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight2, cir2, cbs2, pir2, pbs2)
        sched_oid6 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight3, cir2, cbs2, pir2, pbs2)



        #create scheduler group and queue
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 100, 8]
        root_sched_group = [None]*1
        channel_sched_group = [None]*4
        node_sched_group = [None]*8
        service_queueId = [None]*8
        sched_group_service_id = 10


        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        channel_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        
        node_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id)      
        node_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id)
        node_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id)
        node_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id)
        node_sched_group[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id)      
        node_sched_group[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id)
        node_sched_group[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id)
        node_sched_group[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id)

        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=node_sched_group[0], sche_id=sched_oid1, service_id=sched_group_service_id)        
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=node_sched_group[1], sche_id=sched_oid5, service_id=sched_group_service_id)
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=node_sched_group[1], sche_id=sched_oid6, service_id=sched_group_service_id)
        service_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=node_sched_group[3], sche_id=sched_oid2, service_id=sched_group_service_id)
        service_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=node_sched_group[4], sche_id=sched_oid6, service_id=sched_group_service_id)
        service_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=node_sched_group[4], sche_id=sched_oid5, service_id=sched_group_service_id)
        service_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=node_sched_group[4], sche_id=sched_oid6, service_id=sched_group_service_id)
        service_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=node_sched_group[7], sche_id=sched_oid3, service_id=sched_group_service_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(channel_sched_group[2])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
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
                    if a.value.oid != root_sched_group[0]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 8:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        #if a.value.objlist.object_id_list[o_i] != sched_group_id_group_node[o_i%1]:
                        #    raise NotImplementedError()
            #pdb.set_trace()
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(channel_sched_group[1])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
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
                    if a.value.oid != root_sched_group[0]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        #if a.value.objlist.object_id_list[o_i] != sched_group_id_group_node[o_i%1]:
                        #    raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(oid=channel_sched_group[1])
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[0], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[1], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[2], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[3], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[4], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[5], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[6], attr)
            self.client.sai_thrift_set_scheduler_group_attribute(node_sched_group[7], attr)
            #pdb.set_trace()

            attrs = self.client.sai_thrift_get_scheduler_group_attribute(channel_sched_group[1])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
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
                    if a.value.oid != root_sched_group[0]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 8:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        #if a.value.objlist.object_id_list[o_i] != sched_group_id_group_node[o_i%1]:
                        #    raise NotImplementedError()

            attrs = self.client.sai_thrift_get_scheduler_group_attribute(channel_sched_group[2])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
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
                    if a.value.oid != root_sched_group[0]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
                        #if a.value.objlist.object_id_list[o_i] != sched_group_id_group_node[o_i%1]:
                        #    raise NotImplementedError()




            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[0])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid4:
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
                    if a.value.oid != channel_sched_group[1]:
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
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[1])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("#Get Sched Oid:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid4:
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
                    if a.value.oid != channel_sched_group[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    sys_logging("#Get Port Id:0x%x"%a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 2:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))   
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[2])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[3])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[4])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 3:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[5])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[6])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[7])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            #update queue attribure parent scheduler group and scheduler profile
            attr_value = sai_thrift_attribute_value_t(oid=node_sched_group[3])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            attr_value = sai_thrift_attribute_value_t(oid=node_sched_group[6])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_oid4)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)
            attr_value = sai_thrift_attribute_value_t(oid=sched_oid2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)
            #pdb.set_trace()
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[3])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 3:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[4])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[5])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 0:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(node_sched_group[6])
            sys_logging("get attribute status=%d"%attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    sys_logging("#Get Child Count:",a.value.u32)
                    if a.value.u32 != 1:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    sys_logging("#Get Child Child List Count:",a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))


        finally:
            #remove all
            for i in service_queueId:
                self.client.sai_thrift_remove_queue(i)
            for i in node_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in channel_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in root_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid5)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid6)

'''
class test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)


        #create scheduler profile
        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight1 = 10
        sched_weight2 = 15
        sched_weight3 = 20
        cir = 2000000
        cir2 = 2500000
        cbs = 256000
        cbs2 = 356000
        pir = 1000000
        pir2 = 1500000
        pbs = 64000
        pbs2 = 74000

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid4 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight1, cir2, cbs2, pir2, pbs2)
        sched_oid5 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight2, cir2, cbs2, pir2, pbs2)
        sched_oid6 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight3, cir2, cbs2, pir2, pbs2)



        #create scheduler group and queue
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 64, 8]
        root_sched_group = [None]*1
        channel_sched_group = [None]*4
        node_sched_group1 = [None]*8
        node_sched_group2 = [None]*8
        node_sched_group3 = [None]*8
        node_sched_group4 = [None]*8
        node_sched_group5 = [None]*8
        basic_queueId = [None]*8
        service_queueId1 = [None]*8
        service_queueId2 = [None]*8
        service_queueId3 = [None]*8
        sched_group_service_id1 = 2
        sched_group_service_id2 = 3
        sched_group_service_id3 = 4
        sched_group_service_id4 = 5


        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        channel_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        
        node_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)      
        node_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)      
        node_sched_group1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)

        node_sched_group2[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)      
        node_sched_group2[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)
        node_sched_group2[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)
        node_sched_group2[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)
        node_sched_group2[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)      
        node_sched_group2[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)
        node_sched_group2[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)
        node_sched_group2[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)

        node_sched_group3[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)      
        node_sched_group3[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)
        node_sched_group3[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)
        node_sched_group3[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)
        node_sched_group3[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)      
        node_sched_group3[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)
        node_sched_group3[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)
        node_sched_group3[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)

        node_sched_group4[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)      
        node_sched_group4[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)
        node_sched_group4[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)
        node_sched_group4[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)
        node_sched_group4[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)      
        node_sched_group4[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)
        node_sched_group4[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)
        node_sched_group4[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)

        node_sched_group5[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id4)      
        node_sched_group5[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id4)
        node_sched_group5[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id4)
        node_sched_group5[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id4)
        node_sched_group5[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id4)      
        node_sched_group5[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id4)
        node_sched_group5[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id4)
        node_sched_group5[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id4)

        queue_type = SAI_QUEUE_TYPE_ALL
        queue_index = [0,1,2,3,4,5,6,7]
        basic_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=node_sched_group1[0], sche_id=sched_oid1)        
        basic_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=node_sched_group1[1], sche_id=sched_oid5)
        basic_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=node_sched_group1[1], sche_id=sched_oid6)
        basic_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=node_sched_group1[3], sche_id=sched_oid2)
        basic_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=node_sched_group1[4], sche_id=sched_oid6)
        basic_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=node_sched_group1[4], sche_id=sched_oid5)
        basic_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=node_sched_group1[4], sche_id=sched_oid6)
        basic_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=node_sched_group1[7], sche_id=sched_oid3)

        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId1[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=node_sched_group2[0], sche_id=sched_oid1, service_id=sched_group_service_id1)        
        service_queueId1[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=node_sched_group2[1], sche_id=sched_oid5, service_id=sched_group_service_id1)
        service_queueId1[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=node_sched_group2[1], sche_id=sched_oid6, service_id=sched_group_service_id1)
        service_queueId1[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=node_sched_group2[3], sche_id=sched_oid2, service_id=sched_group_service_id1)
        service_queueId1[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=node_sched_group2[4], sche_id=sched_oid6, service_id=sched_group_service_id1)
        service_queueId1[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=node_sched_group2[4], sche_id=sched_oid5, service_id=sched_group_service_id1)
        service_queueId1[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=node_sched_group2[4], sche_id=sched_oid6, service_id=sched_group_service_id1)
        service_queueId1[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=node_sched_group2[7], sche_id=sched_oid3, service_id=sched_group_service_id1)

        service_queueId2[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=node_sched_group3[0], sche_id=sched_oid1, service_id=sched_group_service_id2)        
        service_queueId2[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=node_sched_group3[1], sche_id=sched_oid5, service_id=sched_group_service_id2)
        service_queueId2[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=node_sched_group3[1], sche_id=sched_oid6, service_id=sched_group_service_id2)
        service_queueId2[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=node_sched_group3[3], sche_id=sched_oid2, service_id=sched_group_service_id2)
        service_queueId2[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=node_sched_group3[4], sche_id=sched_oid6, service_id=sched_group_service_id2)
        service_queueId2[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=node_sched_group3[4], sche_id=sched_oid5, service_id=sched_group_service_id2)
        service_queueId2[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=node_sched_group3[4], sche_id=sched_oid6, service_id=sched_group_service_id2)
        service_queueId2[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=node_sched_group3[7], sche_id=sched_oid3, service_id=sched_group_service_id2)

        service_queueId3[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=node_sched_group4[0], sche_id=sched_oid1, service_id=sched_group_service_id3)        
        service_queueId3[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=node_sched_group4[1], sche_id=sched_oid5, service_id=sched_group_service_id3)
        service_queueId3[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=node_sched_group4[1], sche_id=sched_oid6, service_id=sched_group_service_id3)
        service_queueId3[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=node_sched_group4[3], sche_id=sched_oid2, service_id=sched_group_service_id3)
        service_queueId3[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=node_sched_group4[4], sche_id=sched_oid6, service_id=sched_group_service_id3)
        service_queueId3[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=node_sched_group4[4], sche_id=sched_oid5, service_id=sched_group_service_id3)
        service_queueId3[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=node_sched_group4[4], sche_id=sched_oid6, service_id=sched_group_service_id3)
        service_queueId3[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=node_sched_group4[7], sche_id=sched_oid3, service_id=sched_group_service_id3)
        pdb.set_trace()

        warmboot(self.client)
        pdb.set_trace()
        try:
          
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    assert(32 == a.value.u32)
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS:
                    sys_logging("get port attribute scheduler group num = %d"%a.value.u32)
                    assert (37 == a.value.u32)  
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST:
                    sys_logging("get port attribute scheduler group list count = " ,a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("the %dth scheduler group member = 0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
        finally:
            #remove all
            for i in basic_queueId:
                self.client.sai_thrift_remove_queue(i)
            pdb.set_trace()
            for i in service_queueId1:
                self.client.sai_thrift_remove_queue(i)
            for i in service_queueId2:
                self.client.sai_thrift_remove_queue(i)
            for i in service_queueId3:
                self.client.sai_thrift_remove_queue(i)
            for i in node_sched_group1:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in node_sched_group2:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in node_sched_group3:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in node_sched_group4:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in node_sched_group5:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in channel_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in root_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid5)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid6) 

'''


class fun_10_get_port_attr_scheduler_group_num_and_list_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)


        #create scheduler profile
        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight1 = 10
        sched_weight2 = 15
        sched_weight3 = 20
        cir = 2000000
        cir2 = 2500000
        cbs = 256000
        cbs2 = 356000
        pir = 1000000
        pir2 = 1500000
        pbs = 64000
        pbs2 = 74000

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid3 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, sched_weight1, cir, cbs, pir, pbs)
        sched_oid4 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight1, cir2, cbs2, pir2, pbs2)
        sched_oid5 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight2, cir2, cbs2, pir2, pbs2)
        sched_oid6 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight3, cir2, cbs2, pir2, pbs2)



        #create scheduler group and queue
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 64, 8]
        root_sched_group = [None]*1
        channel_sched_group = [None]*4
        node_sched_group1 = [None]*8
        node_sched_group2 = [None]*8
        node_sched_group3 = [None]*8
        node_sched_group4 = [None]*8
        basic_queueId = [None]*8
        service_queueId1 = [None]*8
        service_queueId2 = [None]*8
        service_queueId3 = [None]*8
        sched_group_service_id1 = 1
        sched_group_service_id2 = 5
        sched_group_service_id3 = 10


        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        channel_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        channel_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        
        node_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)      
        node_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)      
        node_sched_group1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)
        node_sched_group1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4)

        node_sched_group2[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)      
        node_sched_group2[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)
        node_sched_group2[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)
        node_sched_group2[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)
        node_sched_group2[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)      
        node_sched_group2[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)
        node_sched_group2[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)
        node_sched_group2[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[1], sched_oid4, service_id=sched_group_service_id1)

        node_sched_group3[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)      
        node_sched_group3[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)
        node_sched_group3[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)
        node_sched_group3[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)
        node_sched_group3[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)      
        node_sched_group3[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)
        node_sched_group3[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)
        node_sched_group3[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[2], sched_oid4, service_id=sched_group_service_id2)

        node_sched_group4[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)      
        node_sched_group4[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)
        node_sched_group4[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)
        node_sched_group4[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)
        node_sched_group4[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)      
        node_sched_group4[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)
        node_sched_group4[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)
        node_sched_group4[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], channel_sched_group[0], sched_oid4, service_id=sched_group_service_id3)

        queue_type = SAI_QUEUE_TYPE_ALL
        queue_index = [0,1,2,3,4,5,6,7]
        basic_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=node_sched_group1[0], sche_id=sched_oid1)        
        basic_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=node_sched_group1[1], sche_id=sched_oid5)
        basic_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=node_sched_group1[1], sche_id=sched_oid6)
        basic_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=node_sched_group1[3], sche_id=sched_oid2)
        basic_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=node_sched_group1[4], sche_id=sched_oid6)
        basic_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=node_sched_group1[4], sche_id=sched_oid5)
        basic_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=node_sched_group1[4], sche_id=sched_oid6)
        basic_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=node_sched_group1[7], sche_id=sched_oid3)

        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId1[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=node_sched_group2[0], sche_id=sched_oid1, service_id=sched_group_service_id1)        
        service_queueId1[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=node_sched_group2[1], sche_id=sched_oid5, service_id=sched_group_service_id1)
        service_queueId1[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=node_sched_group2[1], sche_id=sched_oid6, service_id=sched_group_service_id1)
        service_queueId1[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=node_sched_group2[3], sche_id=sched_oid2, service_id=sched_group_service_id1)
        service_queueId1[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=node_sched_group2[4], sche_id=sched_oid6, service_id=sched_group_service_id1)
        service_queueId1[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=node_sched_group2[4], sche_id=sched_oid5, service_id=sched_group_service_id1)
        service_queueId1[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=node_sched_group2[4], sche_id=sched_oid6, service_id=sched_group_service_id1)
        service_queueId1[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=node_sched_group2[7], sche_id=sched_oid3, service_id=sched_group_service_id1)

        service_queueId2[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=node_sched_group3[0], sche_id=sched_oid1, service_id=sched_group_service_id2)        
        service_queueId2[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=node_sched_group3[1], sche_id=sched_oid5, service_id=sched_group_service_id2)
        service_queueId2[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=node_sched_group3[1], sche_id=sched_oid6, service_id=sched_group_service_id2)
        service_queueId2[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=node_sched_group3[3], sche_id=sched_oid2, service_id=sched_group_service_id2)
        service_queueId2[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=node_sched_group3[4], sche_id=sched_oid6, service_id=sched_group_service_id2)
        service_queueId2[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=node_sched_group3[4], sche_id=sched_oid5, service_id=sched_group_service_id2)
        service_queueId2[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=node_sched_group3[4], sche_id=sched_oid6, service_id=sched_group_service_id2)
        service_queueId2[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=node_sched_group3[7], sche_id=sched_oid3, service_id=sched_group_service_id2)

        service_queueId3[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=node_sched_group4[0], sche_id=sched_oid1, service_id=sched_group_service_id3)        
        service_queueId3[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=node_sched_group4[1], sche_id=sched_oid5, service_id=sched_group_service_id3)
        service_queueId3[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=node_sched_group4[1], sche_id=sched_oid6, service_id=sched_group_service_id3)
        service_queueId3[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=node_sched_group4[3], sche_id=sched_oid2, service_id=sched_group_service_id3)
        service_queueId3[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=node_sched_group4[4], sche_id=sched_oid6, service_id=sched_group_service_id3)
        service_queueId3[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=node_sched_group4[4], sche_id=sched_oid5, service_id=sched_group_service_id3)
        service_queueId3[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=node_sched_group4[4], sche_id=sched_oid6, service_id=sched_group_service_id3)
        service_queueId3[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=node_sched_group4[7], sche_id=sched_oid3, service_id=sched_group_service_id3)

        warmboot(self.client)
        try:
          
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    assert(32 == a.value.u32)
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS:
                    sys_logging("get port attribute scheduler group num = %d"%a.value.u32)
                    assert (37 == a.value.u32)  
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST:
                    sys_logging("get port attribute scheduler group list count = " ,a.value.objlist.count)
                    for o_i in range(a.value.objlist.count):
                        sys_logging("the %dth scheduler group member = 0x%x"%(o_i, a.value.objlist.object_id_list[o_i]))
        finally:
            #remove all
            for i in basic_queueId:
                self.client.sai_thrift_remove_queue(i)
            for i in service_queueId1:
                self.client.sai_thrift_remove_queue(i)
            for i in service_queueId2:
                self.client.sai_thrift_remove_queue(i)
            for i in service_queueId3:
                self.client.sai_thrift_remove_queue(i)
            for i in node_sched_group1:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in node_sched_group2:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in node_sched_group3:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in node_sched_group4:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in channel_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in root_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid5)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid6) 


            

            
