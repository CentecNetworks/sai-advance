# Copyright 2013-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Thrift SAI interface ACL tests
"""

import socket
import sys
import pdb

from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask

@group('acl')
class CreateAclTableGroup(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
            group_stage,
            group_bind_point_list,
            group_type)
        assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'
        warmboot(self.client)
        status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
        assert (status == SAI_STATUS_SUCCESS)

@group('acl')
class RemoveAclTableGroup(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
            group_stage,
            group_bind_point_list,
            group_type)
        assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'

        # create ACL table
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
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
        mac_src = None
        mac_dst = None
        mac_src_mask = None
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        ip_protocol = None
        in_port = 23
        out_port = None
        out_ports = None
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None

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
            dst_l4_port)
        assert acl_table_id > 0, 'acl_table_id is <= 0'

        # setup ACL table group members
        group_member_priority = 1

        # create ACL table group members
        acl_table_group_member_id = sai_thrift_create_acl_table_group_member(self.client,
            acl_table_group_id,
            acl_table_id,
            group_member_priority)
        warmboot(self.client)
        # test there is a table in group
        status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
        assert (status == SAI_STATUS_OBJECT_IN_USE)

        # remove acl table group member first
        status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id)
        assert (status == SAI_STATUS_SUCCESS)

        # test there is no table in group
        # remove acl table
        status = self.client.sai_thrift_remove_acl_table(acl_table_id)
        assert (status == SAI_STATUS_SUCCESS)
        #remove acl table group
        status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
        assert (status == SAI_STATUS_SUCCESS)

@group('acl')
class GetAclTableGroup(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT, SAI_ACL_BIND_POINT_TYPE_LAG]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
            group_stage,
            group_bind_point_list,
            group_type)
        assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'

        # create ACL table
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT, SAI_ACL_BIND_POINT_TYPE_LAG]
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = None
        mac_dst = None
        mac_src_mask = None
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        ip_protocol = None
        in_port = 3
        out_port = None
        out_ports = None
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
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None

        acl_table_id1 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id1 > 0, 'acl_table_id1 is <= 0'

        acl_table_id2 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id2 > 0, 'acl_table_id2 is <= 0'

        # setup ACL table group members, sequential group tcam block 0~1
        group_member_priority1 = 0
        group_member_priority2 = 1

        # create ACL table group members
        acl_table_group_member_id1 = sai_thrift_create_acl_table_group_member(self.client,
            acl_table_group_id,
            acl_table_id1,
            group_member_priority1)

        acl_table_group_member_id2 = sai_thrift_create_acl_table_group_member(self.client,
            acl_table_group_id,
            acl_table_id2,
            group_member_priority2)
        print "acl_table_group_member_id1 = ", acl_table_group_member_id1
        print "acl_table_group_member_id2 = ", acl_table_group_member_id2

        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_acl_table_group_attribute(acl_table_group_id)
            print "status = ", attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ACL_TABLE_GROUP_ATTR_ACL_STAGE:
                    print "set acl table group stage = ", group_stage
                    print "get acl table group stage = ", a.value.s32
                    if group_stage != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_ACL_TABLE_GROUP_ATTR_TYPE:
                    print "set acl table group type = ", group_type
                    print "get acl table group type = ", a.value.s32
                    if group_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_ACL_TABLE_GROUP_ATTR_ACL_BIND_POINT_TYPE_LIST:
                    print "set acl table group bind point list =  ", group_bind_point_list
                    print "get acl table group bind point list =  ", a.value.s32list.s32list
                    if group_bind_point_list != a.value.s32list.s32list:
                        raise NotImplementedError()
                if a.id == SAI_ACL_TABLE_GROUP_ATTR_MEMBER_LIST:
                    print "create acl table group member with this group ", [acl_table_group_member_id1, acl_table_group_member_id2]
                    print "get acl table group member with this group ", a.value.objlist.object_id_list
                    if ([acl_table_group_member_id1, acl_table_group_member_id2] != a.value.objlist.object_id_list) & ([acl_table_group_member_id2, acl_table_group_member_id1] != a.value.objlist.object_id_list):
                        raise NotImplementedError()
        finally:
            # remove acl table group member first
            status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id1)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id2)
            assert (status == SAI_STATUS_SUCCESS)
            # remove acl table
            status = self.client.sai_thrift_remove_acl_table(acl_table_id1)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_acl_table(acl_table_id2)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
            assert (status == SAI_STATUS_SUCCESS)

@group('acl')
class CreateAclTable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        # create ACL table
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = None
        mac_dst = None
        mac_src_mask = None
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        ip_protocol = None
        in_port = 0
        out_port = None
        out_ports = None
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
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None

        # create acl table
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
            dst_l4_port)
        assert acl_table_id > 0, 'acl_table_id is <= 0'

        warmboot(self.client)

        # remove acl table
        status = self.client.sai_thrift_remove_acl_table(acl_table_id)
        assert (status == SAI_STATUS_SUCCESS)

@group('acl')
class RemoveAclTable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        # create ACL table
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = None
        mac_dst = None
        mac_src_mask = None
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
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
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        ip_protocol = None
        #ip qos info
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        in_port = 0
        out_port = None
        out_ports = None
        ip_protocol = None
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None

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
            dst_l4_port)
        assert acl_table_id > 0, 'acl_table_id is <= 0'

        entry_priority = 1
        admin_state = True

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
            deny_learn)
        assert acl_entry_id > 0, 'acl_entry_id is <= 0'

        warmboot(self.client)

        # try to remove acl table
        status = self.client.sai_thrift_remove_acl_table(acl_table_id)
        assert (status == SAI_STATUS_OBJECT_IN_USE)
        status = self.client.sai_thrift_remove_acl_entry(acl_entry_id)
        assert (status == SAI_STATUS_SUCCESS)
        status = self.client.sai_thrift_remove_acl_table(acl_table_id)
        assert (status == SAI_STATUS_SUCCESS)


@group('acl')
class GetAclTable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]

        # create ACL table
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = '00:22:22:22:22:22'
        mac_dst = None
        mac_src_mask = 'ff:ff:ff:ff:ff:ff'
        mac_dst_mask = None
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
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
        ip_src = None
        ip_src_mask = None
        ip_src1 = "192.168.0.1"
        ip_src1_mask = "255.255.255.0"
        ip_src2 = "192.168.1.1"
        ip_src2_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        #ip qos info
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        ip_protocol = None
        in_port = 0
        out_port = None
        out_ports = None
        ip_protocol = None
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None

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
            dst_l4_port)
        assert acl_table_id > 0, 'acl_table_id is <= 0'

        entry_priority = 1
        admin_state = True

        acl_entry_id1 = sai_thrift_create_acl_entry(self.client,
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
            deny_learn)
        assert acl_entry_id1 > 0, 'acl_entry_id1 is <= 0'

        acl_entry_id2 = sai_thrift_create_acl_entry(self.client,
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
            ip_src1, ip_src1_mask,
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
            deny_learn)
        assert acl_entry_id2 > 0, 'acl_entry_id2 is <= 0'

        admin_state = False
        acl_entry_id3 = sai_thrift_create_acl_entry(self.client,
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
            ip_src2, ip_src2_mask,
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
            deny_learn)
        assert acl_entry_id3 > 0, 'acl_entry_id3 is <= 0'

        attr_list_ids = [SAI_ACL_TABLE_ATTR_ACL_STAGE, SAI_ACL_TABLE_ATTR_SIZE, SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST,
                         SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC, SAI_ACL_TABLE_ATTR_FIELD_DST_MAC, SAI_ACL_TABLE_ATTR_ENTRY_LIST,
                         SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_ENTRY]
        warmboot(self.client)

        try:
            attrs = self.client.sai_thrift_get_acl_table_attribute(acl_table_id, attr_list_ids)
            print "status = ", attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_ACL_TABLE_ATTR_ACL_STAGE:
                    print "set acl table stage = ", table_stage
                    print "get acl table stage = ", a.value.s32
                    if table_stage != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_ACL_TABLE_ATTR_SIZE:
                    print "set acl table size = ", 128
                    print "get acl table size = ", a.value.u32
                    if 0 != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST:
                    print "set acl table bind point list =  ", table_bind_point_list
                    print "get acl table bind point list =  ", a.value.s32list.s32list
                    if table_bind_point_list != a.value.s32list.s32list:
                        raise NotImplementedError()
                # select some wanted match key fields and some not wanted to test the function
                if a.id == SAI_ACL_TABLE_ATTR_FIELD_SRC_MAC:
                    if bool(mac_src) != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ACL_TABLE_ATTR_FIELD_DST_MAC:
                    if bool(mac_dst) != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_ACL_TABLE_ATTR_ENTRY_LIST:
                    print "add entry into table ", [acl_entry_id1, acl_entry_id2, acl_entry_id3]
                    print "get member in the table ", a.value.objlist.object_id_list
                    if ([acl_entry_id1, acl_entry_id2, acl_entry_id3] != a.value.objlist.object_id_list) & ([acl_entry_id3, acl_entry_id2, acl_entry_id1] != a.value.objlist.object_id_list):
                        raise NotImplementedError()
                #there are total 3 entry but only 2 is avalible
                if a.id == SAI_ACL_TABLE_ATTR_AVAILABLE_ACL_ENTRY:
                    print "set available entry num =  ", 2
                    print "get available entry num =  ", a.value.u32
                    if 2 != a.value.u32:
                        raise NotImplementedError()
                # counter to be done
        finally:
            # remove acl entry first
            status = self.client.sai_thrift_remove_acl_entry(acl_entry_id1)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_acl_entry(acl_entry_id2)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_acl_entry(acl_entry_id3)
            assert (status == SAI_STATUS_SUCCESS)
            # remove acl table
            status = self.client.sai_thrift_remove_acl_table(acl_table_id)
            assert (status == SAI_STATUS_SUCCESS)

class CreateAndRemoveAclTableGroupMember(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
            group_stage,
            group_bind_point_list,
            group_type)
        assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'

        # create ACL table
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = None
        mac_dst = None
        mac_src_mask = None
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        ip_protocol = None
        in_port = 0
        out_port = None
        out_ports = None
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
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None

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
            dst_l4_port)
        assert acl_table_id > 0, 'acl_table_id is <= 0'

        # setup ACL table group members
        group_member_priority = 1

        # create ACL table group members
        acl_table_group_member_id = sai_thrift_create_acl_table_group_member(self.client,
            acl_table_group_id,
            acl_table_id,
            group_member_priority)
        assert acl_table_group_member_id > 0, 'acl_table_group_member_id is <= 0'

        warmboot(self.client)

        # remove acl table group member first
        status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id)
        assert (status == SAI_STATUS_SUCCESS)

        # test there is no table in group
        # remove acl table
        status = self.client.sai_thrift_remove_acl_table(acl_table_id)
        assert (status == SAI_STATUS_SUCCESS)
        #remove acl table group
        status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
        assert (status == SAI_STATUS_SUCCESS)

class GetAclTableGroupMember(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
            group_stage,
            group_bind_point_list,
            group_type)
        assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'

        # create ACL table
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = None
        mac_dst = None
        mac_src_mask = None
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        ip_protocol = None
        in_port = 0
        out_port = None
        out_ports = None
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
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None

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
            dst_l4_port)
        assert acl_table_id > 0, 'acl_table_id is <= 0'

        # setup ACL table group members
        group_member_priority = 1

        # create ACL table group members
        acl_table_group_member_id = sai_thrift_create_acl_table_group_member(self.client,
            acl_table_group_id,
            acl_table_id,
            group_member_priority)
        assert acl_table_group_member_id > 0, 'acl_table_group_member_id is <= 0'

        warmboot(self.client)

        attrs = self.client.sai_thrift_get_acl_table_group_member_attribute(acl_table_group_member_id)
        print "status = ", attrs.status
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_GROUP_ID:
                print "set acl table group member group id =  ", acl_table_group_id
                print "get acl table group member group id =  ", a.value.oid
                if acl_table_group_id != a.value.oid:
                    raise NotImplementedError()
            if a.id == SAI_ACL_TABLE_GROUP_MEMBER_ATTR_ACL_TABLE_ID:
                print "set acl table group member table id =  ", acl_table_id
                print "get acl table group member table id =  ", a.value.oid
                if acl_table_id != a.value.oid:
                    raise NotImplementedError()
            if a.id == SAI_ACL_TABLE_GROUP_MEMBER_ATTR_PRIORITY:
                print "set acl table group member priority =  ", group_member_priority
                print "get acl table group member priority =  ", a.value.u32
                if group_member_priority != a.value.u32:
                    raise NotImplementedError()

        # remove acl table group member first
        status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id)
        assert (status == SAI_STATUS_SUCCESS)

        # test there is no table in group
        # remove acl table
        status = self.client.sai_thrift_remove_acl_table(acl_table_id)
        assert (status == SAI_STATUS_SUCCESS)
        #remove acl table group
        status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
        assert (status == SAI_STATUS_SUCCESS)

@group('acl')
class CreateAndRemoveAclEntry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]

        # create ACL table
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = None
        mac_dst = None
        mac_src_mask = None
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
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
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        #ip qos info
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        ip_protocol = None
        in_port = 0
        out_port = None
        out_ports = None
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None

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
            dst_l4_port)
        assert acl_table_id > 0, 'acl_table_id is <= 0'

        entry_priority = 1
        admin_state = True
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
            deny_learn)
        assert acl_entry_id > 0, 'acl_entry_id is <= 0'

        warmboot(self.client)

        status = self.client.sai_thrift_remove_acl_entry(acl_entry_id)
        assert (status == SAI_STATUS_SUCCESS)
        status = self.client.sai_thrift_remove_acl_table(acl_table_id)
        assert (status == SAI_STATUS_SUCCESS)

@group('acl')
class GetAclEntry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        port0 = port_list[0]
        port1 = port_list[1]

        # create ACL table
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        addr_family = None
        #action = SAI_PACKET_ACTION_DROP
        action = SAI_PACKET_ACTION_COPY
        in_ports = None
        mac_src = '12:34:56:78:9A:BC'
        mac_dst = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = None
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
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        ip_protocol = None
        #ip qos info
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        in_port = 0
        out_port = None
        out_ports = None
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None

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
            dst_l4_port)
        assert acl_table_id > 0, 'acl_table_id is <= 0'

        entry_priority = 1
        admin_state = True
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
            deny_learn)
        assert acl_entry_id > 0, 'acl_entry_id is <= 0'

        attr_list_ids = [SAI_ACL_ENTRY_ATTR_TABLE_ID, SAI_ACL_ENTRY_ATTR_PRIORITY, SAI_ACL_ENTRY_ATTR_ADMIN_STATE,
        SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC, SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP, SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION]

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_acl_entry_attribute(acl_entry_id, attr_list_ids)
            print "status = ", attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_ACL_ENTRY_ATTR_TABLE_ID:
                    print "set acl entry table id = ", acl_table_id
                    print "get acl entry table id = ", a.value.oid
                    if acl_table_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_ACL_ENTRY_ATTR_PRIORITY:
                    print "set acl entry priority = ", entry_priority
                    print "get acl entry priority = ", a.value.u32
                    if entry_priority != a.value.u32:
                        raise NotImplementedError()
                if a.id == SAI_ACL_ENTRY_ATTR_ADMIN_STATE:
                    print "set acl entry admin state =  ", admin_state
                    print "get acl entry admin state =  ", a.value.booldata
                    if admin_state != a.value.booldata:
                        raise NotImplementedError()
                # select some wanted key fields and some not wanted to test the function
                if a.id == SAI_ACL_ENTRY_ATTR_FIELD_SRC_MAC:
                    print "set acl entry src mac =  ", mac_src
                    print "get acl entry src mac =  ", a.value.aclfield.data.mac
                    if mac_src.upper() != a.value.aclfield.data.mac.upper():
                        raise NotImplementedError()
                if a.id == SAI_ACL_ENTRY_ATTR_FIELD_SRC_IP:
                    print "set acl entry src ip =  ", ip_src
                    print "get acl entry src ip =  ", a.value.aclfield.data.ip4
                    if ip_src != a.value.aclfield.data.ip4:
                        raise NotImplementedError()
                if a.id == SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION:
                    print "set acl entry packet action =  ", action
                    print "get acl entry packet action =  ", a.value.aclaction.parameter.s32
                    if action != a.value.aclaction.parameter.s32:
                        raise NotImplementedError()
        finally:
            # remove acl entry
            status = self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            assert (status == SAI_STATUS_SUCCESS)
            # remove acl table
            status = self.client.sai_thrift_remove_acl_table(acl_table_id)
            assert (status == SAI_STATUS_SUCCESS)

@group('acl')
class SclV4EntryBindPointPortTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_mask1 = '255.255.255.255'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

        # send the test packet(s)
        pkt = simple_qinq_tcp_packet(pktlen=100,
            eth_dst=router_mac,
            eth_src='00:22:22:22:22:22',
            dl_vlan_outer=20,
            dl_vlan_pcp_outer=4,
            dl_vlan_cfi_outer=1,
            vlan_vid=10,
            vlan_pcp=2,
            dl_vlan_cfi=1,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=64,
            tcp_sport=1234,
            tcp_dport=80)
        exp_pkt = simple_tcp_packet(pktlen=92,
            eth_dst='00:11:22:33:44:55',
            eth_src=router_mac,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=63,
            tcp_sport=1234,
            tcp_dport=80)

        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( exp_pkt, [0])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = '00:22:22:22:22:22'
        mac_dst = router_mac
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=20
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=None
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
        ip_protocol = 6
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        in_port = 1
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
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
            dst_l4_port)
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
            deny_learn)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        warmboot(self.client)

        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet(1, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet(exp_pkt, 0, default_time_out)

        finally:
            # unbind this ACL table from port2s object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

@group('acl')
class SclV6EntryBindPointPortTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_id = 20
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sai_thrift_create_fdb(self.client, vlan_oid, mac_dst, port2, mac_action)

        # send the test packet(s)
        pkt = simple_tcpv6_packet(pktlen=100,
                     eth_dst=mac_dst,
                     eth_src=mac_src,
                     dl_vlan_enable=True,
                     vlan_vid=20,
                     vlan_pcp=4,
                     ipv6_src='2001:db8:85a3::8a2e:370:7334',
                     ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                     ipv6_tc=0,
                     ipv6_ecn=None,
                     ipv6_dscp=None,
                     ipv6_hlim=64,
                     ipv6_fl=0,
                     tcp_sport=1234,
                     tcp_dport=80,
                     tcp_flags="S")
        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 0, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [1])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=20
        svlan_pri=4
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
        ip_type = SAI_ACL_IP_TYPE_IPV6ANY
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
        ip_src = '2001:db8:85a3::8a2e:370:7334'
        ip_src_mask = "FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF"
        ip_dst = '2001:db8:85a3::8a2e:370:7335'
        ip_dst_mask = "FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF:FFFF"
        ip_protocol = 6
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        in_port = 0
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        addr_family = None

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
            dst_l4_port)
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
            deny_learn)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        warmboot(self.client)

        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet(0, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet(pkt, 1, default_time_out)
        finally:
            # unbind this ACL table from vlan object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup FDB
            sai_thrift_delete_fdb(self.client, vlan_oid, mac_dst, port2)

            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('acl')
class SclV4EntryBindPointLagTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_id = 20
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sai_thrift_create_fdb(self.client, vlan_oid, mac_dst, port4, mac_action)

        # send the test packet(s)
        pkt = simple_qinq_tcp_packet(pktlen=100,
            eth_dst=mac_dst,
            eth_src=mac_src,
            dl_vlan_outer=20,
            dl_vlan_pcp_outer=4,
            dl_vlan_cfi_outer=1,
            vlan_vid=10,
            vlan_pcp=2,
            dl_vlan_cfi=1,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=64,
            tcp_sport=1234,
            tcp_dport=80)
        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet(0, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(pkt, [3])

            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet(1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(pkt, [3])

            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet(2, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(pkt, [3])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        #create Linkagg and add members in it
        lag_id = sai_thrift_create_lag(self.client)
        print"lag:%u" %lag_id
        print"lag:%lu" %lag_id
        print"lag:%lx" %lag_id
        print"lag:%x" %lag_id
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id, port2)

        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_LAG]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=20
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=None
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
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        ip_protocol = 6
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        addr_family = None

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
            dst_l4_port)
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
            deny_learn)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id, attr)

        warmboot(self.client)

        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet(0, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet(pkt, 3, default_time_out)

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet(1, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet(pkt, 3, default_time_out)

            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet(2, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(pkt, [3])
        finally:
            print '----------------------------------------------------------------------------------------------'

        #add new member
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id, port3)

        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 0, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( pkt, 3, default_time_out)

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( pkt, 3, default_time_out)

            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 2, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( pkt, 3, default_time_out)
        finally:
            print '----------------------------------------------------------------------------------------------'

        #remove old member
        sai_thrift_remove_lag_member(self.client, lag_member_id2)
        sai_thrift_remove_lag_member(self.client, lag_member_id3)

        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 0, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( pkt, 3, default_time_out)
            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [3])
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 2, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [3])
        finally:
            print '----------------------------------------------------------------------------------------------'
            #keep remove lag member first!!!!
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            # unbind this ACL table from vlan object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_lag_attribute(lag_id, attr)

            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup FDB
            sai_thrift_delete_fdb(self.client, vlan_oid, mac_dst, port4)

            self.client.sai_thrift_remove_vlan(vlan_oid)

            #celanup Lag
            sai_thrift_remove_lag(self.client, lag_id)

#update packet action  SAI_PACKET_ACTION_DROP --> SAI_PACKET_ACTION_LOG
@group('acl')
class SclV4EntryUpdatePacketActionTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_mask1 = '255.255.255.255'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

        # send the test packet(s)
        pkt = simple_qinq_tcp_packet(pktlen=100,
            eth_dst=router_mac,
            eth_src='00:22:22:22:22:22',
            dl_vlan_outer=20,
            dl_vlan_pcp_outer=4,
            dl_vlan_cfi_outer=1,
            vlan_vid=10,
            vlan_pcp=2,
            dl_vlan_cfi=1,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=64,
            tcp_sport=1234,
            tcp_dport=80)
        exp_pkt = simple_tcp_packet(pktlen=92,
            eth_dst='00:11:22:33:44:55',
            eth_src=router_mac,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=63,
            tcp_sport=1234,
            tcp_dport=80)

        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( exp_pkt, [0])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = '00:22:22:22:22:22'
        mac_dst = router_mac
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=20
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=None
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
        ip_protocol = 6
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        in_port = 1
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
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
            dst_l4_port)
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
            deny_learn)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        warmboot(self.client)
        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 1, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( exp_pkt, 0, default_time_out)
        finally:
            print '----------------------------------------------------------------------------------------------'

        # update this entry's packet action: change from SAI_PACKET_ACTION_DROP --> SAI_PACKET_ACTION_LOG
        action = SAI_PACKET_ACTION_LOG
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(s32=action), enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION, value=attribute_value)
        self.client.sai_thrift_set_acl_entry_attribute(acl_entry_id, attribute)

        #clear cpu count
        self.client.sai_thrift_clear_cpu_packet_info()
        warmboot(self.client)
        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'LOG, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 1, str(pkt))
            # ensure packet is received
            # check for present of packet here!
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( exp_pkt, [0])

            #check for cpu count
            ret = self.client.sai_thrift_get_cpu_packet_count()
            print "receive rx packet: %d" %ret.data.u16
            if ret.data.u16 != 1:
                raise NotImplementedError()

            attrs = self.client.sai_thrift_get_cpu_packet_attribute()
            print "success to get packet attribute"
            for a in attrs.attr_list:
                if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                    print "ingress port: 0x%lx" %a.value.oid
                    if port2 != a.value.oid:
                        raise NotImplementedError()
        finally:
            print '----------------------------------------------------------------------------------------------'

        # update this entry's packet action: change from SAI_PACKET_ACTION_LOG --> SAI_PACKET_ACTION_DENY #This is a combination of SAI packet action COPY_CANCEL and DROP
        action = SAI_PACKET_ACTION_DENY
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(s32=action), enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION, value=attribute_value)
        self.client.sai_thrift_set_acl_entry_attribute(acl_entry_id, attribute)

        #clear cpu count
        self.client.sai_thrift_clear_cpu_packet_info()

        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DENY, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 1, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( exp_pkt, 0, default_time_out)

            #check for cpu count
            ret = self.client.sai_thrift_get_cpu_packet_count()
            print "receive rx packet: %d" %ret.data.u16
            if ret.data.u16 != 0:
                raise NotImplementedError()

        finally:
            # unbind this ACL table from port2s object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

# test deny learning action and update to become enable learning
@group('acl')
class SclV4EntryDoNotLearnActionTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        vlan_id1 = 10
        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        sai_thrift_create_fdb(self.client, vlan_oid1, mac_dst, port2, mac_action)

        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = None
        in_ports = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
        ip_type = SAI_ACL_IP_TYPE_IPV4ANY
        mpls_label0_label=None
        mpls_label0_ttl=None
        mpls_label0_exp=None
        mpls_label0_bos=None
        mpls_label1_label=None
        mpls_label1_ttl=None
        mpls_label1_exp=None
        mpls_label1_bos=None
        mpls_label2_label=None
        mpls_label2_ttl=None
        mpls_label2_exp=None
        mpls_label2_bos=None
        mpls_label3_label=None
        mpls_label3_ttl=None
        mpls_label3_exp=None
        mpls_label3_bos=None
        mpls_label4_label=None
        mpls_label4_ttl=None
        mpls_label4_exp=None
        mpls_label4_bos=None
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.255"
        ip_dst = '10.10.10.1'
        ip_dst_mask = "255.255.255.255"
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        ip_protocol = 6
        in_port = 0
        out_port = None
        out_ports = None
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = True
        addr_family = None

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
            dst_l4_port)
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
            deny_learn)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1')
        pkt1 = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                 eth_src='00:22:22:33:33:44',
                                 ip_src='10.10.10.1',
                                 ip_dst='192.168.0.1')

        try:
            #test fdb function
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(pkt, [1])
            #test learning function
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_no_packet(pkt1, 0, default_time_out)

        finally:
            print '----------------------------------------------------------------------------------------------'

        attr_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(enable = False))
        attr = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_DO_NOT_LEARN, value=attr_value)
        self.client.sai_thrift_set_acl_entry_attribute(acl_entry_id, attr)

        warmboot(self.client)

        try:
            #test fdb function
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(pkt, [1])
            #test learning function
            self.ctc_send_packet(1, str(pkt1))
            self.ctc_verify_packets(pkt1, [0])

        finally:
            # unbind this ACL table from port2s object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup FDB
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac_dst, port2)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            self.client.sai_thrift_remove_vlan(vlan_oid1)

############### ACL Test ###############
@group('acl')
class AclV4EntryBindPointVlanTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_id = 20
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sai_thrift_create_fdb(self.client, vlan_oid, mac_dst, port2, mac_action)

        # send the test packet(s)
        pkt = simple_qinq_tcp_packet(pktlen=100,
            eth_dst=mac_dst,
            eth_src=mac_src,
            dl_vlan_outer=20,
            dl_vlan_pcp_outer=4,
            dl_vlan_cfi_outer=1,
            vlan_vid=10,
            vlan_pcp=2,
            dl_vlan_cfi=1,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=64,
            tcp_sport=1234,
            tcp_dport=80)
        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 0, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [1])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=None
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=None
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
        ip_protocol = 6
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        addr_family = None

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
            dst_l4_port)

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
            deny_learn)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        warmboot(self.client)
        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 0, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( pkt, 1, default_time_out)
        finally:
            # unbind this ACL table from vlan object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup FDB
            sai_thrift_delete_fdb(self.client, vlan_oid, mac_dst, port2)

            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('acl')
class AclV4EntryBindPointSwitchTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_id = 20
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sai_thrift_create_fdb(self.client, vlan_oid, mac_dst, port4, mac_action)

        # send the test packet(s)
        pkt = simple_qinq_tcp_packet(pktlen=100,
            eth_dst=mac_dst,
            eth_src=mac_src,
            dl_vlan_outer=20,
            dl_vlan_pcp_outer=4,
            dl_vlan_cfi_outer=1,
            vlan_vid=10,
            vlan_pcp=2,
            dl_vlan_cfi=1,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=64,
            tcp_sport=1234,
            tcp_dport=80)
        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 0, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [3])
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [3])
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 2, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [3])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_SWITCH]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=20
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=None
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
        ip_protocol = 6
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        addr_family = None

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
            dst_l4_port)

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
            deny_learn)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        warmboot(self.client)

        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 0, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( pkt, 3, default_time_out)

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 1, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( pkt, 3, default_time_out)

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 2, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( pkt, 3, default_time_out)
        finally:
            # unbind this ACL table from vlan object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup FDB
            sai_thrift_delete_fdb(self.client, vlan_oid, mac_dst, port4)

            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('acl')
class AclV4EntryPortBitMapTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        port17 = port_list[16]

        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_id = 20
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sai_thrift_create_fdb(self.client, vlan_oid, mac_dst, port4, mac_action)

        # send the test packet(s)
        pkt = simple_qinq_tcp_packet(pktlen=100,
            eth_dst=mac_dst,
            eth_src=mac_src,
            dl_vlan_outer=20,
            dl_vlan_pcp_outer=4,
            dl_vlan_cfi_outer=1,
            vlan_vid=10,
            vlan_pcp=2,
            dl_vlan_cfi=1,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=64,
            tcp_sport=1234,
            tcp_dport=80)
        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 0, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [3])
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [3])
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 2, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [3])
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet( 16, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [3])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_SWITCH]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_DROP
        in_ports = [port1, port2, port17]
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=20
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=None
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
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        ip_protocol = 6
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        addr_family = None

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
            dst_l4_port)

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
            deny_learn)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        warmboot(self.client)

        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 0, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( pkt, 3, default_time_out)

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 1, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( pkt, 3, default_time_out)

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 2, str(pkt))
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( pkt, [3])

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet( 16, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet( pkt, 3, default_time_out)
        finally:
            # unbind this ACL table from vlan object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup FDB
            sai_thrift_delete_fdb(self.client, vlan_oid, mac_dst, port4)

            self.client.sai_thrift_remove_vlan(vlan_oid)

#@group('acl')
#class AclV4EntryUpdatePortBitMapTest(sai_base_test.ThriftInterfaceDataPlane):
#    def runTest(self):
#        print
#        print '----------------------------------------------------------------------------------------------'
#        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"
#
#        switch_init(self.client)
#        port1 = port_list[0]
#        port2 = port_list[1]
#        port3 = port_list[2]
#        port4 = port_list[3]
#        port17 = port_list[16]
#
#        mac_src = '00:11:11:11:11:11'
#        mac_dst = '00:22:22:22:22:22'
#        mac_action = SAI_PACKET_ACTION_FORWARD
#
#        # the relationship between vlan id and vlan_oid
#        vlan_id = 20
#        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
#
#        sai_thrift_create_fdb(self.client, vlan_oid, mac_dst, port4, mac_action)
#
#        # send the test packet(s)
#        pkt = simple_qinq_tcp_packet(pktlen=100,
#            eth_dst=mac_dst,
#            eth_src=mac_src,
#            dl_vlan_outer=20,
#            dl_vlan_pcp_outer=4,
#            dl_vlan_cfi_outer=1,
#            vlan_vid=10,
#            vlan_pcp=2,
#            dl_vlan_cfi=1,
#            ip_dst='10.10.10.1',
#            ip_src='192.168.0.1',
#            ip_tos=5,
#            ip_ecn=1,
#            ip_dscp=1,
#            ip_ttl=64,
#            tcp_sport=1234,
#            tcp_dport=80)
#        try:
#            print '#### NO ACL Applied ####'
#            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            self.ctc_send_packet( 0, str(pkt))
#            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_packets( pkt, [3])
#            print '#### NO ACL Applied ####'
#            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            self.ctc_send_packet( 1, str(pkt))
#            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_packets( pkt, [3])
#            print '#### NO ACL Applied ####'
#            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            self.ctc_send_packet( 2, str(pkt))
#            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_packets( pkt, [3])
#            print '#### NO ACL Applied ####'
#            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            self.ctc_send_packet( 16, str(pkt))
#            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_packets( pkt, [3])
#        finally:
#            print '----------------------------------------------------------------------------------------------'
#
#        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
#        # setup ACL to block based on Source IP
#        table_stage = SAI_ACL_STAGE_INGRESS
#        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_SWITCH]
#        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
#        action = SAI_PACKET_ACTION_DROP
#        in_ports = [port1, port2, port17]
#        mac_src_mask = "ff:ff:ff:ff:ff:ff"
#        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
#        svlan_id=20
#        svlan_pri=4
#        svlan_cfi=1
#        cvlan_id=10
#        cvlan_pri=2
#        cvlan_cfi=None
#        ip_type = SAI_ACL_IP_TYPE_IPV4ANY
#        mpls_label0_label = None
#        mpls_label0_ttl = None
#        mpls_label0_exp = None
#        mpls_label0_bos = None
#        mpls_label1_label = None
#        mpls_label1_ttl = None
#        mpls_label1_exp = None
#        mpls_label1_bos = None
#        mpls_label2_label = None
#        mpls_label2_ttl = None
#        mpls_label2_exp = None
#        mpls_label2_bos = None
#        mpls_label3_label = None
#        mpls_label3_ttl = None
#        mpls_label3_exp = None
#        mpls_label3_bos = None
#        mpls_label4_label = None
#        mpls_label4_ttl = None
#        mpls_label4_exp = None
#        mpls_label4_bos = None
#        ip_src = "192.168.0.1"
#        ip_src_mask = "255.255.255.255"
#        ip_dst = '10.10.10.1'
#        ip_dst_mask = "255.255.255.255"
#        ip_protocol = 6
#        ip_tos=5
#        ip_ecn=1
#        ip_dscp=1
#        ip_ttl=None
#        in_port = None
#        out_port = None
#        out_ports = None
#        src_l4_port = 1234
#        dst_l4_port = 80
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
#        addr_family = None
#
#        acl_table_id = sai_thrift_create_acl_table(self.client,
#            table_stage,
#            table_bind_point_list,
#            addr_family,
#            mac_src,
#            mac_dst,
#            ip_src,
#            ip_dst,
#            in_ports,
#            out_ports,
#            in_port,
#            out_port,
#            svlan_id,
#            svlan_pri,
#            svlan_cfi,
#            cvlan_id,
#            cvlan_pri,
#            cvlan_cfi,
#            ip_type,
#            mpls_label0_label,
#            mpls_label0_ttl,
#            mpls_label0_exp,
#            mpls_label0_bos,
#            mpls_label1_label,
#            mpls_label1_ttl,
#            mpls_label1_exp,
#            mpls_label1_bos,
#            mpls_label2_label,
#            mpls_label2_ttl,
#            mpls_label2_exp,
#            mpls_label2_bos,
#            mpls_label3_label,
#            mpls_label3_ttl,
#            mpls_label3_exp,
#            mpls_label3_bos,
#            mpls_label4_label,
#            mpls_label4_ttl,
#            mpls_label4_exp,
#            mpls_label4_bos,
#            ip_protocol,
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
#            ip_type,
#            mpls_label0_label,
#            mpls_label0_ttl,
#            mpls_label0_exp,
#            mpls_label0_bos,
#            mpls_label1_label,
#            mpls_label1_ttl,
#            mpls_label1_exp,
#            mpls_label1_bos,
#            mpls_label2_label,
#            mpls_label2_ttl,
#            mpls_label2_exp,
#            mpls_label2_bos,
#            mpls_label3_label,
#            mpls_label3_ttl,
#            mpls_label3_exp,
#            mpls_label3_bos,
#            mpls_label4_label,
#            mpls_label4_ttl,
#            mpls_label4_exp,
#            mpls_label4_bos,
#            ip_src, ip_src_mask,
#            ip_dst, ip_dst_mask,
#            ip_protocol,
#            ip_tos, ip_ecn,
#            ip_dscp, ip_ttl,
#            in_ports, out_ports,
#            in_port, out_port,
#            src_l4_port, dst_l4_port,
#            ingress_mirror_id,
#            egress_mirror_id,
#            new_svlan, new_scos,
#            new_cvlan, new_ccos,
#            deny_learn)
#
#        # bind this ACL table to port2s object id
#        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
#        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
#        self.client.sai_thrift_set_switch_attribute(attr)
#
#        warmboot(self.client)
#
#        try:
#            assert acl_table_id > 0, 'acl_entry_id is <= 0'
#            assert acl_entry_id > 0, 'acl_entry_id is <= 0'
#
#            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
#            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            # send the same packet
#            self.ctc_send_packet( 0, str(pkt))
#            # ensure packet is dropped
#            # check for absence of packet here!
#            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_no_packet( pkt, 3, default_time_out)
#
#            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
#            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            # send the same packet
#            self.ctc_send_packet( 1, str(pkt))
#            # ensure packet is dropped
#            # check for absence of packet here!
#            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_no_packet( pkt, 3, default_time_out)
#
#            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
#            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            # send the same packet
#            self.ctc_send_packet( 2, str(pkt))
#            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_packets( pkt, [3])
#
#            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
#            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            # send the same packet
#            self.ctc_send_packet( 16, str(pkt))
#            # ensure packet is dropped
#            # check for absence of packet here!
#            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_no_packet( pkt, 3, default_time_out)
#        finally:
#            print '----------------------------------------------------------------------------------------------'
#
#        in_port_list = [port2, port3, port17]
#        acl_port_list = sai_thrift_object_list_t(count=len(in_port_list), object_id_list=in_port_list)
#        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(objlist=acl_port_list)))
#        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_IN_PORTS, value=attribute_value)
#        self.client.sai_thrift_set_acl_entry_attribute(acl_entry_id, attribute)
#
#        warmboot(self.client)
#
#        try:
#            assert acl_table_id > 0, 'acl_entry_id is <= 0'
#            assert acl_entry_id > 0, 'acl_entry_id is <= 0'
#
#            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
#            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            # send the same packet
#            self.ctc_send_packet( 0, str(pkt))
#            # ensure packet is dropped
#            # check for absence of packet here!
#            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_packets( pkt, [3])
#
#            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
#            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            # send the same packet
#            self.ctc_send_packet( 1, str(pkt))
#            # ensure packet is dropped
#            # check for absence of packet here!
#            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_no_packet( pkt, 3, default_time_out)
#
#            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
#            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            # send the same packet
#            self.ctc_send_packet( 2, str(pkt))
#            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_no_packet( pkt, 3, default_time_out)
#
#            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
#            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
#            # send the same packet
#            self.ctc_send_packet( 16, str(pkt))
#            # ensure packet is dropped
#            # check for absence of packet here!
#            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
#            self.ctc_verify_no_packet( pkt, 3, default_time_out)
#        finally:
#            # unbind this ACL table from vlan object id
#            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
#            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
#            self.client.sai_thrift_set_switch_attribute(attr)
#
#            # cleanup ACL
#            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
#            self.client.sai_thrift_remove_acl_table(acl_table_id)
#            # cleanup FDB
#            sai_thrift_delete_fdb(self.client, vlan_oid, mac_dst, port4)
#
#            self.client.sai_thrift_remove_vlan(vlan_oid)

###############################

@group('acl')
class CreateParaellAclTableGroup(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_PARALLEL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
                                                               group_stage,
                                                               group_bind_point_list,
                                                               group_type)
        assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'

        # bind this ACL table to port0s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_group_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        warmboot(self.client)

        attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
        assert (status == SAI_STATUS_SUCCESS)

class CreateIgrParaAclTableGroupMember(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_PARALLEL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
            group_stage,
            group_bind_point_list,
            group_type)
        assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'

        # create ACL table
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = None
        mac_dst = None
        mac_src_mask = None
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        ip_protocol = None
        in_port = 0
        out_port = None
        out_ports = None
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
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None

        acl_table_id0 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id0 > 0, 'acl_table_id0 is <= 0'

        acl_table_id1 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id1 > 0, 'acl_table_id1 is <= 0'

        acl_table_id2 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id2 > 0, 'acl_table_id2 is <= 0'

        acl_table_id3 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id3 > 0, 'acl_table_id3 is <= 0'

        # setup ACL table group members
        group_member_priority0 = 0

        # create ACL table group members
        acl_table_group_member_id0 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id0,
                                                                              group_member_priority0)
        assert acl_table_group_member_id0 > 0, 'acl_table_group_member_id0 is <= 0'

        group_member_priority1 = 1

        # create ACL table group members
        acl_table_group_member_id1 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id1,
                                                                              group_member_priority1)
        assert acl_table_group_member_id1 > 0, 'acl_table_group_member_id1 is <= 0'

        group_member_priority2 = 2

        # create ACL table group members
        acl_table_group_member_id2 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id2,
                                                                              group_member_priority2)
        assert acl_table_group_member_id2 > 0, 'acl_table_group_member_id2 is <= 0'

        group_member_priority3 = 3

        # create ACL table group members
        acl_table_group_member_id3 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id3,
                                                                              group_member_priority3)
        assert acl_table_group_member_id3 == 0, 'acl_table_group_member_id3 is > 0'

        # bind this ACL table to port0s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_group_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        warmboot(self.client)

        attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        # remove acl table group member first
        status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id0)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id1)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id2)
        assert (status == SAI_STATUS_SUCCESS)

        # test there is no table in group
        # remove acl table
        status = self.client.sai_thrift_remove_acl_table(acl_table_id0)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_remove_acl_table(acl_table_id1)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_remove_acl_table(acl_table_id2)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_remove_acl_table(acl_table_id3)
        assert (status == SAI_STATUS_SUCCESS)

        #remove acl table group
        status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
        assert (status == SAI_STATUS_SUCCESS)

class CreateEgrParaAclTableGroupMember(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_EGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_PARALLEL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
            group_stage,
            group_bind_point_list,
            group_type)
        assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'

        # create ACL table
        table_stage = SAI_ACL_STAGE_EGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = None
        mac_dst = None
        mac_src_mask = None
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        ip_src = "192.168.0.1"
        ip_src_mask = "255.255.255.0"
        ip_dst = None
        ip_dst_mask = None
        ip_protocol = None
        in_port = None
        out_port = 0
        out_ports = None
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
        src_l4_port = None
        dst_l4_port = None
        ingress_mirror_id = None
        egress_mirror_id = None

        acl_table_id0 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id0 > 0, 'acl_table_id0 is <= 0'

        acl_table_id1 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id1 > 0, 'acl_table_id1 is <= 0'

        acl_table_id2 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id2 > 0, 'acl_table_id2 is <= 0'

        acl_table_id3 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id3 > 0, 'acl_table_id3 is <= 0'

        # setup ACL table group members
        group_member_priority0 = 0

        # create ACL table group members
        acl_table_group_member_id0 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id0,
                                                                              group_member_priority0)
        assert acl_table_group_member_id0 > 0, 'acl_table_group_member_id0 is <= 0'

        group_member_priority1 = 1

        # create ACL table group members
        acl_table_group_member_id1 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id1,
                                                                              group_member_priority1)
        assert acl_table_group_member_id1 > 0, 'acl_table_group_member_id1 is <= 0'

        group_member_priority2 = 2

        # create ACL table group members
        acl_table_group_member_id2 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id2,
                                                                              group_member_priority2)
        assert acl_table_group_member_id2 > 0, 'acl_table_group_member_id2 is <= 0'

        group_member_priority3 = 3

        # create ACL table group members
        acl_table_group_member_id3 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id3,
                                                                              group_member_priority3)
        assert acl_table_group_member_id3 == 0, 'acl_table_group_member_id3 is > 0'

        # bind this ACL table to port0s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_group_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        warmboot(self.client)

        # remove acl table group member first
        status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id0)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id1)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id2)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id3)
        assert (status == SAI_STATUS_ITEM_NOT_FOUND)

        # test there is no table in group
        # remove acl table
        status = self.client.sai_thrift_remove_acl_table(acl_table_id0)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_remove_acl_table(acl_table_id1)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_remove_acl_table(acl_table_id2)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_remove_acl_table(acl_table_id3)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        #remove acl table group
        status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
        assert (status == SAI_STATUS_SUCCESS)

class CreateIgrSeqAclMaxTable(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
            group_stage,
            group_bind_point_list,
            group_type)
        assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'

        # create ACL table
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = None
        mac_dst = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=1
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
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
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        ip_protocol = 6
        in_port = 0
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        addr_family = None

        acl_table_id_list = []
        acl_entry_id_list = []
        acl_table_group_member_id_list = []

        for a in range(0, 512):

            svlan_id = a
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
                                                       dst_l4_port)
            assert acl_table_id > 0, 'acl_table_id is <= 0'
            acl_table_id_list.append(acl_table_id)
            print 'append acl_table_id_list[', a, "]:0x%lx" %acl_table_id_list[a]

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
                                                       deny_learn)
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'
            acl_entry_id_list.append(acl_entry_id)
            print 'append acl_entry_id_list[', a, "]:0x%lx" %acl_entry_id_list[a]

            # setup ACL table group members
            group_member_priority = a

            # create ACL table group members
            acl_table_group_member_id = sai_thrift_create_acl_table_group_member(self.client,
                                                                                 acl_table_group_id,
                                                                                 acl_table_id,
                                                                                 group_member_priority)
            assert acl_table_group_member_id > 0, 'acl_table_group_member_id is <= 0'
            acl_table_group_member_id_list.append(acl_table_group_member_id)

        # bind this ACL table to port0s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_group_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        warmboot(self.client)

        attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        for a in range(0, 512):
            status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id_list[a])
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_acl_entry(acl_entry_id_list[a])
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_acl_table(acl_table_id_list[a])
            assert (status == SAI_STATUS_SUCCESS)

        #remove acl table group
        status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
        assert (status == SAI_STATUS_SUCCESS)

@group('acl')
class IgrParaAclEntryBindPointVlanTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_PARALLEL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
                                                               group_stage,
                                                               group_bind_point_list,
                                                               group_type)
        assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'

        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_id = 20
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sai_thrift_create_fdb(self.client, vlan_oid, mac_dst, port2, mac_action)

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_FORWARD
        in_ports = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=20
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=1
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
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        ip_protocol = 6
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        addr_family = None

        acl_table_id0 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id0 > 0, 'acl_entry_id0 is <= 0'

        acl_table_id1 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id1 > 0, 'acl_entry_id1 is <= 0'

        new_scos = 2
        new_ccos = 1
        acl_entry_id0 = sai_thrift_create_acl_entry(self.client,
                                                    acl_table_id0,
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
                                                    deny_learn)
        assert acl_entry_id0 > 0, 'acl_entry_id0 is <= 0'

        new_scos = None
        new_ccos = None
        deny_learn = True
        acl_entry_id1 = sai_thrift_create_acl_entry(self.client,
                                                    acl_table_id1,
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
                                                    deny_learn)
        assert acl_entry_id1 > 0, 'acl_entry_id1 is <= 0'

        # setup ACL table group members
        group_member_priority = None

        # create ACL table group members
        acl_table_group_member_id0 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id0,
                                                                              group_member_priority)
        assert acl_table_group_member_id0 > 0, 'acl_table_group_member_id0 is <= 0'

          # create ACL table group members
        acl_table_group_member_id1 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id1,
                                                                              group_member_priority)
        assert acl_table_group_member_id1 > 0, 'acl_table_group_member_id1 is <= 0'

        # bind this ACL group to vlan object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_group_id)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)

        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        warmboot(self.client)

        # send the test packet(s)
        tx_pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=4,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=2,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        tx_pkt2 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_src,
                                         eth_src=mac_dst,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=4,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=2,
                                         dl_vlan_cfi=1,
                                         ip_dst='192.168.0.1',
                                         ip_src='10.10.10.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=80,
                                         tcp_dport=1234)

        rx_pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=2,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=1,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        rx_pkt2 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_src,
                                         eth_src=mac_dst,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=2,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=1,
                                         dl_vlan_cfi=1,
                                         ip_dst='192.168.0.1',
                                         ip_src='10.10.10.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=80,
                                         tcp_dport=1234)

        try:
            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet(0, str(tx_pkt1))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(rx_pkt1, [1])

            #self.ctc_send_packet(1, str(tx_pkt2))
            #self.ctc_verify_no_packet(rx_pkt2, 0, default_time_out)

        finally:
            # unbind this ACL table from vlan object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            # remove acl table group member first
            status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id0)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id1)
            assert (status == SAI_STATUS_SUCCESS)

            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id0)
            self.client.sai_thrift_remove_acl_entry(acl_entry_id1)

            self.client.sai_thrift_remove_acl_table(acl_table_id0)
            self.client.sai_thrift_remove_acl_table(acl_table_id1)

            #remove acl table group
            status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
            assert (status == SAI_STATUS_SUCCESS)

            # cleanup FDB
            sai_thrift_delete_fdb(self.client, vlan_oid, mac_dst, port2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('acl')
class IgrSeqAclEntryBindPointVlanPrioTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS
        group_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_SEQUENTIAL

        # create ACL table group
        acl_table_group_id = sai_thrift_create_acl_table_group(self.client,
                                                               group_stage,
                                                               group_bind_point_list,
                                                               group_type)
        assert acl_table_group_id > 0, 'acl_table_group_id is <= 0'

        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_id = 20
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        sai_thrift_create_fdb(self.client, vlan_oid, mac_dst, port2, mac_action)

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_FORWARD
        in_ports = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=20
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=1
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
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        ip_protocol = 6
        in_port = None
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        addr_family = None

        acl_table_id0 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id0 > 0, 'acl_entry_id0 is <= 0'

        acl_table_id1 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id1 > 0, 'acl_entry_id1 is <= 0'

        new_scos = 2
        new_ccos = 1
        acl_entry_id0 = sai_thrift_create_acl_entry(self.client,
                                                    acl_table_id0,
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
                                                    deny_learn)
        assert acl_entry_id0 > 0, 'acl_entry_id0 is <= 0'

        new_scos = None
        new_ccos = None
        deny_learn = True
        acl_entry_id1 = sai_thrift_create_acl_entry(self.client,
                                                    acl_table_id1,
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
                                                    deny_learn)
        assert acl_entry_id1 > 0, 'acl_entry_id1 is <= 0'

        # setup ACL table group members
        group_member_priority = 1

        # create ACL table group members
        acl_table_group_member_id0 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id0,
                                                                              group_member_priority)
        assert acl_table_group_member_id0 > 0, 'acl_table_group_member_id0 is <= 0'

        group_member_priority = 0
          # create ACL table group members
        acl_table_group_member_id1 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id,
                                                                              acl_table_id1,
                                                                              group_member_priority)
        assert acl_table_group_member_id1 > 0, 'acl_table_group_member_id1 is <= 0'

        # bind this ACL group to vlan object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_group_id)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)

        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        warmboot(self.client)

        # send the test packet(s)
        tx_pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=4,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=2,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        tx_pkt2 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_src,
                                         eth_src=mac_dst,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=2,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=1,
                                         dl_vlan_cfi=1,
                                         ip_dst='192.168.0.1',
                                         ip_src='10.10.10.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=80,
                                         tcp_dport=1234)

        rx_pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=2,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=1,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        rx_pkt2 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_src,
                                         eth_src=mac_dst,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=2,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=1,
                                         dl_vlan_cfi=1,
                                         ip_dst='192.168.0.1',
                                         ip_src='10.10.10.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=80,
                                         tcp_dport=1234)


        try:
            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet(0, str(tx_pkt1))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(rx_pkt1, [1])

            self.ctc_send_packet(1, str(tx_pkt2))
            self.ctc_verify_packets(rx_pkt2, [0])

        finally:
            # unbind this ACL table from vlan object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            # remove acl table group member first
            status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id0)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id1)
            assert (status == SAI_STATUS_SUCCESS)

            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id0)
            self.client.sai_thrift_remove_acl_entry(acl_entry_id1)

            self.client.sai_thrift_remove_acl_table(acl_table_id0)
            self.client.sai_thrift_remove_acl_table(acl_table_id1)

            #remove acl table group
            status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id)
            assert (status == SAI_STATUS_SUCCESS)

            # cleanup FDB
            sai_thrift_delete_fdb(self.client, vlan_oid, mac_dst, port2)

            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('acl')
class IgrParaAclEntryPrioBetweenBindPointsTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        # setup ACL table group
        group_stage = SAI_ACL_STAGE_INGRESS

        group_bind_point_list0 = [SAI_ACL_BIND_POINT_TYPE_PORT]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_PARALLEL

        # create ACL table group
        acl_table_group_id0 = sai_thrift_create_acl_table_group(self.client,
                                                                group_stage,
                                                                group_bind_point_list0,
                                                                group_type)
        assert acl_table_group_id0 > 0, 'acl_table_group_id0 is <= 0'

        group_bind_point_list1 = [SAI_ACL_BIND_POINT_TYPE_VLAN]
        group_type = SAI_ACL_TABLE_GROUP_TYPE_PARALLEL

        # create ACL table group
        acl_table_group_id1 = sai_thrift_create_acl_table_group(self.client,
                                                                group_stage,
                                                                group_bind_point_list1,
                                                                group_type)
        assert acl_table_group_id1 > 0, 'acl_table_group_id1 is <= 0'

        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_id = 20
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sai_thrift_create_fdb(self.client, vlan_oid, mac_dst, port2, mac_action)

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_FORWARD
        in_ports = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=20
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=1
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
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        ip_protocol = 6
        in_port = 0
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = None
        addr_family = None

        acl_table_id0 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id0 > 0, 'acl_entry_id0 is <= 0'

        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_VLAN]
        acl_table_id1 = sai_thrift_create_acl_table(self.client,
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
        assert acl_table_id1 > 0, 'acl_entry_id1 is <= 0'

        new_scos = 5
        new_ccos = 3
        acl_entry_id0 = sai_thrift_create_acl_entry(self.client,
                                                    acl_table_id0,
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
                                                    deny_learn)
        assert acl_entry_id0 > 0, 'acl_entry_id0 is <= 0'

        new_scos = 6
        new_ccos = 4
        acl_entry_id1 = sai_thrift_create_acl_entry(self.client,
                                                    acl_table_id1,
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
                                                    deny_learn)
        assert acl_entry_id1 > 0, 'acl_entry_id1 is <= 0'

        # setup ACL table group members
        group_member_priority = None

        # create ACL table group members
        acl_table_group_member_id0 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id0,
                                                                              acl_table_id0,
                                                                              group_member_priority)
        assert acl_table_group_member_id0 > 0, 'acl_table_group_member_id0 is <= 0'

        # create ACL table group members
        acl_table_group_member_id1 = sai_thrift_create_acl_table_group_member(self.client,
                                                                              acl_table_group_id1,
                                                                              acl_table_id1,
                                                                              group_member_priority)
        assert acl_table_group_member_id1 > 0, 'acl_table_group_member_id1 is <= 0'

        # bind this ACL table to port0s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_group_id0)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        # bind this ACL group to vlan object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_group_id1)
        attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

        warmboot(self.client)

        # send the test packet(s)
        tx_pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=4,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=2,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        tx_pkt2 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=4,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=2,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        rx_pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=5,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=3,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        rx_pkt2 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=6,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=4,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        try:
            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet(0, str(tx_pkt1))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(rx_pkt1, [1])

        finally:
            # unbind this ACL table from vlan object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_VLAN_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_vlan_attribute(vlan_oid, attr)

            # remove acl table group member first
            status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id0)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_acl_table_group_member(acl_table_group_member_id1)
            assert (status == SAI_STATUS_SUCCESS)

            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id0)
            self.client.sai_thrift_remove_acl_entry(acl_entry_id1)

            self.client.sai_thrift_remove_acl_table(acl_table_id0)
            self.client.sai_thrift_remove_acl_table(acl_table_id1)

            #remove acl table group
            status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id0)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_acl_table_group(acl_table_group_id1)
            assert (status == SAI_STATUS_SUCCESS)

            # cleanup FDB
            sai_thrift_delete_fdb(self.client, vlan_oid, mac_dst, port2)

            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('acl')
class AclV4EntryRangeTypeTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        # the relationship between vlan id and vlan_oid
        vlan_id0 = 2
        vlan_oid0 = sai_thrift_create_vlan(self.client, vlan_id0)

        vlan_id1 = 20
        vlan_oid1 = sai_thrift_create_vlan(self.client, vlan_id1)

        acl_range_type_list = [SAI_ACL_RANGE_TYPE_OUTER_VLAN]
        acl_range_min = 2
        acl_range_max = 3
        acl_range_id0 = sai_thrift_create_acl_range(self.client, SAI_ACL_RANGE_TYPE_OUTER_VLAN, SAI_ACL_STAGE_INGRESS, acl_range_min, acl_range_max)
        acl_range_id_list0 = [acl_range_id0]
        print "acl_range_id0:0x%lx" %acl_range_id0

        acl_range_min = 20
        acl_range_max = 21
        acl_range_id1 = sai_thrift_create_acl_range(self.client, SAI_ACL_RANGE_TYPE_OUTER_VLAN, SAI_ACL_STAGE_INGRESS, acl_range_min, acl_range_max)
        acl_range_id_list1 = [acl_range_id1]
        print "acl_range_id1:0x%lx" %acl_range_id1

        sai_thrift_create_fdb(self.client, vlan_oid0, mac_dst, port2, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid1, mac_dst, port2, mac_action)

        # send the test packet(s)
        tx_pkt0 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=2,
                                         dl_vlan_pcp_outer=4,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=2,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        tx_pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=4,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=2,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        rx_pkt0 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=2,
                                         dl_vlan_pcp_outer=4,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=2,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        rx_pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                         eth_dst=mac_dst,
                                         eth_src=mac_src,
                                         dl_vlan_outer=20,
                                         dl_vlan_pcp_outer=4,
                                         dl_vlan_cfi_outer=1,
                                         vlan_vid=10,
                                         vlan_pcp=2,
                                         dl_vlan_cfi=1,
                                         ip_dst='10.10.10.1',
                                         ip_src='192.168.0.1',
                                         ip_tos=5,
                                         ip_ecn=1,
                                         ip_dscp=1,
                                         ip_ttl=64,
                                         tcp_sport=1234,
                                         tcp_dport=80)

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=2
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=1
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
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        ip_protocol = 6
        in_port = 0
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
        ingress_mirror_id = None
        egress_mirror_id = None
        admin_state = True
        #add vlan edit action
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        #deny learning
        deny_learn = True
        addr_family = None
        range_type = 1
        ingress_samplepacket = None

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
                                                   acl_range_type_list)

        svlan_id=2
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=1

        action = SAI_PACKET_ACTION_DROP
        acl_entry_id0 = sai_thrift_create_acl_entry(self.client,
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
                                                    ingress_samplepacket,
                                                    acl_range_id_list0)

        svlan_id=20
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=1

        action = SAI_PACKET_ACTION_FORWARD
        acl_entry_id1 = sai_thrift_create_acl_entry(self.client,
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
                                                    ingress_samplepacket,
                                                    acl_range_id_list0)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        #pdb.set_trace()

        warmboot(self.client)
        try:
            assert acl_table_id > 0, 'acl_table_id is <= 0'
            assert acl_entry_id0 > 0, 'acl_entry_id0 is <= 0'
            assert acl_entry_id1 > 0, 'acl_entry_id1 is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet(0, str(tx_pkt0))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet(rx_pkt0, 1, default_time_out)

            self.ctc_send_packet(0, str(tx_pkt1))
            self.ctc_verify_packets(rx_pkt1, [1])

        finally:
            # unbind this ACL table from vlan object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id0)
            self.client.sai_thrift_remove_acl_entry(acl_entry_id1)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup FDB
            sai_thrift_delete_fdb(self.client, vlan_oid0, mac_dst, port2)
            sai_thrift_delete_fdb(self.client, vlan_oid1, mac_dst, port2)

            self.client.sai_thrift_remove_acl_range(acl_range_id0)
            self.client.sai_thrift_remove_acl_range(acl_range_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid0)
            self.client.sai_thrift_remove_vlan(vlan_oid1)

@group('acl')
class AclV4EntryRedirectActionTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_mask = '255.255.255.255'
        dmac1 = '00:11:22:33:44:55'
        #dmac2 = '00:11:22:33:44:56'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_addr2, dmac1)

        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id3)

        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask, nhop1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr2, ip_mask, nhop2)

        # send the test packet(s)
        pkt0 = simple_qinq_tcp_packet(pktlen=100,
                                      eth_dst=router_mac,
                                      eth_src='00:22:22:22:22:22',
                                      dl_vlan_outer=20,
                                      dl_vlan_pcp_outer=4,
                                      dl_vlan_cfi_outer=1,
                                      vlan_vid=10,
                                      vlan_pcp=2,
                                      dl_vlan_cfi=1,
                                      ip_dst='10.10.10.1',
                                      ip_src='192.168.0.1',
                                      ip_tos=5,
                                      ip_ecn=1,
                                      ip_dscp=1,
                                      ip_ttl=64,
                                      tcp_sport=1234,
                                      tcp_dport=80)

        pkt1 = simple_qinq_tcp_packet(pktlen=100,
                                      eth_dst=router_mac,
                                      eth_src='00:22:22:22:22:22',
                                      dl_vlan_outer=20,
                                      dl_vlan_pcp_outer=4,
                                      dl_vlan_cfi_outer=1,
                                      vlan_vid=10,
                                      vlan_pcp=2,
                                      dl_vlan_cfi=1,
                                      ip_dst='10.10.10.2',
                                      ip_src='192.168.0.1',
                                      ip_tos=5,
                                      ip_ecn=1,
                                      ip_dscp=1,
                                      ip_ttl=64,
                                      tcp_sport=1234,
                                      tcp_dport=80)

        exp_pkt0 = simple_tcp_packet(pktlen=92,
                                     eth_dst='00:11:22:33:44:55',
                                     eth_src=router_mac,
                                     ip_dst='10.10.10.1',
                                     ip_src='192.168.0.1',
                                     ip_tos=5,
                                     ip_ecn=1,
                                     ip_dscp=1,
                                     ip_ttl=63,
                                     tcp_sport=1234,
                                     tcp_dport=80)

        exp_pkt1 = simple_tcp_packet(pktlen=92,
                                     eth_dst='00:11:22:33:44:55',
                                     eth_src=router_mac,
                                     ip_dst='10.10.10.2',
                                     ip_src='192.168.0.1',
                                     ip_tos=5,
                                     ip_ecn=1,
                                     ip_dscp=1,
                                     ip_ttl=63,
                                     tcp_sport=1234,
                                     tcp_dport=80)

        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet(1, str(pkt0))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(exp_pkt0, [0])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = None
        in_ports = None
        mac_src = '00:22:22:22:22:22'
        mac_dst = router_mac
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        svlan_id=20
        svlan_pri=4
        svlan_cfi=1
        cvlan_id=10
        cvlan_pri=2
        cvlan_cfi=None
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
        ip_dst = '10.10.10.2'
        ip_dst_mask = "255.255.255.255"
        ip_tos=5
        ip_ecn=1
        ip_dscp=1
        ip_ttl=None
        ip_protocol = 6
        in_port = 1
        out_port = None
        out_ports = None
        src_l4_port = 1234
        dst_l4_port = 80
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
        ingress_samplepacket = None
        acl_range_id_list = None
        redirect = nhop3

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
            dst_l4_port)

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
            deny_learn, ingress_samplepacket,
            acl_range_id_list, redirect)

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        #pdb.set_trace()
        warmboot(self.client)
        try:
            print '#### ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.2 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet(1, str(pkt1))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.2 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets(exp_pkt1, [2])

        finally:
            # unbind this ACL table from port2s object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)
            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask, nhop1)
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr2, ip_mask, nhop2)
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_addr2, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

###udf test
@group('acl')
class ACLTableUDFBindPointPortTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print
        print '----------------------------------------------------------------------------------------------'
        print "Sending packet ptf_intf 2 -> ptf_intf 1 (192.168.0.1 ---> 10.10.10.1 [id = 105])"

        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_mask1 = '255.255.255.255'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)

        # send the test packet(s)
        pkt = simple_qinq_tcp_packet(pktlen=100,
            eth_dst=router_mac,
            eth_src='00:22:22:22:22:22',
            dl_vlan_outer=20,
            dl_vlan_pcp_outer=4,
            dl_vlan_cfi_outer=1,
            vlan_vid=10,
            vlan_pcp=2,
            dl_vlan_cfi=1,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=64,
            tcp_sport=1234,
            tcp_dport=80)
        exp_pkt = simple_tcp_packet(pktlen=92,
            eth_dst='00:11:22:33:44:55',
            eth_src=router_mac,
            ip_dst='10.10.10.1',
            ip_src='192.168.0.1',
            ip_tos=5,
            ip_ecn=1,
            ip_dscp=1,
            ip_ttl=63,
            tcp_sport=1234,
            tcp_dport=80)

        try:
            print '#### NO ACL Applied ####'
            print '#### Sending  ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            self.ctc_send_packet(1, str(pkt))
            print '#### Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_packets( exp_pkt, [0])
        finally:
            print '----------------------------------------------------------------------------------------------'

        print "Sending packet ptf_intf 2 -[acl]-> ptf_intf 1 (192.168.0.1 -[acl]-> 10.10.10.1 [id = 105])"
        # setup ACL to block based on Source IP
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_SWITCH]
        entry_priority = SAI_SWITCH_ATTR_ACL_ENTRY_MINIMUM_PRIORITY
        action = SAI_PACKET_ACTION_DROP
        in_ports = [port1, port2]
        #mac_src = '00:22:22:22:22:22'
        #mac_dst = router_mac
        mac_src = None
        mac_dst = None
        mac_src_mask = "ff:ff:ff:ff:ff:ff"
        mac_dst_mask = "ff:ff:ff:ff:ff:ff"
        #svlan_id=20
        #svlan_pri=4
        #svlan_cfi=1
        #cvlan_id=10
        #cvlan_pri=2
        #cvlan_cfi=None
        svlan_id=None
        svlan_pri=None
        svlan_cfi=None
        cvlan_id=None
        cvlan_pri=None
        cvlan_cfi=None
        ip_type=None
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

        #ip_src = "192.168.0.1"
        #ip_src_mask = "255.255.255.255"
        #ip_dst = '10.10.10.1'
        #ip_dst_mask = "255.255.255.255"
        #ip_tos=5
        #ip_ecn=1
        #ip_dscp=1
        #ip_ttl=None
        #ip_protocol = None
        #in_port = 1
        #out_port = None
        #out_ports = None
        #src_l4_port = 1234
        #dst_l4_port = 80

        ip_src=None
        ip_src_mask=None
        ip_dst=None
        ip_dst_mask=None
        ip_tos=None
        ip_ecn=None
        ip_dscp=None
        ip_ttl=None
        ip_protocol=None
        in_port=None
        out_port=None
        out_ports=None
        src_l4_port=None
        dst_l4_port=None

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

        #DsAclQosUdfKey320.udf
        #"128'H0A0A0A01C0A800014006A5F000010000"

        udf0 = ctypes.c_int8(10)
        udf1 = ctypes.c_int8(10)
        udf2 = ctypes.c_int8(10)
        udf3 = ctypes.c_int8(1)

        udf4 = ctypes.c_int8(192)
        udf5 = ctypes.c_int8(168)
        udf6 = ctypes.c_int8(0)
        udf7 = ctypes.c_int8(1)

        udf8 = ctypes.c_int8(64)
        udf9 = ctypes.c_int8(6)
        udf10 = ctypes.c_int8(165)
        udf11 = ctypes.c_int8(240)

        udf12 = ctypes.c_int8(0)
        udf13 = ctypes.c_int8(1)
        udf14 = ctypes.c_int8(0)
        udf15 = ctypes.c_int8(0)

        group0_udf_value = [udf12.value, udf13.value, udf14.value, udf15.value, udf8.value, udf9.value, udf10.value, udf11.value, udf4.value, udf5.value, udf6.value, udf7.value, udf0.value, udf1.value, udf2.value, udf3.value]
        group0_udf_mask  = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  -1, -1, -1, -1, -1, -1]

        group_type = SAI_UDF_GROUP_TYPE_GENERIC
        group_length = 16

        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = 0x%lx" %udf_group_id

        #ipv4
        ether_type = 0x0800
        ether_type_mask = U16MASKFULL
        #tcp
        l3_header_protocol = None
        l3_header_protocol_mask = None
        #gre
        gre_type = None
        gre_type_mask = None
        #l4 port
        l4_src_port = 1234
        l4_src_port_mask = U16MASKFULL
        l4_dst_port = 80
        l4_dst_port_mask = U16MASKFULL
        #mpls label num
        mpls_label_num = None
        #entry proirity
        priority = 0

        udf_match_id = sai_thrift_create_udf_match(self.client,
                                                   ether_type,
                                                   ether_type_mask,
                                                   l3_header_protocol,
                                                   l3_header_protocol_mask,
                                                   gre_type,
                                                   gre_type_mask,
                                                   l4_src_port,
                                                   l4_src_port_mask,
                                                   l4_dst_port,
                                                   l4_dst_port_mask,
                                                   mpls_label_num,
                                                   priority)

        base = SAI_UDF_BASE_L3
        offset = 4
        # default value
        hash_mask_list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

        udf_entry_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, hash_mask_list)
        assert udf_entry_id > 0, 'udf_entry_id is <= 0'
        print "udf_entry_id = 0x%lx" %udf_entry_id

        user_define_filed_group0 = True

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
                    None,
                    user_define_filed_group0)

        assert acl_table_id > 0, 'acl_table_id is <= 0'
        print "acl_table_id = 0x%lx" %acl_table_id

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
                                      None,
                                      None,
                                      None,
                                      group0_udf_value,
                                      group0_udf_mask)

        assert acl_entry_id > 0, 'acl_entry_id is <= 0'
        print "acl_entry_id = 0x%lx" %acl_entry_id

        # bind this ACL table to port2s object id
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_id)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        warmboot(self.client)
        try:
            assert acl_table_id > 0, 'acl_entry_id is <= 0'
            assert acl_entry_id > 0, 'acl_entry_id is <= 0'

            print '#### ACL \'DROP, src 192.168.0.1/255.255.255.0, in_ports[ptf_intf_1,2]\' Applied ####'
            print '#### Sending      ', router_mac, '| 00:22:22:22:22:22 | 10.10.10.1 | 192.168.0.1 | @ ptf_intf 2'
            # send the same packet
            self.ctc_send_packet(1, str(pkt))
            # ensure packet is dropped
            # check for absence of packet here!
            print '#### NOT Expecting 00:11:22:33:44:55 |', router_mac, '| 10.10.10.1 | 192.168.0.1 | @ ptf_intf 1'
            self.ctc_verify_no_packet(exp_pkt, 0, default_time_out)

        finally:
            # unbind this ACL table from switch object id
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            # cleanup ACL
            self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            self.client.sai_thrift_remove_acl_table(acl_table_id)

            # cleanup
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            self.client.sai_thrift_remove_udf(udf_entry_id)
            self.client.sai_thrift_remove_udf_match(udf_match_id)
            self.client.sai_thrift_remove_udf_group(udf_group_id)
