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
Thrift SAI interface ptp tests
"""
import socket
from switch import *
import sai_base_test
from ptf.mask import Mask
import pdb

@group('ptp')

class func_01_create_one_ptp_domain_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        sys_logging("###the ptp_oid %x ###" %ptp_oid)
        first_ptp_domain_id = 0x10000005d        

        try:
            assert(first_ptp_domain_id == ptp_oid)
            
        finally:
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)


class func_02_create_two_ptp_domain_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type1 = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type1 = SAI_PTP_DEVICE_OC
        enable_type2= SAI_PTP_ENABLE_BASED_ON_PORT
        device_type2= SAI_PTP_DEVICE_BC
               
        ptp_oid1 = sai_thrift_create_ptp(self.client, enable_type1, device_type1)
        sys_logging("###the ptp_oid1 %x ###" %ptp_oid1)
        
        ptp_oid2 = sai_thrift_create_ptp(self.client, enable_type2, device_type2)
        sys_logging("###the ptp_oid2 %x ###" %ptp_oid2)
        
        first_ptp_domain_id = 0x10000005d 
        second_ptp_domain_id = SAI_NULL_OBJECT_ID

        try:
            assert(first_ptp_domain_id == ptp_oid1)
            assert(second_ptp_domain_id == ptp_oid2)
            
        finally:
            self.client.sai_thrift_remove_ptp_domain(ptp_oid1)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid2)
            
class func_03_create_two_ptp_domain_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type1 = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type1 = SAI_PTP_DEVICE_OC

               
        ptp_oid1 = sai_thrift_create_ptp(self.client, enable_type1, device_type1)
        sys_logging("###the ptp_oid1 %x ###" %ptp_oid1)
        first_ptp_domain_id = 0x10000005d 
        assert(first_ptp_domain_id == ptp_oid1)
        
        try:
            self.client.sai_thrift_remove_ptp_domain(ptp_oid1)
        
            enable_type2= SAI_PTP_ENABLE_BASED_ON_PORT
            device_type2= SAI_PTP_DEVICE_BC
            
            ptp_oid2 = sai_thrift_create_ptp(self.client, enable_type2, device_type2)
            sys_logging("###the ptp_oid2 %x ###" %ptp_oid2)
            second_ptp_domain_id = 0x10000005d

            assert(second_ptp_domain_id == ptp_oid2)
            
        finally:
             self.client.sai_thrift_remove_ptp_domain(ptp_oid2)
            
class func_04_create_ptp_domain_fn_with_all_attribute(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        is_negative = 0
        #adjust drift
        type = 1
        clockoffset = 50
        tod_foramt = SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375
        tod_leap_second = 15
        tod_pps_status = 0
        tod_pps_accuracy = 0x10
        tod_mode = SAI_PTP_TOD_INTERFACE_INPUT
        tod_enable = True
        
        ptp_oid = sai_thrift_create_ptp(self.client, 
        enable_type, 
        device_type, 
        is_negative, 
        type, 
        clockoffset, 
        tod_foramt,         
        tod_leap_second, 
        tod_pps_status, 
        tod_pps_accuracy,
        tod_mode, 
        tod_enable
        )
        
        sys_logging("###the ptp_oid %x ###" %ptp_oid)
        first_ptp_domain_id = 0x10000005d 

        try:
            assert(first_ptp_domain_id == ptp_oid) 
            
        finally:
             self.client.sai_thrift_remove_ptp_domain(ptp_oid)
             
class func_05_create_ptp_domain_fn_with_all_attribute_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_VLAN
        device_type = SAI_PTP_DEVICE_E2E_TC
        is_negative = 0
        #adjust time
        type = 0
        clockoffset = 10
        tod_foramt = SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375
        tod_leap_second = 15
        tod_pps_status = 0
        tod_pps_accuracy = 0x10
        tod_mode = SAI_PTP_TOD_INTERFACE_OUTPUT
        tod_enable = True
        
        ptp_oid = sai_thrift_create_ptp(self.client, 
        enable_type, 
        device_type, 
        is_negative, 
        type, 
        clockoffset, 
        tod_foramt,         
        tod_leap_second, 
        tod_pps_status, 
        tod_pps_accuracy,
        tod_mode, 
        tod_enable
        )
        
        sys_logging("###the ptp_oid %x ###" %ptp_oid)
        first_ptp_domain_id = 0x10000005d 
        pdb.set_trace()
        try:
            assert(first_ptp_domain_id == ptp_oid) 
            
        finally:
             self.client.sai_thrift_remove_ptp_domain(ptp_oid)