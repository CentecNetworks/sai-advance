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
Thrift SAI interface Wred tests
"""
import socket
from switch import *
import sai_base_test
import pdb

#Wred
@group('Wred')
class WredCreateWithEnableGreenDrop(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create WredId
        step1:create wred id & enable green drop
        step2:verify wred attr 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        color_en = [1,0,0]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [50, 30, 10]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        sys_logging("Color_en:", color_en)
        sys_logging("min_thrd:", min_thrd)
        sys_logging("max_thrd:", max_thrd)
        sys_logging("drop_prob:", drop_prob)
        sys_logging("wred_id:",wred_id)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    if a.value.booldata is not True:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata is not False:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata is not False:
                        sys_logging("red drop en:%d"%a.value.booldata)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("green min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("yellow min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    if a.value.u32 != 100:
                        sys_logging("red min thrd:",a.value.u32)
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 2000:
                        sys_logging("green max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        sys_logging("yellow max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        sys_logging("red max thrd:",a.value.u32)
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 50:
                        sys_logging("green drop prob:",a.value.u32)
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    if a.value.u32 != 30:
                        sys_logging("yellow drop prob:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("red drop prob:",a.value.u32)
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_wred_profile(wred_id)

@group('Wred')
class WredCreateWithEnableYellowDrop(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create WredId
        step1:create wred id & enable yellow drop
        step2:verify wred attr 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        color_en = [0,1,0]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [50, 10, 10]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        sys_logging("Color_en:", color_en)
        sys_logging("min_thrd:", min_thrd)
        sys_logging("max_thrd:", max_thrd)
        sys_logging("drop_prob:", drop_prob)
        sys_logging("wred_id:",wred_id)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    if a.value.booldata is not False:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata is not True:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata is not False:
                        sys_logging("red drop en:%d"%a.value.booldata)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("green min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("yellow min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    if a.value.u32 != 100:
                        sys_logging("red min thrd:",a.value.u32)
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 2000:
                        sys_logging("green max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        sys_logging("yellow max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        sys_logging("red max thrd:",a.value.u32)
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 50:
                        sys_logging("green drop prob:",a.value.u32)
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("yellow drop prob:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("red drop prob:",a.value.u32)
                        raise NotImplementedError()                                   

        finally:
            self.client.sai_thrift_remove_wred_profile(wred_id)

@group('Wred')
class WredCreateWithEnableRedDrop(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create WredId
        step1:create wred id & enable red drop
        step2:verify wred attr 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        color_en = [0,0,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [50, 10, 10]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        sys_logging("Color_en:", color_en)
        sys_logging("min_thrd:", min_thrd)
        sys_logging("max_thrd:", max_thrd)
        sys_logging("drop_prob:", drop_prob)
        sys_logging("wred_id:",wred_id)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    if a.value.booldata is not False:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata is not False:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata is not True:
                        sys_logging("red drop en:%d"%a.value.booldata)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("green min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("yellow min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    if a.value.u32 != 100:
                        sys_logging("red min thrd:",a.value.u32)
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 2000:
                        sys_logging("green max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        sys_logging("yellow max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        sys_logging("red max thrd:",a.value.u32)
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 50:
                        sys_logging("green drop prob:",a.value.u32)
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("yellow drop prob:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("red drop prob:",a.value.u32)
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_wred_profile(wred_id)

@group('Wred')
class WredCreateWithEnableAllColorDrop(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create WredId
        step1:create wred id & enable green/yellow/red drop
        step2:verify wred attr 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [10, 10, 10]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        sys_logging("Color_en:", color_en)
        sys_logging("min_thrd:", min_thrd)
        sys_logging("max_thrd:", max_thrd)
        sys_logging("drop_prob:", drop_prob)
        sys_logging("wred_id:",wred_id)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    if a.value.booldata is not True:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata is not True:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata is not True:
                        sys_logging("red drop en:%d"%a.value.booldata)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("green min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("yellow min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    if a.value.u32 != 100:
                        sys_logging("red min thrd:",a.value.u32)
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 2000:
                        sys_logging("green max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        sys_logging("yellow max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        sys_logging("red max thrd:",a.value.u32)
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("green drop prob:",a.value.u32)
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("yellow drop prob:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("red drop prob:",a.value.u32)
                        raise NotImplementedError()                                   

        finally:
            self.client.sai_thrift_remove_wred_profile(wred_id)

@group('Wred')
class WredCreateWithEnableAllColorDropWithEcn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create WredId
        step1:create wred id & enable green/yellow/red drop
        step2:verify wred attr 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [10, 10, 10]
        ecn_thrd = [1500,1300,150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("Color_en:", color_en)
        sys_logging("min_thrd:", min_thrd)
        sys_logging("max_thrd:", max_thrd)
        sys_logging("drop_prob:", drop_prob)
        sys_logging("drop_prob:", ecn_thrd)
        sys_logging("wred_id:",wred_id)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    if a.value.booldata is not True:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata is not True:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata is not True:
                        sys_logging("red drop en:%d"%a.value.booldata)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("green min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("yellow min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    if a.value.u32 != 100:
                        sys_logging("red min thrd:",a.value.u32)
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 2000:
                        sys_logging("green max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        sys_logging("yellow max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        sys_logging("red max thrd:",a.value.u32)
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("green drop prob:",a.value.u32)
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("yellow drop prob:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("red drop prob:",a.value.u32)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        sys_logging("green ecn thrd:",a.value.u32)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1300:
                        sys_logging("green ecn thrd:",a.value.u32)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                    if a.value.u32 != 150:
                        sys_logging("green ecn thrd:",a.value.u32)
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_wred_profile(wred_id)
            
@group('Wred')
class WredSetWredAttributeTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create WredId
        step1:create wred id & enable yellow/red drop
        step2:verify wred attr & Set attribute
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        color_en = [0,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [10, 10, 10]
        ecn_thrd = [1500,1300,150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("Color_en:", color_en)
        sys_logging("min_thrd:", min_thrd)
        sys_logging("max_thrd:", max_thrd)
        sys_logging("drop_prob:", drop_prob)
        sys_logging("wred_id:",wred_id)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    if a.value.booldata is not False:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata is not True:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata is not True:
                        sys_logging("red drop en:%d"%a.value.booldata)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("green min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        sys_logging("yellow min thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    if a.value.u32 != 100:
                        sys_logging("red min thrd:",a.value.u32)
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 2000:
                        sys_logging("green max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        sys_logging("yellow max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        sys_logging("red max thrd:",a.value.u32)
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("green drop prob:",a.value.u32)
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("yellow drop prob:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        sys_logging("red drop prob:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        sys_logging("green ecn thrd:",a.value.u32)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_ECN_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1300:
                        sys_logging("green ecn thrd:",a.value.u32)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_ECN_RED_MAX_THRESHOLD:
                    if a.value.u32 != 150:
                        sys_logging("green ecn thrd:",a.value.u32)
                        raise NotImplementedError()

            #Set green Attrs
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_ENABLE, value=attr_value)
            self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr) 
            attr_value = sai_thrift_attribute_value_t(u32=2000)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_MIN_THRESHOLD, value=attr_value)
            self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr) 
            attr_value = sai_thrift_attribute_value_t(u32=3000)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_MAX_THRESHOLD, value=attr_value)
            self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr) 
            attr_value = sai_thrift_attribute_value_t(u32=50)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_DROP_PROBABILITY, value=attr_value)
            self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)
            
            attr_value = sai_thrift_attribute_value_t(u32=1550)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD, value=attr_value)
            self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)

            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    sys_logging("new green drop en:%d"%a.value.booldata)
                    if a.value.booldata is not True:
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    sys_logging("yellow drop en:%d"%a.value.booldata)
                    if a.value.booldata is not True:
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    sys_logging("red drop en:%d"%a.value.booldata)
                    if a.value.booldata is not True:
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    sys_logging("new green min thrd:",a.value.u32)
                    if a.value.u32 != 2000:
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    sys_logging("yellow min thrd:",a.value.u32)
                    if a.value.u32 != 1000:
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    sys_logging("red min thrd:",a.value.u32)
                    if a.value.u32 != 100:
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    sys_logging("green max thrd:",a.value.u32)
                    if a.value.u32 != 3000:
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        sys_logging("yellow max thrd:",a.value.u32)
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        sys_logging("red max thrd:",a.value.u32)
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 50:
                        sys_logging("new green drop prob:",a.value.u32)
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    sys_logging("yellow drop prob:",a.value.u32)
                    if a.value.u32 != 10:
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    sys_logging("red drop prob:",a.value.u32)
                    if a.value.u32 != 10:
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_ECN_GREEN_MAX_THRESHOLD:
                    sys_logging("new green ecn thrd:",a.value.u32)
                    if a.value.u32 != 1550:
                        raise NotImplementedError()

        finally:
            self.client.sai_thrift_remove_wred_profile(wred_id)

class QueueSetQueueAttributeWithWredIdTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create queue id & Set Attr with WredId
        step2:verify queue attr 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]
        queue_index = 1

        #create Wred Id
        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        ecn_thrd = [1500,1300,150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("wred_id:",wred_id)

        #Create Queue Id
        queueId = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_UNICAST, port, queue_index, 0) 
        sys_logging("queue_id:",queueId)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId)
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred_id:0x%X"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()                                      
        finally:            
            self.client.sai_thrift_remove_queue(queueId)
            self.client.sai_thrift_remove_wred_profile(wred_id)
            
class SetWredIdUpdateQueueConfigTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueIds
        step1:create queue id & Set Attr with WredId
        step2:verify queue attr 
        step3:modify wred attr
        step4:check queue status        
        step5:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]
        queue_index = 1

        #create Wred Id
        color_en = [0,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        ecn_thrd = [1500,1300,150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("wred_id:",wred_id)

        #Create Queue Id
        queueId1 = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_UNICAST, port, queue_index, wred_id) 
        sys_logging("queue_id1:",queueId1)
        
        queue_index = 2
        queueId2 = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_UNICAST, port, queue_index, wred_id) 
        sys_logging("queue_id2:",queueId2)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId1)
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred_id:0x%X"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()
                        
            #Set green Attrs
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_ENABLE, value=attr_value)
            self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr) 
            attr_value = sai_thrift_attribute_value_t(u32=2000)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_MIN_THRESHOLD, value=attr_value)
            self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr) 
            attr_value = sai_thrift_attribute_value_t(u32=3000)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_MAX_THRESHOLD, value=attr_value)
            self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr) 
            attr_value = sai_thrift_attribute_value_t(u32=50)
            attr = sai_thrift_attribute_t(id=SAI_WRED_ATTR_GREEN_DROP_PROBABILITY, value=attr_value)
            self.client.sai_thrift_set_wred_attribute_profile(wred_id, attr)            
            
        finally:            
            self.client.sai_thrift_remove_queue(queueId1)
            self.client.sai_thrift_remove_queue(queueId2)
            self.client.sai_thrift_remove_wred_profile(wred_id)