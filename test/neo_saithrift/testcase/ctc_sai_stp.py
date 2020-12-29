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
Thrift SAI STP interface tests
"""
import socket
from switch import *
import sai_base_test
import pdb
import time
from scapy.config import *
from scapy.layers.all import *


stp_attr = ['SAI_STP_ATTR_VLAN_LIST',
            'SAI_STP_ATTR_BRIDGE_ID',
            'SAI_STP_ATTR_PORT_LIST']

stp_port_attr = ['SAI_STP_PORT_ATTR_STP',
                 'SAI_STP_PORT_ATTR_BRIDGE_PORT',
                 'SAI_STP_PORT_ATTR_STATE']


def _get_default_stp_instance(client):
    ids_list = [SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID]
    switch_attr_list = client.sai_thrift_get_switch_attribute(ids_list)
    for attribute in switch_attr_list.attr_list:
        if attribute.id == SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID:
            sys_logging("### SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID = 0x%09x ###" %attribute.value.oid)
            return attribute.value.oid


@group('L2')
class func_01_create_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_01_create_stp_fn----- ###")
        switch_init(self.client)

        default_stp_oid = _get_default_stp_instance(self.client)

        stp_oid = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid = 0x%x ###" %stp_oid)

        warmboot(self.client)

        try:
            assert((SAI_NULL_OBJECT_ID != stp_oid) and (default_stp_oid != stp_oid))

        finally:
            self.client.sai_thrift_remove_stp_entry(stp_oid)


@group('L2')
class func_02_create_same_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_02_create_same_stp_fn----- ###")
        switch_init(self.client)

        default_stp_oid = _get_default_stp_instance(self.client)

        stp_oid1 = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid = 0x%x ###" %stp_oid1)
        stp_oid2 = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid = 0x%x ###" %stp_oid2)

        warmboot(self.client)

        try:
            assert((SAI_NULL_OBJECT_ID != stp_oid1) and (SAI_NULL_OBJECT_ID != stp_oid2) and (stp_oid2 != stp_oid1))

        finally:
            self.client.sai_thrift_remove_stp_entry(stp_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid2)


@group('L2')
class func_03_create_max_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_03_create_max_stp_fn----- ###")
        switch_init(self.client)

        ids_list = [SAI_SWITCH_ATTR_MAX_STP_INSTANCE]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        for attribute in switch_attr_list.attr_list:
            if attribute.id == SAI_SWITCH_ATTR_MAX_STP_INSTANCE:
                sys_logging("### SAI_SWITCH_ATTR_MAX_STP_INSTANCE = %d ###" %attribute.value.u32)
                max_stp = attribute.value.u32

        stp_oid = [0 for i in range(0,max_stp+1)]

        for a in range(1,max_stp):
            stp_oid[a] = sai_thrift_create_stp_entry(self.client)
            sys_logging("### stp_oid_%d = 0x%x ###" %(a,stp_oid[a]))

        warmboot(self.client)

        try:
            sys_logging("### create stp_id = 128 and failed ###")
            stp_oid[max_stp] = sai_thrift_create_stp_entry(self.client)
            sys_logging("### stp_oid_128 = 0x%x ###" %stp_oid[max_stp])
            assert(stp_oid[max_stp] == SAI_NULL_OBJECT_ID)

        finally:
            for a in range(1,max_stp+1):
                sys_logging("### remove stp_oid_%d = 0x%x ###" %(a,stp_oid[a]))
                self.client.sai_thrift_remove_stp_entry(stp_oid[a])


@group('L2')
class func_04_remove_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112321
        '''
        sys_logging("### -----func_04_remove_stp_fn----- ###")
        switch_init(self.client)

        vlan_id = 100
        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        stp_oid1 = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid1 = 0x%x ###" %stp_oid1)
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        stp_oid2 = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid2 = 0x%x ###" %stp_oid2)
        state = SAI_STP_PORT_STATE_BLOCKING
        sys_logging("### create stp port with common port at state: SAI_STP_PORT_STATE_BLOCKING ###")
        stp_port_id1 = sai_thrift_create_stp_port(self.client, stp_oid2, port1, state)
        sys_logging("### stp_port_oid1 = 0x%x ###" %stp_port_id1)

        stp_oid3 = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid2 = 0x%x ###" %stp_oid3)
        lag_oid = sai_thrift_create_lag(self.client)
        sys_logging("### lag_oid = 0x%x ###" %lag_oid)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port3)
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)
        is_lag = True
        sys_logging("### create stp port with lag port at state: SAI_STP_PORT_STATE_BLOCKING ###")
        stp_port_id2 = sai_thrift_create_stp_port(self.client, stp_oid3, lag_bridge_oid, state, is_lag)
        sys_logging("### stp_port_oid2 = 0x%x ###" %stp_port_id2)

        warmboot(self.client)

        try:
            status = self.client.sai_thrift_remove_stp_entry(stp_oid1)
            sys_logging("### remove stp_oid1, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

            status = self.client.sai_thrift_remove_stp_entry(stp_oid2)
            sys_logging("### remove stp_oid2, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

            status = self.client.sai_thrift_remove_stp_entry(stp_oid3)
            sys_logging("### remove stp_oid3, status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

        finally:
            self.client.sai_thrift_remove_stp_port(stp_port_id1)
            self.client.sai_thrift_remove_stp_port(stp_port_id2)
            self.client.sai_thrift_remove_bridge_port(lag_bridge_oid)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            self.client.sai_thrift_remove_lag(lag_oid)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid2)
            self.client.sai_thrift_remove_stp_entry(stp_oid3)


@group('L2')
class func_05_remove_not_exist_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_05_remove_not_exist_stp_fn----- ###")
        switch_init(self.client)

        no_exist_stp_oid = 4294967313

        warmboot(self.client)

        try:
            sys_logging("### remove not exist stp_oid = 0x%x ###" %no_exist_stp_oid)
            status = self.client.sai_thrift_remove_stp_entry(no_exist_stp_oid)
            assert(status != SAI_STATUS_SUCCESS)

        finally:
            sys_logging("### remove stp_oid, status = 0x%x ###" %status)


@group('L2')
class func_06_set_and_get_stp_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112301
        '''
        sys_logging("### -----func_06_set_and_get_stp_attribute_fn----- ###")
        switch_init(self.client)

        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        sys_logging("### default_1q_bridge_oid = 0x%x ###" %default_1q_bridge)

        stp_oid = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid = 0x%x ###" %stp_oid)
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)
        port1 = port_list[1]

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_stp_attribute(stp_oid)
            for a in attrs.attr_list:
                if a.id == SAI_STP_ATTR_BRIDGE_ID:
                    sys_logging("### SAI_STP_ATTR_BRIDGE_ID = 0x%x ###" %a.value.oid)
                    assert(default_1q_bridge == a.value.oid)
                if a.id == SAI_STP_ATTR_VLAN_LIST:
                    sys_logging("### SAI_STP_ATTR_VLAN_LIST count = %d ###" %a.value.vlanlist.vlan_count)
                    assert(0 == a.value.vlanlist.vlan_count)
                    for b in a.value.vlanlist.vlan_list:
                        sys_logging("### SAI_STP_ATTR_VLAN_LIST list: %d ###" %b)
                if a.id == SAI_STP_ATTR_PORT_LIST:
                    sys_logging("### SAI_STP_ATTR_PORT_LIST count = %d ###" %a.value.objlist.count)
                    assert(0 == a.value.objlist.count)
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_STP_ATTR_PORT_LIST list: 0x%x ###" %b)

            attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_STP_INSTANCE of vlan %d ###" %vlan_id)

            state = SAI_STP_PORT_STATE_BLOCKING
            stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)
            sys_logging("### stp_port_oid = 0x%x ###" %stp_port_id)

            attrs = self.client.sai_thrift_get_stp_attribute(stp_oid)
            for a in attrs.attr_list:
                if a.id == SAI_STP_ATTR_BRIDGE_ID:
                    sys_logging("### SAI_STP_ATTR_BRIDGE_ID = 0x%x ###" %a.value.oid)
                    assert(default_1q_bridge == a.value.oid)
                if a.id == SAI_STP_ATTR_VLAN_LIST:
                    sys_logging("### SAI_STP_ATTR_VLAN_LIST count = %d ###" %a.value.vlanlist.vlan_count)
                    assert(1 == a.value.vlanlist.vlan_count)
                    for b in a.value.vlanlist.vlan_list:
                        sys_logging("### SAI_STP_ATTR_VLAN_LIST list: %d ###" %b)
                        assert(vlan_id == b)
                if a.id == SAI_STP_ATTR_PORT_LIST:
                    sys_logging("### SAI_STP_ATTR_PORT_LIST count = %d ###" %a.value.objlist.count)
                    assert(1 == a.value.objlist.count)
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_STP_ATTR_PORT_LIST list: 0x%x ###" %b)
                        assert(stp_port_id == b)

        finally:
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)


@group('L2')
class func_07_create_stp_port_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_07_create_stp_port_fn_0----- ###")
        switch_init(self.client)

        vlan_id = 100
        port1 = port_list[1]
        port2 = port_list[2]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member1 = 0x%x ###" %vlan_member1)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member2 = 0x%x ###" %vlan_member2)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2)

        stp_oid = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid = 0x%x ###" %stp_oid)

        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            sys_logging("### create stp port at state: SAI_STP_PORT_STATE_LEARNING ###")
            state = SAI_STP_PORT_STATE_LEARNING
            stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)
            sys_logging("### stp_port_oid = 0x%x ###" %stp_port_id)
            assert(SAI_NULL_OBJECT_ID != stp_port_id)

            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1))

            sys_logging("### stp port state is learning, packet should be discarded ###")
            self.ctc_send_packet(1, str(pkt))
            self.ctc_verify_no_packet(pkt, 2)

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1))

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)


@group('L2')
class func_07_create_stp_port_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_07_create_stp_port_fn_1----- ###")
        switch_init(self.client)

        vlan_id = 100
        port1 = port_list[1]
        port2 = port_list[2]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member1 = 0x%x ###" %vlan_member1)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member2 = 0x%x ###" %vlan_member2)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2)

        stp_oid = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid = 0x%x ###" %stp_oid)

        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            sys_logging("### create stp port at state: SAI_STP_PORT_STATE_FORWARDING ###")
            state = SAI_STP_PORT_STATE_FORWARDING
            stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)
            sys_logging("### stp_port_oid = 0x%x ###" %stp_port_id)
            assert(SAI_NULL_OBJECT_ID != stp_port_id)

            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1))

            sys_logging("### stp port state is forwarding, packet should be forwarded ###")
            self.ctc_send_packet(1, pkt)
            self.ctc_verify_packet(pkt, 2)

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1))

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)


@group('L2')
class func_07_create_stp_port_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_07_create_stp_port_fn_2----- ###")
        switch_init(self.client)

        vlan_id = 100
        port1 = port_list[1]
        port2 = port_list[2]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member1 = 0x%x ###" %vlan_member1)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member2 = 0x%x ###" %vlan_member2)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2)

        stp_oid = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid = 0x%x ###" %stp_oid)

        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            sys_logging("### create stp port at state: SAI_STP_PORT_STATE_BLOCKING ###")
            state = SAI_STP_PORT_STATE_BLOCKING
            stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)
            sys_logging("### stp_port_oid = 0x%x ###" %stp_port_id)
            assert(SAI_NULL_OBJECT_ID != stp_port_id)

            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1))

            sys_logging("### stp port state is blocking, packet should be discarded ###")
            self.ctc_send_packet(1, pkt)
            self.ctc_verify_no_packet(pkt, 2)

            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid, mac1))

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)


@group('L2')
class func_08_remove_stp_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_08_remove_stp_port_fn----- ###")
        switch_init(self.client)

        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2)

        stp_oid = sai_thrift_create_stp_entry(self.client)

        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr) 

        state = SAI_STP_PORT_STATE_BLOCKING
        stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            sys_logging("### stp port state is blocking, packet should be discarded ###")
            self.ctc_send_packet(0, pkt)
            self.ctc_verify_no_packet(pkt, 1)

            sys_logging("### remove stp port, and packet should be forwarded ###")
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.ctc_send_packet(0, pkt)
            self.ctc_verify_packet(pkt, 1)

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)


@group('L2')
class func_09_set_and_get_stp_port_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_09_set_and_get_stp_port_attribute_fn----- ###")
        switch_init(self.client)

        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### bport_oid1 = 0x%x ###" %bport_oid)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2)

        stp_oid = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid = 0x%x ###" %stp_oid)
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        sys_logging("### create stp port at state: SAI_STP_PORT_STATE_BLOCKING ###")
        state = SAI_STP_PORT_STATE_BLOCKING
        stp_port_id = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64)

        warmboot(self.client)

        try:
            sys_logging("### get attributes of stp port ###")
            attrs = self.client.sai_thrift_get_stp_port_attribute(stp_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_STP_PORT_ATTR_STP:
                    sys_logging("### SAI_STP_PORT_ATTR_STP = 0x%x ###" %a.value.oid)
                    assert(stp_oid == a.value.oid)
                if a.id == SAI_STP_PORT_ATTR_BRIDGE_PORT:
                    sys_logging("### SAI_STP_PORT_ATTR_BRIDGE_PORT = 0x%x ###" %a.value.oid)
                    assert(bport_oid == a.value.oid)
                if a.id == SAI_STP_PORT_ATTR_STATE:
                    sys_logging("### SAI_STP_PORT_ATTR_STATE = %d ###" %a.value.s32)
                    assert(SAI_STP_PORT_STATE_BLOCKING == a.value.s32)

            sys_logging("### stp port state is blocking, packet should be discarded ###")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 1)

            sys_logging("### change the state of stp port to forwarding ###")
            state = SAI_STP_PORT_STATE_FORWARDING
            self.client.sai_thrift_set_stp_port_state(stp_port_id, port1, state)

            sys_logging("### get attributes of stp port ###")
            attrs = self.client.sai_thrift_get_stp_port_attribute(stp_port_id)
            for a in attrs.attr_list:
                if a.id == SAI_STP_PORT_ATTR_STP:
                    sys_logging("### SAI_STP_PORT_ATTR_STP = 0x%x ###" %a.value.oid)
                    assert(stp_oid == a.value.oid)
                if a.id == SAI_STP_PORT_ATTR_BRIDGE_PORT:
                    sys_logging("### SAI_STP_PORT_ATTR_BRIDGE_PORT = 0x%x ###" %a.value.oid)
                    assert(bport_oid == a.value.oid)
                if a.id == SAI_STP_PORT_ATTR_STATE:
                    sys_logging("### SAI_STP_PORT_ATTR_STATE = %d ###" %a.value.s32)
                    assert(SAI_STP_PORT_STATE_FORWARDING == a.value.s32)

            sys_logging("### stp port state is forwarding, packet should be forwarded ###")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packet(pkt, 1)

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_stp_entry(stp_oid)


@group('L2')
class func_10_create_and_remove_stp_ports_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_10_create_and_remove_stp_ports_fn----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        stp_oid1 = sai_thrift_create_stp_entry(self.client)

        vlan_id1 = 100
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port4, SAI_VLAN_TAGGING_MODE_TAGGED)

        stp_oid_list = [stp_oid1, stp_oid1, stp_oid1, stp_oid1]
        port_oid_list = [port1, port2, port3, port4]
        state_list = [SAI_STP_PORT_STATE_LEARNING, SAI_STP_PORT_STATE_FORWARDING,
                      SAI_STP_PORT_STATE_BLOCKING, SAI_STP_PORT_STATE_FORWARDING]

        sys_logging("### create 4 stp ports ###")
        results =  sai_thrift_create_stp_ports(self.client, stp_oid_list, port_oid_list, state_list,
                                               4, SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR)
        object_id_list = results[0]
        statuslist = results[1]

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=100,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            sys_logging("### step 1: check obj-id and status of 4 stp ports ###")
            for object_id in object_id_list:
                assert(SAI_NULL_OBJECT_ID != object_id)
            for status in statuslist:
                assert(SAI_STATUS_SUCCESS == status)

            sys_logging("### step 2: send packet verify ###") 
            sys_logging("### send packet to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)
            self.ctc_verify_no_packet(pkt1, 3)

            sys_logging("### send packet to port 2 ###")
            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_no_packet(pkt1, 0)
            self.ctc_verify_no_packet(pkt1, 2)
            self.ctc_verify_packet(pkt1, 3)

            sys_logging("### send packet to port 3 ###")
            self.ctc_send_packet(2, pkt1)
            self.ctc_verify_no_packet(pkt1, 0)
            self.ctc_verify_no_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 3)

            sys_logging("### send packet to port 4 ###")
            self.ctc_send_packet(3, pkt1)
            self.ctc_verify_no_packet(pkt1, 0)
            self.ctc_verify_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)

            sys_logging("### step3: remove 4 stp ports ###")
            statuslist = sai_thrift_remove_stp_ports(self.client, object_id_list, SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR)
            for status in statuslist:
                assert(SAI_STATUS_SUCCESS == status)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid1)


@group('L2')
class func_10_create_and_remove_stp_ports_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_10_create_and_remove_stp_ports_fn_0----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        stp_oid1 = sai_thrift_create_stp_entry(self.client)

        vlan_id1 = 100
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port4, SAI_VLAN_TAGGING_MODE_TAGGED)

        stp_oid_list = [stp_oid1, stp_oid1, stp_oid1, stp_oid1]
        port_oid_list = [port_list[0], port_list[1], port_list[2], port_list[3]]
        state_list = [0, 1, 4, 2]

        sys_logging("### create 4 stp ports at mode 0 and 3rd is failed ###")
        results =  sai_thrift_create_stp_ports(self.client, stp_oid_list, port_oid_list, state_list,
                                               4, SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR)
        object_id_list = results[0]
        statuslist = results[1]

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=100,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            sys_logging("### step1: check 4 stp ports obj-id and status ###")
            assert(object_id_list[0] != SAI_NULL_OBJECT_ID)
            assert(object_id_list[1] != SAI_NULL_OBJECT_ID)
            assert(object_id_list[2] == SAI_NULL_OBJECT_ID)
            assert(object_id_list[3] == SAI_NULL_OBJECT_ID)

            assert(statuslist[0] == SAI_STATUS_SUCCESS)
            assert(statuslist[1] == SAI_STATUS_SUCCESS)
            assert(statuslist[2] != SAI_STATUS_SUCCESS)
            assert(statuslist[3] == SAI_STATUS_NOT_EXECUTED)

            sys_logging("### step2: send packet verify ###")
            sys_logging("### send packet to port 1 ###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)
            self.ctc_verify_no_packet(pkt1, 3)

            sys_logging("### send packet to port 2 ###")
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 0)
            self.ctc_verify_packets(pkt1, [2])
            self.ctc_verify_packets(pkt1, [3])

            sys_logging("### send packet to port 3 ###")
            self.ctc_send_packet(2, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 0)
            self.ctc_verify_packets(pkt1, [1])
            self.ctc_verify_packets(pkt1, [3])

            sys_logging("### send packet to port 4 ###")
            self.ctc_send_packet(3, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 0)
            self.ctc_verify_packets(pkt1, [1])
            self.ctc_verify_packets(pkt1, [2])

            sys_logging("### step3: remove 4 stp ports ###")
            statuslist = sai_thrift_remove_stp_ports(self.client, object_id_list, SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR)
            assert(statuslist[0] == SAI_STATUS_SUCCESS)
            assert(statuslist[1] == SAI_STATUS_SUCCESS)
            assert(statuslist[2] == SAI_STATUS_INVALID_OBJECT_ID)
            assert(statuslist[3] == SAI_STATUS_NOT_EXECUTED)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid1)


@group('L2')
class func_10_create_and_remove_stp_ports_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_10_create_and_remove_stp_ports_fn_1----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        stp_oid1 = sai_thrift_create_stp_entry(self.client)

        vlan_id1 = 100
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr) 
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port4, SAI_VLAN_TAGGING_MODE_TAGGED)

        stp_oid_list = [stp_oid1, stp_oid1, stp_oid1, stp_oid1]
        port_oid_list = [port_list[0], port_list[1], port_list[2], port_list[3]]
        state_list = [0, 1, 4, 2]

        sys_logging("### create 4 stp ports at mode 1 and 3rd is failed ###")
        results =  sai_thrift_create_stp_ports(self.client, stp_oid_list, port_oid_list, state_list,
                                               4, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR)
        object_id_list = results[0]
        statuslist = results[1]

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=100,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            sys_logging("### step1: check 4 stp ports obj-id and status ###")
            assert(object_id_list[0] != SAI_NULL_OBJECT_ID)
            assert(object_id_list[1] != SAI_NULL_OBJECT_ID)
            assert(object_id_list[2] == SAI_NULL_OBJECT_ID)
            assert(object_id_list[3] != SAI_NULL_OBJECT_ID)

            assert(statuslist[0] == SAI_STATUS_SUCCESS)
            assert(statuslist[1] == SAI_STATUS_SUCCESS)
            assert(statuslist[2] != SAI_STATUS_SUCCESS)
            assert(statuslist[3] == SAI_STATUS_SUCCESS)

            sys_logging("### step2: send packet verify ###")
            sys_logging("### send packet to port 1 ###")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)
            self.ctc_verify_no_packet(pkt1, 3)

            sys_logging("### send packet to port 2 ###")
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 0)
            self.ctc_verify_packets(pkt1, [2])
            self.ctc_verify_no_packet(pkt1, 3)

            sys_logging("### send packet to port 3 ###")
            self.ctc_send_packet(2, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 0)
            self.ctc_verify_packets(pkt1, [1])
            self.ctc_verify_no_packet(pkt1, 3)

            sys_logging("### send packet to port 4 ###")
            self.ctc_send_packet(3, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 0)
            self.ctc_verify_no_packet(pkt1, 1)
            self.ctc_verify_no_packet(pkt1, 2)

            sys_logging("### step3: remove 4 stp ports ###")
            statuslist = sai_thrift_remove_stp_ports(self.client, object_id_list, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR)
            assert(statuslist[0] == SAI_STATUS_SUCCESS)
            assert(statuslist[1] == SAI_STATUS_SUCCESS)
            assert(statuslist[2] == SAI_STATUS_INVALID_OBJECT_ID)
            assert(statuslist[3] == SAI_STATUS_SUCCESS)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2) 
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid1)


@group('L2')
class func_11_create_same_stp_port_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112651
        '''
        sys_logging("### -----func_11_create_same_stp_port_fn----- ###")
        switch_init(self.client)

        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]

        stp_oid = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid = 0x%x ###" %stp_oid)

        lag_oid = sai_thrift_create_lag(self.client)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port3)
        #pdb.set_trace()
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)
        sys_logging("### lag_bridge_port_oid = 0x%x ###" %lag_bridge_oid)

        warmboot(self.client)

        try:
            sys_logging("### create stp port with normal bridge port ###")
            state = SAI_STP_PORT_STATE_LEARNING
            stp_port_id1 = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)
            sys_logging("### stp_port_oid1 = 0x%x ###" %stp_port_id1)
            assert(SAI_NULL_OBJECT_ID != stp_port_id1)

            state = SAI_STP_PORT_STATE_FORWARDING
            stp_port_id2 = sai_thrift_create_stp_port(self.client, stp_oid, port1, state)
            sys_logging("### stp_port_oid2 = 0x%x ###" %stp_port_id2)
            assert(SAI_NULL_OBJECT_ID == stp_port_id2)

            stp_attr_list = self.client.sai_thrift_get_stp_attribute(stp_oid)
            for attr in stp_attr_list.attr_list:
                if attr.id == SAI_STP_ATTR_PORT_LIST:
                    sys_logging("### SAI_STP_ATTR_PORT_LIST count = %d ###" %attr.value.objlist.count)
                    assert(1 == attr.value.objlist.count)
                    for stp_port in attr.value.objlist.object_id_list:
                        sys_logging("### SAI_STP_ATTR_PORT_LIST list: 0x%x ###" %stp_port)

            attrs = self.client.sai_thrift_get_stp_port_attribute(stp_port_id1)
            for a in attrs.attr_list:
                if a.id == SAI_STP_PORT_ATTR_STP:
                    sys_logging("### SAI_STP_PORT_ATTR_STP = 0x%x ###" %a.value.oid)
                if a.id == SAI_STP_PORT_ATTR_BRIDGE_PORT:
                    sys_logging("### SAI_STP_PORT_ATTR_BRIDGE_PORT = 0x%x ###" %a.value.oid)
                if a.id == SAI_STP_PORT_ATTR_STATE:
                    sys_logging("### SAI_STP_PORT_ATTR_STATE = %d ###" %a.value.s32)
                    assert(SAI_STP_PORT_STATE_LEARNING == a.value.s32)

            sys_logging("### create stp port with lag bridge port ###")
            state = SAI_STP_PORT_STATE_FORWARDING
            is_lag = True
            stp_port_id3 = sai_thrift_create_stp_port(self.client, stp_oid, lag_bridge_oid, state, is_lag)
            sys_logging("### stp_port_oid3 = 0x%x ###" %stp_port_id3)
            assert(SAI_NULL_OBJECT_ID != stp_port_id3)

            state = SAI_STP_PORT_STATE_BLOCKING
            stp_port_id4 = sai_thrift_create_stp_port(self.client, stp_oid, lag_bridge_oid, state, is_lag)
            sys_logging("### stp_port_oid4 = 0x%x ###" %stp_port_id4)
            assert(SAI_NULL_OBJECT_ID == stp_port_id4)

            stp_attr_list = self.client.sai_thrift_get_stp_attribute(stp_oid)
            for attr in stp_attr_list.attr_list:
                if attr.id == SAI_STP_ATTR_PORT_LIST:
                    sys_logging("### SAI_STP_ATTR_PORT_LIST count = %d ###" %attr.value.objlist.count)
                    assert(2 == attr.value.objlist.count)
                    for bridge_port in attr.value.objlist.object_id_list:
                        sys_logging("### SAI_STP_ATTR_PORT_LIST list: 0x%x ###" %bridge_port)

            attrs = self.client.sai_thrift_get_stp_port_attribute(stp_port_id3)
            for a in attrs.attr_list:
                if a.id == SAI_STP_PORT_ATTR_STP:
                    sys_logging("### SAI_STP_PORT_ATTR_STP = 0x%x ###" %a.value.oid)
                if a.id == SAI_STP_PORT_ATTR_BRIDGE_PORT:
                    sys_logging("### SAI_STP_PORT_ATTR_BRIDGE_PORT = 0x%x ###" %a.value.oid)
                if a.id == SAI_STP_PORT_ATTR_STATE:
                    sys_logging("### SAI_STP_PORT_ATTR_STATE = %d ###" %a.value.s32)
                    assert(SAI_STP_PORT_STATE_FORWARDING == a.value.s32)

        finally:
            self.client.sai_thrift_remove_stp_port(stp_port_id1)
            #self.client.sai_thrift_remove_stp_port(stp_port_id2)
            self.client.sai_thrift_remove_stp_port(stp_port_id3)
            #self.client.sai_thrift_remove_stp_port(stp_port_id4)
            self.client.sai_thrift_remove_stp_entry(stp_oid)
            self.client.sai_thrift_remove_bridge_port(lag_bridge_oid)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            self.client.sai_thrift_remove_lag(lag_oid)


@group('L2')
class func_12_switch_default_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112329
        '''
        sys_logging("### -----func_12_switch_default_stp_fn----- ###")
        switch_init(self.client)

        default_stp_oid = _get_default_stp_instance(self.client)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_stp_attribute(default_stp_oid)
            for a in attrs.attr_list:
                if a.id == SAI_STP_ATTR_VLAN_LIST:
                    sys_logging("### SAI_STP_ATTR_VLAN_LIST count = %d ###" %a.value.vlanlist.vlan_count)
                    #vlan 1 was created by default and bound to default stp instance
                    assert(1 == a.value.vlanlist.vlan_count)
                    for b in a.value.vlanlist.vlan_list:
                        sys_logging("### SAI_STP_ATTR_VLAN_LIST list: %d ###" %b)

            vlan_id = 100
            vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
            sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

            attrs = self.client.sai_thrift_get_stp_attribute(default_stp_oid)
            for a in attrs.attr_list:
                if a.id == SAI_STP_ATTR_VLAN_LIST:
                    sys_logging("### SAI_STP_ATTR_VLAN_LIST count = %d ###" %a.value.vlanlist.vlan_count)
                    assert(2 == a.value.vlanlist.vlan_count)
                    for b in a.value.vlanlist.vlan_list:
                        sys_logging("### SAI_STP_ATTR_VLAN_LIST list: %d ###" %b)

            sys_logging("### remove default_stp_oid = 0x%x ###" %default_stp_oid)
            status = self.client.sai_thrift_remove_stp_entry(default_stp_oid)
            #default stp instance cannot be removed, but no need to return failure
            assert(SAI_STATUS_SUCCESS == status)

            stp_oid = sai_thrift_create_stp_entry(self.client)
            sys_logging("### stp_oid = 0x%x ###" %stp_oid)
            assert(default_stp_oid != stp_oid)

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)


@group('L2')
class func_13_vlan_change_stp_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112330
        '''
        sys_logging("### -----func_13_vlan_change_stp_fn----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        stp_oid1 = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid1 = 0x%x ###" %stp_oid1)
        stp_oid2 = sai_thrift_create_stp_entry(self.client)
        sys_logging("### stp_oid2 = 0x%x ###" %stp_oid2)

        warmboot(self.client)

        try:
            attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### vlan %d bind to stp_oid1 ###" %vlan_id)

            sys_logging("### get attributes of stp_oid1 ###")
            attrs = self.client.sai_thrift_get_stp_attribute(stp_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_STP_ATTR_VLAN_LIST:
                    sys_logging("### SAI_STP_ATTR_VLAN_LIST count = %d ###" %a.value.vlanlist.vlan_count)
                    assert(1 == a.value.vlanlist.vlan_count)
                    for b in a.value.vlanlist.vlan_list:
                        sys_logging("### SAI_STP_ATTR_VLAN_LIST list: %d ###" %b)

            sys_logging("### get attributes of stp_oid2 ###")
            attrs = self.client.sai_thrift_get_stp_attribute(stp_oid2)
            for a in attrs.attr_list:
                if a.id == SAI_STP_ATTR_VLAN_LIST:
                    sys_logging("### SAI_STP_ATTR_VLAN_LIST count = %d ###" %a.value.vlanlist.vlan_count)
                    assert(0 == a.value.vlanlist.vlan_count)
                    for b in a.value.vlanlist.vlan_list:
                        sys_logging("### SAI_STP_ATTR_VLAN_LIST list: %d ###" %b)

            attr_value = sai_thrift_attribute_value_t(oid=stp_oid2)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### vlan %d bind to stp_oid2 ###" %vlan_id)

            sys_logging("### get attributes of stp_oid1 ###")
            attrs = self.client.sai_thrift_get_stp_attribute(stp_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_STP_ATTR_VLAN_LIST:
                    sys_logging("### SAI_STP_ATTR_VLAN_LIST count = %d ###" %a.value.vlanlist.vlan_count)
                    assert(0 == a.value.vlanlist.vlan_count)
                    for b in a.value.vlanlist.vlan_list:
                        sys_logging("### SAI_STP_ATTR_VLAN_LIST list: %d ###" %b)

            sys_logging("### get attributes of stp_oid2 ###")
            attrs = self.client.sai_thrift_get_stp_attribute(stp_oid2)
            for a in attrs.attr_list:
                if a.id == SAI_STP_ATTR_VLAN_LIST:
                    sys_logging("### SAI_STP_ATTR_VLAN_LIST count = %d ###" %a.value.vlanlist.vlan_count)
                    assert(1 == a.value.vlanlist.vlan_count)
                    for b in a.value.vlanlist.vlan_list:
                        sys_logging("### SAI_STP_ATTR_VLAN_LIST list: %d ###" %b)

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid2)


@group('L2')
class scenario_01_stp_rstp_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_01_stp_rstp_port----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        default_stp_oid = _get_default_stp_instance(self.client)
        attr_value = sai_thrift_attribute_value_t(oid=default_stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)
        sys_logging("### vlan 10 bind to stp instance 0 ###")
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)
        sys_logging("### vlan 20 bind to stp instance 0 ###")

        state = SAI_STP_PORT_STATE_LEARNING
        stp_port_id = sai_thrift_create_stp_port(self.client, default_stp_oid, port1, state)
        sys_logging("********************************************")
        sys_logging("* stp port  port  stp instance    state    *")
        sys_logging("* --------  ----  ------------  ---------- *")
        sys_logging("*    1       1          0        LEARNING  *")
        sys_logging("********************************************")

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:01', eth_src='00:00:00:00:00:02',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:01', eth_src='00:00:00:00:00:02',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid2, mac1))

            sys_logging("### ---send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 1)
            sys_logging("### ---send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_no_packet(pkt2, 1)

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_oid1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_oid2, mac1))

            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt3)
            self.ctc_verify_no_packet(pkt3, 0)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt4)
            self.ctc_verify_no_packet(pkt4, 0)

            state = SAI_STP_PORT_STATE_FORWARDING
            self.client.sai_thrift_set_stp_port_state(stp_port_id, port1, state)
            sys_logging("********************************************")
            sys_logging("* stp port  port  stp instance    state    *")
            sys_logging("* --------  ----  ------------  ---------- *")
            sys_logging("*    1       1          0       FORWARDING *")
            sys_logging("********************************************")

            sys_logging("### send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            sys_logging("### send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)
            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt3)
            self.ctc_verify_packet(pkt3, 0)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt4)
            self.ctc_verify_packet(pkt4, 0)

            state = SAI_STP_PORT_STATE_BLOCKING
            self.client.sai_thrift_set_stp_port_state(stp_port_id, port1, state)
            sys_logging("********************************************")
            sys_logging("* stp port  port  stp instance    state    *")
            sys_logging("* --------  ----  ------------  ---------- *")
            sys_logging("*    1       1          0        BLOCKING  *")
            sys_logging("********************************************")

            sys_logging("### send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 1)
            sys_logging("### send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_no_packet(pkt2, 1)
            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt3)
            self.ctc_verify_no_packet(pkt3, 0)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt4)
            self.ctc_verify_no_packet(pkt4, 0)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


@group('L2')
class scenario_02_stp_rstp_lag(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_02_stp_rstp_lag----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        lag_oid = sai_thrift_create_lag(self.client)
        sys_logging("### lag_oid = 0x%x ###" %lag_oid)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        sys_logging("### lag_member_oid1 = 0x%x ###" %lag_member_id1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
        sys_logging("### lag_member_oid2 = 0x%x ###" %lag_member_id2)
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)
        sys_logging("### lag_bridge_port_oid = 0x%x ###" %lag_bridge_oid)

        vlan_id1 = 10
        vlan_id2 = 20
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        is_lag = True
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, lag_bridge_oid,
                                                     SAI_VLAN_TAGGING_MODE_TAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, lag_bridge_oid,
                                                     SAI_VLAN_TAGGING_MODE_TAGGED, is_lag)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        default_stp_oid = _get_default_stp_instance(self.client)
        attr_value = sai_thrift_attribute_value_t(oid=default_stp_oid)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)
        sys_logging("### vlan 10 bind to stp instance 0 ###")
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)
        sys_logging("### vlan 20 bind to stp instance 0 ###")

        state = SAI_STP_PORT_STATE_LEARNING
        stp_port_id = sai_thrift_create_stp_port(self.client, default_stp_oid, lag_bridge_oid, state, is_lag)
        sys_logging("********************************************")
        sys_logging("* stp port  port  stp instance    state    *")
        sys_logging("* --------  ----  ------------  ---------- *")
        sys_logging("*    1      1,2         0        LEARNING  *")
        sys_logging("********************************************")

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:01', eth_src='00:00:00:00:00:02',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:01', eth_src='00:00:00:00:00:02',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        warmboot(self.client)

        try:
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid2, mac1))

            sys_logging("### send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_no_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_no_packet(pkt2, 2)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_no_packet(pkt2, 2)

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_oid1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_oid2, mac1))

            sys_logging("### send packet tagged with vlan 10 to port 3 ###")
            self.ctc_send_packet(2, pkt3)
            self.ctc_verify_no_packet_any(pkt3, [0,1])
            sys_logging("### send packet tagged with vlan 20 to port 3 ###")
            self.ctc_send_packet(2, pkt4)
            self.ctc_verify_no_packet_any(pkt4, [0,1])

            state = SAI_STP_PORT_STATE_FORWARDING
            self.client.sai_thrift_set_stp_port_state(stp_port_id, port1, state)
            sys_logging("********************************************")
            sys_logging("* stp port  port  stp instance    state    *")
            sys_logging("* --------  ----  ------------  ---------- *")
            sys_logging("*    1      1,2         0       FORWARDING *")
            sys_logging("********************************************")

            sys_logging("### send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 2)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packet(pkt2, 2)

            sys_logging("### send packet tagged with vlan 10 to port 3 ###")
            self.ctc_send_packet(2, pkt3)
            self.ctc_verify_packet_any_port(pkt3, [0,1])
            sys_logging("### send packet tagged with vlan 20 to port 3 ###")
            self.ctc_send_packet(2, pkt4)
            self.ctc_verify_packet_any_port(pkt4, [0,1])

            state = SAI_STP_PORT_STATE_BLOCKING
            self.client.sai_thrift_set_stp_port_state(stp_port_id, port1, state)
            sys_logging("********************************************")
            sys_logging("* stp port  port  stp instance    state    *")
            sys_logging("* --------  ----  ------------  ---------- *")
            sys_logging("*    1      1,2         0        BLOCKING  *")
            sys_logging("********************************************")

            sys_logging("### send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_no_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_no_packet(pkt2, 2)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_no_packet(pkt2, 2)

            sys_logging("### send packet tagged with vlan 10 to port 3 ###")
            self.ctc_send_packet(2, pkt3)
            self.ctc_verify_no_packet_any(pkt3, [0,1])
            sys_logging("### send packet tagged with vlan 20 to port 3 ###")
            self.ctc_send_packet(2, pkt4)
            self.ctc_verify_no_packet_any(pkt4, [0,1])

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_stp_port(stp_port_id)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_bridge_port(lag_bridge_oid)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            self.client.sai_thrift_remove_lag(lag_oid)


@group('L2')
class scenario_03_mstp_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_03_mstp_port----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        stp_oid1 = sai_thrift_create_stp_entry(self.client)
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)
        sys_logging("### vlan 10 bind to stp instance 1 ###")
        stp_oid2 = sai_thrift_create_stp_entry(self.client)
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid2)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)
        sys_logging("### vlan 20 bind to stp instance 2 ###")

        state1 = SAI_STP_PORT_STATE_LEARNING
        state2 = SAI_STP_PORT_STATE_FORWARDING
        stp_port_id1 = sai_thrift_create_stp_port(self.client, stp_oid1, port1, state1)
        stp_port_id2 = sai_thrift_create_stp_port(self.client, stp_oid2, port1, state2)

        sys_logging("********************************************")
        sys_logging("* stp port  port  stp instance    state    *")
        sys_logging("* --------  ----  ------------  ---------- *")
        sys_logging("*    1       1     1(VLAN 10)    LEARNING  *")
        sys_logging("*    2       1     2(VLAN 20)   FORWARDING *")
        sys_logging("********************************************")

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:01', eth_src='00:00:00:00:00:02',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:01', eth_src='00:00:00:00:00:02',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid2, mac1))

            sys_logging("### send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 1)
            sys_logging("### send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_oid1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_oid2, mac1))

            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt3)
            self.ctc_verify_no_packet(pkt3, 0)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt4)
            self.ctc_verify_packet(pkt4, 0)

            self.client.sai_thrift_set_stp_port_state(stp_port_id1, port1, state2)
            sys_logging("********************************************")
            sys_logging("* stp port  port  stp instance    state    *")
            sys_logging("* --------  ----  ------------  ---------- *")
            sys_logging("*    1       1     1(VLAN 10)   FORWARDING *")
            sys_logging("*    2       1     2(VLAN 20)   FORWARDING *")
            sys_logging("********************************************")

            sys_logging("### send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 1)
            sys_logging("### send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)

            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt3)
            self.ctc_verify_packet(pkt3, 0)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt4)
            self.ctc_verify_packet(pkt4, 0)

            state3 = SAI_STP_PORT_STATE_BLOCKING
            self.client.sai_thrift_set_stp_port_state(stp_port_id1, port1, state3)
            sys_logging("********************************************")
            sys_logging("* stp port  port  stp instance    state    *")
            sys_logging("* --------  ----  ------------  ---------- *")
            sys_logging("*    1       1     1(VLAN 10)    BLOCKING  *")
            sys_logging("*    2       1     2(VLAN 20)   FORWARDING *")
            sys_logging("********************************************")

            sys_logging("### send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 1)
            sys_logging("### send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 1)

            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt3)
            self.ctc_verify_no_packet(pkt3, 0)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt4)
            self.ctc_verify_packet(pkt4, 0)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_stp_port(stp_port_id1)
            self.client.sai_thrift_remove_stp_port(stp_port_id2)
            self.client.sai_thrift_remove_stp_entry(stp_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid2)


@group('L2')
class scenario_04_mstp_lag(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_04_mstp_lag----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        lag_oid = sai_thrift_create_lag(self.client)
        sys_logging("### lag_oid = 0x%x ###" %lag_oid)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        sys_logging("### lag_member_oid1 = 0x%x ###" %lag_member_id1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
        sys_logging("### lag_member_oid2 = 0x%x ###" %lag_member_id2)
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)
        sys_logging("### lag_bridge_port_oid = 0x%x ###" %lag_bridge_oid)

        vlan_id1 = 10
        vlan_id2 = 20
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        is_lag = True
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, lag_bridge_oid,
                                                     SAI_VLAN_TAGGING_MODE_TAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port3, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, lag_bridge_oid,
                                                     SAI_VLAN_TAGGING_MODE_TAGGED, is_lag)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port3, SAI_VLAN_TAGGING_MODE_TAGGED)

        stp_oid1 = sai_thrift_create_stp_entry(self.client)
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)
        sys_logging("### vlan 10 bind to stp instance 1 ###")
        stp_oid2 = sai_thrift_create_stp_entry(self.client)
        attr_value = sai_thrift_attribute_value_t(oid=stp_oid2)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)
        sys_logging("### vlan 20 bind to stp instance 2 ###")

        state = SAI_STP_PORT_STATE_LEARNING
        stp_port_id1 = sai_thrift_create_stp_port(self.client, stp_oid1, lag_bridge_oid, state, is_lag)
        state = SAI_STP_PORT_STATE_FORWARDING
        stp_port_id2 = sai_thrift_create_stp_port(self.client, stp_oid2, lag_bridge_oid, state, is_lag)
        sys_logging("********************************************")
        sys_logging("* stp port  port  stp instance    state    *")
        sys_logging("* --------  ----  ------------  ---------- *")
        sys_logging("*    1      1,2    1(VLAN 10)    LEARNING  *")
        sys_logging("*    2      1,2    2(VLAN 20)   FORWARDING *")
        sys_logging("********************************************")

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)
        pkt3 = simple_tcp_packet(eth_dst='00:00:00:00:00:01', eth_src='00:00:00:00:00:02',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=103, ip_ttl=64)
        pkt4 = simple_tcp_packet(eth_dst='00:00:00:00:00:01', eth_src='00:00:00:00:00:02',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=104, ip_ttl=64)

        warmboot(self.client)

        try:
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid1, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client, vlan_oid2, mac1))

            sys_logging("### send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_no_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 2)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packet(pkt2, 2)

            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_oid1, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client, vlan_oid2, mac1))

            sys_logging("### send packet tagged with vlan 10 to port 3 ###")
            self.ctc_send_packet(2, pkt3)
            self.ctc_verify_no_packet_any(pkt3, [0,1])
            sys_logging("### send packet tagged with vlan 20 to port 3 ###")
            self.ctc_send_packet(2, pkt4)
            self.ctc_verify_packet_any_port(pkt4, [0,1])

            state = SAI_STP_PORT_STATE_FORWARDING
            self.client.sai_thrift_set_stp_port_state(stp_port_id1, port1, state)
            sys_logging("********************************************")
            sys_logging("* stp port  port  stp instance    state    *")
            sys_logging("* --------  ----  ------------  ---------- *")
            sys_logging("*    1      1,2    1(VLAN 10)   FORWARDING *")
            sys_logging("*    2      1,2    2(VLAN 20)   FORWARDING *")
            sys_logging("********************************************")

            sys_logging("### send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 2)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packet(pkt2, 2)

            sys_logging("### send packet tagged with vlan 10 to port 3 ###")
            self.ctc_send_packet(2, pkt3)
            self.ctc_verify_packet_any_port(pkt3, [0,1])
            sys_logging("### send packet tagged with vlan 20 to port 3 ###")
            self.ctc_send_packet(2, pkt4)
            self.ctc_verify_packet_any_port(pkt4, [0,1])

            state = SAI_STP_PORT_STATE_BLOCKING
            self.client.sai_thrift_set_stp_port_state(stp_port_id1, port1, state)
            sys_logging("********************************************")
            sys_logging("* stp port  port  stp instance    state    *")
            sys_logging("* --------  ----  ------------  ---------- *")
            sys_logging("*    1      1,2    1(VLAN 10)    BLOCKING  *")
            sys_logging("*    2      1,2    2(VLAN 20)   FORWARDING *")
            sys_logging("********************************************")

            sys_logging("### send packet tagged with vlan 10 to port 1 ###")
            self.ctc_send_packet(0, pkt1)
            self.ctc_verify_no_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 10 to port 2 ###")
            self.ctc_send_packet(1, pkt1)
            self.ctc_verify_no_packet(pkt1, 2)
            sys_logging("### send packet tagged with vlan 20 to port 1 ###")
            self.ctc_send_packet(0, pkt2)
            self.ctc_verify_packet(pkt2, 2)
            sys_logging("### send packet tagged with vlan 20 to port 2 ###")
            self.ctc_send_packet(1, pkt2)
            self.ctc_verify_packet(pkt2, 2)

            sys_logging("### send packet tagged with vlan 10 to port 3 ###")
            self.ctc_send_packet(2, pkt3)
            self.ctc_verify_no_packet_any(pkt3, [0,1])
            sys_logging("### send packet tagged with vlan 20 to port 3 ###")
            self.ctc_send_packet(2, pkt4)
            self.ctc_verify_packet_any_port(pkt4, [0,1])

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_stp_port(stp_port_id1)
            self.client.sai_thrift_remove_stp_port(stp_port_id2)
            self.client.sai_thrift_remove_bridge_port(lag_bridge_oid)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            self.client.sai_thrift_remove_lag(lag_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid1)
            self.client.sai_thrift_remove_stp_entry(stp_oid2)


