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
class fun_01_wred_create_with_enable_green_drop(sai_base_test.ThriftInterfaceDataPlane):
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
                    if a.value.booldata != True:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata != False:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata != False:
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
class fun_02_wred_create_with_enable_yellow_drop(sai_base_test.ThriftInterfaceDataPlane):
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
                    if a.value.booldata != False:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata != True:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata != False:
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
class fun_03_wred_create_with_enable_red_drop(sai_base_test.ThriftInterfaceDataPlane):
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
                    if a.value.booldata != False:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata != False:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata != True:
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
class fun_04_wred_create_with_enable_all_color_drop(sai_base_test.ThriftInterfaceDataPlane):
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
                    if a.value.booldata != True:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata != True:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata != True:
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
class fun_05_wred_create_with_enable_all_color_drop_with_ecn(sai_base_test.ThriftInterfaceDataPlane):
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
                    if a.value.booldata != True:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata != True:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata != True:
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
class fun_06_wred_set_wred_attribute_test(sai_base_test.ThriftInterfaceDataPlane):
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
                    if a.value.booldata != False:
                        sys_logging("green drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata != True:
                        sys_logging("yellow drop en:%d"%a.value.booldata)
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata != True:
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
                    if a.value.booldata != True:
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    sys_logging("yellow drop en:%d"%a.value.booldata)
                    if a.value.booldata != True:
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    sys_logging("red drop en:%d"%a.value.booldata)
                    if a.value.booldata != True:
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

class fun_07_queue_set_queue_attribute_with_wred_id_test(sai_base_test.ThriftInterfaceDataPlane):
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
        sys_logging("wred_id:", wred_id)

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

class fun_08_set_wred_id_update_queue_config_test(sai_base_test.ThriftInterfaceDataPlane):
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

class fun_09_wred_id_share_between_queues_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        #attr_value = sai_thrift_attribute_value_t(booldata=True)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECN_ACTION_ENABLE, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr)

        #Create Wred Id
        color_en  = [1, 1, 1]
        min_thrd  = [1000, 1000, 100]
        max_thrd  = [2000, 1500, 200]
        drop_prob = [100,  50,   10]
        ecn_thrd  = [1500, 1300, 150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("wred_id=0x%lx" %wred_id)
        assert (wred_id != SAI_NULL_OBJECT_ID)

        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port1 = port_list[0]
        port2 = port_list[1]
        level = [0,1,2]
        max_childs = [4, 64, 8]
        sched_group_id_group_node = [None]*8
        sched_group_service_id = 1
        service_queueId = [None]*8

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 2000000
        dynamic_th = 0
        xon_th = 1000000
        xoff_th = 1200000
        buf_prof_id1 = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = -2
        xon_th = 1000000
        xoff_th = 1200000
        buf_prof_id2 = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)

        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port1, level[0], max_childs[0], port1, 0)
        sched_group_id_chan_node = sai_thrift_qos_create_scheduler_group(self.client, port1, level[1], max_childs[1], sched_group_id_root, 0)

        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)

        #Create Queue Id
        normal_queueId = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, 0, 0)
        assert (normal_queueId != SAI_NULL_OBJECT_ID)
        sys_logging("normal_queueId=0x%lx" %normal_queueId)

        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[0], parent_id=sched_group_id_group_node[0], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[0]=0x%lx" %service_queueId[0]
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[1], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[1]=0x%lx" %service_queueId[1]
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[2], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[2]=0x%lx" %service_queueId[2]
        service_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[3], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[3]=0x%lx" %service_queueId[3]
        service_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[4], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[4]=0x%lx" %service_queueId[4]
        service_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[5], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[5]=0x%lx" %service_queueId[5]
        service_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[6], parent_id=sched_group_id_group_node[6], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[6]=0x%lx" %service_queueId[6]
        service_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[7], parent_id=sched_group_id_group_node[6], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[7]=0x%lx" %service_queueId[7]

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(normal_queueId, attr)
        assert (status == SAI_STATUS_SUCCESS)

        try:
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(normal_queueId)
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

            status = self.client.sai_thrift_remove_wred_profile(wred_id)
            assert (status != SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_wred_profile(wred_id)
            assert (status != SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_queue_attribute(normal_queueId)
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id:
                        raise NotImplementedError()

            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(normal_queueId, attr)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_wred_profile(wred_id)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(normal_queueId)
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != SAI_NULL_OBJECT_ID:
                        raise NotImplementedError()

        finally:
            for i in range(8):
                print "service_queueId[%d]=0x%lx" %(i, service_queueId[i])
                status = self.client.sai_thrift_remove_queue(service_queueId[i])
                assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_queue(normal_queueId)
            assert (status == SAI_STATUS_SUCCESS)

            for ii in range(8):
                status = self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_id1)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_id2)
            assert (status == SAI_STATUS_SUCCESS)

class fun_10_wred_id_exchange_between_queues_type_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        #attr_value = sai_thrift_attribute_value_t(booldata=True)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECN_ACTION_ENABLE, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr)

        #Create Wred Id1
        color_en  = [1, 1, 1]
        min_thrd  = [1000, 1000, 100]
        max_thrd  = [2000, 1500, 200]
        drop_prob = [100,  50,   10]
        ecn_thrd  = [1500, 1300, 150]
        wred_id1 = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("wred_id=0x%lx" %wred_id1)
        assert (wred_id1 != SAI_NULL_OBJECT_ID)

        #Create Wred Id2
        color_en  = [1, 1, 1]
        min_thrd  = [3000, 3000, 300]
        max_thrd  = [4000, 3500, 350]
        drop_prob = [100,  50,   10]
        ecn_thrd  = [1500, 1300, 150]
        wred_id2 = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("wred_id=0x%lx" %wred_id2)
        assert (wred_id2 != SAI_NULL_OBJECT_ID)

        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port1 = port_list[0]
        port2 = port_list[1]
        level = [0,1,2]
        max_childs = [4, 64, 8]
        sched_group_id_group_node = [None]*8
        sched_group_service_id = 1
        service_queueId = [None]*8

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 2000000
        dynamic_th = 0
        xon_th = 1000000
        xoff_th = 1200000
        buf_prof_id1 = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = -2
        xon_th = 1000000
        xoff_th = 1200000
        buf_prof_id2 = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)

        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port1, level[0], max_childs[0], port1, 0)
        sched_group_id_chan_node = sai_thrift_qos_create_scheduler_group(self.client, port1, level[1], max_childs[1], sched_group_id_root, 0)

        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port1, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)

        #Create Queue Id
        normal_queueId = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, 0, 0)
        assert (normal_queueId != SAI_NULL_OBJECT_ID)
        sys_logging("normal_queueId=0x%lx" %normal_queueId)

        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[0], parent_id=sched_group_id_group_node[0], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[0]=0x%lx" %service_queueId[0]
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[1], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[1]=0x%lx" %service_queueId[1]
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[2], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[2]=0x%lx" %service_queueId[2]
        service_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[3], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[3]=0x%lx" %service_queueId[3]
        service_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[4], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[4]=0x%lx" %service_queueId[4]
        service_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[5], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[5]=0x%lx" %service_queueId[5]
        service_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[6], parent_id=sched_group_id_group_node[6], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[6]=0x%lx" %service_queueId[6]
        service_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port1, queue_index[7], parent_id=sched_group_id_group_node[6], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[7]=0x%lx" %service_queueId[7]

        attr_value = sai_thrift_attribute_value_t(oid=wred_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(normal_queueId, attr)
        assert (status == SAI_STATUS_SUCCESS)

        try:
            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(normal_queueId)
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id2:
                        raise NotImplementedError()

            status = self.client.sai_thrift_remove_wred_profile(wred_id1)
            assert (status != SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_wred_profile(wred_id2)
            assert (status != SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=wred_id2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=wred_id2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=wred_id2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=wred_id2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=wred_id2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=wred_id2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=wred_id2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=wred_id2)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
            assert (status == SAI_STATUS_SUCCESS)

            attr_value = sai_thrift_attribute_value_t(oid=wred_id1)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(normal_queueId, attr)
            assert (status == SAI_STATUS_SUCCESS)

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[0])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id2:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[1])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id2:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[2])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id2:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[3])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id2:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[4])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id2:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[5])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id2:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[6])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id1:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id2:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(service_queueId[7])
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                    sys_logging("get queue buffer profile:0x%x"%a.value.oid)
                    if a.value.oid != buf_prof_id2:
                        raise NotImplementedError()
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id2:
                        raise NotImplementedError()

            attrs = self.client.sai_thrift_get_queue_attribute(normal_queueId)
            assert(SAI_STATUS_SUCCESS == attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    sys_logging("get wred profile:0x%x"%a.value.oid)
                    if a.value.oid != wred_id1:
                        raise NotImplementedError()

        finally:
            for i in range(8):
                print "service_queueId[%d]=0x%lx" %(i, service_queueId[i])
                status = self.client.sai_thrift_remove_queue(service_queueId[i])
                assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_queue(normal_queueId)
            assert (status == SAI_STATUS_SUCCESS)

            for ii in range(8):
                status = self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_id1)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_id2)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_wred_profile(wred_id1)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_wred_profile(wred_id2)
            assert (status == SAI_STATUS_SUCCESS)

@group('Wred')
class fun_11_queue_type_all_reset_default_after_remove_wred(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create WredId
        step1:create wred id & enable green/yellow/red drop
        step2:verify wred attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        #attr_value = sai_thrift_attribute_value_t(booldata=True)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECN_ACTION_ENABLE, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr)

        queue_index = 1
        wred_list = []
        queue_list = []

        for i in range(5):
            for j in range(8):
                #Create Wred Id
                color_en  = [1, 1, 1]
                min_thrd  = [(1000+i*1000+j*100), (1000+i*1000+j*100), (100+i*1000+j*100)]
                max_thrd  = [(2000+i*1000+j*100), (1500+i*1000+j*100), (200+i*1000+j*100)]
                drop_prob = [100,  50,   10]
                ecn_thrd  = [1500, 1300, 150]
                wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
                sys_logging("wred_id[%d]=0x%lx" %(i, wred_id))
                wred_list.append(wred_id)

                if (i*8+j) < 31:
                    sys_logging("i=%d, j=%d, index:%d" %(i, j, (i*8+j)))
                    assert (wred_id != SAI_NULL_OBJECT_ID)
                else:
                    assert (wred_id == SAI_NULL_OBJECT_ID)

                #Create Queue Id
                queue_id = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port_list[i], j, 0)
                assert (queue_id != SAI_NULL_OBJECT_ID)
                queue_list.append(queue_id)
                sys_logging("queue_id[%d][%d]=0x%lx" %(i, j, queue_id))

        sys_logging("set queue wred cfg")
        i = 0
        for queue_id in queue_list:
            if (i < 31):
                wred_id = wred_list[i]
            else:
                wred_id = wred_list[30]

            attr_value = sai_thrift_attribute_value_t(oid=wred_id)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(queue_list[i], attr)
            assert (status == SAI_STATUS_SUCCESS)
            i = i + 1

        warmboot(self.client)
        try:
            for i in range(30, 40):
                attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)

                status = self.client.sai_thrift_set_queue_attribute(queue_list[i], attr)
                assert (status == SAI_STATUS_SUCCESS)

                status = self.client.sai_thrift_remove_wred_profile(wred_list[30])
                if (i != 39):
                    sys_logging("fail i:%d, wred_list[30]:0x%lx" %(i, wred_list[30]))
                    assert (status != SAI_STATUS_SUCCESS)
                else:
                    sys_logging("success i:%d, wred_list[30]:0x%lx" %(i, wred_list[30]))
                    assert (status == SAI_STATUS_SUCCESS)

            min_thrd = [10000, 10000, 5000]
            max_thrd = [20000, 20000, 7000]

            wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
            sys_logging("wred_id=0x%lx" %wred_id)
            assert (wred_id != SAI_NULL_OBJECT_ID)

            attr_value = sai_thrift_attribute_value_t(oid=wred_id)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            for i in range(31, 40):
                status = self.client.sai_thrift_set_queue_attribute(queue_list[i], attr)
                assert (status == SAI_STATUS_SUCCESS)

        finally:
            for queue_id in queue_list:
                attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                status = self.client.sai_thrift_set_queue_attribute(queue_id, attr)
                assert (status == SAI_STATUS_SUCCESS)

            for i in range(31):
                status = self.client.sai_thrift_remove_wred_profile(wred_list[i])
                assert (status == SAI_STATUS_SUCCESS)

            for queue_id in queue_list:
                statue = self.client.sai_thrift_remove_queue(queue_id)
                assert (status == SAI_STATUS_SUCCESS)

class fun_12_queue_type_service_reset_default_after_remove_wred(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        #attr_value = sai_thrift_attribute_value_t(booldata=True)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECN_ACTION_ENABLE, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr)

        #Create Wred Id
        color_en  = [1, 1, 1]
        min_thrd  = [1000, 1000, 100]
        max_thrd  = [2000, 1500, 200]
        drop_prob = [100,  50,   10]
        ecn_thrd  = [1500, 1300, 150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("wred_id=0x%lx" %wred_id)
        assert (wred_id != SAI_NULL_OBJECT_ID)

        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 64, 8]
        sched_group_id_group_node = [None]*8
        sched_group_service_id = 1
        service_queueId = [None]*8

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 2000000
        dynamic_th = 0
        xon_th = 1000000
        xoff_th = 1200000
        buf_prof_id1 = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)

        print "step1:"

        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = -2
        xon_th = 1000000
        xoff_th = 1200000
        buf_prof_id2 = sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)

        sched_group_id_root = sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], port, 0)
        sched_group_id_chan_node = sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], sched_group_id_root, 0)

        sched_group_id_group_node[0] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[1] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[2] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[3] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[4] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[5] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[6] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)
        sched_group_id_group_node[7] = sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[2], sched_group_id_chan_node, 0, service_id=sched_group_service_id)

        #pdb.set_trace()
        print "step2:"

        queue_type = SAI_QUEUE_TYPE_SERVICE
        queue_index = [0,1,2,3,4,5,6,7]
        service_queueId[0] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[0], parent_id=sched_group_id_group_node[0], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[0]=0x%lx" %service_queueId[0]
        service_queueId[1] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[1], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[1]=0x%lx" %service_queueId[1]
        service_queueId[2] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[2], parent_id=sched_group_id_group_node[1], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[2]=0x%lx" %service_queueId[2]
        service_queueId[3] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[3], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[3]=0x%lx" %service_queueId[3]
        service_queueId[4] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[4], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[4]=0x%lx" %service_queueId[4]
        service_queueId[5] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[5], parent_id=sched_group_id_group_node[3], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[5]=0x%lx" %service_queueId[5]
        service_queueId[6] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[6], parent_id=sched_group_id_group_node[6], service_id=sched_group_service_id, buffer_id=buf_prof_id1)
        print "service_queueId[6]=0x%lx" %service_queueId[6]
        service_queueId[7] = sai_thrift_create_queue_id(self.client, queue_type, port, queue_index[7], parent_id=sched_group_id_group_node[6], service_id=sched_group_service_id, buffer_id=buf_prof_id2)
        print "service_queueId[7]=0x%lx" %service_queueId[7]

        #pdb.set_trace()
        print "step3:"

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
        assert (status == SAI_STATUS_SUCCESS)

        #pdb.set_trace()
        print "step4:"

        attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)

        status = self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)
        assert (status == SAI_STATUS_SUCCESS)

        status = self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
        assert (status == SAI_STATUS_SUCCESS)

        #pdb.set_trace()
        print "step5:"

        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)
        assert (status == SAI_STATUS_SUCCESS)

        attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
        assert (status == SAI_STATUS_SUCCESS)

        #pdb.set_trace()
        print "step6:"

        try:
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)

            status = self.client.sai_thrift_set_queue_attribute(service_queueId[0], attr)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_set_queue_attribute(service_queueId[1], attr)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_set_queue_attribute(service_queueId[2], attr)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_set_queue_attribute(service_queueId[3], attr)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_set_queue_attribute(service_queueId[4], attr)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_set_queue_attribute(service_queueId[5], attr)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_set_queue_attribute(service_queueId[6], attr)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_set_queue_attribute(service_queueId[7], attr)
            assert (status == SAI_STATUS_SUCCESS)

            #pdb.set_trace()
            print "step7:"

        finally:
            for i in range(8):
                print "service_queueId[%d]=0x%lx" %(i, service_queueId[i])
                status = self.client.sai_thrift_remove_queue(service_queueId[i])
                assert (status == SAI_STATUS_SUCCESS)

            for ii in range(8):
                status = self.client.sai_thrift_remove_scheduler_group(sched_group_id_group_node[ii])
                assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_scheduler_group(sched_group_id_chan_node)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_scheduler_group(sched_group_id_root)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_id1)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_buffer_profile(buf_prof_id2)
            assert (status == SAI_STATUS_SUCCESS)

            status = self.client.sai_thrift_remove_wred_profile(wred_id)
            assert (status == SAI_STATUS_SUCCESS)

@group('Wred')
class fun_13_wred_id_max_resource(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create WredId
        step1:create wred id & enable green/yellow/red drop
        step2:verify wred attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)

        #attr_value = sai_thrift_attribute_value_t(booldata=True)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECN_ACTION_ENABLE, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr)

        queue_index = 1
        wred_list = []
        queue_list = []

        for i in range(5):
            for j in range(8):
                #Create Wred Id
                color_en  = [1, 1, 1]
                min_thrd  = [(1000+i*1000+j*100), (1000+i*1000+j*100), (100+i*1000+j*100)]
                max_thrd  = [(2000+i*1000+j*100), (1500+i*1000+j*100), (200+i*1000+j*100)]
                drop_prob = [100,  50,   10]
                ecn_thrd  = [1500, 1300, 150]
                wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
                sys_logging("wred_id[%d]=0x%lx" %(i, wred_id))
                wred_list.append(wred_id)

                if (i*8+j) < 31:
                    sys_logging("i=%d, j=%d, index:%d" %(i, j, (i*8+j)))
                    assert (wred_id != SAI_NULL_OBJECT_ID)
                else:
                    assert (wred_id == SAI_NULL_OBJECT_ID)

                #Create Queue Id
                queue_id = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port_list[i], j, 0)
                assert (queue_id != SAI_NULL_OBJECT_ID)
                queue_list.append(queue_id)
                sys_logging("queue_id[%d][%d]=0x%lx" %(i, j, queue_id))

        sys_logging("set queue wred cfg")
        i = 0
        for wred_id in wred_list:
            sys_logging("wred_id[%d]=0x%lx" %(i, wred_id))
            sys_logging("queue_id[%d]=0x%lx" %(i, queue_list[i]))
            attr_value = sai_thrift_attribute_value_t(oid=wred_id)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
            status = self.client.sai_thrift_set_queue_attribute(queue_list[i], attr)
            assert (status == SAI_STATUS_SUCCESS)
            i = i + 1

        warmboot(self.client)
        try:
            for i in range(31):
                attrs = self.client.sai_thrift_get_queue_attribute(queue_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                        sys_logging("get wred_id:0x%X"%a.value.oid)
                        if a.value.oid != wred_list[i]:
                            raise NotImplementedError()

        finally:
            for queue_id in queue_list:
                attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
                status = self.client.sai_thrift_set_queue_attribute(queue_id, attr)
                assert (status == SAI_STATUS_SUCCESS)

            for i in range(31):
                statue = self.client.sai_thrift_remove_wred_profile(wred_list[i])
                assert (status == SAI_STATUS_SUCCESS)

            for queue_id in queue_list:
                statue = self.client.sai_thrift_remove_queue(queue_id)
                assert (status == SAI_STATUS_SUCCESS)

@group('Wred')
class scenario_01_ecn_capable_packet_wred_set_ce_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECN_ACTION_ENABLE, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        port1 = port_list[0]
        port2 = port_list[1]

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        queue_index = 1

        #create Wred Id
        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        ecn_thrd = [1500,1300,150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("wred_id:", wred_id)

        #Create Queue Id
        queueId = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, queue_index, 0)
        sys_logging("queue_id:",queueId)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId, attr)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        ecn_ect0 = 2
        ecn_ce   = 3

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ecn=ecn_ect0,
                                pktlen=120)

        exp_pkt = simple_tcp_packet(eth_dst=dmac1,
                                    eth_src=router_mac,
                                    ip_dst=ip_addr1_subnet,
                                    ip_src='192.168.0.1',
                                    ip_id=105,
                                    ip_ttl=63,
                                    ip_ecn=ecn_ce,
                                    pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet(1, str(pkt))
            self.ctc_verify_packets(exp_pkt, [0])

        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_queue(queueId)
            self.client.sai_thrift_remove_wred_profile(wred_id)

@group('Wred')
class scenario_02_ecn_capable_packet_acl_set_ce_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECN_ACTION_ENABLE, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        port1 = port_list[0]
        port2 = port_list[1]

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        queue_index = 1

        #create Wred Id
        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        ecn_thrd = [1500,1300,150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("wred_id:", wred_id)

        #Create Queue Id
        queueId = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, queue_index, 0)
        sys_logging("queue_id:",queueId)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId, attr)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        ecn_ect0 = 2
        ecn_ce   = 3

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        ##############
        #    ACL
        ##############
        acl_attr_list = []

        # acl table info
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]

        # acl key field
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_IN_PORT, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ECN, value=attribute_value)
        acl_attr_list.append(attribute)

        # create acl table
        attribute_value = sai_thrift_attribute_value_t(s32=table_stage)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_STAGE, value=attribute_value)
        acl_attr_list.append(attribute)

        acl_table_bind_point_list = sai_thrift_s32_list_t(count=len(table_bind_point_list), s32list=table_bind_point_list)
        attribute_value = sai_thrift_attribute_value_t(s32list=acl_table_bind_point_list)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST, value=attribute_value)
        acl_attr_list.append(attribute)

        acl_table_oid = self.client.sai_thrift_create_acl_table(acl_attr_list)

        sys_logging("create acl table = %d" %acl_table_oid)
        assert(acl_table_oid != SAI_NULL_OBJECT_ID )

        # entry info
        acl_attr_list = []
        entry_priority = 1
        admin_state = True
        ip_type = SAI_ACL_IP_TYPE_IPV4ANY
        ip_type_mask = -1
        ipv4_ecn_mask = -1
        ecn_ect0 = 2
        ecn_ce = 3

        action = SAI_PACKET_ACTION_FORWARD

        #ACL table OID
        attribute_value = sai_thrift_attribute_value_t(oid=acl_table_oid)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_TABLE_ID, value=attribute_value)
        acl_attr_list.append(attribute)

        #Priority
        attribute_value = sai_thrift_attribute_value_t(u32=entry_priority)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_PRIORITY, value=attribute_value)
        acl_attr_list.append(attribute)

        # Admin State
        attribute_value = sai_thrift_attribute_value_t(booldata=admin_state)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ADMIN_STATE, value=attribute_value)
        acl_attr_list.append(attribute)

        # ip type
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(s32=ip_type), mask = sai_thrift_acl_mask_t(s32=ip_type_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE, value=attribute_value)
        acl_attr_list.append(attribute)

        # src ipv6
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=ecn_ect0), mask =sai_thrift_acl_mask_t(u8=ipv4_ecn_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ECN, value=attribute_value)
        acl_attr_list.append(attribute)

        #Packet action
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(s32=action), enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(u8=ecn_ce), enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_ECN, value=attribute_value)
        acl_attr_list.append(attribute)

        # create entry entry
        acl_entry_oid = self.client.sai_thrift_create_acl_entry(acl_attr_list)

        sys_logging("create acl entry = %d" %acl_entry_oid)
        assert(acl_entry_oid != SAI_NULL_OBJECT_ID )

        sys_logging(" step2: bind this ACL table to port  ")
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        #pdb.set_trace()

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ecn=ecn_ect0,
                                pktlen=120)

        exp_pkt = simple_tcp_packet(eth_dst=dmac1,
                                    eth_src=router_mac,
                                    ip_dst=ip_addr1_subnet,
                                    ip_src='192.168.0.1',
                                    ip_id=105,
                                    ip_ttl=63,
                                    ip_ecn=ecn_ce,
                                    pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet(1, str(pkt))
            self.ctc_verify_packets(exp_pkt, [0])

        finally:
            sys_logging("clear config")
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            status = self.client.sai_thrift_remove_acl_entry(acl_entry_oid)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_acl_table(acl_table_oid)
            assert (status == SAI_STATUS_SUCCESS)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_queue(queueId)
            self.client.sai_thrift_remove_wred_profile(wred_id)

@group('Wred')
class scenario_03_ecn_nonce_test_packet_wred_ignore_ecn_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECN_ACTION_ENABLE, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        port1 = port_list[0]
        port2 = port_list[1]

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        queue_index = 1

        #create Wred Id
        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        ecn_thrd = [1500,1300,150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("wred_id:", wred_id)

        #Create Queue Id
        queueId = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, queue_index, 0)
        sys_logging("queue_id:",queueId)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId, attr)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        ecn_nonce = 1

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        ##############
        #    ACL
        ##############
        acl_attr_list = []

        # acl table info
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]

        # acl key field
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_IN_PORT, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ECN, value=attribute_value)
        acl_attr_list.append(attribute)

        # create acl table
        attribute_value = sai_thrift_attribute_value_t(s32=table_stage)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_STAGE, value=attribute_value)
        acl_attr_list.append(attribute)

        acl_table_bind_point_list = sai_thrift_s32_list_t(count=len(table_bind_point_list), s32list=table_bind_point_list)
        attribute_value = sai_thrift_attribute_value_t(s32list=acl_table_bind_point_list)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST, value=attribute_value)
        acl_attr_list.append(attribute)

        acl_table_oid = self.client.sai_thrift_create_acl_table(acl_attr_list)

        sys_logging("create acl table = %d" %acl_table_oid)
        assert(acl_table_oid != SAI_NULL_OBJECT_ID )

        # entry info
        acl_attr_list = []
        entry_priority = 1
        admin_state = True
        ip_type = SAI_ACL_IP_TYPE_IPV4ANY
        ip_type_mask = -1
        ipv4_ecn_mask = -1
        ecn_nonce = 1
        ecn_incapable = 0

        action = SAI_PACKET_ACTION_FORWARD

        #ACL table OID
        attribute_value = sai_thrift_attribute_value_t(oid=acl_table_oid)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_TABLE_ID, value=attribute_value)
        acl_attr_list.append(attribute)

        #Priority
        attribute_value = sai_thrift_attribute_value_t(u32=entry_priority)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_PRIORITY, value=attribute_value)
        acl_attr_list.append(attribute)

        # Admin State
        attribute_value = sai_thrift_attribute_value_t(booldata=admin_state)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ADMIN_STATE, value=attribute_value)
        acl_attr_list.append(attribute)

        # ip type
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(s32=ip_type), mask = sai_thrift_acl_mask_t(s32=ip_type_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE, value=attribute_value)
        acl_attr_list.append(attribute)

        # src ipv6
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=ecn_nonce), mask =sai_thrift_acl_mask_t(u8=ipv4_ecn_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ECN, value=attribute_value)
        acl_attr_list.append(attribute)

        #Packet action
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(s32=action), enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION, value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(u8=ecn_incapable), enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_ECN, value=attribute_value)
        acl_attr_list.append(attribute)

        # create entry entry
        acl_entry_oid = self.client.sai_thrift_create_acl_entry(acl_attr_list)

        sys_logging("create acl entry = %d" %acl_entry_oid)
        assert(acl_entry_oid != SAI_NULL_OBJECT_ID )

        sys_logging(" step2: bind this ACL table to port  ")
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ecn=ecn_nonce,
                                pktlen=120)

        exp_pkt = simple_tcp_packet(eth_dst=dmac1,
                                    eth_src=router_mac,
                                    ip_dst=ip_addr1_subnet,
                                    ip_src='192.168.0.1',
                                    ip_id=105,
                                    ip_ttl=63,
                                    ip_ecn=ecn_nonce,
                                    pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet(1, str(pkt))
            self.ctc_verify_packets(exp_pkt, [0])

        finally:
            sys_logging("clear config")
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            status = self.client.sai_thrift_remove_acl_entry(acl_entry_oid)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_acl_table(acl_table_oid)
            assert (status == SAI_STATUS_SUCCESS)

            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_queue(queueId)
            self.client.sai_thrift_remove_wred_profile(wred_id)

#@group('Wred')
class scenario_04_ecn_ect1_test_packet_wred_ecn_ce_test(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECN_ACTION_ENABLE, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        port1 = port_list[0]
        port2 = port_list[1]

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        queue_index = 1

        #create Wred Id
        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        ecn_thrd = [1500,1300,150]
        wred_id = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("wred_id:", wred_id)

        #Create Queue Id
        queueId = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, queue_index, 0)
        sys_logging("queue_id:",queueId)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId, attr)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        ecn_nonce = 1
        ecn_ce = 3

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ecn=ecn_nonce,
                                pktlen=120)

        exp_pkt = simple_tcp_packet(eth_dst=dmac1,
                                    eth_src=router_mac,
                                    ip_dst=ip_addr1_subnet,
                                    ip_src='192.168.0.1',
                                    ip_id=105,
                                    ip_ttl=63,
                                    ip_ecn=ecn_ce,
                                    pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet(1, str(pkt))
            self.ctc_verify_packets(exp_pkt, [0])

        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_queue(queueId)
            self.client.sai_thrift_remove_wred_profile(wred_id)

@group('Wred')
class scenario_05_ipv4_ecn_ce_packet_action_copy_test(sai_base_test.ThriftInterfaceDataPlane):

    def runTest(self):

        switch_init(self.client)

        port1 = port_list[0]
        port2 = port_list[1]
        acl_attr_list = []

        vlan_id = 100
        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        sys_logging(" step1: basic environment ")

        # acl table info
        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]

        # acl key field
        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_IN_PORT,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ACL_IP_TYPE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

        attribute_value = sai_thrift_attribute_value_t(booldata=1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_FIELD_ECN,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

        # create acl table
        attribute_value = sai_thrift_attribute_value_t(s32=table_stage)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_STAGE,
                                            value=attribute_value)
        acl_attr_list.append(attribute)

        acl_table_bind_point_list = sai_thrift_s32_list_t(count=len(table_bind_point_list), s32list=table_bind_point_list)
        attribute_value = sai_thrift_attribute_value_t(s32list=acl_table_bind_point_list)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_TABLE_ATTR_ACL_BIND_POINT_TYPE_LIST,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

        acl_table_oid = self.client.sai_thrift_create_acl_table(acl_attr_list)

        sys_logging("create acl table = %d" %acl_table_oid)
        assert(acl_table_oid != SAI_NULL_OBJECT_ID )

        # entry info
        acl_attr_list = []
        entry_priority = 1
        admin_state = True
        ip_type = SAI_ACL_IP_TYPE_IPV4ANY
        ip_type_mask = -1
        ipv4_ecn = 3
        ipv4_ecn_mask = -1

        action = SAI_PACKET_ACTION_LOG

        #ACL table OID
        attribute_value = sai_thrift_attribute_value_t(oid=acl_table_oid)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_TABLE_ID,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

        #Priority
        attribute_value = sai_thrift_attribute_value_t(u32=entry_priority)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_PRIORITY,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

        # Admin State
        attribute_value = sai_thrift_attribute_value_t(booldata=admin_state)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ADMIN_STATE,
                                               value=attribute_value)
        acl_attr_list.append(attribute)

        # ip type
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(s32=ip_type), mask = sai_thrift_acl_mask_t(s32=ip_type_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

        # src ipv6
        attribute_value = sai_thrift_attribute_value_t(aclfield=sai_thrift_acl_field_data_t(enable = True, data = sai_thrift_acl_data_t(u8=ipv4_ecn), mask =sai_thrift_acl_mask_t(u8=ipv4_ecn_mask)))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_FIELD_ECN, value=attribute_value)
        acl_attr_list.append(attribute)

        #Packet action
        attribute_value = sai_thrift_attribute_value_t(aclaction=sai_thrift_acl_action_data_t(parameter = sai_thrift_acl_parameter_t(s32=action),
                                                                                              enable = True))
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION,
                                           value=attribute_value)
        acl_attr_list.append(attribute)

        # create entry entry
        acl_entry_oid = self.client.sai_thrift_create_acl_entry(acl_attr_list)

        sys_logging("create acl entry = %d" %acl_entry_oid)
        assert(acl_entry_oid != SAI_NULL_OBJECT_ID )

        sys_logging(" step2: bind this ACL table to port  ")
        attr_value = sai_thrift_attribute_value_t(oid=acl_table_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        macsa = '00:11:11:11:11:11'
        macda = '00:22:22:22:22:22'
        ipsa = "20.1.1.1"
        ipda = "30.1.1.1"
        ipv4_ecn_not_match = 0

        warmboot(self.client)
        try:

            sys_logging(" step3: get acl entry attr info  ")
            attr_list_ids = [SAI_ACL_ENTRY_ATTR_TABLE_ID, SAI_ACL_ENTRY_ATTR_PRIORITY, SAI_ACL_ENTRY_ATTR_ADMIN_STATE,
            SAI_ACL_ENTRY_ATTR_FIELD_ECN, SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE, SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION]

            # get acl entry attr
            attrs = self.client.sai_thrift_get_acl_entry_attribute(acl_entry_oid, attr_list_ids)
            assert (attrs.status == SAI_STATUS_SUCCESS)

            for a in attrs.attr_list:

                if a.id == SAI_ACL_ENTRY_ATTR_TABLE_ID:
                    sys_logging("get SAI_ACL_ENTRY_ATTR_TABLE_ID = %d" %a.value.oid)
                    assert(acl_table_oid == a.value.oid )

                if a.id == SAI_ACL_ENTRY_ATTR_PRIORITY:
                    sys_logging("get SAI_ACL_ENTRY_ATTR_PRIORITY = %d" %a.value.u32)
                    assert(entry_priority == a.value.u32 )

                if a.id == SAI_ACL_ENTRY_ATTR_ADMIN_STATE:
                    sys_logging("get SAI_ACL_ENTRY_ATTR_ADMIN_STATE = %d" %a.value.booldata)
                    assert(admin_state == a.value.booldata )

                if a.id == SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE:
                    sys_logging("get SAI_ACL_ENTRY_ATTR_FIELD_ACL_IP_TYPE = %s" %a.value.aclfield.data.s32)
                    assert(ip_type == a.value.aclfield.data.s32 )

                if a.id == SAI_ACL_ENTRY_ATTR_FIELD_ECN:
                    sys_logging("get SAI_ACL_ENTRY_ATTR_FIELD_ECN = %s" %a.value.aclfield.data.u8)
                    assert(ipv4_ecn == a.value.aclfield.data.u8 )

                if a.id == SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION:
                    sys_logging("get SAI_ACL_ENTRY_ATTR_ACTION_PACKET_ACTION = %d" %a.value.aclaction.parameter.s32)
                    assert(action == a.value.aclaction.parameter.s32 )

            sys_logging(" step4: send packet test ")

            pkt = simple_tcp_packet(eth_dst=macda,
                                    eth_src=macsa,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id,
                                    ip_src=ipsa,
                                    ip_dst=ipda,
                                    ip_ecn=ipv4_ecn,
                                    ip_id=101,
                                    ip_ttl=64)

            pkt1 = simple_tcp_packet(eth_dst=macda,
                                    eth_src=macsa,
                                    dl_vlan_enable=True,
                                    vlan_vid=vlan_id,
                                    ip_src=ipsa,
                                    ip_dst=ipda,
                                    ip_ecn=ipv4_ecn_not_match,
                                    ip_id=101,
                                    ip_ttl=64)

            self.client.sai_thrift_clear_cpu_packet_info()

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets(pkt, [1])

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError()

            self.ctc_send_packet(0, str(pkt1))
            self.ctc_verify_packets(pkt1, [1])

            ret = self.client.sai_thrift_get_cpu_packet_count()
            sys_logging ("receive rx packet %d" %ret.data.u16)
            if ret.data.u16 != 1:
                raise NotImplementedError()

            self.client.sai_thrift_clear_cpu_packet_info()

        finally:
            #pdb.set_trace()
            sys_logging("clear config")
            attr_value = sai_thrift_attribute_value_t(oid=SAI_NULL_OBJECT_ID)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_INGRESS_ACL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            status = self.client.sai_thrift_remove_acl_entry(acl_entry_oid)
            assert (status == SAI_STATUS_SUCCESS)
            status = self.client.sai_thrift_remove_acl_table(acl_table_oid)
            assert (status == SAI_STATUS_SUCCESS)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('Wred')
class scenario_06_ucast_packet_wred_drop(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        switch_init(self.client)

        #attr_value = sai_thrift_attribute_value_t(booldata=True)
        #attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_ECN_ACTION_ENABLE, value=attr_value)
        #self.client.sai_thrift_set_switch_attribute(attr)

        port1 = port_list[0]
        port2 = port_list[1]

        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''

        #create Wred Id
        color_en  = [1,1,1]
        min_thrd  = [0,0,0]
        max_thrd  = [32767,32767,32767]
        drop_prob = [100,100,100]
        ecn_thrd  = [1500,1300,150]
        wred_id   = sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob, ecn_thrd)
        sys_logging("wred_id:", wred_id)

        #Create Queue Id
        queueId0 = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, 0, 0)
        sys_logging("queue_id:",queueId0)
        assert (queueId0 != SAI_NULL_OBJECT_ID)

        queueId1 = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, 1, 0)
        sys_logging("queue_id:",queueId1)
        assert (queueId1 != SAI_NULL_OBJECT_ID)

        queueId2 = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, 2, 0)
        sys_logging("queue_id:",queueId2)
        assert (queueId2 != SAI_NULL_OBJECT_ID)

        queueId3 = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, 3, 0)
        sys_logging("queue_id:",queueId3)
        assert (queueId3 != SAI_NULL_OBJECT_ID)

        queueId4 = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, 4, 0)
        sys_logging("queue_id:",queueId4)
        assert (queueId4 != SAI_NULL_OBJECT_ID)

        queueId5 = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, 5, 0)
        sys_logging("queue_id:",queueId5)
        assert (queueId5 != SAI_NULL_OBJECT_ID)

        queueId6 = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, 6, 0)
        sys_logging("queue_id:",queueId6)
        assert (queueId6 != SAI_NULL_OBJECT_ID)

        queueId7 = sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_ALL, port2, 7, 0)
        sys_logging("queue_id:",queueId7)
        assert (queueId7 != SAI_NULL_OBJECT_ID)

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        status = self.client.sai_thrift_set_queue_attribute(queueId0, attr)
        assert (status == SAI_STATUS_SUCCESS)
        status = self.client.sai_thrift_set_queue_attribute(queueId1, attr)
        assert (status == SAI_STATUS_SUCCESS)
        status = self.client.sai_thrift_set_queue_attribute(queueId2, attr)
        assert (status == SAI_STATUS_SUCCESS)
        status = self.client.sai_thrift_set_queue_attribute(queueId3, attr)
        assert (status == SAI_STATUS_SUCCESS)
        status = self.client.sai_thrift_set_queue_attribute(queueId4, attr)
        assert (status == SAI_STATUS_SUCCESS)
        status = self.client.sai_thrift_set_queue_attribute(queueId5, attr)
        assert (status == SAI_STATUS_SUCCESS)
        status = self.client.sai_thrift_set_queue_attribute(queueId6, attr)
        assert (status == SAI_STATUS_SUCCESS)
        status = self.client.sai_thrift_set_queue_attribute(queueId7, attr)
        assert (status == SAI_STATUS_SUCCESS)

        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)

        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        ip_addr2 = '10.10.10.2'
        ip_addr1_subnet = '10.10.10.0'
        ip_mask1 = '255.255.255.0'
        dmac1 = '00:11:22:33:44:55'
        ecn_ect0 = 2
        ecn_ce   = 3

        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)
        #sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr2, dmac1)
        nhop1 = sai_thrift_create_nhop(self.client, addr_family, ip_addr1, rif_id1)
        #nhop2 = sai_thrift_create_nhop(self.client, addr_family, ip_addr2, rif_id2)

        status = sai_thrift_create_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1, packet_action = SAI_PACKET_ACTION_FORWARD)
        sys_logging("route create status = %d" %status)
        assert (status == SAI_STATUS_SUCCESS)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst=ip_addr1_subnet,
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_ecn=ecn_ect0,
                                pktlen=120)

        exp_pkt = simple_tcp_packet(eth_dst=dmac1,
                                    eth_src=router_mac,
                                    ip_dst=ip_addr1_subnet,
                                    ip_src='192.168.0.1',
                                    ip_id=105,
                                    ip_ttl=63,
                                    ip_ecn=ecn_ce,
                                    pktlen=120)

        warmboot(self.client)
        try:
            self.ctc_send_packet(1, str(pkt))
            #board
            #self.ctc_verify_no_packet(pkt, [0])
            #uml
            self.ctc_verify_packets(exp_pkt, [0])

        finally:
            sai_thrift_remove_route(self.client, vr_id, addr_family, ip_addr1_subnet, ip_mask1, nhop1)
            self.client.sai_thrift_remove_next_hop(nhop1)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_addr1, dmac1)

            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_queue(queueId0)
            self.client.sai_thrift_remove_queue(queueId1)
            self.client.sai_thrift_remove_queue(queueId2)
            self.client.sai_thrift_remove_queue(queueId3)
            self.client.sai_thrift_remove_queue(queueId4)
            self.client.sai_thrift_remove_queue(queueId5)
            self.client.sai_thrift_remove_queue(queueId6)
            self.client.sai_thrift_remove_queue(queueId7)
            self.client.sai_thrift_remove_wred_profile(wred_id)
