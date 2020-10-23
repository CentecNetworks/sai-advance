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
class fun_01_port_get_ingress_pg_list_test(sai_base_test.ThriftInterfaceDataPlane):
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
class fun_02_port_enable_flow_ctl_test(sai_base_test.ThriftInterfaceDataPlane):
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
class fun_03_buffer_profile_create_test(sai_base_test.ThriftInterfaceDataPlane):
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
                    if a.value.u64 != static_th:
                        raise NotImplementedError()
                if a.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                    if a.value.u64 != xoff_th:
                        raise NotImplementedError()
                if a.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                    if a.value.u64 != xon_th:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class fun_04_port_set_ingress_pg_bind_buffer_profile_test(sai_base_test.ThriftInterfaceDataPlane):
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
class fun_05_port_set_ingress_pg_bind_buffer_prof_update_test(sai_base_test.ThriftInterfaceDataPlane):
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
        xon_th = 100
        xoff_th = 120
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

        xon_th  = 200
        xoff_th = 240
        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_id, attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_id, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_id)
            for a in attrs.attr_list:
                if a.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                    sys_logging("Get xoff_th:", a.value.u64)
                    if a.value.u64 != xoff_th:
                        raise NotImplementedError()
                if a.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                    sys_logging("Get xon_th:", a.value.u64)
                    if a.value.u64 != xon_th:
                        raise NotImplementedError()
        finally:
            for i in range(pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                self.client.sai_thrift_set_priority_group_attribute(pg_list[i], attr)
                self.client.sai_thrift_remove_priority_group(pg_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class fun_06_queue_bind_buffer_profile_static_mode_test(sai_base_test.ThriftInterfaceDataPlane):
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
class fun_07_queue_bind_buffer_profile_dynamic_mode_test(sai_base_test.ThriftInterfaceDataPlane):
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
class fun_08_queue_bind_buffer_profile_update_test(sai_base_test.ThriftInterfaceDataPlane):
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

@group('Buffer')
class fun_09_check_buffer_profile_wtd_static_threshold_para_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        port = port_list[0]
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 32768*288
        dynamic_th = 0
        xon_th = 224*288
        xoff_th = 256*288
        queue_id_list = []

        attr_list = []
        attr_value = sai_thrift_attribute_value_t(u64=static_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

        buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL == buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X" %buf_prof_id)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        attr_value = sai_thrift_attribute_value_t(s32=th_mode)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
        attr_list.append(attr)

        buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL == buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X" %buf_prof_id)

        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.remove(attr)

        buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL != buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X" %buf_prof_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS != status)

            static_th = 32767*288
            attr_value = sai_thrift_attribute_value_t(u64=static_th)
            attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
            self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_id, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                        attrs = self.client.sai_thrift_get_queue_attribute(queue_id_list[i])
                        for b in attrs.attr_list:
                            if b.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                                sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id_list[i], b.value.oid))
                                if b.value.oid != buf_prof_id:
                                    raise NotImplementedError()
                                buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_id)
                                for c in buffer_attrs.attr_list:
                                    if c.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                        if c.value.s32 != th_mode:
                                            raise NotImplementedError()
                                    if c.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                        if c.value.s8 != dynamic_th:
                                            raise NotImplementedError()
                                    if c.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                        if c.value.u64 != static_th:
                                            raise NotImplementedError()
                                    if c.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                        if c.value.u64 != xoff_th:
                                            raise NotImplementedError()
                                    if c.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                        if c.value.u64 != xon_th:
                                            raise NotImplementedError()

        finally:
            for i in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
                self.client.sai_thrift_remove_queue(queue_id_list[i])

            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class fun_10_check_buffer_profile_wtd_dynamic_threshold_para_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        port = port_list[0]
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 0
        dynamic_th = -8
        xon_th = 224*288
        xoff_th = 256*288
        queue_id_list = []

        attr_list = []
        attr_value = sai_thrift_attribute_value_t(u64=static_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

        buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL == buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X" %buf_prof_id)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        attr_value = sai_thrift_attribute_value_t(s32=th_mode)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
        attr_list.append(attr)

        buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL == buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X" %buf_prof_id)

        attr_value = sai_thrift_attribute_value_t(u64=static_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        attr_list.remove(attr)

        buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL == buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X" %buf_prof_id)

        dynamic_th = -8
        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.remove(attr)

        dynamic_th = 4
        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)

        buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL == buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X" %buf_prof_id)

        dynamic_th = 4
        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.remove(attr)

        dynamic_th = -7
        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)

        buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL != buf_prof_id)
        sys_logging("Create Buffer Profile id:0x%X" %buf_prof_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                        queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id_list[i])
                        for b in queue_attrs.attr_list:
                            if b.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                                sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id_list[i], b.value.oid))
                                if b.value.oid != buf_prof_id:
                                    raise NotImplementedError()
                                buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_id)
                                for c in buffer_attrs.attr_list:
                                    if c.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                        if c.value.s32 != th_mode:
                                            raise NotImplementedError()
                                    if c.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                        if c.value.s8 != dynamic_th:
                                            raise NotImplementedError()
                                    if c.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                        if c.value.u64 != static_th:
                                            raise NotImplementedError()
                                    if c.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                        if c.value.u64 != xoff_th:
                                            raise NotImplementedError()
                                    if c.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                        if c.value.u64 != xon_th:
                                            raise NotImplementedError()

        finally:
            for i in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
                self.client.sai_thrift_remove_queue(queue_id_list[i])

            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class fun_11_different_buffer_profile_threshold_mode_shared_between_ports(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        port0 = port_list[0]
        port1 = port_list[1]

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 32767*288
        dynamic_th = 3
        xon_th = 224*288
        xoff_th = 256*288
        static_queue_id_list = []
        dynamic_queue_id_list = []

        attr_list = []
        attr_value = sai_thrift_attribute_value_t(u64=static_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        attr_list.append(attr)

        #attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        #attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        #attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        attr_value = sai_thrift_attribute_value_t(s32=th_mode)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
        attr_list.append(attr)

        static_buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL != static_buf_prof_id)
        sys_logging("Create Static Buffer Profile id:0x%X" %static_buf_prof_id)

        attr_list = []
        #attr_value = sai_thrift_attribute_value_t(u64=static_th)
        #attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        #attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        attr_value = sai_thrift_attribute_value_t(s32=th_mode)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
        attr_list.append(attr)

        dynamic_buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL != dynamic_buf_prof_id)
        sys_logging("Create Dynamic Buffer Profile id:0x%X" %dynamic_buf_prof_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port0)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        static_queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                        attr_value = sai_thrift_attribute_value_t(oid=static_buf_prof_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(static_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            attrs = self.client.sai_thrift_get_port_attribute(port1)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        dynamic_queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                        attr_value = sai_thrift_attribute_value_t(oid=dynamic_buf_prof_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(dynamic_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_buffer_profile(static_buf_prof_id)
            assert (SAI_STATUS_SUCCESS != status)

            status = self.client.sai_thrift_remove_buffer_profile(dynamic_buf_prof_id)
            assert (SAI_STATUS_SUCCESS != status)

            for queue_id in static_queue_id_list:
                attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != static_buf_prof_id:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(static_buf_prof_id)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
                        dynamic_th = 0
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in dynamic_queue_id_list:
                attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != dynamic_buf_prof_id:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(dynamic_buf_prof_id)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        static_th = 0
                        dynamic_th = 3
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            static_queue_id_list = []
            dynamic_queue_id_list = []

            attrs = self.client.sai_thrift_get_port_attribute(port0)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        dynamic_queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                        attr_value = sai_thrift_attribute_value_t(oid=dynamic_buf_prof_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(dynamic_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            attrs = self.client.sai_thrift_get_port_attribute(port1)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        static_queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))
                        attr_value = sai_thrift_attribute_value_t(oid=static_buf_prof_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(static_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_buffer_profile(static_buf_prof_id)
            assert (SAI_STATUS_SUCCESS != status)

            status = self.client.sai_thrift_remove_buffer_profile(dynamic_buf_prof_id)
            assert (SAI_STATUS_SUCCESS != status)

            for queue_id in static_queue_id_list:
                attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != static_buf_prof_id:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(static_buf_prof_id)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
                        dynamic_th = 0
                        static_th = 32767*288
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in dynamic_queue_id_list:
                attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != dynamic_buf_prof_id:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(dynamic_buf_prof_id)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        static_th = 0
                        dynamic_th = 3
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            status = self.client.sai_thrift_remove_buffer_profile(static_buf_prof_id)
            assert (SAI_STATUS_SUCCESS != status)

            status = self.client.sai_thrift_remove_buffer_profile(dynamic_buf_prof_id)
            assert (SAI_STATUS_SUCCESS != status)

            for queue_id in dynamic_queue_id_list:
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                status = self.client.sai_thrift_set_queue_attribute(queue_id, attr)
                assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_buffer_profile(dynamic_buf_prof_id)
            assert (SAI_STATUS_SUCCESS == status)

            for queue_id in static_queue_id_list:
                attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != static_buf_prof_id:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(static_buf_prof_id)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
                        dynamic_th = 0
                        static_th = 32767*288
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in static_queue_id_list:
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                status = self.client.sai_thrift_set_queue_attribute(queue_id, attr)
                assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_buffer_profile(static_buf_prof_id)
            assert (SAI_STATUS_SUCCESS == status)

        finally:
            for queue_id in static_queue_id_list:
                self.client.sai_thrift_remove_queue(queue_id)

            for queue_id in dynamic_queue_id_list:
                self.client.sai_thrift_remove_queue(queue_id)

            self.client.sai_thrift_remove_buffer_profile(static_buf_prof_id)
            self.client.sai_thrift_remove_buffer_profile(dynamic_buf_prof_id)

@group('Buffer')
class fun_12_buffer_change_between_wred_and_wtd(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 32767*288
        dynamic_th = 3
        xon_th = 224*288
        xoff_th = 256*288
        queue_id_list = []

        attr_list = []
        attr_value = sai_thrift_attribute_value_t(u64=static_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        attr_list.append(attr)

        #attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        #attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        #attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        attr_value = sai_thrift_attribute_value_t(s32=th_mode)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
        attr_list.append(attr)

        static_buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL != static_buf_prof_id)
        sys_logging("Create Static Buffer Profile id:0x%X" %static_buf_prof_id)

        attr_list = []
        #attr_value = sai_thrift_attribute_value_t(u64=static_th)
        #attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        #attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        attr_value = sai_thrift_attribute_value_t(s32=th_mode)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
        attr_list.append(attr)

        dynamic_buf_prof_id = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL != dynamic_buf_prof_id)
        sys_logging("Create Dynamic Buffer Profile id:0x%X" %dynamic_buf_prof_id)

        #create Wred Id
        color_en = [1,1,1]
        min_thrd = [1500,700, 300]
        max_thrd = [3000,1500,700]
        drop_prob = [10, 30, 60]
        ecn_thrd = [2000,1000,500]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        assert (SAI_OBJECT_TYPE_NULL != wred_id)
        sys_logging("wred_id:", wred_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

                        attr_value = sai_thrift_attribute_value_t(oid=dynamic_buf_prof_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                        self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != dynamic_buf_prof_id:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(dynamic_buf_prof_id)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        static_th = 0
                        dynamic_th = 3
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                t = True
                                sys_logging("True:%d"%t)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1500:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 10:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

                        attr_value = sai_thrift_attribute_value_t(oid=static_buf_prof_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != static_buf_prof_id:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(static_buf_prof_id)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
                        dynamic_th = 0
                        static_th = 32767*288
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                t = True
                                sys_logging("True:%d"%t)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1500:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 10:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            status = self.client.sai_thrift_remove_buffer_profile(dynamic_buf_prof_id)
            assert (SAI_STATUS_SUCCESS == status)

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != static_buf_prof_id:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(static_buf_prof_id)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
                        dynamic_th = 0
                        static_th = 32767*288
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                t = True
                                sys_logging("True:%d"%t)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1500:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 10:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            static_th = 16384*288
            attr_value = sai_thrift_attribute_value_t(u64=static_th)
            attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
            self.client.sai_thrift_set_buffer_profile_attribute(static_buf_prof_id, attr)

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != static_buf_prof_id:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(static_buf_prof_id)

                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                t = True
                                sys_logging("True:%d"%t)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1500:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 10:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

        finally:
            for queue_id in queue_id_list:
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                status = self.client.sai_thrift_set_queue_attribute(queue_id, attr)
                assert (SAI_STATUS_SUCCESS == status)

                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                status = self.client.sai_thrift_set_queue_attribute(queue_id, attr)
                assert (SAI_STATUS_SUCCESS == status)

                status = self.client.sai_thrift_remove_queue(queue_id)
                assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_buffer_profile(static_buf_prof_id)
            assert (SAI_STATUS_SUCCESS == status)

            self.client.sai_thrift_remove_wred_profile(wred_id)
            assert (SAI_STATUS_SUCCESS == status)

@group('Buffer')
class fun_13_buffer_profile_share_between_pgs_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        port0 = port_list[0]
        port1 = port_list[1]

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = 0
        xon_th = 224*288
        xoff_th = 256*288

        port0_pg_num = 0
        port1_pg_num = 0
        port0_pg_list = []
        port1_pg_list = []

        buf_prof_oid = 0

        attrs = self.client.sai_thrift_get_port_attribute(port0)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                port0_pg_num = a.value.u32
                sys_logging("Ingress PG Num:",a.value.u32)
            if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                for i in range(a.value.objlist.count):
                    port0_pg_list.append(a.value.objlist.object_id_list[i])
                    assert(0 != port0_pg_list[i])
                    sys_logging("Ingress PG List[%d]:0x%x"%(i, a.value.objlist.object_id_list[i]))

        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                port1_pg_num = a.value.u32
                sys_logging("Ingress PG Num:",a.value.u32)
            if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                for i in range(a.value.objlist.count):
                    port1_pg_list.append(a.value.objlist.object_id_list[i])
                    assert(0 != port1_pg_list[i])
                    sys_logging("Ingress PG List[%d]:0x%x"%(i, a.value.objlist.object_id_list[i]))

        attr_list = []
        #attr_value = sai_thrift_attribute_value_t(u64=static_th)
        #attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        #attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        attr_value = sai_thrift_attribute_value_t(s32=th_mode)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
        attr_list.append(attr)

        buf_prof_oid = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL != buf_prof_oid)
        sys_logging("Create Dynamic Buffer Profile id:0x%X" %buf_prof_oid)

        for i in range(port0_pg_num):
            attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
            attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
            self.client.sai_thrift_set_priority_group_attribute(port0_pg_list[i], attr)

        warmboot(self.client)
        try:
            for i in range(port0_pg_num):
                sys_logging("Get PG:0x%x" %port0_pg_list[i])
                attrs = self.client.sai_thrift_get_priority_group_attribute(port0_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT:
                        if a.value.oid != port0:
                            raise NotImplementedError()
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX:
                        if a.value.u8 != i:
                            raise NotImplementedError()

            for i in range(port0_pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                self.client.sai_thrift_set_priority_group_attribute(port0_pg_list[i], attr)

            for i in range(port1_pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                self.client.sai_thrift_set_priority_group_attribute(port1_pg_list[i], attr)

            for i in range(port1_pg_num):
                sys_logging("Get PG:0x%x" %port1_pg_list[i])
                attrs = self.client.sai_thrift_get_priority_group_attribute(port1_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT:
                        if a.value.oid != port1:
                            raise NotImplementedError()
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX:
                        if a.value.u8 != i:
                            raise NotImplementedError()

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_oid)
            assert (SAI_STATUS_SUCCESS != status)

            for i in range(port0_pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                self.client.sai_thrift_set_priority_group_attribute(port0_pg_list[i], attr)

            for i in range(port0_pg_num):
                sys_logging("Get PG:0x%x" %port0_pg_list[i])
                attrs = self.client.sai_thrift_get_priority_group_attribute(port0_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT:
                        if a.value.oid != port0:
                            raise NotImplementedError()
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX:
                        if a.value.u8 != i:
                            raise NotImplementedError()

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_oid)
            assert (SAI_STATUS_SUCCESS != status)

            for i in range(port0_pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                self.client.sai_thrift_set_priority_group_attribute(port0_pg_list[i], attr)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_oid)
            assert (SAI_STATUS_SUCCESS != status)

            for i in range(port1_pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                self.client.sai_thrift_set_priority_group_attribute(port1_pg_list[i], attr)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_oid)
            assert (SAI_STATUS_SUCCESS == status)

        finally:
            for i in range(port0_pg_num):
                self.client.sai_thrift_remove_priority_group(port0_pg_list[i])

            for i in range(port1_pg_num):
                self.client.sai_thrift_remove_priority_group(port1_pg_list[i])

@group('Buffer')
class fun_14_buffer_profile_xon_xoff_entry_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        buf_prof_oid_list = []
        pg_list = []
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = 0

        for i in range(1, 8):

            xon_th = (224+(i*10))*288
            xoff_th = (256+(i*10))*288

            attr_list = []
            #attr_value = sai_thrift_attribute_value_t(u64=static_th)
            #attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
            #attr_list.append(attr)

            attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
            attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
            attr_list.append(attr)

            attr_value = sai_thrift_attribute_value_t(u64=xon_th)
            attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
            attr_list.append(attr)

            attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
            attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
            attr_list.append(attr)

            th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
            attr_value = sai_thrift_attribute_value_t(s32=th_mode)
            attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
            attr_list.append(attr)

            buf_prof_oid = self.client.sai_thrift_create_buffer_profile(attr_list)
            assert (SAI_OBJECT_TYPE_NULL != buf_prof_oid)
            buf_prof_oid_list.append(buf_prof_oid)
            sys_logging("Create Dynamic Buffer Profile id:0x%X" %buf_prof_oid)

        warmboot(self.client)
        try:
            for i in range(0, 7):

                pg_list = []
                attrs = self.client.sai_thrift_get_port_attribute(port_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                        pg_num = a.value.u32
                        sys_logging("Ingress PG Num:",a.value.u32)
                    if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                        for ii in range(a.value.objlist.count):
                            pg_list.append(a.value.objlist.object_id_list[ii])
                            assert(0 != pg_list[ii])
                            sys_logging("Port:%d, Ingress PG List[%d]:0x%x"%(i, ii, a.value.objlist.object_id_list[ii]))

                for ii in range(pg_num):
                    attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid_list[i])
                    attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                    status = self.client.sai_thrift_set_priority_group_attribute(pg_list[ii], attr)

                    if i < 6:
                        assert (SAI_STATUS_SUCCESS == status)
                        attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[ii])
                        for a in attrs.attr_list:

                            if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:

                                if a.value.oid != buf_prof_oid_list[i]:
                                    raise NotImplementedError()
                                buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid_list[i])

                                xon_th = (224+((i+1)*10))*288
                                xoff_th = (256+((i+1)*10))*288

                                for b in buffer_attrs.attr_list:
                                    if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                        if b.value.s32 != th_mode:
                                            raise NotImplementedError()
                                    if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                        if b.value.s8 != dynamic_th:
                                            raise NotImplementedError()
                                    if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                        if b.value.u64 != static_th:
                                            raise NotImplementedError()
                                    if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                        if b.value.u64 != xoff_th:
                                            raise NotImplementedError()
                                    if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                        if b.value.u64 != xon_th:
                                            raise NotImplementedError()
                            if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT:
                                if a.value.oid != port_list[i]:
                                    raise NotImplementedError()
                            if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX:
                                if a.value.u8 != ii:
                                    raise NotImplementedError()
                    else:
                        assert (SAI_STATUS_SUCCESS != status)

            for i in range(0, 7):

                pg_list = []
                attrs = self.client.sai_thrift_get_port_attribute(port_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                        pg_num = a.value.u32
                        sys_logging("Ingress PG Num:",a.value.u32)
                    if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                        for ii in range(a.value.objlist.count):
                            pg_list.append(a.value.objlist.object_id_list[ii])
                            assert(0 != pg_list[ii])
                            sys_logging("Port:%d, Ingress PG List[%d]:0x%x" %(i, ii, a.value.objlist.object_id_list[ii]))

                if i < 6:
                    for ii in range(pg_num):
                        attr_value = sai_thrift_attribute_value_t(oid=0)
                        attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)

                        status = self.client.sai_thrift_set_priority_group_attribute(pg_list[ii], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                for ii in range(pg_num):
                    status = self.client.sai_thrift_remove_priority_group(pg_list[ii])
                    assert (SAI_STATUS_SUCCESS == status)

            for i in range(0, 7):
                status = self.client.sai_thrift_remove_buffer_profile(buf_prof_oid_list[i])
                assert (SAI_STATUS_SUCCESS == status)

            buf_prof_oid_list = []

            for i in range(1, 8):

                xon_th = (224+(i*10))*288
                xoff_th = (256+(i*10))*288

                attr_list = []
                #attr_value = sai_thrift_attribute_value_t(u64=static_th)
                #attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
                #attr_list.append(attr)

                attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
                attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
                attr_list.append(attr)

                attr_value = sai_thrift_attribute_value_t(u64=xon_th)
                attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
                attr_list.append(attr)

                attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
                attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
                attr_list.append(attr)

                th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                attr_value = sai_thrift_attribute_value_t(s32=th_mode)
                attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
                attr_list.append(attr)

                buf_prof_oid = self.client.sai_thrift_create_buffer_profile(attr_list)
                assert (SAI_OBJECT_TYPE_NULL != buf_prof_oid)
                buf_prof_oid_list.append(buf_prof_oid)
                sys_logging("Create Dynamic Buffer Profile id:0x%X" %buf_prof_oid)

            for i in range(0, 7):

                pg_list = []
                attrs = self.client.sai_thrift_get_port_attribute(port_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                        pg_num = a.value.u32
                        sys_logging("Ingress PG Num:",a.value.u32)
                    if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                        for ii in range(a.value.objlist.count):
                            pg_list.append(a.value.objlist.object_id_list[ii])
                            assert(0 != pg_list[ii])
                            sys_logging("Port:%d, Ingress PG List[%d]:0x%x"%(i, ii, a.value.objlist.object_id_list[ii]))

                for ii in range(pg_num):
                    attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid_list[i])
                    attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                    status = self.client.sai_thrift_set_priority_group_attribute(pg_list[ii], attr)

                    if i != 6:
                        assert (SAI_STATUS_SUCCESS == status)
                        attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[ii])
                        for a in attrs.attr_list:

                            if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:

                                if a.value.oid != buf_prof_oid_list[i]:
                                    raise NotImplementedError()
                                buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid_list[i])

                                xon_th = (224+((i+1)*10))*288
                                xoff_th = (256+((i+1)*10))*288

                                for b in buffer_attrs.attr_list:
                                    if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                        if b.value.s32 != th_mode:
                                            raise NotImplementedError()
                                    if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                        if b.value.s8 != dynamic_th:
                                            raise NotImplementedError()
                                    if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                        if b.value.u64 != static_th:
                                            raise NotImplementedError()
                                    if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                        if b.value.u64 != xoff_th:
                                            raise NotImplementedError()
                                    if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                        if b.value.u64 != xon_th:
                                            raise NotImplementedError()
                            if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT:
                                if a.value.oid != port_list[i]:
                                    raise NotImplementedError()
                            if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX:
                                if a.value.u8 != ii:
                                    raise NotImplementedError()
                    else:
                        assert (SAI_STATUS_SUCCESS != status)

        finally:
            for i in range(0, 7):

                pg_list = []
                attrs = self.client.sai_thrift_get_port_attribute(port_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                        pg_num = a.value.u32
                        sys_logging("Ingress PG Num:",a.value.u32)
                    if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                        for ii in range(a.value.objlist.count):
                            pg_list.append(a.value.objlist.object_id_list[ii])
                            assert(0 != pg_list[ii])
                            sys_logging("Port:%d, Ingress PG List[%d]:0x%x" %(i, ii, a.value.objlist.object_id_list[ii]))

                if i < 6:
                    for ii in range(pg_num):
                        attr_value = sai_thrift_attribute_value_t(oid=0)
                        attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)

                        status = self.client.sai_thrift_set_priority_group_attribute(pg_list[ii], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                for ii in range(pg_num):
                    status = self.client.sai_thrift_remove_priority_group(pg_list[ii])
                    assert (SAI_STATUS_SUCCESS == status)

            for i in range(0, 7):
                status = self.client.sai_thrift_remove_buffer_profile(buf_prof_oid_list[i])
                assert (SAI_STATUS_SUCCESS == status)

@group('Buffer')
class fun_15_buffer_overwrite_between_wred_wtd_and_flow_ctl(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        port = port_list[0]

        pg_list = []
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = 0

        xon_th = 224*288
        xoff_th = 256*288

        attr_list = []
        queue_id_list = []
        pg_num = 0

        #attr_value = sai_thrift_attribute_value_t(u64=static_th)
        #attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        #attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        attr_value = sai_thrift_attribute_value_t(s32=th_mode)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
        attr_list.append(attr)

        buf_prof_oid = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL != buf_prof_oid)
        sys_logging("Create Dynamic Buffer Profile id:0x%X" %buf_prof_oid)

        #create Wred Id
        color_en = [1,1,1]
        min_thrd = [1500,700, 300]
        max_thrd = [3000,1500,700]
        drop_prob = [10, 30, 60]
        ecn_thrd = [2000,1000,500]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        assert (SAI_OBJECT_TYPE_NULL != wred_id)
        sys_logging("wred_id:", wred_id)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                    pg_num = a.value.u32
                    sys_logging("Ingress PG Num:",a.value.u32)
                if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                    for i in range(a.value.objlist.count):
                        pg_list.append(a.value.objlist.object_id_list[i])
                        assert (SAI_NULL_OBJECT_ID != pg_list[i])
                        sys_logging("Port:%d, Ingress PG List[%d]:0x%x" %(port, i, a.value.objlist.object_id_list[i]))

            for i in range(pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                status = self.client.sai_thrift_set_priority_group_attribute(pg_list[i], attr)

            queue_attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in queue_attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

                        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            for i in range(pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1500:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 10:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)
            assert (SAI_STATUS_SUCCESS == status)

            attr_value = sai_thrift_attribute_value_t(u32=1550)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_MIN_THRESHOLD, value=attr_value)
            status = self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)
            assert (SAI_STATUS_SUCCESS == status)

            attr_value = sai_thrift_attribute_value_t(u32=3050)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_MAX_THRESHOLD, value=attr_value)
            status = self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)
            assert (SAI_STATUS_SUCCESS == status)

            attr_value = sai_thrift_attribute_value_t(u32=15)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_DROP_PROBABILITY, value=attr_value)
            status = self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)
            assert (SAI_STATUS_SUCCESS == status)

            for i in range(pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            dynamic_th = 1
            attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
            attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
            self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_oid, attr)

            for i in range(pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            for queue_id in queue_id_list:
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queue_id, attr)

            for i in range(pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != SAI_NULL_OBJECT_ID:
                            raise NotImplementedError()

            for queue_id in queue_id_list:
                attr_value = sai_thrift_attribute_value_t(oid=wred_id)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queue_id, attr)

            for i in range(pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            for queue_id in queue_id_list:
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queue_id, attr)

            for i in range(pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != SAI_NULL_OBJECT_ID:
                            raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                t = True
                                sys_logging("True:%d"%t)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            for queue_id in queue_id_list:
                attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queue_id, attr)

            for i in range(pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            for i in range(pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                status = self.client.sai_thrift_set_priority_group_attribute(pg_list[i], attr)

            for i in range(pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != SAI_NULL_OBJECT_ID:
                            raise NotImplementedError()

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            for queue_id in queue_id_list:
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queue_id, attr)

                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queue_id, attr)

            for i in range(pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != SAI_NULL_OBJECT_ID:
                            raise NotImplementedError()

            for queue_id in queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != SAI_NULL_OBJECT_ID:
                            raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != SAI_NULL_OBJECT_ID:
                            raise NotImplementedError()

        finally:
            for i in range(pg_num):
                status = self.client.sai_thrift_remove_priority_group(pg_list[i])
                assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_oid)
            assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_wred_profile(wred_id)
            assert (SAI_STATUS_SUCCESS == status)

            for queue_id in queue_id_list:
                status = self.client.sai_thrift_remove_queue(queue_id)
                assert (SAI_STATUS_SUCCESS == status)

@group('Buffer')
class fun_16_wred_wtd_and_flow_ctl_shared_between_ports(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        port0 = port_list[0]
        port1 = port_list[1]

        port0_pg_list = []
        port1_pg_list = []
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = 0

        xon_th = 224*288
        xoff_th = 256*288

        attr_list = []
        port0_queue_id_list = []
        port1_queue_id_list = []
        port0_pg_num = 0
        port1_pg_num = 0

        #attr_value = sai_thrift_attribute_value_t(u64=static_th)
        #attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        #attr_list.append(attr)

        #1
        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        attr_value = sai_thrift_attribute_value_t(s32=th_mode)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
        attr_list.append(attr)

        buf_prof_oid = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL != buf_prof_oid)
        sys_logging("Create Dynamic Buffer Profile id:0x%X" %buf_prof_oid)

        #2
        #create Wred Id
        color_en = [0,1,1]
        min_thrd = [1500,700, 300]
        max_thrd = [3000,1500,700]
        drop_prob = [10, 30, 60]
        ecn_thrd = [2000,1000,500]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        assert (SAI_OBJECT_TYPE_NULL != wred_id)
        sys_logging("wred_id:", wred_id)

        #3
        attrs = self.client.sai_thrift_get_port_attribute(port0)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                port0_pg_num = a.value.u32
                sys_logging("Ingress PG Num:",a.value.u32)
            if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                for i in range(a.value.objlist.count):
                    port0_pg_list.append(a.value.objlist.object_id_list[i])
                    assert (SAI_NULL_OBJECT_ID != port0_pg_list[i])
                    sys_logging("Port:0x%lx, Ingress PG List[%d]:0x%x" %(port0, i, a.value.objlist.object_id_list[i]))

        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                port1_pg_num = a.value.u32
                sys_logging("Ingress PG Num:",a.value.u32)
            if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                for i in range(a.value.objlist.count):
                    port1_pg_list.append(a.value.objlist.object_id_list[i])
                    assert (SAI_NULL_OBJECT_ID != port1_pg_list[i])
                    sys_logging("Port:0x%lx, Ingress PG List[%d]:0x%x" %(port1, i, a.value.objlist.object_id_list[i]))

        warmboot(self.client)
        try:
            #4
            for i in range(port0_pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                status = self.client.sai_thrift_set_priority_group_attribute(port0_pg_list[i], attr)

            for i in range(port1_pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                status = self.client.sai_thrift_set_priority_group_attribute(port1_pg_list[i], attr)

            #5
            queue_attrs = self.client.sai_thrift_get_port_attribute(port0)
            for a in queue_attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        port0_queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

                        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port0_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port0_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            queue_attrs = self.client.sai_thrift_get_port_attribute(port1)
            for a in queue_attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        port1_queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

                        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port1_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port1_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            #6
            for i in range(port0_pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(port0_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in port0_queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1500:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 10:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            for i in range(port1_pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(port1_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in port1_queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1500:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 10:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            #7
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)
            assert (SAI_STATUS_SUCCESS == status)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_YELLOW_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)
            assert (SAI_STATUS_SUCCESS == status)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_RED_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)
            assert (SAI_STATUS_SUCCESS == status)

            attr_value = sai_thrift_attribute_value_t(u32=1550)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_MIN_THRESHOLD, value=attr_value)
            status = self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)
            assert (SAI_STATUS_SUCCESS == status)

            attr_value = sai_thrift_attribute_value_t(u32=3050)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_MAX_THRESHOLD, value=attr_value)
            status = self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)
            assert (SAI_STATUS_SUCCESS == status)

            attr_value = sai_thrift_attribute_value_t(u32=15)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_DROP_PROBABILITY, value=attr_value)
            status = self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)
            assert (SAI_STATUS_SUCCESS == status)

            for i in range(port0_pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(port0_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in port0_queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            for i in range(port1_pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(port1_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in port1_queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            #8
            dynamic_th = 1
            attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
            attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
            self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_oid, attr)

            for i in range(port0_pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(port0_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in port0_queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            for i in range(port1_pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(port1_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in port1_queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            #9
            xon_th = 234*288
            xoff_th = 266*288

            attr_value = sai_thrift_attribute_value_t(u64=xon_th)
            attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
            status = self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_oid, attr)
            assert (SAI_STATUS_SUCCESS == status)

            attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
            attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
            status = self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_oid, attr)
            assert (SAI_STATUS_SUCCESS == status)

            for i in range(port0_pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(port0_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in port0_queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            for i in range(port1_pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(port1_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in port1_queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            #10
            for i in range(port0_pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                status = self.client.sai_thrift_set_priority_group_attribute(port0_pg_list[i], attr)

            #11
            queue_attrs = self.client.sai_thrift_get_port_attribute(port0)
            for a in queue_attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        port0_queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

                        attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port0_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                        attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port0_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            #12

            #13
            for i in range(port1_pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(port1_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in port1_queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            #14
            for i in range(port1_pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                status = self.client.sai_thrift_set_priority_group_attribute(port1_pg_list[i], attr)

            #15
            queue_attrs = self.client.sai_thrift_get_port_attribute(port1)
            for a in queue_attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        port1_queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

                        attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port1_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                        attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port1_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            #16
            for i in range(port0_pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                status = self.client.sai_thrift_set_priority_group_attribute(port0_pg_list[i], attr)

            port0_queue_id_list = []
            queue_attrs = self.client.sai_thrift_get_port_attribute(port0)
            for a in queue_attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        port0_queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

                        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port0_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port0_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

            #17

            #18
            for i in range(port0_pg_num):
                attrs = self.client.sai_thrift_get_priority_group_attribute(port0_pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()

            for queue_id in port0_queue_id_list:
                queue_attrs = self.client.sai_thrift_get_queue_attribute(queue_id)
                for a in queue_attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        sys_logging("Get queue[0x%x] Buffer Profile oid: 0x%x"%(queue_id, a.value.oid))
                        if a.value.oid != buf_prof_oid:
                            raise NotImplementedError()
                        buffer_attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_oid)
                        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
                        for b in buffer_attrs.attr_list:
                            if b.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                                if b.value.s32 != th_mode:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                                if b.value.s8 != dynamic_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                                if b.value.u64 != static_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                                if b.value.u64 != xoff_th:
                                    raise NotImplementedError()
                            if b.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                                if b.value.u64 != xon_th:
                                    raise NotImplementedError()
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_id:
                            raise NotImplementedError()
                        wred_attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
                        for b in wred_attrs.attr_list:
                            if b.id == SAI_WRED_ATTR_GREEN_ENABLE:
                                sys_logging("new green drop en:%d"%b.value.booldata)
                                if b.value.booldata != 1:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                                sys_logging("yellow drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_ENABLE:
                                sys_logging("red drop en:%d"%b.value.booldata)
                                if b.value.booldata != 0:
                                    raise NotImplementedError()

                            if b.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                                sys_logging("new green min thrd:",b.value.u32)
                                if b.value.u32 != 1550:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                                sys_logging("yellow min thrd:",b.value.u32)
                                if b.value.u32 != 700:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                                sys_logging("red min thrd:",b.value.u32)
                                if b.value.u32 != 300:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                                sys_logging("green max thrd:",b.value.u32)
                                if b.value.u32 != 3050:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                                if b.value.u32 != 1500:
                                    sys_logging("yellow max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                                if b.value.u32 != 700:
                                    sys_logging("red max thrd:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                                if b.value.u32 != 15:
                                    sys_logging("new green drop prob:",b.value.u32)
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                                sys_logging("yellow drop prob:",b.value.u32)
                                if b.value.u32 != 30:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                                sys_logging("red drop prob:",b.value.u32)
                                if b.value.u32 != 60:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 2000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 1000:
                                    raise NotImplementedError()
                            if b.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                                sys_logging("new green ecn thrd:",b.value.u32)
                                if b.value.u32 != 500:
                                    raise NotImplementedError()

            #19
            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_oid)
            assert (SAI_STATUS_SUCCESS != status)

            status = self.client.sai_thrift_remove_wred_profile(wred_id)
            assert (SAI_STATUS_SUCCESS != status)

            #20
            for i in range(port0_pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                status = self.client.sai_thrift_set_priority_group_attribute(port0_pg_list[i], attr)
                assert (SAI_STATUS_SUCCESS == status)

            port0_queue_id_list = []
            queue_attrs = self.client.sai_thrift_get_port_attribute(port0)
            for a in queue_attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("queue number:%d"%a.value.u32)
                    queue_num = a.value.u32
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for i in range(a.value.objlist.count):
                        port0_queue_id_list.append(a.value.objlist.object_id_list[i])
                        sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

                        attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port0_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)

                        attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                        status = self.client.sai_thrift_set_queue_attribute(port0_queue_id_list[i], attr)
                        assert (SAI_STATUS_SUCCESS == status)
            #21

        finally:
            for i in range(port0_pg_num):
                status = self.client.sai_thrift_remove_priority_group(port0_pg_list[i])
                assert (SAI_STATUS_SUCCESS == status)

            for i in range(port1_pg_num):
                status = self.client.sai_thrift_remove_priority_group(port1_pg_list[i])
                assert (SAI_STATUS_SUCCESS == status)

            for queue_id in port0_queue_id_list:
                status = self.client.sai_thrift_remove_queue(queue_id)
                assert (SAI_STATUS_SUCCESS == status)

            for queue_id in port1_queue_id_list:
                status = self.client.sai_thrift_remove_queue(queue_id)
                assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_oid)
            assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_wred_profile(wred_id)
            assert (SAI_STATUS_SUCCESS == status)

'''
class scenario_01_flow_ctl_based_on_packet_color(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)

        #port0 = port_list[0]
        #port1 = port_list[1]

        port0 = port_list[60]
        port1 = port_list[61]
        queue_id_list = []
        port1_pg_list = []
        queue_num = 0

        port1_pg_num = 0

        attrs = self.client.sai_thrift_get_port_attribute(port1)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                port1_pg_num = a.value.u32
                sys_logging("Ingress PG Num:",a.value.u32)
            if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                for i in range(a.value.objlist.count):
                    port1_pg_list.append(a.value.objlist.object_id_list[i])
                    assert (SAI_NULL_OBJECT_ID != port1_pg_list[i])
                    sys_logging("Port:0x%lx, Ingress PG List[%d]:0x%x" %(port1, i, a.value.objlist.object_id_list[i]))

        sched_type = SAI_SCHEDULING_TYPE_STRICT
        sched_weight = 0
        cir = 1000000
        cbs = 256000
        pir = 1000000
        pbs = 64000

        #sched_oid = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        #sys_logging("sched_oid 0x%x"%sched_oid)
        #assert (0 != sched_oid)

        sched_type = SAI_SCHEDULING_TYPE_STRICT
        sched_weight = 10
        sched_oid = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, 0, 0, 10, 0)

        attrs = self.client.sai_thrift_get_port_attribute(port0)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queue_id_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(queue_id_list[7], attr)
        assert (SAI_STATUS_SUCCESS == status)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        #red
        #dynamic_th = -7
        #dynamic_th = -2
        dynamic_th = 3

        #yellow
        #dynamic_th = -2

        #green
        #dynamic_th = 3

        #64,512
        xon_th = 224*288
        #73,728
        xoff_th = 256*288

        attr_list = []
        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        attr_value = sai_thrift_attribute_value_t(s32=th_mode)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
        attr_list.append(attr)

        buf_prof_oid = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL != buf_prof_oid)
        sys_logging("Create Dynamic Buffer Profile id:0x%X" %buf_prof_oid)

        #attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
        #attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
        #status = self.client.sai_thrift_set_queue_attribute(queue_id_list[0], attr)
        #assert (SAI_STATUS_SUCCESS == status)

        for i in range(port1_pg_num):
            attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
            attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
            status = self.client.sai_thrift_set_priority_group_attribute(port1_pg_list[i], attr)

        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port0, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_mask1 = '255.255.255.255'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

        # send the test packet(s)
        pkt = simple_ip_packet(pktlen=64,
                               eth_dst=router_mac,
                               eth_src='00:22:22:22:22:22',
                               ip_dst='10.10.10.1',
                               ip_src='192.168.0.1',
                               ip_proto=55)

        exp_pkt = simple_ip_packet(pktlen=64,
                                   eth_dst='00:11:22:33:44:55',
                                   eth_src=router_mac,
                                   ip_dst='10.10.10.1',
                                   ip_src='192.168.0.1',
                                   ip_proto=55)


        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            #self.ctc_send_packet(1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            #self.ctc_verify_packets(exp_pkt, [0])
        finally:
            print '----------------------------------------------------------------------------------------------'

        #pdb.set_trace()

        #cir = 1
        #attr_value = sai_thrift_attribute_value_t(u64=cir)
        #attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE, value=attr_value)
        #self.client.sai_thrift_set_scheduler_attribute(sched_oid, attr)
        #
        #print "222222222222222222222222222222"
        #pir = 1
        #attr_value = sai_thrift_attribute_value_t(u64=pir)
        #attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE, value=attr_value)
        #self.client.sai_thrift_set_scheduler_attribute(sched_oid, attr)

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_FORWARD
        #action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = '00:22:22:22:22:22'
        mac_dst = router_mac
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
        #svlan_id=20
        #svlan_pri=4
        #svlan_cfi=1
        #cvlan_id=10
        #cvlan_pri=2
        #cvlan_cfi=None
        ip_type = SAI_ACL_IP_TYPE_IPV4ANY
        mpls_label0_label = None
        mpls_label0_ttl = None
        mpls_label0_exp = None
        mpls_label0_bos = None
        mpls_label1_label = None
        mpls_label1_ttl = None
        mpls_label1_exp = None
        mpls_label1_bos = None
        mpls_label2_label = None
        mpls_label2_ttl = None
        mpls_label2_exp = None
        mpls_label2_bos = None
        mpls_label3_label = None
        mpls_label3_ttl = None
        mpls_label3_exp = None
        mpls_label3_bos = None
        mpls_label4_label = None
        mpls_label4_ttl = None
        mpls_label4_exp = None
        mpls_label4_bos = None
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.255"
        ip_dst = '10.10.10.1'
        ip_dst_mask = "255.255.255.255"
        ipv6_src = None
        ipv6_src_mask = None
        ipv6_dst = None
        ipv6_dst_mask = None
        ip_protocol = None
        #ip_protocol = 6
        #ip_tos=5
        #ip_ecn=1
        #ip_dscp=1
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        in_port = 1
        out_port = None
        out_ports = None
        src_l4_port = None
        dst_l4_port = None
        #src_l4_port = 1234
        #dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        admin_state = True

        ingress_samplepacket=None
        acl_range_id_list=None
        redirect=None
        user_define_filed_group0_data=None
        user_define_filed_group0_mask=None
        user_define_filed_group1_data=None
        user_define_filed_group1_mask=None
        user_define_filed_group2_data=None
        user_define_filed_group2_mask=None
        user_define_filed_group3_data=None
        user_define_filed_group3_mask=None
        user_define_filed_group4_data=None
        user_define_filed_group4_mask=None
        user_define_filed_group5_data=None
        user_define_filed_group5_mask=None
        user_define_filed_group6_data=None
        user_define_filed_group6_mask=None
        user_define_filed_group7_data=None
        user_define_filed_group7_mask=None
        user_define_filed_group8_data=None
        user_define_filed_group8_mask=None
        user_define_filed_group9_data=None
        user_define_filed_group9_mask=None
        user_define_filed_group10_data=None
        user_define_filed_group10_mask=None
        user_define_filed_group11_data=None
        user_define_filed_group11_mask=None
        user_define_filed_group12_data=None
        user_define_filed_group12_mask=None
        user_define_filed_group13_data=None
        user_define_filed_group13_mask=None
        user_define_filed_group14_data=None
        user_define_filed_group14_mask=None
        user_define_filed_group15_data=None
        user_define_filed_group15_mask=None
        ether_type=None
        metadata_port_user=None
        metadata_vlan_user=None
        color = SAI_PACKET_COLOR_GREEN

        acl_table_id = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            in_ports,
            out_ports,
            in_port,
            out_port,
            svlan_id,
            svlan_pri,
            svlan_cfi,
            cvlan_id,
            cvlan_pri,
            cvlan_cfi,
            ip_type,
            mpls_label0_label,
            mpls_label0_ttl,
            mpls_label0_exp,
            mpls_label0_bos,
            mpls_label1_label,
            mpls_label1_ttl,
            mpls_label1_exp,
            mpls_label1_bos,
            mpls_label2_label,
            mpls_label2_ttl,
            mpls_label2_exp,
            mpls_label2_bos,
            mpls_label3_label,
            mpls_label3_ttl,
            mpls_label3_exp,
            mpls_label3_bos,
            mpls_label4_label,
            mpls_label4_ttl,
            mpls_label4_exp,
            mpls_label4_bos,
            ip_protocol,
            src_l4_port,
            dst_l4_port,
            ipv6_src,
            ipv6_dst,
            ip_tos,
            ip_ecn,
            ip_dscp,
            ip_ttl)
        acl_entry_id = sai_thrift_create_acl_entry(self.client,
            acl_table_id,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_type,
            mpls_label0_label,
            mpls_label0_ttl,
            mpls_label0_exp,
            mpls_label0_bos,
            mpls_label1_label,
            mpls_label1_ttl,
            mpls_label1_exp,
            mpls_label1_bos,
            mpls_label2_label,
            mpls_label2_ttl,
            mpls_label2_exp,
            mpls_label2_bos,
            mpls_label3_label,
            mpls_label3_ttl,
            mpls_label3_exp,
            mpls_label3_bos,
            mpls_label4_label,
            mpls_label4_ttl,
            mpls_label4_exp,
            mpls_label4_bos,
            ip_src, ip_src_mask,
            ip_dst, ip_dst_mask,
            ip_protocol,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn,
            ipv6_src,
            ipv6_src_mask,
            ipv6_dst,
            ipv6_dst_mask,
            ingress_samplepacket,
            acl_range_id_list,
            redirect,
            user_define_filed_group0_data,
            user_define_filed_group0_mask,
            user_define_filed_group1_data,
            user_define_filed_group1_mask,
            user_define_filed_group2_data,
            user_define_filed_group2_mask,
            user_define_filed_group3_data,
            user_define_filed_group3_mask,
            user_define_filed_group4_data,
            user_define_filed_group4_mask,
            user_define_filed_group5_data,
            user_define_filed_group5_mask,
            user_define_filed_group6_data,
            user_define_filed_group6_mask,
            user_define_filed_group7_data,
            user_define_filed_group7_mask,
            user_define_filed_group8_data,
            user_define_filed_group8_mask,
            user_define_filed_group9_data,
            user_define_filed_group9_mask,
            user_define_filed_group10_data,
            user_define_filed_group10_mask,
            user_define_filed_group11_data,
            user_define_filed_group11_mask,
            user_define_filed_group12_data,
            user_define_filed_group12_mask,
            user_define_filed_group13_data,
            user_define_filed_group13_mask,
            user_define_filed_group14_data,
            user_define_filed_group14_mask,
            user_define_filed_group15_data,
            user_define_filed_group15_mask,
            ether_type,
            metadata_port_user,
            metadata_vlan_user,
            color)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        warmboot(self.client)
        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            remain_cnt = 0.0
            expect_packet_num = 0

            sc_thrd=1536
            sc_cnt=0

            remain_cnt = sai_thrift_get_remain_cnt(self.client,sc_thrd, sc_cnt)
            factor = sai_thrift_get_wtd_factor(self.client, dynamic_th)
            expect_packet_num = remain_cnt*factor

            pdb.set_trace()

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'

            #pdb.set_trace()

            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(queue_id_list[0], attr)
            assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_scheduler_profile(sched_oid)
            assert (SAI_STATUS_SUCCESS == status)

            # send the same packet
            #self.ctc_send_packet(1, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            #self.ctc_verify_no_packet(exp_pkt, 0, default_time_out)
            #self.ctc_verify_packets(exp_pkt, [0])

        finally:
            # unbind this ACL table from port2s object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            status = self.client.sai_thrift_set_port_attribute(port1, attr)
            assert (SAI_STATUS_SUCCESS == status)

            # cleanup ACL
            status = self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_acl_table(acl_table_id)
            assert (SAI_STATUS_SUCCESS == status)
            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

            status = self.client.sai_thrift_remove_next_hop(nhop1)
            assert (SAI_STATUS_SUCCESS == status)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            status = self.client.sai_thrift_remove_router_interface(rif_id1)
            assert (SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_remove_router_interface(rif_id2)
            assert (SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_remove_virtual_router(vr_id)
            assert (SAI_STATUS_SUCCESS == status)

            for i in range(queue_num):
                status = self.client.sai_thrift_remove_queue(queue_id_list[i])
                assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_oid)
            assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_scheduler_profile(sched_oid)
            assert (SAI_STATUS_SUCCESS == status)

class scenario_02_wtd_drop_mode_dynamic_based_on_packet_color(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)

        #port0 = port_list[0]
        #port1 = port_list[1]

        port0 = port_list[60]
        port1 = port_list[61]
        queue_id_list = []
        queue_num = 0

        sched_type = SAI_SCHEDULING_TYPE_STRICT
        sched_weight = 10
        sched_oid = sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, 0, 0, 10, 0)

        attrs = self.client.sai_thrift_get_port_attribute(port0)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                sys_logging("queue number:%d"%a.value.u32)
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queue_id_list.append(a.value.objlist.object_id_list[i])
                    sys_logging("queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i]))

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        for i in range(queue_num):
            status = self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
            assert (SAI_STATUS_SUCCESS == status)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        #red
        #dynamic_th = -7
        #dynamic_th = -2
        dynamic_th = 3

        #yellow
        #dynamic_th = -2

        #green
        #dynamic_th = 3

        xon_th = 224*288
        xoff_th = 256*288

        attr_list = []
        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr)

        attr_value = sai_thrift_attribute_value_t(u64=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        attr_value = sai_thrift_attribute_value_t(s32=th_mode)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
        attr_list.append(attr)

        buf_prof_oid = self.client.sai_thrift_create_buffer_profile(attr_list)
        assert (SAI_OBJECT_TYPE_NULL != buf_prof_oid)
        sys_logging("Create Dynamic Buffer Profile id:0x%X" %buf_prof_oid)

        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_oid)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
        for i in range(queue_num):
            status = self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
            assert (SAI_STATUS_SUCCESS == status)

        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port0, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_mask1 = '255.255.255.255'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_FORWARD
        in_ports = None
        mac_src = '00:22:22:22:22:22'
        mac_dst = router_mac
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
        #svlan_id=20
        #svlan_pri=4
        #svlan_cfi=1
        #cvlan_id=10
        #cvlan_pri=2
        #cvlan_cfi=None
        ip_type = SAI_ACL_IP_TYPE_IPV4ANY
        mpls_label0_label = None
        mpls_label0_ttl = None
        mpls_label0_exp = None
        mpls_label0_bos = None
        mpls_label1_label = None
        mpls_label1_ttl = None
        mpls_label1_exp = None
        mpls_label1_bos = None
        mpls_label2_label = None
        mpls_label2_ttl = None
        mpls_label2_exp = None
        mpls_label2_bos = None
        mpls_label3_label = None
        mpls_label3_ttl = None
        mpls_label3_exp = None
        mpls_label3_bos = None
        mpls_label4_label = None
        mpls_label4_ttl = None
        mpls_label4_exp = None
        mpls_label4_bos = None
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.255"
        ip_dst = '10.10.10.1'
        ip_dst_mask = "255.255.255.255"
        ipv6_src = None
        ipv6_src_mask = None
        ipv6_dst = None
        ipv6_dst_mask = None
        ip_protocol = None
        #ip_protocol = 6
        #ip_tos=5
        #ip_ecn=1
        #ip_dscp=1
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        in_port = 1
        out_port = None
        out_ports = None
        src_l4_port = None
        dst_l4_port = None
        #src_l4_port = 1234
        #dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        admin_state = True

        ingress_samplepacket=None
        acl_range_id_list=None
        redirect=None
        user_define_filed_group0_data=None
        user_define_filed_group0_mask=None
        user_define_filed_group1_data=None
        user_define_filed_group1_mask=None
        user_define_filed_group2_data=None
        user_define_filed_group2_mask=None
        user_define_filed_group3_data=None
        user_define_filed_group3_mask=None
        user_define_filed_group4_data=None
        user_define_filed_group4_mask=None
        user_define_filed_group5_data=None
        user_define_filed_group5_mask=None
        user_define_filed_group6_data=None
        user_define_filed_group6_mask=None
        user_define_filed_group7_data=None
        user_define_filed_group7_mask=None
        user_define_filed_group8_data=None
        user_define_filed_group8_mask=None
        user_define_filed_group9_data=None
        user_define_filed_group9_mask=None
        user_define_filed_group10_data=None
        user_define_filed_group10_mask=None
        user_define_filed_group11_data=None
        user_define_filed_group11_mask=None
        user_define_filed_group12_data=None
        user_define_filed_group12_mask=None
        user_define_filed_group13_data=None
        user_define_filed_group13_mask=None
        user_define_filed_group14_data=None
        user_define_filed_group14_mask=None
        user_define_filed_group15_data=None
        user_define_filed_group15_mask=None
        ether_type=None
        metadata_port_user=None
        metadata_vlan_user=None
        color = SAI_PACKET_COLOR_GREEN
        #color = SAI_PACKET_COLOR_YELLOW
        #color = SAI_PACKET_COLOR_RED

        acl_table_id = sai_thrift_create_acl_table(self.client,
            table_stage,
            table_bind_point_list,
            addr_family,
            mac_src,
            mac_dst,
            ip_src,
            ip_dst,
            in_ports,
            out_ports,
            in_port,
            out_port,
            svlan_id,
            svlan_pri,
            svlan_cfi,
            cvlan_id,
            cvlan_pri,
            cvlan_cfi,
            ip_type,
            mpls_label0_label,
            mpls_label0_ttl,
            mpls_label0_exp,
            mpls_label0_bos,
            mpls_label1_label,
            mpls_label1_ttl,
            mpls_label1_exp,
            mpls_label1_bos,
            mpls_label2_label,
            mpls_label2_ttl,
            mpls_label2_exp,
            mpls_label2_bos,
            mpls_label3_label,
            mpls_label3_ttl,
            mpls_label3_exp,
            mpls_label3_bos,
            mpls_label4_label,
            mpls_label4_ttl,
            mpls_label4_exp,
            mpls_label4_bos,
            ip_protocol,
            src_l4_port,
            dst_l4_port,
            ipv6_src,
            ipv6_dst,
            ip_tos,
            ip_ecn,
            ip_dscp,
            ip_ttl)
        acl_entry_id = sai_thrift_create_acl_entry(self.client,
            acl_table_id,
            entry_priority,
            admin_state,
            action, addr_family,
            mac_src, mac_src_mask,
            mac_dst, mac_dst_mask,
            svlan_id, svlan_pri,
            svlan_cfi, cvlan_id,
            cvlan_pri, cvlan_cfi,
            ip_type,
            mpls_label0_label,
            mpls_label0_ttl,
            mpls_label0_exp,
            mpls_label0_bos,
            mpls_label1_label,
            mpls_label1_ttl,
            mpls_label1_exp,
            mpls_label1_bos,
            mpls_label2_label,
            mpls_label2_ttl,
            mpls_label2_exp,
            mpls_label2_bos,
            mpls_label3_label,
            mpls_label3_ttl,
            mpls_label3_exp,
            mpls_label3_bos,
            mpls_label4_label,
            mpls_label4_ttl,
            mpls_label4_exp,
            mpls_label4_bos,
            ip_src, ip_src_mask,
            ip_dst, ip_dst_mask,
            ip_protocol,
            ip_tos, ip_ecn,
            ip_dscp, ip_ttl,
            in_ports, out_ports,
            in_port, out_port,
            src_l4_port, dst_l4_port,
            ingress_mirror_id,
            egress_mirror_id,
            new_svlan, new_scos,
            new_cvlan, new_ccos,
            deny_learn,
            ipv6_src,
            ipv6_src_mask,
            ipv6_dst,
            ipv6_dst_mask,
            ingress_samplepacket,
            acl_range_id_list,
            redirect,
            user_define_filed_group0_data,
            user_define_filed_group0_mask,
            user_define_filed_group1_data,
            user_define_filed_group1_mask,
            user_define_filed_group2_data,
            user_define_filed_group2_mask,
            user_define_filed_group3_data,
            user_define_filed_group3_mask,
            user_define_filed_group4_data,
            user_define_filed_group4_mask,
            user_define_filed_group5_data,
            user_define_filed_group5_mask,
            user_define_filed_group6_data,
            user_define_filed_group6_mask,
            user_define_filed_group7_data,
            user_define_filed_group7_mask,
            user_define_filed_group8_data,
            user_define_filed_group8_mask,
            user_define_filed_group9_data,
            user_define_filed_group9_mask,
            user_define_filed_group10_data,
            user_define_filed_group10_mask,
            user_define_filed_group11_data,
            user_define_filed_group11_mask,
            user_define_filed_group12_data,
            user_define_filed_group12_mask,
            user_define_filed_group13_data,
            user_define_filed_group13_mask,
            user_define_filed_group14_data,
            user_define_filed_group14_mask,
            user_define_filed_group15_data,
            user_define_filed_group15_mask,
            ether_type,
            metadata_port_user,
            metadata_vlan_user,
            color)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        pkt = simple_ip_packet(pktlen=64,
                               eth_dst=router_mac,
                               eth_src='00:22:22:22:22:22',
                               ip_dst='10.10.10.1',
                               ip_src='192.168.0.1',
                               ip_proto=55)

        exp_pkt = simple_ip_packet(pktlen=64,
                                   eth_dst='00:11:22:33:44:55',
                                   eth_src=router_mac,
                                   ip_dst='10.10.10.1',
                                   ip_src='192.168.0.1',
                                   ip_proto=55)

        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet(1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(exp_pkt, [0])
        finally:
            print '----------------------------------------------------------------------------------------------'

        warmboot(self.client)
        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'

            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            for i in range(queue_num):
                status = self.client.sai_thrift_set_queue_attribute(queue_id_list[i], attr)
                assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_scheduler_profile(sched_oid)
            assert (SAI_STATUS_SUCCESS == status)

            #pdb.set_trace()

            # send the same packet, just for uml, check manually on board
            self.ctc_send_packet(1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(exp_pkt, [0])

            #pdb.set_trace()

            #10G
            cir = 10000000
            attr_value = sai_thrift_attribute_value_t(u64=cir)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE, value=attr_value)
            self.client.sai_thrift_set_scheduler_attribute(sched_oid, attr)

            # send the same packet, just for uml, check manually on board
            self.ctc_send_packet(1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(exp_pkt, [0])

            #pdb.set_trace()

        finally:
            # unbind this ACL table from port2s object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            status = self.client.sai_thrift_set_port_attribute(port1, attr)
            assert (SAI_STATUS_SUCCESS == status)

            # cleanup ACL
            status = self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_acl_table(acl_table_id)
            assert (SAI_STATUS_SUCCESS == status)
            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

            status = self.client.sai_thrift_remove_next_hop(nhop1)
            assert (SAI_STATUS_SUCCESS == status)

            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            status = self.client.sai_thrift_remove_router_interface(rif_id1)
            assert (SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_remove_router_interface(rif_id2)
            assert (SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_remove_virtual_router(vr_id)
            assert (SAI_STATUS_SUCCESS == status)

            for i in range(queue_num):
                status = self.client.sai_thrift_remove_queue(queue_id_list[i])
                assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_oid)
            assert (SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_scheduler_profile(sched_oid)
            assert (SAI_STATUS_SUCCESS == status)
'''
