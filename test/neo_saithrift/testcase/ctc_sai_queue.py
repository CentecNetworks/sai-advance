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
Thrift SAI interface Queue tests
"""
import socket
from switch import *
import sai_base_test
import pdb

chipname = testutils.test_params_get()['chipname']


@group('Queue')
class QueueCreateQueueIdWithUcTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create queue id  & UC
        step2:verify queue attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]
        queue_index = 1
        queue_type = SAI_QUEUE_TYPE_UNICAST

        queueId = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0) 
        sys_logging("queue_id:",queueId)
        sys_logging("port:",port)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_TYPE:
                    sys_logging("get queue type:%d"%a.value.u32)
                    if a.value.u32 != queue_type:
                        raise NotImplementedError() 
                if a.id == SAI_QUEUE_ATTR_PORT:
                    sys_logging("get port:",a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError()    
                if a.id == SAI_QUEUE_ATTR_INDEX:
                    sys_logging("get index:%d"%a.value.u8)
                    if a.value.u8 != queue_index:
                        raise NotImplementedError()                                          
        finally:
            self.client.sai_thrift_remove_queue(queueId)

@group('Queue')
class QueueCreateQueueIdWithMcTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create queue id & MC
        step2:verify queue attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]
        queue_index = 1
        queue_type = SAI_QUEUE_TYPE_MULTICAST

        queueId = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0) 
        sys_logging("queue_id:",queueId)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_TYPE:
                    sys_logging("get queue type:%d"%a.value.u32)
                    if a.value.u32 != queue_type:
                        raise NotImplementedError() 
                if a.id == SAI_QUEUE_ATTR_PORT:
                    sys_logging("get port:",a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError()    
                if a.id == SAI_QUEUE_ATTR_INDEX:
                    sys_logging("get index:%d"%a.value.u8)
                    if a.value.u8 != queue_index:
                        raise NotImplementedError()                                          
        finally:
            self.client.sai_thrift_remove_queue(queueId)

@group('Queue')
class QueueSetQueueAttributeWithWredIdTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create queue id & Set Attr with WredId
        step2:verify queue attr 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]
        queue_index = 1

        #create Wred Id
        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,2000,2000]
        drop_prob = [100, 50, 10]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        sys_logging("wred_id:",wred_id)

        #Create Queue Id
        queueId = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_UNICAST, port, queue_index, 0) 
        sys_logging("queue_id:",queueId)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId, attr)
        #pdb.set_trace()
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId)
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred_id:0x%X"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()                                      
        finally:
            self.client.sai_thrift_remove_queue(queueId)
            self.client.sai_thrift_remove_wred_profile(wred_id)

@group('Queue')
class GetQueueListFromPortTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Get Queue list from port
        step1:Get queue num & list & set queue attr
        step2:verify queue attr 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]
        queueId = 0
        queueId_list = []

        #create Wred Id
        color_en = [0,0,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        sys_logging("wred_id:0x%X"%wred_id)


        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
        queueId = queueId_list[0]

        #set attr
        #pdb.set_trace()
        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId)
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred_id:0x%X"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError() 
        finally:
            self.client.sai_thrift_remove_queue(queueId)
            self.client.sai_thrift_remove_wred_profile(wred_id)

class fun_01_create_normal_type_queue_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create 3 type queues 
        step2:verify queues attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[1]
        queue_index1 = 1
        queue_index2 = 2
        queue_index3 = 3
        queue_type1 = SAI_QUEUE_TYPE_ALL
        queue_type2 = SAI_QUEUE_TYPE_UNICAST
        queue_type3 = SAI_QUEUE_TYPE_MULTICAST

        queueId1 = sai_thrift_create_queue_id(self.client, queue_type1, port, queue_index1) 
        sys_logging("queue_id:0x%x" %queueId1)

        queueId2 = sai_thrift_create_queue_id(self.client, queue_type2, port, queue_index2) 
        sys_logging("queue_id:0x%x" %queueId2)

        queueId3 = sai_thrift_create_queue_id(self.client, queue_type3, port, queue_index3) 
        sys_logging("queue_id:0x%x" %queueId3)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId1)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_TYPE:
                    sys_logging("get queue type:%d"%a.value.u32)
                    if a.value.u32 != queue_type1:
                        raise NotImplementedError() 
                if a.id == SAI_QUEUE_ATTR_PORT:
                    sys_logging("get port:0x%x" %a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError()    
                if a.id == SAI_QUEUE_ATTR_INDEX:
                    sys_logging("get index:%d"%a.value.u8)
                    if a.value.u8 != queue_index1:
                        raise NotImplementedError()   
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("Get queue Buffer Profile oid: 0x%x"% a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("Get queue scheduler Profile oid: 0x%x"% a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
                    sys_logging("get queue pfc dldr enable:%d"%a.value.booldata)
                    if a.value.booldata != False:
                        raise NotImplementedError()



            attrs = self.client.sai_thrift_get_queue_attribute(queueId2)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_TYPE:
                    sys_logging("get queue type:%d"%a.value.u32)
                    if a.value.u32 != queue_type2:
                        raise NotImplementedError() 
                if a.id == SAI_QUEUE_ATTR_PORT:
                    sys_logging("get port:0x%x" %a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError()    
                if a.id == SAI_QUEUE_ATTR_INDEX:
                    sys_logging("get index:%d"%a.value.u8)
                    if a.value.u8 != queue_index2:
                        raise NotImplementedError() 
                        
            attrs = self.client.sai_thrift_get_queue_attribute(queueId3)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_TYPE:
                    sys_logging("get queue type:%d"%a.value.u32)
                    if a.value.u32 != queue_type3:
                        raise NotImplementedError() 
                if a.id == SAI_QUEUE_ATTR_PORT:
                    sys_logging("get port:0x%x" %a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError()    
                if a.id == SAI_QUEUE_ATTR_INDEX:
                    sys_logging("get index:%d"%a.value.u8)
                    if a.value.u8 != queue_index3:
                        raise NotImplementedError() 
                        
        finally:
            self.client.sai_thrift_remove_queue(queueId1)
            self.client.sai_thrift_remove_queue(queueId2)
            self.client.sai_thrift_remove_queue(queueId3)


class fun_02_get_port_default_queue_list_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:get port attribute queue list 
        step2:verify queues attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[1]
        queueId_list = []
        queue_type1 = SAI_QUEUE_TYPE_ALL

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])

        warmboot(self.client)
        try:
            for i in range(8):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_TYPE:
                        sys_logging("get queue type:%d"%a.value.u32)
                        if a.value.u32 != queue_type1:
                            raise NotImplementedError() 
                    if a.id == SAI_QUEUE_ATTR_PORT:
                        sys_logging("get port:0x%x" %a.value.oid)
                        if a.value.oid != port:
                            raise NotImplementedError()    
                    if a.id == SAI_QUEUE_ATTR_INDEX:
                        sys_logging("get index:%d"%a.value.u8)
                        if a.value.u8 != i:
                            raise NotImplementedError() 
        finally:
            for ii in queueId_list:
                self.client.sai_thrift_remove_queue(ii)


class fun_03_create_service_type_queue_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create service type queues 
        step2:verify queues attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[1]
        port2 = port_list[2]
        queue_index_list = [0,1,2,3,4,5,6,7]
        queue_type1 = SAI_QUEUE_TYPE_SERVICE
        sched_group_service_id = 1
        sched_group_service_id2 = 10
        


        queueId1 = sai_thrift_create_queue_id(self.client, queue_type1, port, queue_index_list[0], service_id=sched_group_service_id) 
        sys_logging("queue_id:0x%x" %queueId1)

        queueId2 = sai_thrift_create_queue_id(self.client, queue_type1, port2, queue_index_list[1], service_id=sched_group_service_id2) 
        sys_logging("queue_id:0x%x" %queueId2)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId1)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_TYPE:
                    sys_logging("get queue type:%d"%a.value.u32)
                    if a.value.u32 != queue_type1:
                        raise NotImplementedError() 
                if a.id == SAI_QUEUE_ATTR_PORT:
                    sys_logging("get port:0x%x" %a.value.oid)
                    if a.value.oid != port:
                        raise NotImplementedError()    
                if a.id == SAI_QUEUE_ATTR_INDEX:
                    sys_logging("get index:%d"%a.value.u8)
                    if a.value.u8 != queue_index_list[0]:
                        raise NotImplementedError()    
                if a.id == SAI_QUEUE_ATTR_SERVICE_ID:
                    sys_logging("get service id:%d"%a.value.u16)
                    if a.value.u16 != sched_group_service_id:
                        raise NotImplementedError()  

            attrs = self.client.sai_thrift_get_queue_attribute(queueId2)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_TYPE:
                    sys_logging("get queue type:%d"%a.value.u32)
                    if a.value.u32 != queue_type1:
                        raise NotImplementedError() 
                if a.id == SAI_QUEUE_ATTR_PORT:
                    sys_logging("get port:0x%x" %a.value.oid)
                    if a.value.oid != port2:
                        raise NotImplementedError()    
                if a.id == SAI_QUEUE_ATTR_INDEX:
                    sys_logging("get index:%d"%a.value.u8)
                    if a.value.u8 != queue_index_list[1]:
                        raise NotImplementedError()    
                if a.id == SAI_QUEUE_ATTR_SERVICE_ID:
                    sys_logging("get service id:%d"%a.value.u16)
                    if a.value.u16 != sched_group_service_id2:
                        raise NotImplementedError()
            
                        
        finally:
            self.client.sai_thrift_remove_queue(queueId1)
            self.client.sai_thrift_remove_queue(queueId2)

class fun_04_create_invalid_index_service_type_queue_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create service type queue with invalid index 
        step2:verify queue oid
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[1]
        port2 = port_list[2]
        queue_index = 8
        queue_type1 = SAI_QUEUE_TYPE_SERVICE
        sched_group_service_id = 1

        warmboot(self.client)
        try:
            queueId1 = sai_thrift_create_queue_id(self.client, queue_type1, port, queue_index, service_id=sched_group_service_id) 
            sys_logging("queue_id:0x%x" %queueId1)
            assert(queueId1 == SAI_NULL_OBJECT_ID)
        finally:
            pass


class fun_05_remove_normal_types_queue_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create wred
        step2:create 3 type queues
        step3:wred bind queue
        step4:verify queues attr
        step5:remove all queue
        step6:verify queues attr again
        step7:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[1]
        queue_index1 = 1
        queue_index2 = 2
        queue_index3 = 3
        queue_index4 = 4
        queue_type1 = SAI_QUEUE_TYPE_ALL
        queue_type2 = SAI_QUEUE_TYPE_UNICAST
        queue_type3 = SAI_QUEUE_TYPE_MULTICAST
        queue_type4 = SAI_QUEUE_TYPE_SERVICE
        sched_group_service_id = 20

        color_en = [0,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        ecn_thrd = [1500,1300,150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)

        queueId1 = sai_thrift_create_queue_id(self.client, queue_type1, port, queue_index1, wred_id=wred_id) 

        queueId2 = sai_thrift_create_queue_id(self.client, queue_type2, port, queue_index2, wred_id=wred_id) 

        queueId3 = sai_thrift_create_queue_id(self.client, queue_type3, port, queue_index3, wred_id=wred_id) 

        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId1)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_queue_attribute(queueId2)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError() 
                        
            attrs = self.client.sai_thrift_get_queue_attribute(queueId3)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

            status = self.client.sai_thrift_remove_queue(queueId1)
            sys_logging("remove queue status:%d"%status)
            status = self.client.sai_thrift_remove_queue(queueId2)
            sys_logging("remove queue status:%d"%status)
            status = self.client.sai_thrift_remove_queue(queueId3)
            sys_logging("remove queue status:%d"%status)


            attrs = self.client.sai_thrift_get_queue_attribute(queueId1)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_queue_attribute(queueId2)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError() 
                        
            attrs = self.client.sai_thrift_get_queue_attribute(queueId3)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

                        
        finally:
            self.client.sai_thrift_remove_wred_profile(wred_id)



class fun_06_set_normal_queue_attr_wred_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create wred
        step2:create all type queue
        step3:wred bind queue
        step4:verify queues attr
        step5:remove all type queue
        step7:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[1]
        queue_index1 = 1
        queue_type1 = SAI_QUEUE_TYPE_ALL

        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        ecn_thrd = [1500,1300,150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        #pdb.set_trace()
        queueId1 = sai_thrift_create_queue_id(self.client, queue_type1, port, queue_index1, wred_id=wred_id) 

        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId1)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

                        
        finally:
            self.client.sai_thrift_remove_queue(queueId1)
            self.client.sai_thrift_remove_wred_profile(wred_id)

class fun_07_set_service_type_queue_attr_wred_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        
        sys_logging("start test")
        switch_init(self.client)
        print chipname
        if chipname != 'tsingma':
            return
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


        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        ecn_thrd = [1500,1300,150]
        wred_id1= sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)

        
        #port level
        sched_group_id_root[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        
        parent_id[1] = sched_group_id_root[0]
        sched_group_id_chan_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        sched_group_id_chan_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        

        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)      
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node[1], 0, service_id=sched_group_service_id)

        
        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = 0
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, wred_id=wred_id1, parent_id=sched_group_id_group_node[0], service_id=sched_group_service_id)
        
        queue_index = 1
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0, parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id)
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()

                        
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()


            attr_value = sai_thrift_attribute_value_t(oid=wred_id1)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()
            
                        
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()
                

        finally:
            self.client.sai_thrift_remove_queue(service_queueId[0])
            self.client.sai_thrift_remove_queue(service_queueId[1])
            
            for ii in range(3):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            for ii in range(2):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node[ii])
            for ii in range(1):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_root[ii])
            self.client.sai_thrift_remove_wred_profile(wred_id1)


class fun_07_set_service_type_queue_attr_wred_fn_tmm(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        if chipname != 'tsingma_mx':
            return
        
        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        ecn_thrd = [1500,1300,150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)


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
        level = [0,1,2,3,4,5]
        max_childs = [12, 100, 100, 100, 100, 8]
        root_sched_group = [None]*1
        level1_sched_group = [None]*4
        level2_sched_group1 = [None]*4
        level3_sched_group1 = [None]*4
        level4_sched_group1 = [None]*4
        level5_sched_group1 = [None]*8
        service1_queueId = [None]*8

        sched_group_service_id = [1,2,3,4,5,6,7,8,9,10,11]

        all_leve2_group = []
        all_leve3_group = []
        all_leve4_group = []
        all_leve5_group = []
        all_queue = []

        print 'create root group'
        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        print 'create level1 group'
        level1_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        
        #pdb.set_trace()
        print 'create level2 group'
        level2_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        all_leve2_group.append(level2_sched_group1)
      

        print 'create level3 group'
        level3_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        all_leve3_group.append(level3_sched_group1)


        print 'create level4 group'
        level4_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        all_leve4_group.append(level4_sched_group1)
        

        pdb.set_trace()
        print 'create level5 group'
        level5_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        all_leve5_group.append(level5_sched_group1)
        

        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service1_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group1[0], sche_id=sched_oid1, service_id=sched_group_service_id[0], wred_id=wred_id)        
        service1_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group1[1], sche_id=sched_oid5, service_id=sched_group_service_id[0])
        service1_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group1[1], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service1_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group1[3], sche_id=sched_oid2, service_id=sched_group_service_id[0])
        service1_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group1[4], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service1_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group1[4], sche_id=sched_oid5, service_id=sched_group_service_id[0])
        service1_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group1[4], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service1_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group1[7], sche_id=sched_oid3, service_id=sched_group_service_id[0])
        all_queue.append(service1_queueId)
        
        
        
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(service1_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

                        
            attrs = self.client.sai_thrift_get_queue_attribute(service1_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(oid=wred_id)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service1_queueId[1], attr)

            attrs = self.client.sai_thrift_get_queue_attribute(service1_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()
            
                        
            attrs = self.client.sai_thrift_get_queue_attribute(service1_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get queue wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()
                

        finally:
            for j in all_queue:
                for i in j:
                    self.client.sai_thrift_remove_queue(i)
            #pdb.set_trace()
            for j in all_leve5_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            #pdb.set_trace()
            for j in all_leve4_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            #pdb.set_trace()
            for j in all_leve3_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            for j in all_leve2_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            for i in level1_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in root_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid5)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid6)
            self.client.sai_thrift_remove_wred_profile(wred_id)


class fun_08_set_normal_queue_attr_buffer_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Get Port Ingress Priority Group List Test
        step1:Get Port Attrs
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[1]
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 2000000
        dynamic_th = 0
        xon_th = 1000000
        xoff_th = 1200000
        queueId_list = []

        buf_prof_id = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        assert(0 != buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X"%buf_prof_id)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                    attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
        #pdb.set_trace()
        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queueId_list[ii], a.value.oid))
                        if a.value.oid != buf_prof_id:
                            raise NotImplementedError() 
        finally:
            for i in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                self.client.sai_thrift_remove_queue(queueId_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

class fun_09_set_service_type_queue_attr_buffer_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        
        sys_logging("start test")
        switch_init(self.client)
        if chipname != 'tsingma':
            return
        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 64, 8]
        sched_group_id_group_node = [None]*8
        sched_group_service_id = 1
        service_queueId = [None]*8


        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 2000000
        dynamic_th = 0
        xon_th = 1000000
        xoff_th = 1200000
        buf_prof_id1 = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = -2
        xon_th = 1000000
        xoff_th = 1200000
        buf_prof_id2 = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)

        
        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        sched_group_id_chan_node = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        
        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)      
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)      
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)

        
        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=sched_group_id_group_node[0], service_id=sched_group_service_id, buffer_id=buf_prof_id1)        
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        service_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        service_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id)
        service_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id)
        service_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=sched_group_id_group_node[6], service_id=sched_group_service_id)
        service_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=sched_group_id_group_node[6], service_id=sched_group_service_id)
        #pdb.set_trace()

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()


            attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id1)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
            #pdb.set_trace()


            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                

        finally:
            for i in range(8):
                self.client.sai_thrift_remove_queue(service_queueId[i])
            
            for ii in range(8):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id1)
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id2)


class fun_09_set_service_type_queue_attr_buffer_fn_tmm(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        
        sys_logging("start test")
        switch_init(self.client)
        if chipname != 'tsingma_mx':
            return

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 2000000
        dynamic_th = 0
        xon_th = 1000000
        xoff_th = 1200000
        buf_prof_id1 = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = -2
        xon_th = 1000000
        xoff_th = 1200000
        buf_prof_id2 = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)

        
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
        level = [0,1,2,3,4,5]
        max_childs = [12, 100, 100, 100, 100, 8]
        root_sched_group = [None]*1
        level1_sched_group = [None]*4
        level2_sched_group1 = [None]*4
        level3_sched_group1 = [None]*4
        level4_sched_group1 = [None]*4
        level5_sched_group1 = [None]*8
        service_queueId = [None]*8

        sched_group_service_id = [1,2,3,4,5,6,7,8,9,10,11]

        all_leve2_group = []
        all_leve3_group = []
        all_leve4_group = []
        all_leve5_group = []
        all_queue = []

        print 'create root group'
        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        print 'create level1 group'
        level1_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        
        #pdb.set_trace()
        print 'create level2 group'
        level2_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        all_leve2_group.append(level2_sched_group1)
      

        print 'create level3 group'
        level3_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        all_leve3_group.append(level3_sched_group1)


        print 'create level4 group'
        level4_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        all_leve4_group.append(level4_sched_group1)
        

        #pdb.set_trace()
        print 'create level5 group'
        level5_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        all_leve5_group.append(level5_sched_group1)
        

        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group1[0], sche_id=sched_oid1, service_id=sched_group_service_id[0], buffer_id=buf_prof_id1)        
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group1[1], sche_id=sched_oid5, service_id=sched_group_service_id[0], buffer_id=buf_prof_id2)
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group1[1], sche_id=sched_oid6, service_id=sched_group_service_id[0], buffer_id=buf_prof_id1)
        service_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group1[3], sche_id=sched_oid2, service_id=sched_group_service_id[0], buffer_id=buf_prof_id2)
        service_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group1[4], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group1[4], sche_id=sched_oid5, service_id=sched_group_service_id[0])
        service_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group1[4], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group1[7], sche_id=sched_oid3, service_id=sched_group_service_id[0])
        all_queue.append(service_queueId)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id1)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
            #pdb.set_trace()


            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                

        finally:
            for j in all_queue:
                for i in j:
                    self.client.sai_thrift_remove_queue(i)
            
            for j in all_leve5_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            
            for j in all_leve4_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            
            for j in all_leve3_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            for j in all_leve2_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            for i in level1_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in root_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid5)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid6)
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id1)
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id2)



class fun_10_set_normal_queue_attr_scheduler_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Get Port Ingress Priority Group List Test
        step1:Get Port Attrs
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
        sys_logging("sched_oid_1 0x%x"%sched_oid2)
        sched_oid_list = [sched_oid1, sched_oid2]
        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                    attr_value = sai_thrift_attribute_value_t(oid=sched_oid_list[i%2])
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
        #pdb.set_trace()
        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] scheduler Profile oid: 0x%x"%(queueId_list[ii], a.value.oid))
                        if a.value.oid != sched_oid_list[ii%2]:
                            raise NotImplementedError() 
            for i in range(8):
                attr_value = sai_thrift_attribute_value_t(oid=sched_oid_list[(i+1)%2])
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
            #pdb.set_trace()
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] scheduler Profile oid: 0x%x"%(queueId_list[ii], a.value.oid))
                        if a.value.oid != sched_oid_list[(ii+1)%2]:
                            raise NotImplementedError() 
        finally:
            for i in range(queue_num):
                self.client.sai_thrift_remove_queue(queueId_list[i])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)


class fun_11_set_service_type_queue_attr_scheduler_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        
        sys_logging("start test")
        switch_init(self.client)
        if chipname != 'tsingma':
            return
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 64, 8]
        sched_group_id_group_node = [None]*8
        sched_group_service_id = 1
        service_queueId = [None]*8


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
        sys_logging("sched_oid_1 0x%x"%sched_oid2)
        sched_oid_list = [sched_oid1, sched_oid2]

        
        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        sched_group_id_chan_node = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        
        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)      
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)      
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)

        
        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=sched_group_id_group_node[0], service_id=sched_group_service_id, sche_id=sched_oid1)        
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, sche_id=sched_oid2)
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, sche_id=sched_oid2)
        service_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, sche_id=sched_oid1)
        service_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=sched_group_id_group_node[4], service_id=sched_group_service_id)
        service_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=sched_group_id_group_node[4], service_id=sched_group_service_id)
        service_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=sched_group_id_group_node[4], service_id=sched_group_service_id)
        service_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=sched_group_id_group_node[7], service_id=sched_group_service_id)
        #pdb.set_trace()

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()


            attr_value = sai_thrift_attribute_value_t(oid=sched_oid2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            
            self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_oid1)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
            
            


            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError()
                

        finally:
            #pdb.set_trace()
            for ii in range(8):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)

            #pdb.set_trace()
            for i in range(8):
                self.client.sai_thrift_remove_queue(service_queueId[i])

            for ii in range(8):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)

            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)


class fun_11_set_service_type_queue_attr_scheduler_fn_tmm(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        if chipname != 'tsingma_mx':
            return

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
        level = [0,1,2,3,4,5]
        max_childs = [12, 100, 100, 100, 100, 8]
        root_sched_group = [None]*1
        level1_sched_group = [None]*4
        level2_sched_group1 = [None]*4
        level3_sched_group1 = [None]*4
        level4_sched_group1 = [None]*4
        level5_sched_group1 = [None]*8
        service_queueId = [None]*8

        sched_group_service_id = [1,2,3,4,5,6,7,8,9,10,11]

        all_leve2_group = []
        all_leve3_group = []
        all_leve4_group = []
        all_leve5_group = []
        all_queue = []

        print 'create root group'
        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        print 'create level1 group'
        level1_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        
        
        print 'create level2 group'
        level2_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        all_leve2_group.append(level2_sched_group1)
      

        print 'create level3 group'
        level3_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        all_leve3_group.append(level3_sched_group1)


        print 'create level4 group'
        level4_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        all_leve4_group.append(level4_sched_group1)
        

        
        print 'create level5 group'
        level5_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        all_leve5_group.append(level5_sched_group1)
        

        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group1[0], sche_id=sched_oid1, service_id=sched_group_service_id[0])        
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group1[1], sche_id=sched_oid5, service_id=sched_group_service_id[0])
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group1[1], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group1[3], sche_id=sched_oid2, service_id=sched_group_service_id[0])
        service_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=level5_sched_group1[4], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=level5_sched_group1[4], sche_id=sched_oid5, service_id=sched_group_service_id[0])
        service_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=level5_sched_group1[4], service_id=sched_group_service_id[0])
        service_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=level5_sched_group1[7], service_id=sched_group_service_id[0])
        all_queue.append(service_queueId)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid5:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid6:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid6:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid5:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(oid=sched_oid3)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_oid4)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_oid2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
            
            


            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid5:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid6:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid3:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid6:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid4:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid4:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()
                

        finally:
            for j in all_queue:
                for i in j:
                    self.client.sai_thrift_remove_queue(i)
            
            for j in all_leve5_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            
            for j in all_leve4_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            
            for j in all_leve3_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            for j in all_leve2_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            for i in level1_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in root_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid5)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid6)



class fun_12_set_normal_queue_attr_parent_node_fn(sai_base_test.ThriftInterfaceDataPlane):
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
        sys_logging("sched_oid_1 0x%x"%sched_oid2)
        sched_oid_list = [sched_oid1, sched_oid2]

        
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
        self.client.sai_thrift_set_queue_attribute(queueId_list[5], attr)
        self.client.sai_thrift_set_queue_attribute(queueId_list[6], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[7])
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[7], attr)
        

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[0]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[1]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[1]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[3]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[7]:
                        raise NotImplementedError()

            sys_logging("=======set queue scheduler profile=======")
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

            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid2:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    sys_logging("get queue scheduler profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_oid1:
                        raise NotImplementedError()


            sys_logging("=======remove queue parent node profile=======")
            
            for ii in range(8):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)

            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()


            

            sys_logging("=======set queue parent node profile again=======")
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

            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[0]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[1]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[1]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[3]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[7]:
                        raise NotImplementedError()

        finally:

            
            for i in range(8):
                self.client.sai_thrift_remove_queue(queueId_list[i])

            for ii in range(8):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)

            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)

class fun_13_set_service_type_queue_attr_parent_node_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        
        sys_logging("start test")
        switch_init(self.client)
        if chipname != 'tsingma':
            return
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 64, 8]
        sched_group_id_group_node = [None]*8
        sched_group_service_id = 1
        service_queueId = [None]*8


        sched_type1 = SAI_SCHEDULING_TYPE_STRICT
        sched_type2 = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 2000000
        cbs = 256000
        pir = 1000000
        pbs = 64000

        sched_oid1 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type1, 0, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid1)

        sched_oid2 = sai_thrift_qos_create_scheduler_profile(self.client, sched_type2, sched_weight, cir, cbs, pir, pbs)
        sys_logging("sched_oid_1 0x%x"%sched_oid2)
        sched_oid_list = [sched_oid1, sched_oid2]

        
        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        sched_group_id_chan_node = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)
        
        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)      
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)      
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)

        
        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=sched_group_id_group_node[0], service_id=sched_group_service_id, sche_id=sched_oid1)        
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, sche_id=sched_oid2)
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, sche_id=sched_oid2)
        service_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, sche_id=sched_oid1)
        service_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], service_id=sched_group_service_id, sche_id=sched_oid2)
        service_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], service_id=sched_group_service_id, sche_id=sched_oid2)
        service_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], service_id=sched_group_service_id, sche_id=sched_oid2)
        service_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], service_id=sched_group_service_id, sche_id=sched_oid1)
        #pdb.set_trace()

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[0]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[1]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[1]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[3]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()


            attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[4])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[7])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
            
            


            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[0]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[1]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[1]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[3]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[7]:
                        raise NotImplementedError()


            for ii in range(8):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[0])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[1])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[3])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[4])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=sched_group_id_group_node[7])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[0]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[1]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[1]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[3]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != sched_group_id_group_node[7]:
                        raise NotImplementedError()

        finally:
            #pdb.set_trace()
            for ii in range(8):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)

            #pdb.set_trace()
            for i in range(8):
                self.client.sai_thrift_remove_queue(service_queueId[i])

            for ii in range(8):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)

            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)


class fun_13_set_service_type_queue_attr_parent_node_fn_tmm(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        if chipname != 'tsingma_mx':
            return

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
        level = [0,1,2,3,4,5]
        max_childs = [12, 100, 100, 100, 100, 8]
        root_sched_group = [None]*1
        level1_sched_group = [None]*4
        level2_sched_group1 = [None]*4
        level3_sched_group1 = [None]*4
        level4_sched_group1 = [None]*4
        level5_sched_group1 = [None]*8
        service_queueId = [None]*8

        sched_group_service_id = [1,2,3,4,5,6,7,8,9,10,11]

        all_leve2_group = []
        all_leve3_group = []
        all_leve4_group = []
        all_leve5_group = []
        all_queue = []

        print 'create root group'
        root_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        
        print 'create level1 group'
        level1_sched_group[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        level1_sched_group[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], root_sched_group[0])
        
        
        print 'create level2 group'
        level2_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        level2_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], level1_sched_group[0], sched_oid4)
        all_leve2_group.append(level2_sched_group1)
      

        print 'create level3 group'
        level3_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        level3_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[3], max_childs[3], level2_sched_group1[0], sched_oid4)
        all_leve3_group.append(level3_sched_group1)


        print 'create level4 group'
        level4_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        level4_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[4], max_childs[4], level3_sched_group1[0], sched_oid4)
        all_leve4_group.append(level4_sched_group1)
        

        
        print 'create level5 group'
        level5_sched_group1[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        level5_sched_group1[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[5], max_childs[5], level4_sched_group1[2], sched_oid4, service_id=sched_group_service_id[0])
        all_leve5_group.append(level5_sched_group1)
        

        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=level5_sched_group1[0], sche_id=sched_oid1, service_id=sched_group_service_id[0])        
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=level5_sched_group1[1], sche_id=sched_oid5, service_id=sched_group_service_id[0])
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=level5_sched_group1[1], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=level5_sched_group1[3], sche_id=sched_oid2, service_id=sched_group_service_id[0])
        service_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], sche_id=sched_oid5, service_id=sched_group_service_id[0])
        service_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], sche_id=sched_oid6, service_id=sched_group_service_id[0])
        service_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], sche_id=sched_oid3, service_id=sched_group_service_id[0])
        all_queue.append(service_queueId)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[0]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[1]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[1]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[3]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            
            attr_value = sai_thrift_attribute_value_t(oid=level5_sched_group1[4])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=level5_sched_group1[7])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
            
            


            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[0]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[1]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[1]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[3]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[4]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[7]:
                        raise NotImplementedError()

            
            for ii in range(8):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(service_queueId[ii], attr)

            attr_value = sai_thrift_attribute_value_t(oid=level5_sched_group1[0])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)

            attr_value = sai_thrift_attribute_value_t(oid=level5_sched_group1[1])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)

            attr_value = sai_thrift_attribute_value_t(oid=level5_sched_group1[3])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)

            attr_value = sai_thrift_attribute_value_t(oid=level5_sched_group1[4])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)

            attr_value = sai_thrift_attribute_value_t(oid=level5_sched_group1[7])
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
            

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[0]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[1]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[1]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[3]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[4]:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[4]:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                    sys_logging("get queue parent node profile:0x%x"%a.value.oid)
                    if a.value.oid != level5_sched_group1[7]:
                        raise NotImplementedError()

        finally:
            for j in all_queue:
                for i in j:
                    self.client.sai_thrift_remove_queue(i)
            
            for j in all_leve5_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            
            for j in all_leve4_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            
            for j in all_leve3_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            for j in all_leve2_group:
                for i in j:
                    self.client.sai_thrift_remove_scheduler_group(i)
            for i in level1_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            for i in root_sched_group:
                self.client.sai_thrift_remove_scheduler_group(i)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid2)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid3)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid4)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid5)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid6)




class fun_14_set_queue_attr_enable_pfc_dldr_fn(sai_base_test.ThriftInterfaceDataPlane):
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

        sys_logging("=======set queue pfc_dldr_enable=======")
        pfc_dldr_enable = 1
        pfc_dldr_disable = 0

        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(booldata=pfc_dldr_enable)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_ENABLE_PFC_DLDR, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=pfc_dldr_enable)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_ENABLE_PFC_DLDR, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[7], attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=pfc_dldr_enable)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_ENABLE_PFC_DLDR, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)

            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
                    sys_logging("get queue pfc dldr enable:%d"%a.value.booldata)
                    if a.value.booldata != pfc_dldr_enable:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
                    sys_logging("get queue pfc dldr enable:%d"%a.value.booldata)
                    if a.value.booldata != pfc_dldr_enable:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
                    sys_logging("get queue pfc dldr enable:%d"%a.value.booldata)
                    if a.value.booldata != pfc_dldr_disable:
                        raise NotImplementedError()   



            attr_value = sai_thrift_attribute_value_t(booldata=pfc_dldr_disable)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_ENABLE_PFC_DLDR, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[7], attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=pfc_dldr_enable)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_ENABLE_PFC_DLDR, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)

            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
                    sys_logging("get queue pfc dldr enable:%d"%a.value.booldata)
                    if a.value.booldata != pfc_dldr_enable:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
                    sys_logging("get queue pfc dldr enable:%d"%a.value.booldata)
                    if a.value.booldata != pfc_dldr_disable:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
                    sys_logging("get queue pfc dldr enable:%d"%a.value.booldata)
                    if a.value.booldata != pfc_dldr_enable:
                        raise NotImplementedError()   



            
            attr_value = sai_thrift_attribute_value_t(booldata=pfc_dldr_disable)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_ENABLE_PFC_DLDR, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
            
            attr_value = sai_thrift_attribute_value_t(booldata=pfc_dldr_disable)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_ENABLE_PFC_DLDR, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[2], attr)

            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
                    sys_logging("get queue pfc dldr enable:%d"%a.value.booldata)
                    if a.value.booldata != pfc_dldr_disable:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
                    sys_logging("get queue pfc dldr enable:%d"%a.value.booldata)
                    if a.value.booldata != pfc_dldr_disable:
                        raise NotImplementedError()   
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_ENABLE_PFC_DLDR:
                    sys_logging("get queue pfc dldr enable:%d"%a.value.booldata)
                    if a.value.booldata != pfc_dldr_disable:
                        raise NotImplementedError() 

        finally:

            
            for i in range(8):
                self.client.sai_thrift_remove_queue(queueId_list[i])
            
            for ii in range(8):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node)
            self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)


class func_15_queue_stats_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_02_trunk_port----- ###")
        switch_init(self.client)
        if chipname != 'tsingma_mx':
            return
        vlan_id1 = 30
        port1 = port_list[0]
        port2 = port_list[30]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        basic_queueId=[None]*8
        queue_type = SAI_QUEUE_TYPE_ALL
        queue_index = [0,1,2,3,4,5,6,7]
        basic_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port2, queue_index[0])        
        basic_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port2, queue_index[1])
        basic_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port2, queue_index[2])
        basic_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port2, queue_index[3])
        basic_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port2, queue_index[4])
        basic_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port2, queue_index[5])
        basic_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port2, queue_index[6])
        basic_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port2, queue_index[7])
        #pdb.set_trace()

        
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)

        pkt_list=[]
        for i in range(8):
            pkt = simple_tcp_packet(pktlen=96,
                                     eth_dst=mac2,
                                     eth_src=mac1,
                                     dl_vlan_enable=True,
                                     vlan_vid=30,
                                     vlan_pcp=i,
                                     dl_vlan_cfi=0,
                                     ip_dst='1.1.1.1',
                                     ip_src='2.2.2.2',
                                     ip_id=105,
                                     ip_ttl=64,
                                     ip_ihl=5)
            pkt_list.append(pkt)

        warmboot(self.client)

        try:
            for i in range(8):
                counter_ids = [SAI_QUEUE_STAT_PACKETS, SAI_QUEUE_STAT_DROPPED_PACKETS]
                self.client.sai_thrift_clear_queue_stats(basic_queueId[i], counter_ids, 2)
                list1 = self.client.sai_thrift_get_queue_stats(basic_queueId[i], counter_ids, 2)
                print list1
                assert (list1[0] == 0)
                assert (list1[1] == 0)
            for i in range(8):
                self.ctc_send_packet(0, str(pkt_list[i]))
                self.ctc_verify_packets( str(pkt_list[i]), [30], 1)
                counter_ids = [SAI_QUEUE_STAT_PACKETS, SAI_QUEUE_STAT_DROPPED_PACKETS]
                list1 = self.client.sai_thrift_get_queue_stats(basic_queueId[i], counter_ids, 2)
                print list1
                assert (list1[0] == 1)
                assert (list1[1] == 0)
            for i in range(8):
                self.ctc_send_packet(0, str(pkt_list[i]))
                self.ctc_verify_packets( str(pkt_list[i]), [30], 1)
                counter_ids = [SAI_QUEUE_STAT_PACKETS, SAI_QUEUE_STAT_DROPPED_PACKETS]
                list1 = self.client.sai_thrift_get_queue_stats_ext(basic_queueId[i], counter_ids, 2, 0)
                print list1
                assert (list1[0] == 2)
                assert (list1[1] == 0)
            for i in range(8):
                self.ctc_send_packet(0, str(pkt_list[i]))
                self.ctc_verify_packets( str(pkt_list[i]), [30], 1)
                counter_ids = [SAI_QUEUE_STAT_PACKETS, SAI_QUEUE_STAT_DROPPED_PACKETS]
                list1 = self.client.sai_thrift_get_queue_stats_ext(basic_queueId[i], counter_ids, 2, 1)
                print list1
                assert (list1[0] == 3)
                assert (list1[1] == 0)
            for i in range(8):
                self.ctc_send_packet(0, str(pkt_list[i]))
                self.ctc_verify_packets( str(pkt_list[i]), [30], 1)
                counter_ids = [SAI_QUEUE_STAT_PACKETS, SAI_QUEUE_STAT_DROPPED_PACKETS]
                list1 = self.client.sai_thrift_get_queue_stats(basic_queueId[i], counter_ids, 2)
                print list1
                assert (list1[0] == 1)
                assert (list1[1] == 0)
            for i in range(8):
                counter_ids = [SAI_QUEUE_STAT_PACKETS, SAI_QUEUE_STAT_DROPPED_PACKETS]
                self.client.sai_thrift_clear_queue_stats(basic_queueId[i], counter_ids, 2)
                list1 = self.client.sai_thrift_get_queue_stats(basic_queueId[i], counter_ids, 2)
                print list1
                assert (list1[0] == 0)
                assert (list1[1] == 0)
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2)


            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            for i in range(8):
                self.client.sai_thrift_remove_queue(basic_queueId[i])
            



