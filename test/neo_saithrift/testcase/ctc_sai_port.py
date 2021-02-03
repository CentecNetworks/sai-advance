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
Thrift SAI interface Port tests
"""
import socket
from switch import *
import sai_base_test
import ctypes

from ctc_sai_qos_map import _QosMapCreateMapId
from ctc_sai_qos_map import _QosMapShowAttribute


def _sai_thrift_qos_create_policer(client,
                                   meter_type, mode, color_source,
                                   cir, cbs, pir, pbs, 
                                   green_act, yellow_act, red_act, act_valid=[]):
    attr_list = []

    #set meter type
    attr_value = sai_thrift_attribute_value_t(s32=meter_type)
    attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_METER_TYPE, value=attr_value)
    attr_list.append(attr)

    #set mode
    attr_value = sai_thrift_attribute_value_t(s32=mode)
    attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_MODE, value=attr_value)
    attr_list.append(attr)

    #set color source
    if SAI_POLICER_MODE_STORM_CONTROL != mode:
        attr_value = sai_thrift_attribute_value_t(s32=color_source)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_COLOR_SOURCE, value=attr_value)
        attr_list.append(attr)

    #set cir
    if cir != 0:
        attr_value = sai_thrift_attribute_value_t(u64=cir)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
        attr_list.append(attr)

    #set cbs
    if cbs != 0:
        attr_value = sai_thrift_attribute_value_t(u64=cbs)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CBS, value=attr_value)
        attr_list.append(attr)

    #set pir
    if pir != 0:
        attr_value = sai_thrift_attribute_value_t(u64=pir)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_PIR, value=attr_value)
        attr_list.append(attr)

    #set pbs
    if pbs != 0:
        attr_value = sai_thrift_attribute_value_t(u64=pbs)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_PBS, value=attr_value)
        attr_list.append(attr)    

    #set green action
    if act_valid[0]:
        attr_value = sai_thrift_attribute_value_t(u64=green_act)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_GREEN_PACKET_ACTION, value=attr_value)
        attr_list.append(attr)

    #set yellow action
    if act_valid[1]:
        attr_value = sai_thrift_attribute_value_t(u64=yellow_act)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_YELLOW_PACKET_ACTION, value=attr_value)
        attr_list.append(attr)

    #set red action
    if act_valid[2]:
        attr_value = sai_thrift_attribute_value_t(u64=red_act)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_RED_PACKET_ACTION, value=attr_value)
        attr_list.append(attr)

    #create policer id
    return client.sai_thrift_create_policer(attr_list)


def _sai_thrift_qos_create_scheduler_profile(client,
                                            sched_type = SAI_SCHEDULING_TYPE_STRICT,
                                            sched_weight = 0,
                                            cir = 0, cbs = 0, pir = 0, pbs = 0):
    attr_list = []
    attr_value = sai_thrift_attribute_value_t(s32=sched_type)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_TYPE, value=attr_value)
    attr_list.append(attr)

    if sched_weight:
        attr_value = sai_thrift_attribute_value_t(u8=sched_weight)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, value=attr_value)
        attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u64=cir)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u64=cbs)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u64=pir)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u64=pbs)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE, value=attr_value)
    attr_list.append(attr)
    return client.sai_thrift_create_scheduler_profile(attr_list)


def _sai_thrift_qos_create_scheduler_group(client, 
                                           port_id, 
                                           level, 
                                           max_childs, 
                                           parent_id, 
                                           sched_id = 0):
    attr_list = []

    attr_value = sai_thrift_attribute_value_t(oid=port_id)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PORT_ID, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u8=level)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_LEVEL, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u8=max_childs)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(oid=parent_id)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
    attr_list.append(attr)

    if sched_id:
        attr_value = sai_thrift_attribute_value_t(oid=sched_id)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        attr_list.append(attr)

    return client.sai_thrift_create_scheduler_group(attr_list)


@group('port')
class func_01_create_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        Not support dynamic switch actually
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = 0x%x ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_02_create_same_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid1 = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid1 = %d ###" %port_oid1)
            assert(port_oid1 != SAI_NULL_OBJECT_ID)

            port_oid2 = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid2 = %d ###" %port_oid2)
            assert(port_oid2 != SAI_NULL_OBJECT_ID)
            assert(port_oid1 == port_oid2)

        finally:
            self.client.sai_thrift_remove_port(port_oid1)


@group('port')
class func_03_create_max_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)
        chipname = testutils.test_params_get()['chipname']

        if chipname == 'tsingma':
            max = 33
            lane_list = [0, 1, 2, 3, 4, 5, 6, 7, 8,
                         9, 10, 11, 12, 13, 14, 15,
                         16, 17, 18, 19, 20, 21, 22, 23,
                         24, 25, 26, 27, 28, 29, 30, 31,
                         32]
        elif chipname == 'tsingma_mx':
            max = 33
            lane_list = [0, 4, 8, 12, 16, 20, 24, 28,
                         32, 33, 34, 35, 36, 37, 38, 39,
                         40, 44, 48, 52, 56, 60, 64, 68,
                         72, 73, 74, 75, 76, 77, 78, 79, 
                         80]

        speed = 10000
        port_oid = [0 for i in range(0, max)]

        warmboot(self.client)
        try:
            for i in range(0, max):
                j = i + 1

                front = 'Ethernet'
                num = str(j)
                front_num = front + num
                sys_logging("### front = %s ###" %front_num)

                if j == max:
                    port_oid[i] = sai_thrift_create_port(self.client, front_num, speed, [lane_list[i]])
                    sys_logging("### port_oid = 0x%x ###" %port_oid[i])
                    assert(port_oid[i] == SAI_NULL_OBJECT_ID)
                else:
                    port_oid[i] = sai_thrift_create_port(self.client, front_num, speed, [lane_list[i]])
                    sys_logging("### port_oid = 0x%x ###" %port_oid[i])
                    assert(port_oid[i] != SAI_NULL_OBJECT_ID)

        finally:
            for i in range(0,max):
                self.client.sai_thrift_remove_port(port_oid[i])


@group('port')
class func_04_remove_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            status = self.client.sai_thrift_remove_port(port_oid)
            assert(status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("### remove port, status = %x ###" %status)


@group('port')
class func_05_remove_not_exist_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert (port_oid != SAI_NULL_OBJECT_ID)

            status = self.client.sai_thrift_remove_port(port_oid)
            assert(status == SAI_STATUS_SUCCESS)
            sys_logging("### remove port, status = %x ###" %status)

            status = self.client.sai_thrift_remove_port(port_oid)
            assert(status == SAI_STATUS_ITEM_NOT_FOUND)
            sys_logging("### remove port, status = %x ###" %status)

        finally:
            pass


@group('port')
class func_06_set_and_get_port_attribute_fn_01_TYPE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        ids_list = [SAI_SWITCH_ATTR_CPU_PORT]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        for attribute in switch_attr_list.attr_list:
            if attribute.id == SAI_SWITCH_ATTR_CPU_PORT:
                sys_logging("### SAI_SWITCH_ATTR_CPU_PORT = 0x%x ###" %attribute.value.oid)
                cpu_port = attribute.value.oid

        warmboot(self.client)
        try:
            logical_port = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = 0x%x ###" %logical_port)
            assert(logical_port != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(logical_port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_TYPE:
                    sys_logging("### SAI_PORT_ATTR_TYPE = %s ###" %a.value.s32)
                    assert(SAI_PORT_TYPE_LOGICAL == a.value.s32)

            attrs = self.client.sai_thrift_get_port_attribute(cpu_port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_TYPE:
                    sys_logging("### SAI_PORT_ATTR_TYPE = %s ###" %a.value.s32)
                    assert(SAI_PORT_TYPE_CPU == a.value.s32)

        finally:
            self.client.sai_thrift_remove_port(logical_port)


@group('port')
class func_06_set_and_get_port_attribute_fn_02_OPER_STATUS(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        uml is always up, TBD, failed
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = 0x%x ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_OPER_STATUS:
                    sys_logging("### SAI_PORT_ATTR_OPER_STATUS = %s ###" %a.value.s32)
                    assert(SAI_PORT_OPER_STATUS_UP == a.value.s32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_03_SUPPORTED_BREAKOUT_MODE_TYPE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]
        breakout_mode_list1 = [SAI_PORT_BREAKOUT_MODE_TYPE_1_LANE, SAI_PORT_BREAKOUT_MODE_TYPE_2_LANE,
                               SAI_PORT_BREAKOUT_MODE_TYPE_4_LANE]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = 0x%x ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_BREAKOUT_MODE_TYPE:
                    for b in a.value.s32list.s32list:
                        sys_logging("### SAI_PORT_ATTR_SUPPORTED_BREAKOUT_MODE_TYPE = %s ###" %b)
                    assert(breakout_mode_list1 == a.value.s32list.s32list)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_04_CURRENT_BREAKOUT_MODE_TYPE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        uml is XFI serdes mode by default
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = 0x%x ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_CURRENT_BREAKOUT_MODE_TYPE:
                    sys_logging("### SAI_PORT_ATTR_CURRENT_BREAKOUT_MODE_TYPE = %s ###" %a.value.s32)
                    assert(SAI_PORT_BREAKOUT_MODE_TYPE_1_LANE == a.value.s32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_05_QOS_NUMBER_OF_QUEUES(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        by switch global config, default is basic q num
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                    sys_logging("### SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES = %d ###" %a.value.u32)
                    assert(8 == a.value.u32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_06_QOS_QUEUE_LIST(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]
        queue_list = [21, 65557, 131093, 196629, 262165, 327701, 393237, 458773]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_PORT_ATTR_QOS_QUEUE_LIST = 0x%x ###" %b)
                    assert(queue_list == a.value.objlist.object_id_list)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_07_QOS_NUMBER_OF_SCHEDULER_GROUPS(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
        sys_logging("### port_oid = %d ###" %port_oid)
        assert (port_oid != SAI_NULL_OBJECT_ID)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS:
                    sys_logging("### SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS = %d ###" %a.value.u32)
                    assert (0 == a.value.u32)

            sched_type = SAI_SCHEDULING_TYPE_DWRR
            sched_weight = 10
            cir = 4000000
            cbs = 256000
            pir = 1000000
            pbs = 64000
            port = port_oid
            level = [0,1,2]
            max_childs = [4, 8]
            parent_id = [port, None, None]
            sched_group_id = [None]*6
            sched_group_id[0] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
            parent_id[1] = sched_group_id[0]
            sched_group_id[1] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS:
                    sys_logging("### SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS = %d ###" %a.value.u32)
                    assert (2 == a.value.u32)

        finally:
            self.client.sai_thrift_remove_scheduler_group(sched_group_id[1])
            self.client.sai_thrift_remove_scheduler_group(sched_group_id[0])
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_08_QOS_SCHEDULER_GROUP_LIST(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]
        group_list = []

        port_oid = sai_thrift_create_port(self.client, front, speed, lane_list);
        sys_logging("### port_oid = %d ###"  %port_oid)
        assert(port_oid != SAI_NULL_OBJECT_ID)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST:
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST = %d ###" %b)
                        assert(b in group_list)

            sched_type = SAI_SCHEDULING_TYPE_DWRR
            sched_weight = 10
            cir = 4000000
            cbs = 256000
            pir = 1000000
            pbs = 64000
            port = port_oid
            level = [0,1,2]
            max_childs = [4, 8]
            parent_id = [port, None, None]
            sched_group_id = [None, None]
            sched_group_id[0] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
            parent_id[1] = sched_group_id[0]
            sched_group_id[1] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST:
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST = %d ###" %b)
                        assert(b in sched_group_id)

        finally:
            self.client.sai_thrift_remove_scheduler_group(sched_group_id[1])
            self.client.sai_thrift_remove_scheduler_group(sched_group_id[0])
            self.client.sai_thrift_remove_port(port_oid) 


@group('port')
class func_06_set_and_get_port_attribute_fn_09_SUPPORTED_SPEED(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        platform bug 110226
        uml is XFI serdes mode by default
        SYSTEM MODIFIED KCAO for UML force support 1G/10G
        '''
        switch_init_without_port(self.client)
        chipname = testutils.test_params_get()['chipname']

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        if chipname == 'tsingma':
            speed_list = [10000, 1000, 10000]
        elif chipname == 'tsingma_mx':
            speed_list = [1000, 100, 10, 2500, 10000,
                          40000, 100000, 5000, 25000, 50000,
                          1000, 10000]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = 0x%x ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_SPEED:
                    for b in a.value.u32list.u32list:
                        sys_logging("### SAI_PORT_ATTR_SUPPORTED_SPEED = %d ###" %b)
                    assert(speed_list == a.value.u32list.u32list)

        finally:
            self.client.sai_thrift_remove_port(port_oid) 


@group('port')
class func_06_set_and_get_port_attribute_fn_10_SUPPORTED_FEC_MODE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 113262
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]
        fec_list = [SAI_PORT_FEC_MODE_NONE, SAI_PORT_FEC_MODE_FC]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = 0x%x ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_FEC_MODE:
                    for b in a.value.s32list.s32list:
                        sys_logging("### SAI_PORT_ATTR_SUPPORTED_FEC_MODE = %s ###" %b)
                    assert(fec_list == a.value.s32list.s32list)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_11_SUPPORTED_HALF_DUPLEX_SPEED(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]
        list = [10, 100]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_HALF_DUPLEX_SPEED:
                    for b in a.value.u32list.u32list:
                        sys_logging("### SAI_PORT_ATTR_SUPPORTED_HALF_DUPLEX_SPEED = %d ###" %b)
                        assert(b in list)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_12_SUPPORTED_AUTO_NEG_MODE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 113126
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert (port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE:
                    sys_logging("### SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_AUTO_NEG_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE:
                    sys_logging("### SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE = %d ###" %a.value.booldata)
                    assert(1 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_AUTO_NEG_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE:
                    sys_logging("### SAI_PORT_ATTR_SUPPORTED_AUTO_NEG_MODE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_13_SUPPORTED_FLOW_CONTROL_MODE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 113126
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FLOW_CONTROL_MODE_DISABLE == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_FLOW_CONTROL_MODE_RX_ONLY)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FLOW_CONTROL_MODE_RX_ONLY == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_FLOW_CONTROL_MODE_TX_ONLY)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FLOW_CONTROL_MODE_TX_ONLY == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_FLOW_CONTROL_MODE_BOTH_ENABLE)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FLOW_CONTROL_MODE_BOTH_ENABLE == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_FLOW_CONTROL_MODE_DISABLE)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_SUPPORTED_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FLOW_CONTROL_MODE_DISABLE == a.value.s32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_14_SUPPORTED_ASYMMETRIC_PAUSE_MODE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        always False
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_ASYMMETRIC_PAUSE_MODE:
                    sys_logging("### SAI_PORT_ATTR_SUPPORTED_ASYMMETRIC_PAUSE_MODE = %d ###" %a.value.booldata)
                    assert(False == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_15_SUPPORTED_MEDIA_TYPE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        always SAI_PORT_MEDIA_TYPE_UNKNOWN
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SUPPORTED_MEDIA_TYPE:
                    sys_logging("### SAI_PORT_ATTR_SUPPORTED_MEDIA_TYPE = %d ###" %a.value.s32)
                    assert(SAI_PORT_MEDIA_TYPE_UNKNOWN == a.value.s32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_16_NUMBER_OF_INGRESS_PRIORITY_GROUPS(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                    sys_logging("### SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS = %d ###" %a.value.u32)
                    assert(8 == a.value.u32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_17_INGRESS_PRIORITY_GROUP_LIST(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]
        list = [26, 8218, 16410, 24602, 32794, 40986, 49178, 57370]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST = 0x%x ###" %b)
                        assert(b in list)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_18_OPER_SPEED(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        uml mac link state is always down, the returned value should be zero
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_OPER_SPEED:
                    sys_logging("### SAI_PORT_ATTR_OPER_SPEED = %d ###" %a.value.u32)
                    assert(0 == a.value.u32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_19_HW_LANE_LIST(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        only return one mac_id, should change code and test on board
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_HW_LANE_LIST:
                    for b in a.value.u32list.u32list:
                        sys_logging("### SAI_PORT_ATTR_HW_LANE_LIST = %d ###" %b)
                        assert(b in lane_list)

        finally:
            self.client.sai_thrift_remove_port(port_oid) 


@group('port')
class func_06_set_and_get_port_attribute_fn_20_FULL_DUPLEX_MODE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        always True
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_FULL_DUPLEX_MODE:
                    sys_logging("### SAI_PORT_ATTR_FULL_DUPLEX_MODE = %d ###" %a.value.booldata)
                    assert(True == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_21_SPEED(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        uml is XFI serdes mode by default
        XFI serdes do not support to config mac speed
        SYSTEM MODIFIED KCAO for UML force to 1G
        SAI Bug 113129
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SPEED:
                    sys_logging("### SAI_PORT_ATTR_SPEED = %d ###" %a.value.u32)
                    assert (1000 == a.value.u32)
                    #actually 10g,not 1g

            attr_value = sai_thrift_attribute_value_t(u32=1000)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_SPEED, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_SPEED:
                    sys_logging("### SAI_PORT_ATTR_SPEED = %d ###" %a.value.u32)
                    assert(1000 == a.value.u32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_22_AUTO_NEG_MODE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_AUTO_NEG_MODE:
                    sys_logging("### SAI_PORT_ATTR_AUTO_NEG_MODE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_AUTO_NEG_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_AUTO_NEG_MODE:
                    sys_logging("### SAI_PORT_ATTR_AUTO_NEG_MODE = %d ###" %a.value.booldata)
                    assert(1 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_AUTO_NEG_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_AUTO_NEG_MODE:
                    sys_logging("### SAI_PORT_ATTR_AUTO_NEG_MODE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_23_ADMIN_STATE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###"  %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_ADMIN_STATE:
                    sys_logging("### SAI_PORT_ATTR_ADMIN_STATE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_ADMIN_STATE:
                    sys_logging("### SAI_PORT_ATTR_ADMIN_STATE = %d ###" %a.value.booldata)
                    assert(1 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_ADMIN_STATE:
                    sys_logging("### SAI_PORT_ATTR_ADMIN_STATE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_24_PORT_VLAN_ID(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PORT_VLAN_ID:
                    sys_logging("### SAI_PORT_ATTR_PORT_VLAN_ID = %d ###" %a.value.u16)
                    assert(1 == a.value.u16)

            attr_value = sai_thrift_attribute_value_t(u16=2)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PORT_VLAN_ID:
                    sys_logging("### SAI_PORT_ATTR_PORT_VLAN_ID = %d ###"  %a.value.u16)
                    assert(2 == a.value.u16)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PORT_VLAN_ID:
                    sys_logging("### SAI_PORT_ATTR_PORT_VLAN_ID = %d ###" %a.value.u16)
                    assert(1 == a.value.u16)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_25_DEFAULT_VLAN_PRIORITY(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                    sys_logging("### SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" %a.value.u8)
                    assert(0 == a.value.u8)

            attr_value = sai_thrift_attribute_value_t(u8=3)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                    sys_logging("### SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" %a.value.u8)
                    assert(3 == a.value.u8)

            attr_value = sai_thrift_attribute_value_t(u8=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY:
                    sys_logging("### SAI_PORT_ATTR_DEFAULT_VLAN_PRIORITY = %d ###" %a.value.u8)
                    assert(0 == a.value.u8)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_26_DROP_UNTAGGED(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_DROP_UNTAGGED:
                    sys_logging("### SAI_PORT_ATTR_DROP_UNTAGGED = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_UNTAGGED, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_DROP_UNTAGGED:
                    sys_logging("### SAI_PORT_ATTR_DROP_UNTAGGED = %d ###" %a.value.booldata)
                    assert(1 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_UNTAGGED, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_DROP_UNTAGGED:
                    sys_logging("### SAI_PORT_ATTR_DROP_UNTAGGED = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_27_DROP_TAGGED(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_DROP_TAGGED:
                    sys_logging("### SAI_PORT_ATTR_DROP_TAGGED = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_DROP_TAGGED:
                    sys_logging("### SAI_PORT_ATTR_DROP_TAGGED = %d ###" %a.value.booldata)
                    assert (1 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_DROP_TAGGED:
                    sys_logging("### SAI_PORT_ATTR_DROP_TAGGED = %d ###" %a.value.booldata)
                    assert (0 == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid)

'''
@group('port')
class func_06_set_and_get_port_attribute_fn_28_INTERNAL_LOOPBACK_MODE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        should test on board, uml do not work
        """
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE:
                    sys_logging("### SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE = %d ###" %a.value.s32)
                    assert (SAI_PORT_INTERNAL_LOOPBACK_MODE_NONE == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_INTERNAL_LOOPBACK_MODE_MAC)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE:
                    sys_logging("### SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE = %d ###" %a.value.s32)
                    assert (SAI_PORT_INTERNAL_LOOPBACK_MODE_MAC == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_INTERNAL_LOOPBACK_MODE_NONE)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE:
                    sys_logging("### SAI_PORT_ATTR_INTERNAL_LOOPBACK_MODE = %d ###" %a.value.s32)
                    assert (SAI_PORT_INTERNAL_LOOPBACK_MODE_NONE == a.value.s32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)
'''

@group('port')
class func_06_set_and_get_port_attribute_fn_29_FEC_MODE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        platform bug 110207
        SAI Bug 113264
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_FEC_MODE:
                    sys_logging("### SAI_PORT_ATTR_FEC_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FEC_MODE_NONE == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_FEC_MODE_FC)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FEC_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_FEC_MODE:
                    sys_logging("### SAI_PORT_ATTR_FEC_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FEC_MODE_FC == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_FEC_MODE_NONE)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FEC_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_FEC_MODE:
                    sys_logging("### SAI_PORT_ATTR_FEC_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FEC_MODE_NONE == a.value.s32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_30_UPDATE_DSCP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_UPDATE_DSCP:
                    sys_logging("### SAI_PORT_ATTR_UPDATE_DSCP = %d ###"  %a.value.booldata)
                    assert(0 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_UPDATE_DSCP:
                    sys_logging("### SAI_PORT_ATTR_UPDATE_DSCP = %d ###"  %a.value.booldata)
                    assert(1 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_UPDATE_DSCP:
                    sys_logging("### SAI_PORT_ATTR_UPDATE_DSCP = %d ###"  %a.value.booldata)
                    assert(0 == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid) 


@group('port')
class func_06_set_and_get_port_attribute_fn_31_MTU(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MTU:
                    sys_logging("### SAI_PORT_ATTR_MTU = %d ###" %a.value.u32)
                    assert(1514 == a.value.u32)

            attr_value = sai_thrift_attribute_value_t(u32=9600)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MTU, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MTU:
                    sys_logging("### SAI_PORT_ATTR_MTU = %d ###" %a.value.u32)
                    assert(9600 == a.value.u32)

            attr_value = sai_thrift_attribute_value_t(u32=1514)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MTU, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MTU:
                    sys_logging("### SAI_PORT_ATTR_MTU = %d ###" %a.value.u32)
                    assert(1514 == a.value.u32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_32_FLOOD_STORM_CONTROL_POLICER_ID(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_STORM_CONTROL, 0,
                                                    100000, 0, 0, 0, 0, 0, 0, [0,0,0])

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=policer_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID = %d ###" %a.value.oid)
                    assert(policer_id == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

        finally:
            self.client.sai_thrift_remove_port(port_oid)
            self.client.sai_thrift_remove_policer(policer_id)


@group('port')
class func_06_set_and_get_port_attribute_fn_33_BROADCAST_STORM_CONTROL_POLICER_ID(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_STORM_CONTROL, 0,
                                                    100000, 0, 0, 0, 0, 0, 0, [0,0,0])

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=policer_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID = %d ###" %a.value.oid)
                    assert(policer_id == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

        finally:
            self.client.sai_thrift_remove_port(port_oid)
            self.client.sai_thrift_remove_policer(policer_id)


@group('port')
class func_06_set_and_get_port_attribute_fn_34_MULTICAST_STORM_CONTROL_POLICER_ID(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_STORM_CONTROL, 0,
                                                    100000, 0, 0, 0, 0, 0, 0, [0,0,0])

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###"  %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=policer_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID = %d ###" %a.value.oid)
                    assert(policer_id == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

        finally:
            self.client.sai_thrift_remove_port(port_oid)
            self.client.sai_thrift_remove_policer(policer_id)


@group('port')
class func_06_set_and_get_port_attribute_fn_35_GLOBAL_FLOW_CONTROL_MODE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###"  %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FLOW_CONTROL_MODE_DISABLE == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_FLOW_CONTROL_MODE_BOTH_ENABLE)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FLOW_CONTROL_MODE_BOTH_ENABLE == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_FLOW_CONTROL_MODE_RX_ONLY)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FLOW_CONTROL_MODE_RX_ONLY == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_FLOW_CONTROL_MODE_TX_ONLY)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FLOW_CONTROL_MODE_TX_ONLY == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_FLOW_CONTROL_MODE_DISABLE)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_GLOBAL_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_FLOW_CONTROL_MODE_DISABLE == a.value.s32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_36_INGRESS_ACL(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]
        port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
        sys_logging("### port_oid = 0x%x ###" %port_oid)

        # acl table info
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]

        action = SAI_PACKET_ACTION_DROP
        addr_family = None

        mac_src = '00:11:11:11:11:11'
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst = None
        mac_dst_mask = None

        ip_src = None
        ip_src_mask = None
        ip_dst = None
        ip_dst_mask = None

        in_ports = None
        out_ports = None
        in_port = port_oid
        out_port = None

        svlan_id = None
        svlan_pri = None
        svlan_cfi = None
        cvlan_id = None
        cvlan_pri = None
        cvlan_cfi = None

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

        ip_protocol = None
        ip_tos = None
        ip_ecn = None
        ip_dscp = None
        ip_ttl = None

        src_l4_port = None
        dst_l4_port = None

        ingress_mirror = None
        egress_mirror = None
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        deny_learn = None

        # create acl table
        acl_table_oid = sai_thrift_create_acl_table(self.client,
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
            dst_l4_port)
        sys_logging("create acl table = 0x%x" %acl_table_oid)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INGRESS_ACL:
                    sys_logging("### SAI_PORT_ATTR_INGRESS_ACL = 0x%x ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=acl_table_oid)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INGRESS_ACL:
                    sys_logging("### SAI_PORT_ATTR_INGRESS_ACL = 0x%x ###" %a.value.oid)
                    assert(acl_table_oid == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INGRESS_ACL:
                    sys_logging("### SAI_PORT_ATTR_INGRESS_ACL = 0x%x ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

        finally:
            self.client.sai_thrift_remove_acl_table(acl_table_oid)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_37_INGRESS_MIRROR_SESSION(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 110194
        '''
        switch_init_without_port(self.client)

        speed = 10000
        port1 = sai_thrift_create_port(self.client, "Ethernet1", speed, [0])
        sys_logging("### port_oid = 0x%x ###" %port1)
        port2 = sai_thrift_create_port(self.client, "Ethernet2", speed, [1])
        sys_logging("### port_oid = 0x%x ###" %port2)

        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port1
        monitor_port_list = []
        port_list_valid = False
        ingress_localmirror_id = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port2)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INGRESS_MIRROR_SESSION:
                    assert(0 == a.value.objlist.count)
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_PORT_ATTR_INGRESS_MIRROR_SESSION = %d ###" %b)
                    assert([] == a.value.objlist.object_id_list)

            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[ingress_localmirror_id]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)
            assert(SAI_STATUS_SUCCESS == self.client.sai_thrift_set_port_attribute(port2, attr))

            attrs = self.client.sai_thrift_get_port_attribute(port2)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INGRESS_MIRROR_SESSION:
                    assert(1 == a.value.objlist.count)
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_PORT_ATTR_INGRESS_MIRROR_SESSION = 0x%x ###" %b)
                    assert([ingress_localmirror_id] == a.value.objlist.object_id_list)

            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_MIRROR_SESSION, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port2)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INGRESS_MIRROR_SESSION:
                    assert(0 == a.value.objlist.count)
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_PORT_ATTR_INGRESS_MIRROR_SESSION = %d ###" %b)
                    assert([] == a.value.objlist.object_id_list)

        finally:
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            self.client.sai_thrift_remove_port(port1)
            self.client.sai_thrift_remove_port(port2)


@group('port')
class func_06_set_and_get_port_attribute_fn_38_EGRESS_MIRROR_SESSION(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 110194
        '''
        switch_init_without_port(self.client)

        speed = 10000
        port1 = sai_thrift_create_port(self.client, "Ethernet1", speed, [0])
        sys_logging("### port_oid = 0x%x ###" %port1)
        port2 = sai_thrift_create_port(self.client, "Ethernet2", speed, [1])
        sys_logging("### port_oid = 0x%x ###" %port2)

        mirror_type = SAI_MIRROR_SESSION_TYPE_LOCAL
        monitor_port = port1
        monitor_port_list = []
        port_list_valid = False
        ingress_localmirror_id = sai_thrift_create_mirror_session(self.client,
            mirror_type,
            monitor_port,
            monitor_port_list,
            port_list_valid,
            None, None, None,
            None, None, None,
            None, None, None,
            None, None, None,
            None)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port2)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_EGRESS_MIRROR_SESSION:
                    assert(0 == a.value.objlist.count)
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_PORT_ATTR_EGRESS_MIRROR_SESSION = %d ###" %b)
                    assert([] == a.value.objlist.object_id_list)

            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=1,object_id_list=[ingress_localmirror_id]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_MIRROR_SESSION, value=attr_value)
            assert(SAI_STATUS_SUCCESS == self.client.sai_thrift_set_port_attribute(port2, attr))

            attrs = self.client.sai_thrift_get_port_attribute(port2)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_EGRESS_MIRROR_SESSION:
                    assert(1 == a.value.objlist.count)
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_PORT_ATTR_EGRESS_MIRROR_SESSION = 0x%x ###" %b)
                    assert([ingress_localmirror_id] == a.value.objlist.object_id_list)

            attr_value = sai_thrift_attribute_value_t(objlist=sai_thrift_object_list_t(count=0,object_id_list=[]))
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_MIRROR_SESSION, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port2)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_EGRESS_MIRROR_SESSION:
                    assert(0 == a.value.objlist.count)
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_PORT_ATTR_EGRESS_MIRROR_SESSION = %d ###" %b)
                    assert([] == a.value.objlist.object_id_list)

        finally:
            self.client.sai_thrift_remove_mirror_session(ingress_localmirror_id)
            self.client.sai_thrift_remove_port(port1)
            self.client.sai_thrift_remove_port(port2)


@group('port')
class func_06_set_and_get_port_attribute_fn_39_INGRESS_SAMPLEPACKET_ENABLE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]
        ing_mirror_list = []

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE = 0x%x ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            samplepacket_attrs = []
            samplepacket_attr_value = sai_thrift_attribute_value_t(u32=50)
            samplepacket_attr = sai_thrift_attribute_t(id=SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE,value=samplepacket_attr_value)
            samplepacket_attrs.append(samplepacket_attr)
            samplepacket_id = self.client.sai_thrift_create_samplepacket(samplepacket_attrs)

            attr_value = sai_thrift_attribute_value_t(oid=samplepacket_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid,attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE = 0x%x ###" %a.value.oid)
                    assert(samplepacket_id == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid,attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_INGRESS_SAMPLEPACKET_ENABLE = 0x%x ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

        finally:
            self.client.sai_thrift_remove_samplepacket(samplepacket_id)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_40_EGRESS_SAMPLEPACKET_ENABLE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]
        ing_mirror_list = []

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE = 0x%x ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            samplepacket_attrs = []
            samplepacket_attr_value = sai_thrift_attribute_value_t(u32=50)
            samplepacket_attr = sai_thrift_attribute_t(id=SAI_SAMPLEPACKET_ATTR_SAMPLE_RATE,value=samplepacket_attr_value)
            samplepacket_attrs.append(samplepacket_attr)
            samplepacket_id = self.client.sai_thrift_create_samplepacket(samplepacket_attrs)

            attr_value = sai_thrift_attribute_value_t(oid=samplepacket_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid,attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE = 0x%x ###" %a.value.oid)
                    assert(samplepacket_id == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid,attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_EGRESS_SAMPLEPACKET_ENABLE = 0x%x ###" %a.value.oid)
                    assert (SAI_NULL_OBJECT_ID == a.value.oid)

        finally:
            self.client.sai_thrift_remove_samplepacket(samplepacket_id)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_41_POLICER_ID(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client, SAI_METER_TYPE_BYTES,
                                                    SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list);
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)
          
            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_POLICER_ID = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=policer_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_POLICER_ID = 0x%x ###" %a.value.oid)
                    assert(policer_id == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_POLICER_ID:
                    sys_logging("### SAI_PORT_ATTR_POLICER_ID = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

        finally:
            self.client.sai_thrift_remove_port(port_oid)
            self.client.sai_thrift_remove_policer(policer_id)


@group('port')
class func_06_set_and_get_port_attribute_fn_42_QOS_DOT1P_TO_TC_MAP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        key_list = [0]
        value_list = [7]
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list, [], value_list)

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###"  %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=map_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = 0x%x ###" %a.value.oid)
                    assert(map_id == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP:
                    sys_logging("### SAI_PORT_ATTR_QOS_DOT1P_TO_TC_MAP = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

        finally:
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_43_QOS_DOT1P_TO_COLOR_MAP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        key_list = [0]
        value_list = [SAI_PACKET_COLOR_YELLOW]
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list, [], value_list)

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list);
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=map_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = 0x%x ###" %a.value.oid)
                    assert(map_id == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP:
                    sys_logging("### SAI_PORT_ATTR_QOS_DOT1P_TO_COLOR_MAP = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

        finally:
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_44_QOS_DSCP_TO_TC_MAP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        key_list = [10]
        value_list = [7]
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list, [], value_list)

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list);
            sys_logging(" port_oid = %d "  %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging(" SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = %d " %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=map_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging(" SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = 0x%x " %a.value.oid)
                    assert(map_id == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP:
                    sys_logging(" SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP = %d " %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

        finally:
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_45_QOS_DSCP_TO_COLOR_MAP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        key_list = [10]
        value_list = [SAI_PACKET_COLOR_YELLOW]
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list, [], value_list)

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging(" port_oid = %d "  %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging(" SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = %d " %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=map_id)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging(" SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = 0x%x " %a.value.oid)
                    assert(map_id == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP:
                    sys_logging(" SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP = %d " %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

        finally:
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_46_QOS_TC_AND_COLOR_TO_DOT1P_MAP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_YELLOW]
        value_list1 = [7]
        map_id_tc_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, key_list1, key_list2 , value_list1)

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###"  %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dot1p)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = %d ###" %a.value.oid)
                    assert(map_id_tc_dot1p == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP:
                    sys_logging("### SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

        finally:
            self.client.sai_thrift_remove_qos_map(map_id_tc_dot1p)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_47_QOS_TC_AND_COLOR_TO_DSCP_MAP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_GREEN]
        value_list1 = [20]
        map_id_tc_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, key_list1, key_list2 , value_list1)

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging(" port_oid = %d " %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging(" SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = %d " %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dscp)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging(" SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = %d " %a.value.oid)
                    assert(map_id_tc_dscp == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP:
                    sys_logging(" SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP = %d " %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

        finally:
            self.client.sai_thrift_remove_qos_map(map_id_tc_dscp)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_48_QOS_SCHEDULER_PROFILE_ID(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        sched_type = SAI_SCHEDULING_TYPE_STRICT
        sched_weight = 0
        cir = 2000000
        cbs = 256000
        pir = 1000000
        pbs = 64000

        sched_oid = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
                    sys_logging("### SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
                    sys_logging("### SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID = 0x%x ###" %a.value.oid)
                    assert(sched_oid == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
                    sys_logging("### SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

        finally:
            self.client.sai_thrift_remove_scheduler_profile(sched_oid)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_49_PRIORITY_FLOW_CONTROL_MODE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_SEPARATE)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_SEPARATE == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE = %d ###" %a.value.s32)
                    assert(SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED == a.value.s32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_50_PRIORITY_FLOW_CONTROL(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###"  %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL = %d ###" %a.value.u8)
                    assert(0 == a.value.u8)

            attr_value = sai_thrift_attribute_value_t(u8=123)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL = %d ###" %a.value.u8)
                    assert(123 == a.value.u8)

            attr_value = sai_thrift_attribute_value_t(u8=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL = %d ###" %a.value.u8)
                    assert(0 == a.value.u8)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_51_PRIORITY_FLOW_CONTROL_RX(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_SEPARATE)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX = %d ###" %a.value.u8)
                    assert(0 == a.value.u8)

            attr_value = sai_thrift_attribute_value_t(u8=123)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX = %d ###" %a.value.u8)
                    assert(123 == a.value.u8)

            attr_value = sai_thrift_attribute_value_t(u8=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_RX = %d ###" %a.value.u8)
                    assert(0 == a.value.u8)

        finally:
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_52_PRIORITY_FLOW_CONTROL_TX(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_SEPARATE)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX = %d ###" %a.value.u8)
                    assert(0 == a.value.u8)

            attr_value = sai_thrift_attribute_value_t(u8=123)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX = %d ###" %a.value.u8)
                    assert(123 == a.value.u8)

            attr_value = sai_thrift_attribute_value_t(u8=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX:
                    sys_logging("### SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_TX = %d ###" %a.value.u8)
                    assert(0 == a.value.u8)

        finally:
            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_PRIORITY_FLOW_CONTROL_MODE_COMBINED)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_53_META_DATA(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_META_DATA:
                    sys_logging("### SAI_PORT_ATTR_META_DATA = %d ###" %a.value.u32)
                    assert (0 == a.value.u32)

            attr_value = sai_thrift_attribute_value_t(u32=254)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_META_DATA, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_META_DATA:
                    sys_logging("### SAI_PORT_ATTR_META_DATA = %d ###" %a.value.u32)
                    assert(254 == a.value.u32)

            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_META_DATA, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_META_DATA:
                    sys_logging("### SAI_PORT_ATTR_META_DATA = %d ###" %a.value.u32)
                    assert (0 == a.value.u32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)

# need config port isolation mode port-mode on sdk internal-mode
# Needs to be deprecated. Isolation group can be used instead
#class func_06_set_and_get_port_attribute_fn_54_EGRESS_BLOCK_PORT_LIST(sai_base_test.ThriftInterfaceDataPlane):
#    def runTest(self):
#            
#        switch_init_without_port(self.client)  
#         
#        front1 = "Ethernet1"
#        front2 = "Ethernet2"
#        front3 = "Ethernet3"        
#        speed = 10000
#        lane_list1 = [0]
#        lane_list2 = [1]
#        lane_list3 = [2]        
#        list = []
#
#        warmboot(self.client)
#        try:
#            port_oid1 = sai_thrift_create_port(self.client, front1, speed, lane_list1);
#            sys_logging("### port_oid1 = %d ###"  %port_oid1)
#            assert (port_oid1 != SAI_NULL_OBJECT_ID)
#
#            port_oid2 = sai_thrift_create_port(self.client, front2, speed, lane_list2);
#            sys_logging("### port_oid2 = %d ###"  %port_oid2)
#            assert (port_oid2 != SAI_NULL_OBJECT_ID)
#
#            port_oid3 = sai_thrift_create_port(self.client, front3, speed, lane_list3);
#            sys_logging("### port_oid3 = %d ###"  %port_oid3)
#            assert (port_oid3 != SAI_NULL_OBJECT_ID)
#            
#            attrs = self.client.sai_thrift_get_port_attribute(port_oid1)
#            for a in attrs.attr_list:
#                if a.id == SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST:
#                    for b in a.value.objlist.object_id_list:
#                        sys_logging("### SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST = %d ###"  %b)
#                        assert (b in list)
#
#            port_list = [port_oid2,port_oid3]
#            attr_value = sai_thrift_object_list_t(count=len(port_list), object_id_list=port_list)
#            attr_value1 = sai_thrift_attribute_value_t(objlist=attr_value)
#            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST, value=attr_value1)
#            self.client.sai_thrift_set_port_attribute(port_oid1, attr)
#                        
#            attrs = self.client.sai_thrift_get_port_attribute(port_oid1)
#            for a in attrs.attr_list:
#                if a.id == SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST:
#                    for b in a.value.objlist.object_id_list:
#                        sys_logging("### SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST = %d ###"  %b)
#                        assert (b in port_list)
#                        
#        finally:
#            port_list = []
#            attr_value = sai_thrift_object_list_t(count=len(port_list), object_id_list=port_list)
#            attr_value1 = sai_thrift_attribute_value_t(objlist=attr_value)
#            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EGRESS_BLOCK_PORT_LIST, value=attr_value1)
#            self.client.sai_thrift_set_port_attribute(port_oid1, attr)
#            self.client.sai_thrift_remove_port(port_oid1)
#            self.client.sai_thrift_remove_port(port_oid2)
#            self.client.sai_thrift_remove_port(port_oid3)

'''
class func_06_set_and_get_port_attribute_fn_55_EEE_ENABLE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        not support set and get on d2/tm/tmm
        only support set on gg (get interface missing on gg, need to add)
        """
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_EEE_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_EEE_ENABLE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EEE_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_EEE_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_EEE_ENABLE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)    #for d2 and tm
                    #assert(1 == a.value.booldata)   #for gg

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_EEE_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_EEE_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_EEE_ENABLE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid)
'''

@group('port')
class func_06_set_and_get_port_attribute_fn_56_ISOLATION_GROUP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        isolation_group_oid = sai_thrift_create_isolation_group(self.client, type = SAI_ISOLATION_GROUP_TYPE_PORT)

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_ISOLATION_GROUP:
                    sys_logging("### SAI_PORT_ATTR_ISOLATION_GROUP = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID== a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=isolation_group_oid)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ISOLATION_GROUP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_ISOLATION_GROUP:
                    sys_logging("### SAI_PORT_ATTR_ISOLATION_GROUP = 0x%x ###" %a.value.oid)
                    assert(isolation_group_oid == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ISOLATION_GROUP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_ISOLATION_GROUP:
                    sys_logging("### SAI_PORT_ATTR_ISOLATION_GROUP = %d ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

        finally:
            sai_thrift_remove_isolation_group(self.client, isolation_group_oid)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_57_PKT_TX_ENABLE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PKT_TX_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_PKT_TX_ENABLE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)
                    #board:1 uml:0


            attr_value = sai_thrift_attribute_value_t(booldata=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PKT_TX_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PKT_TX_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_PKT_TX_ENABLE = %d ###" %a.value.booldata)
                    assert(1 == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PKT_TX_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)
            
            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PKT_TX_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_PKT_TX_ENABLE = %d ###" %a.value.booldata)
                    assert(0 == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_58_PTP_MODE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_MODE:
                    sys_logging("### SAI_PORT_ATTR_PTP_MODE = %s ###" %a.value.s32)
                    assert(SAI_PORT_PTP_MODE_NONE == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_PTP_MODE_SINGLE_STEP_TIMESTAMP)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_MODE:
                    sys_logging("### SAI_PORT_ATTR_PTP_MODE = %s ###" %a.value.s32)
                    assert(SAI_PORT_PTP_MODE_SINGLE_STEP_TIMESTAMP == a.value.s32)

            attr_value = sai_thrift_attribute_value_t(s32=SAI_PORT_PTP_MODE_TWO_STEP_TIMESTAMP)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_MODE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_MODE:
                    sys_logging("### SAI_PORT_ATTR_PTP_MODE = %s ###" %a.value.s32)
                    assert(SAI_PORT_PTP_MODE_TWO_STEP_TIMESTAMP == a.value.s32)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_59_PTP_INGRESS_ASYMMETRY_DELAY(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY:
                    sys_logging("### SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY = %s ###" %a.value.u64)
                    assert(0 == a.value.u64)

            attr_value = sai_thrift_attribute_value_t(u64=10)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY:
                    sys_logging("### SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY = %s ###" %a.value.u64)
                    assert(10 == a.value.u64)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY:
                    sys_logging("### SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY = %s ###" %a.value.u64)
                    assert(0 == a.value.u64)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_60_PTP_EGRESS_ASYMMETRY_DELAY(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY:
                    sys_logging("### SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY = %s ###" %a.value.u64)
                    assert(0 == a.value.u64)

            attr_value = sai_thrift_attribute_value_t(u64=30)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY:
                    sys_logging("### SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY = %s ###" %a.value.u64)
                    assert(30 == a.value.u64)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY:
                    sys_logging("### SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY = %s ###" %a.value.u64)
                    assert(0 == a.value.u64)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_61_PTP_PATH_DELAY(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_PATH_DELAY:
                    sys_logging("### SAI_PORT_ATTR_PTP_PATH_DELAY = %s ###" %a.value.u64)
                    assert(0 == a.value.u64)

            attr_value = sai_thrift_attribute_value_t(u64=90)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_PATH_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_PATH_DELAY:
                    sys_logging("### SAI_PORT_ATTR_PTP_PATH_DELAY = %s ###" %a.value.u64)
                    assert(90 == a.value.u64)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_PATH_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_PATH_DELAY:
                    sys_logging("### SAI_PORT_ATTR_PTP_PATH_DELAY = %s ###" %a.value.u64)
                    assert(0 == a.value.u64)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_62_PTP_DOMAIN_ID(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 113153
        '''
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        enable_type = SAI_PTP_ENABLE_BASED_TYPE_PORT
        device_type = SAI_PTP_DEVICE_TYPE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_DOMAIN_ID:
                    sys_logging("### SAI_PORT_ATTR_PTP_DOMAIN_ID = 0x%x ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_DOMAIN_ID:
                    sys_logging("### SAI_PORT_ATTR_PTP_DOMAIN_ID = 0x%x ###" %a.value.oid)
                    assert(ptp_oid == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PTP_DOMAIN_ID:
                    sys_logging("### SAI_PORT_ATTR_PTP_DOMAIN_ID = 0x%x ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

        finally:
            self.client.sai_thrift_remove_port(port_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_63_ES(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        esi_label=10001
        es_oid = sai_thrift_create_es(self.client, esi_label)

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_ES:
                    sys_logging("### SAI_PORT_ATTR_ES = 0x%x ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=es_oid)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_ES:
                    sys_logging("### SAI_PORT_ATTR_ES = 0x%x ###" %a.value.oid)
                    assert(es_oid == a.value.oid)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ES, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_ES:
                    sys_logging("### SAI_PORT_ATTR_ES = 0x%x ###" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

        finally:
            self.client.sai_thrift_remove_es(es_oid)
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_64_Y1731_ENABLE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %s ###" %a.value.booldata)
                    assert(False == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %s ###" %a.value.booldata)
                    assert(True == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_Y1731_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_Y1731_ENABLE = %s ###" %a.value.booldata)
                    assert(False == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_65_Y1731_LM_ENABLE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_Y1731_LM_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_Y1731_LM_ENABLE = %s ###" %a.value.booldata)
                    assert(False == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_LM_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_Y1731_LM_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_Y1731_LM_ENABLE = %s ###" %a.value.booldata)
                    assert(True == a.value.booldata)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_LM_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_Y1731_LM_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_Y1731_LM_ENABLE = %s ###" %a.value.booldata)
                    assert(False == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_66_Y1731_MIP_ENABLE(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_Y1731_MIP_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_Y1731_MIP_ENABLE = %d ###" %(ctypes.c_uint8(a.value.u8).value))
                    assert(0 == (ctypes.c_uint8(a.value.u8)).value)

            attr_value = sai_thrift_attribute_value_t(u8=(ctypes.c_int8(255)).value)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_MIP_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_Y1731_MIP_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_Y1731_MIP_ENABLE = %d ###" %(ctypes.c_uint8(a.value.u8).value))
                    assert(255 == ctypes.c_uint8(a.value.u8).value)

            attr_value = sai_thrift_attribute_value_t(u8=(ctypes.c_int8(0)).value)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_Y1731_MIP_ENABLE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_Y1731_MIP_ENABLE:
                    sys_logging("### SAI_PORT_ATTR_Y1731_MIP_ENABLE = %d ###" %(ctypes.c_uint8(a.value.u8).value))
                    assert(0 == ctypes.c_uint8(a.value.u8).value)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_06_set_and_get_port_attribute_fn_67_MAC_ADDRESS(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)

        front = "Ethernet1"
        speed = 10000
        lane_list = [0]

        warmboot(self.client)
        try:
            port_oid = sai_thrift_create_port(self.client, front, speed, lane_list)
            sys_logging("### port_oid = %d ###" %port_oid)
            assert(port_oid != SAI_NULL_OBJECT_ID)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MAC_ADDRESS:
                    sys_logging("### SAI_PORT_ATTR_MAC_ADDRESS = %s ###" %a.value.mac)
                    assert('00:00:00:00:00:00' == a.value.mac)

            attr_value = sai_thrift_attribute_value_t(mac='00:11:22:33:44:55')
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MAC_ADDRESS:
                    sys_logging("### SAI_PORT_ATTR_MAC_ADDRESS = %s ###" %a.value.mac)
                    assert('00:11:22:33:44:55' == a.value.mac)

            attr_value = sai_thrift_attribute_value_t(mac='00:00:00:00:00:00')
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MAC_ADDRESS, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid, attr)

            attrs = self.client.sai_thrift_get_port_attribute(port_oid)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MAC_ADDRESS:
                    sys_logging("### SAI_PORT_ATTR_MAC_ADDRESS = %s ###" %a.value.mac)
                    assert('00:00:00:00:00:00' == a.value.mac)

        finally:
            self.client.sai_thrift_remove_port(port_oid)


@group('port')
class func_07_get_port_stats(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)
        chipname = testutils.test_params_get()['chipname']

        front1 = "Ethernet1"
        front2 = "Ethernet2"
        speed = 10000
        if chipname == 'tsingma':
            lane_list1 = [0]
            lane_list2 = [1]
        elif chipname == 'tsingma_mx':
            lane_list1 = [0]
            lane_list2 = [4]

        vlan_id1 = 10

        warmboot(self.client)
        try:
            port_oid1 = sai_thrift_create_port(self.client, front1, speed, lane_list1)
            sys_logging("### port_oid1 = 0x%x ###" %port_oid1)
            assert(port_oid1 != SAI_NULL_OBJECT_ID)

            port_oid2 = sai_thrift_create_port(self.client, front2, speed, lane_list2)
            sys_logging("### port_oid2 = 0x%x ###" %port_oid2)
            assert (port_oid2 != SAI_NULL_OBJECT_ID)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid1, attr)
            self.client.sai_thrift_set_port_attribute(port_oid2, attr)

            vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
            vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port_oid1, SAI_VLAN_TAGGING_MODE_TAGGED)
            vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port_oid2, SAI_VLAN_TAGGING_MODE_TAGGED)

            port_cnt_ids = [SAI_PORT_STAT_IF_IN_OCTETS]
            counters_results = []
            counters_results = self.client.sai_thrift_get_port_stats(port_oid1, port_cnt_ids, len(port_cnt_ids))
            sys_logging("###counters_results[0]= %d###" %counters_results[0])
            assert(counters_results[0] == 0)

            pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                    eth_src='00:11:11:11:11:11',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(str(pkt), [1], 1)

            counters_results = self.client.sai_thrift_get_port_stats(port_oid1, port_cnt_ids, len(port_cnt_ids))
            sys_logging("###counters_results[0]= %d###" %counters_results[0])
            assert(counters_results[0] == 104)

        finally:
            self.client.sai_thrift_clear_port_all_stats(port_oid1)
            self.client.sai_thrift_clear_port_all_stats(port_oid2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid1, attr)
            self.client.sai_thrift_set_port_attribute(port_oid2, attr)
            self.client.sai_thrift_remove_port(port_oid1)
            self.client.sai_thrift_remove_port(port_oid2)


@group('port')
class func_08_get_port_stats_ext(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)
        chipname = testutils.test_params_get()['chipname']

        front1 = "Ethernet1"
        front2 = "Ethernet2"
        speed = 10000
        if chipname == 'tsingma':
            lane_list1 = [0]
            lane_list2 = [1]
        elif chipname == 'tsingma_mx':
            lane_list1 = [0]
            lane_list2 = [4]

        vlan_id1 = 10

        warmboot(self.client)
        try:
            port_oid1 = sai_thrift_create_port(self.client, front1, speed, lane_list1)
            sys_logging("### port_oid1 = 0x%x ###" %port_oid1)
            assert(port_oid1 != SAI_NULL_OBJECT_ID)

            port_oid2 = sai_thrift_create_port(self.client, front2, speed, lane_list2)
            sys_logging("### port_oid2 = 0x%x ###" %port_oid2)
            assert (port_oid2 != SAI_NULL_OBJECT_ID)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid1, attr)
            self.client.sai_thrift_set_port_attribute(port_oid2, attr)

            vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
            vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port_oid1, SAI_VLAN_TAGGING_MODE_TAGGED)
            vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port_oid2, SAI_VLAN_TAGGING_MODE_TAGGED)

            port_cnt_ids = [SAI_PORT_STAT_IF_OUT_OCTETS]
            counters_results = []
            mode = SAI_STATS_MODE_READ
            counters_results = self.client.sai_thrift_get_port_stats_ext(port_oid2, port_cnt_ids, mode, len(port_cnt_ids))
            sys_logging("###counters_results[0]= %d###" %counters_results[0])
            assert(counters_results[0] == 0)

            pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                    eth_src='00:11:11:11:11:11',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)

            counters_results = self.client.sai_thrift_get_port_stats_ext(port_oid2, port_cnt_ids, mode, len(port_cnt_ids))
            sys_logging("### counters_results[0]= %d ###" %counters_results[0])
            assert(counters_results[0] == 104)

        finally:
            self.client.sai_thrift_clear_port_all_stats(port_oid1)
            self.client.sai_thrift_clear_port_all_stats(port_oid2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid1, attr)
            self.client.sai_thrift_set_port_attribute(port_oid2, attr)
            self.client.sai_thrift_remove_port(port_oid1)
            self.client.sai_thrift_remove_port(port_oid2)


@group('port')
class func_09_clear_port_stats(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)
        chipname = testutils.test_params_get()['chipname']

        front1 = "Ethernet1"
        front2 = "Ethernet2"
        speed = 10000
        if chipname == 'tsingma':
            lane_list1 = [0]
            lane_list2 = [1]
        elif chipname == 'tsingma_mx':
            lane_list1 = [0]
            lane_list2 = [4]

        vlan_id1 = 10

        warmboot(self.client)
        try:
            port_oid1 = sai_thrift_create_port(self.client, front1, speed, lane_list1)
            sys_logging("### port_oid1 = 0x%x ###" %port_oid1)
            assert(port_oid1 != SAI_NULL_OBJECT_ID)

            port_oid2 = sai_thrift_create_port(self.client, front2, speed, lane_list2)
            sys_logging("### port_oid2 = 0x%x ###" %port_oid2)
            assert (port_oid2 != SAI_NULL_OBJECT_ID)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid1, attr)
            self.client.sai_thrift_set_port_attribute(port_oid2, attr)

            vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
            vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port_oid1, SAI_VLAN_TAGGING_MODE_TAGGED)
            vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port_oid2, SAI_VLAN_TAGGING_MODE_TAGGED)

            port_cnt_ids = [SAI_PORT_STAT_IF_IN_OCTETS,SAI_PORT_STAT_IF_OUT_OCTETS]
            counters_results = []
            mode = SAI_STATS_MODE_READ
            counters_results = self.client.sai_thrift_get_port_stats_ext(port_oid1, port_cnt_ids, mode, len(port_cnt_ids))
            sys_logging("###counters_results[0]= %d###" %counters_results[0])
            sys_logging("###counters_results[1]= %d###" %counters_results[1])
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)

            pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                    eth_src='00:11:11:11:11:11',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt2 = simple_tcp_packet(eth_src='00:22:22:22:22:22',
                                    eth_dst='00:11:11:11:11:11',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt1), [1], 1)

            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(str(pkt2), [0], 1)

            counters_results = self.client.sai_thrift_get_port_stats_ext(port_oid1, port_cnt_ids, mode, len(port_cnt_ids))
            sys_logging("###counters_results[0]= %d###" %counters_results[0])
            sys_logging("###counters_results[1]= %d###" %counters_results[1])
            assert(counters_results[0] == 104)
            assert(counters_results[1] == 104)

            port_cnt_ids1 = [SAI_PORT_STAT_IF_IN_OCTETS]
            self.client.sai_thrift_clear_port_stats(port_oid1, len(port_cnt_ids1), port_cnt_ids1)

            counters_results = self.client.sai_thrift_get_port_stats_ext(port_oid1, port_cnt_ids, mode, len(port_cnt_ids))
            sys_logging("###counters_results[0]= %d###" %counters_results[0])
            sys_logging("###counters_results[1]= %d###" %counters_results[1])
            assert(counters_results[0] == 0)
            assert(counters_results[1] == 104)

        finally:
            self.client.sai_thrift_clear_port_all_stats(port_oid1)
            self.client.sai_thrift_clear_port_all_stats(port_oid2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid1, attr)
            self.client.sai_thrift_set_port_attribute(port_oid2, attr)
            self.client.sai_thrift_remove_port(port_oid1)
            self.client.sai_thrift_remove_port(port_oid2)


@group('port')
class func_10_debug_counter_get_port_stats(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)
        chipname = testutils.test_params_get()['chipname']

        front1 = "Ethernet1"
        front2 = "Ethernet2"
        front3 = "Ethernet3"
        speed = 10000

        if chipname == 'tsingma':
            lane_list1 = [0]
            lane_list2 = [1]
            lane_list3 = [2]
        elif chipname == 'tsingma_mx':
            lane_list1 = [0]
            lane_list2 = [4]
            lane_list3 = [8]

        port1 = sai_thrift_create_port(self.client, front1, speed, lane_list1)
        port2 = sai_thrift_create_port(self.client, front2, speed, lane_list2)
        port3 = sai_thrift_create_port(self.client, front3, speed, lane_list3)

        type = SAI_DEBUG_COUNTER_TYPE_PORT_IN_DROP_REASONS
        in_drop_list = [SAI_IN_DROP_REASON_SMAC_MULTICAST, SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED]
        counter_id = sai_thrift_create_debugcounter(self.client, type, in_drop_list)
        sys_logging("creat counter_id = %d" %counter_id)

        attrs = self.client.sai_thrift_get_debug_counter_attribute(counter_id)
        sys_logging("get attr status = %d" %attrs.status)
        assert(attrs.status == SAI_STATUS_SUCCESS)

        for a in attrs.attr_list:
            if a.id == SAI_DEBUG_COUNTER_ATTR_INDEX:
                sys_logging("get debug index = %d" %a.value.u32)
                debug_counter_index = a.value.u32

        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30

        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        mcastmac = 'ff:ff:00:00:00:01'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id2)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id3)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        #port1 set to drop tagged mode
        attr_value = sai_thrift_attribute_value_t(booldata=1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port3, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac4, port3, mac_action)

        pkt = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac4,
                                eth_src=mac3,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=104)
                                
        droppkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mcastmac,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)
                                
        droppkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        warmboot(self.client)
        try:
            sys_logging("Sending L2 packet port 1 -> port 3 [access vlan=10]), mcast src mac, discard by SAI_IN_DROP_REASON_SMAC_MULTICAST")
            self.ctc_send_packet(0, str(droppkt1))
            self.ctc_verify_no_packet(droppkt1, 2)

            debug_index_list = [debug_counter_index+SAI_PORT_STAT_IN_DROP_REASON_RANGE_BASE]
            counters_results = sai_thrift_read_port_debug_counters(self.client, port1, debug_index_list,SAI_STATS_MODE_READ)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert(counters_results[0] == 1)

            sys_logging("Sending L2 packet port 1 -> port 3 [with access vlan=10]), discard by SAI_IN_DROP_REASON_VLAN_TAG_NOT_ALLOWED")
            self.ctc_send_packet(0, str(droppkt2))
            self.ctc_verify_no_packet(droppkt2, 2)

            counters_results = sai_thrift_read_port_debug_counters(self.client, port1, debug_index_list)
            sys_logging("drop stats = %d " %(counters_results[0]))
            assert(counters_results[0] == 2)

        finally:
            self.client.sai_thrift_clear_port_all_stats(port1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2, port3)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac4, port3)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid1)
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            attr_value = sai_thrift_attribute_value_t(booldata=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_DROP_TAGGED, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_debug_counter(counter_id)
            self.client.sai_thrift_remove_port(port1)
            self.client.sai_thrift_remove_port(port2)
            self.client.sai_thrift_remove_port(port3)


@group('port')
class func_11_clear_port_all_stats(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init_without_port(self.client)
        chipname = testutils.test_params_get()['chipname']

        front1 = "Ethernet1"
        front2 = "Ethernet2"
        speed = 10000
        if chipname == 'tsingma':
            lane_list1 = [0]
            lane_list2 = [1]
        elif chipname == 'tsingma_mx':
            lane_list1 = [0]
            lane_list2 = [4]

        vlan_id1 = 10

        warmboot(self.client)
        try:
            port_oid1 = sai_thrift_create_port(self.client, front1, speed, lane_list1)
            sys_logging("### port_oid1 = 0x%x ###" %port_oid1)
            assert(port_oid1 != SAI_NULL_OBJECT_ID)

            port_oid2 = sai_thrift_create_port(self.client, front2, speed, lane_list2)
            sys_logging("### port_oid2 = 0x%x ###" %port_oid2)
            assert (port_oid2 != SAI_NULL_OBJECT_ID)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid1, attr)
            self.client.sai_thrift_set_port_attribute(port_oid2, attr)

            vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
            vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port_oid1, SAI_VLAN_TAGGING_MODE_TAGGED)
            vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port_oid2, SAI_VLAN_TAGGING_MODE_TAGGED)

            port_cnt_ids = [SAI_PORT_STAT_IF_IN_OCTETS,SAI_PORT_STAT_IF_OUT_OCTETS]
            counters_results = []
            mode = SAI_STATS_MODE_READ
            counters_results = self.client.sai_thrift_get_port_stats_ext(port_oid1, port_cnt_ids, mode, len(port_cnt_ids))
            sys_logging("###counters_results[0]= %d###" %counters_results[0])
            sys_logging("###counters_results[1]= %d###" %counters_results[1])
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)

            pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                    eth_src='00:11:11:11:11:11',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            pkt2 = simple_tcp_packet(eth_src='00:22:22:22:22:22',
                                    eth_dst='00:11:11:11:11:11',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_dst='10.0.0.1',
                                    ip_id=101,
                                    ip_ttl=64)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt1), [1], 1)

            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(str(pkt2), [0], 1)

            counters_results = self.client.sai_thrift_get_port_stats_ext(port_oid1, port_cnt_ids, mode, len(port_cnt_ids))
            sys_logging("###counters_results[0]= %d###" %counters_results[0])
            sys_logging("###counters_results[1]= %d###" %counters_results[1])
            assert(counters_results[0] == 104)
            assert(counters_results[1] == 104)

            self.client.sai_thrift_clear_port_all_stats(port_oid1)

            counters_results = self.client.sai_thrift_get_port_stats_ext(port_oid1, port_cnt_ids, mode, len(port_cnt_ids))
            sys_logging("###counters_results[0]= %d###" %counters_results[0])
            sys_logging("###counters_results[1]= %d###" %counters_results[1])
            assert(counters_results[0] == 0)
            assert(counters_results[1] == 0)

        finally:
            self.client.sai_thrift_clear_port_all_stats(port_oid1)
            self.client.sai_thrift_clear_port_all_stats(port_oid2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port_oid1, attr)
            self.client.sai_thrift_set_port_attribute(port_oid2, attr)
            self.client.sai_thrift_remove_port(port_oid1)
            self.client.sai_thrift_remove_port(port_oid2)


