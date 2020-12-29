# Copyright 2013-present Barefoot Networks, Inc.
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
Thrift SAI Bridge interface tests
"""
import socket
from switch import *
import sai_base_test
import pdb
import time
from scapy.config import *
from scapy.layers.all import *
from ptf.mask import Mask


bridge_attr = ['SAI_BRIDGE_ATTR_TYPE',
               'SAI_BRIDGE_ATTR_PORT_LIST',
               'SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES',
               'SAI_BRIDGE_ATTR_LEARN_DISABLE',
               'SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE',
               'SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_GROUP',
               'SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE',
               'SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_GROUP',
               'SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE',
               'SAI_BRIDGE_ATTR_BROADCAST_FLOOD_GROUP']

bridge_port_attr = ['SAI_BRIDGE_PORT_ATTR_TYPE',
                    'SAI_BRIDGE_PORT_ATTR_PORT_ID',
                    'SAI_BRIDGE_PORT_ATTR_TAGGING_MODE',
                    'SAI_BRIDGE_PORT_ATTR_VLAN_ID',
                    'SAI_BRIDGE_PORT_ATTR_RIF_ID',
                    'SAI_BRIDGE_PORT_ATTR_TUNNEL_ID',
                    'SAI_BRIDGE_PORT_ATTR_BRIDGE_ID',
                    'SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE',
                    'SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES',
                    'SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION',
                    'SAI_BRIDGE_PORT_ATTR_ADMIN_STATE',
                    'SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING',
                    'SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING',
                    'SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP',
                    'SAI_BRIDGE_PORT_ATTR_CROSS_CONNECT_BRIDGE_PORT',
                    'SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_OAM_ENABLE',
                    'SAI_BRIDGE_PORT_ATTR_FRR_NHP_GRP',
                    'SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID',
                    'SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_SERVICE_ID',
                    'SAI_BRIDGE_PORT_ATTR_OUTGOING_SERVICE_VLAN_ID',
                    'SAI_BRIDGE_PORT_ATTR_OUTGOING_SERVICE_VLAN_COS_MODE',
                    'SAI_BRIDGE_PORT_ATTR_OUTGOING_SERVICE_VLAN_COS',
                    'SAI_BRIDGE_PORT_ATTR_CUSTOMER_VLAN_ID']


def _set_bridge_port_attr(client, bport_id, fdb_learning_mode=None):
    '''
    only one attribute can be set at the same time
    '''
    if fdb_learning_mode is not None:
        attr_value = sai_thrift_attribute_value_t(s32=fdb_learning_mode)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE, value=attr_value)
        status = client.sai_thrift_set_bridge_port_attribute(bridge_port_id=bport_id, thrift_attr=attr)
        sys_logging("### set %s to %s, status = 0x%x ###" %(bridge_port_attr[7], fdb_learning_mode, status))
        return status

def _get_bridge_port_attr(client, bport_id, fdb_learning_mode=False):
    bridge_port_attr_list = client.sai_thrift_get_bridge_port_attribute(bridge_port_id=bport_id)
    if (SAI_STATUS_SUCCESS != bridge_port_attr_list.status):
        return None

    return_list = []
    attr_count = 0
    if fdb_learning_mode is True:
        attr_count = attr_count + 1

    if fdb_learning_mode is True:
        for attr in bridge_port_attr_list.attr_list:
            if attr.id == SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_MODE:
                sys_logging("### %s = %s ###" %(bridge_port_attr[7], attr.value.s32))
                if 1 == attr_count:
                    return attr.value.s32
                else:
                    return_list.append(attr.value.s32)

    return return_list


@group('L2')
class func_01_create_bridge_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_01_create_bridge_fn----- ###")
        switch_init(self.client)

        type1 = SAI_BRIDGE_TYPE_1Q
        bridge_id1 = sai_thrift_create_bridge(self.client, type1)
        sys_logging("### create 1Q bridge, bridge_id = 0x%x ###" %bridge_id1)

        type2 = SAI_BRIDGE_TYPE_1D
        bridge_id2 = sai_thrift_create_bridge(self.client, type2)
        sys_logging("### create 1D bridge, bridge_id = 0x%x ###" %bridge_id2)

        type3 = SAI_BRIDGE_TYPE_CROSS_CONNECT
        bridge_id3 = sai_thrift_create_bridge(self.client, type3)
        sys_logging("### create CROSS_CONNECT bridge, bridge_id = 0x%x ###" %bridge_id3)

        warmboot(self.client)

        try:
            assert(SAI_NULL_OBJECT_ID == bridge_id1)
            assert(SAI_NULL_OBJECT_ID != bridge_id2)
            assert(SAI_NULL_OBJECT_ID != bridge_id3)

        finally:
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            self.client.sai_thrift_remove_bridge(bridge_id3)


@group('L2')
class func_02_create_multi_bridge_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_02_create_multi_bridge_fn----- ###")
        switch_init(self.client)

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### create 1D bridge, bridge_id = 0x%x ###" %bridge_id1)

        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### create 1D bridge, bridge_id = 0x%x ###" %bridge_id2)

        bridge_id3 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)
        sys_logging("### create CROSS_CONNECT bridge, bridge_id = 0x%x ###" %bridge_id3)

        bridge_id4 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)
        sys_logging("### create CROSS_CONNECT bridge, bridge_id = 0x%x ###" %bridge_id4)

        warmboot(self.client)

        try:
            assert(bridge_id1 != bridge_id2)
            assert(bridge_id3 != bridge_id4)

        finally:
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            self.client.sai_thrift_remove_bridge(bridge_id3)
            self.client.sai_thrift_remove_bridge(bridge_id4)


@group('L2')
class func_03_create_max_bridge_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_03_create_max_bridge_fn----- ###")
        switch_init(self.client)

        sys_logging("### alloc fid (0~4k) from opf ###")
        bridge_id = [0 for i in range(0,4096)]
        for a in range(2,4095):
            sys_logging("### create bridge id %d ###" %a)
            bridge_id[a] = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
            sys_logging("### bridge_oid = 0x%x ###" %bridge_id[a])

        warmboot(self.client)

        try:
            sys_logging("### create bridge id 4095 ###")
            bridge_id[4095] = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
            sys_logging("### bridge_oid = 0x%x ###" %bridge_id[4095])
            assert(SAI_NULL_OBJECT_ID == bridge_id[4095])

        finally:
            for a in range(2,4095):
                status = self.client.sai_thrift_remove_bridge(bridge_id[a])
                sys_logging("### remove bridge id %d, status = 0x%x ###" %(a,status))
            status = self.client.sai_thrift_remove_bridge(bridge_id[4095])
            sys_logging("### remove bridge id 4095, status = 0x%x ###" %status)


@group('L2')
class func_04_remove_bridge_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_04_remove_bridge_fn----- ###")
        switch_init(self.client)

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        sys_logging("### default 1Q bridge id = 0x%x ###" %default_1q_bridge)
        status1 = self.client.sai_thrift_remove_bridge(default_1q_bridge)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### created 1D bridge id = 0x%x ###" %bridge_id)
        status2 = self.client.sai_thrift_remove_bridge(bridge_id)

        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)
        sys_logging("### created CROSS_CONNECT bridge, bridge_id = 0x%x ###" %bridge_id2)
        status3 = self.client.sai_thrift_remove_bridge(bridge_id2)

        warmboot(self.client)

        try:
            assert(SAI_STATUS_SUCCESS != status1)
            assert(SAI_STATUS_SUCCESS == status2)
            assert(SAI_STATUS_SUCCESS == status3)

        finally:
            sys_logging("### remove 1Q bridge, status = 0x%x ###" %status1)
            sys_logging("### remove 1D bridge, status = 0x%x ###" %status2)
            sys_logging("### remove CROSS_CONNECT bridge, status = 0x%x ###" %status3)


@group('L2')
class func_05_remove_not_exist_bridge_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_05_remove_not_exist_bridge_fn----- ###")
        switch_init(self.client)

        not_exist_bridge_id = 8589942841
        status = self.client.sai_thrift_remove_bridge(not_exist_bridge_id)

        warmboot(self.client)

        try:
            assert(SAI_STATUS_ITEM_NOT_FOUND == status)

        finally:
            sys_logging("### remove bridge, status = 0x%x ###" %status)


@group('L2')
class func_06_set_and_get_bridge_attribute_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_bridge_attribute_fn_0----- ###")
        id_list = [SAI_BRIDGE_ATTR_TYPE]
        switch_init(self.client)

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        sys_logging("### default 1Q bridge id = 0x%x ###" %default_1q_bridge)
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### created 1D bridge id = 0x%x ###" %bridge_id1)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)
        sys_logging("### created CROSS_CONNECT bridge id = 0x%x ###" %bridge_id2)

        warmboot(self.client)

        try:
            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(default_1q_bridge,bridge_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_TYPE_1Q == a.value.s32)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(default_1q_bridge,bridge_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_TYPE_1D == a.value.s32)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id2)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(default_1q_bridge,bridge_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_TYPE_CROSS_CONNECT == a.value.s32)

        finally:
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)


@group('L2')
class func_06_set_and_get_bridge_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_bridge_attribute_fn_1----- ###")
        switch_init(self.client)

        ids_list = [SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        for attribute in switch_attr_list.attr_list:
            if attribute.id == SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS:
                sys_logging("### SAI_SWITCH_ATTR_NUMBER_OF_ACTIVE_PORTS = %d ###" %attribute.value.u32)
                max_port =  attribute.value.u32

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        sys_logging("### default 1Q bridge id = 0x%x ###" %default_1q_bridge)
        ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
        bridge_port_list1 = ret.data.objlist.object_id_list
        count3 = ret.data.objlist.count
        sys_logging("### count of 1Q bridge port list = %d ###" %count3)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### created 1D bridge id = 0x%x ###" %bridge_id)
        ret = self.client.sai_thrift_get_bridge_port_list(bridge_id)
        bridge_port_list2 = ret.data.objlist.object_id_list
        count4 = ret.data.objlist.count
        sys_logging("### count of 1D bridge port list = %d ###" %count4)

        vlan_id = 10
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        bport_id = [0 for i in range(0,4)]
        bport_id[0] = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id, admin_state=False)
        bport_id[1] = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, admin_state=False)
        bport_id[2] = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan_id, admin_state=False)
        bport_id[3] = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id, vlan_id, admin_state=False)

        sys_logging("### By default each port has a corresponding bridge port added to the default 1Q bridge ###")
        ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
        bridge_port_list1 = ret.data.objlist.object_id_list
        count1 = ret.data.objlist.count

        sys_logging("### port can bind to 1Q or 1D bridge at the same time ###")
        ret = self.client.sai_thrift_get_bridge_port_list(bridge_id)
        bridge_port_list2 = ret.data.objlist.object_id_list
        count2 = ret.data.objlist.count

        warmboot(self.client)

        try:
            sys_logging("### count of 1Q bridge port list = %d ###" %count1)
            assert(max_port == count1)
            bport_id1 = [0 for i in range(0,32)]
            for i in range(0,32):
                bport_id1[i] = sai_thrift_get_bridge_port_by_port(self.client, port_list[i])
                sys_logging("### default bport_id[%d] = 0x%x ###" %(i,bport_id1[i]))
                sys_logging("### 1Q bridge_port_list[%d] = 0x%x ###" %(i,bridge_port_list1[i]))
                assert(bport_id1[i] in bridge_port_list1)

            sys_logging("### count of 1D bridge port list = %d ###" %count2)
            assert( 4 == count2)
            for i in range(0,4):
                sys_logging("### created bport_id[%d] = 0x%x ###" %(i,bport_id[i]))
                sys_logging("### 1D bridge port_list[%d] = 0x%x ###" %(i,bridge_port_list2[i]))
                assert(bport_id[i] in bridge_port_list2)

        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[0], port1)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[1], port2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[2], port3)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[3], port4)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_06_set_and_get_bridge_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        only support SAI_BRIDGE_TYPE_1D
        '''
        sys_logging("### -----func_06_set_and_get_bridge_attribute_fn_2----- ###")
        id_list = [SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES]
        switch_init(self.client)

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        sys_logging("### default 1Q bridge id = 0x%x ###" %default_1q_bridge)
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### created 1D bridge id = 0x%x ###" %bridge_id1)

        warmboot(self.client)

        try:
            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            sys_logging("### get 1Q bridge attr: %s, status = 0x%x ###"
                        %(bridge_attr[id_list[0]],bridge_attr_list.status))
            assert(SAI_STATUS_SUCCESS != bridge_attr_list.status)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(bridge_id1,bridge_attr[id_list[0]],a.value.u32))
                    assert(0 == a.value.u32)

            value = 99
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(bridge_id1,bridge_attr[id_list[0]],a.value.u32))
                    assert(value == a.value.u32)

        finally:
            self.client.sai_thrift_remove_bridge(bridge_id1)


@group('L2')
class func_06_set_and_get_bridge_attribute_fn_3(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        only support SAI_BRIDGE_TYPE_1D
        '''
        sys_logging("### -----func_06_set_and_get_bridge_attribute_fn_3----- ###")
        id_list = [SAI_BRIDGE_ATTR_LEARN_DISABLE]
        switch_init(self.client)

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        sys_logging("### default 1Q bridge id = 0x%x ###" %default_1q_bridge)
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### created 1D bridge id = 0x%x ###" %bridge_id1)

        warmboot(self.client)

        try:
            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            sys_logging("### get 1Q bridge attr: %s, status = 0x%x ###"
                        %(bridge_attr[id_list[0]],bridge_attr_list.status))
            assert(SAI_STATUS_SUCCESS != bridge_attr_list.status)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(bridge_id1,bridge_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            value = True
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(bridge_id1,bridge_attr[id_list[0]],a.value.booldata))
                    assert(value == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_bridge(bridge_id1)


@group('L2')
class func_06_set_and_get_bridge_attribute_fn_4(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        only support SAI_BRIDGE_TYPE_1D
        '''
        sys_logging("### -----func_06_set_and_get_bridge_attribute_fn_4----- ###")
        id_list = [SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE]
        switch_init(self.client)

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        sys_logging("### default 1Q bridge id = 0x%x ###" %default_1q_bridge)
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### created 1D bridge id = 0x%x ###" %bridge_id1)

        warmboot(self.client)

        try:
            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            sys_logging("### get 1Q bridge attr: %s, status = 0x%x ###"
                        %(bridge_attr[id_list[0]],bridge_attr_list.status))
            assert(SAI_STATUS_SUCCESS != bridge_attr_list.status)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(bridge_id1,bridge_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.s32)

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(bridge_id1,bridge_attr[id_list[0]],a.value.s32))
                    assert(value == a.value.s32)

        finally:
            self.client.sai_thrift_remove_bridge(bridge_id1)


@group('L2')
class func_06_set_and_get_bridge_attribute_fn_6(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        only support SAI_BRIDGE_TYPE_1D
        '''
        sys_logging("### -----func_06_set_and_get_bridge_attribute_fn_6----- ###")
        id_list = [SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE]
        switch_init(self.client)

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        sys_logging("### default 1Q bridge id = 0x%x ###" %default_1q_bridge)
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### created 1D bridge id = 0x%x ###" %bridge_id1)

        warmboot(self.client)

        try:
            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            sys_logging("### get 1Q bridge attr: %s, status = 0x%x ###"
                        %(bridge_attr[id_list[0]],bridge_attr_list.status))
            assert(SAI_STATUS_SUCCESS != bridge_attr_list.status)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(bridge_id1,bridge_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.s32)

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(bridge_id1,bridge_attr[id_list[0]],a.value.s32))
                    assert(value == a.value.s32)

        finally:
            self.client.sai_thrift_remove_bridge(bridge_id1)


@group('L2')
class func_06_set_and_get_bridge_attribute_fn_8(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        only support SAI_BRIDGE_TYPE_1D
        '''
        sys_logging("### -----func_06_set_and_get_bridge_attribute_fn_8----- ###")
        id_list = [SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE]
        switch_init(self.client)

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        sys_logging("### default 1Q bridge id = 0x%x ###" %default_1q_bridge)
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### created 1D bridge id = 0x%x ###" %bridge_id1)

        warmboot(self.client)

        try:
            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(default_1q_bridge)
            sys_logging("### get 1Q bridge attr: %s, status = 0x%x ###"
                        %(bridge_attr[id_list[0]],bridge_attr_list.status))
            assert(SAI_STATUS_SUCCESS != bridge_attr_list.status)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(bridge_id1,bridge_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_FLOOD_CONTROL_TYPE_SUB_PORTS == a.value.s32)

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)

            bridge_attr_list = self.client.sai_thrift_get_bridge_attribute(bridge_id1)
            for a in bridge_attr_list.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### bridge id = 0x%x, %s = %d ###"
                                %(bridge_id1,bridge_attr[id_list[0]],a.value.s32))
                    assert(value == a.value.s32)

        finally:
            self.client.sai_thrift_remove_bridge(bridge_id1)


@group('L2')
class func_07_create_bridge_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_07_create_bridge_port_fn----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        port1 = port_list[0]

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_port_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1, admin_state=False)
        sys_logging("###create bridge port of type: sub port, id = 0x%x ###" %sub_port_id)

        bport_attr_list = []
        bport_attr_type_value = sai_thrift_attribute_value_t(s32=SAI_BRIDGE_PORT_TYPE_1Q_ROUTER)
        bport_attr_type = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_TYPE, value=bport_attr_type_value)
        bport_attr_list.append(bport_attr_type)
        ret = self.client.sai_thrift_create_bridge_port(bport_attr_list)
        sys_logging("###create bridge port of type: 1Q router, status = 0x%x ###" %ret.status)

        warmboot(self.client)

        try:
            assert(SAI_NULL_OBJECT_ID != sub_port_id)
            assert(SAI_STATUS_SUCCESS != ret.status)

        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_port_id, port1)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_08_create_same_bridge_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_08_create_same_bridge_port_fn----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        self.client.sai_thrift_remove_bridge_port(bport_oid)

        bport_id1 = sai_thrift_create_bridge_port(self.client, port1)
        sys_logging("### create bridge port of type: port, id = 0x%x ###" %bport_id1)
        bport_id2 = sai_thrift_create_bridge_port(self.client, port1)
        sys_logging("### create bridge port of type: port, id = 0x%x ###" %bport_id2)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1, admin_state=False)
        sys_logging("### create bridge port of type: sub port, id = 0x%x ###" %sub_bport_id1)
        sub_bport_id2 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1, admin_state=False)
        sys_logging("### create bridge port of type: sub port, id = 0x%x ###" %sub_bport_id2)

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        bridge_rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                           0, 0, v4_enabled, v6_enabled, mac)
        rif_bport_id1 = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_id, admin_state=False)
        sys_logging("### create bridge port of type: 1D router, id = 0x%x ###" %rif_bport_id1)
        rif_bport_id2 = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_id, admin_state=False)
        sys_logging("### create bridge port of type: 1D router, id = 0x%x ###" %rif_bport_id2)

        vlan_id = 33
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        mac_action = SAI_PACKET_ACTION_FORWARD
        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                     port3, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        tunnel_id= sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id, label_list2,
                                                             next_level_nhop_oid=next_hop)

        tunnel_bport1 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id, admin_state=False)
        sys_logging("### create bridge port of type: tunnel, id = 0x%x ###" %tunnel_bport1)
        tunnel_bport2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id, admin_state=False)
        sys_logging("### create bridge port of type: tunnel, id = 0x%x ###" %tunnel_bport2)
        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, admin_state=False)

        svlan_id = 30
        cvlan_id = 20
        qinq_bport1 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id,
                                                                    svlan_id, cvlan_id, admin_state=False)
        sys_logging("### create bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport1)
        qinq_bport2 = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id,
                                                                    svlan_id, cvlan_id, admin_state=False)
        sys_logging("### create bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport2)

        warmboot(self.client)

        try:
            assert(SAI_NULL_OBJECT_ID != bport_id1)
            assert((SAI_NULL_OBJECT_ID == bport_id2) or (bport_id1 == bport_id2))

            assert(SAI_NULL_OBJECT_ID != sub_bport_id1)
            assert((SAI_NULL_OBJECT_ID == sub_bport_id2) or (sub_bport_id1 == sub_bport_id2))

            assert(SAI_NULL_OBJECT_ID != rif_bport_id1)
            assert((SAI_NULL_OBJECT_ID == rif_bport_id2) or (rif_bport_id1 == rif_bport_id2))

            assert(SAI_NULL_OBJECT_ID != tunnel_bport1)
            assert((SAI_NULL_OBJECT_ID == tunnel_bport2) or (tunnel_bport1 == tunnel_bport2))

            assert(SAI_NULL_OBJECT_ID != qinq_bport1)
            assert((SAI_NULL_OBJECT_ID == qinq_bport2) or (qinq_bport1 == qinq_bport2))

        finally:
            self.client.sai_thrift_remove_bridge_port(qinq_bport1)
            self.client.sai_thrift_remove_bridge_port(qinq_bport2)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport2)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_bridge_port(rif_bport_id1)
            self.client.sai_thrift_remove_bridge_port(rif_bport_id2)
            self.client.sai_thrift_remove_router_interface(bridge_rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport_id1)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

'''
@group('L2')
class func_08_create_same_bridge_port_fn_tunnel_vxlan(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_08_create_same_bridge_port_fn_tunnel_vxlan----- ###")
        switch_init(self.client)

        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac=router_mac
        inner_mac_da = '00:00:AA:AA:00:00'
        inner_mac_sa = '00:00:AA:AA:11:11'
        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_VLAN_ID
        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_VLAN_ID_TO_VNI
        vlan_id = 20
        vni_id = 1000
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        ip_encap_addr_da = '192.168.1.2'
        ip_decap_addr_da = '192.168.1.1'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vr_id = sai_thrift_get_default_router_id(self.client)

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK,
                                                             port1, 0, v4_enabled, v6_enabled, mac)

        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)
        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type,
                                                                       tunnel_map_decap_id, vni_id, vlan_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type,
                                                                       tunnel_map_encap_id, vlan_id, vni_id)

        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]
        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa,
                                                   encap_mapper_list=encap_mapper_list,
                                                   decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        btunnel_id1 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        sys_logging("###create bridge port of type: tunnel, id = 0x%x ###" %btunnel_id1)
        btunnel_id2 = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        sys_logging("###create bridge port of type: tunnel, id = 0x%x ###" %btunnel_id2)

        warmboot(self.client)

        try:
            assert((SAI_NULL_OBJECT_ID == btunnel_id2) or (btunnel_id1 == btunnel_id2))

        finally:
            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)
            self.client.sai_thrift_remove_bridge_port(btunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id)
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id)
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
'''

@group('L2')
class func_09_remove_bridge_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112429
        '''
        sys_logging("### -----func_09_remove_bridge_port_fn----- ###")
        switch_init(self.client)

        vlan_id = 10
        vlan_id1 = 20
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        sys_logging("### default 1Q bridge id = 0x%x ###" %default_1q_bridge)
        ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
        count1 = ret.data.objlist.count
        sys_logging("### count of 1Q bridge port list = %d ###" %count1)
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        self.client.sai_thrift_remove_bridge_port(bport_oid)
        ret = self.client.sai_thrift_get_bridge_port_list(default_1q_bridge)
        count2 = ret.data.objlist.count
        sys_logging("### count of 1Q bridge port list = %d ###" %count2)

        bport_id = [0 for i in range(0,7)]
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sys_logging("### created 1D bridge id = 0x%x ###" %bridge_id)
        bport_id[0] = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id, admin_state=False)
        bport_id[1] = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, admin_state=False)
        bport_id[2] = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id, vlan_id, admin_state=False)
        bport_id[3] = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id, vlan_id, admin_state=False)

        ret = self.client.sai_thrift_get_bridge_port_list(bridge_id)
        count3 = ret.data.objlist.count
        sys_logging("### count of 1D bridge port list = %d ###" %count3)
        sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[0])
        sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[1])
        ret = self.client.sai_thrift_get_bridge_port_list(bridge_id)
        count4 = ret.data.objlist.count
        sys_logging("### count of 1D bridge port list = %d ###" %count4)

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_CROSS_CONNECT)
        sys_logging("### created CROSS_CONNECT bridge, bridge_id = 0x%x ###" %bridge_id1)
        bport_id[4] = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1, admin_state=False)
        bport_id[5] = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id1, admin_state=False)
        bport_id[6] = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id1, vlan_id1, admin_state=False)

        ret = self.client.sai_thrift_get_bridge_port_list(bridge_id1)
        count5 = ret.data.objlist.count
        sys_logging("### count of CROSS CONNECT bridge port list = %d ###" %count5)
        sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[6])
        sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[5])
        ret = self.client.sai_thrift_get_bridge_port_list(bridge_id1)
        count6 = ret.data.objlist.count
        sys_logging("### count of CROSS CONNECT bridge port list = %d ###" %count6)

        for i in range(0,7):
            sys_logging("### created sub port id = 0x%x ###" %bport_id[i])

        warmboot(self.client)

        try:
            assert(32 == count1)
            assert(31 == count2)
            assert(4 == count3)
            assert(2 == count4)
            assert(3 == count5)
            assert(1 == count6)

        finally:
            sai_thrift_create_bridge_port(self.client, port1)
            sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[2])
            sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[3])
            sai_thrift_remove_bridge_sub_port_2(self.client, bport_id[4])
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id1)


@group('L2')
class func_10_remove_not_exist_bridge_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_10_remove_not_exist_bridge_port_fn----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        port1 = port_list[0]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)

        not_exist_bport_oid = bport_oid+1
        status = self.client.sai_thrift_remove_bridge_port(not_exist_bport_oid)

        warmboot(self.client)

        try:
            assert(SAI_STATUS_INVALID_OBJECT_ID == status)

        finally:
            sys_logging("### remove not exist bridge port, status = 0x%x ###" %status)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_0----- ###")
        id_list = [SAI_BRIDGE_ATTR_TYPE]
        switch_init(self.client)

        vlan_id1 = 10
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### default bridge port of type: port, id = 0x%x ###" %bport)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1, admin_state=False)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport)

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        bridge_rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                           0, 0, v4_enabled, v6_enabled, mac)
        rif_bport = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_id, admin_state=False)
        sys_logging("### created bridge port of type: 1D router, id = 0x%x ###" %rif_bport)

        vlan_id = 33
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        mac_action = SAI_PACKET_ACTION_FORWARD
        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                     port3, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        tunnel_id= sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id, label_list2,
                                                             next_level_nhop_oid=next_hop)

        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id, admin_state=False)
        sys_logging("###created bridge port of type: tunnel, id = 0x%x ###" %tunnel_bport)

        svlan_id = 30
        cvlan_id = 20
        qinq_bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id,
                                                                    svlan_id, cvlan_id, admin_state=False)
        sys_logging("###created bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_PORT_TYPE_PORT == a.value.s32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_PORT_TYPE_SUB_PORT == a.value.s32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(rif_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_PORT_TYPE_1D_ROUTER == a.value.s32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_PORT_TYPE_TUNNEL == a.value.s32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(qinq_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_PORT_TYPE_DOUBLE_VLAN_SUB_PORT == a.value.s32)

        finally:
            self.client.sai_thrift_remove_bridge_port(qinq_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_bridge_port(rif_bport)
            self.client.sai_thrift_remove_router_interface(bridge_rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_1----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_PORT_ID]
        switch_init(self.client)

        vlan_id1 = 10
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### default bridge port of type: port, id = 0x%x ###" %bport)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id1, admin_state=False)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport)

        svlan_id = 30
        cvlan_id = 20
        qinq_bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port3, bridge_id,
                                                                    svlan_id, cvlan_id, admin_state=False)
        sys_logging("### created bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(port1 == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(port2 == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(qinq_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(port3 == a.value.oid)

        finally:
            self.client.sai_thrift_remove_bridge_port(qinq_bport)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        create-only, not support set SAI_BRIDGE_PORT_ATTR_TAGGING_MODE
        '''
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_2----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_TAGGING_MODE]
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 200
        port1 = port_list[1]
        port2 = port_list[2]
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport1 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id1, admin_state=False)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport1)
        sub_bport2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id2, admin_state=False,
                                                       tagging_mode=SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport2)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport1)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED == a.value.s32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport2)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED == a.value.s32)

            value = SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            status = self.client.sai_thrift_set_bridge_port_attribute(sub_bport1, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)

            value = SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            status = self.client.sai_thrift_set_bridge_port_attribute(sub_bport2, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)

        finally:
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport1)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport2)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_3(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_3----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_VLAN_ID]
        switch_init(self.client)

        vlan_id = 10
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id, admin_state=False)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport)

        svlan_id = 30
        cvlan_id = 20
        qinq_bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id,
                                                                    svlan_id, cvlan_id, admin_state=False)
        sys_logging("### created bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.u16))
                    assert(vlan_id == a.value.u16)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(qinq_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.u16))
                    assert(svlan_id == a.value.u16)

        finally:
            self.client.sai_thrift_remove_bridge_port(qinq_bport)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_4(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_4----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_RIF_ID]
        switch_init(self.client)

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        bridge_rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                           0, 0, v4_enabled, v6_enabled, mac)
        sys_logging("### created router interface of type: bridge, id = 0x%x ###" %bridge_rif_id)
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        rif_bport = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_id, admin_state=False)
        sys_logging("### created bridge port of type: 1D router, id = 0x%x ###" %rif_bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(rif_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(bridge_rif_id == a.value.oid)

        finally:
            self.client.sai_thrift_remove_bridge_port(rif_bport)
            self.client.sai_thrift_remove_router_interface(bridge_rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_5(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_5----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_TUNNEL_ID]
        switch_init(self.client)

        port3 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                     port3, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        tunnel_id= sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        sys_logging("### created tunnel, id = 0x%x ###" %tunnel_id)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id, label_list2,
                                                             next_level_nhop_oid=next_hop)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id, admin_state=False)
        sys_logging("### created bridge port of type: tunnel, id = 0x%x ###" %tunnel_bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(tunnel_id == a.value.oid)

        finally:
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_6(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_6----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_BRIDGE_ID]
        switch_init(self.client)

        vlan_id1 = 10
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1, admin_state=False)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport)

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        bridge_rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                           0, 0, v4_enabled, v6_enabled, mac)
        rif_bport = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_id, admin_state=False)
        sys_logging("### created bridge port of type: 1D router, id = 0x%x ###" %rif_bport)

        vlan_id = 33
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        mac_action = SAI_PACKET_ACTION_FORWARD
        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                     port3, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        tunnel_id= sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id, label_list2,
                                                             next_level_nhop_oid=next_hop)

        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id, admin_state=False)
        sys_logging("### created bridge port of type: tunnel, id = 0x%x ###" %tunnel_bport)

        svlan_id = 30
        cvlan_id = 20
        qinq_bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id,
                                                                    svlan_id, cvlan_id, admin_state=False)
        sys_logging("### created bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(bridge_id == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(rif_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(bridge_id == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(bridge_id == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(qinq_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(bridge_id == a.value.oid)

            bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
            value = bridge_id1
            attr_value = sai_thrift_attribute_value_t(oid=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            status = self.client.sai_thrift_set_bridge_port_attribute(sub_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_set_bridge_port_attribute(rif_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_set_bridge_port_attribute(qinq_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(bridge_id1 == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(rif_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(bridge_id1 == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(bridge_id1 == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(qinq_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(bridge_id1 == a.value.oid)

        finally:
            self.client.sai_thrift_remove_bridge_port(qinq_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_bridge_port(rif_bport)
            self.client.sai_thrift_remove_router_interface(bridge_rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_bridge(bridge_id1)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_7(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 110766
        '''
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_7----- ###")
        learning_mode = [SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DROP,
                         SAI_BRIDGE_PORT_FDB_LEARNING_MODE_DISABLE,
                         SAI_BRIDGE_PORT_FDB_LEARNING_MODE_HW,
                         SAI_BRIDGE_PORT_FDB_LEARNING_MODE_CPU_TRAP,
                         SAI_BRIDGE_PORT_FDB_LEARNING_MODE_CPU_LOG,
                         SAI_BRIDGE_PORT_FDB_LEARNING_MODE_FDB_NOTIFICATION]
        switch_init(self.client)

        port1 = port_list[0] #SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
        port2 = port_list[1] #SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
        port3 = port_list[2] #SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_PORT
        port4 = port_list[3] #SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
        port5 = port_list[4] #SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_DOUBLE_VLAN_SUB_PORT
        port6 = port_list[5] #SAI_ROUTER_INTERFACE_TYPE_PORT

        default_1q_bridge = switch.default_1q_bridge
        default_vlan_id = switch.default_vlan.oid
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### default bridge port of type: port, id = 0x%x ###" %bport1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)
        sys_logging("### default bridge port of type: port, id = 0x%x ###" %bport2)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        bport3 = sai_thrift_get_bridge_port_by_port(self.client, port3)
        self.client.sai_thrift_remove_bridge_port(bport3)
        bport_1d = sai_thrift_create_bridge_port(self.client, port3, bridge_id=bridge_id)
        sys_logging("### created bridge port of type: port_1d, id = 0x%x ###" %bport_1d)

        vlan1 = 10
        sub_bport = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id, vlan1)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport)

        vlan2 = 20
        qinq_bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port5, bridge_id, vlan1, vlan2)
        sys_logging("### created bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport)

        vr_id = sai_thrift_create_virtual_router(self.client, 1, 1)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, 1, 1, '', dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, 1, 1, '')
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                     port6, 0, 1, 1, '')
        ip_da = '20.20.20.1'
        ip_sa = '10.10.10.1'
        dmac = '00:55:55:55:55:55'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        sai_thrift_create_inseg_entry(self.client, label1, 1, None, rif_id3, SAI_PACKET_ACTION_FORWARD)
        tunnel_id= sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        sai_thrift_create_inseg_entry(self.client, label2, 1, None, rif_id2, SAI_PACKET_ACTION_FORWARD, tunnel_id=tunnel_id)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id, label_list2, next_level_nhop_oid=next_hop)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)
        sys_logging("### created bridge port of type: tunnel, id = 0x%x ###" %tunnel_bport)

        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst=ip_da, ip_src=ip_sa, ip_ttl=64, pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan1,
                                 ip_dst=ip_da, ip_src=ip_sa, ip_ttl=64, pktlen=104)
        pkt3 = simple_qinq_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                      dl_vlan_outer=vlan1, dl_vlan_pcp_outer=0, dl_vlan_cfi_outer=0,
                                      vlan_vid=vlan2, vlan_pcp=0, dl_vlan_cfi=0,
                                      ip_dst=ip_da, ip_src=ip_sa, ip_ttl=64, pktlen=108)
        pkt4 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_dst=ip_da, ip_src=ip_sa, ip_ttl=64, pktlen=104)

        mpls = [{'label':label1, 'tc':0, 'ttl':32, 's':0}, {'label':label2, 'tc':0, 'ttl':16, 's':1}]
        inner_ip_pkt = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                         dl_vlan_enable=True, vlan_vid=vlan2,
                                         ip_dst=ip_da, ip_src=ip_sa,
                                         ip_ttl=64, ip_ihl=5, pktlen=104)
        pkt5 = simple_mpls_packet(eth_dst=router_mac, eth_src=dmac, mpls_type=0x8847,
                                  mpls_tags=mpls, inner_frame=inner_ip_pkt)

        warmboot(self.client)

        try:
            '''
            STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            sys_logging("### -----STEP 1: SAI_BRIDGE_TYPE_1Q, SAI_BRIDGE_PORT_TYPE_PORT----- ###")
            assert(learning_mode[2] == _get_bridge_port_attr(self.client, bport1, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, default_vlan_id, mac2, bport2))
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            assert(1 == sai_thrift_check_fdb_exist(self.client, default_vlan_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, default_vlan_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, default_vlan_id, mac2))

            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, bport1, fdb_learning_mode=learning_mode[0]))
            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, bport1, fdb_learning_mode=learning_mode[3]))
            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, bport1, fdb_learning_mode=learning_mode[4]))

            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, default_vlan_id, mac2, bport2))
            assert(SAI_STATUS_SUCCESS == _set_bridge_port_attr(self.client, bport1, fdb_learning_mode=learning_mode[1]))
            assert(learning_mode[1] == _get_bridge_port_attr(self.client, bport1, fdb_learning_mode=True))
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            assert(0 == sai_thrift_check_fdb_exist(self.client, default_vlan_id, mac1))
            assert(SAI_STATUS_SUCCESS != sai_thrift_delete_fdb(self.client, default_vlan_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, default_vlan_id, mac2))

            assert(SAI_STATUS_SUCCESS == _set_bridge_port_attr(self.client, bport1, fdb_learning_mode=learning_mode[5]))
            assert(learning_mode[5] == _get_bridge_port_attr(self.client, bport1, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, default_vlan_id, mac2, bport1))
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 0)
            assert(1 == sai_thrift_check_fdb_exist(self.client, default_vlan_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, default_vlan_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, default_vlan_id, mac2))

            '''
            STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_PORT
            '''
            sys_logging("### -----STEP 2: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_PORT----- ###")
            assert(learning_mode[2] == _get_bridge_port_attr(self.client, bport_1d, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_bport))
            self.ctc_send_packet(2, pkt1)
            self.ctc_verify_packet(pkt2, 3)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, bport_1d, fdb_learning_mode=learning_mode[0]))
            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, bport_1d, fdb_learning_mode=learning_mode[3]))
            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, bport_1d, fdb_learning_mode=learning_mode[4]))

            assert(SAI_STATUS_SUCCESS == _set_bridge_port_attr(self.client, bport_1d, fdb_learning_mode=learning_mode[1]))
            assert(learning_mode[1] == _get_bridge_port_attr(self.client, bport_1d, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, qinq_bport))
            self.ctc_send_packet(2, pkt1)
            self.ctc_verify_packet(pkt2, 4)
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS != sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

            assert(SAI_STATUS_SUCCESS == _set_bridge_port_attr(self.client, bport_1d, fdb_learning_mode=learning_mode[5]))
            assert(learning_mode[5] == _get_bridge_port_attr(self.client, bport_1d, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, bport_1d))
            self.ctc_send_packet(2, pkt1)
            self.ctc_verify_no_packet(pkt1, 2)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

            '''
            STEP 3: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT
            '''
            sys_logging("### -----STEP 3: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_SUB_PORT----- ###")
            assert(learning_mode[2] == _get_bridge_port_attr(self.client, sub_bport, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, bport_1d))
            self.ctc_send_packet(3, pkt2)
            self.ctc_verify_packet(pkt1, 2)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, sub_bport, fdb_learning_mode=learning_mode[0]))
            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, sub_bport, fdb_learning_mode=learning_mode[3]))
            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, sub_bport, fdb_learning_mode=learning_mode[4]))

            assert(SAI_STATUS_SUCCESS == _set_bridge_port_attr(self.client, sub_bport, fdb_learning_mode=learning_mode[1]))
            assert(learning_mode[1] == _get_bridge_port_attr(self.client, sub_bport, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, qinq_bport))
            self.ctc_send_packet(3, pkt2)
            self.ctc_verify_packet(pkt2, 4)
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS != sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

            assert(SAI_STATUS_SUCCESS == _set_bridge_port_attr(self.client, sub_bport, fdb_learning_mode=learning_mode[5]))
            assert(learning_mode[5] == _get_bridge_port_attr(self.client, sub_bport, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_bport))
            self.ctc_send_packet(3, pkt2)
            self.ctc_verify_no_packet(pkt2, 3)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

            '''
            STEP 4: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_DOUBLE_VLAN_SUB_PORT
            '''
            sys_logging("### -----STEP 4: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_DOUBLE_VLAN_SUB_PORT----- ###")
            assert(learning_mode[2] == _get_bridge_port_attr(self.client, qinq_bport, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, bport_1d))
            self.ctc_send_packet(4, pkt3)
            self.ctc_verify_packet(pkt4, 2)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, qinq_bport, fdb_learning_mode=learning_mode[0]))
            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, qinq_bport, fdb_learning_mode=learning_mode[3]))
            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, qinq_bport, fdb_learning_mode=learning_mode[4]))

            assert(SAI_STATUS_SUCCESS == _set_bridge_port_attr(self.client, qinq_bport, fdb_learning_mode=learning_mode[1]))
            assert(learning_mode[1] == _get_bridge_port_attr(self.client, qinq_bport, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_bport))
            self.ctc_send_packet(4, pkt3)
            self.ctc_verify_packet(pkt3, 3)
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS != sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

            assert(SAI_STATUS_SUCCESS == _set_bridge_port_attr(self.client, qinq_bport, fdb_learning_mode=learning_mode[5]))
            assert(learning_mode[5] == _get_bridge_port_attr(self.client, qinq_bport, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, qinq_bport))
            self.ctc_send_packet(4, pkt3)
            self.ctc_verify_no_packet(pkt3, 4)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

            '''
            STEP 5: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_TUNNEL
            '''
            sys_logging("### -----STEP 5: SAI_BRIDGE_TYPE_1D, SAI_BRIDGE_PORT_TYPE_TUNNEL----- ###")
            assert(learning_mode[2] == _get_bridge_port_attr(self.client, tunnel_bport, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, bport_1d))
            self.ctc_send_packet(5, pkt5)
            self.ctc_verify_packet(pkt4, 2)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, tunnel_bport, fdb_learning_mode=learning_mode[0]))
            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, tunnel_bport, fdb_learning_mode=learning_mode[3]))
            assert(SAI_STATUS_SUCCESS != _set_bridge_port_attr(self.client, tunnel_bport, fdb_learning_mode=learning_mode[4]))

            assert(SAI_STATUS_SUCCESS == _set_bridge_port_attr(self.client, tunnel_bport, fdb_learning_mode=learning_mode[1]))
            assert(learning_mode[1] == _get_bridge_port_attr(self.client, tunnel_bport, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, sub_bport))
            self.ctc_send_packet(5, pkt5)
            self.ctc_verify_packet(pkt3, 3)
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS != sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

            assert(SAI_STATUS_SUCCESS == _set_bridge_port_attr(self.client, tunnel_bport, fdb_learning_mode=learning_mode[5]))
            assert(learning_mode[5] == _get_bridge_port_attr(self.client, tunnel_bport, fdb_learning_mode=True))
            assert(SAI_STATUS_SUCCESS == sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, qinq_bport))
            self.ctc_send_packet(5, pkt5)
            self.ctc_verify_packet(pkt3, 4)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac1))
            assert(SAI_STATUS_SUCCESS == sai_thrift_delete_fdb(self.client, bridge_id, mac2))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_bridge_port(qinq_bport)
            self.client.sai_thrift_remove_bridge_port(sub_bport)
            self.client.sai_thrift_remove_bridge_port(bport_1d)
            sai_thrift_create_bridge_port(self.client, port3)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_8(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        only support SAI_BRIDGE_PORT_TYPE_PORT
        '''
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_8----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES]
        switch_init(self.client)

        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### default bridge port of type: port, id = 0x%x ###" %bport)

        vlan_id1 = 10
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1, admin_state=False)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport)

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        bridge_rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                           0, 0, v4_enabled, v6_enabled, mac)
        rif_bport = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_id, admin_state=False)
        sys_logging("### created bridge port of type: 1D router, id = 0x%x ###" %rif_bport)

        vlan_id = 33
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        mac_action = SAI_PACKET_ACTION_FORWARD
        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                     port3, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        tunnel_id= sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id, label_list2,
                                                             next_level_nhop_oid=next_hop)

        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id, admin_state=False)
        sys_logging("### created bridge port of type: tunnel, id = 0x%x ###" %tunnel_bport)

        svlan_id = 30
        cvlan_id = 20
        qinq_bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id,
                                                                    svlan_id, cvlan_id, admin_state=False)
        sys_logging("### created bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.u32))
                    assert(0 == a.value.u32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.u32))
                    assert(0 == a.value.u32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(rif_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.u32))
                    assert(0 == a.value.u32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.u32))
                    assert(0 == a.value.u32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(qinq_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.u32))
                    assert(0 == a.value.u32)

            value = 333
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            status = self.client.sai_thrift_set_bridge_port_attribute(bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_set_bridge_port_attribute(sub_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(rif_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(qinq_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.u32))
                    assert(value == a.value.u32)

        finally:
            self.client.sai_thrift_remove_bridge_port(bport)
            bport = sai_thrift_create_bridge_port(self.client, port1)
            self.client.sai_thrift_remove_bridge_port(qinq_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_bridge_port(rif_bport)
            self.client.sai_thrift_remove_router_interface(bridge_rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_9(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        only support SAI_BRIDGE_PORT_TYPE_PORT
        SAI Bug 112461
        '''
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_9----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION]
        switch_init(self.client)

        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### default bridge port of type: port, id = 0x%x ###" %bport)

        vlan_id1 = 10
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1, admin_state=False)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport)

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        bridge_rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                           0, 0, v4_enabled, v6_enabled, mac)
        rif_bport = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_id, admin_state=False)
        sys_logging("### created bridge port of type: 1D router, id = 0x%x ###" %rif_bport)

        vlan_id = 33
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        mac_action = SAI_PACKET_ACTION_FORWARD
        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                     port3, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        tunnel_id= sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id, label_list2,
                                                             next_level_nhop_oid=next_hop)

        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id, admin_state=False)
        sys_logging("### created bridge port of type: tunnel, id = 0x%x ###" %tunnel_bport)

        svlan_id = 30
        cvlan_id = 20
        qinq_bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id,
                                                                    svlan_id, cvlan_id, admin_state=False)
        sys_logging("### created bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_PACKET_ACTION_DENY == a.value.s32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_PACKET_ACTION_DROP == a.value.s32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(rif_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_PACKET_ACTION_DROP == a.value.s32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_PACKET_ACTION_DROP == a.value.s32)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(qinq_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_PACKET_ACTION_DROP == a.value.s32)

            #only support SAI_BRIDGE_PORT_TYPE_PORT
            value = SAI_PACKET_ACTION_FORWARD
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            status = self.client.sai_thrift_set_bridge_port_attribute(bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_set_bridge_port_attribute(sub_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(rif_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(qinq_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.s32))
                    assert(SAI_PACKET_ACTION_TRANSIT == a.value.s32)

        finally:
            self.client.sai_thrift_remove_bridge_port(bport)
            bport = sai_thrift_create_bridge_port(self.client, port1)
            self.client.sai_thrift_remove_bridge_port(qinq_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_bridge_port(rif_bport)
            self.client.sai_thrift_remove_router_interface(bridge_rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_10(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_10----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_ADMIN_STATE]
        switch_init(self.client)

        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport = sai_thrift_get_bridge_port_by_port(self.client, port1)
        self.client.sai_thrift_remove_bridge_port(bport)
        bport = sai_thrift_create_bridge_port(self.client, port1, admin_state=False)
        sys_logging("### created bridge port of type: port, id = 0x%x ###" %bport)

        vlan_id1 = 10
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1, admin_state=False)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport)

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        bridge_rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                           0, 0, v4_enabled, v6_enabled, mac)
        rif_bport = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_id, admin_state=False)
        sys_logging("### created bridge port of type: 1D router, id = 0x%x ###" %rif_bport)

        vlan_id = 33
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        mac_action = SAI_PACKET_ACTION_FORWARD
        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                     port3, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        tunnel_id= sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id, label_list2,
                                                             next_level_nhop_oid=next_hop)

        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id, admin_state=False)
        sys_logging("### created bridge port of type: tunnel, id = 0x%x ###" %tunnel_bport)

        svlan_id = 30
        cvlan_id = 20
        qinq_bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id,
                                                                   svlan_id, cvlan_id, admin_state=False)
        sys_logging("### created bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(rif_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(qinq_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            value = True
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            status = self.client.sai_thrift_set_bridge_port_attribute(bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_set_bridge_port_attribute(sub_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_set_bridge_port_attribute(rif_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_set_bridge_port_attribute(qinq_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(value == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(value == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(rif_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(value == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(value == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(qinq_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(value == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_bridge_port(qinq_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_bridge_port(rif_bport)
            self.client.sai_thrift_remove_router_interface(bridge_rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_11(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        only support SAI_BRIDGE_PORT_TYPE_PORT
        '''
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_11----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING]
        switch_init(self.client)

        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### default bridge port of type: port, id = 0x%x ###" %bport)

        vlan_id1 = 10
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1, admin_state=False)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport)

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        bridge_rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                           0, 0, v4_enabled, v6_enabled, mac)
        rif_bport = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_id, admin_state=False)
        sys_logging("### created bridge port of type: 1D router, id = 0x%x ###" %rif_bport)

        vlan_id = 33
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        mac_action = SAI_PACKET_ACTION_FORWARD
        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                     port3, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        tunnel_id= sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id, label_list2,
                                                             next_level_nhop_oid=next_hop)

        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id, admin_state=False)
        sys_logging("### created bridge port of type: tunnel, id = 0x%x ###" %tunnel_bport)

        svlan_id = 30
        cvlan_id = 20
        qinq_bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id,
                                                                   svlan_id, cvlan_id, admin_state=False)
        sys_logging("### created bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(rif_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(qinq_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            value = True
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            status = self.client.sai_thrift_set_bridge_port_attribute(bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_set_bridge_port_attribute(sub_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(rif_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(qinq_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(value == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_bridge_port(bport)
            bport = sai_thrift_create_bridge_port(self.client, port1)
            self.client.sai_thrift_remove_bridge_port(qinq_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_bridge_port(rif_bport)
            self.client.sai_thrift_remove_router_interface(bridge_rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_12(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_12----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING]
        switch_init(self.client)

        port1 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### default bridge port of type: port, id = 0x%x ###" %bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(False == a.value.booldata)

            value = True
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            status = self.client.sai_thrift_set_bridge_port_attribute(bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.booldata))
                    assert(value == a.value.booldata)

        finally:
            self.client.sai_thrift_remove_bridge_port(bport)
            bport = sai_thrift_create_bridge_port(self.client, port1)


@group('L2')
class func_11_set_and_get_bridge_port_attribute_fn_13(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        only support SAI_BRIDGE_PORT_TYPE_PORT
        '''
        sys_logging("### -----func_11_set_and_get_bridge_port_attribute_fn_13----- ###")
        id_list = [SAI_BRIDGE_PORT_ATTR_ISOLATION_GROUP]
        switch_init(self.client)

        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### default bridge port of type: port, id = 0x%x ###" %bport)

        vlan_id1 = 10
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id1, admin_state=False)
        sys_logging("### created bridge port of type: sub port, id = 0x%x ###" %sub_bport)

        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        bridge_rif_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                           0, 0, v4_enabled, v6_enabled, mac)
        rif_bport = sai_thrift_create_bridge_rif_port(self.client, bridge_id, bridge_rif_id, admin_state=False)
        sys_logging("### created bridge port of type: 1D router, id = 0x%x ###" %rif_bport)

        vlan_id = 33
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        mac_action = SAI_PACKET_ACTION_FORWARD
        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER,
                                                     0, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT,
                                                     port3, 0, v4_enabled, v6_enabled, mac)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        tunnel_id= sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id, label_list2,
                                                             next_level_nhop_oid=next_hop)

        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id, admin_state=False)
        sys_logging("### created bridge port of type: tunnel, id = 0x%x ###" %tunnel_bport)

        svlan_id = 30
        cvlan_id = 20
        qinq_bport = sai_thrift_create_bridge_double_vlan_sub_port(self.client, port2, bridge_id,
                                                                   svlan_id, cvlan_id, admin_state=False)
        sys_logging("### created bridge port of type: double vlan sub port, id = 0x%x ###" %qinq_bport)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(rif_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(qinq_bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)

            isolation_group_oid = sai_thrift_create_isolation_group(self.client,
                                                                    type = SAI_ISOLATION_GROUP_TYPE_BRIDGE_PORT)
            value = isolation_group_oid
            attr_value = sai_thrift_attribute_value_t(oid=value)
            attr = sai_thrift_attribute_t(id=id_list[0], value=attr_value)
            status = self.client.sai_thrift_set_bridge_port_attribute(bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS == status)
            status = self.client.sai_thrift_set_bridge_port_attribute(sub_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(rif_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)
            status = self.client.sai_thrift_set_bridge_port_attribute(qinq_bport, attr)
            sys_logging("### set %s, status = 0x%x ###" %(bridge_port_attr[id_list[0]],status))
            assert(SAI_STATUS_SUCCESS != status)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == id_list[0]:
                    sys_logging("### %s = 0x%x ###" %(bridge_port_attr[id_list[0]],a.value.oid))
                    assert(value == a.value.oid)

        finally:
            sai_thrift_remove_isolation_group(self.client, isolation_group_oid)
            self.client.sai_thrift_remove_bridge_port(bport)
            sai_thrift_create_bridge_port(self.client, port1)
            self.client.sai_thrift_remove_bridge_port(qinq_bport)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2)
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_bridge_port(rif_bport)
            self.client.sai_thrift_remove_router_interface(bridge_rif_id)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport)
            self.client.sai_thrift_remove_bridge(bridge_id)


@group('L2')
class func_12_get_bridge_port_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_12_get_bridge_port_stats_fn----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport_oid1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport_oid2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        counter_ids = [SAI_BRIDGE_PORT_STAT_IN_OCTETS, SAI_BRIDGE_PORT_STAT_IN_PACKETS,
                       SAI_BRIDGE_PORT_STAT_OUT_OCTETS, SAI_BRIDGE_PORT_STAT_OUT_PACKETS]
        self.client.sai_thrift_clear_bridge_port_stats(bport_oid1, counter_ids, 4)

        list = self.client.sai_thrift_get_bridge_port_stats(bport_oid1, counter_ids, 4)
        for a in range(0, 4):
            sys_logging("### counter list[%d] = %d ###" %(a, list[a]))

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True, vlan_vid=10,
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            assert(list[0] == 0)
            assert(list[1] == 0)
            assert(list[2] == 0)
            assert(list[3] == 0)

            self.ctc_send_packet(0, pkt)
            self.ctc_verify_packet(pkt, 1)

            list = self.client.sai_thrift_get_bridge_port_stats(bport_oid1, counter_ids, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 104)
            assert(list[1] == 1)
            assert(list[2] == 0)
            assert(list[3] == 0)

            self.ctc_send_packet(1, pkt)
            self.ctc_verify_packet(pkt, 0)

            list = self.client.sai_thrift_get_bridge_port_stats(bport_oid1, counter_ids, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 104)
            assert(list[1] == 1)
            assert(list[2] == 104)
            assert(list[3] == 1)

            list = self.client.sai_thrift_get_bridge_port_stats(bport_oid1, counter_ids, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 104)
            assert(list[1] == 1)
            assert(list[2] == 104)
            assert(list[3] == 1)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)


@group('L2')
class func_13_get_bridge_port_stats_ext_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_13_get_bridge_port_stats_ext_fn_0----- ###")
        switch_init(self.client)

        mode = SAI_STATS_MODE_READ
        vlan_id1 = 10
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport_oid1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport_oid2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        counter_ids = [SAI_BRIDGE_PORT_STAT_IN_OCTETS, SAI_BRIDGE_PORT_STAT_IN_PACKETS,
                       SAI_BRIDGE_PORT_STAT_OUT_OCTETS, SAI_BRIDGE_PORT_STAT_OUT_PACKETS]
        self.client.sai_thrift_clear_bridge_port_stats(bport_oid1, counter_ids, 4)

        list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
        for a in range(0, 4):
            sys_logging("### counter list[%d]= %d ###" %(a, list[a]))

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True, vlan_vid=10,
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            assert(list[0] == 0)
            assert(list[1] == 0)
            assert(list[2] == 0)
            assert(list[3] == 0)

            self.ctc_send_packet(0, pkt)
            self.ctc_verify_packet(pkt, 1)

            list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 104)
            assert(list[1] == 1)
            assert(list[2] == 0)
            assert(list[3] == 0)

            self.ctc_send_packet(1, pkt)
            self.ctc_verify_packet(pkt, 0)

            list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 104)
            assert(list[1] == 1)
            assert(list[2] == 104)
            assert(list[3] == 1)

            list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 104)
            assert(list[1] == 1)
            assert(list[2] == 104)
            assert(list[3] == 1)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)


@group('L2')
class func_13_get_bridge_port_stats_ext_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_13_get_bridge_port_stats_ext_fn_1----- ###")
        switch_init(self.client)

        mode = SAI_STATS_MODE_READ_AND_CLEAR
        vlan_id1 = 10
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport_oid1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport_oid2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        counter_ids = [SAI_BRIDGE_PORT_STAT_IN_OCTETS, SAI_BRIDGE_PORT_STAT_IN_PACKETS,
                       SAI_BRIDGE_PORT_STAT_OUT_OCTETS, SAI_BRIDGE_PORT_STAT_OUT_PACKETS]
        self.client.sai_thrift_clear_bridge_port_stats(bport_oid1, counter_ids, 4)

        list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
        for a in range(0, 4):
            sys_logging("### counter list[%d]= %d ###" %(a, list[a]))

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True, vlan_vid=10,
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            assert(list[0] == 0)
            assert(list[1] == 0)
            assert(list[2] == 0)
            assert(list[3] == 0)

            self.ctc_send_packet(0, pkt)
            self.ctc_verify_packet(pkt, 1)

            list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 104)
            assert(list[1] == 1)
            assert(list[2] == 0)
            assert(list[3] == 0)

            self.ctc_send_packet(1, pkt)
            self.ctc_verify_packet(pkt, 0)

            list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 0)
            assert(list[1] == 0)
            assert(list[2] == 104)
            assert(list[3] == 1)

            list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 0)
            assert(list[1] == 0)
            assert(list[2] == 0)
            assert(list[3] == 0)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)


@group('L2')
class func_14_clear_bridge_port_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_14_clear_bridge_port_stats_fn----- ###")
        switch_init(self.client)

        mode = SAI_STATS_MODE_READ
        vlan_id1 = 10
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        bport_oid1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport_oid2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        counter_ids = [SAI_BRIDGE_PORT_STAT_IN_OCTETS, SAI_BRIDGE_PORT_STAT_IN_PACKETS,
                       SAI_BRIDGE_PORT_STAT_OUT_OCTETS, SAI_BRIDGE_PORT_STAT_OUT_PACKETS]
        self.client.sai_thrift_clear_bridge_port_stats(bport_oid1, counter_ids, 4)

        list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
        for a in range(0, 4):
            sys_logging("### counter list[%d] = %d ###" %(a, list[a]))

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True, vlan_vid=10,
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            assert(list[0] == 0)
            assert(list[1] == 0)
            assert(list[2] == 0)
            assert(list[3] == 0)

            self.ctc_send_packet(0, pkt)
            self.ctc_verify_packet(pkt, 1)

            list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 104)
            assert(list[1] == 1)
            assert(list[2] == 0)
            assert(list[3] == 0)

            self.client.sai_thrift_clear_bridge_port_stats(bport_oid1, counter_ids, 4)
            list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 0)
            assert(list[1] == 0)
            assert(list[2] == 0)
            assert(list[3] == 0)

            self.ctc_send_packet(1, pkt)
            self.ctc_verify_packet(pkt, 0)

            list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 0)
            assert(list[1] == 0)
            assert(list[2] == 104)
            assert(list[3] == 1)

            self.client.sai_thrift_clear_bridge_port_stats(bport_oid1, counter_ids, 4)
            list = self.client.sai_thrift_get_bridge_port_stats_ext(bport_oid1, counter_ids, mode, 4)
            for a in range(0, 4):
                sys_logging("### counter list[%d] = %d ###" %(a, list[a]))
            assert(list[0] == 0)
            assert(list[1] == 0)
            assert(list[2] == 0)
            assert(list[3] == 0)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid1)


@group('L2')
class scenario_01_sub_port_to_sub_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_01_sub_port_to_sub_port----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        port4 = port_list[4]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        mode1 = SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED
        mode2 = SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1, tagging_mode=mode1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id1, tagging_mode=mode1)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id1, vlan_id2, tagging_mode=mode1)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id1, vlan_id2, tagging_mode=mode2)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64,
                                 pktlen=104)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64,
                                 pktlen=104)
        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64,
                                 pktlen=100)
        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:01', eth_src='00:00:00:00:00:02',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64,
                                 pktlen=104)
        pkt5 = simple_tcp_packet(eth_dst='00:00:00:00:00:01', eth_src='00:00:00:00:00:02',
                                dl_vlan_enable=True, vlan_vid=20,
                                ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_packet(pkt1, 2)
            self.ctc_verify_packet(pkt2, 3)
            self.ctc_verify_packet(pkt3, 4)

            self.ctc_send_packet(2, pkt4)
            self.ctc_verify_packet(pkt4, 1)
            self.ctc_verify_no_packet(pkt4, 3)
            self.ctc_verify_no_packet(pkt4, 4)

        finally:
            sai_thrift_flush_fdb(self.client, bv_id=bridge_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)
            self.client.sai_thrift_remove_bridge(bridge_id1)


@group('L2')
class scenario_02_sub_port_to_1d_router(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_02_sub_port_to_1d_router----- ###")
        switch_init(self.client)

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        v4_enabled = 1
        v6_enabled = 1
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        port1 = port_list[1]
        port2 = port_list[2]
        vlan1 = 10
        vlan2 = 20
        sub_bport1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan1)
        sub_bport2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan2)

        router_mac = '00:11:22:33:44:55'
        bridge_rif1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                         0, 0, v4_enabled, v6_enabled, router_mac,
                                                         dot1d_bridge_id=bridge_id1)
        bridge_rif2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_BRIDGE,
                                                         0, 0, v4_enabled, v6_enabled, router_mac,
                                                         dot1d_bridge_id=bridge_id2)

        rif_bport1 = sai_thrift_create_bridge_rif_port(self.client, bridge_id1, bridge_rif1)
        rif_bport2 = sai_thrift_create_bridge_rif_port(self.client, bridge_id2, bridge_rif2)

        ip1 = '11.11.11.11'
        ip2 = '22.22.22.22'
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        sai_thrift_create_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV4, bridge_rif1, ip1, mac1)
        sai_thrift_create_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV4, bridge_rif2, ip2, mac2)

        ip_addr_subnet1 = '11.11.11.0'
        ip_addr_subnet2 = '22.22.22.0'
        ip_mask = '255.255.255.0'
        sai_thrift_create_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet1, ip_mask, bridge_rif1)
        sai_thrift_create_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet2, ip_mask, bridge_rif2)

        sai_thrift_create_fdb_bport(self.client, bridge_id1, mac1, sub_bport1)
        sai_thrift_create_fdb_bport(self.client, bridge_id2, mac2, sub_bport2)

        pkt1 = simple_tcp_packet(eth_src=mac1, eth_dst=router_mac,
                                 dl_vlan_enable=True, vlan_vid=vlan1,
                                 ip_src=ip1, ip_dst=ip2,
                                 ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_src=router_mac, eth_dst=mac2,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_src=ip1, ip_dst=ip2,
                                 ip_id=101, ip_ttl=63)
        pkt3 = simple_tcp_packet(eth_src=mac2, eth_dst=mac3,
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_src=ip2, ip_dst='22.22.22.11',
                                 ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_packet(pkt2, 2)

            sai_thrift_delete_fdb(self.client, bridge_id1, mac1)
            sai_thrift_delete_fdb(self.client, bridge_id2, mac2)

            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_no_packet(pkt2, 2)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            sai_thrift_remove_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet1, ip_mask, bridge_rif1)
            sai_thrift_remove_route(self.client, vr_id, SAI_IP_ADDR_FAMILY_IPV4, ip_addr_subnet2, ip_mask, bridge_rif2)
            sai_thrift_remove_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV4, bridge_rif1, ip1, mac1)
            sai_thrift_remove_neighbor(self.client, SAI_IP_ADDR_FAMILY_IPV4, bridge_rif2, ip2, mac2)
            self.client.sai_thrift_remove_bridge_port(rif_bport1)
            self.client.sai_thrift_remove_bridge_port(rif_bport2)
            self.client.sai_thrift_remove_router_interface(bridge_rif1)
            self.client.sai_thrift_remove_router_interface(bridge_rif2)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport1)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport2)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

'''
@group('L2')
class scenario_03_sub_port_to_tunnel(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        VXLAN is not supported at this time, TBD
        """
        sys_logging("### -----scenario_02_sub_port_to_tunnel----- ###")
        switch_init(self.client)

        port0 = port_list[0]
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]

        v4_enabled = 1
        v6_enabled = 1

        mac=router_mac
        inner_mac_da = '00:00:AA:AA:00:00'
        inner_mac_sa = '00:00:AA:AA:11:11'

        tunnel_map_decap_type = SAI_TUNNEL_MAP_TYPE_VNI_TO_BRIDGE_IF
        tunnel_map_encap_type = SAI_TUNNEL_MAP_TYPE_BRIDGE_IF_TO_VNI

        vlan_id = 20
        vni_id = 1000

        addr_family = SAI_IP_ADDR_FAMILY_IPV4

        ip_mask = '255.255.255.0'
        ip_outer_addr_sa = '30.30.30.30'
        ip_outer_addr_da = '40.40.40.40'
        ip_encap_addr_da = '192.168.1.2'
        ip_decap_addr_da = '192.168.1.1'

        mac_action = SAI_PACKET_ACTION_FORWARD

        vr_id = sai_thrift_get_default_router_id(self.client)

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        bport1_id = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan_id)

        rif_lp_inner_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_LOOPBACK, port1, 0, v4_enabled, v6_enabled, mac)

        tunnel_map_decap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_decap_type)
        tunnel_map_encap_id = sai_thrift_create_tunnel_map(self.client, tunnel_map_encap_type)

        tunnel_map_entry_decap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_decap_type, tunnel_map_decap_id, vni_id, bridge_id)
        tunnel_map_entry_encap_id = sai_thrift_create_tunnel_map_entry(self.client, tunnel_map_encap_type, tunnel_map_encap_id, bridge_id, vni_id)

        encap_mapper_list=[tunnel_map_encap_id, tunnel_map_decap_id]
        decap_mapper_list=[tunnel_map_decap_id, tunnel_map_encap_id]

        tunnel_id = sai_thrift_create_tunnel_vxlan(self.client, ip_addr=ip_outer_addr_sa, encap_mapper_list=encap_mapper_list, decap_mapper_list=decap_mapper_list, underlay_if=rif_lp_inner_id)

        tunnel_term_table_entry_id = sai_thrift_create_tunnel_term_table_entry(self.client, vr_id, ip_outer_addr_da, ip_outer_addr_sa, tunnel_id, tunnel_type=SAI_TUNNEL_TYPE_VXLAN)

        tunnel_nexthop_id = sai_thrift_create_tunnel_nhop(self.client, SAI_IP_ADDR_FAMILY_IPV4, ip_outer_addr_da, tunnel_id);

        btunnel_id = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id, bridge_id)

        sai_thrift_create_fdb_tunnel(self.client, bridge_id, inner_mac_da, btunnel_id, mac_action, ip_outer_addr_da)

        rif_encap_id = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        encap_mac_da = '00:0e:00:0e:00:0e'

        sai_thrift_create_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)

        sai_thrift_create_fdb_bport(self.client, bridge_id, inner_mac_sa, bport1_id, mac_action)

        pkt1 = simple_tcp_packet(pktlen=100,
                                eth_dst=inner_mac_da,
                                eth_src=inner_mac_sa,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)

        exp_pkt1 = simple_vxlan_packet(pktlen=300,
                        eth_dst=encap_mac_da,
                        eth_src=router_mac,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_sa,
                        ip_dst=ip_outer_addr_da,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=63,
                        ip_id=0x0000,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = pkt1)

        m1_exp_pkt1=Mask(exp_pkt1)
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'chksum')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.IP,'id')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'chksum')
        m1_exp_pkt1.set_do_not_care_scapy(ptf.packet.UDP,'sport')
        inner_pkt2 = simple_tcp_packet(pktlen=100,
                                eth_dst=inner_mac_sa,
                                eth_src=inner_mac_da,
                                dl_vlan_enable=True,
                                vlan_vid=vlan_id,
                                vlan_pcp=0,
                                dl_vlan_cfi=0,
                                ip_dst=ip_encap_addr_da,
                                ip_src=ip_decap_addr_da,
                                ip_id=105,
                                ip_ttl=64,
                                ip_ihl=5)
        pkt2 = simple_vxlan_packet(pktlen=300,
                        eth_dst=router_mac,
                        eth_src=encap_mac_da,
                        dl_vlan_enable=False,
                        vlan_vid=0,
                        vlan_pcp=0,
                        dl_vlan_cfi=0,
                        ip_src=ip_outer_addr_da,
                        ip_dst=ip_outer_addr_sa,
                        ip_tos=0,
                        ip_ecn=None,
                        ip_dscp=None,
                        ip_ttl=63,
                        ip_id=0x0000,
                        ip_flags=0x0,
                        udp_sport=49180,
                        udp_dport=4789,
                        with_udp_chksum=False,
                        ip_ihl=None,
                        ip_options=False,
                        vxlan_reserved1=0x000000,
                        vxlan_vni = vni_id,
                        vxlan_reserved2=0x00,
                        inner_frame = inner_pkt2)

        warmboot(self.client)

        try:
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( m1_exp_pkt1, 2)
            self.ctc_send_packet( 2, str(pkt2))
            self.ctc_verify_packet( inner_pkt2, 1)

        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id)
            sai_thrift_delete_fdb(self.client, bridge_id, inner_mac_sa, port1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_encap_id, ip_outer_addr_da, encap_mac_da)
            self.client.sai_thrift_remove_router_interface(rif_lp_inner_id)
            self.client.sai_thrift_remove_router_interface(rif_encap_id)
            sai_thrift_delete_fdb(self.client, bridge_id, inner_mac_da, tunnel_id)
            self.client.sai_thrift_remove_bridge_port(btunnel_id)
            self.client.sai_thrift_remove_next_hop(tunnel_nexthop_id)
            self.client.sai_thrift_remove_tunnel_term_table_entry(tunnel_term_table_entry_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_decap_id);
            self.client.sai_thrift_remove_tunnel_map_entry(tunnel_map_entry_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_encap_id);
            self.client.sai_thrift_remove_tunnel_map(tunnel_map_decap_id);
            self.client.sai_thrift_remove_bridge_port(bport1_id)
            self.client.sai_thrift_remove_bridge(bridge_id)
'''

@group('L2')
class scenario_04_bridge_max_learned_addresses(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_04_bridge_max_learned_addresses----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id1)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:04', eth_src='00:00:00:00:00:03',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:04', eth_src='00:00:00:00:00:03',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt2), [1], 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets(str(pkt4), [1], 1)

            time.sleep(1)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))

            sai_thrift_flush_fdb(self.client, bv_id=bridge_id1)
            time.sleep(1)
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))

            value = 1
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt2), [1], 1)
            time.sleep(1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets(str(pkt4), [1], 1)

            time.sleep(1)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)


@group('L2')
class scenario_05_bridge_learn_disable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_05_bridge_learn_disable----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id1)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:04', eth_src='00:00:00:00:00:03',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:04', eth_src='00:00:00:00:00:03',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt2), [1], 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets(str(pkt4), [1], 1)

            time.sleep(1)
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))

            sai_thrift_flush_fdb(self.client, bv_id=bridge_id1)
            time.sleep(1)
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))

            value = 1
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            time.sleep(1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt4), [1], 1)

            time.sleep(1)
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, bridge_id1, mac2))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)


@group('L2')
class scenario_06_bridge_unknown_unicast_flood_control(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_06_bridge_unknown_unicast_flood_control----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id1)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:04', eth_src='00:00:00:00:00:03',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:04', eth_src='00:00:00:00:00:03',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt4), [1], 1)

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_no_packet(str(pkt4), 1)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)


@group('L2')
class scenario_07_bridge_unknown_multicast_flood_control(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_07_bridge_unknown_unicast_flood_control----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id1)

        pkt1 = simple_tcp_packet(eth_dst='01:00:5e:01:01:01', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='01:00:5e:01:01:01', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst='01:00:5e:01:01:01', eth_src='00:00:00:00:00:03',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst='01:00:5e:01:01:01', eth_src='00:00:00:00:00:03',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt4), [1], 1)

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_no_packet(str(pkt4), 1)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)


@group('L2')
class scenario_08_bridge_broadcast_flood_control(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_08_bridge_broadcast_flood_control----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id2, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id2, vlan_id1)

        pkt1 = simple_tcp_packet(eth_dst='ff:ff:ff:ff:ff:ff', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='ff:ff:ff:ff:ff:ff', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst='ff:ff:ff:ff:ff:ff', eth_src='00:00:00:00:00:03',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst='ff:ff:ff:ff:ff:ff', eth_src='00:00:00:00:00:03',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1], 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt4), [1], 1)

            value = SAI_BRIDGE_FLOOD_CONTROL_TYPE_NONE
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_bridge_attribute(bridge_id1, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_no_packet(str(pkt4), 1)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)


@group('L2')
class scenario_09_bridge_port_change_bridge_id(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_09_bridge_port_change_bridge_id----- ###")
        switch_init(self.client)

        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]

        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        bridge_id2 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id2, vlan_id3)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=vlan_id1,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=vlan_id2,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=vlan_id3,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_packet(pkt2, 2)
            self.ctc_verify_no_packet(pkt3, 3)

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id1, attr)

            sai_thrift_flush_fdb_by_bridge_port(self.client, sub_port_id1)

            attr_value = sai_thrift_attribute_value_t(oid=bridge_id2)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_BRIDGE_ID, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id1, attr)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE,value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id1, attr)

            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_no_packet(pkt2, 2)
            self.ctc_verify_packet(pkt3, 3)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            self.client.sai_thrift_remove_bridge(bridge_id2)


@group('L2')
class scenario_10_bridge_port_learning_limit_and_violation(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        only support TRANSMIT, DENY, TRAP, FORWARD(== TRASMIT), DROP(== DENY)
        '''
        sys_logging("### -----scenario_10_bridge_port_learning_limit_and_violation----- ###")
        switch_init(self.client)
        self.client.sai_thrift_clear_cpu_packet_info()

        port1 = port_list[0]
        port2 = port_list[1]
        bport_oid1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        pkt1 = simple_tcp_packet(eth_dst=mac3, eth_src=mac1,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac3, eth_src=mac2,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2))

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt1), [1], 1)
            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_packets(str(pkt2), [1], 1)

            assert(1 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2))

            sai_thrift_flush_fdb(self.client, bv_id=vlan_oid)

            attr_value = sai_thrift_attribute_value_t(u32=1)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)

            #default packet action is DROP
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
            time.sleep(1)
            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_no_packet(str(pkt2), 1)

            assert(1 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2))
            assert(0 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            value = SAI_PACKET_ACTION_FORWARD
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION,
                                          value=sai_thrift_attribute_value_t(s32=value))
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt1), [1], 1)
            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_packet(pkt2, 1)

            assert(1 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2))
            assert(0 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            value = SAI_PACKET_ACTION_TRAP
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION,
                                          value=sai_thrift_attribute_value_t(s32=value))
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt1), [1], 1)
            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_no_packet(str(pkt2), 1)

            assert(1 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2))
            assert(1 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION,
                                          value=sai_thrift_attribute_value_t(s32=SAI_PACKET_ACTION_DROP))
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)
            attr_value = sai_thrift_attribute_value_t(u32=0)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class scenario_11_bridge_port_change_admin_state(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        admin state of SAI_BRIDGE_PORT_TYPE_PORT cannot be set to false actually
        '''
        sys_logging("### -----scenario_11_bridge_port_change_admin_state----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        bport1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
        bport2 = sai_thrift_get_bridge_port_by_port(self.client, port2)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(str(pkt), [1], 1)

            #admin state is true actually
            value = False
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport1, attr)
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_ADMIN_STATE:
                    sys_logging("### %s = %d ###" %(bridge_port_attr[SAI_BRIDGE_PORT_ATTR_ADMIN_STATE],a.value.booldata))
                    assert(False == a.value.booldata)

            self.ctc_send_packet(0, str(pkt))
            #self.ctc_verify_no_packet(pkt, 1)
            self.ctc_verify_packets(str(pkt), [1], 1)

            '''
            value = True
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport1, attr)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(str(pkt), [1], 1)

            value = False
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, attr)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 1)

            value = True
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport2, attr)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(str(pkt), [1], 1)
            '''

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class scenario_12_bridge_port_ingress_filtering(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_12_bridge_port_ingress_filtering----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        vlan1 = 100
        vlan2 = 200
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan2)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        vlan3 = 300
        vlan4 = 400
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)
        sub_bport1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id, vlan3)
        sub_bport2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan3)

        attr_value = sai_thrift_attribute_value_t(u16=vlan1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1',
                                 dl_vlan_enable=True, vlan_vid=vlan2,
                                 ip_id=101, ip_ttl=64, pktlen=104)
        pkt2 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1',
                                 ip_id=101, ip_ttl=64, pktlen=100)
        pkt3 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1',
                                 dl_vlan_enable=True, vlan_vid=vlan3,
                                 ip_id=101, ip_ttl=64, pktlen=104)
                                 

        warmboot(self.client)

        try:
            bport_oid1 = sai_thrift_get_bridge_port_by_port(self.client, port1)
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING:
                    sys_logging("### SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING = %d ###" %a.value.booldata)
                    assert(False == a.value.booldata)

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt2, 1)
            self.ctc_send_packet(0, pkt3)
            self.ctc_verify_packet(pkt3, 1)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)

            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt2, 1)
            self.ctc_send_packet(0, pkt3)
            self.ctc_verify_no_packet(pkt3, 1)

        finally:
            #pdb.set_trace()
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport1)
            sai_thrift_remove_bridge_sub_port_2(self.client, sub_bport2)
            self.client.sai_thrift_remove_bridge(bridge_id)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_bridge_port(bport_oid1)
            sai_thrift_create_bridge_port(self.client, port1)


@group('L2')
class scenario_13_bridge_port_egress_filtering(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_13_bridge_port_egress_filtering----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        vlan_id1 = 100
        vlan_id2 = 200
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac_action = SAI_PACKET_ACTION_FORWARD

        pkt1 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1',
                                 dl_vlan_enable=True, vlan_vid=vlan_id2,
                                 ip_id=101, ip_ttl=64, pktlen=104)
        pkt2 = simple_tcp_packet(eth_dst=mac2, eth_src=mac1,
                                 ip_dst='10.0.0.1',
                                 dl_vlan_enable=True, vlan_vid=vlan_id2,
                                 ip_id=101, ip_ttl=64, pktlen=104)

        warmboot(self.client)

        try:
            bport_oid1 = sai_thrift_get_bridge_port_by_port(self.client, port2)
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING:
                    sys_logging("### SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING = %d ###" %a.value.booldata)
                    assert(False == a.value.booldata)

            sai_thrift_create_fdb(self.client, vlan_oid2, mac2, port2, mac_action)
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt2), [1], 1)

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid1, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(str(pkt2), 1)

        finally:
            sai_thrift_flush_fdb(self.client, type=SAI_FDB_FLUSH_ENTRY_TYPE_ALL)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_bridge_port(bport_oid1)
            sai_thrift_create_bridge_port(self.client, port2)


@group('L2')
class scenario_14_bridge_port_is_lag(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_14_bridge_port_is_lag----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        lag_oid = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        is_lag = 1
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_bridge_oid,
                                                     SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_oid, attr)

        value = 1
        attr_value = sai_thrift_attribute_value_t(u32=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)

        value = SAI_PACKET_ACTION_DROP
        attr_value = sai_thrift_attribute_value_t(s32=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        mac4 = '00:33:33:33:33:34'
        mac_action = SAI_PACKET_ACTION_FORWARD
        pkt = simple_tcp_packet(eth_dst=mac1, eth_src=mac2,
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac1, eth_src=mac3,
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac1, eth_src=mac4,
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            self.ctc_verify_packets( str(pkt), [2], 1)

            sys_logging("### exceed mac learning limit num, so discard this packet ###")
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(str(pkt1), 1)
            self.ctc_verify_no_packet(str(pkt1), 2)

            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_verify_no_packet(str(pkt2), 2)

        finally:
            flush_all_fdb(self.client)
            value = 0
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
            value = SAI_PACKET_ACTION_DROP
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_oid, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag(self.client, lag_oid)


@group('L2')
class scenario_15_bridge_port_change_lag_member(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_15_bridge_port_change_lag_member----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac3 = '00:33:33:33:33:33'
        mac4 = '00:33:33:33:33:34'
        mac5 = '00:33:33:33:33:35'
        mac_action = SAI_PACKET_ACTION_FORWARD

        lag_oid = sai_thrift_create_lag(self.client)
        sai_thrift_vlan_remove_ports(self.client, switch.default_vlan.oid, [port1,port2,port3])
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        is_lag = 1
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_bridge_oid, SAI_VLAN_TAGGING_MODE_UNTAGGED,is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_oid, attr)

        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port3)

        value = 1
        attr_value = sai_thrift_attribute_value_t(booldata=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)

        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)

        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)

        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)

        value = 2
        attr_value = sai_thrift_attribute_value_t(u32=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)

        value = SAI_PACKET_ACTION_DROP
        attr_value = sai_thrift_attribute_value_t(s32=value)
        attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, value=attr_value)
        self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)

        pkt = simple_tcp_packet(eth_dst=mac1, eth_src=mac2,
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt1 = simple_tcp_packet(eth_dst=mac1, eth_src=mac3,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst=mac1, eth_src=mac4,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst=mac1, eth_src=mac5,
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)
            self.ctc_verify_packets( str(pkt), [2], 1)
            self.ctc_verify_no_packet(str(pkt), 3)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(str(pkt1), 0)
            self.ctc_verify_packets( str(pkt1), [2], 1)
            self.ctc_verify_no_packet(str(pkt1), 3)

            self.ctc_send_packet(3, str(pkt2))
            self.ctc_verify_no_packet(str(pkt2), 0)
            self.ctc_verify_no_packet(str(pkt2), 1)
            self.ctc_verify_no_packet(str(pkt2), 2)

            sys_logging("### add lag member ###")
            lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_oid, port4)

            sys_logging("### exceed mac learning limit num, so discard this packet ###")
            self.ctc_send_packet(3, str(pkt3))
            self.ctc_verify_no_packet(str(pkt3), 0)
            self.ctc_verify_no_packet(str(pkt3), 1)
            self.ctc_verify_no_packet(str(pkt3), 2)

            flush_all_fdb(self.client)

            self.ctc_send_packet(3, str(pkt3))
            self.ctc_verify_no_packet(str(pkt3), 0)
            self.ctc_verify_no_packet(str(pkt3), 1)
            self.ctc_verify_packets( str(pkt3), [2], 1)

            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac5)
            assert(1 == result)

            sys_logging("### remove lag member ###")
            sai_thrift_remove_lag_member(self.client, lag_member_id1)

            flush_all_fdb(self.client)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [2], 1) 

            port0_pkt_cnt = 0
            port1_pkt_cnt = 0
            rcv_idx = self.ctc_verify_any_packet_any_port( [pkt1], [1, 3])
            if rcv_idx == 1:
                port0_pkt_cnt = 1
            elif rcv_idx == 3:
                port1_pkt_cnt = 1
            sys_logging("### port 0 receive packet conut is %d ###" %port0_pkt_cnt)
            sys_logging("### port 1 receive packet conut is %d ###" %port1_pkt_cnt)

            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_packets( str(pkt2), [2], 1)

            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets( str(pkt3), [2], 1)
            
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac3)
            assert(1 == result)
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac4)
            assert(1 == result)
            result = sai_thrift_check_fdb_exist(self.client,vlan_oid, mac5)
            assert(1 == result)

        finally:
            flush_all_fdb(self.client)

            value = 0
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)

            value = SAI_PACKET_ACTION_DROP
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_FDB_LEARNING_LIMIT_VIOLATION_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(lag_bridge_oid, attr)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port3, attr)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_oid, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)

            sai_thrift_remove_lag(self.client, lag_oid)

            vlan_memberb = sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            vlan_memberb = sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            vlan_memberb = sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)

            bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port2)
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)

            bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port3)
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)

            bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port4)
            value = 0
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_INGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_EGRESS_FILTERING, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport_oid, attr)

'''
class scenario_16_sub_port_change_tagging_mode(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        
        switch_init(self.client)
        vlan_id1 = 10
        vlan_id2 = 20        
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]        
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'
        
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    
        
        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, port1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id1, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, port3, bridge_id1, vlan_id1)
        sub_port_id4 = sai_thrift_create_bridge_sub_port(self.client, port4, bridge_id1, vlan_id2)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:02',
                                eth_src='00:00:00:00:00:01',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                ip_ttl=64)
                                
        
        warmboot(self.client)
        try:

            attrs = self.client.sai_thrift_get_bridge_port_attribute(sub_port_id2)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_TAGGING_MODE:
                    sys_logging("###SAI_BRIDGE_PORT_ATTR_TAGGING_MODE = %d ###" %a.value.s32)
                    assert( SAI_BRIDGE_PORT_TAGGING_MODE_TAGGED == a.value.s32)    
            
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt2), [1,3], 1)
            self.ctc_verify_packets( str(pkt1), [2], 1)  

            # do not support update tag mode for sub port
            value = SAI_BRIDGE_PORT_TAGGING_MODE_UNTAGGED
            attr_value = sai_thrift_attribute_value_t(s32=value)
            attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_TAGGING_MODE, value=attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(sub_port_id2, attr)
  
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt3), [1], 1)
            self.ctc_verify_packets( str(pkt1), [2], 1) 
            self.ctc_verify_packets( str(pkt2), [3], 1)
                     
        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge_port(sub_port_id4)                     
            self.client.sai_thrift_remove_bridge(bridge_id1)       
'''


