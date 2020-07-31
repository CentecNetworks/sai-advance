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

@group('Buffer')
class PortGetIngressPGListTest(sai_base_test.ThriftInterfaceDataPlane):
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
        pg_list = []

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:           
            if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                sys_logging("Ingress PG Num:",a.value.u32)
                assert(0 != a.value.u32)
            if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                for i in range(a.value.objlist.count):
                    pg_list.append(a.value.objlist.object_id_list[i])
                    assert(0 != pg_list[i])
                    sys_logging("Ingress PG List[%d]:0x%x"%(i, a.value.objlist.object_id_list[i]))
        try:
            pass
        finally:
            pass

@group('Buffer')
class PortEnableFlowCtlTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Port Enable Flow Contorl Test
        step1:Get Port Attrs
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[1]

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL:
                sys_logging("default flowctl:", a.value.u8)
                flowctl = a.value.u8

        flowctl = -1
        attr_value = sai_thrift_attribute_value_t(u8=flowctl)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port, attr)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL:
                    sys_logging("default flowctl:", a.value.u8)
                    if flowctl != a.value.u8:
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(u8=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port, attr)

@group('Buffer')
class BufferProfileCreateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create Buffer Profile Id Test
        step1:Create Buffer Profile Id
        step2:verify 
        step3:clean up
        """
        
        sys_logging("start test")
        switch_init(self.client)
        
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 2000000
        dynamic_th = 0
        xon_th = 1000000
        xoff_th = 1200000

        buf_prof_id = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        assert(0 != buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X"%buf_prof_id)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_id)
            for a in attrs.attr_list:
                if a.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                    if a.value.s32 != th_mode:
                        raise NotImplementedError() 
                if a.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                    if a.value.s8 != dynamic_th:
                        raise NotImplementedError()
                if a.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                    if a.value.u32 != static_th:
                        raise NotImplementedError()
                if a.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                    if a.value.u32 != xoff_th:
                        raise NotImplementedError()
                if a.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                    if a.value.u32 != xon_th:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class PortSetIngressPGBindBufferProfileTest(sai_base_test.ThriftInterfaceDataPlane):
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
        pg_list = []

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:           
            if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                pg_num = a.value.u32
                sys_logging("Ingress PG Num:",a.value.u32)
            if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                for i in range(a.value.objlist.count):
                    pg_list.append(a.value.objlist.object_id_list[i])
                    assert(0 != pg_list[i])
                    sys_logging("Ingress PG List[%d]:0x%x"%(i, a.value.objlist.object_id_list[i]))

        buf_prof_id = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        assert(0 != buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X"%buf_prof_id)

        for i in range(pg_num):
            attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
            attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
            self.client.sai_thrift_set_priority_group_attribute(pg_list[i], attr)

        warmboot(self.client)
        try:
            for i in range(pg_num):
                sys_logging("Get PG:0x%x    >>>"%pg_list[i])
                attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        sys_logging("<<< Buffer Oid:0x%x"%a.value.oid)
                        if a.value.oid != buf_prof_id:
                            raise NotImplementedError()
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT:
                        sys_logging("<<< Port Oid:0x%x"%a.value.oid)
                        if a.value.oid != port:
                            raise NotImplementedError()    
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX:
                        sys_logging("<<< Index:",a.value.u8)
                        if a.value.u8 != i:
                            raise NotImplementedError() 
        finally:
            for i in range(pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                self.client.sai_thrift_set_priority_group_attribute(pg_list[i], attr)
                self.client.sai_thrift_remove_priority_group(pg_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class PortSetIngressPGBindBufferProfUpdateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Get Port Ingress Priority Group List Test
        step1:Get Port Attrs & Create Buffer Profile
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
        pg_list = []

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:           
            if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                pg_num = a.value.u32
                sys_logging("Ingress PG Num:",a.value.u32)
            if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                for i in range(a.value.objlist.count):
                    pg_list.append(a.value.objlist.object_id_list[i])
                    assert(0 != pg_list[i])
                    sys_logging("Ingress PG List[%d]:0x%x"%(i, a.value.objlist.object_id_list[i]))

        buf_prof_id = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        assert(0 != buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X"%buf_prof_id)

        for i in range(pg_num):
            attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
            attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
            self.client.sai_thrift_set_priority_group_attribute(pg_list[i], attr)

        xoff_th = 2000000
        xon_th  = 1500000
        attr_value = sai_thrift_attribute_value_t(u32=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_id, attr)

        attr_value = sai_thrift_attribute_value_t(u32=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_id, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_id)
            for a in attrs.attr_list:  
                if a.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                    sys_logging("Get xoff_th:", a.value.u32)
                    if a.value.u32 != xoff_th:
                        raise NotImplementedError()
                if a.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                    sys_logging("Get xon_th:", a.value.u32)
                    if a.value.u32 != xon_th:
                        raise NotImplementedError()
        finally:
            for i in range(pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                self.client.sai_thrift_set_priority_group_attribute(pg_list[i], attr)
                self.client.sai_thrift_remove_priority_group(pg_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class QueueBindBufferProfileStaticModeTest(sai_base_test.ThriftInterfaceDataPlane):
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
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                self.client.sai_thrift_remove_queue(queueId_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class QueueBindBufferProfileDynamicModeTest(sai_base_test.ThriftInterfaceDataPlane):
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
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = -2
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
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                self.client.sai_thrift_remove_queue(queueId_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class QueueBindBufferProfileUpdateTest(sai_base_test.ThriftInterfaceDataPlane):
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
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = -2
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

        dynamic_th = 1
        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_id, attr)

        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queueId_list[ii], a.value.oid))
                        if a.value.oid != buf_prof_id:
                            raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_id)
            for a in attrs.attr_list:  
                if a.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                    sys_logging("Get dynamic_th:", a.value.s8)
                    if a.value.s8 != dynamic_th:
                        raise NotImplementedError() 
        finally:
            for i in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                self.client.sai_thrift_remove_queue(queueId_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)