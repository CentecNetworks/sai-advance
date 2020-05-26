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
class UDF_GROUP_CreateTest(sai_base_test.ThriftInterfaceDataPlane):
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
        
        print "the str cmp result: %d" %cmp('duet2',testutils.test_params_get()['chipname'])
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 4
            group_length = 4 
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate 1    
            group_length = 1 
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 4    
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
            
class UDF_GROUP_RemoveTest(sai_base_test.ThriftInterfaceDataPlane):
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
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 4
            group_length = 4 
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate 1    
            group_length = 1 
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 4    
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

class UDF_GROUP_GetTest(sai_base_test.ThriftInterfaceDataPlane):
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
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 4
            group_length = 4 
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate 1    
            group_length = 1 
            group_type = SAI_UDF_GROUP_TYPE_GENERIC
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 4    
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

class UDF_MATCH_CreateTest(sai_base_test.ThriftInterfaceDataPlane):
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
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       l3_type, l3_type_mask,
                       gre_type,gre_type_mask,
                       priority)
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate    
            l2_type = 0x1122 
            l2_type_mask = U16MASKFULL
            priority = 2
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       None,None,
                       priority)
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       l3_type, l3_type_mask,
                       gre_type,gre_type_mask,
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
                if 'duet2' == testutils.test_params_get()['chipname']:
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
        finally:
            self.client.sai_thrift_remove_udf_match(udf_match_id)  
 
class UDF_MATCH_RemoveTest(sai_base_test.ThriftInterfaceDataPlane):
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
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       l3_type, l3_type_mask,
                       gre_type,gre_type_mask,
                       priority)
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate    
            l2_type = 0x1122 
            l2_type_mask = U16MASKFULL
            priority = 2
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       None,None,
                       priority)
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       l3_type, l3_type_mask,
                       gre_type,gre_type_mask,
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
                if 'duet2' == testutils.test_params_get()['chipname']:
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

class UDF_MATCH_GetTest(sai_base_test.ThriftInterfaceDataPlane):
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
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
            l2_type = 0x3456 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       l3_type, l3_type_mask,
                       gre_type,gre_type_mask,
                       priority)
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate    
            l2_type = 0x3456 
            l2_type_mask = U16MASKFULL
            priority = 2
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       None,None,
                       priority)
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 
            l2_type = 0x3456 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       l3_type, l3_type_mask,
                       gre_type,gre_type_mask,
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
                if 'duet2' == testutils.test_params_get()['chipname']:
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
        finally:
            self.client.sai_thrift_remove_udf_match(udf_match_id)  

class UDF_CreateTest(sai_base_test.ThriftInterfaceDataPlane):
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
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 4
            group_type = SAI_UDF_GROUP_TYPE_HASH
            group_length = 4 
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate 1 
            group_type = SAI_UDF_GROUP_TYPE_GENERIC         
            group_length = 1 
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 4
            group_type = SAI_UDF_GROUP_TYPE_HASH
            group_length = 4 
            
        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = %lx" %udf_group_id
        
        # setup udf match  zhuan buma                     
        print "Create udf match:"
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       gre_type,gre_type_mask,
                       priority)
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate    
            l2_type = 0x1122 
            l2_type_mask = U16MASKFULL
            #priority = 3
            priority = 0
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       None,None,
                       priority)
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       gre_type,gre_type_mask,
                       priority)
                       
        print "udf_match_id = 0x%lx" %udf_match_id
        
        # setup udf 
        base = SAI_UDF_BASE_L3
        offset = 4 
        # default value
        hash_mask_list = [-1, -1, -1, -1]
        print "Create udf: "
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
            udf_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, hash_mask_list)
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate 
            udf_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, None)
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 
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
                if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
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
            print "udf_match_id = 0x%lx" %udf_match_id            
            self.client.sai_thrift_remove_udf_group(udf_group_id)                          
    
class UDF_RemoveTest(sai_base_test.ThriftInterfaceDataPlane):
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
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 4
            group_length = 4 
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate 1      
            group_length = 1 
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 4
            group_length = 4 
            
        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = 0x%lx" %udf_group_id
        
        # setup udf match  zhuan buma                     
        print "Create udf match:"
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       gre_type,gre_type_mask,
                       priority)
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate    
            l2_type = 0x1122 
            l2_type_mask = U16MASKFULL
            #priority = 3
            priority = 0
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       None,None,
                       priority)
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       gre_type,gre_type_mask,
                       priority)
                       
        print "udf_match_id = 0x%lx" %udf_match_id
        
        # setup udf 
        base = SAI_UDF_BASE_L3
        offset = 4 
        print "Create udf: "
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
  
class UDF_GetTest(sai_base_test.ThriftInterfaceDataPlane):
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
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 4
            group_type = SAI_UDF_GROUP_TYPE_HASH
            group_length = 4 
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate 1 
            group_type = SAI_UDF_GROUP_TYPE_GENERIC         
            group_length = 1 
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 4
            group_type = SAI_UDF_GROUP_TYPE_HASH
            group_length = 4 
            
        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = 0x%lx" %udf_group_id
        
        # setup udf match  zhuan buma                     
        print "Create udf match:"
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       gre_type,gre_type_mask,
                       priority)
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate    
            l2_type = 0x1122 
            l2_type_mask = U16MASKFULL
            #priority = 3
            priority = 0
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       None,None,
                       priority)
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       gre_type,gre_type_mask,
                       priority)
                       
        print "udf_match_id = 0x%lx" %udf_match_id
        
        # setup udf 
        base = SAI_UDF_BASE_L3
        offset = 4 
        hash_mask_list = [-1, -1, -1, -1]
        print "Create udf: "
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
            udf_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, hash_mask_list)
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate 
            udf_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, None)
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 
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
                if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
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
            
class UDF_SetTest(sai_base_test.ThriftInterfaceDataPlane):
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
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 4
            group_type = SAI_UDF_GROUP_TYPE_HASH
            group_length = 4 
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate 1 
            group_type = SAI_UDF_GROUP_TYPE_GENERIC         
            group_length = 1 
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 4
            group_type = SAI_UDF_GROUP_TYPE_HASH
            group_length = 4 
        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = 0x%lx" %udf_group_id
        
        # setup udf match  zhuan buma                     
        print "Create udf match:"
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       gre_type,gre_type_mask,
                       priority)
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate    
            l2_type = 0x1122 
            l2_type_mask = U16MASKFULL
            #priority = 3
            priority = 0
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       None,None,
                       priority)
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 
            l2_type = 0x1122 
            #l2_type = 0x86DD
            l2_type_mask = U16MASKFULL
            l3_type = 57
            l3_type_mask = 0x0F
            gre_type = 0x22eb
            gre_type_mask = U16MASKFULL
            priority = 15
            udf_match_id = sai_thrift_create_udf_match(self.client, 
                       l2_type, l2_type_mask,
                       None, None,
                       gre_type,gre_type_mask,
                       priority)
        print "udf_match_id = 0x%lx" %udf_match_id
        
        # setup udf 
        base = SAI_UDF_BASE_L3
        base_set = SAI_UDF_BASE_L4
        offset = 4 
        hash_mask_list_set = [0, -1, 0, -1]
        hash_mask_list = [-1, -1, -1, -1]
        print "Create udf: "
        if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
            udf_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, hash_mask_list)
        elif 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate 
            udf_id =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset, None)
        elif 'tsingma' == testutils.test_params_get()['chipname']:    # tsingma 
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
                if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
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
            assert (status == SAI_STATUS_NOT_SUPPORTED)
            if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
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
                if 'duet2' == testutils.test_params_get()['chipname']:    # dt2 
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
            
@group('lag')
class UDF_HashL2LagTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)
        
        if 'goldengate' == testutils.test_params_get()['chipname']:    # goldengate 
            print "Goldengate not UDF_HashL2LagTest, just pass for case"
            return
            
        #setup udf group
        group_type = SAI_UDF_GROUP_TYPE_HASH
        group_length = 4 
        print "Create udf group: udf_group_type = SAI_UDF_GROUP_ATTR_TYPE, group_length = SAI_UDF_GROUP_ATTR_LENGTH "
        udf_group_id = sai_thrift_create_udf_group(self.client, group_type, group_length)
        print "udf_group_id = 0x%lx" %udf_group_id
        
        # setup udf match  zhuan buma
        l2_type = 0x0800 
        l2_type_mask = U16MASKFULL
        priority = 15
        print "Create udf match:"
        udf_match_id = sai_thrift_create_udf_match(self.client, 
                               l2_type, l2_type_mask,
                               None, None,
                               None, None,
                               priority)
        print "udf_match_id = 0x%lx" %udf_match_id
        
        # setup udf 
        base = SAI_UDF_BASE_L2
        offset1 = 16
        # default value
        hash_mask_list1 = [-1, -1, 0, 0]
        print "Create udf: "
        udf_id1 =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset1, hash_mask_list1)
        print "udf_id1 = 0x%lx" %udf_id1
        
        base = SAI_UDF_BASE_L2
        offset2 = 8 
        # default value
        hash_mask_list2 = [-1, 0, 0, 0]
        print "Create udf: "
        udf_id2 =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset2, hash_mask_list2)
        print "udf_id2 = 0x%lx" %udf_id2
        
        base = SAI_UDF_BASE_L2
        offset3 = 24 
        # default value
        hash_mask_list3 = [-1, -1, -1, -1]
        print "Create udf: "
        udf_id3 =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset3, hash_mask_list3)
        print "udf_id3 = 0x%lx" %udf_id3
        
        base = SAI_UDF_BASE_L2
        offset4 = 20
        # default value
        hash_mask_list4 = [-1, -1, -1, 0]
        print "Create udf: "
        udf_id4 =  sai_thrift_create_udf(self.client, udf_match_id, udf_group_id, base, offset4, hash_mask_list4)
        print "udf_id4 = 0x%lx" %udf_id4
        
        vlan_id = 10
        hash_id_lag = 0x201C
        hash_id_ecmp = 0x1C
        udf_group_list = [udf_group_id]
        port1 = port_list[0]
        port2 = port_list[1]
        port3 = port_list[2]
        port4 = port_list[3]
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        
        lag_id1 = sai_thrift_create_lag(self.client, [])
        print"lag:%lx" %lag_id1
        
        """sai_thrift_vlan_remove_all_ports(self.client, switch.default_vlan.oid)"""
        print "port:%lx" %port1
        print "lag_id1:%lx" %lag_id1
        lag_member_id1 = sai_thrift_create_lag_member(self.client, lag_id1, port1)
        lag_member_id2 = sai_thrift_create_lag_member(self.client, lag_id1, port2)
        lag_member_id3 = sai_thrift_create_lag_member(self.client, lag_id1, port3)
        
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, lag_id1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port4, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_LAG_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_lag_attribute(lag_id1, attr)
        
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port4, attr)
        
        sai_thrift_create_fdb(self.client, vlan_oid, mac1, lag_id1, mac_action)
        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port4, mac_action)
        
        #UDF Group list   
        if udf_group_list:
            hash_udf_group_list = sai_thrift_object_list_t(count=len(udf_group_list), object_id_list=udf_group_list)
            attr_value = sai_thrift_attribute_value_t(objlist=hash_udf_group_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_UDF_GROUP_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)
        
        warmboot(self.client)
        try:
            # get hash attribute
            print "Get Hash attribute: SAI_HASH_ATTR_UDF_GROUP_LIST = udf_group_id"
            attrs = self.client.sai_thrift_get_hash_attribute(hash_id_lag)
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            udf_group_list_temp = [None]*len(udf_group_list)
            for a in attrs.attr_list:
                if a.id == SAI_HASH_ATTR_UDF_GROUP_LIST:
                    print "udf_group_list cnt = %d" %a.value.objlist.count
                    if a.value.objlist.count != len(udf_group_list):
                        print "get udf group list error!!! count: %d" % a.value.objlist.count
                        raise NotImplementedError()
                    for i in range(a.value.objlist.count):
                        udf_group_list_temp[i] = a.value.objlist.object_id_list[i]
                    print "**************************************get udf_group_list_temp[0]: 0x%lx ",udf_group_list_temp[0]
                    print "**************************************get udf_group_list: 0x%lx ",udf_group_list_temp
                    if udf_group_list_temp != udf_group_list:
                        print "get udf group list error!!!"
                        raise NotImplementedError()
            
            # get udf_id1 attribute
            print "Get udf_id1 attribute: "
            attrs = self.client.sai_thrift_get_udf_attribute(udf_id1)
            print "udf_id1 = %lx" %udf_id1
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            hash_mask_list_temp = [None]*len(hash_mask_list1)
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
                    print "set offset1 = %d" %offset1
                    print "get offset1 = %d" %a.value.u16
                    if offset1 != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_HASH_MASK: 
                    if a.value.u8list.count != len(hash_mask_list1):
                        print "get hash mask list1 error!!! count: %d" % a.value.u8list.count
                        raise NotImplementedError()
                    for i in range(a.value.u8list.count):
                        hash_mask_list_temp[i] = a.value.u8list.u8list[i]
                    print "get hash_mask_list1:  ",hash_mask_list_temp
                    if hash_mask_list_temp != hash_mask_list1:
                        print "get hash mask list1 error!!!"
                        raise NotImplementedError()
                        
            # get udf_id2 attribute
            print "Get udf_id2 attribute: "
            attrs = self.client.sai_thrift_get_udf_attribute(udf_id2)
            print "udf_id2 = %lx" %udf_id2
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            hash_mask_list_temp = [None]*len(hash_mask_list2)
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
                    print "set offset2 = %d" %offset2
                    print "get offset2 = %d" %a.value.u16
                    if offset2 != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_HASH_MASK: 
                    if a.value.u8list.count != len(hash_mask_list2):
                        print "get hash mask list2 error!!! count: %d" % a.value.u8list.count
                        raise NotImplementedError()
                    for i in range(a.value.u8list.count):
                        hash_mask_list_temp[i] = a.value.u8list.u8list[i]
                    print "get hash_mask_list2:  ",hash_mask_list_temp
                    if hash_mask_list_temp != hash_mask_list2:
                        print "get hash mask list2 error!!!"
                        raise NotImplementedError()
                        
            # get udf_id3 attribute
            print "Get udf_id3 attribute: "
            attrs = self.client.sai_thrift_get_udf_attribute(udf_id3)
            print "udf_id3 = %lx" %udf_id3
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            hash_mask_list_temp = [None]*len(hash_mask_list3)
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
                    print "set offset3 = %d" %offset3
                    print "get offset3 = %d" %a.value.u16
                    if offset3 != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_HASH_MASK: 
                    if a.value.u8list.count != len(hash_mask_list3):
                        print "get hash mask list3 error!!! count: %d" % a.value.u8list.count
                        raise NotImplementedError()
                    for i in range(a.value.u8list.count):
                        hash_mask_list_temp[i] = a.value.u8list.u8list[i]
                    print "get hash_mask_list3:  ",hash_mask_list_temp
                    if hash_mask_list_temp != hash_mask_list3:
                        print "get hash mask list3 error!!!"
                        raise NotImplementedError()
                        
            # get udf_id4 attribute
            print "Get udf_id4 attribute: "
            attrs = self.client.sai_thrift_get_udf_attribute(udf_id4)
            print "udf_id4 = %lx" %udf_id4
            print "status = %d" %attrs.status
            assert (attrs.status == SAI_STATUS_SUCCESS)
            hash_mask_list_temp = [None]*len(hash_mask_list4)
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
                    print "set offset4 = %d" %offset4
                    print "get offset4 = %d" %a.value.u16
                    if offset4 != a.value.u16:
                        raise NotImplementedError()
                if a.id == SAI_UDF_ATTR_HASH_MASK: 
                    if a.value.u8list.count != len(hash_mask_list4):
                        print "get hash mask list4 error!!! count: %d" % a.value.u8list.count
                        raise NotImplementedError()
                    for i in range(a.value.u8list.count):
                        hash_mask_list_temp[i] = a.value.u8list.u8list[i]
                    print "get hash_mask_list4:  ",hash_mask_list_temp
                    if hash_mask_list_temp != hash_mask_list4:
                        print "get hash mask list4 error!!!"
                        raise NotImplementedError()
            
            # get udf match attribute            
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
                if a.id == SAI_UDF_MATCH_ATTR_PRIORITY: 
                    print "set priority = %d" %priority
                    print "get priority = %d" %a.value.u8
                    if priority != a.value.u8:
                        raise NotImplementedError()
            
            # get udf group attribute             
            print "Get udf group attribute: udf_group_type = SAI_UDF_GROUP_TYPE_HASH, group_length = 4"
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
            
            #(gdb) p/x p_udf_group->hash_udf_bmp
            #$24 = 0xf731
            dump_status = self.client.sai_thrift_dump_log("UDF_HashL2LagTest.txt")
            print "dump_status = %d" %dump_status
            assert (dump_status == SAI_STATUS_SUCCESS)
            
        finally:
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, lag_id1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port4)
        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
        
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
            
            udf_group_list = []
        #if udf_group_list:
            hash_udf_group_list = sai_thrift_object_list_t(count=len(udf_group_list), object_id_list=udf_group_list)
            attr_value = sai_thrift_attribute_value_t(objlist=hash_udf_group_list)
            attr = sai_thrift_attribute_t(id=SAI_HASH_ATTR_UDF_GROUP_LIST,
                                                value=attr_value)
            self.client.sai_thrift_set_hash_attribute(hash_id_lag, attr)   
            
            self.client.sai_thrift_remove_udf(udf_id1)
            self.client.sai_thrift_remove_udf(udf_id2)
            self.client.sai_thrift_remove_udf(udf_id3)
            self.client.sai_thrift_remove_udf(udf_id4)
            self.client.sai_thrift_remove_udf_match(udf_match_id)  
            self.client.sai_thrift_remove_udf_group(udf_group_id) 

         
