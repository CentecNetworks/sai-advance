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
Thrift SAI interface Hash tests
"""

import socket
import sys
from struct import pack, unpack

from switch import *

import sai_base_test
from ptf.mask import Mask

@group('hash_api')
class func_01_create_hash(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_01_create_hash======")
        switch_init(self.client)

        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]
        udf_group_list = [123]

        # create hash
        sys_logging("======create hash======")
        hash_id = sai_thrift_create_hash(self.client, field_list, udf_group_list)
        sys_logging("hash_id = %d" %hash_id)
        
        warmboot(self.client)
        try:
            sys_logging("Check create hash, not support create hash")
            assert (hash_id == 0)
        finally:
            sys_logging("Success!")

class func_02_remove_hash(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_02_remove_hash======")
        switch_init(self.client)

        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]
        udf_group_list = [123]
        
        # create hash
        sys_logging("======create hash======")
        hash_id = sai_thrift_create_hash(self.client, field_list, udf_group_list)
        sys_logging("hash_id = %d" %hash_id)
        
        # remove hash
        sys_logging("======remove hash======")
        status = self.client.sai_thrift_remove_hash(hash_id)
        sys_logging("remove hash status = %d" %status)
        assert (status == SAI_STATUS_NOT_SUPPORTED)
        sys_logging("Check remove hash, not support remove hash")
        
        warmboot(self.client)
        try:
            assert (hash_id == 0)
        finally:
            sys_logging("Success!")

class func_03_hash_set_attribute_lag_hashfield(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_03_hash_set_attribute_lag_hashfield======")
        switch_init(self.client)

        hash_id_lag = 0;
        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]

        warmboot(self.client)
        try:
            # get lag hash object id
            sys_logging("======get lag hash object id======")
            ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                    hash_id_lag = attribute.value.oid

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

            # set hash attribute
            sys_logging("======set lag hash attribute:SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,field list:[SAI_NATIVE_HASH_FIELD_DST_IP]======")
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            print(attr)
            status = self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
            sys_logging( "set hash attribute status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_DST_IP == a.value.s32list.s32list[0])

        finally:
            sys_logging("Success!")
            sys_logging("Clean up")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class func_04_hash_set_attribute_ecmp_hashfield(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_04_hash_set_attribute_ecmp_hashfield======")
        switch_init(self.client)

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]

        warmboot(self.client)
        try:
            # get ecmp hash object id
            sys_logging("======get ecmp hash object id======")
            ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                    hash_id_ecmp = attribute.value.oid

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_ecmp)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

            # set hash attribute
            sys_logging("======set ecmp hash attribute:SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,field list:[SAI_NATIVE_HASH_FIELD_DST_IP]======")
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            print(attr)
            status = self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
            sys_logging( "set hash attribute status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_ecmp)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_DST_IP == a.value.s32list.s32list[0])

        finally:
            sys_logging("Success!")
            sys_logging("Clean up")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class func_05_hash_set_attribute_lag_multi_hashfield(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_05_hash_set_attribute_lag_multi_hashfield======")
        switch_init(self.client)

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP, SAI_NATIVE_HASH_FIELD_IP_PROTOCOL, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_L4_DST_PORT]

        warmboot(self.client)
        try:
            # get lag hash object id
            sys_logging("======get lag hash object id======")
            ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                    hash_id_lag = attribute.value.oid

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

            # set hash attribute
            sys_logging("======set lag hash attribute:SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST======")
            sys_logging("======field list:[SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP, SAI_NATIVE_HASH_FIELD_IP_PROTOCOL, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_L4_DST_PORT]======")
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            print(attr)
            status = self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
            sys_logging( "set hash attribute status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_SRC_IP == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_DST_IP == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_IP_PROTOCOL == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_L4_SRC_PORT == a.value.s32list.s32list[3])
                    assert(SAI_NATIVE_HASH_FIELD_L4_DST_PORT == a.value.s32list.s32list[4])

        finally:
            sys_logging("Success!")
            sys_logging("Clean up")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class func_06_hash_set_attribute_ecmp_multi_hashfield(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_06_hash_set_attribute_ecmp_multi_hashfield======")
        switch_init(self.client)

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP, SAI_NATIVE_HASH_FIELD_IP_PROTOCOL, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_L4_DST_PORT]

        warmboot(self.client)
        try:
            # get ecmp hash object id
            sys_logging("======get ecmp hash object id======")
            ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                    hash_id_ecmp = attribute.value.oid

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_ecmp)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

            # set hash attribute
            sys_logging("======set ecmp hash attribute:SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST======")
            sys_logging("======field list:[SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP, SAI_NATIVE_HASH_FIELD_IP_PROTOCOL, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_L4_DST_PORT]======")
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            print(attr)
            status = self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
            sys_logging( "set hash attribute status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_ecmp)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_SRC_IP == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_DST_IP == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_IP_PROTOCOL == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_L4_SRC_PORT == a.value.s32list.s32list[3])
                    assert(SAI_NATIVE_HASH_FIELD_L4_DST_PORT == a.value.s32list.s32list[4])

        finally:
            sys_logging("Success!")
            sys_logging("Clean up")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

#unsupport
class func_07_hash_set_attribute_lag_udf(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_07_hash_set_attribute_lag_udf======")
        switch_init(self.client)

        hash_id_lag = 0
        objlist = [0x1F]

        warmboot(self.client)
        try:
            # get lag hash object id
            sys_logging("======get lag hash object id======")
            ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                    hash_id_lag = attribute.value.oid

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

            # set hash attribute
            sys_logging("======set lag hash attribute:SAI_HASH_ATTR_UDF_GROUP_LIST======")
            hash_obj_list = sai_thrift_object_list_t(count=len(objlist), object_id_list=objlist)
            attr_value = sai_thrift_attribute_value_t(objlist=hash_obj_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_UDF_GROUP_LIST,
                                                value=attr_value)
            print(attr)
            status = self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
            sys_logging( "set hash attribute status = %d" %status)
            #TBD
            #assert (status == SAI_STATUS_SUCCESS)

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_UDF_GROUP_LIST:
                    print(a.value.objlist)
                    #TBD
                    #assert(SAI_NATIVE_HASH_FIELD_DST_IP == a.value.s32list.s32list[0])
        finally:
            sys_logging("Success!")
            sys_logging("Clean up")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

#unsupport
class func_08_hash_set_attribute_ecmp_udf(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_08_hash_set_attribute_ecmp_udf======")
        switch_init(self.client)

        hash_id_ecmp = 0
        objlist = [0x1F]

        warmboot(self.client)
        try:
            # get ecmp hash object id
            sys_logging("======get ecmp hash object id======")
            ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                    hash_id_ecmp = attribute.value.oid

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_ecmp)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

            # set hash attribute
            sys_logging("======set ecmp hash attribute:SAI_HASH_ATTR_UDF_GROUP_LIST======")
            hash_obj_list = sai_thrift_object_list_t(count=len(objlist), object_id_list=objlist)
            attr_value = sai_thrift_attribute_value_t(objlist=hash_obj_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_UDF_GROUP_LIST,
                                                value=attr_value)
            print(hash_obj_list)
            print(attr)
            status = self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
            sys_logging( "set hash attribute status = %d" %status)
            #TBD
            #assert (status == SAI_STATUS_SUCCESS)

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_ecmp)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_UDF_GROUP_LIST:
                    print(a.value.objlist)
                    #TBD
                    #assert(SAI_NATIVE_HASH_FIELD_DST_IP == a.value.s32list.s32list[0])
        finally:
            sys_logging("Success!")
            sys_logging("Clean up")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class func_09_hash_set_attribute_lag_unnormal(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_09_hash_set_attribute_lag_unnormal======")
        switch_init(self.client)

        hash_id_lag = 0

        warmboot(self.client)
        try:
            # get lag hash object id
            sys_logging("======get lag hash object id======")
            ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                    hash_id_lag = attribute.value.oid

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

            # set hash attribute
            sys_logging("======set lag hash attribute:SAI_HASH_ATTR_END======")
            hash_field_list = sai_thrift_s32_list_t()
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_END,
                                                value=attr_value)

            status = self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
            sys_logging( "set hash attribute status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

        finally:
            sys_logging("Success!")
            sys_logging("Clean up")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class func_10_hash_set_attribute_ecmp_unnormal(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_10_hash_set_attribute_ecmp_unnormal======")
        switch_init(self.client)

        hash_id_ecmp = 0

        warmboot(self.client)
        try:
            # get ecmp hash object id
            sys_logging("======get ecmp hash object id======")
            ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                    hash_id_ecmp = attribute.value.oid

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_ecmp)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

            # set hash attribute
            sys_logging("======set ecmp hash attribute:SAI_HASH_ATTR_END======")
            hash_field_list = sai_thrift_s32_list_t()
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_END,
                                                value=attr_value)

            status = self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
            sys_logging( "set hash attribute status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_ecmp)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

        finally:
            sys_logging("Success!")
            sys_logging("Clean up")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class func_11_hash_set_attribute_lag_hashfield_replace(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_11_hash_set_attribute_lag_hashfield_replace======")
        switch_init(self.client)

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]

        warmboot(self.client)
        try:
            # get lag hash object id
            sys_logging("======get lag hash object id======")
            ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                    hash_id_lag = attribute.value.oid

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

            # set hash attribute
            sys_logging("======reset lag hash attribute:SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,field list:[SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP]======")
            field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP]
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            print(attr)
            status = self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
            sys_logging( "reset hash attribute status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            # get hash attribute
            sys_logging("get hash attribute")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_INNER_SRC_IP == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_INNER_DST_IP == a.value.s32list.s32list[1])

            # set hash attribute again
            sys_logging("======set lag hash attribute again,field list:[SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_VLAN_ID]======")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_VLAN_ID]
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            print attr
            status = self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
            sys_logging( "set hash attribute status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            # get hash attribute
            sys_logging("get hash attribute again")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_SRC_IP == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_VLAN_ID == a.value.s32list.s32list[1])
        finally:
            sys_logging("Success!")
            sys_logging("Clean up")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class func_12_hash_set_attribute_ecmp_hashfield_replace(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_12_hash_set_attribute_ecmp_hashfield_replace======")
        switch_init(self.client)

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]

        warmboot(self.client)
        try:
            # get ecmp hash object id
            sys_logging("======get ecmp hash object id======")
            ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                    hash_id_ecmp = attribute.value.oid

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_ecmp)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

            # set hash attribute
            sys_logging("======reset ecmp hash attribute:SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,field list:[SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP]======")
            field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP]
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            print(attr)
            status = self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
            sys_logging( "reset hash attribute status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            # get hash attribute
            sys_logging("get hash attribute")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_ecmp)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_INNER_SRC_IP == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_INNER_DST_IP == a.value.s32list.s32list[1])

            # set hash attribute again
            sys_logging("======set ecmp hash attribute again,field list:[SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_VLAN_ID]======")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_VLAN_ID]
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            print attr
            status = self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
            sys_logging( "set hash attribute status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            # get hash attribute
            sys_logging("get hash attribute again")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_ecmp)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_SRC_IP == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_VLAN_ID == a.value.s32list.s32list[1])
        finally:
            sys_logging("Success!")
            sys_logging("Clean up")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class func_13_hash_get_attributes(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======func_13_hash_get_attributes======")
        switch_init(self.client)

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP, SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        warmboot(self.client)
        try:
            # get lag hash object id
            sys_logging("======get lag hash object id======")
            ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
            switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
            attr_list = switch_attr_list.attr_list
            for attribute in attr_list:
                if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                    sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                    hash_id_lag = attribute.value.oid

            # get hash attribute
            sys_logging("======get hash attribute======")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    assert(SAI_NATIVE_HASH_FIELD_ETHERTYPE == a.value.s32list.s32list[0])
                    assert(SAI_NATIVE_HASH_FIELD_SRC_MAC == a.value.s32list.s32list[1])
                    assert(SAI_NATIVE_HASH_FIELD_DST_MAC == a.value.s32list.s32list[2])
                    assert(SAI_NATIVE_HASH_FIELD_IN_PORT == a.value.s32list.s32list[3])

            # set hash attribute
            sys_logging("set hash attribute")
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)

            status = self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
            sys_logging( "set hash attribute status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            # get hash attribute
            sys_logging("get hash attribute")
            attrs= self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            sys_logging( "get hash attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            print attrs
            for a in attrs.attr_list:
                print(a.id)
                if a.id == SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST:
                    print(a.value.s32list)
                    for i in range (a.value.s32list.count):
                        assert(i == a.value.s32list.s32list[i])
                if a.id == SAI_HASH_ATTR_UDF_GROUP_LIST:
                    # random value
                    print(a.value.objlist)
                    # TBD
        finally:
            sys_logging("Success!")
            sys_logging("Clean up")
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

@group('lag_hash')
class scenario_01_lag_hash_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_01_lag_hash_src_ip_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src ip to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to lag,every package's src ip is not equal======")
            src_ip = int(socket.inet_aton('192.168.8.1').encode('hex'),16)
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.1',
                                        ip_src=src_ip_addr,
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst='10.10.10.1',
                                            ip_src=src_ip_addr,
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_ip += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_02_lag_hash_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_02_lag_hash_dst_ip_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set dst ip to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_ip = int(socket.inet_aton('10.10.10.1').encode('hex'),16)
            sys_logging("======send 20 packages to lag,every package's dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst=dst_ip_addr,
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst=dst_ip_addr,
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_ip += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_03_lag_hash_vlan_id_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_03_lag_hash_vlan_id_test======")
        switch_init(self.client)
        vlan_id = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_VLAN_ID]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create vlans======")
        vlan_oid = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(0, len(vlan_id)):
            vlan_oid[i] = sai_thrift_create_vlan(self.client, vlan_id[i])

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlans======")
        vlan_member1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        vlan_member2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(0, len(vlan_oid)):
            #vlan_member1[i] = sai_thrift_create_vlan_member(self.client, vlan_oid[i], lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
            #vlan_member2[i] = sai_thrift_create_vlan_member(self.client, vlan_oid[i], port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            vlan_member1[i] = sai_thrift_create_vlan_member(self.client, vlan_oid[i], lag_oid1, SAI_VLAN_TAGGING_MODE_TAGGED, is_lag)
            vlan_member2[i] = sai_thrift_create_vlan_member(self.client, vlan_oid[i], port4, SAI_VLAN_TAGGING_MODE_TAGGED)
        '''
        #set default vlan
        attr_value = sai_thrift_attribute_value_t(u16=10)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)
        '''
        for i in range(0, len(vlan_oid)):
            sai_thrift_create_fdb_bport(self.client, vlan_oid[i], mac1, lag_oid1, mac_action)
            sai_thrift_create_fdb(self.client, vlan_oid[i], mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set vlan id to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            sys_logging("======send 20 packages to lag,every package's vlan id is not equal======")
            count = [0, 0, 0]
            for i in range(0, len(vlan_id)):
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        dl_vlan_enable=True,
                                        vlan_vid=vlan_id[i],
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            dl_vlan_enable=True,
                                            vlan_vid=vlan_id[i],
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((len(vlan_id) / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            for i in range(0, len(vlan_oid)):
                sai_thrift_delete_fdb(self.client, vlan_oid[i], mac2, port4)
                sai_thrift_delete_fdb(self.client, vlan_oid[i], mac1, lag_oid1)

            for i in range(0, len(vlan_oid)):
                self.client.sai_thrift_remove_vlan_member(vlan_member1[i])
                self.client.sai_thrift_remove_vlan_member(vlan_member2[i])
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            
            for i in range(0, len(vlan_id)):
                self.client.sai_thrift_remove_vlan(vlan_oid[i])
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_04_lag_hash_ip_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_04_lag_hash_ip_protocol_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_IP_PROTOCOL]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set ip protocol to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            ip_protocol = 1
            sys_logging("======send 20 packages to lag,every package's ip protocol is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_ip_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64,
                                        ip_proto=ip_protocol)

                exp_pkt = simple_ip_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64,
                                            ip_proto=ip_protocol)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                ip_protocol += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_ip_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_ip_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_05_lag_hash_ethertype_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_05_lag_hash_ethertype_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_ETHERTYPE]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set ethertype to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            ethertype = [0x0800, 0x0801, 0x0802, 0x0803, 0x0804, 0x0805, 0x0806, 0x0807, 0x0808, 0x0809, 0x080a, 0x080b, 0x080c, 0x080d, 0x080e, 0x080f, 0x0806, 0x86dd, 0x86de, 0x86df]
            sys_logging("======send 20 packages to lag,every package's ethertype is not equal======")
            for i in range(0, len(ethertype)):
                pkt = simple_eth_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        eth_type=ethertype[i],
                                        pktlen=200)

                exp_pkt = simple_eth_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            eth_type=ethertype[i],
                                            pktlen=200)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((len(ethertype) / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_eth_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                        pktlen=200)
            exp_pkt = simple_eth_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                        pktlen=200)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_06_lag_hash_l4_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_06_lag_hash_l4_src_port_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_L4_SRC_PORT]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src port to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            sys_logging("======send 20 packages to lag,every package's src port is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64,
                                        tcp_sport=src_port,
                                        tcp_dport=80)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64,
                                            tcp_sport=src_port,
                                            tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64,
                                    tcp_sport=1234,
                                    tcp_dport=80)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64,
                                    tcp_sport=1234,
                                    tcp_dport=80)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)  
                
class scenario_07_lag_hash_l4_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_07_lag_hash_l4_dst_port_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_L4_DST_PORT]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set dst port to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_port = 80
            sys_logging("======send 20 packages to lag,every package's dst port is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64,
                                            tcp_sport=1234,
                                            tcp_dport=dst_port)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64,
                                    tcp_sport=1234,
                                    tcp_dport=80)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64,
                                    tcp_sport=1234,
                                    tcp_dport=80)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr) 

class scenario_08_lag_hash_src_mac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_08_lag_hash_src_mac_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src mac address to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_mac_start = '00:22:22:22:22:{0}'
            sys_logging("======send 20 packages to lag,every package's src mac address is not equal======")
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_09_lag_hash_dst_mac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_09_lag_hash_dst_mac_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_DST_MAC]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set dst mac address to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_mac_start = '00:11:11:11:11:{0}'
            sys_logging("======send 20 packages to lag,every package's dst mac address is not equal======")
            for i in range(0, max_itrs):
                dst_mac = dst_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=dst_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst=dst_mac,
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)  

class scenario_10_lag_hash_in_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_10_lag_hash_in_port_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_IN_PORT]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        
        ports = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(0, len(ports)):
            ports[i] = port_list[i + 3]

        mac1 = '00:11:11:11:11:11'
        mac2 = ['00:22:22:22:22:22','00:22:22:22:22:23','00:22:22:22:22:24','00:22:22:22:22:25','00:22:22:22:22:26',
                '00:22:22:22:22:27','00:22:22:22:22:28','00:22:22:22:22:29','00:22:22:22:22:2a','00:22:22:22:22:2b',
                '00:22:22:22:22:2c','00:22:22:22:22:2d','00:22:22:22:22:2e','00:22:22:22:22:2f','00:22:22:22:22:30',
                '00:22:22:22:22:31','00:22:22:22:22:32','00:22:22:22:22:33','00:22:22:22:22:34','00:22:22:22:22:35']
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and twenty ports to vlan======")
        vlan_member2 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        
        for i in range(0, len(vlan_member2)):
            vlan_member2[i] = sai_thrift_create_vlan_member(self.client, vlan_oid, ports[i], SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        for i in range(0, len(ports)):
            self.client.sai_thrift_set_port_attribute(ports[i], attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        for i in range(0, 20):
            sai_thrift_create_fdb(self.client, vlan_oid, mac2[i], ports[i], mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set gport to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to lag,every package's gport is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( i+3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")
            '''
            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            '''
        finally:
            sys_logging("======clean up======")
            for i in range(0, 20):
                sai_thrift_delete_fdb(self.client, vlan_oid, mac2[i], ports[i])
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            for i in range(0, len(vlan_member2)):
                self.client.sai_thrift_remove_vlan_member(vlan_member2[i])
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            for i in range(0, len(ports)):
                self.client.sai_thrift_set_port_attribute(ports[i], attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)  

class scenario_11_lag_hash_mpls_label_stack_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_11_lag_hash_mpls_label_stack_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.1'
        dmac = '00:55:55:55:55:55'

        label = [201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220]

        label_list = [(100<<12) | 32]
        pop_nums = 0
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%u" %lag_id1
        print"lag:%lu" %lag_id1
        print"lag:%lx" %lag_id1
        print"lag:%x" %lag_id1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set mpls label stack to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create two interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create a neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

        sys_logging("======create a mpls nexthop======")
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list, outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_UNIFORM, outseg_type = SAI_OUTSEG_TYPE_SWAP)

        sys_logging("======create entrys======")
        for i in range(0, len(label)):
            sai_thrift_create_inseg_entry(self.client, label[i], pop_nums, None, next_hop, packet_action)

        mplss = [[{'label':201,'tc':0,'ttl':32,'s':1}],
                 [{'label':202,'tc':0,'ttl':32,'s':1}],
                 [{'label':203,'tc':0,'ttl':32,'s':1}],
                 [{'label':204,'tc':0,'ttl':32,'s':1}],
                 [{'label':205,'tc':0,'ttl':32,'s':1}],
                 [{'label':206,'tc':0,'ttl':32,'s':1}],
                 [{'label':207,'tc':0,'ttl':32,'s':1}],
                 [{'label':208,'tc':0,'ttl':32,'s':1}],
                 [{'label':209,'tc':0,'ttl':32,'s':1}],
                 [{'label':210,'tc':0,'ttl':32,'s':1}],
                 [{'label':211,'tc':0,'ttl':32,'s':1}],
                 [{'label':212,'tc':0,'ttl':32,'s':1}],
                 [{'label':213,'tc':0,'ttl':32,'s':1}],
                 [{'label':214,'tc':0,'ttl':32,'s':1}],
                 [{'label':215,'tc':0,'ttl':32,'s':1}],
                 [{'label':216,'tc':0,'ttl':32,'s':1}],
                 [{'label':217,'tc':0,'ttl':32,'s':1}],
                 [{'label':218,'tc':0,'ttl':32,'s':1}],
                 [{'label':219,'tc':0,'ttl':32,'s':1}],
                 [{'label':220,'tc':0,'ttl':32,'s':1}]]

        exp_mpls = [{'label':100,'tc':0,'ttl':31,'s':1}]

        warmboot(self.client)
        try:
            max_itrs = 20
            count = [0, 0, 0]
            sys_logging("======send 20 packages to lag,every package's mpls label stack is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst='10.10.10.1',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:33',
                                        mpls_type=0x8847,
                                        mpls_tags= mplss[i],
                                        inner_frame = ip_only_pkt)   
            
                ip_only_exp_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst='10.10.10.1',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                                        
                exp_pkt = simple_mpls_packet(
                                        eth_dst=dmac,
                                        eth_src=router_mac,
                                        mpls_type=0x8847,
                                        mpls_tags= exp_mpls,
                                        inner_frame = ip_only_exp_pkt) 
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            for i in range(0, len(label)):
                mpls = sai_thrift_inseg_entry_t(label[i]) 
                self.client.sai_thrift_remove_inseg_entry(mpls)

            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_12_lag_hash_unnormal(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_12_lag_hash_unnormal======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_DST_MAC]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set dst mac address to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_mac_start = '00:22:22:22:22:{0}'
            sys_logging("======send 20 packages to lag,every package's src mac address is not equal======")
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            '''
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")
            '''

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

#=====basic mpls=====
class scenario_13_lag_hash_basic_mpls_inner_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_13_lag_hash_basic_mpls_inner_src_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = int(socket.inet_aton('1.1.1.2').encode('hex'),16)
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src=src_ip_addr,
                                        ip_dst=ip_addr_subnet,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcp_packet(eth_dst=dmac,
                                       eth_src=router_mac,
                                       ip_dst=ip_addr_subnet,
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_ip += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
                
class scenario_14_lag_hash_basic_mpls_inner_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_14_lag_hash_basic_mpls_inner_dst_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_ip = int(socket.inet_aton('20.20.20.1').encode('hex'),16)
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst=dst_ip_addr,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcp_packet(eth_dst=dmac,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_ip += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_15_lag_hash_basic_mpls_inner_ip_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_15_lag_hash_basic_mpls_inner_ip_protocol_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner ip protocol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            ip_protocol = 1
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner ip protocol is not equal======")
            for i in range(0, max_itrs):
                inner_pkt = simple_only_ip_no_l4hdr_packet(pktlen=100,
                                        ip_dst=ip_addr_subnet,
                                        ip_src='1.1.1.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        ip_proto=ip_protocol)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = inner_pkt)
                exp_pkt = simple_ip_packet(eth_dst=dmac,
                                           eth_src=router_mac,
                                           ip_dst=ip_addr_subnet,
                                           ip_src='1.1.1.2',
                                           ip_id=105,
                                           ip_ttl=99,
                                           pktlen=114,
                                           ip_proto=ip_protocol)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                ip_protocol += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_16_lag_hash_basic_mpls_inner_l4_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_16_lag_hash_basic_mpls_inner_l4_src_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst='20.20.20.1',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5,
                                        tcp_sport=src_port,
                                        tcp_dport=80
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcp_packet(eth_dst=dmac,
                                       eth_src=router_mac,
                                       ip_dst='20.20.20.1',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_17_lag_hash_basic_mpls_inner_l4_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_17_lag_hash_basic_mpls_inner_l4_dst_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_port = 80
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst='20.20.20.1',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcp_packet(eth_dst=dmac,
                                       eth_src=router_mac,
                                       ip_dst='20.20.20.1',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
#====================

#=====l3VPN=====
class scenario_18_lag_hash_l3vpn_inner_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_18_lag_hash_l3vpn_inner_src_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = int(socket.inet_aton('1.1.1.2').encode('hex'),16)
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src=src_ip_addr,
                                        ip_dst=ip_addr_subnet,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcp_packet(eth_dst=dmac,
                                       eth_src=router_mac,
                                       ip_dst=ip_addr_subnet,
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_ip += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_19_lag_hash_l3vpn_inner_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        sys_logging("======scenario_19_lag_hash_l3vpn_inner_dst_ip_test======")
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_ip = int(socket.inet_aton('20.20.20.1').encode('hex'),16)
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst ip is not equal======")
 
            for i in range(0, max_itrs):
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst=dst_ip_addr,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcp_packet(eth_dst=dmac,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_ip += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_20_lag_hash_l3vpn_inner_ip_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_20_lag_hash_l3vpn_inner_ip_protocol_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner ip protocol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            ip_protocol = 1
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner ip protocol is not equal======")
            for i in range(0, max_itrs):
                inner_pkt = simple_only_ip_no_l4hdr_packet(pktlen=100,
                                        ip_dst=ip_addr_subnet,
                                        ip_src='1.1.1.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        ip_proto=ip_protocol)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = inner_pkt)
                exp_pkt = simple_ip_packet(eth_dst=dmac,
                                           eth_src=router_mac,
                                           ip_dst=ip_addr_subnet,
                                           ip_src='1.1.1.2',
                                           ip_id=105,
                                           ip_ttl=99,
                                           pktlen=114,
                                           ip_proto=ip_protocol)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                ip_protocol += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_21_lag_hash_l3vpn_inner_l4_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_21_lag_hash_l3vpn_inner_l4_src_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT]
        
        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1235
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst=ip_addr_subnet,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5,
                                        tcp_sport=src_port,
                                        tcp_dport=80
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcp_packet(eth_dst=dmac,
                                       eth_src=router_mac,
                                       ip_dst=ip_addr_subnet,
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_22_lag_hash_l3vpn_inner_l4_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_22_lag_hash_l3vpn_inner_l4_dst_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_port = 80
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst=ip_addr_subnet,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcp_packet(eth_dst=dmac,
                                       eth_src=router_mac,
                                       ip_dst=ip_addr_subnet,
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
#===============

#=====l2VPN=====
class scenario_23_lag_hash_l2vpn_inner_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_23_lag_hash_l2vpn_inner_src_ip_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = int(socket.inet_aton('2.2.2.2').encode('hex'),16)
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=30,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src=src_ip_addr,
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src=src_ip_addr,
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_ip += 1
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_24_lag_hash_l2vpn_inner_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_24_lag_hash_l2vpn_inner_dst_ip_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_ip = int(socket.inet_aton('1.1.1.1').encode('hex'),16)
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=30,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst=dst_ip_addr,
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst=dst_ip_addr,
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_ip += 1
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_25_lag_hash_l2vpn_inner_ip_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_25_lag_hash_l2vpn_inner_ip_protocol_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner ip protocol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            ip_protocol = 1
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner ip protocol is not equal======")
            for i in range(0, max_itrs):
                mpls_inner_pkt = simple_ip_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=30,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        ip_proto=ip_protocol)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_ip_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        ip_proto=ip_protocol)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                ip_protocol += 1
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_26_lag_hash_l2vpn_inner_ethertype_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_26_lag_hash_l2vpn_inner_ethertype_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_ETHERTYPE]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner ethertype to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbor and nexthop======")
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            ethertype = [0x0800, 0x0801, 0x0802, 0x0803, 0x0804, 0x0805, 0x0806, 0x0807, 0x0808, 0x0809, 0x080a, 0x080b, 0x080c, 0x080d, 0x080e, 0x080f, 0x0806, 0x86dd, 0x86de, 0x86df]
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner ethertype is not equal======")
            for i in range(0, max_itrs):
                mpls_inner_pkt = simple_eth_packet(eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=30,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        eth_type=ethertype[i],
                                        pktlen=100)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_eth_packet(eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        eth_type=ethertype[i],
                                        pktlen=100)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            #include the fdb which is learning
            flush_all_fdb(self.client)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_27_lag_hash_l2vpn_inner_l4_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_27_lag_hash_l2vpn_inner_l4_src_port_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src port is not equal======")
            for i in range(0, max_itrs):
                mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=30,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        tcp_sport=src_port,
                                        tcp_dport=80
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        tcp_sport=src_port,
                                        tcp_dport=80
                                        )
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_28_lag_hash_l2vpn_inner_l4_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_28_lag_hash_l2vpn_inner_l4_dst_port_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_port = 80
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst port is not equal======")
            for i in range(0, max_itrs):
                mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=30,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port
                                        )
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_29_lag_hash_l2vpn_inner_src_mac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_29_lag_hash_l2vpn_inner_src_mac_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src mac address to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbor and nexthop======")
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_mac_start = '00:00:00:02:03:{0}'
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src mac address is not equal======")
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=src_mac,
                                        dl_vlan_enable=True,
                                        vlan_vid=30,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=mac1,
                                        eth_src=src_mac,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            #include the fdb which is learning
            flush_all_fdb(self.client)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_30_lag_hash_l2vpn_inner_dst_mac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_30_lag_hash_l2vpn_inner_dst_mac_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_MAC]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst mac address to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbor and nexthop======")
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_mac_start = '00:00:00:01:02:{0}'
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst mac address is not equal======")
            for i in range(0, max_itrs):
                dst_mac = dst_mac_start.format(str(i).zfill(4)[2:])
                mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=dst_mac,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=30,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=dst_mac,
                                        eth_src=mac2,
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst='1.1.1.1',
                                        ip_src='2.2.2.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            #include the fdb which is learning
            flush_all_fdb(self.client)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
#===============

@group('ecmp_hash')
class scenario_31_ecmp_hash_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_31_ecmp_hash_src_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP]

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=64)

            exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=63)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt2 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:56',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt3 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:57',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            src_ip = int(socket.inet_aton('192.168.100.3').encode('hex'),16)
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.4',
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=64)
            
                exp_pkt1 = simple_tcp_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt2 = simple_tcp_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt3 = simple_tcp_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=63)
            
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx
                src_ip += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
                
class scenario_32_ecmp_hash_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_32_ecmp_hash_dst_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=64)

            exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=63)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt2 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:56',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt3 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:57',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            dst_ip = int(socket.inet_aton('10.10.10.4').encode('hex'),16)
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst=dst_ip_addr,
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=64)
            
                exp_pkt1 = simple_tcp_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ip_dst=dst_ip_addr,
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt2 = simple_tcp_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ip_dst=dst_ip_addr,
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt3 = simple_tcp_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ip_dst=dst_ip_addr,
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx
                dst_ip += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_33_ecmp_hash_vlan_id_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_33_ecmp_hash_vlan_id_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_VLAN_ID]

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create twenty three interfaces======")
        vlan_id = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200]
        vlan_oid = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        rif4 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        vlan_member1 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(0, len(vlan_id)):
            vlan_oid[i] = sai_thrift_create_vlan(self.client, vlan_id[i])
            vlan_member1[i] = sai_thrift_create_vlan_member(self.client, vlan_oid[i], port4, SAI_VLAN_TAGGING_MODE_TAGGED)
            rif4[i] = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_VLAN, 0, vlan_oid[i], v4_enabled, v6_enabled, mac)
        
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set vlan id to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_id=106,
                                ip_ttl=64)

            exp_pkt1 = simple_tcp_packet(pktlen=96,
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=63)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt2 = simple_tcp_packet(pktlen=96,
                                    eth_dst='00:11:22:33:44:56',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    dl_vlan_enable=True,
                                    vlan_vid=10,
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt3 = simple_tcp_packet(pktlen=96,
                                    eth_dst='00:11:22:33:44:57',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's vlan id is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.4',
                                        dl_vlan_enable=True,
                                        vlan_vid=vlan_id[i],
                                        ip_id=106,
                                        ip_ttl=64)
            
                exp_pkt1 = simple_tcp_packet(pktlen=96,
                                        eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.4',
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt2 = simple_tcp_packet(pktlen=96,
                                        eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.4',
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt3 = simple_tcp_packet(pktlen=96,
                                        eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.4',
                                        ip_id=106,
                                        ip_ttl=63)
            
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            for i in range(0, len(rif4)):
                self.client.sai_thrift_remove_router_interface(rif4[i])

            self.client.sai_thrift_remove_virtual_router(vr1)
            
            for i in range(0, len(vlan_member1)):
                self.client.sai_thrift_remove_vlan_member(vlan_member1[i])
                
            for i in range(0, len(vlan_oid)):
                self.client.sai_thrift_remove_vlan(vlan_oid[i])

            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
                
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_34_ecmp_hash_ip_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_34_ecmp_hash_ip_protocol_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_IP_PROTOCOL]

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set ip protocol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_ip_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=64)

            exp_pkt1 = simple_ip_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=63)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_ip_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt2 = simple_ip_packet(
                                    eth_dst='00:11:22:33:44:56',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_ip_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt3 = simple_ip_packet(
                                    eth_dst='00:11:22:33:44:57',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            max_itrs = 20
            ip_protocol = 1
            sys_logging("======send 20 packages to ecmp,every package's ip protocol is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_ip_packet(eth_dst=router_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=64,
                                        ip_proto=ip_protocol,
                                        pktlen=200)
            
                exp_pkt1 = simple_ip_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63,
                                        ip_proto=ip_protocol,
                                        pktlen=200)
                exp_pkt2 = simple_ip_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63,
                                        ip_proto=ip_protocol,
                                        pktlen=200)
                exp_pkt3 = simple_ip_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63,
                                        ip_proto=ip_protocol,
                                        pktlen=200)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1, exp_pkt2, exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx
                ip_protocol += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_35_ecmp_hash_l4_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_35_ecmp_hash_l4_src_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_L4_SRC_PORT]

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=64,
                                tcp_sport=1234,
                                tcp_dport=80)

            exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=63,
                                tcp_sport=1234,
                                tcp_dport=80)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64,
                                    tcp_sport=1234,
                                    tcp_dport=80)

            exp_pkt2 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:56',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63,
                                    tcp_sport=1234,
                                    tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64,
                                    tcp_sport=1234,
                                    tcp_dport=80)

            exp_pkt3 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:57',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63,
                                    tcp_sport=1234,
                                    tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            src_port = 1234
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's src port is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=64,
                                        tcp_sport=src_port,
                                        tcp_dport=80)
            
                exp_pkt1 = simple_tcp_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63,
                                        tcp_sport=src_port,
                                        tcp_dport=80)
                exp_pkt2 = simple_tcp_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63,
                                        tcp_sport=src_port,
                                        tcp_dport=80)
                exp_pkt3 = simple_tcp_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63,
                                        tcp_sport=src_port,
                                        tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx
                src_port += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
                
class scenario_36_ecmp_hash_l4_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_36_ecmp_hash_l4_dst_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_L4_DST_PORT]

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        
        sys_logging("======add nexthops to group======")
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=64,
                                tcp_sport=1234,
                                tcp_dport=80)

            exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=63,
                                tcp_sport=1234,
                                tcp_dport=80)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64,
                                    tcp_sport=1234,
                                    tcp_dport=80)

            exp_pkt2 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:56',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63,
                                    tcp_sport=1234,
                                    tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64,
                                    tcp_sport=1234,
                                    tcp_dport=80)

            exp_pkt3 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:57',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63,
                                    tcp_sport=1234,
                                    tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            dst_port = 80
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's dst port is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=64,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port)
            
                exp_pkt1 = simple_tcp_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port)
                exp_pkt2 = simple_tcp_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port)
                exp_pkt3 = simple_tcp_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port)
            
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx
                dst_port += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
                
class scenario_37_ecmp_hash_src_mac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_37_ecmp_hash_src_mac_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC]

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set src mac address to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=64)

            exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=63)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt2 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:56',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt3 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:57',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            src_mac_start = '00:22:22:22:22:{0}'
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's src mac address is not equal======")
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=64)
            
                exp_pkt1 = simple_tcp_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt2 = simple_tcp_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt3 = simple_tcp_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_38_ecmp_hash_in_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_38_ecmp_hash_in_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        ports = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(0, len(ports)):
            ports[i] = port_list[i + 3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_IN_PORT]

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create twenty three interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rifs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        for i in range(0, len(ports)):
            rifs[i] = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, ports[i], 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set gport to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=64)

            exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=63)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt2 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:56',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt3 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:57',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's gport is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=64)
            
                exp_pkt1 = simple_tcp_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt2 = simple_tcp_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt3 = simple_tcp_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src='192.168.100.3',
                                        ip_id=106,
                                        ip_ttl=63)
            
                self.ctc_send_packet( i+3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            for i in range(0, len(rifs)):
                self.client.sai_thrift_remove_router_interface(rifs[i])
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_39_ecmp_hash_mpls_label_stack_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_39_ecmp_hash_mpls_label_stack_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4

        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        label = [201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220]

        label_list = [(100<<12) | 32]
        pop_nums = 0
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set mpls label stack to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id3, ip_addr3, dmac3)

        sys_logging("======create mpls nexthops======")
        next_hop1 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_addr1, rif_id1, label_list, outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_UNIFORM, outseg_type = SAI_OUTSEG_TYPE_SWAP)
        next_hop2 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_addr2, rif_id2, label_list, outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_UNIFORM, outseg_type = SAI_OUTSEG_TYPE_SWAP)
        next_hop3 = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_addr3, rif_id3, label_list, outseg_ttl_mode= SAI_OUTSEG_TTL_MODE_UNIFORM, outseg_type = SAI_OUTSEG_TYPE_SWAP)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create entrys======")
        for i in range(0, len(label)):
            sai_thrift_create_inseg_entry(self.client, label[i], pop_nums, None, nhop_group1, packet_action)

        mplss = [[{'label':201,'tc':0,'ttl':32,'s':1}],
                 [{'label':202,'tc':0,'ttl':32,'s':1}],
                 [{'label':203,'tc':0,'ttl':32,'s':1}],
                 [{'label':204,'tc':0,'ttl':32,'s':1}],
                 [{'label':205,'tc':0,'ttl':32,'s':1}],
                 [{'label':206,'tc':0,'ttl':32,'s':1}],
                 [{'label':207,'tc':0,'ttl':32,'s':1}],
                 [{'label':208,'tc':0,'ttl':32,'s':1}],
                 [{'label':209,'tc':0,'ttl':32,'s':1}],
                 [{'label':210,'tc':0,'ttl':32,'s':1}],
                 [{'label':211,'tc':0,'ttl':32,'s':1}],
                 [{'label':212,'tc':0,'ttl':32,'s':1}],
                 [{'label':213,'tc':0,'ttl':32,'s':1}],
                 [{'label':214,'tc':0,'ttl':32,'s':1}],
                 [{'label':215,'tc':0,'ttl':32,'s':1}],
                 [{'label':216,'tc':0,'ttl':32,'s':1}],
                 [{'label':217,'tc':0,'ttl':32,'s':1}],
                 [{'label':218,'tc':0,'ttl':32,'s':1}],
                 [{'label':219,'tc':0,'ttl':32,'s':1}],
                 [{'label':220,'tc':0,'ttl':32,'s':1}]]

        exp_mpls = [{'label':100,'tc':0,'ttl':31,'s':1}]

        warmboot(self.client)
        try:
            max_itrs = 20
            count = [0, 0, 0]
            sys_logging("======send 20 packages to ecmp,every package's mpls label stack is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst='10.10.10.4',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:33',
                                        mpls_type=0x8847,
                                        mpls_tags= mplss[i],
                                        inner_frame = ip_only_pkt)   
            
                ip_only_exp_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst='10.10.10.4',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                                        
                exp_pkt1 = simple_mpls_packet(
                                        eth_dst=dmac1,
                                        eth_src=router_mac,
                                        mpls_type=0x8847,
                                        mpls_tags= exp_mpls,
                                        inner_frame = ip_only_exp_pkt) 
                                        
                exp_pkt2 = simple_mpls_packet(
                                        eth_dst=dmac2,
                                        eth_src=router_mac,
                                        mpls_type=0x8847,
                                        mpls_tags= exp_mpls,
                                        inner_frame = ip_only_exp_pkt)
                                        
                exp_pkt3 = simple_mpls_packet(
                                        eth_dst=dmac3,
                                        eth_src=router_mac,
                                        mpls_type=0x8847,
                                        mpls_tags= exp_mpls,
                                        inner_frame = ip_only_exp_pkt)
                                        
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1, exp_pkt2, exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            for i in range(0, len(label)):
                mpls = sai_thrift_inseg_entry_t(label[i]) 
                self.client.sai_thrift_remove_inseg_entry(mpls)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)    
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id3, ip_addr3, dmac3)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_40_ecmp_hash_unnormal(sai_base_test.ThriftInterfaceDataPlane): 
    def runTest(self):
        sys_logging("======scenario_40_ecmp_hash_unnormal======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=64)

            exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=63)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt2 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:56',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt3 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:57',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            src_ip = int(socket.inet_aton('192.168.100.3').encode('hex'),16)
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.4',
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=64)
            
                exp_pkt1 = simple_tcp_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt2 = simple_tcp_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=63)
                exp_pkt3 = simple_tcp_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ip_dst='10.10.10.4',
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=63)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx
                src_ip += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            '''
            for i in range(0, 2):
                self.assertTrue((count[i] >= ((max_itrs / 2) * 0.8)),
                        "Not all paths are equally balanced")
            '''
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

#=====basic mpls=====
class scenario_41_ecmp_hash_basic_mpls_inner_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_41_ecmp_hash_basic_mpls_inner_src_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = int(socket.inet_aton('1.1.1.2').encode('hex'),16)
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src=src_ip_addr,
                                        ip_dst='10.10.10.4',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99)

                exp_pkt2 = simple_tcp_packet(eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99)

                exp_pkt3 = simple_tcp_packet(eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_ip += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)  
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_42_ecmp_hash_basic_mpls_inner_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_42_ecmp_hash_basic_mpls_inner_dst_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_ip = int(socket.inet_aton('10.10.10.4').encode('hex'),16)
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst=dst_ip_addr,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99)

                exp_pkt2 = simple_tcp_packet(eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99)

                exp_pkt3 = simple_tcp_packet(eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_ip += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_43_ecmp_hash_basic_mpls_inner_ip_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_43_ecmp_hash_basic_mpls_inner_ip_protocol_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner ip protocol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            ip_protocol = 1
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner ip protocol is not equal======")
            for i in range(0, max_itrs):
                inner_pkt = simple_only_ip_no_l4hdr_packet(pktlen=86,
                                        ip_dst='10.10.10.4',
                                        ip_src='1.1.1.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        ip_proto=ip_protocol)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = inner_pkt)
                                        
                exp_pkt1 = simple_ip_packet(eth_dst=dmac1,
                                           eth_src=router_mac,
                                           ip_dst='10.10.10.4',
                                           ip_src='1.1.1.2',
                                           ip_id=105,
                                           ip_ttl=99,
                                           ip_proto=ip_protocol)

                exp_pkt2 = simple_ip_packet(eth_dst=dmac2,
                                           eth_src=router_mac,
                                           ip_dst='10.10.10.4',
                                           ip_src='1.1.1.2',
                                           ip_id=105,
                                           ip_ttl=99,
                                           ip_proto=ip_protocol)

                exp_pkt3 = simple_ip_packet(eth_dst=dmac3,
                                           eth_src=router_mac,
                                           ip_dst='10.10.10.4',
                                           ip_src='1.1.1.2',
                                           ip_id=105,
                                           ip_ttl=99,
                                           ip_proto=ip_protocol)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                ip_protocol += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_44_ecmp_hash_basic_mpls_inner_l4_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_44_ecmp_hash_basic_mpls_inner_l4_src_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1235
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner src port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst='10.10.10.4',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5,
                                        tcp_sport=src_port,
                                        tcp_dport=80
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                exp_pkt2 = simple_tcp_packet(eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                exp_pkt3 = simple_tcp_packet(eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_45_ecmp_hash_basic_mpls_inner_l4_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_45_ecmp_hash_basic_mpls_inner_l4_dst_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_port = 80
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner dst port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst='10.10.10.4',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                exp_pkt2 = simple_tcp_packet(eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                exp_pkt3 = simple_tcp_packet(eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
#====================

#=====l3VPN=====
class scenario_46_ecmp_hash_l3vpn_inner_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_46_ecmp_hash_l3vpn_inner_src_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = int(socket.inet_aton('1.1.1.2').encode('hex'),16)
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src=src_ip_addr,
                                        ip_dst='10.10.10.4',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99)

                exp_pkt2 = simple_tcp_packet(eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99)

                exp_pkt3 = simple_tcp_packet(eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_ip += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_47_ecmp_hash_l3vpn_inner_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_47_ecmp_hash_l3vpn_inner_dst_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_ip = int(socket.inet_aton('10.10.10.4').encode('hex'),16)
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst=dst_ip_addr,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99)

                exp_pkt2 = simple_tcp_packet(eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99)

                exp_pkt3 = simple_tcp_packet(eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_ip += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_48_ecmp_hash_l3vpn_inner_ip_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_48_ecmp_hash_l3vpn_inner_ip_protocol_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner ip protocol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            ip_protocol = 1
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner ip protocol is not equal======")
            for i in range(0, max_itrs):
                inner_pkt = simple_only_ip_no_l4hdr_packet(pktlen=86,
                                        ip_dst='10.10.10.4',
                                        ip_src='1.1.1.2',
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        ip_proto=ip_protocol)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = inner_pkt)
                                        
                exp_pkt1 = simple_ip_packet(eth_dst=dmac1,
                                           eth_src=router_mac,
                                           ip_dst='10.10.10.4',
                                           ip_src='1.1.1.2',
                                           ip_id=105,
                                           ip_ttl=99,
                                           ip_proto=ip_protocol)

                exp_pkt2 = simple_ip_packet(eth_dst=dmac2,
                                           eth_src=router_mac,
                                           ip_dst='10.10.10.4',
                                           ip_src='1.1.1.2',
                                           ip_id=105,
                                           ip_ttl=99,
                                           ip_proto=ip_protocol)

                exp_pkt3 = simple_ip_packet(eth_dst=dmac3,
                                           eth_src=router_mac,
                                           ip_dst='10.10.10.4',
                                           ip_src='1.1.1.2',
                                           ip_id=105,
                                           ip_ttl=99,
                                           ip_proto=ip_protocol)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                ip_protocol += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_49_ecmp_hash_l3vpn_inner_l4_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_49_ecmp_hash_l3vpn_inner_l4_src_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1235
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner src port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst='10.10.10.4',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5,
                                        tcp_sport=src_port,
                                        tcp_dport=80
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                exp_pkt2 = simple_tcp_packet(eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                exp_pkt3 = simple_tcp_packet(eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_50_ecmp_hash_l3vpn_inner_l4_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_50_ecmp_hash_l3vpn_inner_l4_dst_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_port = 80
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner dst port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst='10.10.10.4',
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                exp_pkt2 = simple_tcp_packet(eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                exp_pkt3 = simple_tcp_packet(eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ip_dst='10.10.10.4',
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
#===============

@group('multi_filed_value_hash')
class scenario_51_lag_hash_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_51_lag_hash_multi_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src and dst ip to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to lag,every package's src and dst ip is not equal======")
            src_ip = int(socket.inet_aton('192.168.8.1').encode('hex'),16)
            dst_ip = int(socket.inet_aton('10.10.10.1').encode('hex'),16)
            src_ip1 = ['192.168.8.1', '192.168.8.30', '192.168.8.50', '192.168.8.80', '192.168.8.100',
                       '192.168.20.11', '192.168.20.41', '192.168.8.72', '192.168.8.123', '192.168.8.175',
                       '192.168.101.1', '192.168.101.15', '192.168.101.55', '192.168.101.145', '192.168.101.201',
                       '192.168.205.2', '192.168.205.18', '192.168.205.75', '192.168.205.131', '192.168.205.213']
            dst_ip1 = ['10.10.8.1', '10.10.8.30', '10.10.8.50', '10.10.8.80', '10.10.8.100',
                       '10.10.20.11', '10.10.20.41', '10.10.8.72', '10.10.8.123', '10.10.8.175',
                       '10.10.101.1', '10.10.101.15', '10.10.101.55', '10.10.101.145', '10.10.101.201',
                       '10.10.205.2', '10.10.205.18', '10.10.205.75', '10.10.205.131', '10.10.205.213']
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst=dst_ip_addr,
                                        ip_src=src_ip_addr,
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst=dst_ip_addr,
                                            ip_src=src_ip_addr,
                                            ip_id=109,
                                            ip_ttl=64)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_ip += 1
                #dst_ip += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_52_lag_hash_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_52_lag_hash_multi_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_L4_DST_PORT]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src and dst port to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            dst_port = 80
            sys_logging("======send 20 packages to lag,every package's src and dst port is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64,
                                            tcp_sport=src_port,
                                            tcp_dport=dst_port)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                #src_port += 1
                dst_port += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64,
                                    tcp_sport=1234,
                                    tcp_dport=80)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64,
                                    tcp_sport=1234,
                                    tcp_dport=80)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_53_lag_hash_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_53_lag_hash_multi_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src and dst mac address to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_mac_start = '00:22:22:22:22:{0}'
            dst_mac_start = '00:11:11:11:11:{0}'
            sys_logging("======send 20 packages to lag,every package's src and dst mac address is not equal======")
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                dst_mac = dst_mac_start.format(str(i).zfill(4)[2:])
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src=src_mac,
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src=src_mac,
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)

                pkt1 = simple_tcp_packet(eth_dst=dst_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst='10.10.10.1',
                                        ip_src='192.168.8.1',
                                        ip_id=109,
                                        ip_ttl=64)

                exp_pkt1 = simple_tcp_packet(eth_dst=dst_mac,
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst='10.10.10.1',
                                            ip_src='192.168.8.1',
                                            ip_id=109,
                                            ip_ttl=64)
                #self.ctc_send_packet( 3, str(pkt))
                #rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                
                self.ctc_send_packet( 3, str(pkt1))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_54_lag_hash_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_54_lag_hash_multi_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_L4_DST_PORT]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        #port5 = port_list[4]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        #vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port5, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src ip,dst ip,src port,dst port to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to lag,every package's src ip,dst ip,src port,dst port is not equal======")
            src_ip = int(socket.inet_aton('192.168.8.1').encode('hex'),16)
            dst_ip = int(socket.inet_aton('10.10.10.1').encode('hex'),16)
            src_port = 1234
            dst_port = 80
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst=dst_ip_addr,
                                        ip_src=src_ip_addr,
                                        ip_id=109,
                                        ip_ttl=64,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port)

                exp_pkt = simple_tcp_packet(eth_dst='00:11:11:11:11:11',
                                            eth_src='00:22:22:22:22:22',
                                            ip_dst=dst_ip_addr,
                                            ip_src=src_ip_addr,
                                            ip_id=109,
                                            ip_ttl=64,
                                            tcp_sport=src_port,
                                            tcp_dport=dst_port)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_ip += 1
                #dst_ip += 1
                #src_port += 1
                #dst_port += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_55_lag_hash_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_55_lag_hash_multi_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src and dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = int(socket.inet_aton('1.1.1.2').encode('hex'),16)
            dst_ip = int(socket.inet_aton('20.20.20.1').encode('hex'),16)
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src and dst ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src=src_ip_addr,
                                        ip_dst=dst_ip_addr,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcp_packet(eth_dst=dmac,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                #src_ip += 1
                dst_ip += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
                
class scenario_56_lag_hash_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_56_lag_hash_multi_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]
        
        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src and dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1235
            dst_port = 80
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src and dst port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src='1.1.1.2',
                                        ip_dst=ip_addr_subnet,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcp_packet(eth_dst=dmac,
                                       eth_src=router_mac,
                                       ip_dst=ip_addr_subnet,
                                       ip_src='1.1.1.2',
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=dst_port)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                #src_port += 1
                dst_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_57_lag_hash_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_57_lag_hash_multi_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:66'
        ip_addr_subnet = '20.20.20.1'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP, SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src ip,dst ip,src port,dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1235
            dst_port = 80
            src_ip = int(socket.inet_aton('1.1.1.2').encode('hex'),16)
            dst_ip = int(socket.inet_aton('20.20.20.1').encode('hex'),16)
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src ip,dst ip,src port,dst port is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src=src_ip_addr,
                                        ip_dst=dst_ip_addr,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcp_packet(eth_dst=dmac,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=dst_port
                                       )
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_ip += 1
                #dst_ip += 1
                #src_port += 1
                #dst_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_58_ecmp_hash_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_58_ecmp_hash_multi_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_L4_DST_PORT]

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set src ip,dst ip,src port,dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=64)

            exp_pkt1 = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=106,
                                ip_ttl=63)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt2 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:56',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.2',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcp_packet(eth_dst=router_mac,
                                    eth_src='00:22:22:22:22:22',
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=64)

            exp_pkt3 = simple_tcp_packet(
                                    eth_dst='00:11:22:33:44:57',
                                    eth_src=router_mac,
                                    ip_dst='10.10.10.3',
                                    ip_src='192.168.100.3',
                                    ip_id=106,
                                    ip_ttl=63)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            src_port = 1235
            dst_port = 80
            src_ip = int(socket.inet_aton('192.168.100.3').encode('hex'),16)
            dst_ip = int(socket.inet_aton('10.10.10.4').encode('hex'),16)
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's src ip,dst ip,src port,dst port is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                pkt = simple_tcp_packet(eth_dst=router_mac,
                                        eth_src='00:22:22:22:22:22',
                                        ip_dst=dst_ip_addr,
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=64,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port
                                        )
            
                exp_pkt1 = simple_tcp_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ip_dst=dst_ip_addr,
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=63,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port
                                        )
                exp_pkt2 = simple_tcp_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ip_dst=dst_ip_addr,
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=63,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port
                                        )
                exp_pkt3 = simple_tcp_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ip_dst=dst_ip_addr,
                                        ip_src=src_ip_addr,
                                        ip_id=106,
                                        ip_ttl=63,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port
                                        )
            
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx
                #src_ip += 1
                #dst_ip += 1
                #src_port += 1
                dst_port += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_59_ecmp_hash_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_59_ecmp_hash_multi_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr3 = '10.10.10.3'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '10.10.10.0'
        ip_mask = '255.255.255.0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP, SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner src ip,dst ip,src port,dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1235
            dst_port = 80
            src_ip = int(socket.inet_aton('1.1.1.2').encode('hex'),16)
            dst_ip = int(socket.inet_aton('10.10.10.4').encode('hex'),16)
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner src ip,dst ip,src port,dst port is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                ip_only_pkt = simple_ip_only_packet(pktlen=86,
                                        ip_src=src_ip_addr,
                                        ip_dst=dst_ip_addr,
                                        ip_ttl=64,
                                        ip_id=105,
                                        ip_ihl=5,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port
                                        )
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcp_packet(eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=dst_port
                                       )

                exp_pkt2 = simple_tcp_packet(eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=dst_port
                                       )

                exp_pkt3 = simple_tcp_packet(eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ip_dst=dst_ip_addr,
                                       ip_src=src_ip_addr,
                                       ip_id=105,
                                       ip_ttl=99,
                                       tcp_sport=src_port,
                                       tcp_dport=dst_port
                                       )

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_ip += 1
                #dst_ip += 1
                #src_port += 1
                #dst_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_60_lag_hash_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_60_lag_hash_multi_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP, SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_L4_DST_PORT, SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT, SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC, SAI_NATIVE_HASH_FIELD_INNER_DST_MAC]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        #port5 = port_list[4]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        #vlan_member3 = sai_thrift_create_vlan_member(self.client, vlan_oid, port5, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src ip,dst ip,inner src ip,inner dst ip,src port,dst port,src port,dst port,inner src port,inner dst port,inner src mac,inner dst mac to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to lag,every package's src ip/dst ip/inner src ip/inner dst ip/src port/dst port/src port/dst port/inner src port/inner dst port/inner src mac/inner dst mac is not equal======")
            src_ip = int(socket.inet_aton('192.168.8.1').encode('hex'),16)
            dst_ip = int(socket.inet_aton('10.10.10.1').encode('hex'),16)
            src_port = 1234
            dst_port = 80
            m = 0
            n = 0
            src_mac = ['00:22:22:22:22:01', '00:22:22:22:22:02', '00:22:22:22:22:03', '00:22:22:22:22:04', '00:22:22:22:22:05',
                       '00:22:22:22:22:06', '00:22:22:22:22:07', '00:22:22:22:22:08', '00:22:22:22:22:09', '00:22:22:22:22:0a',
                       '00:22:22:22:22:0b', '00:22:22:22:22:0c', '00:22:22:22:22:0d', '00:22:22:22:22:0e', '00:22:22:22:22:0f',
                       '00:22:22:22:22:10', '00:22:22:22:22:11', '00:22:22:22:22:12', '00:22:22:22:22:13', '00:22:22:22:22:14']
            dst_mac = ['00:11:11:11:11:00', '00:11:11:11:11:01', '00:11:11:11:11:02', '00:11:11:11:11:03', '00:11:11:11:11:04',
                       '00:11:11:11:11:05', '00:11:11:11:11:06', '00:11:11:11:11:07', '00:11:11:11:11:08', '00:11:11:11:11:09',
                       '00:11:11:11:11:0a', '00:11:11:11:11:0b', '00:11:11:11:11:0c', '00:11:11:11:11:0d', '00:11:11:11:11:0e',
                       '00:11:11:11:11:0f', '00:11:11:11:11:10', '00:11:11:11:11:11', '00:11:11:11:11:12', '00:11:11:11:11:13']
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                pkt = simple_tcp_packet(eth_dst=dst_mac[n],
                                        eth_src=src_mac[m],
                                        ip_dst=dst_ip_addr,
                                        ip_src=src_ip_addr,
                                        ip_id=109,
                                        ip_ttl=64,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port)

                exp_pkt = simple_tcp_packet(eth_dst=dst_mac[n],
                                            eth_src=src_mac[m],
                                            ip_dst=dst_ip_addr,
                                            ip_src=src_ip_addr,
                                            ip_id=109,
                                            ip_ttl=64,
                                            tcp_sport=src_port,
                                            tcp_dport=dst_port)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_ip += 1
                #dst_ip += 1
                #src_port += 1
                #dst_port += 1
                #m += 1
                #n += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

            pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            exp_pkt = simple_tcp_packet(eth_src='00:11:11:11:11:11',
                                    eth_dst='00:22:22:22:22:22',
                                    ip_dst='10.0.0.1',
                                    ip_src='192.168.8.1',
                                    ip_id=109,
                                    ip_ttl=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_61_lag_hash_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_61_lag_hash_multi_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP, 
                      SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP, 
                      SAI_NATIVE_HASH_FIELD_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_L4_DST_PORT, 
                      SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, 
                      SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT, 
                      SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC, SAI_NATIVE_HASH_FIELD_INNER_DST_MAC,
                      SAI_NATIVE_HASH_FIELD_MPLS_LABEL_STACK]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src ip,dst ip,inner src ip,inner dst ip,src port,dst port,src port,dst port,inner src port,inner dst port,inner src mac,inner dst mac,mpls label stack to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbor and nexthop======")
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = int(socket.inet_aton('2.2.2.2').encode('hex'),16)
            dst_ip = int(socket.inet_aton('1.1.1.1').encode('hex'),16)
            src_port = 1234
            dst_port = 80
            m = 0
            n = 0
            src_mac = ['00:22:22:22:22:01', '00:22:22:22:22:02', '00:22:22:22:22:03', '00:22:22:22:22:04', '00:22:22:22:22:05',
                       '00:22:22:22:22:06', '00:22:22:22:22:07', '00:22:22:22:22:08', '00:22:22:22:22:09', '00:22:22:22:22:0a',
                       '00:22:22:22:22:0b', '00:22:22:22:22:0c', '00:22:22:22:22:0d', '00:22:22:22:22:0e', '00:22:22:22:22:0f',
                       '00:22:22:22:22:10', '00:22:22:22:22:11', '00:22:22:22:22:12', '00:22:22:22:22:13', '00:22:22:22:22:14']
            dst_mac = ['00:11:11:11:11:00', '00:11:11:11:11:01', '00:11:11:11:11:02', '00:11:11:11:11:03', '00:11:11:11:11:04',
                       '00:11:11:11:11:05', '00:11:11:11:11:06', '00:11:11:11:11:07', '00:11:11:11:11:08', '00:11:11:11:11:09',
                       '00:11:11:11:11:0a', '00:11:11:11:11:0b', '00:11:11:11:11:0c', '00:11:11:11:11:0d', '00:11:11:11:11:0e',
                       '00:11:11:11:11:0f', '00:11:11:11:11:10', '00:11:11:11:11:11', '00:11:11:11:11:12', '00:11:11:11:11:13']
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's src ip/dst ip/inner src ip/inner dst ip/src port/dst port/src port/dst port/inner src port/inner dst port/inner src mac/inner dst mac/mpls label stack is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = socket.inet_ntoa(hex(src_ip)[2:].zfill(8).decode('hex'))
                dst_ip_addr = socket.inet_ntoa(hex(dst_ip)[2:].zfill(8).decode('hex'))
                mpls_inner_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=dst_mac[n],
                                        eth_src=src_mac[m],
                                        dl_vlan_enable=True,
                                        vlan_vid=30,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst=dst_ip_addr,
                                        ip_src=src_ip_addr,
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcp_packet(pktlen=96,
                                        eth_dst=dst_mac[n],
                                        eth_src=src_mac[m],
                                        dl_vlan_enable=True,
                                        vlan_vid=20,
                                        vlan_pcp=0,
                                        dl_vlan_cfi=0,
                                        ip_dst=dst_ip_addr,
                                        ip_src=src_ip_addr,
                                        ip_id=105,
                                        ip_ttl=64,
                                        ip_ihl=5,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                #src_ip += 1
                #dst_ip += 1
                #src_port += 1
                #dst_port += 1
                m += 1
                #n += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            #include the fdb which is learning
            flush_all_fdb(self.client)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

#=================add  lag=====================
class scenario_62_lag_hash_ipv6_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_62_lag_hash_ipv6_src_ip_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src ip to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to lag,every package's src ip is not equal======")
            src_ip = '2001:db8:85a3::8a2e:370:73{0}'
            for i in range(0, max_itrs):
                src_ip_addr = src_ip.format(str(i).zfill(4)[2:])
                pkt = simple_tcpv6_packet(eth_dst='00:11:11:11:11:11',
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src=src_ip_addr,
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

                exp_pkt = simple_tcpv6_packet(eth_dst='00:11:11:11:11:11',
                                              eth_src='00:22:22:22:22:22',
                                              ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_src=src_ip_addr,
                                              ipv6_hlim=64,
                                              tcp_sport=1234,
                                              tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcpv6_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            exp_pkt = simple_tcpv6_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_63_lag_hash_ipv6_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_63_lag_hash_ipv6_dst_ip_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set dst ip to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to lag,every package's dst ip is not equal======")
            dst_ip = '2001:db8:85a3::8a2e:370:74{0}'
            for i in range(0, max_itrs):
                dst_ip_addr = dst_ip.format(str(i).zfill(4)[2:])
                pkt = simple_tcpv6_packet(eth_dst='00:11:11:11:11:11',
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst=dst_ip_addr,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

                exp_pkt = simple_tcpv6_packet(eth_dst='00:11:11:11:11:11',
                                              eth_src='00:22:22:22:22:22',
                                              ipv6_dst=dst_ip_addr,
                                              ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_hlim=64,
                                              tcp_sport=1234,
                                              tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcpv6_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            exp_pkt = simple_tcpv6_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_64_lag_hash_ipv6_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_64_lag_hash_ipv6_src_port_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_L4_SRC_PORT]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src port to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to lag,every package's src port is not equal======")
            src_port = 1234
            for i in range(0, max_itrs):
                pkt = simple_tcpv6_packet(eth_dst='00:11:11:11:11:11',
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_hlim=64,
                                          tcp_sport=src_port,
                                          tcp_dport=80)

                exp_pkt = simple_tcpv6_packet(eth_dst='00:11:11:11:11:11',
                                              eth_src='00:22:22:22:22:22',
                                              ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                              ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_hlim=64,
                                              tcp_sport=src_port,
                                              tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcpv6_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            exp_pkt = simple_tcpv6_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_65_lag_hash_ipv6_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_65_lag_hash_ipv6_dst_port_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_L4_DST_PORT]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set dst port to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to lag,every package's dst port is not equal======")
            dst_port = 80
            for i in range(0, max_itrs):
                pkt = simple_tcpv6_packet(eth_dst='00:11:11:11:11:11',
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=dst_port)

                exp_pkt = simple_tcpv6_packet(eth_dst='00:11:11:11:11:11',
                                              eth_src='00:22:22:22:22:22',
                                              ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                              ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_hlim=64,
                                              tcp_sport=1234,
                                              tcp_dport=dst_port)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcpv6_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            exp_pkt = simple_tcpv6_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_66_lag_hash_ipv6_ip_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_66_lag_hash_ipv6_ip_protocol_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_IP_PROTOCOL]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set ip protocol to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            sys_logging("======send 20 packages to lag,every package's ip protocol is not equal======")
            nh = 1
            for i in range(0, max_itrs):
                pkt = simple_tcpv6_no_l4hdr_packet(eth_dst='00:11:11:11:11:11',
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_hlim=64,
                                          ipv6_nh=nh)

                exp_pkt = simple_tcpv6_no_l4hdr_packet(eth_dst='00:11:11:11:11:11',
                                              eth_src='00:22:22:22:22:22',
                                              ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                              ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_hlim=64,
                                              ipv6_nh=nh)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                nh += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcpv6_no_l4hdr_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64)
            exp_pkt = simple_tcpv6_no_l4hdr_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

#=================basic mpls================
class scenario_67_lag_hash_basic_mpls_ipv6_inner_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_67_lag_hash_basic_mpls_ipv6_inner_src_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
        dmac = '00:55:55:55:55:66'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = '2001:db8:85a3::8a2e:370:73{0}'
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = src_ip.format(str(i).zfill(4)[2:])
                ip_only_pkt = simple_tcpv6_only_packet(
                                          ipv6_dst=ip_da,
                                          ipv6_src=src_ip_addr,
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                       
                exp_pkt = simple_tcpv6_packet(pktlen=114,
                                          eth_dst=dmac,
                                          eth_src=router_mac,
                                          ipv6_dst=ip_da,
                                          ipv6_src=src_ip_addr,
                                          ipv6_hlim=99,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_68_lag_hash_basic_mpls_ipv6_inner_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_68_lag_hash_basic_mpls_ipv6_inner_dst_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
        dmac = '00:55:55:55:55:66'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_ip = '1234:5678:9abc:def0:4422:1133:5577:{0}'
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = dst_ip.format(str(i).zfill(4)[2:])
                ip_only_pkt = simple_tcpv6_only_packet(
                                          ipv6_dst=dst_ip_addr,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                       
                exp_pkt = simple_tcpv6_packet(pktlen=114,
                                          eth_dst=dmac,
                                          eth_src=router_mac,
                                          ipv6_dst=dst_ip_addr,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=99,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_69_lag_hash_basic_mpls_ipv6_inner_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_69_lag_hash_basic_mpls_ipv6_inner_src_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
        dmac = '00:55:55:55:55:66'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_packet(
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=src_port,
                                          tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                       
                exp_pkt = simple_tcpv6_packet(pktlen=114,
                                          eth_dst=dmac,
                                          eth_src=router_mac,
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=99,
                                          tcp_sport=src_port,
                                          tcp_dport=80)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_70_lag_hash_basic_mpls_ipv6_inner_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_70_lag_hash_basic_mpls_ipv6_inner_dst_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
        dmac = '00:55:55:55:55:66'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_port = 80
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_packet(
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=dst_port)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                       
                exp_pkt = simple_tcpv6_packet(pktlen=114,
                                          eth_dst=dmac,
                                          eth_src=router_mac,
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=99,
                                          tcp_sport=1234,
                                          tcp_dport=dst_port)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_71_lag_hash_basic_mpls_ipv6_inner_ip_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_71_lag_hash_basic_mpls_ipv6_inner_ip_protocol_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
        dmac = '00:55:55:55:55:66'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner ip protocol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            nh = 1
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner ip protocol is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_no_l4hdr_packet(
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          ipv6_nh=nh)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                       
                exp_pkt = simple_tcpv6_no_l4hdr_packet(pktlen=114,
                                          eth_dst=dmac,
                                          eth_src=router_mac,
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=99,
                                          ipv6_nh=nh)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                nh += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
#===========================================

#====================L3VPN==================
class scenario_72_lag_hash_l3vpn_ipv6_inner_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_72_lag_hash_l3vpn_ipv6_inner_src_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6

        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac = '00:55:55:55:55:66'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = '2001:db8:85a3::8a2e:370:73{0}'
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = src_ip.format(str(i).zfill(4)[2:])
                ip_only_pkt = simple_tcpv6_only_packet(
                                          ipv6_dst=ip_da,
                                          ipv6_src=src_ip_addr,
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcpv6_packet(pktlen=114,
                                          eth_dst=dmac,
                                          eth_src=router_mac,
                                          ipv6_dst=ip_da,
                                          ipv6_src=src_ip_addr,
                                          ipv6_hlim=99,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_73_lag_hash_l3vpn_ipv6_inner_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_73_lag_hash_l3vpn_ipv6_inner_dst_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6

        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac = '00:55:55:55:55:66'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_ip = '1234:5678:9abc:def0:4422:1133:5577:99{0}'
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = dst_ip.format(str(i).zfill(4)[2:])
                ip_only_pkt = simple_tcpv6_only_packet(
                                          ipv6_dst=dst_ip_addr,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcpv6_packet(pktlen=114,
                                          eth_dst=dmac,
                                          eth_src=router_mac,
                                          ipv6_dst=dst_ip_addr,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=99,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_74_lag_hash_l3vpn_ipv6_inner_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_74_lag_hash_l3vpn_ipv6_inner_src_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6

        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac = '00:55:55:55:55:66'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_packet(
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=src_port,
                                          tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcpv6_packet(pktlen=114,
                                          eth_dst=dmac,
                                          eth_src=router_mac,
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=99,
                                          tcp_sport=src_port,
                                          tcp_dport=80)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_75_lag_hash_l3vpn_ipv6_inner_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_75_lag_hash_l3vpn_ipv6_inner_dst_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6

        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac = '00:55:55:55:55:66'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_port = 80
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_packet(
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=dst_port)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcpv6_packet(pktlen=114,
                                          eth_dst=dmac,
                                          eth_src=router_mac,
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=99,
                                          tcp_sport=1234,
                                          tcp_dport=dst_port)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_76_lag_hash_l3vpn_ipv6_inner_ip_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_76_lag_hash_l3vpn_ipv6_inner_ip_protocol_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6

        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac = '00:55:55:55:55:66'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner ip protocol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            nh = 1
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner ip protocol is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_no_l4hdr_packet(
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          ipv6_nh=nh)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt = simple_tcpv6_no_l4hdr_packet(pktlen=114,
                                          eth_dst=dmac,
                                          eth_src=router_mac,
                                          ipv6_dst=ip_da,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=99,
                                          ipv6_nh=nh)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                nh += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
#===========================================

#====================L2VPN==================
class scenario_77_lag_hash_l2vpn_ipv6_inner_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_77_lag_hash_l2vpn_ipv6_inner_src_ip_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = '2001:db8:85a3::8a2e:370:73{0}'
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = src_ip.format(str(i).zfill(4)[2:])
                mpls_inner_pkt = simple_tcpv6_packet(eth_dst=mac1,
                                          eth_src=mac2,
                                          dl_vlan_enable=True,
                                          vlan_vid=30,
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src=src_ip_addr,
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcpv6_packet(eth_dst=mac1,
                                              eth_src=mac2,
                                              dl_vlan_enable=True,
                                              vlan_vid=20,
                                              ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_src=src_ip_addr,
                                              ipv6_hlim=64,
                                              tcp_sport=1234,
                                              tcp_dport=80)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_78_lag_hash_l2vpn_ipv6_inner_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_78_lag_hash_l2vpn_ipv6_inner_dst_ip_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_ip = '2001:db8:85a3::8a2e:370:73{0}'
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = dst_ip.format(str(i).zfill(4)[2:])
                mpls_inner_pkt = simple_tcpv6_packet(eth_dst=mac1,
                                          eth_src=mac2,
                                          dl_vlan_enable=True,
                                          vlan_vid=30,
                                          ipv6_dst=dst_ip_addr,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcpv6_packet(eth_dst=mac1,
                                              eth_src=mac2,
                                              dl_vlan_enable=True,
                                              vlan_vid=20,
                                              ipv6_dst=dst_ip_addr,
                                              ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_hlim=64,
                                              tcp_sport=1234,
                                              tcp_dport=80)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_79_lag_hash_l2vpn_ipv6_inner_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_79_lag_hash_l2vpn_ipv6_inner_src_port_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src port is not equal======")
            for i in range(0, max_itrs):
                mpls_inner_pkt = simple_tcpv6_packet(eth_dst=mac1,
                                          eth_src=mac2,
                                          dl_vlan_enable=True,
                                          vlan_vid=30,
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_hlim=64,
                                          tcp_sport=src_port,
                                          tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcpv6_packet(eth_dst=mac1,
                                              eth_src=mac2,
                                              dl_vlan_enable=True,
                                              vlan_vid=20,
                                              ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                              ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_hlim=64,
                                              tcp_sport=src_port,
                                              tcp_dport=80)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_80_lag_hash_l2vpn_ipv6_inner_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_80_lag_hash_l2vpn_ipv6_inner_dst_port_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_port = 1234
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst port is not equal======")
            for i in range(0, max_itrs):
                mpls_inner_pkt = simple_tcpv6_packet(eth_dst=mac1,
                                          eth_src=mac2,
                                          dl_vlan_enable=True,
                                          vlan_vid=30,
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=dst_port)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcpv6_packet(eth_dst=mac1,
                                              eth_src=mac2,
                                              dl_vlan_enable=True,
                                              vlan_vid=20,
                                              ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                              ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_hlim=64,
                                              tcp_sport=1234,
                                              tcp_dport=dst_port)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_81_lag_hash_l2vpn_ipv6_inner_ip_protocol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_81_lag_hash_l2vpn_ipv6_inner_ip_protocol_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner ip protocol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            nh = 1
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner ip protocol is not equal======")
            for i in range(0, max_itrs):
                mpls_inner_pkt = simple_tcpv6_no_l4hdr_packet(eth_dst=mac1,
                                          eth_src=mac2,
                                          dl_vlan_enable=True,
                                          vlan_vid=30,
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_hlim=64,
                                          ipv6_nh=nh)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcpv6_no_l4hdr_packet(eth_dst=mac1,
                                              eth_src=mac2,
                                              dl_vlan_enable=True,
                                              vlan_vid=20,
                                              ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                              ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_hlim=64,
                                              ipv6_nh=nh)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                nh += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_82_lag_hash_l2vpn_ipv6_inner_src_mac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_82_lag_hash_l2vpn_ipv6_inner_src_mac_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_MAC]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src mac to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_mac_start = '00:00:00:01:02:{0}'
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src mac is not equal======")
            for i in range(0, max_itrs):
                src_mac = src_mac_start.format(str(i).zfill(4)[2:])
                mpls_inner_pkt = simple_tcpv6_packet(eth_dst=mac1,
                                          eth_src=src_mac,
                                          dl_vlan_enable=True,
                                          vlan_vid=30,
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcpv6_packet(eth_dst=mac1,
                                              eth_src=src_mac,
                                              dl_vlan_enable=True,
                                              vlan_vid=20,
                                              ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                              ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_hlim=64,
                                              tcp_sport=1234,
                                              tcp_dport=80)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            #include the fdb which is learning
            flush_all_fdb(self.client)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_83_lag_hash_l2vpn_ipv6_inner_dst_mac_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("scenario_83_lag_hash_l2vpn_ipv6_inner_dst_mac_test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_MAC]

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner dst mac to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        sys_logging("======create a bridge======")
        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        sys_logging("======create tunnels======")
        #tunnel_id1 = sai_thrift_create_tunnel_mpls_l2vpn(self.client, encap_tagged_vlan=30)
        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        #rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        sys_logging("======create neighbor and nexthop======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sys_logging("======create entrys======")
        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)        

        bport = sai_thrift_create_bridge_sub_port(self.client, lag_id1, bridge_id, vlan_id)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id)

        sys_logging("======create fdbs======")
        mac_action = SAI_PACKET_ACTION_FORWARD
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac1, bport, mac_action)
        sai_thrift_create_fdb_bport(self.client, bridge_id, mac2, tunnel_bport, mac_action)

        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_mac_start = '00:00:00:01:02:{0}'
            mpls_label_stack = [{'label':label1,'tc':0,'ttl':64,'s':0},{'label':label2,'tc':0,'ttl':32,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner dst mac is not equal======")
            for i in range(0, max_itrs):
                dst_mac = dst_mac_start.format(str(i).zfill(4)[2:])
                mpls_inner_pkt = simple_tcpv6_packet(eth_dst=dst_mac,
                                          eth_src=mac2,
                                          dl_vlan_enable=True,
                                          vlan_vid=30,
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:55:55:55:55:66',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls_label_stack,
                                        inner_frame = mpls_inner_pkt)
                exp_pkt = simple_tcpv6_packet(eth_dst=dst_mac,
                                              eth_src=mac2,
                                              dl_vlan_enable=True,
                                              vlan_vid=20,
                                              ipv6_dst='2001:db8:85a3::8a2e:370:7334',
                                              ipv6_src='2001:db8:85a3::8a2e:370:7335',
                                              ipv6_hlim=64,
                                              tcp_sport=1234,
                                              tcp_dport=80)
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")
        finally:
            sys_logging("======clean up======")
            #include the fdb which is learning
            flush_all_fdb(self.client)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac1, bport)
            #sai_thrift_delete_fdb(self.client, bridge_id, mac2, tunnel_bport)
            
            sai_thrift_remove_bridge_sub_port(self.client, bport, lag_id1)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls1 = sai_thrift_inseg_entry_t(label1)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)

            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_tunnel(tunnel_id2)
            self.client.sai_thrift_remove_bridge(bridge_id)

            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
#===========================================

class scenario_84_lag_hash_ipv6_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_84_lag_hash_ipv6_multi_test======")
        switch_init(self.client)
        vlan_id = 10
        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_L4_DST_PORT]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]

        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        is_lag = True
        sys_logging("======create a vlan======")
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        lag_oid1 = sai_thrift_create_bport_by_lag(self.client, lag_id1)
        print"lag:%lx" %lag_id1
        print"lag_oid:%lx" %lag_oid1

        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        sys_logging("======add lag and port4 to vlan======")
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_oid1, SAI_VLAN_TAGGING_MODE_UNTAGGED, is_lag)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)

        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)

        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)

        sai_thrift_create_fdb_bport(self.client, vlan_oid, mac1, lag_oid1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set src ip,dst ip,src port,dst port to calculate hash======")
        #Hash field list
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            dst_port = 80
            m = 0
            n = 0
            src_ip = ['2001:db8:85a3::8a2e:370:7300', '2001:db8:85a3::8a2e:370:7301', '2001:db8:85a3::8a2e:370:7302', '2001:db8:85a3::8a2e:370:7303', '2001:db8:85a3::8a2e:370:7304',
                      '2001:db8:85a3::8a2e:370:7305', '2001:db8:85a3::8a2e:370:7306', '2001:db8:85a3::8a2e:370:7307', '2001:db8:85a3::8a2e:370:7308', '2001:db8:85a3::8a2e:370:7309',
                      '2001:db8:85a3::8a2e:370:730a', '2001:db8:85a3::8a2e:370:730b', '2001:db8:85a3::8a2e:370:730c', '2001:db8:85a3::8a2e:370:730d', '2001:db8:85a3::8a2e:370:730e',
                      '2001:db8:85a3::8a2e:370:730f', '2001:db8:85a3::8a2e:370:7310', '2001:db8:85a3::8a2e:370:7311', '2001:db8:85a3::8a2e:370:7312', '2001:db8:85a3::8a2e:370:7313']
            dst_ip = ['2001:db8:85a3::8a2e:370:7400', '2001:db8:85a3::8a2e:370:7401', '2001:db8:85a3::8a2e:370:7402', '2001:db8:85a3::8a2e:370:7403', '2001:db8:85a3::8a2e:370:7404',
                      '2001:db8:85a3::8a2e:370:7405', '2001:db8:85a3::8a2e:370:7406', '2001:db8:85a3::8a2e:370:7407', '2001:db8:85a3::8a2e:370:7408', '2001:db8:85a3::8a2e:370:7409',
                      '2001:db8:85a3::8a2e:370:740a', '2001:db8:85a3::8a2e:370:740b', '2001:db8:85a3::8a2e:370:740c', '2001:db8:85a3::8a2e:370:740d', '2001:db8:85a3::8a2e:370:740e',
                      '2001:db8:85a3::8a2e:370:740f', '2001:db8:85a3::8a2e:370:7410', '2001:db8:85a3::8a2e:370:7411', '2001:db8:85a3::8a2e:370:7412', '2001:db8:85a3::8a2e:370:7413']
            sys_logging("======send 20 packages to lag,every package's src ip,dst ip,src port,dst port is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcpv6_packet(eth_dst='00:11:11:11:11:11',
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst=dst_ip[n],
                                          ipv6_src=src_ip[m],
                                          ipv6_hlim=64,
                                          tcp_sport=src_port,
                                          tcp_dport=dst_port)

                exp_pkt = simple_tcpv6_packet(eth_dst='00:11:11:11:11:11',
                                              eth_src='00:22:22:22:22:22',
                                              ipv6_dst=dst_ip[n],
                                              ipv6_src=src_ip[m],
                                              ipv6_hlim=64,
                                              tcp_sport=src_port,
                                              tcp_dport=dst_port)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                #src_port += 1
                #dst_port += 1
                #m += 1
                n += 1

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                       "Not all paths are equally balanced")

            pkt = simple_tcpv6_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            exp_pkt = simple_tcpv6_packet(eth_src='00:11:11:11:11:11',
                                          eth_dst='00:22:22:22:22:22',
                                          ipv6_dst='2001:db8:85a3::8a2e:370:7335',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            print "Sending packet port 1 (lag member) -> port 4"
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 2 (lag member) -> port 4"
            self.ctc_send_packet( 1, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])
            print "Sending packet port 3 (lag member) -> port 4"
            self.ctc_send_packet( 2, str(pkt))
            self.ctc_verify_packets( exp_pkt, [3])

        finally:
            sys_logging("======clean up======")
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_oid1)

            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            
            sai_thrift_remove_bport_by_lag(self.client, lag_oid1)
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            for port in sai_port_list:
                sai_thrift_create_vlan_member(self.client, switch.default_vlan.oid, port, SAI_VLAN_TAGGING_MODE_UNTAGGED)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port4, attr) 
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)

class scenario_85_lag_hash_ipv6_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_85_lag_hash_ipv6_multi_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        
        dmac = '00:55:55:55:55:66'
        ip_da = '1234:5678:9abc:def0:4422:1133:5577:99aa'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_lag = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP, SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        sys_logging("======create a lag include three ports======")
        lag_id1 = sai_thrift_create_lag(self.client)
        print"lag:%lx" %lag_id1
        
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)

        #get lag hash object id
        sys_logging("======get lag hash object id======")
        ids_list = [SAI_SWITCH_ATTR_LAG_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_LAG_HASH:
                sys_logging("### SAI_SWITCH_ATTR_LAG_HASH = %d ###"  %attribute.value.oid)
                hash_id_lag = attribute.value.oid

        sys_logging("======set inner src ip,inner dst ip,inner src port,inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, lag_id1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        
        sys_logging("======create neighbor======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        sys_logging("======create next hop======")
        next_hop = sai_thrift_create_nhop(self.client, addr_family, ip_da, rif_id1)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            dst_port = 80
            m = 0
            n = 0
            src_ip = ['2001:db8:85a3::8a2e:370:7300', '2001:db8:85a3::8a2e:370:7301', '2001:db8:85a3::8a2e:370:7302', '2001:db8:85a3::8a2e:370:7303', '2001:db8:85a3::8a2e:370:7304',
                      '2001:db8:85a3::8a2e:370:7305', '2001:db8:85a3::8a2e:370:7306', '2001:db8:85a3::8a2e:370:7307', '2001:db8:85a3::8a2e:370:7308', '2001:db8:85a3::8a2e:370:7309',
                      '2001:db8:85a3::8a2e:370:730a', '2001:db8:85a3::8a2e:370:730b', '2001:db8:85a3::8a2e:370:730c', '2001:db8:85a3::8a2e:370:730d', '2001:db8:85a3::8a2e:370:730e',
                      '2001:db8:85a3::8a2e:370:730f', '2001:db8:85a3::8a2e:370:7310', '2001:db8:85a3::8a2e:370:7311', '2001:db8:85a3::8a2e:370:7312', '2001:db8:85a3::8a2e:370:7313']
            dst_ip = ['1234:5678:9abc:def0:4422:1133:5577:9900', '1234:5678:9abc:def0:4422:1133:5577:9901', '1234:5678:9abc:def0:4422:1133:5577:9902', '1234:5678:9abc:def0:4422:1133:5577:9903',
			          '1234:5678:9abc:def0:4422:1133:5577:9904', '1234:5678:9abc:def0:4422:1133:5577:9905', '1234:5678:9abc:def0:4422:1133:5577:9906', '1234:5678:9abc:def0:4422:1133:5577:9907',
					  '1234:5678:9abc:def0:4422:1133:5577:9908', '1234:5678:9abc:def0:4422:1133:5577:9909', '1234:5678:9abc:def0:4422:1133:5577:990a', '1234:5678:9abc:def0:4422:1133:5577:990b',
					  '1234:5678:9abc:def0:4422:1133:5577:990c', '1234:5678:9abc:def0:4422:1133:5577:990d', '1234:5678:9abc:def0:4422:1133:5577:990e', '1234:5678:9abc:def0:4422:1133:5577:990f',
					  '1234:5678:9abc:def0:4422:1133:5577:9910', '1234:5678:9abc:def0:4422:1133:5577:9911', '1234:5678:9abc:def0:4422:1133:5577:9912', '1234:5678:9abc:def0:4422:1133:5577:9913']
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to lag,every package's inner src ip,inner dst ip,inner src port,inner dst port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_packet(
                                          ipv6_dst=dst_ip[n],
                                          ipv6_src=src_ip[m],
                                          ipv6_hlim=64,
                                          tcp_sport=src_port,
                                          tcp_dport=dst_port)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                       
                exp_pkt = simple_tcpv6_packet(pktlen=114,
                                          eth_dst=dmac,
                                          eth_src=router_mac,
                                          ipv6_dst=dst_ip[n],
                                          ipv6_src=src_ip[m],
                                          ipv6_hlim=99,
                                          tcp_sport=src_port,
                                          tcp_dport=dst_port)
                
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                #src_port += 1
                #dst_port += 1
                #m += 1
                n += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, next_hop)
            
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            
            sai_thrift_remove_lag_member(self.client, lag_member_id1)
            sai_thrift_remove_lag_member(self.client, lag_member_id2)
            sai_thrift_remove_lag_member(self.client, lag_member_id3)
            sai_thrift_remove_lag(self.client, lag_id1)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
                
#=================add  ecmp=====================
class scenario_86_ecmp_hash_ipv6_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_31_ecmp_hash_src_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP]

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt1 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:55',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt2 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:56',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt3 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:57',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            src_ip = '2001:db8:85a3::8a2e:370:73{0}'
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = src_ip.format(str(i).zfill(4)[2:])
                pkt = simple_tcpv6_packet(eth_dst=router_mac,
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                          ipv6_src=src_ip_addr,
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
                exp_pkt1 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src=src_ip_addr,
                                        ipv6_hlim=63,
                                        tcp_sport=1234,
                                        tcp_dport=80)
                exp_pkt2 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src=src_ip_addr,
                                        ipv6_hlim=63,
                                        tcp_sport=1234,
                                        tcp_dport=80)
                exp_pkt3 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src=src_ip_addr,
                                        ipv6_hlim=63,
                                        tcp_sport=1234,
                                        tcp_dport=80)
            
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
                
class scenario_87_ecmp_hash_ipv6_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_87_ecmp_hash_ipv6_dst_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_DST_IP]

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt1 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:55',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt2 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:56',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt3 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:57',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            dst_ip = '1234:5678:9abc:def0:4422:1133:5577:98{0}'
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = dst_ip.format(str(i).zfill(4)[2:])
                pkt = simple_tcpv6_packet(eth_dst=router_mac,
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst=dst_ip_addr,
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
                exp_pkt1 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ipv6_dst=dst_ip_addr,
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        tcp_sport=1234,
                                        tcp_dport=80)
                exp_pkt2 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ipv6_dst=dst_ip_addr,
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        tcp_sport=1234,
                                        tcp_dport=80)
                exp_pkt3 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ipv6_dst=dst_ip_addr,
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        tcp_sport=1234,
                                        tcp_dport=80)
            
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                print"*********************** rcv_idx:%d" %rcv_idx

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_88_ecmp_hash_ipv6_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_88_ecmp_hash_ipv6_src_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_L4_SRC_PORT]

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt1 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:55',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt2 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:56',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt3 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:57',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            src_port = 1234
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's src port is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcpv6_packet(eth_dst=router_mac,
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=src_port,
                                          tcp_dport=80)
            
                exp_pkt1 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        tcp_sport=src_port,
                                        tcp_dport=80)
                exp_pkt2 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        tcp_sport=src_port,
                                        tcp_dport=80)
                exp_pkt3 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        tcp_sport=src_port,
                                        tcp_dport=80)
            
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                src_port += 1
                print"*********************** rcv_idx:%d" %rcv_idx

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_89_ecmp_hash_ipv6_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_89_ecmp_hash_ipv6_dst_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_L4_DST_PORT]

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt1 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:55',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt2 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:56',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt3 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:57',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            dst_port = 80
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's dst port is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcpv6_packet(eth_dst=router_mac,
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=dst_port)
            
                exp_pkt1 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port)
                exp_pkt2 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port)
                exp_pkt3 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port)
            
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                dst_port += 1
                print"*********************** rcv_idx:%d" %rcv_idx

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_90_ecmp_hash_ipv6_ip_procotol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_90_ecmp_hash_ipv6_ip_procotol_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_IP_PROTOCOL]

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set ip procotol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcpv6_no_l4hdr_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          ipv6_nh=1)

            exp_pkt1 = simple_tcpv6_no_l4hdr_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:55',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          ipv6_nh=1)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcpv6_no_l4hdr_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          ipv6_nh=1)

            exp_pkt2 = simple_tcpv6_no_l4hdr_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:56',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          ipv6_nh=1)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcpv6_no_l4hdr_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          ipv6_nh=1)

            exp_pkt3 = simple_tcpv6_no_l4hdr_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:57',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          ipv6_nh=1)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            nh = 1
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's ip procotol is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcpv6_no_l4hdr_packet(eth_dst=router_mac,
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          ipv6_nh=nh)
            
                exp_pkt1 = simple_tcpv6_no_l4hdr_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        ipv6_nh=nh)
                exp_pkt2 = simple_tcpv6_no_l4hdr_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        ipv6_nh=nh)
                exp_pkt3 = simple_tcpv6_no_l4hdr_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_hlim=63,
                                        ipv6_nh=nh)
            
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                nh += 1
                print"*********************** rcv_idx:%d" %rcv_idx

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

#=================basic mpls================
class scenario_91_ecmp_hash_basic_mpls_ipv6_inner_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_91_ecmp_hash_basic_mpls_ipv6_inner_src_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = '2001:db8:85a3::8a2e:370:73{0}'
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = src_ip.format(str(i).zfill(4)[2:])
                ip_only_pkt = simple_tcpv6_only_packet(
                                        ipv6_src=src_ip_addr,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_hlim=64,
                                        tcp_sport=1234,
                                        tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src=src_ip_addr,
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                exp_pkt2 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src=src_ip_addr,
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                exp_pkt3 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src=src_ip_addr,
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)  
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_92_ecmp_hash_basic_mpls_ipv6_inner_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_92_ecmp_hash_basic_mpls_ipv6_inner_dst_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_ip = '1234:5678:9abc:def0:4422:1133:5577:98{0}'
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = dst_ip.format(str(i).zfill(4)[2:])
                ip_only_pkt = simple_tcpv6_only_packet(
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_dst=dst_ip_addr,
                                        ipv6_hlim=64,
                                        tcp_sport=1234,
                                        tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ipv6_dst=dst_ip_addr,
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                exp_pkt2 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ipv6_dst=dst_ip_addr,
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                exp_pkt3 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ipv6_dst=dst_ip_addr,
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)  
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_93_ecmp_hash_basic_mpls_ipv6_inner_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_93_ecmp_hash_basic_mpls_ipv6_inner_src_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner src port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_packet(
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_hlim=64,
                                        tcp_sport=src_port,
                                        tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                exp_pkt2 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                exp_pkt3 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)  
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_94_ecmp_hash_basic_mpls_ipv6_inner_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_94_ecmp_hash_basic_mpls_ipv6_inner_dst_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_port = 80
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner dst port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_packet(
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_hlim=64,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                exp_pkt2 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                exp_pkt3 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)  
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_95_ecmp_hash_basic_mpls_ipv6_inner_ip_procotol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_95_ecmp_hash_basic_mpls_ipv6_inner_ip_procotol_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner ip procotol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            nh = 1
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner ip procotol is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_no_l4hdr_packet(
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_hlim=64,
                                        ipv6_nh=nh)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcpv6_no_l4hdr_packet(pktlen=114,
                                       eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       ipv6_nh=nh)

                exp_pkt2 = simple_tcpv6_no_l4hdr_packet(pktlen=114,
                                       eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       ipv6_nh=nh)

                exp_pkt3 = simple_tcpv6_no_l4hdr_packet(pktlen=114,
                                       eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       ipv6_nh=nh)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                nh += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)  
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
#===========================================

#====================L3VPN==================
class scenario_96_ecmp_hash_l3vpn_ipv6_inner_src_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_96_ecmp_hash_l3vpn_ipv6_inner_src_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner src ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_ip = '2001:db8:85a3::8a2e:370:73{0}'
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner src ip is not equal======")
            for i in range(0, max_itrs):
                src_ip_addr = src_ip.format(str(i).zfill(4)[2:])
                ip_only_pkt = simple_tcpv6_only_packet(
                                        ipv6_src=src_ip_addr,
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_hlim=64,
                                        tcp_sport=1234,
                                        tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src=src_ip_addr,
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                exp_pkt2 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src=src_ip_addr,
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                exp_pkt3 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src=src_ip_addr,
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_97_ecmp_hash_l3vpn_ipv6_inner_dst_ip_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_97_ecmp_hash_l3vpn_ipv6_inner_dst_ip_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_DST_IP]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner dst ip to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_ip = '1234:5678:9abc:def0:4422:1133:5577:98{0}'
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner dst ip is not equal======")
            for i in range(0, max_itrs):
                dst_ip_addr = dst_ip.format(str(i).zfill(4)[2:])
                ip_only_pkt = simple_tcpv6_only_packet(
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_dst=dst_ip_addr,
                                        ipv6_hlim=64,
                                        tcp_sport=1234,
                                        tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ipv6_dst=dst_ip_addr,
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                exp_pkt2 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ipv6_dst=dst_ip_addr,
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                exp_pkt3 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ipv6_dst=dst_ip_addr,
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_98_ecmp_hash_l3vpn_ipv6_inner_src_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_98_ecmp_hash_l3vpn_ipv6_inner_src_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner src port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner src port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_packet(
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_hlim=64,
                                        tcp_sport=src_port,
                                        tcp_dport=80)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                exp_pkt2 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                exp_pkt3 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=src_port,
                                       tcp_dport=80)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                src_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_99_ecmp_hash_l3vpn_ipv6_inner_dst_port_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_99_ecmp_hash_l3vpn_ipv6_inner_dst_port_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            dst_port = 80
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner dst port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_packet(
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_hlim=64,
                                        tcp_sport=1234,
                                        tcp_dport=dst_port)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                exp_pkt2 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                exp_pkt3 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       tcp_sport=1234,
                                       tcp_dport=dst_port)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                dst_port += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_100_ecmp_hash_l3vpn_ipv6_inner_ip_procotol_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_100_ecmp_hash_l3vpn_ipv6_inner_ip_procotol_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200
        label2 = 300

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_IP_PROTOCOL]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner ip procotol to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        tunnel_id = sai_thrift_create_tunnel_mpls(self.client)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        rif_id4 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id4, packet_action, tunnel_id=tunnel_id)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            nh = 1
            mpls = [{'label':200,'tc':3,'ttl':100,'s':0}, {'label':300,'tc':3,'ttl':50,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner ip procotol is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_no_l4hdr_packet(
                                        ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                        ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                        ipv6_hlim=64,
                                        ipv6_nh=nh)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcpv6_no_l4hdr_packet(pktlen=114,
                                       eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       ipv6_nh=nh)

                exp_pkt2 = simple_tcpv6_no_l4hdr_packet(pktlen=114,
                                       eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       ipv6_nh=nh)

                exp_pkt3 = simple_tcpv6_no_l4hdr_packet(pktlen=114,
                                       eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9904',
                                       ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                       ipv6_hlim=99,
                                       ipv6_nh=nh)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                nh += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1) 
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls1)
            self.client.sai_thrift_remove_inseg_entry(mpls2)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_router_interface(rif_id4)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
#===========================================

class scenario_101_ecmp_hash_ipv6_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_101_ecmp_hash_ipv6_multi_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_SRC_IP, SAI_NATIVE_HASH_FIELD_DST_IP, SAI_NATIVE_HASH_FIELD_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_L4_DST_PORT]

        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        ip_addr1_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask1 = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'

        sys_logging("======create a VRF======")
        vr1 = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create four interfaces======")
        rif1 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif2 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif3 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif4 = sai_thrift_create_router_interface(self.client, vr1, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif1)
        nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif2)
        nhop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif3)
        
        sys_logging("======add nexthops to group======")
        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, nhop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set src ip,dst ip,src port,dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

        warmboot(self.client)
        try:
            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt1 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:55',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9901',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt1, [0])

            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt2 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:56',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9902',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt2, [1])

            pkt = simple_tcpv6_packet(eth_src='00:22:22:22:22:22',
                                          eth_dst=router_mac,
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=64,
                                          tcp_sport=1234,
                                          tcp_dport=80)

            exp_pkt3 = simple_tcpv6_packet(eth_src=router_mac,
                                          eth_dst='00:11:22:33:44:57',
                                          ipv6_dst='1234:5678:9abc:def0:4422:1133:5577:9903',
                                          ipv6_src='2001:db8:85a3::8a2e:370:7334',
                                          ipv6_hlim=63,
                                          tcp_sport=1234,
                                          tcp_dport=80)
            
            self.ctc_send_packet( 3, str(pkt))
            self.ctc_verify_packets( exp_pkt3, [2])

            count = [0, 0, 0]
            src_port = 1234
            dst_port = 80
            m = 0
            n = 0
            src_ip = ['2001:db8:85a3::8a2e:370:7300', '2001:db8:85a3::8a2e:370:7301', '2001:db8:85a3::8a2e:370:7302', '2001:db8:85a3::8a2e:370:7303', '2001:db8:85a3::8a2e:370:7304',
                      '2001:db8:85a3::8a2e:370:7305', '2001:db8:85a3::8a2e:370:7306', '2001:db8:85a3::8a2e:370:7307', '2001:db8:85a3::8a2e:370:7308', '2001:db8:85a3::8a2e:370:7309',
                      '2001:db8:85a3::8a2e:370:730a', '2001:db8:85a3::8a2e:370:730b', '2001:db8:85a3::8a2e:370:730c', '2001:db8:85a3::8a2e:370:730d', '2001:db8:85a3::8a2e:370:730e',
                      '2001:db8:85a3::8a2e:370:730f', '2001:db8:85a3::8a2e:370:7310', '2001:db8:85a3::8a2e:370:7311', '2001:db8:85a3::8a2e:370:7312', '2001:db8:85a3::8a2e:370:7313']
            dst_ip = ['1234:5678:9abc:def0:4422:1133:5577:9904', '1234:5678:9abc:def0:4422:1133:5577:9905', '1234:5678:9abc:def0:4422:1133:5577:9906', '1234:5678:9abc:def0:4422:1133:5577:9907',
			          '1234:5678:9abc:def0:4422:1133:5577:9908', '1234:5678:9abc:def0:4422:1133:5577:9909', '1234:5678:9abc:def0:4422:1133:5577:990a', '1234:5678:9abc:def0:4422:1133:5577:990b',
					  '1234:5678:9abc:def0:4422:1133:5577:990c', '1234:5678:9abc:def0:4422:1133:5577:990d', '1234:5678:9abc:def0:4422:1133:5577:990e', '1234:5678:9abc:def0:4422:1133:5577:990f',
					  '1234:5678:9abc:def0:4422:1133:5577:9910', '1234:5678:9abc:def0:4422:1133:5577:9911', '1234:5678:9abc:def0:4422:1133:5577:9912', '1234:5678:9abc:def0:4422:1133:5577:9913',
					  '1234:5678:9abc:def0:4422:1133:5577:9914', '1234:5678:9abc:def0:4422:1133:5577:9915', '1234:5678:9abc:def0:4422:1133:5577:9916', '1234:5678:9abc:def0:4422:1133:5577:9917']
            max_itrs = 20
            sys_logging("======send 20 packages to ecmp,every package's src ip,dst ip,src port,dst port is not equal======")
            for i in range(0, max_itrs):
                pkt = simple_tcpv6_packet(eth_dst=router_mac,
                                          eth_src='00:22:22:22:22:22',
                                          ipv6_dst=dst_ip[n],
                                          ipv6_src=src_ip[m],
                                          ipv6_hlim=64,
                                          tcp_sport=src_port,
                                          tcp_dport=dst_port)
            
                exp_pkt1 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:55',
                                        eth_src=router_mac,
                                        ipv6_dst=dst_ip[n],
                                        ipv6_src=src_ip[m],
                                        ipv6_hlim=63,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port)
                exp_pkt2 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:56',
                                        eth_src=router_mac,
                                        ipv6_dst=dst_ip[n],
                                        ipv6_src=src_ip[m],
                                        ipv6_hlim=63,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port)
                exp_pkt3 = simple_tcpv6_packet(eth_dst='00:11:22:33:44:57',
                                        eth_src=router_mac,
                                        ipv6_dst=dst_ip[n],
                                        ipv6_src=src_ip[m],
                                        ipv6_hlim=63,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port)
            
                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port( [exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                count[rcv_idx] += 1
                #src_port += 1
                #dst_port += 1
                #m += 1
                n += 1
                print"*********************** rcv_idx:%d" %rcv_idx

            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.8)),
                        "Not all paths are equally balanced")
                        
        finally:
            sys_logging("======clean up======")
            sai_thrift_remove_route(self.client, vr1, addr_family, ip_addr1_subnet, ip_mask1, nhop_group1)
            
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)
            
            self.client.sai_thrift_remove_next_hop(nhop1)
            self.client.sai_thrift_remove_next_hop(nhop2)
            self.client.sai_thrift_remove_next_hop(nhop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif1)
            self.client.sai_thrift_remove_router_interface(rif2)
            self.client.sai_thrift_remove_router_interface(rif3)
            self.client.sai_thrift_remove_router_interface(rif4)
            
            self.client.sai_thrift_remove_virtual_router(vr1)  
            
            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)

class scenario_102_ecmp_hash_ipv6_multi_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        sys_logging("======scenario_102_ecmp_hash_ipv6_multi_test======")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        addr_family = SAI_IP_ADDR_FAMILY_IPV6
        ip_addr1 = '1234:5678:9abc:def0:4422:1133:5577:9901'
        ip_addr2 = '1234:5678:9abc:def0:4422:1133:5577:9902'
        ip_addr3 = '1234:5678:9abc:def0:4422:1133:5577:9903'
        dmac1 = '00:11:22:33:44:55'
        dmac2 = '00:11:22:33:44:56'
        dmac3 = '00:11:22:33:44:57'
        ip_addr_subnet = '1234:5678:9abc:def0:4422:1133:5577:0'
        ip_mask = 'ffff:ffff:ffff:ffff:ffff:ffff:ffff:0'

        label1 = 200

        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        hash_id_ecmp = 0
        field_list = [SAI_NATIVE_HASH_FIELD_INNER_SRC_IP, SAI_NATIVE_HASH_FIELD_INNER_DST_IP, SAI_NATIVE_HASH_FIELD_INNER_L4_SRC_PORT, SAI_NATIVE_HASH_FIELD_INNER_L4_DST_PORT]

        # get ecmp hash object id
        sys_logging("======get ecmp hash object id======")
        ids_list = [SAI_SWITCH_ATTR_ECMP_HASH]
        switch_attr_list = self.client.sai_thrift_get_switch_attribute(ids_list)
        attr_list = switch_attr_list.attr_list
        for attribute in attr_list:
            if attribute.id == SAI_SWITCH_ATTR_ECMP_HASH:
                sys_logging("### SAI_SWITCH_ATTR_ECMP_HASH = %d ###"  %attribute.value.oid)
                hash_id_ecmp = attribute.value.oid

        sys_logging("======set inner src ip,inner dst ip,inner src port,inner dst port to calculate hash======")
        if field_list:
            hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
            attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                            value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)
        
        sys_logging("======create a VRF======")
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        sys_logging("======create interfaces======")
        rif_id1_1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id1_2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        rif_id1_3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port3, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port4, 0, v4_enabled, v6_enabled, mac)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)

        sys_logging("======create neighbors======")
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)

        sys_logging("======create nexthops======")
        next_hop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1_1)
        next_hop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id1_2)
        next_hop3 = sai_thrift_create_nhop(self.client, addr_family, ip_addr3, rif_id1_3)

        nhop_group1 = sai_thrift_create_next_hop_group(self.client)
        nhop_gmember1 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop1)
        nhop_gmember2 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop2)
        nhop_gmember3 = sai_thrift_create_next_hop_group_member(self.client, nhop_group1, next_hop3)

        sys_logging("======create route======")
        sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        
        warmboot(self.client)
        try:
            count = [0, 0, 0]
            max_itrs = 20
            src_port = 1234
            dst_port = 80
            m = 0
            n = 0
            src_ip = ['2001:db8:85a3::8a2e:370:7300', '2001:db8:85a3::8a2e:370:7301', '2001:db8:85a3::8a2e:370:7302', '2001:db8:85a3::8a2e:370:7303', '2001:db8:85a3::8a2e:370:7304',
                      '2001:db8:85a3::8a2e:370:7305', '2001:db8:85a3::8a2e:370:7306', '2001:db8:85a3::8a2e:370:7307', '2001:db8:85a3::8a2e:370:7308', '2001:db8:85a3::8a2e:370:7309',
                      '2001:db8:85a3::8a2e:370:730a', '2001:db8:85a3::8a2e:370:730b', '2001:db8:85a3::8a2e:370:730c', '2001:db8:85a3::8a2e:370:730d', '2001:db8:85a3::8a2e:370:730e',
                      '2001:db8:85a3::8a2e:370:730f', '2001:db8:85a3::8a2e:370:7310', '2001:db8:85a3::8a2e:370:7311', '2001:db8:85a3::8a2e:370:7312', '2001:db8:85a3::8a2e:370:7313']
            dst_ip = ['1234:5678:9abc:def0:4422:1133:5577:9904', '1234:5678:9abc:def0:4422:1133:5577:9905', '1234:5678:9abc:def0:4422:1133:5577:9906', '1234:5678:9abc:def0:4422:1133:5577:9907',
			          '1234:5678:9abc:def0:4422:1133:5577:9908', '1234:5678:9abc:def0:4422:1133:5577:9909', '1234:5678:9abc:def0:4422:1133:5577:990a', '1234:5678:9abc:def0:4422:1133:5577:990b',
					  '1234:5678:9abc:def0:4422:1133:5577:990c', '1234:5678:9abc:def0:4422:1133:5577:990d', '1234:5678:9abc:def0:4422:1133:5577:990e', '1234:5678:9abc:def0:4422:1133:5577:990f',
					  '1234:5678:9abc:def0:4422:1133:5577:9910', '1234:5678:9abc:def0:4422:1133:5577:9911', '1234:5678:9abc:def0:4422:1133:5577:9912', '1234:5678:9abc:def0:4422:1133:5577:9913',
					  '1234:5678:9abc:def0:4422:1133:5577:9914', '1234:5678:9abc:def0:4422:1133:5577:9915', '1234:5678:9abc:def0:4422:1133:5577:9916', '1234:5678:9abc:def0:4422:1133:5577:9917']
            mpls = [{'label':200,'tc':0,'ttl':100,'s':1}]
            sys_logging("======send 20 packages to ecmp,every package's inner src ip,inner dst ip,inner src port,inner dst port is not equal======")
            for i in range(0, max_itrs):
                ip_only_pkt = simple_tcpv6_only_packet(
                                        ipv6_src=src_ip[m],
                                        ipv6_dst=dst_ip[n],
                                        ipv6_hlim=64,
                                        tcp_sport=src_port,
                                        tcp_dport=dst_port)
                pkt = simple_mpls_packet(
                                        eth_dst=router_mac,
                                        eth_src='00:11:11:11:11:22',
                                        mpls_type=0x8847,
                                        mpls_tags= mpls,
                                        inner_frame = ip_only_pkt)
                                        
                exp_pkt1 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac1,
                                       eth_src=router_mac,
                                       ipv6_dst=dst_ip[n],
                                       ipv6_src=src_ip[m],
                                       ipv6_hlim=99,
                                       tcp_sport=src_port,
                                       tcp_dport=dst_port)

                exp_pkt2 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac2,
                                       eth_src=router_mac,
                                       ipv6_dst=dst_ip[n],
                                       ipv6_src=src_ip[m],
                                       ipv6_hlim=99,
                                       tcp_sport=src_port,
                                       tcp_dport=dst_port)

                exp_pkt3 = simple_tcpv6_packet(pktlen=114,
                                       eth_dst=dmac3,
                                       eth_src=router_mac,
                                       ipv6_dst=dst_ip[n],
                                       ipv6_src=src_ip[m],
                                       ipv6_hlim=99,
                                       tcp_sport=src_port,
                                       tcp_dport=dst_port)

                self.ctc_send_packet( 3, str(pkt))
                rcv_idx = self.ctc_verify_any_packet_any_port([exp_pkt1,exp_pkt2,exp_pkt3], [0, 1, 2])
                print"*********************** rcv_idx:%d" %rcv_idx
                count[rcv_idx] += 1
                #src_port += 1
                #dst_port += 1
                #m += 1
                n += 1
                
            print"############################count###################################"
            print count
            print"####################################################################"
            for i in range(0, 3):
                self.assertTrue((count[i] >= ((max_itrs / 3) * 0.3)),
                       "Not all paths are equally balanced")

        finally:
            sys_logging("======clean up======")
            mpls1 = sai_thrift_inseg_entry_t(label1)  
            self.client.sai_thrift_remove_inseg_entry(mpls1)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr_subnet, ip_mask, nhop_group1)

            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember1)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember2)
            self.client.sai_thrift_remove_next_hop_group_member(nhop_gmember3)
            
            self.client.sai_thrift_remove_next_hop_group(nhop_group1)

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop2)
            self.client.sai_thrift_remove_next_hop(next_hop3)
            
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_1, ip_addr1, dmac1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_2, ip_addr2, dmac2)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1_3, ip_addr3, dmac3)
            
            self.client.sai_thrift_remove_router_interface(rif_id1_1)
            self.client.sai_thrift_remove_router_interface(rif_id1_2)
            self.client.sai_thrift_remove_router_interface(rif_id1_3)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_router_interface(rif_id3)
            self.client.sai_thrift_remove_virtual_router(vr_id)

            field_list = [SAI_NATIVE_HASH_FIELD_SRC_MAC, SAI_NATIVE_HASH_FIELD_DST_MAC, SAI_NATIVE_HASH_FIELD_IN_PORT, SAI_NATIVE_HASH_FIELD_ETHERTYPE]
            if field_list:
                hash_field_list = sai_thrift_s32_list_t(count=len(field_list), s32list=field_list)
                attr_value = sai_thrift_attribute_value_t(s32list=hash_field_list)
                attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_NATIVE_HASH_FIELD_LIST,
                                                    value=attr_value)
                self.client.sai_thrift_set_hash_attribute(hash_id_ecmp, attr)