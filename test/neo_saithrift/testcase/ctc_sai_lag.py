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
Thrift SAI interface LAG tests
"""
import socket
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask


lag_attr = ['SAI_LAG_ATTR_PORT_LIST',
            'SAI_LAG_ATTR_INGRESS_ACL', 'SAI_LAG_ATTR_EGRESS_ACL',
            'SAI_LAG_ATTR_PORT_VLAN_ID', 'SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY',
            'SAI_LAG_ATTR_DROP_UNTAGGED', 'SAI_LAG_ATTR_DROP_TAGGED',
            'SAI_LAG_ATTR_TPID', 'SAI_LAG_ATTR_SYSTEM_PORT_AGGREGATE_ID',
            'SAI_LAG_ATTR_MODE', 'SAI_LAG_ATTR_CUSTOM_MAX_MEMBER_NUM']

def _set_lag_attr(client, lag_id,
                  ingress_acl=None, egress_acl=None, port_vlan_id=None, default_vlan_priority=None,
                  drop_untagged=None, drop_tagged=None, tpid=None):
    '''
    only one attribute can be set at the same time
    '''
    if ingress_acl is not None:
        attr_value = sai_thrift_attribute_value_t(oid=ingress_acl)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_INGRESS_ACL, value=attr_value)
        status = client.sai_thrift_set_lag_attribute(lag_id=lag_id, thrift_attr=attr)
        sys_logging("### set %s to 0x%x, status = 0x%x ###" %(lag_attr[1], ingress_acl, status))
        return status

    if egress_acl is not None:
        attr_value = sai_thrift_attribute_value_t(oid=egress_acl)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_EGRESS_ACL, value=attr_value)
        status = client.sai_thrift_set_lag_attribute(lag_id=lag_id, thrift_attr=attr)
        sys_logging("### set %s to 0x%x, status = 0x%x ###" %(lag_attr[2], egress_acl, status))
        return status

    if port_vlan_id is not None:
        attr_value = sai_thrift_attribute_value_t(u16=port_vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        status = client.sai_thrift_set_lag_attribute(lag_id=lag_id, thrift_attr=attr)
        sys_logging("### set %s to %d, status = 0x%x ###" %(lag_attr[3], port_vlan_id, status))
        return status

    if default_vlan_priority is not None:
        attr_value = sai_thrift_attribute_value_t(u8=default_vlan_priority)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY, value=attr_value)
        status = client.sai_thrift_set_lag_attribute(lag_id=lag_id, thrift_attr=attr)
        sys_logging("### set %s to %d, status = 0x%x ###" %(lag_attr[4], default_vlan_priority, status))
        return status

    if drop_untagged is not None:
        attr_value = sai_thrift_attribute_value_t(booldata=drop_untagged)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_DROP_UNTAGGED, value=attr_value)
        status = client.sai_thrift_set_lag_attribute(lag_id=lag_id, thrift_attr=attr)
        sys_logging("### set %s to %s, status = 0x%x ###" %(lag_attr[5], drop_untagged, status))
        return status

    if drop_tagged is not None:
        attr_value = sai_thrift_attribute_value_t(booldata=drop_tagged)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_DROP_TAGGED, value=attr_value)
        status = client.sai_thrift_set_lag_attribute(lag_id=lag_id, thrift_attr=attr)
        sys_logging("### set %s to %s, status = 0x%x ###" %(lag_attr[6], drop_tagged, status))
        return status

    if tpid is not None:
        attr_value = sai_thrift_attribute_value_t(u16=tpid)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_TPID, value=attr_value)
        status = client.sai_thrift_set_lag_attribute(lag_id=lag_id, thrift_attr=attr)
        sys_logging("### set %s to %d, status = 0x%x ###" %(lag_attr[7], tpid, status))
        return status

def _get_lag_attr(client, lag_id, port_list=False, ingress_acl=False, egress_acl=False,
                  port_vlan_id=False, default_vlan_priority=False, drop_untagged=False, drop_tagged=False,
                  tpid=False, system_port_aggregate_id=False, mode=False, max_member_num=False):
    lag_attr_list = client.sai_thrift_get_lag_attribute(lag_id=lag_id)
    if (SAI_STATUS_SUCCESS != lag_attr_list.status):
        return None

    return_list = []
    attr_count = 0
    if port_list is True:
        attr_count += 1
    if ingress_acl is True:
        attr_count += 1
    if egress_acl is True:
        attr_count += 1
    if port_vlan_id is True:
        attr_count += 1
    if default_vlan_priority is True:
        attr_count += 1
    if drop_untagged is True:
        attr_count += 1
    if drop_tagged is True:
        attr_count += 1
    if tpid is True:
        attr_count += 1
    if system_port_aggregate_id is True:
        attr_count += 1
    if mode is True:
        attr_count += 1
    if max_member_num is True:
        attr_count += 1

    if port_list is True:
        for attr in lag_attr_list.attr_list:
            if attr.id == SAI_LAG_ATTR_PORT_LIST:
                sys_logging("### count of %s = %d ###" %(lag_attr[0], attr.value.objlist.count))
                for port in attr.value.objlist.object_id_list:
                    print ("### list of %s = ", attr.value.objlist.object_id_list, " ###" %lag_attr[0])
                if 1 == attr_count:
                    return attr.value.objlist
                else:
                    return_list.append(attr.value.objlist)

    if ingress_acl is True:
        for attr in lag_attr_list.attr_list:
            if attr.id == SAI_LAG_ATTR_INGRESS_ACL:
                sys_logging("### %s = 0x%x ###" %(lag_attr[1], attr.value.oid))
                if 1 == attr_count:
                    return attr.value.oid
                else:
                    return_list.append(attr.value.oid)

    if egress_acl is True:
        for attr in lag_attr_list.attr_list:
            if attr.id == SAI_LAG_ATTR_EGRESS_ACL:
                sys_logging("### %s = 0x%x ###" %(lag_attr[2], attr.value.oid))
                if 1 == attr_count:
                    return attr.value.oid
                else:
                    return_list.append(attr.value.oid)

    if port_vlan_id is True:
        for attr in lag_attr_list.attr_list:
            if attr.id == SAI_LAG_ATTR_PORT_VLAN_ID:
                sys_logging("### %s = %d ###" %(lag_attr[3], attr.value.u16))
                if 1 == attr_count:
                    return attr.value.u16
                else:
                    return_list.append(attr.value.u16)

    if default_vlan_priority is True:
        for attr in lag_attr_list.attr_list:
            if attr.id == SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY:
                sys_logging("### %s = %d ###" %(lag_attr[4], attr.value.u8))
                if 1 == attr_count:
                    return attr.value.u8
                else:
                    return_list.append(attr.value.u8)

    if drop_untagged is True:
        for attr in lag_attr_list.attr_list:
            if attr.id == SAI_LAG_ATTR_DROP_UNTAGGED:
                sys_logging("### %s = %s ###" %(lag_attr[5], attr.value.booldata))
                if 1 == attr_count:
                    return attr.value.booldata
                else:
                    return_list.append(attr.value.booldata)

    if drop_tagged is True:
        for attr in lag_attr_list.attr_list:
            if attr.id == SAI_LAG_ATTR_DROP_TAGGED:
                sys_logging("### %s = %s ###" %(lag_attr[6], attr.value.booldata))
                if 1 == attr_count:
                    return attr.value.booldata
                else:
                    return_list.append(attr.value.booldata)

    if mode is True:
        for attr in lag_attr_list.attr_list:
            if attr.id == SAI_LAG_ATTR_MODE:
                sys_logging("### %s = %s ###" %(lag_attr[9], attr.value.s32))
                if 1 == attr_count:
                    return attr.value.s32
                else:
                    return_list.append(attr.value.s32)

    if max_member_num is True:
        for attr in lag_attr_list.attr_list:
            if attr.id == SAI_LAG_ATTR_CUSTOM_MAX_MEMBER_NUM:
                sys_logging("### %s = %d ###" %(lag_attr[10], attr.value.u16))
                if 1 == attr_count:
                    return attr.value.u16
                else:
                    return_list.append(attr.value.u16)

    return return_list


lag_member_attr = ['SAI_LAG_MEMBER_ATTR_LAG_ID', 'SAI_LAG_MEMBER_ATTR_PORT_ID',
                   'SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE', 'SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE']

def _set_lag_member_attr(client, lag_member_id, egress_disable=None, ingress_disable=None):
    '''
    only one attribute can be set at the same time
    '''
    if egress_disable is not None:
        attr_value = sai_thrift_attribute_value_t(booldata=egress_disable)
        attr = sai_thrift_attribute_t(id=SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE, value=attr_value)
        status = client.sai_thrift_set_lag_member_attribute(lag_member_id, thrift_attr=attr)
        sys_logging("### set %s to %s, status = 0x%x ###" %(lag_member_attr[2], egress_disable, status))
        return status

    if ingress_disable is not None:
        attr_value = sai_thrift_attribute_value_t(booldata=ingress_disable)
        attr = sai_thrift_attribute_t(id=SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE, value=attr_value)
        status = client.sai_thrift_set_lag_member_attribute(lag_member_id, thrift_attr=attr)
        sys_logging("### set %s to %s, status = 0x%x ###" %(lag_member_attr[3], ingress_disable, status))
        return status

def _get_lag_member_attr(client, lag_member_id, lag_id=False, port_id=False, egress_disable=False, ingress_disable=False):
    lag_member_attr_list = client.sai_thrift_get_lag_member_attribute(lag_member_id)
    if (SAI_STATUS_SUCCESS != lag_member_attr_list.status):
        return None

    return_list = []
    attr_count = 0
    if lag_id is True:
        attr_count += 1
    if port_id is True:
        attr_count += 1
    if egress_disable is True:
        attr_count += 1
    if ingress_disable is True:
        attr_count += 1

    if lag_id is True:
        for attr in lag_member_attr_list.attr_list:
            if attr.id == SAI_LAG_MEMBER_ATTR_LAG_ID:
                sys_logging("### %s = 0x%x ###" %(lag_member_attr[0], attr.value.oid))
                if 1 == attr_count:
                    return attr.value.oid
                else:
                    return_list.append(attr.value.oid)

    if port_id is True:
        for attr in lag_member_attr_list.attr_list:
            if attr.id == SAI_LAG_MEMBER_ATTR_PORT_ID:
                sys_logging("### %s = 0x%x ###" %(lag_member_attr[1], attr.value.oid))
                if 1 == attr_count:
                    return attr.value.oid
                else:
                    return_list.append(attr.value.oid)

    if egress_disable is True:
        for attr in lag_member_attr_list.attr_list:
            if attr.id == SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE:
                sys_logging("### %s = %s ###" %(lag_member_attr[2], attr.value.booldata))
                if 1 == attr_count:
                    return attr.value.booldata
                else:
                    return_list.append(attr.value.booldata)

    if ingress_disable is True:
        for attr in lag_member_attr_list.attr_list:
            if attr.id == SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE:
                sys_logging("### %s = %s ###" %(lag_member_attr[3], attr.value.booldata))
                if 1 == attr_count:
                    return attr.value.booldata
                else:
                    return_list.append(attr.value.booldata)

    return return_list


class fun_01_create_5_mode_lag_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        lag_mode0 = SAI_LAG_MODE_STATIC
        lag_mode1 = SAI_LAG_MODE_STATIC_FAILOVER
        lag_mode2 = SAI_LAG_MODE_RR
        lag_mode3 = SAI_LAG_MODE_DLB
        lag_mode4 = SAI_LAG_MODE_RH
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_id2 = sai_thrift_create_lag(self.client, lag_mode=lag_mode1)
        lag_id3 = sai_thrift_create_lag(self.client, lag_mode=lag_mode2)
        lag_id4 = sai_thrift_create_lag(self.client, lag_mode=lag_mode3)
        lag_id5 = sai_thrift_create_lag(self.client, lag_mode=lag_mode4)

        try:
            sys_logging("lag1 oid = 0x%x" %lag_id1)
            assert(lag_mode0 == _get_lag_attr(self.client, lag_id1, mode=True))

            sys_logging("lag2 oid = 0x%x" %lag_id2)
            assert(lag_mode1 == _get_lag_attr(self.client, lag_id2, mode=True))

            sys_logging("lag3 oid = 0x%x" %lag_id3)
            assert(lag_mode2 == _get_lag_attr(self.client, lag_id3, mode=True))

            sys_logging("lag4 oid = 0x%x" %lag_id4)
            assert(lag_mode3 == _get_lag_attr(self.client, lag_id4, mode=True))

            sys_logging("lag5 oid = 0x%x" %lag_id5)
            assert(lag_mode4 == _get_lag_attr(self.client, lag_id5, mode=True))

        finally:
            self.client.sai_thrift_remove_lag(lag_id1)
            self.client.sai_thrift_remove_lag(lag_id2)
            self.client.sai_thrift_remove_lag(lag_id3)
            self.client.sai_thrift_remove_lag(lag_id4)
            self.client.sai_thrift_remove_lag(lag_id5)


class fun_02_create_max_lag_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        chipname = testutils.test_params_get()['chipname']

        id_list = [SAI_SWITCH_ATTR_NUMBER_OF_LAGS, SAI_SWITCH_ATTR_LAG_MEMBERS]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(id_list)
        for attr in switch_attr_list.attr_list:
            if attr.id == SAI_SWITCH_ATTR_NUMBER_OF_LAGS:
                sys_logging("### SAI_SWITCH_ATTR_NUMBER_OF_LAGS = %d ###" %attr.value.u32)
                max_lag =attr.value.u32
            if attr.id == SAI_SWITCH_ATTR_LAG_MEMBERS:
                sys_logging("### SAI_SWITCH_ATTR_LAG_MEMBERS = %d ###" %attr.value.u32)
                max_member =attr.value.u32

        try:
            '''
            Single Mode
            '''
            sys_logging("### -----SAI_LAG_MODE_STATIC----- ###")
            sys_logging("### number of all lags * number of members per lag <= 2048 ###")
            sys_logging("### max LAGs: 256; valid MAX_MEMBERS_NUM: 1~255 ###")
            lag_list = []
            for i in range(129):
                lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_STATIC, max_member=16)
                sys_logging("lag_id = 0x%x" %lag_id)
                if 128 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_id)
                    lag_list.append(lag_id)
            for lag_id in lag_list:
                self.client.sai_thrift_remove_lag(lag_id)

            sys_logging("### -----SAI_LAG_MODE_STATIC_FAILOVER----- ###")
            sys_logging("### number of all lags * number of members per lag <= 2048 ###")
            sys_logging("### max LAGs: 256; valid MAX_MEMBERS_NUM: 1~24 ###")
            lag_list = []
            for i in range(129):
                lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_STATIC_FAILOVER, max_member=16)
                sys_logging("lag_id = 0x%x" %lag_id)
                if 128 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_id)
                    lag_list.append(lag_id)
            for lag_id in lag_list:
                self.client.sai_thrift_remove_lag(lag_id)

            sys_logging("### -----SAI_LAG_MODE_RR----- ###")
            sys_logging("### number of all lags * number of members per lag <= 2048 ###")
            sys_logging("### max LAGs: 16; valid MAX_MEMBERS_NUM: 1~255 ###")
            lag_list = []
            for i in range(17):
                lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_RR, max_member=128)
                sys_logging("lag_id = 0x%x" %lag_id)
                if 16 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_id)
                    lag_list.append(lag_id)
            for lag_id in lag_list:
                self.client.sai_thrift_remove_lag(lag_id)

            sys_logging("### -----SAI_LAG_MODE_DLB----- ###")
            lag_list = []
            if chipname == 'tsingma':
                sys_logging("### number of all lags * number of members per lag <= 2048 ###")
                sys_logging("### max LAGs: 128; valid MAX_MEMBERS_NUM: 16/32/64/128/255/512/1024/2048 ###")
                for i in range(129):
                    lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_DLB, max_member=16)
                    sys_logging("lag_id = 0x%x" %lag_id)
                    if 128 == i:
                        assert(SAI_NULL_OBJECT_ID == lag_id)
                    else:
                        assert(SAI_NULL_OBJECT_ID != lag_id)
                        lag_list.append(lag_id)
            elif chipname == 'tsingma_mx':
                sys_logging("### number of all lags * number of members per lag <= 8192 ###")
                sys_logging("### max LAGs: 256; valid MAX_MEMBERS_NUM: 16/32/64/128/255/512/1024/2048/4096/8192 ###")
                for i in range(257):
                    lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_DLB, max_member=32)
                    sys_logging("lag_id = 0x%x" %lag_id)
                    if 256 == i:
                        assert(SAI_NULL_OBJECT_ID == lag_id)
                    else:
                        assert(SAI_NULL_OBJECT_ID != lag_id)
                        lag_list.append(lag_id)
            for lag_id in lag_list:
                self.client.sai_thrift_remove_lag(lag_id)

            sys_logging("### -----SAI_LAG_MODE_RH----- ###")
            lag_list = []
            sys_logging("### number of all lags * number of members per lag <= 2048 ###")
            sys_logging("### max LAGs: 128; valid MAX_MEMBERS_NUM: 16/32/64/128/255/512/1024/2048 ###")
            for i in range(129):
                lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_RH, max_member=16)
                sys_logging("lag_id = 0x%x" %lag_id)
                if 128 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_id)
                    lag_list.append(lag_id)
            for lag_id in lag_list:
                self.client.sai_thrift_remove_lag(lag_id)

            '''
            Mixed Mode
            '''
            lag_list = []
            for i in range(32):
                lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_STATIC, max_member=16)
                sys_logging("lag_id = 0x%x" %lag_id)
                lag_list.append(lag_id)
                assert(SAI_NULL_OBJECT_ID != lag_id)

            for i in range(32):
                lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_STATIC_FAILOVER, max_member=16)
                sys_logging("lag_id = 0x%x" %lag_id)
                lag_list.append(lag_id)
                assert(SAI_NULL_OBJECT_ID != lag_id)

            for i in range(16):
                lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_RR, max_member=16)
                sys_logging("lag_id = 0x%x" %lag_id)
                lag_list.append(lag_id)
                assert(SAI_NULL_OBJECT_ID != lag_id)

            for i in range(16):
                lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_RH, max_member=16)
                sys_logging("lag_id = 0x%x" %lag_id)
                lag_list.append(lag_id)
                assert(SAI_NULL_OBJECT_ID != lag_id)

            if chipname == 'tsingma':
                sys_logging("### -----mixed mode on tsingma----- ###")
                sys_logging("### number of all lags * number of members per lag <= 2048 ###")
                for i in range(33):
                    lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_DLB, max_member=16)
                    sys_logging("lag_id = 0x%x" %lag_id)
                    if 32 == i:
                        assert(SAI_NULL_OBJECT_ID == lag_id)
                    else:
                        assert(SAI_NULL_OBJECT_ID != lag_id)
                        lag_list.append(lag_id)
                lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_RH, max_member=16)
                sys_logging("lag_id = 0x%x" %lag_id)
                assert(SAI_NULL_OBJECT_ID == lag_id)
            elif chipname == 'tsingma_mx':
                sys_logging("### -----mixed mode on tsingma_mx----- ###")
                sys_logging("### number of all lags except DLB * number of members per lag <= 2048 ###")
                sys_logging("### number of all DLB lags * number of members per lag <= 8192 ###")
                for i in range(129):
                    lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_DLB, max_member=64)
                    sys_logging("lag_id = 0x%x" %lag_id)
                    if 128 == i:
                        assert(SAI_NULL_OBJECT_ID == lag_id)
                    else:
                        assert(SAI_NULL_OBJECT_ID != lag_id)
                        lag_list.append(lag_id)
                for i in range(33):
                    lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_RH, max_member=16)
                    sys_logging("lag_id = 0x%x" %lag_id)
                    if 32 == i:
                        assert(SAI_NULL_OBJECT_ID == lag_id)
                    else:
                        assert(SAI_NULL_OBJECT_ID != lag_id)
                        lag_list.append(lag_id)

        finally:
            for lag_id in lag_list:
                self.client.sai_thrift_remove_lag(lag_id)


class fun_03_create_max_lag_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        chipname = testutils.test_params_get()['chipname']

        lag_list = []
        lag_member_list = []

        try:
            sys_logging("### -----SAI_LAG_MODE_STATIC----- ###")
            sys_logging("### MAX_MEMBERS_NUM means number of ports ###")
            lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_STATIC, max_member=8)
            for i in range(9):
                lag_member_id = sai_thrift_create_lag_member(self.client, lag_id, port_list[i])
                sys_logging("### lag_member_id = 0x%x ###" %lag_member_id)
                lag_member_list.append(lag_member_id)
                if 8 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_member_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_member_id)
            for lag_member_id in lag_member_list:
                sai_thrift_remove_lag_member(self.client, lag_member_id)
            lag_member_list = []
            self.client.sai_thrift_remove_lag(lag_id)

            lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_STATIC, max_member=16)
            for i in range(17):
                lag_member_id = sai_thrift_create_lag_member(self.client, lag_id, port_list[i])
                sys_logging("### lag_member_id = 0x%x ###" %lag_member_id)
                lag_member_list.append(lag_member_id)
                if 16 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_member_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_member_id)
            for lag_member_id in lag_member_list:
                sai_thrift_remove_lag_member(self.client, lag_member_id)
            lag_member_list = []
            self.client.sai_thrift_remove_lag(lag_id)

            sys_logging("### -----SAI_LAG_MODE_STATIC_FAILOVER----- ###")
            sys_logging("### MAX_MEMBERS_NUM means number of ports ###")
            lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_STATIC_FAILOVER, max_member=8)
            for i in range(9):
                lag_member_id = sai_thrift_create_lag_member(self.client, lag_id, port_list[i])
                sys_logging("### lag_member_id = 0x%x ###" %lag_member_id)
                lag_member_list.append(lag_member_id)
                if 8 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_member_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_member_id)
            for lag_member_id in lag_member_list:
                sai_thrift_remove_lag_member(self.client, lag_member_id)
            lag_member_list = []
            self.client.sai_thrift_remove_lag(lag_id)

            lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_STATIC_FAILOVER, max_member=16)
            for i in range(17):
                lag_member_id = sai_thrift_create_lag_member(self.client, lag_id, port_list[i])
                sys_logging("### lag_member_id = 0x%x ###" %lag_member_id)
                lag_member_list.append(lag_member_id)
                if 16 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_member_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_member_id)
            for lag_member_id in lag_member_list:
                sai_thrift_remove_lag_member(self.client, lag_member_id)
            lag_member_list = []
            self.client.sai_thrift_remove_lag(lag_id)

            sys_logging("### -----SAI_LAG_MODE_RR----- ###")
            sys_logging("### MAX_MEMBERS_NUM means number of ports ###")
            lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_RR, max_member=8)
            for i in range(9):
                lag_member_id = sai_thrift_create_lag_member(self.client, lag_id, port_list[i])
                sys_logging("### lag_member_id = 0x%x ###" %lag_member_id)
                lag_member_list.append(lag_member_id)
                if 8 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_member_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_member_id)
            for lag_member_id in lag_member_list:
                sai_thrift_remove_lag_member(self.client, lag_member_id)
            lag_member_list = []
            self.client.sai_thrift_remove_lag(lag_id)

            lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_RR, max_member=16)
            for i in range(17):
                lag_member_id = sai_thrift_create_lag_member(self.client, lag_id, port_list[i])
                sys_logging("### lag_member_id = 0x%x ###" %lag_member_id)
                lag_member_list.append(lag_member_id)
                if 16 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_member_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_member_id)
            for lag_member_id in lag_member_list:
                sai_thrift_remove_lag_member(self.client, lag_member_id)
            lag_member_list = []
            self.client.sai_thrift_remove_lag(lag_id)

            sys_logging("### -----SAI_LAG_MODE_DLB----- ###")
            sys_logging("### MAX_MEMBERS_NUM means number of flows, and max num of ports = 16 ###")
            lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_DLB, max_member=64)
            for i in range(17):
                lag_member_id = sai_thrift_create_lag_member(self.client, lag_id, port_list[i])
                sys_logging("### lag_member_id = 0x%x ###" %lag_member_id)
                lag_member_list.append(lag_member_id)
                if 16 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_member_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_member_id)
            for lag_member_id in lag_member_list:
                sai_thrift_remove_lag_member(self.client, lag_member_id)
            lag_member_list = []
            self.client.sai_thrift_remove_lag(lag_id)

            lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_DLB, max_member=256)
            for i in range(17):
                lag_member_id = sai_thrift_create_lag_member(self.client, lag_id, port_list[i])
                sys_logging("### lag_member_id = 0x%x ###" %lag_member_id)
                lag_member_list.append(lag_member_id)
                if 16 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_member_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_member_id)
            for lag_member_id in lag_member_list:
                sai_thrift_remove_lag_member(self.client, lag_member_id)
            lag_member_list = []
            self.client.sai_thrift_remove_lag(lag_id)

            sys_logging("### -----SAI_LAG_MODE_RH----- ###")
            sys_logging("### MAX_MEMBERS_NUM means number of ports ###")
            lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_RH, max_member=16)
            for i in range(17):
                lag_member_id = sai_thrift_create_lag_member(self.client, lag_id, port_list[i])
                sys_logging("### lag_member_id = 0x%x ###" %lag_member_id)
                lag_member_list.append(lag_member_id)
                if 16 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_member_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_member_id)
            for lag_member_id in lag_member_list:
                sai_thrift_remove_lag_member(self.client, lag_member_id)
            lag_member_list = []
            self.client.sai_thrift_remove_lag(lag_id)

            lag_id = sai_thrift_create_lag(self.client, lag_mode=SAI_LAG_MODE_RH, max_member=32)
            for i in range(32):
                lag_member_id = sai_thrift_create_lag_member(self.client, lag_id, port_list[i])
                sys_logging("### lag_member_id = 0x%x ###" %lag_member_id)
                lag_member_list.append(lag_member_id)
                if 32 == i:
                    assert(SAI_NULL_OBJECT_ID == lag_member_id)
                else:
                    assert(SAI_NULL_OBJECT_ID != lag_member_id)
            for lag_member_id in lag_member_list:
                sai_thrift_remove_lag_member(self.client, lag_member_id)
            lag_member_list = []
            self.client.sai_thrift_remove_lag(lag_id)

        finally:
            for lag_member_id in lag_member_list:
                sai_thrift_remove_lag_member(self.client, lag_member_id)


class fun_04_create_5_mode_invalid_param_lag_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        lag_mode1 = SAI_LAG_MODE_STATIC_FAILOVER
        lag_mode2 = SAI_LAG_MODE_RR
        lag_mode3 = SAI_LAG_MODE_DLB
        lag_mode4 = SAI_LAG_MODE_RH
        lag_id1 = sai_thrift_create_lag(self.client, max_member=256)
        lag_id2 = sai_thrift_create_lag(self.client, lag_mode=lag_mode1, max_member=25)
        lag_id3 = sai_thrift_create_lag(self.client, lag_mode=lag_mode2, max_member=0)
        lag_id4 = sai_thrift_create_lag(self.client, lag_mode=lag_mode3, max_member=255)
        lag_id5 = sai_thrift_create_lag(self.client, lag_mode=lag_mode4, max_member=15)

        lag_id6 = sai_thrift_create_lag(self.client, max_member=255)
        lag_id7 = sai_thrift_create_lag(self.client, lag_mode=lag_mode1, max_member=24)
        lag_id8 = sai_thrift_create_lag(self.client, lag_mode=lag_mode2, max_member=208)
        lag_id9 = sai_thrift_create_lag(self.client, lag_mode=lag_mode3, max_member=1024)
        lag_id10 = sai_thrift_create_lag(self.client, lag_mode=lag_mode4, max_member=512)

        try:
            sys_logging("lag1 oid = 0x%x" %lag_id1)
            assert(lag_id1==SAI_NULL_OBJECT_ID)
            sys_logging("lag2 oid = 0x%x" %lag_id2)
            assert(lag_id2==SAI_NULL_OBJECT_ID)
            sys_logging("lag3 oid = 0x%x" %lag_id3)
            assert(lag_id3==SAI_NULL_OBJECT_ID)
            sys_logging("lag4 oid = 0x%x" %lag_id4)
            assert(lag_id4==SAI_NULL_OBJECT_ID)
            sys_logging("lag5 oid = 0x%x" %lag_id5)
            assert(lag_id5==SAI_NULL_OBJECT_ID)

            sys_logging("lag6 oid = 0x%x" %lag_id6)
            assert(lag_id6 != SAI_NULL_OBJECT_ID)
            sys_logging("lag7 oid = 0x%x" %lag_id7)
            assert(lag_id7 != SAI_NULL_OBJECT_ID)
            sys_logging("lag8 oid = 0x%x" %lag_id8)
            assert(lag_id8 != SAI_NULL_OBJECT_ID)
            sys_logging("lag9 oid = 0x%x" %lag_id9)
            assert(lag_id9 != SAI_NULL_OBJECT_ID)
            sys_logging("lag10 oid = 0x%x" %lag_id10)
            assert(lag_id10 != SAI_NULL_OBJECT_ID)

        finally:
            self.client.sai_thrift_remove_lag(lag_id6)
            self.client.sai_thrift_remove_lag(lag_id7)
            self.client.sai_thrift_remove_lag(lag_id8)
            self.client.sai_thrift_remove_lag(lag_id9)
            self.client.sai_thrift_remove_lag(lag_id10)


class fun_05_remove_5_mode_lag_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        lag_mode1 = SAI_LAG_MODE_STATIC_FAILOVER
        lag_mode2 = SAI_LAG_MODE_RR
        lag_mode3 = SAI_LAG_MODE_DLB
        lag_mode4 = SAI_LAG_MODE_RH
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_id2 = sai_thrift_create_lag(self.client, lag_mode=lag_mode1)
        lag_id3 = sai_thrift_create_lag(self.client, lag_mode=lag_mode2)
        lag_id4 = sai_thrift_create_lag(self.client, lag_mode=lag_mode3)
        lag_id5 = sai_thrift_create_lag(self.client, lag_mode=lag_mode4)

        try:
            status = self.client.sai_thrift_remove_lag(lag_id1)
            sys_logging( "status = %d" %status)
            assert(status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_lag(lag_id2)
            sys_logging( "status = %d" %status)
            assert(status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_lag(lag_id3)
            sys_logging( "status = %d" %status)
            assert(status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_lag(lag_id4)
            sys_logging( "status = %d" %status)
            assert(status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_lag(lag_id5)
            sys_logging( "status = %d" %status)
            assert(status == SAI_STATUS_SUCCESS)

            attrs= self.client.sai_thrift_get_lag_attribute(lag_id1)
            sys_logging( "status = %d" %attrs.status)
            assert(attrs.status == SAI_STATUS_INVALID_OBJECT_ID)
            attrs = self.client.sai_thrift_get_lag_attribute(lag_id2)
            sys_logging( "status = %d" %attrs.status)
            assert(attrs.status == SAI_STATUS_INVALID_OBJECT_ID)
            attrs = self.client.sai_thrift_get_lag_attribute(lag_id3)
            sys_logging( "status = %d" %attrs.status)
            assert(attrs.status == SAI_STATUS_INVALID_OBJECT_ID)
            attrs = self.client.sai_thrift_get_lag_attribute(lag_id4)
            sys_logging( "status = %d" %attrs.status)
            assert(attrs.status == SAI_STATUS_INVALID_OBJECT_ID)
            attrs = self.client.sai_thrift_get_lag_attribute(lag_id5)
            sys_logging( "status = %d" %attrs.status)
            assert(attrs.status == SAI_STATUS_INVALID_OBJECT_ID)

        finally:
            pass


class fun_06_remove_no_exist_lag_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        lag_id1 = sai_thrift_create_lag(self.client)
        self.client.sai_thrift_remove_lag(lag_id1)

        try:
            status = self.client.sai_thrift_remove_lag(lag_id1)
            sys_logging("status = %d" %status)
            assert(status == SAI_STATUS_INVALID_OBJECT_ID)

        finally:
            pass


class fun_07_set_lag_attr_igs_acl_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        lag_id1 = sai_thrift_create_lag(self.client)

        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_LAG]
        in_ports = [port1, port2]
        svlan_id=None
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=None
        ip_src = "192.168.0.1"
        ip_dst = '10.10.10.1'
        ip_type = None
        ip_proto = None
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        addr_family = None
        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'

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
            None,None,None,None,None,None,None,None,None,None,
            None,None,None,None,None,None,None,None,None,None,
            ip_proto,
            src_l4_port,
            dst_l4_port)

        try:
            assert(SAI_NULL_OBJECT_ID == _get_lag_attr(self.client, lag_id1, ingress_acl=True))

            assert(SAI_STATUS_SUCCESS == _set_lag_attr(self.client, lag_id1, ingress_acl=acl_table_id))
            assert(acl_table_id == _get_lag_attr(self.client, lag_id1, ingress_acl=True))

        finally:
            #_set_lag_attr(self.client, lag_id1, ingress_acl=SAI_NULL_OBJECT_ID)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_08_set_lag_attr_pvid_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port_vlan_id = 100
        lag_id1 = sai_thrift_create_lag(self.client)

        try:
            assert(1 == _get_lag_attr(self.client, lag_id1, port_vlan_id=True))

            assert(SAI_STATUS_SUCCESS == _set_lag_attr(self.client, lag_id1, port_vlan_id=port_vlan_id))
            assert(port_vlan_id == _get_lag_attr(self.client, lag_id1, port_vlan_id=True))

        finally:
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_09_set_lag_attr_default_cos_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        default_vlan_cos = 6
        lag_id1 = sai_thrift_create_lag(self.client)
        
        try:
            assert(0 == _get_lag_attr(self.client, lag_id1, default_vlan_priority=True))

            assert(SAI_STATUS_SUCCESS == _set_lag_attr(self.client, lag_id1, default_vlan_priority=default_vlan_cos))
            assert(default_vlan_cos == _get_lag_attr(self.client, lag_id1, default_vlan_priority=True))

        finally:
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_10_set_lag_attr_drop_untagged_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        lag_id1 = sai_thrift_create_lag(self.client)

        try:
            assert(False == _get_lag_attr(self.client, lag_id1, drop_untagged=True))

            assert(SAI_STATUS_SUCCESS == _set_lag_attr(self.client, lag_id1, drop_untagged=True))
            assert(True == _get_lag_attr(self.client, lag_id1, drop_untagged=True))

        finally:
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_11_set_lag_attr_drop_tagged_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        lag_id1 = sai_thrift_create_lag(self.client, drop_tagged=True)
        
        try:
            assert(True == _get_lag_attr(self.client, lag_id1, drop_tagged=True))

            assert(SAI_STATUS_SUCCESS == _set_lag_attr(self.client, lag_id1, drop_tagged=False))
            assert(False == _get_lag_attr(self.client, lag_id1, drop_tagged=True))

        finally:
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_12_get_lag_all_default_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        lag_id1 = sai_thrift_create_lag(self.client)

        try:
            attrs= _get_lag_attr(self.client, lag_id1, port_list=True, ingress_acl=True,
                                 port_vlan_id=True, default_vlan_priority=True, drop_untagged=True, drop_tagged=True,
                                 mode=True, max_member_num=True)

            assert(0 == attrs[0].count)
            assert([] == attrs[0].object_id_list)
            assert(SAI_NULL_OBJECT_ID == attrs[1])
            assert(1 == attrs[2])
            assert(0 == attrs[3])
            assert(False == attrs[4])
            assert(False == attrs[5])
            assert(SAI_LAG_MODE_STATIC == attrs[6])
            assert(16 == attrs[7])

        finally:
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_13_get_lag_all_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        lag_mode4 = SAI_LAG_MODE_RH
        port_vlan_id = 100
        default_cos = 4
        drop_untagged = True
        drop_tagged = True
        max_member = 128
        lag_id1 = sai_thrift_create_lag(self.client, lag_mode=lag_mode4,
                                        pvid=port_vlan_id, default_vlan_pri=default_cos,
                                        drop_untagged=drop_untagged, drop_tagged=drop_tagged,
                                        max_member=max_member)
        sys_logging("lag1 oid = 0x%x" %lag_id1)

        try:
            attrs= self.client.sai_thrift_get_lag_attribute(lag_id1)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_LAG_ATTR_PORT_LIST:
                    sys_logging("get lag member list")
                    assert (a.value.objlist.object_id_list == [])
                if a.id == SAI_LAG_ATTR_MODE:
                    sys_logging("get lag mode = %d" %a.value.s32)
                    assert(4 == a.value.s32)
                if a.id == SAI_LAG_ATTR_PORT_VLAN_ID:
                    sys_logging("get port vlan id = %d" %a.value.u16)
                    assert(100 == a.value.u16)
                if a.id == SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY:
                    sys_logging("get default vlan priority = %d" %a.value.u8)
                    assert(4 == a.value.u8)
                if a.id == SAI_LAG_ATTR_DROP_UNTAGGED:
                    sys_logging("get drrop untagged value = %d" %a.value.booldata)
                    assert(True == a.value.booldata)
                if a.id == SAI_LAG_ATTR_DROP_TAGGED:
                    sys_logging("get drrop tagged value = %d" %a.value.booldata)
                    assert(True == a.value.booldata)
                if a.id == SAI_LAG_ATTR_INGRESS_ACL:
                    sys_logging("get ingress acl = %d" %a.value.oid)
                    assert(SAI_NULL_OBJECT_ID == a.value.oid)
                if a.id == SAI_LAG_ATTR_CUSTOM_MAX_MEMBER_NUM:
                    sys_logging("get max member number = %d" %a.value.u16)
                    assert(128 == a.value.u16)

        finally:
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_14_add_member_get_lag_attr_port_list_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

        lag_id1 = sai_thrift_create_lag(self.client)

        try:
            attrs= self.client.sai_thrift_get_lag_attribute(lag_id1)
            sys_logging( "status = %d" %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_LAG_ATTR_PORT_LIST:
                    print "get lag member list =",
                    print a.value.objlist.object_id_list
                    assert(a.value.objlist.object_id_list == [])

            lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
            lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
            lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
            lag_member_list = [lag_member_id1, lag_member_id2, lag_member_id3]

            attrs= self.client.sai_thrift_get_lag_attribute(lag_id1)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_LAG_ATTR_PORT_LIST:
                    print "get lag member list =",
                    print a.value.objlist.object_id_list
                    assert(a.value.objlist.object_id_list == lag_member_list)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_15_create_lag_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        lag_id1 = sai_thrift_create_lag(self.client)
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2, egress_disable=True)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3, ingress_disable=True)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id1, port4, egress_disable=True, ingress_disable=True)

        try:
            sys_logging("lag member oid = 0x%x" %lag_member_id1)
            
            assert(lag_member_id1%0x100000000==0x1f00001b)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id1)
            sys_logging("status = %d" %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("lag member oid = 0x%x" %lag_member_id2)
            assert(lag_member_id2%0x100000000==0x1f00001b)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id2)
            sys_logging("status = %d" %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("lag member oid = 0x%x" %lag_member_id3)
            assert(lag_member_id3%0x100000000==0x1f00001b)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id3)
            sys_logging("status = %d" %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("lag member oid = 0x%x" %lag_member_id4)
            assert(lag_member_id4%0x100000000==0x1f00001b)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id4)
            sys_logging("status = %d" %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_16_create_exist_lag_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        lag_id1 = sai_thrift_create_lag(self.client)

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1, egress_disable = True, ingress_disable = True)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port1, egress_disable = True)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port1, ingress_disable = True)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id1, port1)

        lag_member_id5 = sai_thrift_create_lag_member(self.client, lag_id1, port2, egress_disable = True)
        lag_member_id6 = sai_thrift_create_lag_member(self.client, lag_id1, port2, ingress_disable = True)

        lag_member_id7 = sai_thrift_create_lag_member(self.client, lag_id1, port3, ingress_disable = True)
        lag_member_id8 = sai_thrift_create_lag_member(self.client, lag_id1, port3, egress_disable = True)

        lag_member_id9 = sai_thrift_create_lag_member(self.client, lag_id1, port4)
        lag_member_id10 = sai_thrift_create_lag_member(self.client, lag_id1, port4, egress_disable = True, ingress_disable = True)

        try:
            sys_logging("lag member oid = 0x%x" %lag_member_id1)
            assert(lag_member_id1%0x100000000==0x1f00001b)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id1)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("lag member oid = 0x%x" %lag_member_id2)
            assert(lag_member_id2==SAI_NULL_OBJECT_ID)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id2)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_INVALID_OBJECT_ID)

            sys_logging("lag member oid = 0x%x" %lag_member_id3)
            assert(lag_member_id3==SAI_NULL_OBJECT_ID)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id3)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_INVALID_OBJECT_ID)

            sys_logging("lag member oid = 0x%x" %lag_member_id4)
            assert(lag_member_id4==SAI_NULL_OBJECT_ID)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id4)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_INVALID_OBJECT_ID)

            sys_logging("lag member oid = 0x%x" %lag_member_id5)
            assert(lag_member_id1%0x100000000==0x1f00001b)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id5)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("lag member oid = 0x%x" %lag_member_id6)
            assert(lag_member_id2==SAI_NULL_OBJECT_ID)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id6)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_INVALID_OBJECT_ID)

            sys_logging("lag member oid = 0x%x" %lag_member_id7)
            assert(lag_member_id1%0x100000000==0x1f00001b)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id7)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("lag member oid = 0x%x" %lag_member_id8)
            assert(lag_member_id2==SAI_NULL_OBJECT_ID)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id8)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_INVALID_OBJECT_ID)

            sys_logging("lag member oid = 0x%x" %lag_member_id9)
            assert(lag_member_id1%0x100000000==0x1f00001b)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id9)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            sys_logging("lag member oid = 0x%x" %lag_member_id10)
            assert(lag_member_id2==SAI_NULL_OBJECT_ID)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id10)
            sys_logging( "status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_INVALID_OBJECT_ID)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id5)
            sai_thrift_remove_lag_member(self.client, lag_member_id7)
            sai_thrift_remove_lag_member(self.client, lag_member_id9)
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_17_remove_lag_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        lag_id1 = sai_thrift_create_lag(self.client)

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2, egress_disable=True)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3, ingress_disable=True)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id1, port4, egress_disable=True, ingress_disable=True)

        try:
            status = sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sys_logging("remove lag member status = %d" %status)
            assert(status==SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id1)
            sys_logging( "get lag member status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

            status = sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sys_logging("remove lag member status = %d" %status)
            assert(status==SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id2)
            sys_logging( "get lag member status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

            status = sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sys_logging("remove lag member status = %d" %status)
            assert(status==SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id3)
            sys_logging( "get lag member status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

            status = sai_thrift_remove_lag_member(self.client, lag_member_id4)
            sys_logging("remove lag member status = %d" %status)
            assert(status==SAI_STATUS_SUCCESS)
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id4)
            sys_logging( "get lag member status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_18_remove_no_exist_lag_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        lag_id1 = sai_thrift_create_lag(self.client)

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2, egress_disable=True)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3, ingress_disable=True)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id1, port4, egress_disable=True, ingress_disable=True)

        sai_thrift_remove_lag_member(self.client, lag_member_id1)
        sai_thrift_remove_lag_member(self.client, lag_member_id2)
        sai_thrift_remove_lag_member(self.client, lag_member_id3)
        sai_thrift_remove_lag_member(self.client, lag_member_id4)

        try:
            status = self.client.sai_thrift_remove_lag_member(lag_member_id1)
            sys_logging("remove lag member status = %d" %status)
            assert(status==SAI_STATUS_ITEM_NOT_FOUND)

            status = self.client.sai_thrift_remove_lag_member(lag_member_id2)
            sys_logging("remove lag member status = %d" %status)
            assert(status==SAI_STATUS_ITEM_NOT_FOUND)

            status = self.client.sai_thrift_remove_lag_member(lag_member_id3)
            sys_logging("remove lag member status = %d" %status)
            assert(status==SAI_STATUS_ITEM_NOT_FOUND)

            status = self.client.sai_thrift_remove_lag_member(lag_member_id4)
            sys_logging("remove lag member status = %d" %status)
            assert(status==SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_19_set_lag_member_attribute_igs_disable_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1,)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2, ingress_disable=True)

        try:
            assert(False == _get_lag_member_attr(self.client, lag_member_id1, ingress_disable=True))
            assert(True == _get_lag_member_attr(self.client, lag_member_id2, ingress_disable=True))

            assert(SAI_STATUS_SUCCESS == _set_lag_member_attr(self.client, lag_member_id1, ingress_disable=True))
            assert(SAI_STATUS_SUCCESS == _set_lag_member_attr(self.client, lag_member_id2, ingress_disable=False))

            assert(True == _get_lag_member_attr(self.client, lag_member_id1, ingress_disable=True))
            assert(False == _get_lag_member_attr(self.client, lag_member_id2, ingress_disable=True))

        finally:
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_20_set_lag_member_attribute_egs_disable_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2, egress_disable=True)

        try:
            assert(False == _get_lag_member_attr(self.client, lag_member_id1, egress_disable=True))
            assert(True == _get_lag_member_attr(self.client, lag_member_id2, egress_disable=True))

            assert(SAI_STATUS_SUCCESS == _set_lag_member_attr(self.client, lag_member_id1, egress_disable=True))
            assert(SAI_STATUS_SUCCESS == _set_lag_member_attr(self.client, lag_member_id2, egress_disable=False))

            assert(True == _get_lag_member_attr(self.client, lag_member_id1, egress_disable=True))
            assert(False == _get_lag_member_attr(self.client, lag_member_id2, egress_disable=True))

        finally:
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            self.client.sai_thrift_remove_lag(lag_id1)


class fun_21_get_lag_member_all_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        lag_mode2 = SAI_LAG_MODE_RR

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_id2 = sai_thrift_create_lag(self.client, lag_mode=lag_mode2, max_member=24)

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id2, port2, ingress_disable=True, egress_disable=True)

        try:
            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id1)
            sys_logging( "get lag member attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_LAG_MEMBER_ATTR_LAG_ID:
                    sys_logging("get ingress disable value = 0x%x" %a.value.oid)
                    assert(lag_id1 == a.value.oid)
                if a.id == SAI_LAG_MEMBER_ATTR_PORT_ID:
                    sys_logging("get egress disable value = 0x%x" %a.value.oid)
                    assert(port1 == a.value.oid)
                if a.id == SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE:
                    sys_logging("get ingress disable value = %d" %a.value.booldata)
                    assert(False == a.value.booldata)
                if a.id == SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE:
                    sys_logging("get egress disable value = %d" %a.value.booldata)
                    assert(False == a.value.booldata)

            attrs = self.client.sai_thrift_get_lag_member_attribute(lag_member_id2)
            sys_logging( "get lag member attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_LAG_MEMBER_ATTR_LAG_ID:
                    sys_logging("get ingress disable value = 0x%x" %a.value.oid)
                    assert(lag_id2 == a.value.oid)
                if a.id == SAI_LAG_MEMBER_ATTR_PORT_ID:
                    sys_logging("get egress disable value = 0x%x" %a.value.oid)
                    assert(port2 == a.value.oid)
                if a.id == SAI_LAG_MEMBER_ATTR_INGRESS_DISABLE:
                    sys_logging("get ingress disable value = %d" %a.value.booldata)
                    assert(True == a.value.booldata)
                if a.id == SAI_LAG_MEMBER_ATTR_EGRESS_DISABLE:
                    sys_logging("get egress disable value = %d" %a.value.booldata)
                    assert(True == a.value.booldata)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            self.client.sai_thrift_remove_lag(lag_id1)
            self.client.sai_thrift_remove_lag(lag_id2)


class scenario_01_lag_bind_bridge_port_vlan_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        port7 = port_list[6]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_oid1 = sai_thrift_create_bridge_port(self.client, lag_id1)

        lag_id2 = sai_thrift_create_lag(self.client)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id2, port5)
        lag_member_id5 = sai_thrift_create_lag_member(self.client, lag_id2, port6)
        lag_member_id6 = sai_thrift_create_lag_member(self.client, lag_id2, port7)
        lag_oid2 = sai_thrift_create_bridge_port(self.client, lag_id2)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid2, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)
        self.client.sai_thrift_set_lag_attribute(lag_id2, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        # set lag hash
        id_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(id_list)
        for attr in switch_attr_list.attr_list:
            if attr.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = 0x%x ###" %attr.value.oid)
                lag_hash_id =attr.value.oid
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(lag_hash_id, attr)

        warmboot(self.client)

        try:
            count = [0, 0, 0, 0, 0, 0, 0]
            max_itrs = 3
            src_mac_start = '00:22:22:22:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(eth_dst=mac1,
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet(3, str(pkt))
                self.ctc_verify_packets(exp_pkt, [i,i+4])

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            sai_thrift_remove_bport_by_lag(self.client, lag_oid2)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            sai_thrift_remove_lag_member(self.client, lag_member_id5)
            sai_thrift_remove_lag_member(self.client, lag_member_id6)
            sai_thrift_remove_lag(self.client, lag_id2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            #for port in sai_port_list:
            #    sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC,
                          SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(lag_hash_id, attr)


class scenario_02_lag_bind_bridge_port_fdb_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        port7 = port_list[6]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        is_lag = True
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_oid1 = sai_thrift_create_bridge_port(self.client, lag_id1)

        lag_id2 = sai_thrift_create_lag(self.client)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id2, port5)
        lag_member_id5 = sai_thrift_create_lag_member(self.client, lag_id2, port6)
        lag_member_id6 = sai_thrift_create_lag_member(self.client, lag_id2, port7)
        lag_oid2 = sai_thrift_create_bridge_port(self.client, lag_id2)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid2, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)
        self.client.sai_thrift_set_lag_attribute(lag_id2, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1)
        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac2, lag_oid2)

        # set lag hash
        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)

        try:
            count = [0, 0, 0, 0, 0, 0, 0]
            max_itrs = 3
            src_mac_start = '00:22:22:22:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst=mac1,
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_port = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"rcv_port = %d" %rcv_port
                count[rcv_port] += 1

            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac2,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst=mac2,
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_port = self.ctc_verify_any_packet_any_port( [exp_pkt], [4, 5, 6])
                print"rcv_port = %d" %rcv_port
                count[rcv_port] += 1

            print"count =",
            print count
            assert(count == [1,1,1,0,1,1,1])

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            sai_thrift_remove_bport_by_lag(self.client, lag_oid2)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            sai_thrift_remove_lag_member(self.client, lag_member_id5)
            sai_thrift_remove_lag_member(self.client, lag_member_id6)
            sai_thrift_remove_lag(self.client, lag_id2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC,
                          SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr) 


class scenario_03_lag_bind_bridge_port_add_and_remove_member_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        port7 = port_list[6]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        is_lag = True
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_oid1 = sai_thrift_create_bridge_port(self.client, lag_id1)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr) 

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1)

        # set lag hash
        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)

        try:
            count = [0, 0, 0, 0, 0]
            max_itrs = 3
            src_mac_start = '00:22:22:22:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst=mac1,
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet(3, str(pkt))
                rcv_port = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"rcv_port = %d" %rcv_port
                count[rcv_port] += 1

            print"count =",
            print count
            assert(count == [1,1,1,0,0])

            lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id1, port5)
            max_itrs = 4
            src_mac_start = '00:22:22:22:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst=mac1,
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_port = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2, 4])
                print"rcv_port = %d" %rcv_port
                count[rcv_port] += 1

            print"count =",
            print count
            assert(count == [2,2,2,0,1])

            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            max_itrs = 2
            src_mac_start = '00:22:22:22:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst=mac1,
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_port = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1])
                print"rcv_port = %d" %rcv_port
                count[rcv_port] += 1

            print"count =",
            print count
            assert(count == [3,3,2,0,1])

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr) 


class scenario_04_lag_bind_sub_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3] 
        port5 = port_list[4]
        port6 = port_list[5]
        port7 = port_list[6]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_id2 = sai_thrift_create_lag(self.client)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id2, port5)
        lag_member_id5 = sai_thrift_create_lag_member(self.client, lag_id2, port6)
        lag_member_id6 = sai_thrift_create_lag_member(self.client, lag_id2, port7)
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)    

        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id1, vlan_id2)
        sub_port_id3 = sai_thrift_create_bridge_sub_port(self.client, lag_id2, bridge_id1, vlan_id1)

        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)

        try:
            count = [0, 0, 0, 0, 0, 0, 0]
            max_itrs = 4
            src_mac_start = '00:00:00:00:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])

                pkt1 = simple_tcp_packet(eth_dst=mac2,
                                        eth_src=src_mac,
                                        dl_vlan_enable=True,
                                        vlan_vid=10,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                pkt2 = simple_tcp_packet(eth_dst=mac2,
                                            eth_src=src_mac,
                                            dl_vlan_enable=True,
                                            vlan_vid=20,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet(2, str(pkt1))
                self.ctc_verify_any_packet_any_port( [pkt1], [4, 5, 6]) 
                self.ctc_verify_any_packet_any_port( [pkt2], [0, 1, 2]) 

                self.ctc_send_packet(1, str(pkt2))
                self.ctc_verify_any_packet_any_port( [pkt1], [4, 5, 6]) 
                self.ctc_verify_any_packet_any_port( [pkt1], [0, 1, 2]) 

                self.ctc_send_packet(4, str(pkt1))
                self.ctc_verify_any_packet_any_port( [pkt1], [0, 1, 2]) 
                self.ctc_verify_any_packet_any_port( [pkt2], [0, 1, 2]) 

        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge_port(sub_port_id3)
            self.client.sai_thrift_remove_bridge(bridge_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            sai_thrift_remove_lag_member(self.client, lag_member_id5)
            sai_thrift_remove_lag_member(self.client, lag_member_id6)
            sai_thrift_remove_lag(self.client, lag_id2)
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)


class scenario_05_lag_bind_sub_port_add_and_remove_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        port7 = port_list[6]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:03'

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)

        lag_id2 = sai_thrift_create_lag(self.client)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id2, port5)
        lag_member_id5 = sai_thrift_create_lag_member(self.client, lag_id2, port6)
        lag_member_id6 = sai_thrift_create_lag_member(self.client, lag_id2, port7)
        bridge_id1 = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sub_port_id1 = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id1, vlan_id1)
        sub_port_id2 = sai_thrift_create_bridge_sub_port(self.client, lag_id2, bridge_id1, vlan_id2)

        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)

        try:
            lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
            lag_member_id7 = sai_thrift_create_lag_member(self.client, lag_id1, port4)

            max_itrs = 4
            src_mac_start = '00:00:00:00:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])

                pkt1 = simple_tcp_packet(eth_dst=mac2,
                                        eth_src=src_mac,
                                        dl_vlan_enable=True,
                                        vlan_vid=10,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                pkt2 = simple_tcp_packet(eth_dst=mac2,
                                            eth_src=src_mac,
                                            dl_vlan_enable=True,
                                            vlan_vid=20,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet(i, str(pkt1))
                self.ctc_verify_any_packet_any_port( [pkt2], [4, 5, 6]) 

                self.ctc_send_packet(i%3+4, str(pkt2))
                self.ctc_verify_any_packet_any_port( [pkt1], [0, 1, 2, 3])

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            max_itrs = 3
            src_mac_start = '00:00:00:00:33:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])

                pkt1 = simple_tcp_packet(eth_dst=mac2,
                                        eth_src=src_mac,
                                        dl_vlan_enable=True,
                                        vlan_vid=10,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                pkt2 = simple_tcp_packet(eth_dst=mac2,
                                            eth_src=src_mac,
                                            dl_vlan_enable=True,
                                            vlan_vid=20,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet(i%3+4, str(pkt2))
                self.ctc_verify_any_packet_any_port( [pkt1], [2, 3])

        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, bridge_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id1)
            self.client.sai_thrift_remove_bridge_port(sub_port_id2)
            self.client.sai_thrift_remove_bridge(bridge_id1) 
            sai_thrift_remove_lag_member(self.client, lag_member_id7)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            sai_thrift_remove_lag_member(self.client, lag_member_id5)
            sai_thrift_remove_lag_member(self.client, lag_member_id6)
            sai_thrift_remove_lag(self.client, lag_id2)
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)


class scenario_06_lag_set_drop_untagged_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        port7 = port_list[6]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_oid1 = sai_thrift_create_bridge_port(self.client, lag_id1)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        # set lag hash
        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)

        try:
            max_itrs = 3
            src_mac_start = '00:22:22:22:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                pkt1 = simple_tcp_packet(eth_dst=mac1,
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet(i, str(pkt))
                self.ctc_verify_packets(pkt1, [3])

            drop_untagged = True
            lag_attr_value = sai_thrift_attribute_value_t(booldata=drop_untagged)
            attribute = sai_thrift_attribute_t(id=SAI_LAG_ATTR_DROP_UNTAGGED, value=lag_attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_id1, attribute)

            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                pkt1 = simple_tcp_packet(eth_dst=mac1,
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet(i, str(pkt))
                self.ctc_verify_no_packet(pkt1, 3)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr) 


class scenario_07_lag_set_drop_tagged_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, port3, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id1)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id2)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        pkt1 = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:23',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64)
        exp_pkt1 = simple_tcp_packet(
                                eth_dst=dmac1,
                                eth_src=router_mac,
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_dst='10.10.10.10',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packet(exp_pkt, 2)

            self.ctc_send_packet(1, str(pkt))
            self.ctc_verify_packet(exp_pkt, 2)

            drop_untagged = True
            lag_attr_value = sai_thrift_attribute_value_t(booldata=drop_untagged)
            attribute = sai_thrift_attribute_t(id=SAI_LAG_ATTR_DROP_TAGGED, value=lag_attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_id1, attribute)

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet(exp_pkt, 2)

            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_no_packet(exp_pkt, 2)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag(self.client, lag_id1)
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr) 


class scenario_08_lag_set_pvid_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        vlan_id = 10
        vlan_id1 = 20

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        port7 = port_list[6]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_oid1 = sai_thrift_create_bridge_port(self.client, lag_id1)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_TAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        # set lag hash
        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)

        try:
            max_itrs = 3
            src_mac_start = '00:22:22:22:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                pkt1 = simple_tcp_packet(eth_dst=mac1,
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                self.ctc_verify_packets( pkt1, [i])

            vlan_id_new = 30
            lag_attr_value = sai_thrift_attribute_value_t(u16=vlan_id_new)
            attribute = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=lag_attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_id1, attribute)

            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                pkt1 = simple_tcp_packet(eth_dst=mac1,
                                            eth_src=src_mac,
                                            dl_vlan_enable=True,
                                            vlan_vid=10,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64,
                                            pktlen=104)

                self.ctc_send_packet( 3, str(pkt))
                self.ctc_verify_packets( pkt1, [i])

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr) 


class scenario_09_lag_set_default_vlan_cos_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        vlan_id = 10
        vlan_id1 = 20

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        port7 = port_list[6]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        lag_oid1 = sai_thrift_create_bridge_port(self.client, lag_id1)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_TAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        # set lag hash
        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)

        try:
            max_itrs = 3
            src_mac_start = '00:22:22:22:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                pkt1 = simple_tcp_packet(eth_dst=mac1,
                                            eth_src=src_mac,
                                            dl_vlan_enable=True,
                                            vlan_vid=10,
                                            vlan_pcp=0,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64,
                                            pktlen=104)

                self.ctc_send_packet( i, str(pkt))
                self.ctc_verify_packets( pkt1, [3])

            default_vlan_cos = 5
            lag_attr_value = sai_thrift_attribute_value_t(u8=default_vlan_cos)
            attribute = sai_thrift_attribute_t(id=SAI_LAG_ATTR_DEFAULT_VLAN_PRIORITY, value=lag_attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_id1, attribute)

            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                pkt1 = simple_tcp_packet(eth_dst=mac1,
                                            eth_src=src_mac,
                                            dl_vlan_enable=True,
                                            vlan_vid=10,
                                            vlan_pcp=5,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64,
                                            pktlen=104)

                self.ctc_send_packet( i, str(pkt))
                self.ctc_verify_packets( pkt1, [3])

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr) 


class scenario_10_lag_bind_phyif_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '20.20.20.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2= '00:11:22:33:44:66'

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3= sai_thrift_create_lag_member(self.client, lag_id1, port3)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2) 

        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)

        try:
            max_itrs = 6
            src_mac_start = '00:00:00:00:33:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])

                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src=src_mac ,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(
                                        eth_dst=dmac1,
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=63)

                self.ctc_send_packet(3, str(pkt))
                self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2]) 

            pkt1 = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:23',
                                    ip_dst='20.20.20.1',
                                    ip_src='192.168.0.1',
                                    ip_id=105,
                                    ip_ttl=64)
            exp_pkt1 = simple_tcp_packet(
                                    eth_dst=dmac2,
                                    eth_src=router_mac,
                                    ip_dst='20.20.20.1',
                                    ip_src='192.168.0.1',
                                    ip_id=105,
                                    ip_ttl=63)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 3)
            self.ctc_send_packet( 1, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 3)
            self.ctc_send_packet( 2, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 3)

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag(self.client, lag_id1)
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)


class scenario_11_lag_bind_phyif_add_and_remove_member_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '20.20.20.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2= '00:11:22:33:44:66'

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3= sai_thrift_create_lag_member(self.client, lag_id1, port3)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2) 

        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)

        try:
            lag_member_id4= sai_thrift_create_lag_member(self.client, lag_id1, port5)
            lag_member_id5= sai_thrift_create_lag_member(self.client, lag_id1, port6)
            max_itrs = 10
            src_mac_start = '00:00:00:00:33:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])

                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src=src_mac ,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(
                                        eth_dst=dmac1,
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=63)

                self.ctc_send_packet(3, str(pkt))
                self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2, 4, 5]) 

            pkt1 = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:23',
                                    ip_dst='20.20.20.1',
                                    ip_src='192.168.0.1',
                                    ip_id=105,
                                    ip_ttl=64)
            exp_pkt1 = simple_tcp_packet(
                                    eth_dst=dmac2,
                                    eth_src=router_mac,
                                    ip_dst='20.20.20.1',
                                    ip_src='192.168.0.1',
                                    ip_id=105,
                                    ip_ttl=63)

            self.ctc_send_packet( 4, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 3)
            self.ctc_send_packet( 5, str(pkt1))
            self.ctc_verify_packet( exp_pkt1, 3)

            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            max_itrs = 4
            src_mac_start = '00:00:00:00:33:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])

                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src=src_mac ,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(
                                        eth_dst=dmac1,
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=63)

                self.ctc_send_packet(3, str(pkt))
                self.ctc_verify_any_packet_any_port( [exp_pkt], [4, 5]) 

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_lag_member(self.client, lag_member_id5)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            sai_thrift_remove_lag(self.client, lag_id1)
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)


class scenario_12_lag_bind_subif_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '20.20.20.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2= '00:11:22:33:44:66'

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        lag_id2 = sai_thrift_create_lag(self.client)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id2, port4)
        lag_member_id5 = sai_thrift_create_lag_member(self.client, lag_id2, port5)
        lag_member_id6 = sai_thrift_create_lag_member(self.client, lag_id2, port6)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, lag_id2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id1)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2) 

        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)

        try:
            max_itrs = 3
            src_mac_start = '00:00:00:00:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])

                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src=src_mac ,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(
                                        eth_dst=dmac1,
                                        eth_src=router_mac,
                                        dl_vlan_enable=True,
                                        vlan_vid=10,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=63)

                self.ctc_send_packet(i+3, str(pkt))
                self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2]) 

            max_itrs = 3
            src_mac_start = '00:00:00:00:33:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])

                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src=src_mac ,
                                        dl_vlan_enable=True,
                                        vlan_vid=10,
                                        ip_dst='20.20.20.1',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(
                                        eth_dst=dmac2,
                                        eth_src=router_mac,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        ip_dst='20.20.20.1',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=63)

                self.ctc_send_packet(i, str(pkt))
                self.ctc_verify_any_packet_any_port( [exp_pkt], [3, 4, 5])

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag(self.client, lag_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            sai_thrift_remove_lag_member(self.client, lag_member_id5)
            sai_thrift_remove_lag_member(self.client, lag_member_id6)
            sai_thrift_remove_lag(self.client, lag_id2)
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)


class scenario_13_lag_bind_subif_add_and_remove_member_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port5 = port_list[4]
        port6 = port_list[5]
        v4_enabled = 1
        v6_enabled = 1
        vlan_id = 10
        vlan_id1 = 20
        mac = ''
        mac1 = '00:00:00:01:01:01'
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '20.20.20.1'
        ip_addr3 = '30.30.30.1'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2= '00:11:22:33:44:66'
        dmac3= '00:11:22:33:44:77'

        lag_id1 = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        #lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        lag_id2 = sai_thrift_create_lag(self.client)
        lag_member_id4 = sai_thrift_create_lag_member(self.client, lag_id2, port4)
        lag_member_id5 = sai_thrift_create_lag_member(self.client, lag_id2, port5)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, lag_id2, 0, v4_enabled, v6_enabled, mac, outer_vlan_id = vlan_id1)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_SUB_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac1, outer_vlan_id = vlan_id1)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1) 
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)

        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_addr3, dmac3)

        hash_id_lag = 0x201C
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST, value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)

        try:
            lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
            max_itrs = 3
            src_mac_start = '00:00:00:00:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])

                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src=src_mac ,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(
                                        eth_dst=dmac1,
                                        eth_src=router_mac,
                                        dl_vlan_enable=True,
                                        vlan_vid=10,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=63)
                pkt1 = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src=src_mac ,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        ip_dst='30.30.30.1',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt1 = simple_tcp_packet(
                                        eth_dst=dmac3,
                                        eth_src=mac1,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        ip_dst='30.30.30.1',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=63)

                self.ctc_send_packet(i%2+3, str(pkt))
                self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2]) 
                self.ctc_send_packet(i%2+3, str(pkt1))
                self.ctc_verify_any_packet_any_port( [exp_pkt1], [0, 1, 2]) 

            max_itrs = 3
            src_mac_start = '00:00:00:00:33:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])

                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src=src_mac ,
                                        dl_vlan_enable=True,
                                        vlan_vid=10,
                                        ip_dst='20.20.20.1',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(
                                        eth_dst=dmac2,
                                        eth_src=router_mac,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        ip_dst='20.20.20.1',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=63)
                pkt1 = simple_tcp_packet(eth_dst=mac1,
                                        eth_src=src_mac ,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        ip_dst='20.20.20.1',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt1 = simple_tcp_packet(
                                        eth_dst=dmac2,
                                        eth_src=router_mac,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        ip_dst='20.20.20.1',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=63)

                self.ctc_send_packet(i, str(pkt))
                self.ctc_verify_any_packet_any_port( [exp_pkt], [3, 4])
                self.ctc_send_packet(i, str(pkt1))
                self.ctc_verify_any_packet_any_port( [exp_pkt1], [3, 4])

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            max_itrs = 2
            src_mac_start = '00:00:00:00:22:{0}'
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])

                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src=src_mac ,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt = simple_tcp_packet(
                                        eth_dst=dmac1,
                                        eth_src=router_mac,
                                        dl_vlan_enable=True,
                                        vlan_vid=10,
                                        ip_dst='10.10.10.10',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=63)
                pkt1 = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src=src_mac ,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        ip_dst='30.30.30.1',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=64)
                exp_pkt1 = simple_tcp_packet(
                                        eth_dst=dmac3,
                                        eth_src=mac1,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        ip_dst='30.30.30.1',
                                        ip_src='192.168.0.1',
                                        ip_id=105,
                                        ip_ttl=63)

                self.ctc_send_packet(i%2+3, str(pkt))
                self.ctc_verify_any_packet_any_port( [exp_pkt], [1, 2]) 
                self.ctc_send_packet(i%2+3, str(pkt1))
                self.ctc_verify_any_packet_any_port( [exp_pkt1], [1, 2]) 

        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_addr3, dmac3)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag(self.client, lag_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id4)
            sai_thrift_remove_lag_member(self.client, lag_member_id5)
            sai_thrift_remove_lag(self.client, lag_id2)
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)


