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
Thrift SAI VLAN interface tests
"""
import socket
from switch import *
import sai_base_test
import pdb
import time
from scapy.config import *
from scapy.layers.all import *


@group('L2')
class func_01_create_vlan_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_01_create_vlan_fn----- ###")
        switch_init(self.client)

        vlan_id1 = 100
        vlan_id2 = 0
        vlan_id3 = 4095
        vlan_id4 = 4096

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        sys_logging("### create vlan: id = %d, vlan_oid1 = 0x%x ###" %(vlan_id1, vlan_oid1))
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        sys_logging("### create vlan: id = %d, vlan_oid2 = 0x%x ###" %(vlan_id2, vlan_oid2))
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        sys_logging("### create vlan: id = %d, vlan_oid3 = 0x%x ###" %(vlan_id3, vlan_oid3))
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
        sys_logging("### create vlan: id = %d, vlan_oid4 = 0x%x ###" %(vlan_id4, vlan_oid4))

        warmboot(self.client)

        try:
            if vlan_oid1 == SAI_NULL_OBJECT_ID:
                raise NotImplementedError()
            if vlan_oid2 != SAI_NULL_OBJECT_ID:
                raise NotImplementedError()
            if vlan_oid3 == SAI_NULL_OBJECT_ID:
                raise NotImplementedError()
            if vlan_oid4 != SAI_NULL_OBJECT_ID:
                raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)


@group('L2')
class func_02_create_same_vlan_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_02_create_same_vlan_fn----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oid1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oid2)

        warmboot(self.client)

        try:
            if vlan_oid1 == SAI_NULL_OBJECT_ID:
                raise NotImplementedError()
            if vlan_oid2 != SAI_NULL_OBJECT_ID:
                raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


@group('L2')
class func_03_create_max_vlan_with_stats_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_03_create_max_vlan_with_stats_enable----- ###")
        switch_init(self.client)

        vlan_oid = [0 for i in range(0,4096)]

        warmboot(self.client)

        try:
            chipname = testutils.test_params_get()['chipname']

            if chipname == 'tsingma':
                vlan_max = 2048
            elif chipname == 'tsingma_mx':
                vlan_max = 4095
            sys_logging("### vlan_max = %d ###" %vlan_max)

            for a in range(2, vlan_max):
                sys_logging("### create vlan id = %d ###" %a) 
                vlan_oid[a] = sai_thrift_create_vlan(self.client, a)
                sys_logging("### vlan oid = 0x%x ###" %vlan_oid[a])
                assert(SAI_NULL_OBJECT_ID != vlan_oid[a])

            sys_logging("### create vlan id = %d ###" %vlan_max)
            vlan_oid[vlan_max] = sai_thrift_create_vlan(self.client, vlan_max)
            sys_logging("### vlan oid = 0x%x ###" %vlan_oid[vlan_max])
            assert(SAI_NULL_OBJECT_ID == vlan_oid[vlan_max])

        finally:
             for a in range(2, vlan_max):
                sys_logging("### remove vlan id %d ###" %a) 
                self.client.sai_thrift_remove_vlan(vlan_oid[a])


@group('L2')
class func_03_create_max_vlan_with_stats_disable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112283
        '''
        sys_logging("### -----func_03_create_max_vlan_with_stats_disable----- ###")
        switch_init(self.client)

        stats_enable = False
        vlan_oid = [0 for i in range(0,4096)]
        for a in range(2,4095):
            vlan_oid[a] = sai_thrift_create_vlan(self.client, a, stats_enable)
            sys_logging("### create vlan: id = %d, vlan_oid = 0x%x ###" %(a, vlan_oid[a]))

        warmboot(self.client)

        try:
            vlan_oid[4095] = sai_thrift_create_vlan(self.client, 4095, stats_enable)
            sys_logging("### create vlan: id = %d, vlan_oid = 0x%x ###" %(4095, vlan_oid[4095]))
            if vlan_oid[4095] != SAI_NULL_OBJECT_ID:
                raise NotImplementedError()

        finally:
            for a in range(2,4096):
                status = self.client.sai_thrift_remove_vlan(vlan_oid[a])
                sys_logging("### remove vlan: id = %d, status = %d ###" %(a, status))


@group('L2')
class func_04_remove_vlan_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_04_remove_vlan_fn----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        defalut_vlan = switch.default_vlan.oid
        sys_logging("### SAI_SWITCH_ATTR_DEFAULT_VLAN_ID = 0x%x ###" %defalut_vlan)

        warmboot(self.client)

        try:
            status = self.client.sai_thrift_remove_vlan(vlan_oid)
            sys_logging("### status = %d ###" %status)
            assert(SAI_STATUS_SUCCESS == status)

            status = self.client.sai_thrift_remove_vlan(defalut_vlan)
            sys_logging("### status = 0x%x ###" %status)
            #assert(SAI_STATUS_SUCCESS != status)

        finally:
            defalut_vlan = sai_thrift_create_vlan(self.client, 1)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, defalut_vlan, port)


@group('L2')
class func_05_remove_not_exist_vlan_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_05_remove_not_exist_vlan_fn----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        warmboot(self.client)

        try:
            self.client.sai_thrift_remove_vlan(vlan_oid)
            status = self.client.sai_thrift_remove_vlan(vlan_oid)
            assert(status != SAI_STATUS_SUCCESS)

        finally:
            sys_logging("### status = 0x%x ###" %status)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_0----- ###")
        switch_init(self.client)

        vlan_id = 100
        sys_logging("### create vlan: id = %d ###" %vlan_id)
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_VLAN_ID:
                    sys_logging("### SAI_VLAN_ATTR_VLAN_ID = %d ###" %a.value.u16)
                    if vlan_id != a.value.u16:
                        raise NotImplementedError()

            value = 200
            attr_value = sai_thrift_attribute_value_t(u16=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_VLAN_ID, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_VLAN_ID: status = 0x%x ###" %status)
            if status == SAI_STATUS_SUCCESS:
                raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_1----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)
        vlan_member = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member_oid = 0x%x ###" %vlan_member)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(switch.default_vlan.oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_MEMBER_LIST:
                    sys_logging("### SAI_VLAN_ATTR_MEMBER_LIST count = %d ###" %a.value.objlist.count)
                    assert(len(port_list) == a.value.objlist.count)
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_VLAN_ATTR_MEMBER_LIST = 0x%x ###" %b)

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_MEMBER_LIST:
                    sys_logging("### SAI_VLAN_ATTR_MEMBER_LIST count = %d ###" %a.value.objlist.count)
                    assert(1 == a.value.objlist.count)
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_VLAN_ATTR_MEMBER_LIST = 0x%x ###" %b)
                    assert(vlan_member in a.value.objlist.object_id_list)

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_2----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("### SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    if 0 != a.value.u32:
                        raise NotImplementedError()

            value = 1234
            attr_value = sai_thrift_attribute_value_t(u32=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES:
                    sys_logging("### SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES = %d ###" %a.value.u32)
                    if value != a.value.u32:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_3(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_3----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        ids_list = [SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        for attribute in switch_attr_list.attr_list:
            if attribute.id == SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID:
                sys_logging("### SAI_SWITCH_ATTR_DEFAULT_STP_INST_ID = 0x%x ###" %attribute.value.oid)
                default_stp_oid = attribute.value.oid

        vlan_list1 = [100]
        stp_oid = sai_thrift_create_stp_entry(self.client, vlan_list1)
        sys_logging("### stp_oid = 0x%x ###" %stp_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_STP_INSTANCE:
                    sys_logging("### SAI_VLAN_ATTR_STP_INSTANCE = 0x%x ###" %a.value.oid)
                    if default_stp_oid != a.value.oid:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(oid=stp_oid)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_STP_INSTANCE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_STP_INSTANCE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_STP_INSTANCE:
                    sys_logging("### SAI_VLAN_ATTR_STP_INSTANCE = 0x%x ###" %a.value.oid)
                    if stp_oid != a.value.oid:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_stp_entry(stp_oid)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_4(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_4----- ###")
        switch_init(self.client)
        
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_LEARN_DISABLE:
                    sys_logging("### SAI_VLAN_ATTR_LEARN_DISABLE = %d ###" %a.value.booldata)
                    if False != a.value.booldata:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_LEARN_DISABLE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_LEARN_DISABLE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_LEARN_DISABLE:
                    sys_logging("### SAI_VLAN_ATTR_LEARN_DISABLE = %d ###" %a.value.booldata)
                    if True != a.value.booldata:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_5(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_5----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_MAC_DA != a.value.s32:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_SG)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_SG != a.value.s32:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG_AND_SG)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_IPV4_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG_AND_SG != a.value.s32:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_6(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_6----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_MAC_DA != a.value.s32:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG != a.value.s32:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG_AND_SG)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()
            
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_IPV6_MCAST_LOOKUP_KEY_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_MCAST_LOOKUP_KEY_TYPE_XG_AND_SG != a.value.s32:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)


#class func_06_set_and_get_vlan_attribute_fn_7(sai_base_test.ThriftInterfaceDataPlane):
#    def runTest(self):
#
#        sys_logging("###set_and_get_vlan_attribute###")
#        
#        switch_init(self.client)
#        
#        vlan_id = 100
#        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
#        
#        addr_family = SAI_IP_ADDR_FAMILY_IPV4
#        ip_addr1 = '10.10.10.1'
#        ip_mask1 = '255.255.255.255'
#        dmac1 = '00:11:22:33:44:55'
#
#        table_stage = SAI_ACL_STAGE_INGRESS
#        table_bind_vlan_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
#        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
#        action = SAI_PACKET_ACTION_DROP
#        in_ports = None
#        mac_src = None
#        mac_dst = None
#        mac_src_mask = None
#        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
#        svlan_id=None
#        svlan_pri=None
#        svlan_cfi=None
#        cvlan_id=None
#        cvlan_pri=None
#        cvlan_cfi=None
#        ip_src = "192.168.0.1"
#        ip_src_mask = "255.255.255.0"
#        ip_dst = None
#        ip_dst_mask = None
#        is_ipv6 = False
#        ip_tos=None
#        ip_ecn=None
#        ip_dscp=None
#        ip_ttl=None
#        ip_proto = None
#        in_port = None
#        out_port = None
#        out_ports = None
#        src_l4_port = None
#        dst_l4_port = None
#        ingress_mirror_id = None
#        egress_mirror_id = None
#        admin_state = True
#        #add vlan edit action
#        new_svlan = None
#        new_scos = None
#        new_cvlan = None
#        new_ccos = None
#        #deny learning
#        deny_learn = None
#
#        acl_table_id = sai_thrift_create_acl_table(self.client,
#            table_stage,
#            table_bind_vlan_list,
#            addr_family,
#            mac_src,
#            mac_dst,
#            ip_src,
#            ip_dst,
#            ip_proto,
#            in_ports,
#            out_ports,
#            in_port,
#            out_port,
#            None,
#            None,
#            None,
#            None,
#            None,
#            None,            
#            src_l4_port,
#            dst_l4_port)
#        acl_entry_id = sai_thrift_create_acl_entry(self.client,
#            acl_table_id,
#            entry_priority,
#            admin_state,
#            action, addr_family,
#            mac_src, mac_src_mask,
#            mac_dst, mac_dst_mask,
#            svlan_id, svlan_pri,
#            svlan_cfi, cvlan_id,
#            cvlan_pri, cvlan_cfi,
#            ip_src, ip_src_mask,
#            ip_dst, ip_dst_mask,
#            is_ipv6,
#            ip_tos, ip_ecn,
#            ip_dscp, ip_ttl,
#            ip_proto,
#            in_ports, out_ports,
#            in_port, out_port,
#            src_l4_port, dst_l4_port,
#            ingress_mirror_id,
#            egress_mirror_id,
#            new_svlan, new_scos,
#            new_cvlan, new_ccos,
#            deny_learn)
#            
#                    
#        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
#        for a in attrs.attr_list:
#            if a.id == SAI_VLAN_ATTR_INGRESS_ACL:
#                sys_logging("###SAI_VLAN_ATTR_INGRESS_ACL = %d ###" %a.value.oid)
#                if SAI_NULL_OBJECT_ID != a.value.oid:
#                    raise NotImplementedError()
#        warmboot(self.client)
#        try:
#            attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
#            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            sys_logging("###status = %d###" %status) 
#            if status != SAI_STATUS_SUCCESS:
#                raise NotImplementedError()
#            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
#            for a in attrs.attr_list:
#                if a.id == SAI_VLAN_ATTR_INGRESS_ACL:
#                    sys_logging("###SAI_VLAN_ATTR_INGRESS_ACL = %d ###" %a.value.oid)
#                    if acl_table_id != a.value.oid:
#                        raise NotImplementedError()            
#        finally:
#            sys_logging("###unbind this ACL table and remove ###" )
#            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
#            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
#            self.client.sai_thrift_remove_acl_table(acl_table_id)
#            self.client.sai_thrift_remove_vlan(vlan_oid)             
#            
#            
#            
#            
#class func_06_set_and_get_vlan_attribute_fn_8(sai_base_test.ThriftInterfaceDataPlane):
#    def runTest(self):
#
#        sys_logging("###set_and_get_vlan_attribute###")
#        
#        switch_init(self.client)
#        
#        vlan_id = 100
#        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
#        
#        addr_family = SAI_IP_ADDR_FAMILY_IPV4
#        ip_addr1 = '10.10.10.1'
#        ip_mask1 = '255.255.255.255'
#        dmac1 = '00:11:22:33:44:55'
#
#        table_stage = SAI_ACL_STAGE_EGRESS
#        table_bind_vlan_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
#        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
#        action = SAI_PACKET_ACTION_DROP
#        in_ports = None
#        mac_src = None
#        mac_dst = None
#        mac_src_mask = None
#        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
#        svlan_id=None
#        svlan_pri=None
#        svlan_cfi=None
#        cvlan_id=None
#        cvlan_pri=None
#        cvlan_cfi=None
#        ip_src = "192.168.0.1"
#        ip_src_mask = "255.255.255.0"
#        ip_dst = None
#        ip_dst_mask = None
#        is_ipv6 = False
#        ip_tos=None
#        ip_ecn=None
#        ip_dscp=None
#        ip_ttl=None
#        ip_proto = None
#        in_port = None
#        out_port = None
#        out_ports = None
#        src_l4_port = None
#        dst_l4_port = None
#        ingress_mirror_id = None
#        egress_mirror_id = None
#        admin_state = True
#        #add vlan edit action
#        new_svlan = None
#        new_scos = None
#        new_cvlan = None
#        new_ccos = None
#        #deny learning
#        deny_learn = None
#
#        acl_table_id = sai_thrift_create_acl_table(self.client,
#            table_stage,
#            table_bind_vlan_list,
#            addr_family,
#            mac_src,
#            mac_dst,
#            ip_src,
#            ip_dst,
#            ip_proto,
#            in_ports,
#            out_ports,
#            in_port,
#            out_port,
#            src_l4_port,
#            dst_l4_port)
#        acl_entry_id = sai_thrift_create_acl_entry(self.client,
#            acl_table_id,
#            entry_priority,
#            admin_state,
#            action, addr_family,
#            mac_src, mac_src_mask,
#            mac_dst, mac_dst_mask,
#            svlan_id, svlan_pri,
#            svlan_cfi, cvlan_id,
#            cvlan_pri, cvlan_cfi,
#            ip_src, ip_src_mask,
#            ip_dst, ip_dst_mask,
#            is_ipv6,
#            ip_tos, ip_ecn,
#            ip_dscp, ip_ttl,
#            ip_proto,
#            in_ports, out_ports,
#            in_port, out_port,
#            src_l4_port, dst_l4_port,
#            ingress_mirror_id,
#            egress_mirror_id,
#            new_svlan, new_scos,
#            new_cvlan, new_ccos,
#            deny_learn)
#            
#                    
#        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
#        for a in attrs.attr_list:
#            if a.id == SAI_VLAN_ATTR_EGRESS_ACL:
#                sys_logging("###SAI_VLAN_ATTR_EGRESS_ACL = %d ###" %a.value.oid)
#                if SAI_NULL_OBJECT_ID != a.value.oid:
#                    raise NotImplementedError()
#        warmboot(self.client)
#        try:
#            attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_EGRESS_ACL, value=attr_value)
#            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            sys_logging("###status = %d###" %status) 
#            if status != SAI_STATUS_SUCCESS:
#                raise NotImplementedError()
#            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
#            for a in attrs.attr_list:
#                if a.id == SAI_VLAN_ATTR_EGRESS_ACL:
#                    sys_logging("###SAI_VLAN_ATTR_EGRESS_ACL = %d ###" %a.value.oid)
#                    if acl_table_id != a.value.oid:
#                        raise NotImplementedError()            
#        finally:
#            sys_logging("###unbind this ACL table and remove ###" )
#            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_EGRESS_ACL, value=attr_value)
#            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
#            self.client.sai_thrift_remove_acl_table(acl_table_id)
#            self.client.sai_thrift_remove_vlan(vlan_oid)                 
#            
#            
#            
#class func_06_set_and_get_vlan_attribute_fn_9(sai_base_test.ThriftInterfaceDataPlane):
#    def runTest(self):
#
#        sys_logging("###set_and_get_vlan_attribute###")
#        
#        switch_init(self.client)
#        
#        vlan_id = 100
#        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
#
#        addr_family = SAI_IP_ADDR_FAMILY_IPV4
#        ip_addr1 = '10.10.10.1'
#        ip_mask1 = '255.255.255.255'
#        dmac1 = '00:11:22:33:44:55'
#
#        table_stage = SAI_ACL_STAGE_INGRESS
#        table_bind_vlan_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
#        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
#        action = SAI_PACKET_ACTION_DROP
#        in_ports = None
#        mac_src = None
#        mac_dst = None
#        mac_src_mask = None
#        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
#        svlan_id=None
#        svlan_pri=None
#        svlan_cfi=None
#        cvlan_id=None
#        cvlan_pri=None
#        cvlan_cfi=None
#        ip_src = "192.168.0.1"
#        ip_src_mask = "255.255.255.0"
#        ip_dst = None
#        ip_dst_mask = None
#        is_ipv6 = False
#        ip_tos=None
#        ip_ecn=None
#        ip_dscp=None
#        ip_ttl=None
#        ip_proto = None
#        in_port = None
#        out_port = None
#        out_ports = None
#        src_l4_port = None
#        dst_l4_port = None
#        ingress_mirror_id = None
#        egress_mirror_id = None
#        admin_state = True
#        #add vlan edit action
#        new_svlan = None
#        new_scos = None
#        new_cvlan = None
#        new_ccos = None
#        #deny learning
#        deny_learn = None
#
#        acl_table_id = sai_thrift_create_acl_table(self.client,
#            table_stage,
#            table_bind_vlan_list,
#            addr_family,
#            mac_src,
#            mac_dst,
#            ip_src,
#            ip_dst,
#            ip_proto,
#            in_ports,
#            out_ports,
#            in_port,
#            out_port,
#            src_l4_port,
#            dst_l4_port)
#        acl_entry_id = sai_thrift_create_acl_entry(self.client,
#            acl_table_id,
#            entry_priority,
#            admin_state,
#            action, addr_family,
#            mac_src, mac_src_mask,
#            mac_dst, mac_dst_mask,
#            svlan_id, svlan_pri,
#            svlan_cfi, cvlan_id,
#            cvlan_pri, cvlan_cfi,
#            ip_src, ip_src_mask,
#            ip_dst, ip_dst_mask,
#            is_ipv6,
#            ip_tos, ip_ecn,
#            ip_dscp, ip_ttl,
#            ip_proto,
#            in_ports, out_ports,
#            in_port, out_port,
#            src_l4_port, dst_l4_port,
#            ingress_mirror_id,
#            egress_mirror_id,
#            new_svlan, new_scos,
#            new_cvlan, new_ccos,
#            deny_learn)
#                        
#        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
#        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
#        status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#        sys_logging("###status = %d###" %status) 
#        if status != SAI_STATUS_SUCCESS:
#            raise NotImplementedError()
#            
#                    
#        attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
#        for a in attrs.attr_list:
#            if a.id == SAI_VLAN_ATTR_META_DATA:
#                sys_logging("###SAI_VLAN_ATTR_META_DATA = %d ###" %a.value.u32)
#                if 0 != a.value.u32:
#                    raise NotImplementedError()
#        warmboot(self.client)
#        try:
#            attr_value = sai_thrift_attribute_value_t(u32=254)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_META_DATA, value=attr_value)
#            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            sys_logging("###status = %d###" %status) 
#            if status != SAI_STATUS_SUCCESS:
#                raise NotImplementedError()
#            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)            
#            for a in attrs.attr_list:
#                if a.id == SAI_VLAN_ATTR_META_DATA:
#                    sys_logging("###SAI_VLAN_ATTR_META_DATA = %d ###" %a.value.u32)
#                    if 254 != a.value.u32:
#                        raise NotImplementedError()            
#        finally:
#            sys_logging("###unbind this ACL table and remove ###" )
#            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
#            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
#            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
#            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
#            self.client.sai_thrift_remove_acl_table(acl_table_id)
#            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_10(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_10----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_FLOOD_CONTROL_TYPE_ALL != a.value.s32:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_FLOOD_CONTROL_TYPE_L2MC_GROUP)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE: status = 0x%x ###" %status)
            if status == SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_FLOOD_CONTROL_TYPE_NONE)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_FLOOD_CONTROL_TYPE_NONE != a.value.s32:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_11(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_11----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_FLOOD_CONTROL_TYPE_ALL != a.value.s32:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_FLOOD_CONTROL_TYPE_COMBINED)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE: status = 0x%x ###" %status)
            if status == SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_FLOOD_CONTROL_TYPE_NONE)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_FLOOD_CONTROL_TYPE_NONE != a.value.s32:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid) 


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_12(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_12----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_FLOOD_CONTROL_TYPE_ALL != a.value.s32:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_FLOOD_CONTROL_TYPE_NONE)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE:
                    sys_logging("### SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE = %d ###" %a.value.s32)
                    if SAI_VLAN_FLOOD_CONTROL_TYPE_NONE != a.value.s32:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_13(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_13----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE:
                    sys_logging("### SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE = %d ###" %a.value.booldata)
                    if False != a.value.booldata:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE:
                    sys_logging("### SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE = %d ###" %a.value.booldata)
                    if True != a.value.booldata:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_14(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_14----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        enable_type = SAI_PTP_ENABLE_BASED_TYPE_VLAN
        device_type = SAI_PTP_DEVICE_TYPE_BC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        sys_logging("### ptp_oid = 0x%x ###" %ptp_oid)

        warmboot(self.client)

        try:
            default_ptp_oid = (0 << 32 | SAI_OBJECT_TYPE_PTP_DOMAIN)
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_PTP_DOMAIN_ID:
                    sys_logging("### SAI_VLAN_ATTR_PTP_DOMAIN_ID = 0x%x ###" %a.value.oid)
                    if default_ptp_oid != a.value.oid:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_PTP_DOMAIN_ID, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_PTP_DOMAIN_ID: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_PTP_DOMAIN_ID:
                    sys_logging("### SAI_VLAN_ATTR_PTP_DOMAIN_ID = 0x%x ###" %a.value.oid)
                    if ptp_oid != a.value.oid:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_15(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_15----- ###")
        switch_init(self.client)

        vlan_id1 = 100
        vlan_id2 = 200
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1, True)
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oid1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2, False)
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oid2)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE:
                    sys_logging("### SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE = %d ###" %a.value.booldata)
                    if True != a.value.booldata:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid2)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE:
                    sys_logging("### SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE = %d ###" %a.value.booldata)
                    if False != a.value.booldata:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)
            sys_logging("### set SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid2, attr)
            sys_logging("### set SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid1)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE:
                    sys_logging("### SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE = %d ###" %a.value.booldata)
                    if False != a.value.booldata:
                        raise NotImplementedError()
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid2)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE:
                    sys_logging("### SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE = %d ###" %a.value.booldata)
                    if True != a.value.booldata:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


@group('L2')
class func_06_set_and_get_vlan_attribute_fn_16(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        '''
        SAI Bug 112256
        '''
        sys_logging("### -----func_06_set_and_get_vlan_attribute_fn_16----- ###")
        switch_init(self.client)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        cir = 100000
        cbs = 2000
        pir = 200000
        pbs = 4000
        pkt_action = SAI_PACKET_ACTION_FORWARD
        policer_oid = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_ENHANCED_TR_TCM,
                                                    SAI_POLICER_COLOR_SOURCE_AWARE, cir, cbs, pir, pbs,
                                                    pkt_action, pkt_action, pkt_action, [1,1,1])
        sys_logging("### policer_oid = 0x%x ###" %policer_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id ==  SAI_VLAN_ATTR_POLICER_ID:
                    sys_logging("### SAI_VLAN_ATTR_POLICER_ID = 0x%x ###" %a.value.oid)
                    if SAI_NULL_OBJECT_ID != a.value.oid:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(oid=policer_oid)
            attr = sai_thrift_attribute_t(id= SAI_VLAN_ATTR_POLICER_ID, value=attr_value)
            status = self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            sys_logging("### set SAI_VLAN_ATTR_POLICER_ID: status = 0x%x ###" %status)
            if status != SAI_STATUS_SUCCESS:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id ==  SAI_VLAN_ATTR_POLICER_ID:
                    sys_logging("### SAI_VLAN_ATTR_POLICER_ID = 0x%x ###" %a.value.oid)
                    if policer_oid != a.value.oid:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_policer(policer_oid)


@group('L2')
class func_07_create_vlan_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_07_create_vlan_member_fn----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        warmboot(self.client)

        try:
            vlan_member = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            sys_logging("### vlan_member oid = 0x%x ###" %vlan_member)
            if SAI_NULL_OBJECT_ID == vlan_member:
                raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_08_create_same_vlan_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_08_create_same_vlan_member_fn----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member1 oid = 0x%x ###" %vlan_member1)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member2 oid = 0x%x ###" %vlan_member2)

        warmboot(self.client)

        try:
            if SAI_NULL_OBJECT_ID == vlan_member1:
                raise NotImplementedError()
            if vlan_member1 != vlan_member2:
                raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_09_remove_vlan_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_09_remove_vlan_member_fn----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member1 oid = 0x%x ###" %vlan_member1)

        warmboot(self.client)

        try:
            status = self.client.sai_thrift_remove_vlan_member(vlan_member1)
            sys_logging("### status = %d ###" %status)
            if SAI_STATUS_SUCCESS != status:
                raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_10_remove_not_exist_vlan_member_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_10_remove_not_exist_vlan_member_fn----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)

        vlan_member_id = sai_thrift_create_vlan_member(self.client, vlan_oid, port1)
        sys_logging("### vlan_member_id = 0x%x ###" %vlan_member_id)

        warmboot(self.client)

        try:
            self.client.sai_thrift_remove_vlan_member(vlan_member_id)
            status = self.client.sai_thrift_remove_vlan_member(vlan_member_id)
            sys_logging("### status = 0x%x ###" %status)
            assert(SAI_STATUS_SUCCESS != status)

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_11_set_and_get_vlan_member_attribute_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_11_set_and_get_vlan_member_attribute_fn_0----- ###")
        switch_init(self.client)

        port1 = port_list[0]
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member1 oid = 0x%x ###" %vlan_member1)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_member_attribute(vlan_member1)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_MEMBER_ATTR_VLAN_ID:
                    sys_logging("### SAI_VLAN_MEMBER_ATTR_VLAN_ID = 0x%x ###" %a.value.oid)
                    if vlan_oid != a.value.oid:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(oid=vlan_oid)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_MEMBER_ATTR_VLAN_ID, value=attr_value)
            status = self.client.sai_thrift_set_vlan_member_attribute(vlan_member1, attr)
            sys_logging("### set SAI_VLAN_MEMBER_ATTR_VLAN_ID: status = 0x%x ###" %status)
            if SAI_STATUS_SUCCESS == status:
                raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_11_set_and_get_vlan_member_attribute_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_11_set_and_get_vlan_member_attribute_fn_1----- ###")
        switch_init(self.client)
        
        port1 = port_list[1]
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member1 oid = 0x%x ###" %vlan_member1)
        bport_oid = sai_thrift_get_bridge_port_by_port(self.client, port1)
        sys_logging("### bport_oid = 0x%x ###" %bport_oid)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_member_attribute(vlan_member1)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID:
                    sys_logging("### SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID  = 0x%x ###" %a.value.oid)
                    if bport_oid != a.value.oid:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(oid=bport_oid)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID, value=attr_value)
            status = self.client.sai_thrift_set_vlan_member_attribute(vlan_member1, attr)
            sys_logging("### set SAI_VLAN_MEMBER_ATTR_BRIDGE_PORT_ID: status = 0x%x ###" %status)
            if SAI_STATUS_SUCCESS == status:
                raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_11_set_and_get_vlan_member_attribute_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_11_set_and_get_vlan_member_attribute_fn_2----- ###")
        switch_init(self.client)

        port1 = port_list[1]
        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)
        tag_mode = SAI_VLAN_TAGGING_MODE_UNTAGGED
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, tag_mode)
        sys_logging("### vlan_member1 oid = 0x%x ###" %vlan_member1)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_member_attribute(vlan_member1)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE:
                    sys_logging("### SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE = %d ###" %a.value.s32)
                    if tag_mode != a.value.s32:
                        raise NotImplementedError()

            tag_mode = SAI_VLAN_TAGGING_MODE_PRIORITY_TAGGED
            attr_value = sai_thrift_attribute_value_t(s32=tag_mode)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_member_attribute(vlan_member1, attr)
            sys_logging("### set SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE: status = 0x%x ###" %status)
            if SAI_STATUS_SUCCESS == status:
                raise NotImplementedError()

            tag_mode = SAI_VLAN_TAGGING_MODE_TAGGED
            attr_value = sai_thrift_attribute_value_t(s32=tag_mode)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE, value=attr_value)
            status = self.client.sai_thrift_set_vlan_member_attribute(vlan_member1, attr)
            sys_logging("### set SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE: status = 0x%x ###" %status)
            if SAI_STATUS_SUCCESS != status:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_vlan_member_attribute(vlan_member1)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE:
                    sys_logging("### SAI_VLAN_MEMBER_ATTR_VLAN_TAGGING_MODE = %d ###" %a.value.s32)
                    if tag_mode != a.value.s32:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class func_12_get_vlan_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_12_get_vlan_stats_fn----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[1]
        port2 = port_list[2]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oid1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oid2)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member1 oid = 0x%x ###" %vlan_member1)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member2 oid = 0x%x ###" %vlan_member2)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member3 oid = 0x%x ###" %vlan_member3)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member4 oid = 0x%x ###" %vlan_member4)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                    ip_dst='10.0.0.1', ip_id=102,
                                    dl_vlan_enable=True, vlan_vid=10,
                                    ip_ttl=64, pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                     ip_dst='10.0.0.1', ip_id=102,
                                     dl_vlan_enable=True, vlan_vid=20,
                                     ip_ttl=64, pktlen=100)

        warmboot(self.client)

        try:
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS,
                           SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS]
            sys_logging("### get vlan stats before sending packets ###")
            list1 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5)
            for a in range(0, 4):
                sys_logging("### list1[%d] = %d ###" %(a, list1[a]))
            assert(list1[0] == 0)
            assert(list1[1] == 0)
            assert(list1[2] == 0)
            assert(list1[3] == 0)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(pkt1, [2])
            self.ctc_send_packet(2, str(pkt2))
            self.ctc_verify_packets(pkt2, [1])

            sys_logging("### get vlan stats after sending packets ###")
            list2 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5)
            for a in range(0, 4):
                sys_logging("### list2[%d] = %d ###" %(a, list2[a]))
            assert(list2[0] == 104)
            assert(list2[1] == 1)
            assert(list2[2] == 104)
            assert(list2[3] == 1)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


@group('L2')
class func_13_get_vlan_stats_ext_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_13_get_vlan_stats_ext_fn_0----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[1]
        port2 = port_list[2]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oid1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oid2)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member1 oid = 0x%x ###" %vlan_member1)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member2 oid = 0x%x ###" %vlan_member2)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member3 oid = 0x%x ###" %vlan_member3)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member4 oid = 0x%x ###" %vlan_member4)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                     ip_dst='10.0.0.1', ip_id=102,
                                     dl_vlan_enable=True, vlan_vid=10,
                                     ip_ttl=64, pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                     ip_dst='10.0.0.1', ip_id=102,
                                     dl_vlan_enable=True, vlan_vid=20,
                                     ip_ttl=64, pktlen=100)

        warmboot(self.client)

        try:
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS,
                           SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS,
                           SAI_VLAN_STAT_IN_UCAST_PKTS]
            mode = SAI_STATS_MODE_READ
            sys_logging("### get vlan stats at mode 0 before sending packets ###")
            list1 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5)
            for a in range(0, 4):
                sys_logging("### list1[%d] = %d ###" %(a, list1[a]))
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(pkt1, [2])
            self.ctc_send_packet(2, str(pkt2))
            self.ctc_verify_packets(pkt2, [1])

            sys_logging("### get vlan stats at mode 0 after sending packets ###")
            list2 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5)
            for a in range(0, 4):
                sys_logging("### list2[%d] = %d ###" %(a, list2[a]))
            assert (list2[0] == 104)
            assert (list2[1] == 1)
            assert (list2[2] == 104)
            assert (list2[3] == 1)

            sys_logging("### get vlan stats at mode 0 without sending packets ###")
            list3 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5)
            for a in range(0, 4):
                sys_logging("### list3[%d] = %d ###" %(a, list3[a]))
            assert (list3[0] == 104)
            assert (list3[1] == 1)
            assert (list3[2] == 104)
            assert (list3[3] == 1)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


@group('L2')
class func_13_get_vlan_stats_ext_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_13_get_vlan_stats_ext_fn_1----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[1]
        port2 = port_list[2]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oid1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oid2)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member1 oid = 0x%x ###" %vlan_member1)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member2 oid = 0x%x ###" %vlan_member2)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member3 oid = 0x%x ###" %vlan_member3)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member4 oid = 0x%x ###" %vlan_member4)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                     ip_dst='10.0.0.1', ip_id=102,
                                     dl_vlan_enable=True, vlan_vid=10,
                                     ip_ttl=64, pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                     ip_dst='10.0.0.1', ip_id=102,
                                     dl_vlan_enable=True, vlan_vid=20,
                                     ip_ttl=64, pktlen=100)

        warmboot(self.client)

        try:
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS,
                           SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS,
                           SAI_VLAN_STAT_IN_UCAST_PKTS]
            mode = SAI_STATS_MODE_READ_AND_CLEAR
            sys_logging("### get vlan stats at mode 1 before sending packets ###")
            list1 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5) 
            for a in range(0, 4):
                sys_logging("### list1[%d] = %d ###" %(a, list1[a]))
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(pkt1, [2])
            self.ctc_send_packet(2, str(pkt2))
            self.ctc_verify_packets(pkt2, [1])

            sys_logging("### get vlan stats at mode 1 after sending packets ###")
            list2 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5)
            for a in range(0, 4):
                sys_logging("### list2[%d] = %d ###" %(a, list2[a]))
            assert (list2[0] == 104)
            assert (list2[1] == 1)
            assert (list2[2] == 104)
            assert (list2[3] == 1)

            sys_logging("### get vlan stats at mode 1 without sending packets ###")
            list3 = self.client.sai_thrift_get_vlan_stats_ext(vlan_oid1, counter_ids, mode, 5)
            for a in range(0, 4):
                sys_logging("### list3[%d] = %d ###" %(a, list3[a]))
            assert (list3[0] == 0)
            assert (list3[1] == 0)
            assert (list3[2] == 0)
            assert (list3[3] == 0)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


@group('L2')
class func_14_clear_vlan_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_14_clear_vlan_stats_fn----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oid1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oid2)

        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member1 oid = 0x%x ###" %vlan_member1)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member2 oid = 0x%x ###" %vlan_member2)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member3 oid = 0x%x ###" %vlan_member3)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        sys_logging("### vlan_member4 oid = 0x%x ###" %vlan_member4)

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                     ip_dst='10.0.0.1', ip_id=102,
                                     dl_vlan_enable=True, vlan_vid=10,
                                     ip_ttl=64, pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                     ip_dst='10.0.0.1', ip_id=102,
                                     dl_vlan_enable=True, vlan_vid=20,
                                     ip_ttl=64, pktlen=100)

        warmboot(self.client)

        try:
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS,
                           SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS,
                           SAI_VLAN_STAT_IN_UCAST_PKTS]
            sys_logging("### get vlan stats before sending packets ###")
            list1 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5)
            for a in range(0, 4):
                sys_logging("### list1[%d] = %d ###" %(a, list1[a]))
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])

            sys_logging("### get vlan stats after sending packets ###")
            list2 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5)
            for a in range(0, 4):
                sys_logging("### list2[%d] = %d ###" %(a, list2[a]))
            assert (list2[0] == 104)
            assert (list2[1] == 1)
            assert (list2[2] == 104)
            assert (list2[3] == 1)

            status = self.client.sai_thrift_clear_vlan_stats(vlan_oid1, counter_ids, 5)
            sys_logging("### clear vlan stats: status = 0x%x ###" %status)
            sys_logging("### get vlan stats after clearing ###")
            list3 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5)
            for a in range(0, 4):
                sys_logging("### list3[%d] = %d ###" %(a, list3[a]))
            assert (list3[0] == 0)
            assert (list3[1] == 0)
            assert (list3[2] == 0)
            assert (list3[3] == 0)

            sys_logging("### get vlan stats without sending packets ###")
            list4 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 5)
            for a in range(0, 4):
                sys_logging("### list4[%d] = %d ###" %(a, list4[a]))
            assert (list4[0] == 0)
            assert (list4[1] == 0)
            assert (list4[2] == 0)
            assert (list4[3] == 0)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


@group('L2')
class func_15_create_and_remove_vlan_members_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_15_create_and_remove_vlan_members_fn----- ###")
        switch_init(self.client)

        vlan_id1 = 100
        vlan_id2 = 200
        vlan_id3 = 300
        vlan_id4 = 400
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oid1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oid2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        sys_logging("### vlan_oid3 = 0x%x ###" %vlan_oid3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
        sys_logging("### vlan_oid4 = 0x%x ###" %vlan_oid4)

        vlan_oid_list = [vlan_oid1, vlan_oid2, vlan_oid3, vlan_oid4]
        port_oid_list = [port_list[1], port_list[2], port_list[3], port_list[4]]
        tagging_mode_list = [SAI_VLAN_TAGGING_MODE_UNTAGGED, SAI_VLAN_TAGGING_MODE_TAGGED,
                             SAI_VLAN_TAGGING_MODE_UNTAGGED, SAI_VLAN_TAGGING_MODE_TAGGED]

        sys_logging("### create 4 vlan members with correct attributes ###")
        results = sai_thrift_create_vlan_members(self.client, vlan_oid_list, port_oid_list, tagging_mode_list, 4, 0)
        object_id_list = results[0]
        statuslist = results[1]

        warmboot(self.client)

        try:
            for object_id in object_id_list:
                sys_logging("### vlan_members_oid = 0x%x ###" %object_id)
                assert(object_id != SAI_NULL_OBJECT_ID)
            for status in statuslist:
                sys_logging("### status = 0x%x ###" %status)
                assert(status == SAI_STATUS_SUCCESS)

            sys_logging("### remove 4 vlan members ###")
            statuslist1 = sai_thrift_remove_vlan_members(self.client, object_id_list, 0)
            for status in statuslist1:
                sys_logging("### status = 0x%x ###" %status)
                assert(status == SAI_STATUS_SUCCESS)

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)


@group('L2')
class func_15_create_and_remove_vlan_members_fn_0(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_15_create_and_remove_vlan_members_fn_0----- ###")
        switch_init(self.client)

        vlan_id1 = 100
        vlan_id2 = 200
        vlan_id3 = 300
        vlan_id4 = 400
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oid1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oid2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        sys_logging("### vlan_oid3 = 0x%x ###" %vlan_oid3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
        sys_logging("### vlan_oid4 = 0x%x ###" %vlan_oid4)

        vlan_oid_fail = vlan_oid3 + 1
        vlan_oid_list = [vlan_oid1, vlan_oid2, vlan_oid_fail, vlan_oid4]
        port_oid_list = [port_list[1], port_list[2], port_list[3], port_list[4]]
        tagging_mode_list = [SAI_VLAN_TAGGING_MODE_UNTAGGED, SAI_VLAN_TAGGING_MODE_TAGGED,
                             SAI_VLAN_TAGGING_MODE_UNTAGGED, SAI_VLAN_TAGGING_MODE_TAGGED]

        sys_logging("### create 4 vlan members at mode 0 and 3rd is failed ###")
        results = sai_thrift_create_vlan_members(self.client, vlan_oid_list, port_oid_list, tagging_mode_list,
                                                 4, SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR)
        object_id_list = results[0]
        statuslist = results[1]

        warmboot(self.client)

        try:
            for a in range(0, 4):
                sys_logging("### vlan_members_oid%d = 0x%x ###" %(a, object_id_list[a]))
            assert(object_id_list[0] != SAI_NULL_OBJECT_ID)
            assert(object_id_list[1] != SAI_NULL_OBJECT_ID)
            assert(object_id_list[2] == SAI_NULL_OBJECT_ID)
            assert(object_id_list[3] == SAI_NULL_OBJECT_ID)

            for a in range(0, 4):
                sys_logging("### status%d = 0x%x ###" %(a, statuslist[a]))
            assert(statuslist[0] == SAI_STATUS_SUCCESS)
            assert(statuslist[1] == SAI_STATUS_SUCCESS)
            assert(statuslist[2] != SAI_STATUS_SUCCESS)
            assert(statuslist[3] == SAI_STATUS_NOT_EXECUTED)

            sys_logging("### remove 4 vlan members at mode 0 and 3rd is failed ###")
            statuslist1 = sai_thrift_remove_vlan_members(self.client, object_id_list,
                                                         SAI_BULK_OP_ERROR_MODE_STOP_ON_ERROR)
            for a in range(0, 4):
                sys_logging("### status%d = 0x%x ###" %(a, statuslist1[a]))
            assert(statuslist1[0] == SAI_STATUS_SUCCESS)
            assert(statuslist1[1] == SAI_STATUS_SUCCESS)
            assert(statuslist1[2] == SAI_STATUS_INVALID_OBJECT_ID)
            assert(statuslist1[3] == SAI_STATUS_NOT_EXECUTED)

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)


@group('L2')
class func_15_create_and_remove_vlan_members_fn_1(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----func_15_create_and_remove_vlan_members_fn_1----- ###")
        switch_init(self.client)

        vlan_id1 = 100
        vlan_id2 = 200
        vlan_id3 = 300
        vlan_id4 = 400
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        sys_logging("### vlan_oid1 = 0x%x ###" %vlan_oid1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        sys_logging("### vlan_oid2 = 0x%x ###" %vlan_oid2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        sys_logging("### vlan_oid3 = 0x%x ###" %vlan_oid3)
        vlan_oid4 = sai_thrift_create_vlan(self.client, vlan_id4)
        sys_logging("### vlan_oid4 = 0x%x ###" %vlan_oid4)

        vlan_oid_fail = vlan_oid3 + 1
        vlan_oid_list = [vlan_oid1, vlan_oid2, vlan_oid_fail, vlan_oid4]
        port_oid_list = [port_list[1], port_list[2], port_list[3], port_list[4]]
        tagging_mode_list = [SAI_VLAN_TAGGING_MODE_UNTAGGED, SAI_VLAN_TAGGING_MODE_TAGGED,
                             SAI_VLAN_TAGGING_MODE_UNTAGGED, SAI_VLAN_TAGGING_MODE_TAGGED]

        sys_logging("### create 4 vlan members at mode 1 and 3rd is failed ###")
        results = sai_thrift_create_vlan_members(self.client, vlan_oid_list, port_oid_list, tagging_mode_list,
                                                 4, SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR)
        object_id_list = results[0]
        statuslist = results[1]

        warmboot(self.client)

        try:
            for a in range(0, 4):
                sys_logging("### vlan_members_oid%d = 0x%x ###" %(a, object_id_list[a]))
            assert(object_id_list[0] != SAI_NULL_OBJECT_ID)
            assert(object_id_list[1] != SAI_NULL_OBJECT_ID)
            assert(object_id_list[2] == SAI_NULL_OBJECT_ID)
            assert(object_id_list[3] != SAI_NULL_OBJECT_ID)

            for a in range(0, 4):
                sys_logging("### status%d = 0x%x ###" %(a, statuslist[a]))
            assert(statuslist[0] == SAI_STATUS_SUCCESS)
            assert(statuslist[1] == SAI_STATUS_SUCCESS)
            assert(statuslist[2] != SAI_STATUS_SUCCESS)
            assert(statuslist[3] == SAI_STATUS_SUCCESS)

            sys_logging("### remove 4 vlan members at mode 1 and 3rd is failed ###")
            statuslist1 = sai_thrift_remove_vlan_members(self.client, object_id_list,
                                                         SAI_BULK_OP_ERROR_MODE_IGNORE_ERROR)
            for a in range(0, 4):
                sys_logging("### status%d = 0x%x ###" %(a, statuslist1[a]))
            assert(statuslist1[0] == SAI_STATUS_SUCCESS)
            assert(statuslist1[1] == SAI_STATUS_SUCCESS)
            assert(statuslist1[2] == SAI_STATUS_INVALID_OBJECT_ID)
            assert(statuslist1[3] == SAI_STATUS_SUCCESS)

        finally:
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)
            self.client.sai_thrift_remove_vlan(vlan_oid4)


@group('L2')
class scenario_01_access_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_01_access_port----- ###")
        switch_init(self.client)

        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packet(str(pkt), 1)

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class scenario_02_trunk_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_02_trunk_port----- ###")
        switch_init(self.client)

        vlan_id1 = 100
        vlan_id2 = 200
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                 dl_vlan_enable=True, vlan_vid=200,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


@group('L2')
class scenario_03_hybrid_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_03_hybrid_port----- ###")
        switch_init(self.client)

        vlan_id1 = 100
        vlan_id2 = 200
        vlan_id3 = 300
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member5 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member6 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac2, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid3, mac1, port1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid3, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                 dl_vlan_enable=True, vlan_vid=200,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        pkt2 = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                 dl_vlan_enable=True, vlan_vid=300,
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64, pktlen=104)

        exp_pkt2 = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                     ip_dst='10.0.0.1', ip_id=101, ip_ttl=64, pktlen=100)

        warmboot(self.client)

        try:
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)

            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_packets( str(exp_pkt2), [1], 1)

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid3, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid3, mac2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan_member(vlan_member5)
            self.client.sai_thrift_remove_vlan_member(vlan_member6)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)


@group('L2')
class scenario_04_access_port_to_hybrid_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_04_access_port_to_hybrid_port----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]

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

        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        mac3 = '00:30:30:30:30:30'
        mac4 = '00:40:40:40:40:40'
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port3)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac4, port3)

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

        warmboot(self.client)

        try:
            sys_logging ("Sending L2 packet port 1 -> port 3 [access vlan=10]), packet from port3 without vlan")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(pkt, [2])
            sys_logging ("Sending L2 packet port 2 -> port 3 [access vlan=20]) packet from port3 with vlan 20")
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(exp_pkt1, [2])

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac4)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_set_port_attribute(port3, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)


@group('L2')
class scenario_05_trunk_port_to_hybrid_port(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_05_trunk_port_to_hybrid_port----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        vlan_id3 = 30
        port1 = port_list[0]
        port2 = port_list[1]

        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oid3 = sai_thrift_create_vlan(self.client, vlan_id3)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member5 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member6 = sai_thrift_create_vlan_member(self.client, vlan_oid3, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id3)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        mac1 = '00:10:10:10:10:10'
        mac2 = '00:20:20:20:20:20'
        sai_thrift_create_fdb(self.client, vlan_oid1, mac2, port2)
        sai_thrift_create_fdb(self.client, vlan_oid2, mac2, port2)
        sai_thrift_create_fdb(self.client, vlan_oid3, mac2, port2)

        pkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=96)
        pkt2 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='10.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=100)
        pkt3 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='20.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=20,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        pkt4 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='30.0.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=30,
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst=mac2,
                                eth_src=mac1,
                                ip_dst='30.0.0.1',
                                ip_id=102,
                                ip_ttl=64,
                                pktlen=96)

        warmboot(self.client)

        try:
            sys_logging ("Sending L2 packet port 1 -> port 2 [without vlan]), packet from port2 with vlan 10")
            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt2, [1])

            sys_logging ("Sending L2 packet port 1 -> port 2 [with vlan 10]) packet from port2 with vlan 10")
            self.ctc_send_packet(0, str(pkt2))
            self.ctc_verify_packets(pkt2, [1])

            sys_logging ("Sending L2 packet port 1 -> port 2 [with vlan 20]) packet from port2 with  vlan 20")
            self.ctc_send_packet(0, str(pkt3))
            self.ctc_verify_packets(pkt3, [1])

            sys_logging ("Sending L2 packet port 1 -> port 2 [with vlan 30]) packet from port2 without vlan")
            self.ctc_send_packet(0, str(pkt4))
            self.ctc_verify_packets(exp_pkt1, [1])

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid2, mac2)
            sai_thrift_delete_fdb(self.client, vlan_oid3, mac2)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan_member(vlan_member5)
            self.client.sai_thrift_remove_vlan_member(vlan_member6)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)
            self.client.sai_thrift_remove_vlan(vlan_oid3)


@group('L2')
class scenario_06_vlan_unknown_ucast(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_06_vlan_unknown_ucast----- ###")
        switch_init(self.client)

        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            sys_logging("### -----enable flood----- ###")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_FLOOD_CONTROL_TYPE_ALL)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)

            sys_logging("### -----disable flood----- ###")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_FLOOD_CONTROL_TYPE_NONE)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_UNICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)

        finally:
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class scenario_07_vlan_unknown_mcast(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_07_vlan_unknown_mcast----- ###")
        switch_init(self.client)

        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        pkt = simple_tcp_packet(eth_dst='01:00:5e:7f:01:01', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            sys_logging("### -----enable flood----- ###")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_FLOOD_CONTROL_TYPE_ALL)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)

            sys_logging("### -----disable flood----- ###")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_FLOOD_CONTROL_TYPE_NONE)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_UNKNOWN_MULTICAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)

        finally:
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class scenario_08_vlan_broadcast(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_08_vlan_broadcast----- ###")
        switch_init(self.client)

        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        pkt = simple_tcp_packet(eth_dst='ff:ff:ff:ff:ff:ff', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        warmboot(self.client)

        try:
            sys_logging("### -----enable flood----- ###")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_FLOOD_CONTROL_TYPE_ALL)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)

            sys_logging("### -----disable flood----- ###")
            attr_value = sai_thrift_attribute_value_t(s32=SAI_VLAN_FLOOD_CONTROL_TYPE_NONE)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_BROADCAST_FLOOD_CONTROL_TYPE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)

        finally:
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class scenario_09_vlan_max_learned_addresses(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_09_vlan_max_learned_addresses----- ###")
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

        pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:11:11:11:11:11', eth_src='00:22:22:22:22:22',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        sys_logging ("### step1: no fdb entry ###")
        assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1))
        assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2))

        warmboot(self.client)

        try:
            sys_logging ("### step2: mac learnning address num is 1, so only can learning one fdb entry ###")
            limit_num = 1
            attr_value = sai_thrift_attribute_value_t(u32=limit_num)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt1), [1], 1)
            time.sleep(3)
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(str(pkt2), [0], 1)

            assert(1 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2))

            sys_logging ("### step3: flush all fdb entry ###")
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)
            time.sleep(3)
            sys_logging ("### step4: mac learnning address num is 0 means disable ###")
            limit_num = 0
            attr_value = sai_thrift_attribute_value_t(u32=limit_num)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_MAX_LEARNED_ADDRESSES, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets( str(pkt1), [1], 1)
            time.sleep(3)
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(str(pkt2), [0], 1)

            assert(1 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2))

        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class scenario_10_vlan_learn_disable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_10_vlan_learn_disable----- ###")
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

        pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:11:11:11:11:11', eth_src='00:22:22:22:22:22',
                                ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)

        sys_logging ("### step1: no fdb entry ###")
        assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1))
        assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2))

        warmboot(self.client)

        try:
            sys_logging ("### step2: mac learning enable ###")
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt1), [1], 1)
            time.sleep(3)
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(str(pkt2), [0], 1)

            assert(1 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1))
            assert(1 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2))

            sys_logging ("### step3: flush all fdb entry ###")
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)
            time.sleep(3)
            sys_logging ("### step4: mac learnning disable ###")

            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_LEARN_DISABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(str(pkt1), [1], 1)
            time.sleep(3)
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(str(pkt2), [0], 1)

            assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac1))
            assert(0 == sai_thrift_check_fdb_exist(self.client,vlan_oid, mac2))

        finally:
            sai_thrift_flush_fdb_by_vlan(self.client, vlan_oid)
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class scenario_11_vlan_igmp_snooping_enable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_11_vlan_igmp_snooping_enable----- ###")
        switch_init(self.client)

        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        pkt = simple_igmpv2_packet(eth_dst='01:00:5e:01:01:01', eth_src='00:00:00:00:00:01',
                                   ip_src='10.1.1.1', ip_dst='225.1.1.1', ip_ttl=1)

        warmboot(self.client)

        try:
            sys_logging("### step 1: igmp snooping disable ###")
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(str(pkt), [1], 1)

            assert(0 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

            sys_logging("### step 2: igmp snooping enable ###")
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_IGMP_SNOOPING_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(str(pkt), 1)

            assert(1 == sai_thrift_get_cpu_packet_count(self.client, mode=1))

        finally:
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


@group('L2')
class scenario_12_create_vlan_with_stats_enable_and_set(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_12_create_vlan_with_stats_enable_and_set----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[1]
        port2 = port_list[2]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sys_logging("### vlan stats control is default enable ###")
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2)
        vlan_oids = [vlan_oid1, vlan_oid2]
        for i in range(0, 2):
            sys_logging("### vlan_oid%d = 0x%x ###" %(i+1, vlan_oids[i]))
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_members = [vlan_member1, vlan_member2, vlan_member3, vlan_member4]
        for i in range(0, 4):
            sys_logging("### vlan_member%d = 0x%x ###" %(i+1, vlan_members[i]))

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                     ip_dst='10.0.0.1', ip_id=102,
                                     dl_vlan_enable=True, vlan_vid=10,
                                     ip_ttl=64, pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                     ip_dst='10.0.0.1', ip_id=102,
                                     dl_vlan_enable=True, vlan_vid=20,
                                     ip_ttl=64, pktlen=100)

        warmboot(self.client)

        try:
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS,
                           SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS]

            sys_logging("### step 1: do not send packet, so all stats is zero ###")
            list1 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4)
            for a in range(0, 4):
                sys_logging("### list1[%d] = %d ###" %(a, list1[a]))
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(pkt1, [2])
            self.ctc_send_packet(2, str(pkt2))
            self.ctc_verify_packets(pkt2, [1])

            sys_logging("### step 2: send packet, so all stats is not zero ###")
            list2 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4)
            for a in range(0, 4):
                sys_logging("### list2[%d] = %d ###" %(a, list2[a]))
            assert (list2[0] == 104)
            assert (list2[1] == 1)
            assert (list2[2] == 104)
            assert (list2[3] == 1)

            value = False
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(pkt1, [2])
            self.ctc_send_packet(2, str(pkt2))
            self.ctc_verify_packets(pkt2, [1])

            sys_logging("### step 3: disable vlan stats and send packet, all stats is zero ###")
            list3 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4)
            for a in range(0, 4):
                sys_logging("### list3[%d] = %d ###" %(a, list3[a]))
            assert (list3[0] == 0)
            assert (list3[1] == 0)
            assert (list3[2] == 0)
            assert (list3[3] == 0)

            value = True
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(pkt1, [2])
            self.ctc_send_packet(2, str(pkt2))
            self.ctc_verify_packets(pkt2, [1])

            sys_logging("### step 4: enable vlan stats and send packet, all stats is not zero ###")
            list4 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4)
            for a in range(0, 4):
                sys_logging("### list4[%d] = %d ###" %(a, list4[a]))
            assert (list4[0] == 104)
            assert (list4[1] == 1)
            assert (list4[2] == 104)
            assert (list4[3] == 1)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


@group('L2')
class scenario_13_create_vlan_with_stats_disable_and_set(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_13_create_vlan_with_stats_disable_and_set----- ###")
        switch_init(self.client)

        vlan_id1 = 10
        vlan_id2 = 20
        port1 = port_list[0]
        port2 = port_list[1]
        mac1 = '00:00:00:00:00:01'
        mac2 = '00:00:00:00:00:02'
        mac3 = '00:00:00:00:00:03'
        mac4 = '00:00:00:00:00:04'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sys_logging("### vlan stats control is disable ###")
        stats_enable = False
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1, stats_enable)
        vlan_oid2 = sai_thrift_create_vlan(self.client, vlan_id2, stats_enable)
        vlan_oids = [vlan_oid1, vlan_oid2]
        for i in range(0, 2):
            sys_logging("### vlan_oid%d = 0x%x ###" %(i+1, vlan_oids[i]))
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid1, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member4 = sai_thrift_create_vlan_member(self.client, vlan_oid2, port2, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_members = [vlan_member1, vlan_member2, vlan_member3, vlan_member4]
        for i in range(0, 4):
            sys_logging("### vlan_member%d = 0x%x ###" %(i+1, vlan_members[i]))

        pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                 dl_vlan_enable=True, vlan_vid=10,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt1 = simple_tcp_packet(eth_dst='00:00:00:00:00:02', eth_src='00:00:00:00:00:01',
                                     ip_dst='10.0.0.1', ip_id=102,
                                     dl_vlan_enable=True, vlan_vid=10,
                                     ip_ttl=64, pktlen=100)
        pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                 dl_vlan_enable=True, vlan_vid=20,
                                 ip_dst='10.0.0.1', ip_id=102,
                                 ip_ttl=64, pktlen=100)
        exp_pkt2 = simple_tcp_packet(eth_dst='00:00:00:00:00:03', eth_src='00:00:00:00:00:04',
                                     ip_dst='10.0.0.1', ip_id=102,
                                     dl_vlan_enable=True, vlan_vid=20,
                                     ip_ttl=64, pktlen=100)

        warmboot(self.client)

        try:
            counter_ids = [SAI_VLAN_STAT_IN_OCTETS, SAI_VLAN_STAT_IN_PACKETS,
                           SAI_VLAN_STAT_OUT_OCTETS, SAI_VLAN_STAT_OUT_PACKETS]
            sys_logging("### step 1: all stats is zero ###")
            list1 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4)
            for a in range(0, 4):
                sys_logging("### list1[%d] = %d ###" %(a, list1[a]))
            assert (list1[0] == 0)
            assert (list1[1] == 0)
            assert (list1[2] == 0)
            assert (list1[3] == 0)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])

            sys_logging("### step 2: send packet but vlan stats is disable, so all stats is zero ###")
            list2 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4)
            for a in range(0, 4):
                sys_logging("### list2[%d] = %d ###" %(a, list2[a]))
            assert (list2[0] == 0)
            assert (list2[1] == 0)
            assert (list2[2] == 0)
            assert (list2[3] == 0)

            value = True
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])

            sys_logging("### step 3: enable vlan stats and send packet, so all stats is not zero ###")
            list3 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4) 
            for a in range(0, 4):
                sys_logging("### list3[%d] = %d ###" %(a, list3[a]))
            assert (list3[0] == 104)
            assert (list3[1] == 1)
            assert (list3[2] == 104)
            assert (list3[3] == 1)

            value = False
            attr_value = sai_thrift_attribute_value_t(booldata=value)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_CUSTOM_STATS_ENABLE, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid1, attr)

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])
            self.ctc_send_packet(1, str(pkt2))
            self.ctc_verify_packets(pkt2, [0])

            sys_logging("### step 4: disable vlan stats and send packet, all stats is  zero ###")
            list4 = self.client.sai_thrift_get_vlan_stats(vlan_oid1, counter_ids, 4)
            for a in range(0, 4):
                sys_logging("### list4[%d] = %d ###" %(a, list4[a]))
            assert (list4[0] == 0)
            assert (list4[1] == 0)
            assert (list4[2] == 0)
            assert (list4[3] == 0)

        finally:
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan_member(vlan_member3)
            self.client.sai_thrift_remove_vlan_member(vlan_member4)
            self.client.sai_thrift_remove_vlan(vlan_oid1)
            self.client.sai_thrift_remove_vlan(vlan_oid2)


@group('L2')
class scenario_14_vlan_member_is_lag(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("### -----scenario_14_vlan_member_is_lag----- ###")
        switch_init(self.client)

        port1 = port_list[1]
        port2 = port_list[2]
        port3 = port_list[3]
        lag_oid = sai_thrift_create_lag(self.client)
        sys_logging("### lag_oid = 0x%x ###" %lag_oid)
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_oid, port1)
        sys_logging("### lag_member_id1 = 0x%x ###" %lag_member_id1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_oid, port2)
        sys_logging("### lag_member_id2 = 0x%x ###" %lag_member_id2)
        lag_bridge_oid = sai_thrift_create_bport_by_lag(self.client, lag_oid)
        sys_logging("### lag_bridge_oid = 0x%x ###" %lag_bridge_oid)

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sys_logging("### vlan_oid = 0x%x ###" %vlan_oid)
        is_lag = True
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_bridge_oid,
                                                     SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        sys_logging("### vlan_member1 = 0x%x ###" %vlan_member1)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port3, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        sys_logging("### vlan_member2 = 0x%x ###" %vlan_member2)
        vlan_member_list = [vlan_member1, vlan_member2]

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        self.client.sai_thrift_set_port_attribute(port3, attr)

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_bridge_oid, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port3, mac_action)

        pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22', eth_src='00:11:11:11:11:11',
                                 ip_dst='10.0.0.1', ip_id=101, ip_ttl=64)
        pkt2 = simple_tcp_packet(eth_dst='00:11:11:11:11:11', eth_src='00:22:22:22:22:22',
                                 ip_dst='10.0.0.1', ip_id=102, ip_ttl=64)

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_vlan_attribute(vlan_oid)
            for a in attrs.attr_list:
                if a.id == SAI_VLAN_ATTR_MEMBER_LIST:
                    sys_logging("### SAI_VLAN_ATTR_MEMBER_LIST count = %d ###" %a.value.objlist.count)
                    assert (a.value.objlist.count == 2)
                    for b in a.value.objlist.object_id_list:
                        sys_logging("### SAI_VLAN_ATTR_MEMBER_LIST = 0x%x ###" %b)
                        assert(b in vlan_member_list)

            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packet(str(pkt1), 3)

            self.ctc_send_packet(2, str(pkt1))
            self.ctc_verify_packet(str(pkt1), 3)

            self.ctc_send_packet(3, str(pkt2))
            self.ctc_verify_packet_any_port(str(pkt2), [1,2])

        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            sai_thrift_remove_bport_by_lag(self.client, lag_bridge_oid)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag(self.client, lag_oid)


