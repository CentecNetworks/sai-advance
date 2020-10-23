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
            sys_logging("======clean up======")
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
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ptp_domain(ptp_oid1)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid2)
            
class func_03_create_4_device_type_ptp_domain_fn(sai_base_test.ThriftInterfaceDataPlane):
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

            self.client.sai_thrift_remove_ptp_domain(ptp_oid1)
            enable_type2= SAI_PTP_ENABLE_BASED_ON_PORT
            device_type2= SAI_PTP_DEVICE_E2E_TC
            ptp_oid2 = sai_thrift_create_ptp(self.client, enable_type2, device_type2)
            sys_logging("###the ptp_oid2 %x ###" %ptp_oid2)
            second_ptp_domain_id = 0x10000005d
            assert(second_ptp_domain_id == ptp_oid2)

            self.client.sai_thrift_remove_ptp_domain(ptp_oid1)
            enable_type2= SAI_PTP_ENABLE_BASED_ON_PORT
            device_type2= SAI_PTP_DEVICE_P2P_TC
            ptp_oid2 = sai_thrift_create_ptp(self.client, enable_type2, device_type2)
            sys_logging("###the ptp_oid2 %x ###" %ptp_oid2)
            second_ptp_domain_id = 0x10000005d
            assert(second_ptp_domain_id == ptp_oid2)
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ptp_domain(ptp_oid2)
            
class func_04_create_ptp_domain_fn_with_input_tod_interface(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        drift_is_negative = 0
        time_is_negative = 0
        
        driftoffset = 50
        timeoffset = 30
        tod_foramt = SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375
        tod_leap_second = 0
        tod_pps_status = 0
        tod_pps_accuracy = 0
        tod_mode = SAI_PTP_TOD_INTERFACE_INPUT
        tod_enable = True
        
        ptp_oid = sai_thrift_create_ptp(self.client, 
        enable_type, 
        device_type, 
        drift_is_negative,
        time_is_negative,
        driftoffset,
        timeoffset,
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
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = 1, value = 30))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class func_05_create_ptp_domain_fn_with_output_tod_interface(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_VLAN
        device_type = SAI_PTP_DEVICE_E2E_TC
        drift_is_negative = 0
        time_is_negative = 0
        driftoffset = 10
        timeoffset =70
        tod_foramt = SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375
        tod_leap_second = 15
        tod_pps_status = 0
        tod_pps_accuracy = 0x10
        tod_mode = SAI_PTP_TOD_INTERFACE_OUTPUT
        tod_enable = True
        
        ptp_oid = sai_thrift_create_ptp(self.client, 
        enable_type, 
        device_type, 
        drift_is_negative,
        time_is_negative, 
        driftoffset, 
        timeoffset,
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
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = 1, value = 70))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class func_06_remove_ptp_domain_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        sys_logging("###the ptp_oid %x ###" %ptp_oid)
        attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
        sys_logging("get ptp attribute status = %d" %attrs.status)
        assert (attrs.status == SAI_STATUS_SUCCESS)
         
        try:
            status = self.client.sai_thrift_remove_ptp_domain(ptp_oid) 
            sys_logging("remove ptp status = %d" %status)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            sys_logging("get ptp attribute status = %d" %attrs.status)
            assert (attrs.status == SAI_STATUS_ITEM_NOT_FOUND)
         
            
        finally:
            sys_logging("======clean up======") 
            
class func_07_remove_no_exist_ptp_domain_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        sys_logging("###the ptp_oid %x ###" %ptp_oid)
        self.client.sai_thrift_remove_ptp_domain(ptp_oid) 
         
        try:
            status = self.client.sai_thrift_remove_ptp_domain(ptp_oid) 
            sys_logging("remove ptp status = %d" %status)
            assert (status == SAI_STATUS_ITEM_NOT_FOUND)
         
            
        finally:
            sys_logging("======clean up======")


class func_08_get_basic_ptp_domain_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        sys_logging("###the ptp_oid %x ###" %ptp_oid)
        first_ptp_domain_id = 0x10000005d        

        try:
            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE:
                    sys_logging("get ptp based type = %d" %a.value.s32)
                    if enable_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE:
                    sys_logging("get ptp device type = %d" %a.value.s32)
                    if device_type != a.value.s32:
                        raise NotImplementedError()
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class func_09_get_basic_ptp_domain_attr_fn_2(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_VLAN
        device_type = SAI_PTP_DEVICE_BC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        sys_logging("###the ptp_oid %x ###" %ptp_oid)
        first_ptp_domain_id = 0x10000005d        

        try:
            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE:
                    sys_logging("get ptp based type = %d" %a.value.s32)
                    if enable_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE:
                    sys_logging("get ptp device type = %d" %a.value.s32)
                    if device_type != a.value.s32:
                        raise NotImplementedError()
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class func_10_get_output_tod_interface_ptp_domain_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        drift_is_negative = 0
        time_is_negative = 0
        driftoffset = 10
        timeoffset =50
        tod_foramt = SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375
        tod_leap_second = 15
        tod_pps_status = 0
        tod_pps_accuracy = 0x10
        tod_mode = SAI_PTP_TOD_INTERFACE_OUTPUT
        tod_enable = True
        
        ptp_oid = sai_thrift_create_ptp(self.client, 
        enable_type, 
        device_type, 
        drift_is_negative,
        time_is_negative, 
        driftoffset,
        timeoffset, 
        tod_foramt,         
        tod_leap_second, 
        tod_pps_status, 
        tod_pps_accuracy,
        tod_mode, 
        tod_enable
        )
        
        sys_logging("###the ptp_oid 0X%x ###" %ptp_oid)


        try:
            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE:
                    sys_logging("get ptp based type = %d" %a.value.s32)
                    if enable_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE:
                    sys_logging("get ptp device type = %d" %a.value.s32)
                    if device_type != a.value.s32:
                        raise NotImplementedError() 
                if a.id == SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET:
                    sys_logging(a.value.timeoffset)
                    if drift_is_negative != a.value.timeoffset.flag:
                        raise NotImplementedError()
                    if driftoffset != a.value.timeoffset.value:
                        raise NotImplementedError() 
                if a.id == SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET:
                    sys_logging(a.value.timeoffset)
                    if time_is_negative != a.value.timeoffset.flag:
                        raise NotImplementedError()
                    if timeoffset != a.value.timeoffset.value:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_FORMAT_TYPE:
                    sys_logging("get ptp tod format type = %d" %a.value.s32)
                    if tod_foramt != a.value.s32:
                        raise NotImplementedError() 
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE:
                    sys_logging("get ptp tod interface mode = %d" %a.value.s32)
                    if tod_mode != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE:
                    sys_logging("get ptp tod interface enable status = %d" %a.value.booldata)
                    if tod_enable != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND:
                    sys_logging("get ptp tod interface leap second = %d" %a.value.s8)
                    if tod_leap_second != a.value.s8:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS:
                    sys_logging("get ptp tod interface pps status = %d" %a.value.u8)
                    if tod_pps_status != a.value.u8:
                        raise NotImplementedError() 
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY:
                    sys_logging("get ptp tod interface pps accuracy = %d" %a.value.u8)
                    if tod_pps_accuracy != a.value.u8:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_TAI_TIMESTAMP:
                    sys_logging(a.value.timespec)
                if a.id == SAI_PTP_DOMAIN_ATTR_CAPTURED_TIMESTAMP:
                    sys_logging(a.value.captured_timespec)

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = 1, value = 50))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class func_11_get_input_tod_interface_ptp_domain_attr_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        drift_is_negative = 0
        time_is_negative = 0
        driftoffset = 10
        timeoffset =50
        tod_foramt = SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375
        tod_leap_second = 15
        tod_pps_status = 0
        tod_pps_accuracy = 0x10
        tod_mode = SAI_PTP_TOD_INTERFACE_OUTPUT
        tod_enable = True
        
        ptp_oid = sai_thrift_create_ptp(self.client, 
        enable_type, 
        device_type, 
        drift_is_negative,
        time_is_negative, 
        driftoffset,
        timeoffset, 
        tod_foramt,         
        tod_leap_second, 
        tod_pps_status, 
        tod_pps_accuracy,
        tod_mode, 
        tod_enable
        )
        
        sys_logging("###the ptp_oid 0X%x ###" %ptp_oid)

        try:
            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_PTP_DOMAIN_ATTR_PTP_ENABLE_BASED_TYPE:
                    sys_logging("get ptp based type = %d" %a.value.s32)
                    if enable_type != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_DEVICE_TYPE:
                    sys_logging("get ptp device type = %d" %a.value.s32)
                    if device_type != a.value.s32:
                        raise NotImplementedError() 
                if a.id == SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET:
                    sys_logging(a.value.timeoffset)
                    if drift_is_negative != a.value.timeoffset.flag:
                        raise NotImplementedError()
                    if driftoffset != a.value.timeoffset.value:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET:
                    sys_logging(a.value.timeoffset)
                    if time_is_negative != a.value.timeoffset.flag:
                        raise NotImplementedError()
                    if timeoffset != a.value.timeoffset.value:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_FORMAT_TYPE:
                    sys_logging("get ptp tod format type = %d" %a.value.s32)
                    if tod_foramt != a.value.s32:
                        raise NotImplementedError() 
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE:
                    sys_logging("get ptp tod interface mode = %d" %a.value.s32)
                    if tod_mode != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE:
                    sys_logging("get ptp tod interface enable status = %d" %a.value.booldata)
                    if tod_enable != a.value.booldata:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND:
                    sys_logging("get ptp tod interface leap second = %d" %a.value.s8)
                    if tod_leap_second != a.value.s8:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS:
                    sys_logging("get ptp tod interface pps status = %d" %a.value.u8)
                    if tod_pps_status != a.value.u8:
                        raise NotImplementedError() 
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY:
                    sys_logging("get ptp tod interface pps accuracy = %d" %a.value.u8)
                    if tod_pps_accuracy != a.value.u8:
                        raise NotImplementedError()
                if a.id == SAI_PTP_DOMAIN_ATTR_TAI_TIMESTAMP:
                    sys_logging(a.value.timespec)
                if a.id == SAI_PTP_DOMAIN_ATTR_CAPTURED_TIMESTAMP:
                    sys_logging(a.value.captured_timespec)

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = 1, value = 50))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class func_12_set_ptp_domain_attr_time_offset_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        is_negative = 0
        #adjust drift
        type = 1
        timeoffset = 50
        timeoffset2 = 20
        is_negative2 = 1
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        sys_logging("###the ptp_oid %x ###" %ptp_oid)
        first_ptp_domain_id = 0x10000005d        

        try:
            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET:
                    sys_logging(a.value.timeoffset)
                    if 0 != a.value.timeoffset.flag:
                        raise NotImplementedError()
                    if 0 != a.value.timeoffset.value:
                        raise NotImplementedError()
                        
            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = is_negative, value = timeoffset))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)

            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET:
                    sys_logging(a.value.timeoffset)
                    if is_negative != a.value.timeoffset.flag:
                        raise NotImplementedError()
                    if timeoffset != a.value.timeoffset.value:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = is_negative2, value = timeoffset2))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)

            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET:
                    sys_logging(a.value.timeoffset)
                    if is_negative2 != a.value.timeoffset.flag:
                        raise NotImplementedError()
                    if (timeoffset2) != a.value.timeoffset.value:
                        raise NotImplementedError()
            
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = 1, value = 30))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)            

class func_13_set_ptp_domain_attr_drift_offset_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        is_negative = 0
        #adjust drift
        type = 1
        driftoffset = 100
        driftoffset2 = 30
        is_negative2 = 1
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        sys_logging("###the ptp_oid %x ###" %ptp_oid)
        first_ptp_domain_id = 0x10000005d        

        try:
            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET:
                    sys_logging(a.value.timeoffset)
                    if 0 != a.value.timeoffset.flag:
                        raise NotImplementedError()
                    if 0 != a.value.timeoffset.value:
                        raise NotImplementedError()
                        
            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = is_negative, value = driftoffset))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)

            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET:
                    sys_logging(a.value.timeoffset)
                    if is_negative != a.value.timeoffset.flag:
                        raise NotImplementedError()
                    if driftoffset != a.value.timeoffset.value:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = is_negative2, value = driftoffset2))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)

            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_DRIFT_OFFSET:
                    sys_logging(a.value.timeoffset)
                    if is_negative2 != a.value.timeoffset.flag:
                        raise NotImplementedError()
                    if (driftoffset2) != a.value.timeoffset.value:
                        raise NotImplementedError()
            
        finally:
            sys_logging("======clean up======")
            self.client.sai_thrift_remove_ptp_domain(ptp_oid) 


class func_14_set_ptp_domain_attr_tod_intf_enable_and_mode_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        drift_is_negative = 0
        time_is_negative = 0
        driftoffset = 10
        timeoffset =50
        tod_foramt = SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375
        tod_leap_second = 15
        tod_pps_status = 0
        tod_pps_accuracy = 0x10
        tod_mode = SAI_PTP_TOD_INTERFACE_OUTPUT
        tod_enable = True
        
        ptp_oid = sai_thrift_create_ptp(self.client, 
        enable_type, 
        device_type, 
        drift_is_negative,
        time_is_negative, 
        driftoffset,
        timeoffset, 
        tod_foramt,         
        tod_leap_second, 
        tod_pps_status, 
        tod_pps_accuracy,
        tod_mode, 
        tod_enable
        )
        
        sys_logging("###the ptp_oid 0X%x ###" %ptp_oid)
        attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list: 
            if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE:
                sys_logging("get ptp tod interface mode = %d" %a.value.s32)
            if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE:
                sys_logging("get ptp tod interface enable status = %d" %a.value.booldata)
                
        tod_mode = SAI_PTP_TOD_INTERFACE_INPUT
        tod_enable = False
        try:      

            attr_value = sai_thrift_attribute_value_t(booldata=tod_enable)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(s32=tod_mode)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list: 
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE:
                    sys_logging("get ptp tod interface mode = %d" %a.value.s32)
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE:
                    sys_logging("get ptp tod interface enable status = %d" %a.value.booldata)
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = 1, value = 50))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class func_15_set_ptp_domain_attr_tod_intf_leap_second_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        drift_is_negative = 0
        time_is_negative = 0
        driftoffset = 10
        timeoffset =50
        tod_foramt = SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375
        tod_leap_second = 15
        tod_pps_status = 0
        tod_pps_accuracy = 0x10
        tod_mode = SAI_PTP_TOD_INTERFACE_OUTPUT
        tod_enable = True
        
        ptp_oid = sai_thrift_create_ptp(self.client, 
        enable_type, 
        device_type, 
        drift_is_negative,
        time_is_negative, 
        driftoffset,
        timeoffset, 
        tod_foramt,         
        tod_leap_second, 
        tod_pps_status, 
        tod_pps_accuracy,
        tod_mode, 
        tod_enable
        )
        
        sys_logging("###the ptp_oid 0X%x ###" %ptp_oid)
        attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list: 
            if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND:
                sys_logging("get ptp tod interface leap second = %d" %a.value.s8)


        tod_mode = SAI_PTP_TOD_INTERFACE_DISABLE
        tod_enable = False        
        tod_leap_second = 20
        tod_pps_status = 1
        tod_pps_accuracy = 0x20
        try:
            attr_value = sai_thrift_attribute_value_t(s8=tod_leap_second)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)
            assert (statu == SAI_STATUS_FAILURE)


            attr_value = sai_thrift_attribute_value_t(booldata=tod_enable)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)
            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(s32=tod_mode)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)



            attr_value = sai_thrift_attribute_value_t(s8=tod_leap_second)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)


            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list: 
                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_LEAP_SECOND:
                    sys_logging("get ptp tod interface leap second = %d" %a.value.s8)

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = 1, value = 50))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class func_16_set_ptp_domain_attr_tod_intf_pps_status_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        drift_is_negative = 0
        time_is_negative = 0
        driftoffset = 10
        timeoffset =50
        tod_foramt = SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375
        tod_leap_second = 15
        tod_pps_status = 0
        tod_pps_accuracy = 0x10
        tod_mode = SAI_PTP_TOD_INTERFACE_OUTPUT
        tod_enable = True
        
        ptp_oid = sai_thrift_create_ptp(self.client, 
        enable_type, 
        device_type, 
        drift_is_negative,
        time_is_negative, 
        driftoffset,
        timeoffset, 
        tod_foramt,         
        tod_leap_second, 
        tod_pps_status, 
        tod_pps_accuracy,
        tod_mode, 
        tod_enable
        )
        
        sys_logging("###the ptp_oid 0X%x ###" %ptp_oid)
        attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list: 

            if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS:
                sys_logging("get ptp tod interface pps status = %d" %a.value.u8)

        tod_mode = SAI_PTP_TOD_INTERFACE_DISABLE
        tod_enable = False        
        tod_leap_second = 20
        tod_pps_status = 1
        tod_pps_accuracy = 0x20
        try:

            attr_value = sai_thrift_attribute_value_t(u8=tod_pps_status)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)
            assert (statu == SAI_STATUS_FAILURE)  


            attr_value = sai_thrift_attribute_value_t(booldata=tod_enable)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)
            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(s32=tod_mode)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)



            attr_value = sai_thrift_attribute_value_t(u8=tod_pps_status)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list: 

                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_STATUS:
                    sys_logging("get ptp tod interface pps status = %d" %a.value.u8)

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = 1, value = 50))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class func_17_set_ptp_domain_attr_tod_intf_pps_accuracy_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        print ''

        switch_init(self.client)

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        drift_is_negative = 0
        time_is_negative = 0
        driftoffset = 10
        timeoffset =50
        tod_foramt = SAI_PTP_TOD_INTERFACE_FORMAT_CCSA_YDT2375
        tod_leap_second = 15
        tod_pps_status = 0
        tod_pps_accuracy = 0x10
        tod_mode = SAI_PTP_TOD_INTERFACE_OUTPUT
        tod_enable = True
        
        ptp_oid = sai_thrift_create_ptp(self.client, 
        enable_type, 
        device_type, 
        drift_is_negative,
        time_is_negative, 
        driftoffset,
        timeoffset, 
        tod_foramt,         
        tod_leap_second, 
        tod_pps_status, 
        tod_pps_accuracy,
        tod_mode, 
        tod_enable
        )
        
        sys_logging("###the ptp_oid 0X%x ###" %ptp_oid)
        attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
        assert (attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list: 

            if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY:
                sys_logging("get ptp tod interface pps accuracy = %d" %a.value.u8)

        tod_mode = SAI_PTP_TOD_INTERFACE_DISABLE
        tod_enable = False        
        tod_leap_second = 20
        tod_pps_status = 1
        tod_pps_accuracy = 0x20
        try:

            attr_value = sai_thrift_attribute_value_t(u8=tod_pps_accuracy)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)
            assert (statu == SAI_STATUS_FAILURE)            



            attr_value = sai_thrift_attribute_value_t(booldata=tod_enable)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_ENABLE, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)
            #pdb.set_trace()
            attr_value = sai_thrift_attribute_value_t(s32=tod_mode)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_MODE, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)




            attr_value = sai_thrift_attribute_value_t(u8=tod_pps_accuracy)
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY, value=attr_value)
            statu = self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            sys_logging("set ptp domain attribute statu = %d"%statu)
            assert (statu == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_ptp_domain_attribute(ptp_oid)
            assert (attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list: 

                if a.id == SAI_PTP_DOMAIN_ATTR_TOD_INTF_PPS_ACCURACY:
                    sys_logging("get ptp tod interface pps accuracy = %d" %a.value.u8)

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(timeoffset=sai_thrift_timeoffset_t(flag = 1, value = 50))
            attr = sai_thrift_attribute_t(id=SAI_PTP_DOMAIN_ATTR_ADJUEST_CLOCK_TIME_OFFSET,value=attr_value)
            self.client.sai_thrift_set_ptp_domain_attribute(ptp_oid, attr)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class scenario_01_oc_device_rx_pkt_to_cpu_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        sys_logging("###the ptp_oid 0X%x ###" %ptp_oid)
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #pdb.set_trace()
        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        
        #sync
        ptppkt = simple_ptp_packet(msgType=0,
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00030005,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        
        warmboot(self.client)
        try:
            #self.ctc_send_packet(0, str(pkt))
            #self.ctc_verify_packets( str(pkt), [1])

            self.client.sai_thrift_clear_cpu_packet_info()              
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 0:
                raise NotImplementedError() 
                                        
            self.ctc_send_packet(0, str(pkt))
            time.sleep(1)

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_cpu_packet_attribute()

            for a in attrs.attr_list:

                if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT = 0x%x" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID = 0x%x" %a.value.oid)
                    if default_1q_bridge != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID = 0x%x" %a.value.oid)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()

                if a.id == SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL = 0x%x" %a.value.u64)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()
                
                if a.id == SAI_HOSTIF_PACKET_ATTR_TIMESTAMP:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_TIMESTAMP = 0x%x" %a.value.timespec.tv_sec)
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_TIMESTAMP = 0x%x" %a.value.timespec.tv_nsec)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()
                    
            self.client.sai_thrift_clear_cpu_packet_info()
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)
        
class scenario_02_bc_device_rx_pkt_to_cpu_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_BC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        

        #delay_req
        ptppkt = simple_ptp_packet(msgType=1, #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00030005,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=None,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=15,
                                   tsNs=31,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        
        warmboot(self.client)
        try:
            #self.ctc_send_packet(0, str(pkt))
            #self.ctc_verify_packets( str(pkt), [1])
            
            self.client.sai_thrift_clear_cpu_packet_info()              
            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 0:
                raise NotImplementedError() 
                                        
            self.ctc_send_packet(0, str(pkt))
            time.sleep(1)

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_cpu_packet_attribute()

            for a in attrs.attr_list:

                if a.id == SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_INGRESS_PORT = 0x%x" %a.value.oid)
                    if port1 != a.value.oid:
                        raise NotImplementedError()
                        
                if a.id == SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_BRIDGE_ID = 0x%x" %a.value.oid)
                    if default_1q_bridge != a.value.oid:
                        raise NotImplementedError()

                if a.id == SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_HOSTIF_TRAP_ID = 0x%x" %a.value.oid)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()

                if a.id == SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_Y1731_RXFCL = 0x%x" %a.value.u64)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()
                
                if a.id == SAI_HOSTIF_PACKET_ATTR_TIMESTAMP:
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_TIMESTAMP = 0x%x" %a.value.timespec.tv_sec)
                    sys_logging("get SAI_HOSTIF_PACKET_ATTR_TIMESTAMP = 0x%x" %a.value.timespec.tv_nsec)
                    #if port1 != a.value.oid:
                    #    raise NotImplementedError()
                    
            self.client.sai_thrift_clear_cpu_packet_info()

        finally:

            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
        
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)
'''
class scenario_03_oc_device_sync_pkt_cpu_to_tx_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync
        ptppkt = simple_ptp_packet(msgType=0,  #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00030000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        ptppkt1 = simple_ptp_packet(msgType=0,
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0x66,
                                   cfLow=0x567b0000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt1 = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt1)

        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PTP_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14, ptp_tx_op_type=SAI_HOSTIF_PACKET_PTP_TX_PACKET_TYPE_1_STEP_TS_UPDATE)

            self.ctc_show_packet(1,None,str(pkt1),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)
'''
class scenario_03_oc_device_sync_pkt_cpu_to_tx_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync
        ptppkt = simple_ptp_packet(msgType=0,  #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00030000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=64,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        ptppkt1 = simple_ptp_packet(msgType=0,
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0x22,
                                   cfLow=0x00030000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0x445678,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt1 = simple_eth_packet(pktlen=64,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt1)

        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PTP_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14, ptp_tx_op_type=SAI_HOSTIF_PACKET_PTP_TX_PACKET_OP_TYPE_1)

            self.ctc_show_packet(1,None,str(pkt1),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class scenario_04_oc_device_delay_req_pkt_cpu_to_tx_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync
        ptppkt = simple_ptp_packet(msgType=1,  #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00030000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        ptppkt1 = simple_ptp_packet(msgType=1,
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0x22,
                                   #cfLow=0x00350000, bug110916
                                   cfLow=0x00030000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0x445678,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt1 = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt1)

        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PTP_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14, ptp_tx_op_type=SAI_HOSTIF_PACKET_PTP_TX_PACKET_OP_TYPE_1)                                    

            self.ctc_show_packet(1,None,str(pkt1),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class scenario_05_bc_device_sync_pkt_cpu_to_tx_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_BC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync
        ptppkt = simple_ptp_packet(msgType=0,  #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=64,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00030000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=64,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        ptppkt1 = simple_ptp_packet(msgType=0,
                                   msgLen=64,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0x22,
                                   cfLow=0x00030000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0x445678,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt1 = simple_eth_packet(pktlen=64,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt1)

        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PTP_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14, ptp_tx_op_type=SAI_HOSTIF_PACKET_PTP_TX_PACKET_OP_TYPE_1)                                    

            self.ctc_show_packet(1,None,str(pkt1),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class scenario_06_bc_device_delay_req_pkt_cpu_to_tx_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_BC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync
        ptppkt = simple_ptp_packet(msgType=1,  #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=64,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00030000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=64,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        ptppkt1 = simple_ptp_packet(msgType=1,
                                   msgLen=64,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0x66,
                                   cfLow=0x567b0000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt1 = simple_eth_packet(pktlen=64,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt1)

        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PTP_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14, ptp_tx_op_type=SAI_HOSTIF_PACKET_PTP_TX_PACKET_OP_TYPE_2)                                    

            self.ctc_show_packet(1,None,str(pkt1),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class scenario_07_e2e_tc_device_delay_resp_pkt_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        path_delay = 100
        igs_delay = 200
        egs_delay = 50

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_E2E_TC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(u64=path_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_PATH_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u64=igs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        #delay_req
        ptppkt = simple_ptp_packet(msgType=9, #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=54,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00030005,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=None,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=2,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=54,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)
        
        warmboot(self.client)
        try:
            #pdb.set_trace()
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1])


        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_PATH_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)


class scenario_08_e2e_tc_device_sync_pkt_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        path_delay = 100
        igs_delay = 200
        egs_delay = 50

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_E2E_TC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(u64=path_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_PATH_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u64=igs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        #delay_req
        ptppkt = simple_ptp_packet(msgType=0, #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=54,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00030005,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=None,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=2,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=54,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        ptppkt1 = simple_ptp_packet(msgType=0, #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=54,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0x32, #mac_tx_gen_ts - ipe_fwd_gen_ts
                                   cfLow=0x00cb0005, # igs_delay
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=None,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=2,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt1 = simple_eth_packet(pktlen=54,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt1)

        
        warmboot(self.client)
        try:
            #pdb.set_trace()
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt1), [1])


        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_PATH_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class scenario_09_p2p_tc_device_follow_up_pkt_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        path_delay = 100
        igs_delay = 200
        egs_delay = 50

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_P2P_TC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(u64=path_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_PATH_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u64=igs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        #delay_req
        ptppkt = simple_ptp_packet(msgType=8, #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00030005,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=None,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=63,
                                   tsNs=62,
                                   reqClockId="1023",
                                   reqSrcPortId=2,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)
        
        warmboot(self.client)
        try:
            #pdb.set_trace()
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1])


        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_PATH_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class scenario_10_p2p_tc_device_sync_pkt_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD
        path_delay = 100
        igs_delay = 200
        egs_delay = 50

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_P2P_TC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(u64=path_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_PATH_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u64=igs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        #delay_req
        ptppkt = simple_ptp_packet(msgType=0, #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00030005,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=None,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=63,
                                   tsNs=62,
                                   reqClockId="1023",
                                   reqSrcPortId=2,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        ptppkt1 = simple_ptp_packet(msgType=0, #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0x32, #mac_tx_gen_ts - ipe_fwd_gen_ts
                                   cfLow=0x012f0005, #path_delay + igs_delay
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=None,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=63,
                                   tsNs=62,
                                   reqClockId="1023",
                                   reqSrcPortId=2,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt1 = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt1)

        
        warmboot(self.client)
        try:
            #pdb.set_trace()
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt1), [1])


        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_PATH_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_INGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class scenario_11_oc_device_sync_pkt_cpu_to_tx_2_step_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync
        ptppkt = simple_ptp_packet(msgType=0,  #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00000000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        ptppkt1 = simple_ptp_packet(msgType=0,
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0x66,
                                   cfLow=0x56780000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt1 = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt1)

        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PTP_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14, ptp_tx_op_type=SAI_HOSTIF_PACKET_PTP_TX_PACKET_OP_TYPE_2)

            self.ctc_show_packet(1,None,str(pkt1),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)

class scenario_12_oc_device_cpu_to_tx_2_step_followup_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync

                                   
        ptppkt = simple_ptp_packet(msgType=8, #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00000005,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=None,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0x12345678,
                                   tsNs=0x87654321,
                                   reqClockId="1023",
                                   reqSrcPortId=2,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14)

            self.ctc_show_packet(1,None,str(pkt),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)


class scenario_13_oc_device_pdelay_resp_pkt_cpu_to_tx_1_step_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync
        ptppkt = simple_ptp_packet(msgType=3,  #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00070000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=64,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        ptppkt1 = simple_ptp_packet(msgType=3,
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0x55,
                                   cfLow=0x456e0000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt1 = simple_eth_packet(pktlen=64,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt1)

        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PTP_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14, ptp_tx_op_type=SAI_HOSTIF_PACKET_PTP_TX_PACKET_OP_TYPE_3, sec=0, nsec=0x111111)

            self.ctc_show_packet(1,None,str(pkt1),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)



class scenario_14_oc_device_pdelay_resp_pkt_cpu_to_tx_2_step_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync
        ptppkt = simple_ptp_packet(msgType=3,  #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00000000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        ptppkt1 = simple_ptp_packet(msgType=3,
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0x66,
                                   cfLow=0x56780000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt1 = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt1)

        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PTP_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14, ptp_tx_op_type=SAI_HOSTIF_PACKET_PTP_TX_PACKET_OP_TYPE_2)

            self.ctc_show_packet(1,None,str(pkt1),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)



class scenario_15_oc_device_cpu_to_tx_2_step_pdelay_resp_followup_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_OC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync

                                   
        ptppkt = simple_ptp_packet(msgType=10, #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00000005,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=None,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0x12345678,
                                   tsNs=0x87654321,
                                   reqClockId="1023",
                                   reqSrcPortId=2,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)


        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14)

            self.ctc_show_packet(1,None,str(pkt),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)



class scenario_16_bc_device_sync_pkt_cpu_to_tx_2_step_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_BC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync
        ptppkt = simple_ptp_packet(msgType=0,  #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00000000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        ptppkt1 = simple_ptp_packet(msgType=0,
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0x66,
                                   cfLow=0x56780000,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=0,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0,
                                   tsNs=0,
                                   reqClockId="1023",
                                   reqSrcPortId=0,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt1 = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt1)

        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PTP_PACKET_TX
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14, ptp_tx_op_type=SAI_HOSTIF_PACKET_PTP_TX_PACKET_OP_TYPE_2)

            self.ctc_show_packet(1,None,str(pkt1),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)



class scenario_17_bc_device_cpu_to_tx_2_step_followup_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging ("access port to access port")
        
        switch_init(self.client)
        
        vlan_id = 100
        port1 = port_list[0]
        port2 = port_list[1]
        default_1q_bridge = self.client.sai_thrift_get_default_1q_bridge_id()
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        enable_type = SAI_PTP_ENABLE_BASED_ON_PORT
        device_type = SAI_PTP_DEVICE_BC
        ptp_oid = sai_thrift_create_ptp(self.client, enable_type, device_type)
        
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_UNTAGGED)
        
        attr_value = sai_thrift_attribute_value_t(u16=vlan_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        attr_value = sai_thrift_attribute_value_t(oid=ptp_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_DOMAIN_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        egs_delay = 50
        attr_value = sai_thrift_attribute_value_t(u64=egs_delay)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)
        #sync

                                   
        ptppkt = simple_ptp_packet(msgType=8, #0:sync 1:delay_req 2:pdelay_req 3:pdelay_resp 8:follow_up 9:delay_resp 10:pdelay_resp_follow_up
                                   msgLen=44,
                                   flag0=0,
                                   flag1=0,
                                   cfHigh=0,
                                   cfLow=0x00000005,
                                   clockId="4097",
                                   srcPortId=1,
                                   seqId=302,
                                   controlFld=None,
                                   logMsgInt=0x7F,
                                   tsSecHigh=0,
                                   tsSec=0x12345678,
                                   tsNs=0x87654321,
                                   reqClockId="1023",
                                   reqSrcPortId=2,
                                   utcOffset=0,
                                   masterPri1=0,
                                   clockQuality=0,
                                   masterPri2=0,
                                   masterId=0,
                                   stepRemove=0,
                                   timeSrc=0)
        
        pkt = simple_eth_packet(pktlen=44,
                                eth_dst=mac2,
                                eth_src=mac1,
                                eth_type=0x88f7,
                                inner_frame=ptppkt)

        
        warmboot(self.client)
        try:
            oam_tx_type = SAI_HOSTIF_PACKET_OAM_TX_TYPE_DM #no use
            host_if_tx_type = SAI_HOSTIF_TX_TYPE_PIPELINE_BYPASS
            sai_thrift_send_hostif_packet(self.client, ptp_oid, str(pkt), oam_tx_type, host_if_tx_type, egress_port = port2, oam_session=None, dm_offset=14)

            self.ctc_show_packet(1,None,str(pkt),1)
            #self.ctc_verify_packets( str(pkt), [1])
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)

            attr_value = sai_thrift_attribute_value_t(u64=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PTP_EGRESS_ASYMMETRY_DELAY, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            self.client.sai_thrift_remove_ptp_domain(ptp_oid)











            
