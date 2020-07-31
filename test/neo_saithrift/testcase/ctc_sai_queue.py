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
        color_en = [0,0,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        sys_logging("wred_id:",wred_id)

        #Create Queue Id
        queueId = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_UNICAST, port, queue_index, 0) 
        sys_logging("queue_id:",queueId)

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


