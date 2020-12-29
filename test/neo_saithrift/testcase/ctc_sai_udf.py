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
Thrift SAI interface UDF tests
"""
import socket
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask
import pdb

@group('udf')
class fun_01_udf_group_create_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        UDF GROUP Create Test.
        Steps:
        1. Create UDF GROUP.
        2. get attribute and check
        3. clean up.
        """
        print ""
        switch_init(self.client)

        print type(testutils.test_params_get()['chipname'])
        print "the chipname %s" %testutils.test_params_get()['chipname']
        print testutils.test_params_get()['chipname']

        # setup udf group
        group_type = SAI_UDF_GROUP_TYPE_GENERIC
        group_length = 4

        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = %d" %udf_group_id
        print "udf_group_id = %u" %udf_group_id
        print "udf_group_id = %lu" %udf_group_id
        print "udf_group_id = %x" %udf_group_id
        print "udf_group_id = %lx" %udf_group_id

        warmboot(self.client)
        try:
            print "Get udf group attribute: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH"
            attrs = self.client.sai_thrift_get_udf_group_attribute(udf_group_id)
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_UDF_GROUP_ATTR_TYPE:
                    print "set group_type = %d" %group_type
                    print "get group_type = %d" %a.value.s32
                    if group_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_UDF_GROUP_ATTR_LENGTH:
                    print "set group_length = %d" %group_length
                    print "get group_length = %d" %a.value.u16
                    if group_length != a.value.u16:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_udf_group(udf_group_id)

class fun_02_udf_group_remove_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        UDF Group Remove Test.
        Steps:
        1. create UDF Group
        2. remove UDF Group
        3. get attribute and check
        5. clean up.
        """
        print ""
        switch_init(self.client)

        # setup udf group
        group_type = SAI_UDF_GROUP_TYPE_GENERIC
        group_length = 4

        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = %u" %udf_group_id
        print "udf_group_id = %lu" %udf_group_id
        print "udf_group_id = %x" %udf_group_id
        print "udf_group_id = %lx" %udf_group_id

        warmboot(self.client)
        try:
            print "Get udf group attribute: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH"
            attrs = self.client.sai_thrift_get_udf_group_attribute(udf_group_id)
            print "sai_thrift_get_udf_group_attribute; status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)

            print "sai_thrift_remove_udf_group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH"
            status=self.client.sai_thrift_remove_udf_group(udf_group_id)
            print "sai_thrift_remove_udf_group; status = %d" %status
            assert (status == SAI_STATUS_SUCCESS)

            print "Get udf group attribute: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH"
            attrs = self.client.sai_thrift_get_udf_group_attribute(udf_group_id)
            print "sai_thrift_get_udf_group_attribute; status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            print "Success!"

class fun_03_udf_group_get_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        UDF GROUP GET Test.
        Steps:
        1. Create UDF GROUP.
        2. get attribute and check
        3. clean up.
        """
        print ""
        switch_init(self.client)

        # setup udf group
        group_type = SAI_UDF_GROUP_TYPE_HASH
        group_length = 4

        print "Create udf group: udf_group_type = SAI_UDF_GROUP_TYPE_HASH, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = %d" %udf_group_id
        print "udf_group_id = %u" %udf_group_id
        print "udf_group_id = %lu" %udf_group_id
        print "udf_group_id = %x" %udf_group_id
        print "udf_group_id = %lx" %udf_group_id

        warmboot(self.client)
        try:
            print "Get udf group attribute: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH"
            attrs = self.client.sai_thrift_get_udf_group_attribute(udf_group_id)
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_UDF_GROUP_ATTR_TYPE:
                    print "set group_type = %d" %group_type
                    print "get group_type = %d" %a.value.s32
                    if group_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_UDF_GROUP_ATTR_LENGTH:
                    print "set group_length = %d" %group_length
                    print "get group_length = %d" %a.value.u16
                    if group_length != a.value.u16:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_udf_group(udf_group_id)

class fun_04_udf_match_create_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):
        """
        UDF MATCH Create Test.
        Steps:
        1. Create UDF MATCH.
        2. get attribute and check
        3. clean up.
        """
        print ""
        switch_init(self.client)

        # setup udf match  zhuan buma
        print "Create udf match:"
        l2_type = 0x1122
        #l2_type = 0x86DD
        l2_type_mask = U16MASKFULL
        l3_type = 57
        l3_type_mask = 0x0F
        gre_type = 0x22eb
        gre_type_mask = U16MASKFULL
        mpls_label_num = 2
        l4_src_port = 0x1234
        l4_src_port_mask = U16MASKFULL
        l4_dst_port = 0x4321
        l4_dst_port_mask = U16MASKFULL
        priority = 15

        udf_match_id = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   l3_type,
                                                   l3_type_mask,
                                                   gre_type,
                                                   gre_type_mask,
                                                   l4_src_port,
                                                   l4_src_port_mask,
                                                   l4_dst_port,
                                                   l4_dst_port_mask,
                                                   mpls_label_num,
                                                   priority)

        print "udf_match_id = %d"    %udf_match_id
        print "udf_match_id = %u"    %udf_match_id
        print "udf_match_id = %lu"   %udf_match_id
        print "udf_match_id = 0x%x " %udf_match_id
        print "udf_match_id = 0x%lx" %udf_match_id

        udf_match_id0 = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   l3_type,
                                                   l3_type_mask,
                                                   gre_type,
                                                   gre_type_mask,
                                                   l4_src_port,
                                                   l4_src_port_mask,
                                                   l4_dst_port,
                                                   l4_dst_port_mask,
                                                   mpls_label_num,
                                                   priority)
        assert(udf_match_id0 == SAI_NULL_OBJECT_ID)

        print "udf_match_id = %d"    %udf_match_id0
        print "udf_match_id = %u"    %udf_match_id0
        print "udf_match_id = %lu"   %udf_match_id0
        print "udf_match_id = 0x%x " %udf_match_id0
        print "udf_match_id = 0x%lx" %udf_match_id0

        warmboot(self.client)
        try:
            print "Get udf match attribute:"

            attrs = self.client.sai_thrift_get_udf_match_attribute(udf_match_id)
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_UDF_MATCH_ATTR_L2_TYPE:
                    print "set l2_type = 0x%x" %l2_type
                    print "get l2_type = 0x%x" %a.value.aclfield.data.u16
                    if l2_type != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set l2_type_mask = 0x%x" %l2_type_mask
                    print "get l2_type_mask = 0x%x" %a.value.aclfield.mask.u16
                    if l2_type_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_L3_TYPE:
                    print "set l3_type = %d" %l3_type
                    print "get l3_type = %d" %a.value.aclfield.data.u8
                    if l3_type != a.value.aclfield.data.u8:
                        raise NotImplementedError()
                    print "set l3_type_mask = 0x%x" %l3_type_mask
                    print "get l3_type_mask = 0x%x" %a.value.aclfield.mask.u8
                    if l3_type_mask != a.value.aclfield.mask.u8:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_GRE_TYPE:
                    print "set gre_type = 0x%x" %gre_type
                    print "get gre_type = 0x%x" %a.value.aclfield.data.u16
                    if gre_type != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set gre_type_mask = 0x%x" %gre_type_mask
                    print "get gre_type_mask = 0x%x" %a.value.aclfield.mask.u16
                    if gre_type_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_PRIORITY:
                    print "set priority = %d" %priority
                    print "get priority = %d" %a.value.u8
                    if priority != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_CUSTOM_MPLS_LABEL_NUM:
                    print "set mpls_label_num = %d" %mpls_label_num
                    print "get mpls_label_num = %d" %a.value.u8
                    if mpls_label_num != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_CUSTOM_L4_SRC_PORT:
                    print "set l4_src_port = 0x%x" %l4_src_port
                    print "get l4_src_port = 0x%x" %a.value.aclfield.data.u16
                    if l4_src_port != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set l4_src_port_mask = 0x%x" %l4_src_port_mask
                    print "get l4_src_port_mask = 0x%x" %a.value.aclfield.mask.u16
                    if l4_src_port_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_CUSTOM_L4_DST_PORT:
                    print "set l4_dst_port = 0x%x" %l4_dst_port
                    print "get l4_dst_port = 0x%x" %a.value.aclfield.data.u16
                    if l4_dst_port != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set l4_dst_port_mask = 0x%x" %l4_dst_port_mask
                    print "get l4_dst_port_mask = 0x%x" %a.value.aclfield.mask.u16
                    if l4_dst_port_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_udf_match(udf_match_id)

class fun_05_udf_match_remove_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        UDF Match Remove Test.
        Steps:
        1. create UDF Match
        2. remove UDF Match
        3. get attribute and check
        5. clean up.
        """
        print ""
        switch_init(self.client)

        print "Create udf match:"
        l2_type = 0x1122
        #l2_type = 0x86DD
        l2_type_mask = U16MASKFULL
        l3_type = 57
        l3_type_mask = 0x0F
        gre_type = 0x22eb
        gre_type_mask = U16MASKFULL
        mpls_label_num = 2
        l4_src_port = 0x1234
        l4_src_port_mask = U16MASKFULL
        l4_dst_port = 0x4321
        l4_dst_port_mask = U16MASKFULL
        priority = 15

        udf_match_id = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   l3_type,
                                                   l3_type_mask,
                                                   gre_type,
                                                   gre_type_mask,
                                                   l4_src_port,
                                                   l4_src_port_mask,
                                                   l4_dst_port,
                                                   l4_dst_port_mask,
                                                   mpls_label_num,
                                                   priority)

        print "udf_match_id = %d"    %udf_match_id
        print "udf_match_id = %u"    %udf_match_id
        print "udf_match_id = %lu"   %udf_match_id
        print "udf_match_id = 0x%x"  %udf_match_id
        print "udf_match_id = 0x%lx" %udf_match_id

        warmboot(self.client)
        try:
            print "Get udf match attribute:"
            attrs = self.client.sai_thrift_get_udf_match_attribute(udf_match_id)
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_UDF_MATCH_ATTR_L2_TYPE:
                    print "set l2_type = 0x%x" %l2_type
                    print "get l2_type = 0x%x" %a.value.aclfield.data.u16
                    if l2_type != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set l2_type_mask = 0x%x" %l2_type_mask
                    print "get l2_type_mask = 0x%x" %a.value.aclfield.mask.u16
                    if l2_type_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_L3_TYPE:
                    print "set l3_type = %d" %l3_type
                    print "get l3_type = %d" %a.value.aclfield.data.u8
                    if l3_type != a.value.aclfield.data.u8:
                        raise NotImplementedError()
                    print "set l3_type_mask = 0x%x" %l3_type_mask
                    print "get l3_type_mask = 0x%x" %a.value.aclfield.mask.u8
                    if l3_type_mask != a.value.aclfield.mask.u8:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_GRE_TYPE:
                    print "set gre_type = 0x%x" %gre_type
                    print "get gre_type = 0x%x" %a.value.aclfield.data.u16
                    if gre_type != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set gre_type_mask = 0x%x" %gre_type_mask
                    print "get gre_type_mask = 0x%x" %a.value.aclfield.mask.u16
                    if gre_type_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_PRIORITY:
                    print "set priority = %d" %priority
                    print "get priority = %d" %a.value.u8
                    if priority != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_CUSTOM_MPLS_LABEL_NUM:
                    print "set mpls_label_num = %d" %mpls_label_num
                    print "get mpls_label_num = %d" %a.value.u8
                    if mpls_label_num != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_CUSTOM_L4_SRC_PORT:
                    print "set l4_src_port = 0x%x" %l4_src_port
                    print "get l4_src_port = 0x%x" %a.value.aclfield.data.u16
                    if l4_src_port != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set l4_src_port_mask = 0x%x" %l4_src_port_mask
                    print "get l4_src_port_mask = 0x%x" %a.value.aclfield.mask.u16
                    if l4_src_port_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_CUSTOM_L4_DST_PORT:
                    print "set l4_dst_port = 0x%x" %l4_dst_port
                    print "get l4_dst_port = 0x%x" %a.value.aclfield.data.u16
                    if l4_dst_port != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set l4_dst_port_mask = 0x%x" %l4_dst_port_mask
                    print "get l4_dst_port_mask = 0x%x" %a.value.aclfield.mask.u16
                    if l4_dst_port_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()

            print "sai_thrift_remove_udf_match:"
            status=self.client.sai_thrift_remove_udf_match(udf_match_id)
            print "sai_thrift_remove_udf_match; status = %d" %status
            assert (status == SAI_STATUS_SUCCESS)
            print "Get udf match attribute: "
            attrs = self.client.sai_thrift_get_udf_match_attribute(udf_match_id)
            print "sai_thrift_get_udf_match_attribute; status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            print "Success!"

class fun_06_udf_match_get_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        UDF MATCH Create Test.
        Steps:
        1. Create UDF MATCH.
        2. get attribute and check
        3. clean up.
        """
        print ""
        switch_init(self.client)

        # setup udf match  zhuan buma
        print "Create udf match:"

        l2_type = 0x3456
        #l2_type = 0x86DD
        l2_type_mask = U16MASKFULL
        l3_type = 57
        l3_type_mask = 0x0F
        gre_type = 0x22eb
        gre_type_mask = U16MASKFULL
        priority = 15
        mpls_label_num = 2
        l4_src_port = 0x1234
        l4_src_port_mask = U16MASKFULL
        l4_dst_port = 0x4321
        l4_dst_port_mask = U16MASKFULL

        udf_match_id = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   l3_type,
                                                   l3_type_mask,
                                                   gre_type,
                                                   gre_type_mask,
                                                   l4_src_port,
                                                   l4_src_port_mask,
                                                   l4_dst_port,
                                                   l4_dst_port_mask,
                                                   mpls_label_num,
                                                   priority)

        print "udf_match_id = %d" %udf_match_id
        print "udf_match_id = %u" %udf_match_id
        print "udf_match_id = %lu" %udf_match_id
        print "udf_match_id = 0x%x" %udf_match_id
        print "udf_match_id = 0x%lx" %udf_match_id

        warmboot(self.client)
        try:
            print "Get udf match attribute:"
            attrs = self.client.sai_thrift_get_udf_match_attribute(udf_match_id)
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_UDF_MATCH_ATTR_L2_TYPE:
                    print "set l2_type = 0x%x" %l2_type
                    print "get l2_type = 0x%x" %a.value.aclfield.data.u16
                    if l2_type != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set l2_type_mask = 0x%x" %l2_type_mask
                    print "get l2_type_mask = 0x%x" %a.value.aclfield.mask.u16
                    if l2_type_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_L3_TYPE:
                    print "set l3_type = %d" %l3_type
                    print "get l3_type = %d" %a.value.aclfield.data.u8
                    if l3_type != a.value.aclfield.data.u8:
                        raise NotImplementedError()
                    print "set l3_type_mask = 0x%x" %l3_type_mask
                    print "get l3_type_mask = 0x%x" %a.value.aclfield.mask.u8
                    if l3_type_mask != a.value.aclfield.mask.u8:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_GRE_TYPE:
                    print "set gre_type = 0x%x" %gre_type
                    print "get gre_type = 0x%x" %a.value.aclfield.data.u16
                    if gre_type != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set gre_type_mask = 0x%x" %gre_type_mask
                    print "get gre_type_mask = 0x%x" %a.value.aclfield.mask.u16
                    if gre_type_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_PRIORITY:
                    print "set priority = %d" %priority
                    print "get priority = %d" %a.value.u8
                    if priority != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_CUSTOM_MPLS_LABEL_NUM:
                    print "set mpls_label_num = %d" %mpls_label_num
                    print "get mpls_label_num = %d" %a.value.u8
                    if mpls_label_num != a.value.u8:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_CUSTOM_L4_SRC_PORT:
                    print "set l4_src_port = 0x%x" %l4_src_port
                    print "get l4_src_port = 0x%x" %a.value.aclfield.data.u16
                    if l4_src_port != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set l4_src_port_mask = 0x%x" %l4_src_port_mask
                    print "get l4_src_port_mask = 0x%x" %a.value.aclfield.mask.u16
                    if l4_src_port_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()

                if a.id == SAI_UDF_MATCH_ATTR_CUSTOM_L4_DST_PORT:
                    print "set l4_dst_port = 0x%x" %l4_dst_port
                    print "get l4_dst_port = 0x%x" %a.value.aclfield.data.u16
                    if l4_dst_port != a.value.aclfield.data.u16:
                        raise NotImplementedError()
                    print "set l4_dst_port_mask = 0x%x" %l4_dst_port_mask
                    print "get l4_dst_port_mask = 0x%x" %a.value.aclfield.mask.u16
                    if l4_dst_port_mask != a.value.aclfield.mask.u16:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_udf_match(udf_match_id)

class fun_07_udf_create_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        UDF Create Test.
        Steps:
        1. Create UDF.
        2. get attribute and check
        3. clean up.
        """
        print ""
        switch_init(self.client)

        #setup udf group
        group_type = SAI_UDF_GROUP_TYPE_HASH
        group_length = 16

        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = %lx" %udf_group_id

        # setup udf match  zhuan buma
        print "Create udf match:"

        l2_type = 0x1122
        #l2_type = 0x86DD
        l2_type_mask = U16MASKFULL
        l3_type = 57
        l3_type_mask = 0x0F
        gre_type = 0x22eb
        gre_type_mask = U16MASKFULL
        priority = 15

        udf_match_id = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   None,
                                                   None,
                                                   gre_type,
                                                   gre_type_mask,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   priority)

        print "udf_match_id = 0x%lx" %udf_match_id

        # setup udf
        base = SAI_UDF_BASE_L3
        offset = 4
        # default value
        hash_mask_list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        print "Create udf: "
        udf_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, hash_mask_list)

        print "udf_id = 0x%lx" %udf_id

        warmboot(self.client)
        try:
            print "Get udf attribute: "
            attrs = self.client.sai_thrift_get_udf_attribute(udf_id)
            print "udf_id = %lx" %udf_id
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            hash_mask_list_temp = [None]*len(hash_mask_list)
            for a in attrs.attr_list:
                if a.id == SAI_UDF_ATTR_MATCH_ID:
                    print "set udf_match_id = 0x%lx" %udf_match_id
                    print "get udf_match_id = 0x%lx" %a.value.oid
                    if udf_match_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_GROUP_ID:
                    print "set udf_group_id = 0x%lx" %udf_group_id
                    print "get udf_group_id = 0x%lx" %a.value.oid
                    if udf_group_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_BASE:
                    print "set base = %d" %base
                    print "get base = %d" %a.value.s32
                    if base != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_OFFSET:
                    print "set offset = %d" %offset
                    print "get offset = %d" %a.value.u16
                    if offset != a.value.u16:
                        raise NotImplementedError()

                if a.id == SAI_UDF_ATTR_HASH_MASK:
                    if a.value.u8list.count != len(hash_mask_list):
                        print "get hash mask list error!!! count: %d" % a.value.u8list.count
                        raise NotImplementedError()
                    for i in range(a.value.u8list.count):
                        hash_mask_list_temp[i] = a.value.u8list.u8list[i]
                    print "get hash_mask_list:  ", hash_mask_list_temp
                    if hash_mask_list_temp != hash_mask_list:
                        print "get hash mask list error!!!"
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_udf(udf_id)
            self.client.sai_thrift_remove_udf_match(udf_match_id)
            print "udf_match_id = 0x%lx" %udf_match_id
            self.client.sai_thrift_remove_udf_group(udf_group_id)

class fun_08_udf_remove_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        UDF Remove Test.
        Steps:
        1. Remove UDF.
        2. get attribute and check
        3. clean up.
        """
        print ""
        switch_init(self.client)
        #setup udf group
        group_type = SAI_UDF_GROUP_TYPE_GENERIC
        group_length = 4

        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = 0x%lx" %udf_group_id

        # setup udf match  zhuan buma
        print "Create udf match:"
        l2_type = 0x1122
        #l2_type = 0x86DD
        l2_type_mask = U16MASKFULL
        l3_type = 57
        l3_type_mask = 0x0F
        gre_type = 0x22eb
        gre_type_mask = U16MASKFULL
        priority = 15
        udf_match_id = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   None,
                                                   None,
                                                   gre_type,
                                                   gre_type_mask,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   priority)

        print "udf_match_id = 0x%lx" %udf_match_id

        # setup udf
        base = SAI_UDF_BASE_L3
        offset = 4
        print "Create udf: "

        #udf_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, hash_mask_list)
        udf_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, None)
        print "udf_id = 0x%lx" %udf_id

        warmboot(self.client)
        try:
            print "Get udf attribute: "
            attrs = self.client.sai_thrift_get_udf_attribute(udf_id)
            print "udf_id = 0x%lx" %udf_id
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:
                if a.id == SAI_UDF_ATTR_MATCH_ID:
                    print "set udf_match_id = 0x%lx" %udf_match_id
                    print "get udf_match_id = 0x%lx" %a.value.oid
                    if udf_match_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_GROUP_ID:
                    print "set udf_group_id = 0x%lx" %udf_group_id
                    print "get udf_group_id = 0x%lx" %a.value.oid
                    if udf_group_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_BASE:
                    print "set base = %d" %base
                    print "get base = %d" %a.value.s32
                    if base != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_OFFSET:
                    print "set offset = %d" %offset
                    print "get offset = %d" %a.value.u16
                    if offset != a.value.u16:
                        raise NotImplementedError()
            print "sai_thrift_remove_udf:"
            status=self.client.sai_thrift_remove_udf(udf_id)
            print "sai_thrift_remove_udf; status = %d" %status
            assert (status == SAI_STATUS_SUCCESS)
            print "Get udf attribute: "
            attrs = self.client.sai_thrift_get_udf_attribute(udf_id)
            print "sai_thrift_get_udf_attribute; status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
        finally:
            print "Success!"
            self.client.sai_thrift_remove_udf_match(udf_match_id)
            self.client.sai_thrift_remove_udf_group(udf_group_id)

class fun_09_udf_get_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        UDF Get Test.
        Steps:
        1. Get UDF.
        2. get attribute and check
        3. clean up.
        """
        print ""
        switch_init(self.client)

        #setup udf group
        group_type = SAI_UDF_GROUP_TYPE_HASH
        group_length = 4

        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = 0x%lx" %udf_group_id

        # setup udf match  zhuan buma
        print "Create udf match:"

        l2_type = 0x1122
        #l2_type = 0x86DD
        l2_type_mask = U16MASKFULL
        l3_type = 57
        l3_type_mask = 0x0F
        gre_type = 0x22eb
        gre_type_mask = U16MASKFULL
        priority = 15
        udf_match_id = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   None,
                                                   None,
                                                   gre_type,
                                                   gre_type_mask,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   priority)

        print "udf_match_id = 0x%lx" %udf_match_id

        # setup udf
        base = SAI_UDF_BASE_L3
        offset = 4
        hash_mask_list = [-1, -1, -1, -1]
        print "Create udf: "
        udf_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, hash_mask_list)

        print "udf_id = 0x%lx" %udf_id

        warmboot(self.client)
        try:
            print "Get udf attribute: "
            attrs = self.client.sai_thrift_get_udf_attribute(udf_id)
            print "udf_id = %lx" %udf_id
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            hash_mask_list_temp = [None]*len(hash_mask_list)
            for a in attrs.attr_list:
                if a.id == SAI_UDF_ATTR_MATCH_ID:
                    print "set udf_match_id = 0x%lx" %udf_match_id
                    print "get udf_match_id = 0x%lx" %a.value.oid
                    if udf_match_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_GROUP_ID:
                    print "set udf_group_id = 0x%lx" %udf_group_id
                    print "get udf_group_id = 0x%lx" %a.value.oid
                    if udf_group_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_BASE:
                    print "set base = %d" %base
                    print "get base = %d" %a.value.s32
                    if base != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_OFFSET:
                    print "set offset = %d" %offset
                    print "get offset = %d" %a.value.u16
                    if offset != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_HASH_MASK:
                    if a.value.u8list.count != len(hash_mask_list):
                        print "get hash mask list error!!! count: %d" % a.value.u8list.count
                        raise NotImplementedError()
                    for i in range(a.value.u8list.count):
                        hash_mask_list_temp[i] = a.value.u8list.u8list[i]
                    print "get hash_mask_list:  ",hash_mask_list_temp
                    if hash_mask_list_temp != hash_mask_list:
                        print "get hash mask list error!!!"
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_udf(udf_id)
            self.client.sai_thrift_remove_udf_match(udf_match_id)
            self.client.sai_thrift_remove_udf_group(udf_group_id)

class fun_10_udf_set_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        UDF Set Test.
        Steps:
        1. Get UDF.
        2. get attribute and check.
        3. Set UDF attribute.
        4. get attribute and check.
        5. clean up.
        """
        print ""
        switch_init(self.client)

        #setup udf group
        group_type = SAI_UDF_GROUP_TYPE_HASH
        group_length = 4
        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = 0x%lx" %udf_group_id

        # setup udf match  zhuan buma
        print "Create udf match:"
        l2_type = 0x1122
        #l2_type = 0x86DD
        l2_type_mask = U16MASKFULL
        l3_type = 57
        l3_type_mask = 0x0F
        gre_type = 0x22eb
        gre_type_mask = U16MASKFULL
        priority = 15
        udf_match_id = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   None,
                                                   None,
                                                   gre_type,
                                                   gre_type_mask,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   None,
                                                   priority)
        print "udf_match_id = 0x%lx" %udf_match_id

        # setup udf
        base = SAI_UDF_BASE_L3
        base_set = SAI_UDF_BASE_L4
        offset = 4
        hash_mask_list_set = [0, -1, 0, -1]
        hash_mask_list = [-1, -1, -1, -1]
        print "Create udf: "
        udf_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, hash_mask_list)
        print "udf_id = 0x%lx" %udf_id

        warmboot(self.client)
        try:
            print "Get udf attribute: "
            attrs = self.client.sai_thrift_get_udf_attribute(udf_id)
            print "udf_id = %lx" %udf_id
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            hash_mask_list_temp = [None]*len(hash_mask_list)
            for a in attrs.attr_list:
                if a.id == SAI_UDF_ATTR_MATCH_ID:
                    print "set udf_match_id = 0x%lx" %udf_match_id
                    print "get udf_match_id = 0x%lx" %a.value.oid
                    if udf_match_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_GROUP_ID:
                    print "set udf_group_id = 0x%lx" %udf_group_id
                    print "get udf_group_id = 0x%lx" %a.value.oid
                    if udf_group_id != a.value.oid:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_BASE:
                    print "set base = %d" %base
                    print "get base = %d" %a.value.s32
                    if base != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_OFFSET:
                    print "set offset = %d" %offset
                    print "get offset = %d" %a.value.u16
                    if offset != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_HASH_MASK:
                    if a.value.u8list.count != len(hash_mask_list):
                        print "get hash mask list error!!! count: %d" % a.value.u8list.count
                        raise NotImplementedError()
                    for i in range(a.value.u8list.count):
                        hash_mask_list_temp[i] = a.value.u8list.u8list[i]
                    print "get hash_mask_list:  ",hash_mask_list_temp
                    if hash_mask_list_temp != hash_mask_list:
                        print "get hash mask list error!!!"
                        raise NotImplementedError()
            print "Set udf attribute: SAI_UDF_ATTR_BASE not support"
            attr_value = sai_thrift_attribute_value_t(s32=base_set)
            attr = sai_thrift_attribute_t(id=SAI_UDF_ATTR_BASE, value=attr_value)
            status = self.client.sai_thrift_set_udf_attribute(udf_id, attr)
            print "udf_id = 0x%lx" %udf_id
            print "status = %d" %status
            assert (status != SAI_STATUS_SUCCESS)

            print "Set udf attribute: SAI_UDF_ATTR_HASH_MASK [0,-1,0,-1]"
            hash_mask_list_tmp = sai_thrift_u8_list_t(count=len(hash_mask_list_set), u8list=hash_mask_list_set)
            attribute5_value = sai_thrift_attribute_value_t(u8list=hash_mask_list_tmp)
            attribute5 = sai_thrift_attribute_t(id=SAI_UDF_ATTR_HASH_MASK,
                                                value=attribute5_value)
            status = self.client.sai_thrift_set_udf_attribute(udf_id, attribute5)
            print "udf_id = 0x%lx" %udf_id
            print "status = %d" %status
            assert (status == SAI_STATUS_SUCCESS)
            print "Get udf attribute: "
            attrs = self.client.sai_thrift_get_udf_attribute(udf_id)
            print "udf_id = 0x%lx" %udf_id
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            hash_mask_list_temp2 = [None]*len(hash_mask_list_set)
            for a in attrs.attr_list:
                if a.id == SAI_UDF_ATTR_MATCH_ID:
                    print "set udf_match_id = 0x%lx" %udf_match_id
                    print "get udf_match_id = 0x%lx" %a.value.oid
                    if udf_match_id != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_UDF_ATTR_GROUP_ID:
                    print "set udf_group_id = 0x%lx" %udf_group_id
                    print "get udf_group_id = 0x%lx" %a.value.oid
                    if udf_group_id != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_UDF_ATTR_BASE:
                    print "set base = %d" %base
                    print "get base = %d" %a.value.s32
                    if base != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_OFFSET:
                    print "set offset = %d" %offset
                    print "get offset = %d" %a.value.u16
                    if offset != a.value.u16:
                        raise NotImplementedError()

                if a.id == SAI_UDF_ATTR_HASH_MASK:
                    if a.value.u8list.count != len(hash_mask_list_set):
                        print "get hash mask list error!!! count: %d" % a.value.u8list.count
                        raise NotImplementedError()
                    for i in range(a.value.u8list.count):
                        hash_mask_list_temp2[i] = a.value.u8list.u8list[i]
                    print "get hash_mask_list:  ",hash_mask_list_temp2
                    if hash_mask_list_temp2 != hash_mask_list_set:
                        print "get hash mask list error!!!"
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_udf(udf_id)
            self.client.sai_thrift_remove_udf_match(udf_match_id)
            self.client.sai_thrift_remove_udf_group(udf_group_id)
# add one udf hash case

#@group('lag')
#class fun_11_udf_hash_l2_lag_test(sai_base_test.ThriftInterfaceDataPlane):
#    def runTest(self):
#        switch_init(self.client)
#
#        if 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate
#            print "Goldengate not UDF_HashL2LagTest, just pass for case"
#            return
#
#        #setup udf group
#        group_type = SAI_UDF_GROUP_TYPE_HASH
#        group_length = 4
#        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
#        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
#        print "udf_group_id = 0x%lx" %udf_group_id
#
#        # setup udf match  zhuan buma
#        l2_type = 0x0800
#        l2_type_mask = U16MASKFULL
#        priority = 15
#        print "Create udf match:"
#        udf_match_id = sai_thrift_create_udf_match(self.client,
#                               l2_type, l2_type_mask,
#                               None, None,
#                               None, None,
#                               priority)
#        print "udf_match_id = 0x%lx" %udf_match_id
#
#        # setup udf
#        base = SAI_UDF_BASE_L2
#        offset1 = 16
#        # default value
#        hash_mask_list1 = [-1, -1, 0, 0]
#        print "Create udf: "
#        udf_id1 =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset1, hash_mask_list1)
#        print "udf_id1 = 0x%lx" %udf_id1
#
#        base = SAI_UDF_BASE_L2
#        offset2 = 8
#        # default value
#        hash_mask_list2 = [-1, 0, 0, 0]
#        print "Create udf: "
#        udf_id2 =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset2, hash_mask_list2)
#        print "udf_id2 = 0x%lx" %udf_id2
#
#        base = SAI_UDF_BASE_L2
#        offset3 = 24
#        # default value
#        hash_mask_list3 = [-1, -1, -1, -1]
#        print "Create udf: "
#        udf_id3 =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset3, hash_mask_list3)
#        print "udf_id3 = 0x%lx" %udf_id3
#
#        base = SAI_UDF_BASE_L2
#        offset4 = 20
#        # default value
#        hash_mask_list4 = [-1, -1, -1, 0]
#        print "Create udf: "
#        udf_id4 =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset4, hash_mask_list4)
#        print "udf_id4 = 0x%lx" %udf_id4
#
#        vlan_id = 10
#        hash_id_lag = 0x201C
#        hash_id_ecmp = 0x1C
#        udf_group_list = [udf_group_id]
#        port1 = port_list[0]
#        port2 = port_list[1]
#        port3 = port_list[2]
#        port4 = port_list[3]
#        mac1 = '00:11:11:11:11:11'
#        mac2 = '00:22:22:22:22:22'
#        mac_action = SAI_PACKET_ACTION_FORWARD
#
#        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
#
#        lag_id1 = sai_thrift_create_lag(self.client, [])
#        print"lag:%lx" %lag_id1
#
#        """sai_thrift_vlan_remove_all_ports(self.client, switch.default_vlan.oid)"""
#        print "port:%lx" %port1
#        print "lag_id1:%lx" %lag_id1
#        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
#        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
#        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
#
#        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_id1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
#        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)
#
#        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
#        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
#        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)
#
#        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
#        self.client.sai_thrift_set_port_attribute(port4, attr)
#
#        sai_thrift_create_fdb(self.client, vlan_oid, mac1, lag_id1, mac_action)
#        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)
#
#        #UDF Group list
#        if udf_group_list:
#            hash_udf_group_list = sai_thrift_object_list_t(count=len(udf_group_list), object_id_list=udf_group_list)
#            attr_value = sai_thrift_attribute_value_t(objlist=hash_udf_group_list)
#            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_UDF_GROUP_LIST,
#                                                value=attr_value)
#            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
#
#        warmboot(self.client)
#        try:
#            # get hash attribute
#            print "Get Hash attribute: SAI_HASH_ATTR_UDF_GROUP_LIST = udf_group_id"
#            attrs = self.client.sai_thrift_get_hash_attribute(hash_id_lag)
#            print "status = %d" %attrs.status
#            assert (attrs.status == SAI_STATUS_SUCCESS)
#            udf_group_list_temp = [None]*len(udf_group_list)
#            for a in attrs.attr_list:
#                if a.id == SAI_HASH_ATTR_UDF_GROUP_LIST:
#                    print "udf_group_list cnt = %d" %a.value.objlist.count
#                    if a.value.objlist.count != len(udf_group_list):
#                        print "get udf group list error!!! count: %d" % a.value.objlist.count
#                        raise NotImplementedError()
#                    for i in range(a.value.objlist.count):
#                        udf_group_list_temp[i] = a.value.objlist.object_id_list[i]
#                    print "**************************************get udf_group_list_temp[0]: 0x%lx ",udf_group_list_temp[0]
#                    print "**************************************get udf_group_list: 0x%lx ",udf_group_list_temp
#                    if udf_group_list_temp != udf_group_list:
#                        print "get udf group list error!!!"
#                        raise NotImplementedError()
#
#            # get udf_id1 attribute
#            print "Get udf_id1 attribute: "
#            attrs = self.client.sai_thrift_get_udf_attribute(udf_id1)
#            print "udf_id1 = %lx" %udf_id1
#            print "status = %d" %attrs.status
#            assert (attrs.status == SAI_STATUS_SUCCESS)
#            hash_mask_list_temp = [None]*len(hash_mask_list1)
#            for a in attrs.attr_list:
#                if a.id == SAI_UDF_ATTR_MATCH_ID:
#                    print "set udf_match_id = 0x%lx" %udf_match_id
#                    print "get udf_match_id = 0x%lx" %a.value.oid
#                    if udf_match_id != a.value.oid:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_GROUP_ID:
#                    print "set udf_group_id = 0x%lx" %udf_group_id
#                    print "get udf_group_id = 0x%lx" %a.value.oid
#                    if udf_group_id != a.value.oid:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_BASE:
#                    print "set base = %d" %base
#                    print "get base = %d" %a.value.s32
#                    if base != a.value.s32:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_OFFSET:
#                    print "set offset1 = %d" %offset1
#                    print "get offset1 = %d" %a.value.u16
#                    if offset1 != a.value.u16:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_HASH_MASK:
#                    if a.value.u8list.count != len(hash_mask_list1):
#                        print "get hash mask list1 error!!! count: %d" % a.value.u8list.count
#                        raise NotImplementedError()
#                    for i in range(a.value.u8list.count):
#                        hash_mask_list_temp[i] = a.value.u8list.u8list[i]
#                    print "get hash_mask_list1:  ",hash_mask_list_temp
#                    if hash_mask_list_temp != hash_mask_list1:
#                        print "get hash mask list1 error!!!"
#                        raise NotImplementedError()
#
#            # get udf_id2 attribute
#            print "Get udf_id2 attribute: "
#            attrs = self.client.sai_thrift_get_udf_attribute(udf_id2)
#            print "udf_id2 = %lx" %udf_id2
#            print "status = %d" %attrs.status
#            assert (attrs.status == SAI_STATUS_SUCCESS)
#            hash_mask_list_temp = [None]*len(hash_mask_list2)
#            for a in attrs.attr_list:
#                if a.id == SAI_UDF_ATTR_MATCH_ID:
#                    print "set udf_match_id = 0x%lx" %udf_match_id
#                    print "get udf_match_id = 0x%lx" %a.value.oid
#                    if udf_match_id != a.value.oid:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_GROUP_ID:
#                    print "set udf_group_id = 0x%lx" %udf_group_id
#                    print "get udf_group_id = 0x%lx" %a.value.oid
#                    if udf_group_id != a.value.oid:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_BASE:
#                    print "set base = %d" %base
#                    print "get base = %d" %a.value.s32
#                    if base != a.value.s32:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_OFFSET:
#                    print "set offset2 = %d" %offset2
#                    print "get offset2 = %d" %a.value.u16
#                    if offset2 != a.value.u16:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_HASH_MASK:
#                    if a.value.u8list.count != len(hash_mask_list2):
#                        print "get hash mask list2 error!!! count: %d" % a.value.u8list.count
#                        raise NotImplementedError()
#                    for i in range(a.value.u8list.count):
#                        hash_mask_list_temp[i] = a.value.u8list.u8list[i]
#                    print "get hash_mask_list2:  ",hash_mask_list_temp
#                    if hash_mask_list_temp != hash_mask_list2:
#                        print "get hash mask list2 error!!!"
#                        raise NotImplementedError()
#
#            # get udf_id3 attribute
#            print "Get udf_id3 attribute: "
#            attrs = self.client.sai_thrift_get_udf_attribute(udf_id3)
#            print "udf_id3 = %lx" %udf_id3
#            print "status = %d" %attrs.status
#            assert (attrs.status == SAI_STATUS_SUCCESS)
#            hash_mask_list_temp = [None]*len(hash_mask_list3)
#            for a in attrs.attr_list:
#                if a.id == SAI_UDF_ATTR_MATCH_ID:
#                    print "set udf_match_id = 0x%lx" %udf_match_id
#                    print "get udf_match_id = 0x%lx" %a.value.oid
#                    if udf_match_id != a.value.oid:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_GROUP_ID:
#                    print "set udf_group_id = 0x%lx" %udf_group_id
#                    print "get udf_group_id = 0x%lx" %a.value.oid
#                    if udf_group_id != a.value.oid:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_BASE:
#                    print "set base = %d" %base
#                    print "get base = %d" %a.value.s32
#                    if base != a.value.s32:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_OFFSET:
#                    print "set offset3 = %d" %offset3
#                    print "get offset3 = %d" %a.value.u16
#                    if offset3 != a.value.u16:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_HASH_MASK:
#                    if a.value.u8list.count != len(hash_mask_list3):
#                        print "get hash mask list3 error!!! count: %d" % a.value.u8list.count
#                        raise NotImplementedError()
#                    for i in range(a.value.u8list.count):
#                        hash_mask_list_temp[i] = a.value.u8list.u8list[i]
#                    print "get hash_mask_list3:  ",hash_mask_list_temp
#                    if hash_mask_list_temp != hash_mask_list3:
#                        print "get hash mask list3 error!!!"
#                        raise NotImplementedError()
#
#            # get udf_id4 attribute
#            print "Get udf_id4 attribute: "
#            attrs = self.client.sai_thrift_get_udf_attribute(udf_id4)
#            print "udf_id4 = %lx" %udf_id4
#            print "status = %d" %attrs.status
#            assert (attrs.status == SAI_STATUS_SUCCESS)
#            hash_mask_list_temp = [None]*len(hash_mask_list4)
#            for a in attrs.attr_list:
#                if a.id == SAI_UDF_ATTR_MATCH_ID:
#                    print "set udf_match_id = 0x%lx" %udf_match_id
#                    print "get udf_match_id = 0x%lx" %a.value.oid
#                    if udf_match_id != a.value.oid:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_GROUP_ID:
#                    print "set udf_group_id = 0x%lx" %udf_group_id
#                    print "get udf_group_id = 0x%lx" %a.value.oid
#                    if udf_group_id != a.value.oid:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_BASE:
#                    print "set base = %d" %base
#                    print "get base = %d" %a.value.s32
#                    if base != a.value.s32:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_OFFSET:
#                    print "set offset4 = %d" %offset4
#                    print "get offset4 = %d" %a.value.u16
#                    if offset4 != a.value.u16:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_ATTR_HASH_MASK:
#                    if a.value.u8list.count != len(hash_mask_list4):
#                        print "get hash mask list4 error!!! count: %d" % a.value.u8list.count
#                        raise NotImplementedError()
#                    for i in range(a.value.u8list.count):
#                        hash_mask_list_temp[i] = a.value.u8list.u8list[i]
#                    print "get hash_mask_list4:  ",hash_mask_list_temp
#                    if hash_mask_list_temp != hash_mask_list4:
#                        print "get hash mask list4 error!!!"
#                        raise NotImplementedError()
#
#            # get udf match attribute
#            print "Get udf match attribute:"
#            attrs = self.client.sai_thrift_get_udf_match_attribute(udf_match_id)
#            print "status = %d" %attrs.status
#            assert (attrs.status == SAI_STATUS_SUCCESS)
#            for a in attrs.attr_list:
#                if a.id == SAI_UDF_MATCH_ATTR_L2_TYPE:
#                    print "set l2_type = 0x%x" %l2_type
#                    print "get l2_type = 0x%x" %a.value.aclfield.data.u16
#                    if l2_type != a.value.aclfield.data.u16:
#                        raise NotImplementedError()
#                    print "set l2_type_mask = 0x%x" %l2_type_mask
#                    print "get l2_type_mask = 0x%x" %a.value.aclfield.mask.u16
#                    if l2_type_mask != a.value.aclfield.mask.u16:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_MATCH_ATTR_PRIORITY:
#                    print "set priority = %d" %priority
#                    print "get priority = %d" %a.value.u8
#                    if priority != a.value.u8:
#                        raise NotImplementedError()
#
#            # get udf group attribute
#            print "Get udf group attribute: udf_group_type = SAI_UDF_GROUP_TYPE_HASH, group_length = 4"
#            attrs = self.client.sai_thrift_get_udf_group_attribute(udf_group_id)
#            print "status = %d" %attrs.status
#            assert (attrs.status == SAI_STATUS_SUCCESS)
#            for a in attrs.attr_list:
#                if a.id == SAI_UDF_GROUP_ATTR_TYPE:
#                    print "set group_type = %d" %group_type
#                    print "get group_type = %d" %a.value.s32
#                    if group_type != a.value.s32:
#                        raise NotImplementedError()
#                if a.id == SAI_UDF_GROUP_ATTR_LENGTH:
#                    print "set group_length = %d" %group_length
#                    print "get group_length = %d" %a.value.u16
#                    if group_length != a.value.u16:
#                        raise NotImplementedError()
#
#            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
#                                    eth_dst='00:22:22:22:22:22',
#                                    ip_dst='10.0.0.1',
#                                    ip_id=109,
#                                    ip_ttl=64)
#            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
#                                    eth_dst='00:22:22:22:22:22',
#                                    ip_dst='10.0.0.1',
#                                    ip_id=109,
#                                    ip_ttl=64)
#            print "Sending packet port 1 (lag member) -> port 4"
#            self.ctc_send_packet( 0, str(pkt))
#            self.ctc_verify_packets( exp_pkt, [3])
#            print "Sending packet port 2 (lag member) -> port 4"
#            self.ctc_send_packet( 1, str(pkt))
#            self.ctc_verify_packets( exp_pkt, [3])
#            print "Sending packet port 3 (lag member) -> port 4"
#            self.ctc_send_packet( 2, str(pkt))
#            self.ctc_verify_packets( exp_pkt, [3])
#
#            #(gdb) p/x p_udf_group->hash_udf_bmp
#            #$24 = 0xf731
#            dump_status = self.client.sai_thrift_dump_log("UDF_HashL2LagTest.txt")
#            print "dump_status = %d" %dump_status
#            assert (dump_status == SAI_STATUS_SUCCESS)
#
#        finally:
#            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_id1)
#            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
#
#            self.client.sai_thrift_remove_vlan_member(vlan_member1)
#            self.client.sai_thrift_remove_vlan_member(vlan_member2)
#
#            sai_thrift_remove_lag_member(self.client, lag_member_id1)
#            sai_thrift_remove_lag_member(self.client, lag_member_id2)
#            sai_thrift_remove_lag_member(self.client, lag_member_id3)
#            sai_thrift_remove_lag(self.client, lag_id1)
#            self.client.sai_thrift_remove_vlan(vlan_oid)
#
#            for port in sai_port_list:
#                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
#
#            attr_value = sai_thrift_attribute_value_t(u16=1)
#            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
#            self.client.sai_thrift_set_port_attribute(port4, attr)
#
#            udf_group_list = []
#        #if udf_group_list:
#            hash_udf_group_list = sai_thrift_object_list_t(count=len(udf_group_list), object_id_list=udf_group_list)
#            attr_value = sai_thrift_attribute_value_t(objlist=hash_udf_group_list)
#            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_UDF_GROUP_LIST,
#                                                value=attr_value)
#            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
#
#            self.client.sai_thrift_remove_udf(udf_id1)
#            self.client.sai_thrift_remove_udf(udf_id2)
#            self.client.sai_thrift_remove_udf(udf_id3)
#            self.client.sai_thrift_remove_udf(udf_id4)
#            self.client.sai_thrift_remove_udf_match(udf_match_id)
#            self.client.sai_thrift_remove_udf_group(udf_group_id)

######################################################################

class fun_12_udf_group_max_entry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)

        # setup udf match  zhuan buma
        print "Create udf match:"

        #ipv4
        ether_type = 0x0800
        ether_type_mask = U16MASKFULL
        #tcp
        l3_header_protocol = 6
        l3_header_protocol_mask = U8MASKFULL
        #gre
        gre_type = None
        gre_type_mask = None
        #l4 port
        l4_src_port = 0x0000
        l4_src_port_mask = U16MASKFULL
        l4_dst_port = 0x0000
        l4_dst_port_mask = U16MASKFULL
        #mpls label num
        mpls_label_num = None
        #entry proirity
        priority = 0

        max_entry_num = 0
        if 'tsingma' == testutils.test_params_get()['chipname']:      # tsingma
            max_entry_num = 16
        elif 'tsingma_mx' == testutils.test_params_get()['chipname']: # tsingma_mx
            max_entry_num = 256

        priority_list = []
        for value in range(0, 128):
            priority_list.append(value)
        for value in range(-128, 0):
            priority_list.append(value)

        udf_match_oid_list = []
        for n in range(0, max_entry_num):

            udf_match_oid = sai_thrift_create_udf_match(self.client,
                                                        ether_type,
                                                        ether_type_mask,
                                                        l3_header_protocol,
                                                        l3_header_protocol_mask,
                                                        gre_type,
                                                        gre_type_mask,
                                                        (l4_src_port+n),
                                                        l4_src_port_mask,
                                                        (l4_dst_port+n),
                                                        l4_dst_port_mask,
                                                        mpls_label_num,
                                                        priority_list[n])
            assert udf_match_oid > 0, 'udf_match_oid is <= 0'
            print "udf_match_oid = 0x%lx" %udf_match_oid
            udf_match_oid_list.append(udf_match_oid)

        l4_src_port = 0x1200
        l4_src_port_mask = U16MASKFULL
        l4_dst_port = 0x0012
        l4_dst_port_mask = U16MASKFULL
        priority = 0

        udf_match_oid = sai_thrift_create_udf_match(self.client,
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
        print "udf_match_oid = 0x%lx" %udf_match_oid
        assert udf_match_oid == 0, 'udf_match_oid is != 0'

        group_type = SAI_UDF_GROUP_TYPE_GENERIC
        group_length = 16

        udf_group_oid0 = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_oid0 = 0x%lx" %udf_group_oid0
        assert udf_group_oid0 != 0, 'udf_group_oid0 is == 0'

        udf_group_oid1 = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_oid1 = 0x%lx" %udf_group_oid1
        assert udf_group_oid1 != 0, 'udf_group_oid1 is == 0'

        warmboot(self.client)
        try:
            base = SAI_UDF_BASE_L3
            offset = 4
            # default value
            hash_mask_list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

            udf_entry_oid_list = []
            for n in range(0, max_entry_num):
                udf_entry_oid =  sai_thrift_create_udf(self.client, udf_match_oid_list[n], udf_group_oid0, base, offset, hash_mask_list)
                assert udf_entry_oid > 0, 'udf_entry_oid is <= 0'
                print "udf_entry_oid = 0x%lx" %udf_entry_oid
                udf_entry_oid_list.append(udf_entry_oid)

            udf_entry_oid = sai_thrift_create_udf(self.client, udf_match_oid_list[0], udf_group_oid1, base, offset, hash_mask_list)
            assert udf_entry_oid == 0, 'udf_entry_oid is != 0'
            print "udf_entry_oid = 0x%lx" %udf_entry_oid

        finally:
            for n in range(0, max_entry_num):
                status = self.client.sai_thrift_remove_udf(udf_entry_oid_list[n])
                assert (status == SAI_STATUS_SUCCESS)

            for n in range(0, max_entry_num):
                status = self.client.sai_thrift_remove_udf_match(udf_match_oid_list[n])
                assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_udf_group(udf_group_oid0)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_udf_group(udf_group_oid1)
            assert (status == SAI_STATUS_SUCCESS)

class fun_13_udf_match_exclude_entry(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)

        #setup udf group
        group_type = SAI_UDF_GROUP_TYPE_GENERIC
        group_length = 16

        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = 0x%lx" %udf_group_id

        # setup udf match  zhuan buma
        print "Create udf match:"

        #ipv4
        ether_type = 0x0800
        ether_type_mask = U16MASKFULL
        #tcp
        l3_header_protocol = 6
        l3_header_protocol_mask = U8MASKFULL
        #gre
        gre_type = None
        gre_type_mask = None
        #l4 port
        l4_src_port = 0x1200
        l4_src_port_mask = U16MASKFULL
        l4_dst_port = 0x0021
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
        assert udf_match_id > 0, 'udf_match_id is <= 0'
        print "udf_match_id = 0x%lx" %udf_match_id

        base = SAI_UDF_BASE_L3
        offset = 4
        # default value
        hash_mask_list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

        udf_entry_id0 =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, hash_mask_list)
        assert udf_entry_id0 > 0, 'udf_entry_id is <= 0'
        print "udf_entry_id = 0x%lx" %udf_entry_id0

        udf_entry_id1 =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, hash_mask_list)
        assert udf_entry_id1 == 0, 'udf_entry_id is != 0'
        print "udf_entry_id = 0x%lx" %udf_entry_id1

        warmboot(self.client)
        try:
            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        finally:
            self.client.sai_thrift_remove_udf(udf_entry_id0)
            self.client.sai_thrift_remove_udf_match(udf_match_id)
            self.client.sai_thrift_remove_udf_group(udf_group_id)


class fun_14_udf_max_generic_groups(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        switch_init(self.client)

        # setup udf match  zhuan buma
        print "Create udf match:"

        #ipv4
        ether_type = 0x0800
        ether_type_mask = U16MASKFULL
        #tcp
        l3_header_protocol = 6
        l3_header_protocol_mask = U8MASKFULL
        #gre
        gre_type = None
        gre_type_mask = None
        #l4 port
        l4_src_port = 0x1200
        l4_src_port_mask = U16MASKFULL
        l4_dst_port = 0x0021
        l4_dst_port_mask = U16MASKFULL
        #mpls label num
        mpls_label_num = None
        #entry proirity
        priority = 0

        max_group_num = 0
        if 'tsingma' == testutils.test_params_get()['chipname']:      # tsingma
            max_group_num = 16
        elif 'tsingma_mx' == testutils.test_params_get()['chipname']: # tsingma_mx
            max_group_num = 256

        priority_list = []
        for value in range(0, 128):
            priority_list.append(value)
        for value in range(-128, 0):
            priority_list.append(value)

        udf_match_oid_list = []

        for n in range(0, max_group_num):

            udf_match_oid = sai_thrift_create_udf_match(self.client,
                                                        ether_type,
                                                        ether_type_mask,
                                                        l3_header_protocol,
                                                        l3_header_protocol_mask,
                                                        gre_type,
                                                        gre_type_mask,
                                                        (l4_src_port+n),
                                                        l4_src_port_mask,
                                                        (l4_dst_port+n),
                                                        l4_dst_port_mask,
                                                        mpls_label_num,
                                                        priority_list[n])
            assert udf_match_oid > 0, 'udf_match_oid is <= 0'
            print "udf_match_oid[%u] = 0x%lx" %(priority_list[n], udf_match_oid)
            udf_match_oid_list.append(udf_match_oid)

        group_type = SAI_UDF_GROUP_TYPE_GENERIC
        group_length = 16

        udf_group_oid_list = []
        for n in range(0, max_group_num):
            udf_group_oid = sai_thrift_create_udf_group(self.client, group_type, group_length)
            assert udf_group_oid > 0, 'udf_group_oid is <= 0'
            print "udf_group_oid = 0x%lx" %udf_group_oid
            udf_group_oid_list.append(udf_group_oid)

        base = SAI_UDF_BASE_L3
        offset = 4
        # default value
        hash_mask_list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

        udf_entry_oid_list = []
        for n in range(0, max_group_num):

            udf_entry_oid = sai_thrift_create_udf(self.client, udf_match_oid_list[n], udf_group_oid_list[n], base, offset, hash_mask_list)
            assert udf_entry_oid > 0, 'udf_entry_oid is <= 0'
            print "udf_entry_oid = 0x%lx" %udf_entry_oid
            udf_entry_oid_list.append(udf_entry_oid)

        warmboot(self.client)
        try:
            for n in range(0, max_group_num):

                print "Get udf attribute: "
                attrs = self.client.sai_thrift_get_udf_attribute(udf_entry_oid_list[n])
                print "udf_id = 0x%lx" %udf_entry_oid_list[n]
                print "status = %d" %attrs.status
                assert (attrs.status == SAI_STATUS_SUCCESS)

                for a in attrs.attr_list:
                    if a.id == SAI_UDF_ATTR_MATCH_ID:
                        print "set udf_match_oid = 0x%lx" %udf_match_oid_list[n]
                        print "get udf_match_oid = 0x%lx" %a.value.oid
                        if udf_match_oid_list[n] != a.value.oid:
                            raise NotImplementedError()
                    if a.id == SAI_UDF_ATTR_GROUP_ID:
                        print "set udf_group_oid = 0x%lx" %udf_group_oid_list[n]
                        print "get udf_group_oid = 0x%lx" %a.value.oid
                        if udf_group_oid_list[n] != a.value.oid:
                            raise NotImplementedError()
                    if a.id == SAI_UDF_ATTR_BASE:
                        print "set base = %d" %base
                        print "get base = %d" %a.value.s32
                        if base != a.value.s32:
                            raise NotImplementedError()
                    if a.id == SAI_UDF_ATTR_OFFSET:
                        print "set offset = %d" %offset
                        print "get offset = %d" %a.value.u16
                        if offset != a.value.u16:
                            raise NotImplementedError()

            for n in range(0, max_group_num):

                print "Get udf match attribute:"
                attrs = self.client.sai_thrift_get_udf_match_attribute(udf_match_oid_list[n])
                print "status = %d" %attrs.status
                assert (attrs.status == SAI_STATUS_SUCCESS)
                for a in attrs.attr_list:
                    if a.id == SAI_UDF_MATCH_ATTR_L2_TYPE:
                        print "set l2_type = 0x%x" %ether_type
                        print "get l2_type = 0x%x" %a.value.aclfield.data.u16
                        if ether_type != a.value.aclfield.data.u16:
                            raise NotImplementedError()
                        print "set l2_type_mask = 0x%x" %ether_type_mask
                        print "get l2_type_mask = 0x%x" %a.value.aclfield.mask.u16
                        if ether_type_mask != a.value.aclfield.mask.u16:
                            raise NotImplementedError()

                    if a.id == SAI_UDF_MATCH_ATTR_L3_TYPE:
                        print "set l3_type = %d" %l3_header_protocol
                        print "get l3_type = %d" %a.value.aclfield.data.u8
                        if l3_header_protocol != a.value.aclfield.data.u8:
                            raise NotImplementedError()
                        print "set l3_type_mask = 0x%x" %l3_header_protocol_mask
                        print "get l3_type_mask = 0x%x" %a.value.aclfield.mask.u8
                        if l3_header_protocol_mask != a.value.aclfield.mask.u8:
                            raise NotImplementedError()

                    if a.id == SAI_UDF_MATCH_ATTR_PRIORITY:
                        print "set priority = %d" %priority_list[n]
                        print "get priority = %d" %a.value.u8
                        if priority_list[n] != a.value.u8:
                            raise NotImplementedError()

                    if a.id == SAI_UDF_MATCH_ATTR_CUSTOM_L4_SRC_PORT:
                        print "set l4_src_port = 0x%x" %(l4_src_port+n)
                        print "get l4_src_port = 0x%x" %a.value.aclfield.data.u16
                        if (l4_src_port+n) != a.value.aclfield.data.u16:
                            raise NotImplementedError()
                        print "set l4_src_port_mask = 0x%x" %l4_src_port_mask
                        print "get l4_src_port_mask = 0x%x" %a.value.aclfield.mask.u16
                        if l4_src_port_mask != a.value.aclfield.mask.u16:
                            raise NotImplementedError()

                    if a.id == SAI_UDF_MATCH_ATTR_CUSTOM_L4_DST_PORT:
                        print "set l4_dst_port = 0x%x" %(l4_dst_port+n)
                        print "get l4_dst_port = 0x%x" %a.value.aclfield.data.u16
                        if (l4_dst_port+n) != a.value.aclfield.data.u16:
                            raise NotImplementedError()
                        print "set l4_dst_port_mask = 0x%x" %l4_dst_port_mask
                        print "get l4_dst_port_mask = 0x%x" %a.value.aclfield.mask.u16
                        if l4_dst_port_mask != a.value.aclfield.mask.u16:
                            raise NotImplementedError()

            print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

        finally:
            for n in range(0, max_group_num):
                self.client.sai_thrift_remove_udf(udf_entry_oid_list[n])

            for n in range(0, max_group_num):
                self.client.sai_thrift_remove_udf_match(udf_match_oid_list[n])

            for n in range(0, max_group_num):
                self.client.sai_thrift_remove_udf_group(udf_group_oid_list[n])

class scenario_01_ingress_acl_bind_switch_with_udf_key_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging(" step 1 basic data environment")
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

        sys_logging(" step 2 udf config ")
        group_type = SAI_UDF_GROUP_TYPE_GENERIC
        group_length = 16

        udf_group_oid = sai_thrift_create_udf_group(self.client, group_type, group_length)

        l2_type = 0x0800
        l2_type_mask = -1
        l3_type = 0x11
        l3_type_mask = -1
        gre_type = None
        gre_type_mask = -1
        mpls_label_num = None
        l4_src_port = 1234
        l4_src_port_mask = -1
        l4_dst_port = 5678
        l4_dst_port_mask = -1
        priority = 15

        udf_match_oid = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   l3_type,
                                                   l3_type_mask,
                                                   gre_type,
                                                   gre_type_mask,
                                                   l4_src_port,
                                                   l4_src_port_mask,
                                                   l4_dst_port,
                                                   l4_dst_port_mask,
                                                   mpls_label_num,
                                                   priority)

        base = SAI_UDF_BASE_L4
        offset = 8

        udf_oid =  sai_thrift_create_udf(self.client, udf_match_oid, udf_group_oid, base, offset, None)

        udf0 = ctypes.c_int8(17)
        udf1 = ctypes.c_int8(17)
        udf2 = ctypes.c_int8(17)
        udf3 = ctypes.c_int8(17)

        udf4 = ctypes.c_int8(34)
        udf5 = ctypes.c_int8(34)
        udf6 = ctypes.c_int8(34)
        udf7 = ctypes.c_int8(34)

        udf8 = ctypes.c_int8(0)
        udf9 = ctypes.c_int8(68)
        udf10 = ctypes.c_int8(86)
        udf11 = ctypes.c_int8(120)

        udf12 = ctypes.c_int8(0)
        udf13 = ctypes.c_int8(0)
        udf14 = ctypes.c_int8(0)
        udf15 = ctypes.c_int8(0)

        group0_udf_value = [udf12.value, udf13.value, udf14.value, udf15.value, udf8.value, udf9.value, udf10.value, udf11.value, udf4.value, udf5.value, udf6.value, udf7.value, udf0.value, udf1.value, udf2.value, udf3.value]
        group0_udf_mask  = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  -1, -1, -1, -1, -1, -1]

        sys_logging(" step 3 acl config ")

        # acl table info
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_SWITCH]

        action = SAI_PACKET_ACTION_DROP
        addr_family = None

        mac_src = None
        mac_src_mask = None
        mac_dst = None
        mac_dst_mask = None

        ip_src = None
        ip_src_mask = None
        ip_dst = None
        ip_dst_mask = None

        in_ports = None
        out_ports = None
        in_port = None
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

        ipv6_src = None
        ipv6_dst = None

        ipv6_src_mask = None
        ipv6_dst_mask = None
        ingress_samplepacket = None
        acl_range_id_list = None
        redirect = None

        src_l4_port = None
        dst_l4_port = None

        ingress_mirror = None
        egress_mirror = None
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        deny_learn = None

        acl_range_type_list = None

        user_define_filed_group0 = True

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
            dst_l4_port,
            ipv6_src,
            ipv6_dst,
            ip_tos,
            ip_ecn,
            ip_dscp,
            ip_ttl,
            acl_range_type_list,
            user_define_filed_group0)

        sys_logging("create acl table = %d" %acl_table_oid)
        assert(acl_table_oid != SAI_NULL_OBJECT_ID )

        entry_priority = 1
        admin_state = True

        # create acl entry
        acl_entry_oid = sai_thrift_create_acl_entry(self.client,
            acl_table_oid,
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
            ingress_mirror,
            egress_mirror,
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
            group0_udf_value,
            group0_udf_mask)

        sys_logging("create acl entry = %d" %acl_entry_oid)
        assert(acl_entry_oid != SAI_NULL_OBJECT_ID)

        warmboot(self.client)
        try:
            src_mac = mac1
            dst_mac = mac2
            src_ip = '1.2.3.4'
            dst_ip = '5.6.7.8'
            udp_src_port = 1234
            udp_dst_port = 5678
            ttl = 100
            tc = 0
            pkt_len = 100

            Sequence_Number = hexstr_to_ascii('11111111')
            Timestamp = hexstr_to_ascii('2222222200445678')

            npm_test_pkt = Sequence_Number + Timestamp
            pkt = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=False,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            sys_logging(" step4: none acl , packet will forwarding  ")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(pkt, [1])

            sys_logging(" step5: bind this ACL table to switch ")
            attr_value = sai_thrift_attribute_value_t(oid=acl_table_oid)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging(" step6: match drop acl entry ")
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_no_packet(pkt, 1)

        finally:
            sys_logging("clear config")

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            status = self.client.sai_thrift_remove_acl_entry(acl_entry_oid)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_acl_table(acl_table_oid)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

            self.client.sai_thrift_remove_udf(udf_oid)
            self.client.sai_thrift_remove_udf_match(udf_match_oid)
            self.client.sai_thrift_remove_udf_group(udf_group_oid)


class scenario_02_ingress_acl_bind_switch_with_multi_udf_key_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        sys_logging(" step 1 basic data environment")

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

        sys_logging(" step 2 udf config ")

        group_type = SAI_UDF_GROUP_TYPE_GENERIC
        group_length = 16

        udf_group_oid = sai_thrift_create_udf_group(self.client, group_type, group_length)

        l2_type = 0x0800
        l2_type_mask = -1
        l3_type = 0x11
        l3_type_mask = -1
        gre_type = None
        gre_type_mask = -1
        mpls_label_num = None
        l4_src_port = 1234
        l4_src_port_mask = -1
        l4_dst_port = None
        l4_dst_port_mask = -1
        priority = 1

        udf_match_oid = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   l3_type,
                                                   l3_type_mask,
                                                   gre_type,
                                                   gre_type_mask,
                                                   l4_src_port,
                                                   l4_src_port_mask,
                                                   l4_dst_port,
                                                   l4_dst_port_mask,
                                                   mpls_label_num,
                                                   priority)

        base = SAI_UDF_BASE_L4
        offset = 8

        udf_oid =  sai_thrift_create_udf(self.client, udf_match_oid, udf_group_oid, base, offset, None)


        l2_type = 0x0800
        l2_type_mask = -1
        l3_type = 0x11
        l3_type_mask = -1
        gre_type = None
        gre_type_mask = -1
        mpls_label_num = None
        l4_src_port = None
        l4_src_port_mask = -1
        l4_dst_port = 5678
        l4_dst_port_mask = -1
        priority = 2

        udf_match_oid_2 = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   l3_type,
                                                   l3_type_mask,
                                                   gre_type,
                                                   gre_type_mask,
                                                   l4_src_port,
                                                   l4_src_port_mask,
                                                   l4_dst_port,
                                                   l4_dst_port_mask,
                                                   mpls_label_num,
                                                   priority)

        base = SAI_UDF_BASE_L4
        offset = 8

        udf_oid_2 =  sai_thrift_create_udf(self.client, udf_match_oid_2, udf_group_oid, base, offset, None)



        l2_type = 0x0800
        l2_type_mask = -1
        l3_type = 0x11
        l3_type_mask = -1
        gre_type = None
        gre_type_mask = -1
        mpls_label_num = None
        l4_src_port = 1234
        l4_src_port_mask = -1
        l4_dst_port = 5678
        l4_dst_port_mask = -1
        priority = 3

        udf_match_oid_3 = sai_thrift_create_udf_match(self.client,
                                                   l2_type,
                                                   l2_type_mask,
                                                   l3_type,
                                                   l3_type_mask,
                                                   gre_type,
                                                   gre_type_mask,
                                                   l4_src_port,
                                                   l4_src_port_mask,
                                                   l4_dst_port,
                                                   l4_dst_port_mask,
                                                   mpls_label_num,
                                                   priority)

        base = SAI_UDF_BASE_L4
        offset = 8

        udf_oid_3 =  sai_thrift_create_udf(self.client, udf_match_oid_3, udf_group_oid, base, offset, None)

        udf0 = ctypes.c_int8(17)
        udf1 = ctypes.c_int8(17)
        udf2 = ctypes.c_int8(17)
        udf3 = ctypes.c_int8(17)

        udf4 = ctypes.c_int8(34)
        udf5 = ctypes.c_int8(34)
        udf6 = ctypes.c_int8(34)
        udf7 = ctypes.c_int8(34)

        udf8 = ctypes.c_int8(0)
        udf9 = ctypes.c_int8(68)
        udf10 = ctypes.c_int8(86)
        udf11 = ctypes.c_int8(120)

        udf12 = ctypes.c_int8(0)
        udf13 = ctypes.c_int8(0)
        udf14 = ctypes.c_int8(0)
        udf15 = ctypes.c_int8(0)

        group0_udf_value = [udf12.value, udf13.value, udf14.value, udf15.value, udf8.value, udf9.value, udf10.value, udf11.value, udf4.value, udf5.value, udf6.value, udf7.value, udf0.value, udf1.value, udf2.value, udf3.value]
        group0_udf_mask  = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  -1, -1, -1, -1, -1, -1]

        sys_logging(" step 3 acl config ")

        # acl table info
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_SWITCH]

        action = SAI_PACKET_ACTION_DROP
        addr_family = None

        mac_src = None
        mac_src_mask = None
        mac_dst = None
        mac_dst_mask = None

        ip_src = None
        ip_src_mask = None
        ip_dst = None
        ip_dst_mask = None

        in_ports = None
        out_ports = None
        in_port = None
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

        ipv6_src = None
        ipv6_dst = None

        ipv6_src_mask = None
        ipv6_dst_mask = None
        ingress_samplepacket = None
        acl_range_id_list = None
        redirect = None


        src_l4_port = None
        dst_l4_port = None

        ingress_mirror = None
        egress_mirror = None
        new_svlan = None
        new_scos = None
        new_cvlan = None
        new_ccos = None
        deny_learn = None

        acl_range_type_list = None

        user_define_filed_group0 = True

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
            dst_l4_port,
            ipv6_src,
            ipv6_dst,
            ip_tos,
            ip_ecn,
            ip_dscp,
            ip_ttl,
            acl_range_type_list,
            user_define_filed_group0)


        sys_logging("create acl table = %d" %acl_table_oid)
        assert(acl_table_oid != SAI_NULL_OBJECT_ID )

        entry_priority = 1
        admin_state = True

        # create acl entry
        acl_entry_oid = sai_thrift_create_acl_entry(self.client,
            acl_table_oid,
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
            ingress_mirror,
            egress_mirror,
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
            group0_udf_value,
            group0_udf_mask)

        sys_logging("create acl entry = %d" %acl_entry_oid)
        assert(acl_entry_oid != SAI_NULL_OBJECT_ID )

        warmboot(self.client)
        try:
            src_mac = mac1
            dst_mac = mac2
            src_ip = '1.2.3.4'
            dst_ip = '5.6.7.8'
            udp_src_port = 1234
            udp_dst_port = 5678
            ttl = 100
            tc = 0
            pkt_len = 100

            Sequence_Number = hexstr_to_ascii('11111111')
            Timestamp = hexstr_to_ascii('2222222200445678')

            npm_test_pkt = Sequence_Number + Timestamp
            pkt = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=False,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            pkt1 = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=False,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=1235,
                                    udp_dport=udp_dst_port,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            pkt2 = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=False,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=udp_src_port,
                                    udp_dport=5679,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)

            pkt3 = simple_udp_packet(pktlen=pkt_len-4,
                                    eth_dst=dst_mac,
                                    eth_src=src_mac,
                                    dl_vlan_enable=False,
                                    ip_src=src_ip,
                                    ip_dst=dst_ip,
                                    ip_tos=0,
                                    ip_ttl=ttl,
                                    udp_sport=1235,
                                    udp_dport=5679,
                                    ip_ihl=None,
                                    ip_id=0,
                                    ip_options=False,
                                    with_udp_chksum=True,
                                    udp_payload=npm_test_pkt,
                                    pattern_type=1)


            sys_logging(" step4: none acl , packet will forwarding  ")

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( pkt, [1])

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( pkt1, [1])

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_packets( pkt2, [1])

            self.ctc_send_packet( 0, str(pkt3))
            self.ctc_verify_packets( pkt3, [1])

            sys_logging(" step5: bind this ACL table to switch ")
            attr_value = sai_thrift_attribute_value_t(oid=acl_table_oid)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            sys_logging(" step6: match drop acl entry ")

            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_no_packet( pkt, 1)

            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_no_packet( pkt1, 1)

            self.ctc_send_packet( 0, str(pkt2))
            self.ctc_verify_no_packet( pkt2, 1)

            self.ctc_send_packet( 0, str(pkt3))
            self.ctc_verify_packets( pkt3, [1])

        finally:
            sys_logging("clear config")

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)

            status = self.client.sai_thrift_remove_acl_entry(acl_entry_oid)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_acl_table(acl_table_oid)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

            self.client.sai_thrift_remove_udf(udf_oid)
            self.client.sai_thrift_remove_udf(udf_oid_2)
            self.client.sai_thrift_remove_udf(udf_oid_3)
            self.client.sai_thrift_remove_udf_match(udf_match_oid)
            self.client.sai_thrift_remove_udf_match(udf_match_oid_2)
            self.client.sai_thrift_remove_udf_match(udf_match_oid_3)
            self.client.sai_thrift_remove_udf_group(udf_group_oid)

class scenario_03_ingress_acl_bind_switch_with_each_udf_group_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        max_group_num = 0
        if 'tsingma' == testutils.test_params_get()['chipname']:      # tsingma
            max_group_num = 16
        elif 'tsingma_mx' == testutils.test_params_get()['chipname']: # tsingma_mx
            max_group_num = 256

        priority_list = []
        for value in range(0, 128):
            priority_list.append(value)
        for value in range(-128, 0):
            priority_list.append(value)

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

        group_type = SAI_UDF_GROUP_TYPE_GENERIC
        group_length = 16

        udf_group_oid_list = []
        for n in range(0, max_group_num):
            udf_group_oid = sai_thrift_create_udf_group(self.client, group_type, group_length)
            assert udf_group_oid > 0, 'udf_group_oid is <= 0'
            print "udf_group_oid = 0x%lx" %udf_group_oid
            udf_group_oid_list.append(udf_group_oid)

        l2_type = 0x0800
        l2_type_mask = -1
        l3_type = 0x11
        l3_type_mask = -1
        gre_type = None
        gre_type_mask = -1
        mpls_label_num = None
        l4_src_port = 1234
        l4_src_port_mask = -1
        l4_dst_port = 5678
        l4_dst_port_mask = -1

        udf_match_oid_list = []
        n = 0
        for n in range(0, max_group_num):
            print "priority:%u" %priority_list[n]
            udf_match_oid = sai_thrift_create_udf_match(self.client,
                                                        l2_type,
                                                        l2_type_mask,
                                                        l3_type,
                                                        l3_type_mask,
                                                        gre_type,
                                                        gre_type_mask,
                                                        (l4_src_port+n),
                                                        l4_src_port_mask,
                                                        (l4_dst_port+n),
                                                        l4_dst_port_mask,
                                                        mpls_label_num,
                                                        priority_list[n])

            assert udf_match_oid > 0, 'udf_match_oid is <= 0'
            print "udf_match_oid[%u] = 0x%lx" %(priority_list[n], udf_match_oid)
            udf_match_oid_list.append(udf_match_oid)

        base = SAI_UDF_BASE_L4
        offset = 8

        hash_mask_list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        udf_entry_oid_list = []
        for n in range(0, max_group_num):
            udf_entry_oid = sai_thrift_create_udf(self.client, udf_match_oid_list[n], udf_group_oid_list[n], base, offset, hash_mask_list)
            assert udf_entry_oid > 0, 'udf_entry_oid is <= 0'
            print "udf_entry_oid = 0x%lx" %udf_entry_oid
            udf_entry_oid_list.append(udf_entry_oid)

        # acl table info
        action = SAI_PACKET_ACTION_DROP
        ip_type = SAI_ACL_IP_TYPE_IPV4ANY
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_SWITCH]

        acl_table_oid_list = []
        for n in range(0, max_group_num):
            acl_attr_list = []

            # create acl table
            attribute_value = sai_thrift_attribute_value_t(s32=table_stage)
            attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_STAGE, value=attribute_value)
            acl_attr_list.append(attribute)

            acl_table_bind_point_list = sai_thrift_s32_list_t(count=len(table_bind_point_list), s32list=table_bind_point_list)
            attribute_value = sai_thrift_attribute_value_t(s32list=acl_table_bind_point_list)
            attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST, value=attribute_value)
            acl_attr_list.append(attribute)

            attribute_value = sai_thrift_attribute_value_t(booldata=1)
            attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE, value=attribute_value)
            acl_attr_list.append(attribute)

            attribute_value = sai_thrift_attribute_value_t(booldata=1)
            attribute = sai_thrift_attribute_t(id=(SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN+n), value=attribute_value)
            acl_attr_list.append(attribute)

            acl_table_oid = self.client.sai_thrift_create_acl_table(acl_attr_list)
            sys_logging("create acl table = %d" %acl_table_oid)
            assert(acl_table_oid != SAI_NULL_OBJECT_ID)
            acl_table_oid_list.append(acl_table_oid)

        entry_priority = 1
        admin_state = True
        action = SAI_PACKET_ACTION_DROP

        acl_entry_oid_list = []
        for n in range(0, max_group_num):

            acl_attr_list = []
            attribute_value = sai_thrift_attribute_value_t(oid=acl_table_oid_list[n])
            attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_TABLE_ID, value=attribute_value)
            acl_attr_list.append(attribute)

            attribute_value = sai_thrift_attribute_value_t(u32=entry_priority)
            attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_PRIORITY, value=attribute_value)
            acl_attr_list.append(attribute)

            attribute_value = sai_thrift_attribute_value_t(booldata=admin_state)
            attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ADMIN_STATE, value=attribute_value)
            acl_attr_list.append(attribute)

            attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(s32=ip_type), mask = sai_thrift_acl_mask_t(0)))
            attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE, value=attribute_value)
            acl_attr_list.append(attribute)

            udf0 = ctypes.c_int8(17)
            udf1 = ctypes.c_int8(n)
            udf2 = ctypes.c_int8(17)
            udf3 = ctypes.c_int8(17)

            udf4 = ctypes.c_int8(34)
            udf5 = ctypes.c_int8(34)
            udf6 = ctypes.c_int8(34)
            udf7 = ctypes.c_int8(34)

            udf8 = ctypes.c_int8(0)
            udf9 = ctypes.c_int8(68)
            udf10 = ctypes.c_int8(86)
            udf11 = ctypes.c_int8(120)

            udf12 = ctypes.c_int8(0)
            udf13 = ctypes.c_int8(0)
            udf14 = ctypes.c_int8(0)
            udf15 = ctypes.c_int8(0)

            group_udf_data = [udf12.value, udf13.value, udf14.value, udf15.value, udf8.value, udf9.value, udf10.value, udf11.value, udf4.value, udf5.value, udf6.value, udf7.value, udf0.value, udf1.value, udf2.value, udf3.value]
            group_udf_mask = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  -1, -1, -1, -1, -1, -1]

            user_define_filed_group_data_list = sai_thrift_u8_list_t(count=len(group_udf_data), u8list=group_udf_data)
            user_define_filed_group_mask_list = sai_thrift_u8_list_t(count=len(group_udf_mask), u8list=group_udf_mask)

            attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                                data = sai_thrift_acl_data_t(u8list=user_define_filed_group_data_list),
                                                                                                mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group_mask_list)))
            attribute = sai_thrift_attribute_t(id=(SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN+n), value=attribute_value)
            acl_attr_list.append(attribute)

            attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(s32=action), enable = True))
            attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION, value=attribute_value)
            acl_attr_list.append(attribute)

            acl_entry_oid = self.client.sai_thrift_create_acl_entry(acl_attr_list)
            sys_logging("create acl entry = %d" %acl_entry_oid)
            assert(acl_entry_oid != SAI_NULL_OBJECT_ID)
            acl_entry_oid_list.append(acl_entry_oid)

        warmboot(self.client)
        try:
            for n in range(0, max_group_num):
                src_mac = mac1
                dst_mac = mac2
                src_ip = '1.2.3.4'
                dst_ip = '5.6.7.8'
                udp_src_port = 1234
                udp_dst_port = 5678
                ttl = 100
                tc = 0
                pkt_len = 100

                sequence_number_list  = [0x11, (0x0+n), 0x11, 0x11]
                sequence_number_byte  = str(bytearray(sequence_number_list))

                time_stamp = hexstr_to_ascii('2222222200445678')
                npm_test_pkt = sequence_number_byte + time_stamp

                pkt = simple_udp_packet(pktlen=pkt_len-4,
                                        eth_dst=dst_mac,
                                        eth_src=src_mac,
                                        dl_vlan_enable=False,
                                        ip_src=src_ip,
                                        ip_dst=dst_ip,
                                        ip_tos=0,
                                        ip_ttl=ttl,
                                        udp_sport=(udp_src_port+n),
                                        udp_dport=(udp_dst_port+n),
                                        ip_ihl=None,
                                        ip_id=0,
                                        ip_options=False,
                                        with_udp_chksum=True,
                                        udp_payload=npm_test_pkt,
                                        pattern_type=1)

                self.ctc_send_packet(0, str(pkt))
                self.ctc_verify_packets(pkt, [1])

                attr_value = sai_thrift_attribute_value_t(oid=acl_table_oid_list[n])
                attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
                status = self.client.sai_thrift_set_switch_attribute(attr)
                assert(status == SAI_STATUS_SUCCESS)

                #pdb.set_trace()
                self.ctc_send_packet(0, str(pkt))
                self.ctc_verify_no_packet(pkt, 1)

                attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
                status = self.client.sai_thrift_set_switch_attribute(attr)
                assert(status == SAI_STATUS_SUCCESS)

        finally:
            for n in range(0, max_group_num):
                status = self.client.sai_thrift_remove_acl_entry(acl_entry_oid_list[n])
                assert(status == SAI_STATUS_SUCCESS)

            for n in range(0, max_group_num):
                status = self.client.sai_thrift_remove_acl_table(acl_table_oid_list[n])
                assert(status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

            for n in range(0, max_group_num):
                status = self.client.sai_thrift_remove_udf(udf_entry_oid_list[n])
                assert(status == SAI_STATUS_SUCCESS)
                status = self.client.sai_thrift_remove_udf_match(udf_match_oid_list[n])
                assert(status == SAI_STATUS_SUCCESS)
                status = self.client.sai_thrift_remove_udf_group(udf_group_oid_list[n])
                assert(status == SAI_STATUS_SUCCESS)


class scenario_04_ingress_acl_bind_switch_with_group_max_entry_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)
        max_entry_num = 0
        if 'tsingma' == testutils.test_params_get()['chipname']:      # tsingma
            max_entry_num = 16
        elif 'tsingma_mx' == testutils.test_params_get()['chipname']: # tsingma_mx
            max_entry_num = 256

        priority_list = []
        for value in range(0, 128):
            priority_list.append(value)
        for value in range(-128, 0):
            priority_list.append(value)

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

        group_type = SAI_UDF_GROUP_TYPE_GENERIC
        group_length = 16

        udf_group_oid = sai_thrift_create_udf_group(self.client, group_type, group_length)
        assert udf_group_oid > 0, 'udf_group_oid is <= 0'
        print "udf_group_oid = 0x%lx" %udf_group_oid

        l2_type = 0x0800
        l2_type_mask = -1
        l3_type = 0x11
        l3_type_mask = -1
        gre_type = None
        gre_type_mask = -1
        mpls_label_num = None
        l4_src_port = 1234
        l4_src_port_mask = -1
        l4_dst_port = 5678
        l4_dst_port_mask = -1

        udf_match_oid_list = []
        n = 0
        for n in range(0, max_entry_num):
            udf_match_oid = sai_thrift_create_udf_match(self.client,
                                                        l2_type,
                                                        l2_type_mask,
                                                        l3_type,
                                                        l3_type_mask,
                                                        gre_type,
                                                        gre_type_mask,
                                                        (l4_src_port+n),
                                                        l4_src_port_mask,
                                                        (l4_dst_port+n),
                                                        l4_dst_port_mask,
                                                        mpls_label_num,
                                                        priority_list[n])
            assert udf_match_oid > 0, 'udf_match_oid is <= 0'
            print "udf_match_oid[%u] = 0x%lx" %(priority_list[n], udf_match_oid)
            udf_match_oid_list.append(udf_match_oid)

        base = SAI_UDF_BASE_L4
        offset = 8

        hash_mask_list = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
        udf_entry_oid_list = []
        for n in range(0, max_entry_num):
            udf_entry_oid = sai_thrift_create_udf(self.client, udf_match_oid_list[n], udf_group_oid, base, offset, hash_mask_list)
            assert udf_entry_oid > 0, 'udf_entry_oid is <= 0'
            print "udf_entry_oid = 0x%lx" %udf_entry_oid
            udf_entry_oid_list.append(udf_entry_oid)

        # acl table info
        action = SAI_PACKET_ACTION_DROP
        ip_type = SAI_ACL_IP_TYPE_IPV4ANY
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_SWITCH]

        acl_attr_list = []
        # create acl table
        attribute_value = sai_thrift_attribute_value_t(s32=table_stage)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_STAGE, value=attribute_value)
        acl_attr_list.append(attribute)

        acl_table_bind_point_list = sai_thrift_s32_list_t(count=len(table_bind_point_list), s32list=table_bind_point_list)
        attribute_value = sai_thrift_attribute_value_t(s32list=acl_table_bind_point_list)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_USER_DEFINED_FIELD_GROUP_MIN, value=attribute_value)
        acl_attr_list.append(attribute)

        acl_table_oid = self.client.sai_thrift_create_acl_table(acl_attr_list)
        sys_logging("create acl table = %d" %acl_table_oid)
        assert(acl_table_oid != SAI_NULL_OBJECT_ID)

        entry_priority = 1
        admin_state = True
        action = SAI_PACKET_ACTION_DROP

        acl_attr_list = []
        attribute_value = sai_thrift_attribute_value_t(oid=acl_table_oid)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_TABLE_ID, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(u32=entry_priority)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_PRIORITY, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(booldata=admin_state)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ADMIN_STATE, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(s32=ip_type), mask = sai_thrift_acl_mask_t(0)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE, value=attribute_value)
        acl_attr_list.append(attribute)

        udf0 = ctypes.c_int8(17)
        udf1 = ctypes.c_int8(17)
        udf2 = ctypes.c_int8(17)
        udf3 = ctypes.c_int8(17)

        udf4 = ctypes.c_int8(34)
        udf5 = ctypes.c_int8(34)
        udf6 = ctypes.c_int8(34)
        udf7 = ctypes.c_int8(34)

        udf8 = ctypes.c_int8(0)
        udf9 = ctypes.c_int8(68)
        udf10 = ctypes.c_int8(86)
        udf11 = ctypes.c_int8(120)

        udf12 = ctypes.c_int8(0)
        udf13 = ctypes.c_int8(0)
        udf14 = ctypes.c_int8(0)
        udf15 = ctypes.c_int8(0)

        group_udf_data = [udf12.value, udf13.value, udf14.value, udf15.value, udf8.value, udf9.value, udf10.value, udf11.value, udf4.value, udf5.value, udf6.value, udf7.value, udf0.value, udf1.value, udf2.value, udf3.value]
        group_udf_mask = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  -1, -1, -1, -1, -1, -1]

        user_define_filed_group_data_list = sai_thrift_u8_list_t(count=len(group_udf_data), u8list=group_udf_data)
        user_define_filed_group_mask_list = sai_thrift_u8_list_t(count=len(group_udf_mask), u8list=group_udf_mask)

        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True,
                                                                                            data = sai_thrift_acl_data_t(u8list=user_define_filed_group_data_list),
                                                                                            mask = sai_thrift_acl_mask_t(u8list=user_define_filed_group_mask_list)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(s32=action), enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION, value=attribute_value)
        acl_attr_list.append(attribute)

        acl_entry_oid = self.client.sai_thrift_create_acl_entry(acl_attr_list)
        sys_logging("create acl entry = %d" %acl_entry_oid)
        assert(acl_entry_oid != SAI_NULL_OBJECT_ID)

        warmboot(self.client)
        try:
            for n in range(0, max_entry_num):
                src_mac = mac1
                dst_mac = mac2
                src_ip = '1.2.3.4'
                dst_ip = '5.6.7.8'
                udp_src_port = 1234
                udp_dst_port = 5678
                ttl = 100
                tc = 0
                pkt_len = 100

                sequence_number_list  = [0x11, 0x11, 0x11, 0x11]
                sequence_number_byte  = str(bytearray(sequence_number_list))

                time_stamp = hexstr_to_ascii('2222222200445678')
                npm_test_pkt = sequence_number_byte + time_stamp

                pkt = simple_udp_packet(pktlen=pkt_len-4,
                                        eth_dst=dst_mac,
                                        eth_src=src_mac,
                                        dl_vlan_enable=False,
                                        ip_src=src_ip,
                                        ip_dst=dst_ip,
                                        ip_tos=0,
                                        ip_ttl=ttl,
                                        udp_sport=(udp_src_port+n),
                                        udp_dport=(udp_dst_port+n),
                                        ip_ihl=None,
                                        ip_id=0,
                                        ip_options=False,
                                        with_udp_chksum=True,
                                        udp_payload=npm_test_pkt,
                                        pattern_type=1)

                self.ctc_send_packet(0, str(pkt))
                self.ctc_verify_packets(pkt, [1])

                attr_value = sai_thrift_attribute_value_t(oid=acl_table_oid)
                attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
                status = self.client.sai_thrift_set_switch_attribute(attr)
                assert(status == SAI_STATUS_SUCCESS)

                self.ctc_send_packet(0, str(pkt))
                self.ctc_verify_no_packet(pkt, 1)

                attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_INGRESS_ACL, value=attr_value)
                status = self.client.sai_thrift_set_switch_attribute(attr)
                assert(status == SAI_STATUS_SUCCESS)

        finally:
            status = self.client.sai_thrift_remove_acl_entry(acl_entry_oid)
            assert(status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_acl_table(acl_table_oid)
            assert(status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

            for n in range(0, max_entry_num):
                status = self.client.sai_thrift_remove_udf(udf_entry_oid_list[n])
                assert(status == SAI_STATUS_SUCCESS)
                status = self.client.sai_thrift_remove_udf_match(udf_match_oid_list[n])
                assert(status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_udf_group(udf_group_oid)
            assert(status == SAI_STATUS_SUCCESS)

