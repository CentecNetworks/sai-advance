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
Thrift SAI interface Policer tests
"""
import socket
from switch import *
import sai_base_test
import pdb

@group('Policer')
class PortRFC2697SrTCMBPSPoicer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC2697 SrTCM Poicer,verify policer attribute
        step1:create policer_id & binding port
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        
        warmboot(self.client)
        try:
            #set policer attr
            attr_value = sai_thrift_attribute_value_t(u64=200000)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)

            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    sys_logging("cbs: %d" %a.value.u64)
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.s32:
                        sys_logging("meter type error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_SR_TCM != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_BLIND != a.value.s32:
                        sys_logging("color source error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("green drop error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("yellow drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("red drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()                                             
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

@group('Policer')
class PortRFC2697SrTCMPPSPoicer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC2697 SrTCM Poicer,verify policer attribute
        step1:create policer_id & binding port
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        
        warmboot(self.client)
        try:
            #set policer attr
            attr_value = sai_thrift_attribute_value_t(u64=200000)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)

            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    sys_logging("cbs: %d" %a.value.u64)
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_PACKETS != a.value.s32:
                        sys_logging("meter type error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_SR_TCM != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_BLIND != a.value.s32:
                        sys_logging("color source error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("green drop error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("yellow drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("red drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()                                
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

@group('Policer')
class PortRFC2697SrTCMColorAwarePoicer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC2697 SrTCM Poicer,verify policer attribute
        step1:create policer_id & binding port
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        
        warmboot(self.client)
        try:
            #set policer attr
            attr_value = sai_thrift_attribute_value_t(u64=200000)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)

            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    sys_logging("cbs: %d" %a.value.u64)
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.s32:
                        sys_logging("meter type error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_SR_TCM != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_AWARE != a.value.s32:
                        sys_logging("color source error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("green drop error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("yellow drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("red drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()                                                
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

@group('Policer')
class PortRFC2697SrTCMColorDropPoicer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC2697 SrTCM Poicer,verify policer attribute
        step1:create policer_id & binding port
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 0, 0,
                                                    SAI_PACKET_ACTION_DROP, SAI_PACKET_ACTION_DROP, SAI_PACKET_ACTION_DROP, [1,1,1])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        
        warmboot(self.client)
        try:
            #set policer attr
            attr_value = sai_thrift_attribute_value_t(u64=200000)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)

            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    sys_logging("cbs: %d" %a.value.u64)
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.s32:
                        sys_logging("meter type error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_SR_TCM != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_BLIND != a.value.s32:
                        sys_logging("color source error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("green drop error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("yellow drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("red drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()                                               
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)


@group('Policer')
class PortRFC4115TrTCMColorBlindPoicer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC4115 TrTCM Poicer,verify policer attribute
        step1:create policer_id & binding port
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_TR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 200000, 4000,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        
        warmboot(self.client)
        try:
            #set policer attr
            attr_value = sai_thrift_attribute_value_t(u64=120000)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)

            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    sys_logging("cbs: %d" %a.value.u64)
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PIR:
                    sys_logging("pir: %d" %a.value.u64)
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PBS:
                    sys_logging("pbs: %d" %a.value.u64)
                    if 4000 != a.value.u64:
                        raise NotImplementedError()        
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.s32:
                        sys_logging("meter type error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_TR_TCM != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_BLIND != a.value.s32:
                        sys_logging("color source error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("green drop error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("yellow drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("red drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

@group('Policer')
class PortRFC4115TrTCMColorAwarePoicer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC4115 TrTCM Poicer,verify policer attribute
        step1:create policer_id & binding port
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_TR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    100000, 2000, 200000, 4000,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        
        warmboot(self.client)
        try:
            #set policer attr
            attr_value = sai_thrift_attribute_value_t(u64=120000)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)

            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    sys_logging("cbs: %d" %a.value.u64)
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PIR:
                    sys_logging("pir: %d" %a.value.u64)
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PBS:
                    sys_logging("pbs: %d" %a.value.u64)
                    if 4000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.s32:
                        sys_logging("meter type error!!! %d" %a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_TR_TCM != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_AWARE != a.value.s32:
                        sys_logging("color source error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("green drop error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("yellow drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("red drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()                                             
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

@group('Policer')
class PortRFC4115TrTCMColorDropPoicer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC4115 TrTCM Poicer,verify policer attribute
        step1:create policer_id & binding port
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_TR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 200000, 4000,
                                                    SAI_PACKET_ACTION_DROP, SAI_PACKET_ACTION_DROP, SAI_PACKET_ACTION_DROP, [1,1,1])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        
        warmboot(self.client)
        try:
            #set policer attr
            attr_value = sai_thrift_attribute_value_t(u64=120000)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)

            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    sys_logging("cbs: %d" %a.value.u64)
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PIR:
                    sys_logging("pir: %d" %a.value.u64)
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PBS:
                    sys_logging("pbs: %d" %a.value.u64)
                    if 4000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.s32:
                        sys_logging("meter type error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_TR_TCM != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_BLIND != a.value.s32:
                        sys_logging("color source error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("green drop error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("yellow drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("red drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()                                               
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

@group('Policer')
class PortStormCtlFlood(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Storm Contorl Poicer, verify policer attribute
        step1:create policer_id & binding port & as flood
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]
        port1 = port_list[1]

        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_STORM_CONTROL, 0,
                                                    100000, 0, 0, 0,
                                                    0, 0, 0, [0,0,0])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)

        #attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        #attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID, value=attr_value)
        #self.client.sai_thrift_set_port_attribute(port,attr)

        #attr_value = sai_thrift_attribute_value_t(oid=0)
        #attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID, value=attr_value)
        #self.client.sai_thrift_set_port_attribute(port,attr)

        #attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        #attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID, value=attr_value)
        #self.client.sai_thrift_set_port_attribute(port1,attr)
        #
        warmboot(self.client)
        try:
            #set policer attr
            attr_value = sai_thrift_attribute_value_t(u64=120000)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)

            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.s32:
                        sys_logging("meter type error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_STORM_CONTROL != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()                                          
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)

            #attr_value = sai_thrift_attribute_value_t(oid=0)
            #attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID, value=attr_value)
            #self.client.sai_thrift_set_port_attribute(port1,attr)

        
            self.client.sai_thrift_remove_policer(policer_id)

@group('Policer')
class PortStormCtlMcast(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Storm Contorl Poicer, verify policer attribute
        step1:create policer_id & binding port & as multicast
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_STORM_CONTROL, 0,
                                                    100000, 0, 0, 0,
                                                    0, 0, 0, [0,0,0])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        
        warmboot(self.client)
        try:
            #set policer attr
            attr_value = sai_thrift_attribute_value_t(u64=120000)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)

            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_PACKETS != a.value.s32:
                        sys_logging("meter type error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_STORM_CONTROL != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()                                          
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

@group('Policer')
class PortStormCtlBcast(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Storm Contorl Poicer, verify policer attribute
        step1:create policer_id & binding port & as broadcast
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_STORM_CONTROL, 0,
                                                    100000, 0, 0, 0,
                                                    0, 0, 0, [0,0,0])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        
        warmboot(self.client)
        try:
            #set policer attr
            attr_value = sai_thrift_attribute_value_t(u64=120000)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)

            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_PACKETS != a.value.s32:
                        sys_logging("meter type error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_STORM_CONTROL != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id) 

@group('Policer')
class PortRFC2697SrTCMPPSPoicerResetId(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC2697 SrTCM Poicer,verify policer attribute 
        step1:create policer_id1 & binding port
        step2:create policer_id2 & binding port
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id 1
        policer_id1 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        status = self.client.sai_thrift_set_port_attribute(port,attr)
        sys_logging('set attribute status = %d' %status)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        sys_logging('get attribute status = %d' %attrs.status)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_POLICER_ID:
                sys_logging("get port bind policer id = 0x%x" %a.value.oid)

        warmboot(self.client)
        try:
            #create policer id 2
            policer_id2 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_TR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    200000, 4000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,1,1])   
            #apply to port 
            
            attr_value = sai_thrift_attribute_value_t(oid=policer_id2)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)  
            sys_logging('set attribute status = %d' %status)

            attrs = self.client.sai_thrift_get_port_attribute(port)
            sys_logging('get attribute status = %d' %attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_POLICER_ID:
                    sys_logging("get port bind policer id = 0x%x" %a.value.oid)
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id1)
            self.client.sai_thrift_remove_policer(policer_id2)

@group('Policer')
class PortRFC2697SrTCMColorAwarePoicerStatsEn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC2697 SrTCM Poicer,verify policer attribute
        step1:create policer_id & binding port
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("Configure policer")
        #create policer id
        stats_en_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS]
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1], stats_en_list=stats_en_list)

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1,attr)
        
        #set policer attr
        attr_value = sai_thrift_attribute_value_t(u64=200000)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
        self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
        sys_logging("Configure fdb entry")
        vlan_id = 100
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
            
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=80)
                                
        warmboot(self.client)
        try:
            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    sys_logging("cbs: %d" %a.value.u64)
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.s32:
                        sys_logging("meter type error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_SR_TCM != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_AWARE != a.value.s32:
                        sys_logging("color source error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("green drop error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("yellow drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("red drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_ENABLE_COUNTER_LIST:
                    sys_logging ("set stats_en_list =  ", stats_en_list)
                    sys_logging ("get stats_en_list =  ", a.value.s32list.s32list)
                    if stats_en_list != a.value.s32list.s32list:
                        raise NotImplementedError()
                        
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            stats_get_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS, SAI_POLICER_STAT_GREEN_BYTES]
            counters_results = self.client.sai_thrift_get_policer_stats(policer_id,stats_get_list)
            sys_logging("green packets = %d " %(counters_results[0]))
            sys_logging("yellow packets = %d " %(counters_results[1]))
            sys_logging("red packets = %d " %(counters_results[2]))
            sys_logging("green bytes = %d " %(counters_results[3]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 0)
            assert (counters_results[2] == 0)
            assert (counters_results[3] == 84)
            
            
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1,attr)
            self.client.sai_thrift_remove_policer(policer_id)
            
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)
            
@group('Policer')
class PolicerStressTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Policer Stress Test
        step1:Create policer Id
        step2:verify 
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port_num = 32
        port = 0
        test_num = port_num*50
        policer_id = []
        #create policer id
        for i in range(test_num):
            policer_id_temp = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000+i*8, 2000+i*4, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
            sys_logging("policer_oid:0x%x"%policer_id_temp)
            policer_id.append(policer_id_temp)
            
        warmboot(self.client)
        try:
            
            for i in range(test_num):
                attr_value = sai_thrift_attribute_value_t(oid=policer_id[i])
                attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
                self.client.sai_thrift_set_port_attribute(port_list[port],attr)
                sys_logging("port[%d] bind policer_oid:0x%x" %(port, policer_id[i]))

                port += 1
                if port >= port_num:
                    port = 0
            
            port = 16
            for i in range(test_num):
                attr_value = sai_thrift_attribute_value_t(oid=policer_id[i])
                attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
                self.client.sai_thrift_set_port_attribute(port_list[port],attr)
                sys_logging("port[%d] bind policer_oid:0x%x" %(port, policer_id[i]))

                port += 1
                if port >= port_num:
                    port = 0
        finally:
            sys_logging("Clean Config")
            for i in range(port_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
                self.client.sai_thrift_set_port_attribute(port_list[i],attr)
            for i in range(test_num):
                self.client.sai_thrift_remove_policer(policer_id[i])

class SubPortPoicer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC4115 TrTCM Poicer,verify policer attribute
        step1:create policer_id & binding port
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_TR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 200000, 4000,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
                                                    
        policer_id2 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_TR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 200000, 4000,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
        #apply to port
        #attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        #attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        #self.client.sai_thrift_set_port_attribute(port,attr)
        
        #vpls config
        port1 = port
        port2 = port_list[2]
        
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label3 = 300
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        tunnel_id2 = sai_thrift_create_tunnel_mpls_l2vpn(self.client)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        rif_id3 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label1, pop_nums, None, rif_id3, packet_action)
        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)  
        
        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, policer_id = policer_id)
        
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, policer_id=policer_id2)
        
        
        
        warmboot(self.client)
        try:
            #set policer attr
            attr_value = sai_thrift_attribute_value_t(u64=120000)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID:
                    sys_logging("SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID = %x " %a.value.oid)
                    assert( policer_id == a.value.oid) 
                    
            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID:
                    sys_logging("SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID = %x " %a.value.oid)
                    assert( policer_id2 == a.value.oid) 

            #get policer attr
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    sys_logging("cbs: %d" %a.value.u64)
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PIR:
                    sys_logging("pir: %d" %a.value.u64)
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PBS:
                    sys_logging("pbs: %d" %a.value.u64)
                    if 4000 != a.value.u64:
                        raise NotImplementedError()        
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.s32:
                        sys_logging("meter type error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_TR_TCM != a.value.s32:
                        sys_logging("policer mode error!!! %d" % a.value.s32)
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_BLIND != a.value.s32:
                        sys_logging("color source error!!! %d" % a.value.s32)
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("green drop error!!! %d" % a.value.s32)
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        sys_logging("yellow drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.s32:
                        sys_logging("red drop error!!! %d" % a.value.s32)
                        raise NotImplementedError()
        finally:
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
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
            
            self.client.sai_thrift_remove_policer(policer_id)
            self.client.sai_thrift_remove_policer(policer_id2)


'''
class AclRFC2697SrTCMPPSPoicerResetId(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC2697 SrTCM Poicer,verify policer attribute 
        step1:create policer_id1 & binding acl
        step2:create policer_id2 & binding acl
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]
                

        table_stage = SAI_ACL_STAGE_INGRESS
        table_bind_point_list = [SAI_ACL_BIND_POINT_TYPE_PORT]
        addr_family = None
        action = SAI_PACKET_ACTION_DROP
        in_ports = None
        mac_src = '00:11:11:11:11:11'
        mac_dst = '00:22:22:22:22:22'
        mac_src_mask = None
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
            
        #create policer id 1
        policer_id1 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
        #apply to port
        attribute_value = sai_thrift_attribute_value_t(oid=policer_id1)
        attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER, value=attribute_value)
        status = self.client.sai_thrift_set_acl_entry_attribute(acl_entry_id, attribute)
        sys_logging('set attribute status = %d' %status)

        attrs = self.client.sai_thrift_get_acl_entry_attribute(acl_entry_id, [SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER])
        sys_logging('get attribute status = %d' %attrs.status)
        for a in attrs.attr_list:
            if a.id == SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER:
                sys_logging("get port bind policer id = 0x%x" %a.value.aclaction.parameter.oid)

        warmboot(self.client)
        try:
            #create policer id 2
            policer_id2 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    200000, 4000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,1,1])   
            #apply to port 
            
            attribute_value = sai_thrift_attribute_value_t(oid=policer_id2)
            attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER, value=attribute_value)
            status = self.client.sai_thrift_set_acl_entry_attribute(acl_entry_id, attribute)
            sys_logging('set attribute status = %d' %status)

            attrs = self.client.sai_thrift_get_acl_entry_attribute(acl_entry_id, [SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER])
            sys_logging('get attribute status = %d' %attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER:
                    sys_logging("get port bind policer id = 0x%x" %a.value.aclaction.parameter.oid)
        finally:
            attribute_value = sai_thrift_attribute_value_t(oid=0)
            attribute = sai_thrift_attribute_t(id=SAI_ACL_ENTRY_ATTR_ACTION_SET_POLICER, value=attribute_value)
            self.client.sai_thrift_set_acl_entry_attribute(acl_entry_id, attribute)
            self.client.sai_thrift_remove_policer(policer_id1)
            self.client.sai_thrift_remove_policer(policer_id2)
            status = self.client.sai_thrift_remove_acl_entry(acl_entry_id)
            status = self.client.sai_thrift_remove_acl_table(acl_table_id)
'''

class SubportAndTunnelportRFC2697SrTCMPPSPoicerResetId(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC4115 TrTCM Poicer,verify policer attribute
        step1:create policer_id & binding port
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id1 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_TR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 200000, 4000,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
        policer_id2 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_TR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    200000, 4000, 400000, 8000,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
        #vpls config
        port1 = port
        port2 = port_list[2]
        
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label3 = 300
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)  
        
        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, policer_id = policer_id1)
        #pdb.set_trace()
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, policer_id=policer_id2)
        
        #pdb.set_trace()
        
        warmboot(self.client)
        try:
            #set policer attr
            
            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID:
                    sys_logging("SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID = %x " %a.value.oid)
                    assert( policer_id1 == a.value.oid) 
                    
            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID:
                    sys_logging("SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID = %x " %a.value.oid)
                    assert( policer_id2 == a.value.oid) 

            policer_id3 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_TR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    150000, 2500, 250000, 4500,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
            #pdb.set_trace()
            bport_attr_value = sai_thrift_attribute_value_t(booldata=False)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)

            bport_attr_value = sai_thrift_attribute_value_t(oid=policer_id3)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)
            bport_attr_value = sai_thrift_attribute_value_t(oid=policer_id1)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID, value=bport_attr_value)
            
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)

            bport_attr_value = sai_thrift_attribute_value_t(booldata=True)
            bport_attr = sai_thrift_attribute_t(id=SAI_BRIDGE_PORT_ATTR_ADMIN_STATE, value=bport_attr_value)
            self.client.sai_thrift_set_bridge_port_attribute(tunnel_bport, bport_attr)
            self.client.sai_thrift_set_bridge_port_attribute(bport, bport_attr)

            attrs = self.client.sai_thrift_get_bridge_port_attribute(bport)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID:
                    sys_logging("SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID = %x " %a.value.oid)
                    assert( policer_id3 == a.value.oid) 
                    
            attrs = self.client.sai_thrift_get_bridge_port_attribute(tunnel_bport)
            for a in attrs.attr_list:
                if a.id == SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID:
                    sys_logging("SAI_BRIDGE_PORT_ATTR_SUB_TUNNEL_PORT_POLICER_ID = %x " %a.value.oid)
                    assert( policer_id1 == a.value.oid) 
            #pdb.set_trace()
                
        finally:
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            self.client.sai_thrift_remove_policer(policer_id1)
            self.client.sai_thrift_remove_policer(policer_id2)
            self.client.sai_thrift_remove_policer(policer_id3)

class PortBindModeNotMatchPolicer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Storm Contorl Poicer, verify policer attribute
        step1:create policer_id & binding port & as multicast
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id1 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
                                                    
        policer_id2 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_STORM_CONTROL, 0,
                                                    100000, 0, 0, 0,
                                                    0, 0, 0, [0,0,0])

        #apply to port
        
        
        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(oid=policer_id1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            status = self.client.sai_thrift_set_port_attribute(port,attr)
            sys_logging('set mode not match attribute status = %d' %status)
            
            attr_value = sai_thrift_attribute_value_t(oid=policer_id2)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            status = self.client.sai_thrift_set_port_attribute(port,attr) 
            sys_logging('set mode not match attribute status = %d' %status)

            
            attr_value = sai_thrift_attribute_value_t(oid=policer_id2)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            status = self.client.sai_thrift_set_port_attribute(port,attr)
            sys_logging('set port attribute status = %d' %status)

            attr_value = sai_thrift_attribute_value_t(oid=policer_id1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            status = self.client.sai_thrift_set_port_attribute(port,attr) 
            sys_logging('set port attribute status = %d' %status)

            
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            
            self.client.sai_thrift_remove_policer(policer_id1)
            self.client.sai_thrift_remove_policer(policer_id2)

class PortBindThreeTypeStormctlPolicer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Storm Contorl Poicer, verify policer attribute
        step1:create policer_id & binding port & as multicast
        step2:verify policer attr
        step3:clean up
        """
        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id1 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_STORM_CONTROL, 0,
                                                    100000, 0, 0, 0,
                                                    0, 0, 0, [0,0,0])
                                                    
        policer_id2 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_STORM_CONTROL, 0,
                                                    150000, 0, 0, 0,
                                                    0, 0, 0, [0,0,0])
                                                    
        policer_id3 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_STORM_CONTROL, 0,
                                                    200000, 0, 0, 0,
                                                    0, 0, 0, [0,0,0])
        
        warmboot(self.client)
        try:
            attr_value = sai_thrift_attribute_value_t(oid=policer_id1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            status = self.client.sai_thrift_set_port_attribute(port,attr)
            sys_logging('set port attribute status = %d' %status)
            
            attr_value = sai_thrift_attribute_value_t(oid=policer_id1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID, value=attr_value)
            status = self.client.sai_thrift_set_port_attribute(port,attr)
            sys_logging('set port attribute status = %d' %status)

            
            attr_value = sai_thrift_attribute_value_t(oid=policer_id1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            status = self.client.sai_thrift_set_port_attribute(port,attr)
            sys_logging('set port attribute status = %d' %status)

            attrs = self.client.sai_thrift_get_port_attribute(port)
            sys_logging('get attribute status = %d' %attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("get port multicast storm control policer id = 0x%x" %a.value.oid)
                    assert(a.value.oid==policer_id1)
                if a.id == SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID:
                    sys_logging("get port flood storm control policer id = 0x%x" %a.value.oid)
                    assert(a.value.oid==policer_id1)
                if a.id == SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("get port broadcast storm control policer id = 0x%x" %a.value.oid)
                    assert(a.value.oid==policer_id1)
                
            
            attr_value = sai_thrift_attribute_value_t(oid=policer_id2)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            status = self.client.sai_thrift_set_port_attribute(port,attr)
            sys_logging('set port attribute status = %d' %status)

            attr_value = sai_thrift_attribute_value_t(oid=policer_id3)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            status = self.client.sai_thrift_set_port_attribute(port,attr)
            sys_logging('set port attribute status = %d' %status)

            attrs = self.client.sai_thrift_get_port_attribute(port)
            sys_logging('get attribute status = %d' %attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("get port multicast storm control policer id = 0x%x" %a.value.oid)
                    assert(a.value.oid==policer_id3)
                if a.id == SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID:
                    sys_logging("get port flood storm control policer id = 0x%x" %a.value.oid)
                    assert(a.value.oid==policer_id1)
                if a.id == SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("get port broadcast storm control policer id = 0x%x" %a.value.oid)
                    assert(a.value.oid==policer_id1)

            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            
            attrs = self.client.sai_thrift_get_port_attribute(port)
            sys_logging('get attribute status = %d' %attrs.status)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_MULTICAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("get port multicast storm control policer id = 0x%x" %a.value.oid)
                    assert(a.value.oid==SAI_NULL_OBJECT_ID)
                if a.id == SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID:
                    sys_logging("get port flood storm control policer id = 0x%x" %a.value.oid)
                    assert(a.value.oid==SAI_NULL_OBJECT_ID)
                if a.id == SAI_PORT_ATTR_BROADCAST_STORM_CONTROL_POLICER_ID:
                    sys_logging("get port broadcast storm control policer id = 0x%x" %a.value.oid)
                    assert(a.value.oid==SAI_NULL_OBJECT_ID)
        finally:
            
            self.client.sai_thrift_remove_policer(policer_id1)
            self.client.sai_thrift_remove_policer(policer_id2)
            self.client.sai_thrift_remove_policer(policer_id3)

            
class fun_01_create_policer_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)
        
        #create policer id
        policer_id1 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 50000, 3000,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
        policer_id2 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_STORM_CONTROL, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    100000, 0, 0, 0,
                                                    0, 0, 0, [0,0,1])
        try:
            sys_logging('create policer_id1 = 0x%x' %policer_id1) 
            assert(policer_id1%0x100000000==0x12)

            sys_logging('create policer_id2 = 0x%x' %policer_id2) 
            assert(policer_id2%0x100000000==0x12)
        finally:

            self.client.sai_thrift_remove_policer(policer_id1)
            self.client.sai_thrift_remove_policer(policer_id2)

class fun_02_remove_policer_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_STORM_CONTROL, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    100000, 0, 0, 0,
                                                    0, 0, 0, [1,1,1])
        sys_logging('create policer_id = 0x%x' %policer_id) 
        attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
        sys_logging('get policer attribute status = %d' %attrs.status)
        try:
            status = self.client.sai_thrift_remove_policer(policer_id)
            sys_logging('remove policer status = %d' %status)
            assert(status == SAI_STATUS_SUCCESS)
            
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")
            
class fun_03_remove_no_exist_policer_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_STORM_CONTROL, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    100000, 0, 0, 0,
                                                    0, 0, 0, [1,1,1])
        status = self.client.sai_thrift_remove_policer(policer_id)
        sys_logging('remove policer status = %d' %status)
        try:
            status = self.client.sai_thrift_remove_policer(policer_id)
            sys_logging('remove policer status = %d' %status)
            assert(status == SAI_STATUS_ITEM_NOT_FOUND)

        finally:
            sys_logging("======clean up======")            

class fun_04_remove_bind_port_policer_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)
        
        port = port_list[0]
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    100000, 0, 0, 0,
                                                    0, 0, 0, [1,1,1])
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        try:
            status = self.client.sai_thrift_remove_policer(policer_id)
            sys_logging('remove policer status = %d' %status)
            assert(status == SAI_STATUS_OBJECT_IN_USE)
            
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

class fun_05_remove_bind_bridge_port_policer_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id1 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_TR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 200000, 4000,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
        policer_id2 = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_TR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    200000, 4000, 400000, 8000,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
        #vpls config
        port1 = port
        port2 = port_list[2]
        vlan_id = 20
        v4_enabled = 1
        v6_enabled = 1
        mac = ''
        ip_mask = '255.255.255.0'
        ip_da = '5.5.5.2'
        dmac = '00:55:55:55:55:55'
        mac1 = '00:00:00:01:01:01'
        mac2 = '00:00:00:02:02:02'

        label1 = 100
        label2 = 200
        label3 = 300
        label_list1 = [(label1<<12) | 64]
        label_list2 = [(label2<<12) | 32]
        pop_nums = 1
        packet_action = SAI_PACKET_ACTION_FORWARD

        bridge_id = sai_thrift_create_bridge(self.client, SAI_BRIDGE_TYPE_1D)

        tunnel_id1= sai_thrift_create_tunnel_mpls_l2vpn(self.client, decap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, encap_pw_mode=SAI_TUNNEL_MPLS_PW_MODE_TAGGED, decap_cw_en=False, encap_cw_en=False, encap_ttl_val=0, encap_tagged_vlan=30)
        
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)

        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_MPLS_ROUTER, 0, 0, v4_enabled, v6_enabled, mac, dot1d_bridge_id=bridge_id)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        
        sai_thrift_create_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
        next_hop = sai_thrift_create_mpls_nhop(self.client, addr_family, ip_da, rif_id1, label_list1)
        next_hop1 = sai_thrift_create_tunnel_mpls_l2vpn_nhop(self.client, tunnel_id1, label_list2, next_level_nhop_oid=next_hop)

        sai_thrift_create_inseg_entry(self.client, label2, pop_nums, None, rif_id2, packet_action, tunnel_id=tunnel_id1)  
        
        bport = sai_thrift_create_bridge_sub_port(self.client, port2, bridge_id, vlan_id, policer_id = policer_id1)
        tunnel_bport = sai_thrift_create_bridge_tunnel_port(self.client, tunnel_id=tunnel_id1, bridge_id=bridge_id, policer_id=policer_id2)
        
        warmboot(self.client)
        try:
            status = self.client.sai_thrift_remove_policer(policer_id1)
            sys_logging('remove policer status = %d' %status)
            assert(status == SAI_STATUS_OBJECT_IN_USE)
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id1)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            

            status = self.client.sai_thrift_remove_policer(policer_id2)
            sys_logging('remove policer status = %d' %status)
            assert(status == SAI_STATUS_OBJECT_IN_USE)
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id2)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
        finally:
            sai_thrift_remove_bridge_sub_port(self.client, bport, port2)
            self.client.sai_thrift_remove_bridge_port(tunnel_bport)
            mpls2 = sai_thrift_inseg_entry_t(label2) 
            self.client.sai_thrift_remove_inseg_entry(mpls2)  

            self.client.sai_thrift_remove_next_hop(next_hop1)
            self.client.sai_thrift_remove_next_hop(next_hop)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id1, ip_da, dmac)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_tunnel(tunnel_id1)
            self.client.sai_thrift_remove_bridge(bridge_id)
            
            self.client.sai_thrift_remove_policer(policer_id1)
            self.client.sai_thrift_remove_policer(policer_id2)

class fun_06_set_policer_attribute_cir_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        cir = 100000
        cbs = 2000
        pir = 200000
        pbs = 4000

        cir_new = 150000
        port = port_list[0]
        pkt_action = SAI_PACKET_ACTION_FORWARD
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    cir, cbs, pir, pbs,
                                                    pkt_action, pkt_action, pkt_action, [1,1,1])
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)

        attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
        sys_logging('get policer attribute status = %d' %attrs.status)
        assert(attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_POLICER_ATTR_CIR:
                sys_logging("cir: %d" %a.value.u64)

        try:
            attr_value = sai_thrift_attribute_value_t(u64=cir_new)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if cir_new != a.value.u64:
                        raise NotImplementedError()

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

class fun_07_set_policer_attribute_cbs_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        cir = 100000
        cbs = 2000
        pir = 200000
        pbs = 4000

        cbs_new = 3000
        port = port_list[0]
        pkt_action = SAI_PACKET_ACTION_FORWARD
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    cir, cbs, pir, pbs,
                                                    pkt_action, pkt_action, pkt_action, [1,1,1])
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)

        attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
        sys_logging('get policer attribute status = %d' %attrs.status)
        assert(attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_POLICER_ATTR_CBS:
                sys_logging("cbs: %d" %a.value.u64)

        try:
            attr_value = sai_thrift_attribute_value_t(u64=cbs_new)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CBS, value=attr_value)
            
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CBS:
                    sys_logging("cbs: %d" %a.value.u64)
                    if cbs_new != a.value.u64:
                        raise NotImplementedError()

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

class fun_08_set_policer_attribute_pir_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        cir = 100000
        cbs = 2000
        pir = 200000
        pbs = 4000

        pir_new = 300000
        port = port_list[0]
        pkt_action = SAI_PACKET_ACTION_FORWARD
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    cir, cbs, pir, pbs,
                                                    pkt_action, pkt_action, pkt_action, [1,1,1])
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)

        attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
        sys_logging('get policer attribute status = %d' %attrs.status)
        assert(attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_POLICER_ATTR_PIR:
                sys_logging("pir: %d" %a.value.u64)

        try:
            attr_value = sai_thrift_attribute_value_t(u64=pir_new)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_PIR, value=attr_value)
            
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_PIR:
                    sys_logging("pir: %d" %a.value.u64)
                    if pir_new != a.value.u64:
                        raise NotImplementedError()

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

class fun_09_set_policer_attribute_pbs_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        cir = 100000
        cbs = 2000
        pir = 200000
        pbs = 4000

        pbs_new = 4500
        port = port_list[0]
        pkt_action = SAI_PACKET_ACTION_FORWARD
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    cir, cbs, pir, pbs,
                                                    pkt_action, pkt_action, pkt_action, [1,1,1])
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)

        attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
        sys_logging('get policer attribute status = %d' %attrs.status)
        assert(attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_POLICER_ATTR_PBS:
                sys_logging("pbs: %d" %a.value.u64)

        try:
            attr_value = sai_thrift_attribute_value_t(u64=pbs_new)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_PBS, value=attr_value)
            
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_PBS:
                    sys_logging("pbs: %d" %a.value.u64)
                    if pbs_new != a.value.u64:
                        raise NotImplementedError()

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)


class fun_10_set_policer_attribute_green_pkt_action_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        cir = 100000
        cbs = 2000
        pir = 200000
        pbs = 4000

        pkt_action_new = SAI_PACKET_ACTION_DROP
        port = port_list[0]
        pkt_action = SAI_PACKET_ACTION_FORWARD
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    cir, cbs, pir, pbs,
                                                    pkt_action, pkt_action, pkt_action, [1,1,1])
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)

        attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
        sys_logging('get policer attribute status = %d' %attrs.status)
        assert(attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                #sys_logging("pbs: %d" %a.value.s32)
                print 'green packet action :',
                print a.value.s32

        try:
            attr_value = sai_thrift_attribute_value_t(s32=pkt_action_new)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_GREEN_PACKET_ACTION, value=attr_value)
            
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    #sys_logging("pbs: %d" %a.value.s32)
                    print 'green packet action :',
                    print a.value.s32
                    if pkt_action_new != a.value.s32:
                        raise NotImplementedError()

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

class fun_11_set_policer_attribute_yellow_pkt_action_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        cir = 100000
        cbs = 2000
        pir = 200000
        pbs = 4000

        pkt_action_new = SAI_PACKET_ACTION_FORWARD
        port = port_list[0]
        pkt_action = SAI_PACKET_ACTION_DROP
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    cir, cbs, pir, pbs,
                                                    pkt_action, pkt_action, pkt_action, [1,1,1])
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)

        attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
        sys_logging('get policer attribute status = %d' %attrs.status)
        assert(attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                #sys_logging("pbs: %d" %a.value.s32)
                print 'yellow packet action :',
                print a.value.s32

        try:
            attr_value = sai_thrift_attribute_value_t(s32=pkt_action_new)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_YELLOW_PACKET_ACTION, value=attr_value)
            
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    #sys_logging("pbs: %d" %a.value.s32)
                    print 'yellow packet action :',
                    print a.value.s32
                    if pkt_action_new != a.value.s32:
                        raise NotImplementedError()

        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

class fun_12_set_policer_attribute_red_pkt_action_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)

        cir = 100000
        cbs = 2000
        pir = 200000
        pbs = 4000

        pkt_action_new = SAI_PACKET_ACTION_FORWARD
        port = port_list[0]
        pkt_action = SAI_PACKET_ACTION_DROP
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    cir, cbs, pir, pbs,
                                                    pkt_action, pkt_action, pkt_action, [1,1,1])
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)

        attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
        sys_logging('get policer attribute status = %d' %attrs.status)
        assert(attrs.status == SAI_STATUS_SUCCESS)
        for a in attrs.attr_list:
            if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                #sys_logging("pbs: %d" %a.value.s32)
                print 'yellow packet action :',
                print a.value.s32

        try:
            attr_value = sai_thrift_attribute_value_t(s32=pkt_action_new)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_RED_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    #sys_logging("pbs: %d" %a.value.s32)
                    print 'yellow packet action :',
                    print a.value.s32
                    if pkt_action_new != a.value.s32:
                        raise NotImplementedError()
                        
            attr_value = sai_thrift_attribute_value_t(s32=pkt_action)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_RED_PACKET_ACTION, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            sys_logging('get policer attribute status = %d' %attrs.status)
            assert(attrs.status == SAI_STATUS_SUCCESS)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    #sys_logging("pbs: %d" %a.value.s32)
                    print 'yellow packet action :',
                    print a.value.s32
                    if pkt_action != a.value.s32:
                        raise NotImplementedError()
        finally:
            sys_logging("======clean up======")
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)

class fun_13_set_policer_attribute_enable_counter_list_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("Configure policer")
        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1,attr)
                                
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_ENABLE_COUNTER_LIST:
                    print "get stats_en_list =  ",
                    print a.value.s32list.s32list
                    if [] != a.value.s32list.s32list:
                        raise NotImplementedError()
            #pdb.set_trace()
            stats_en_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS]
            attr_value_list = sai_thrift_s32_list_t(count=len(stats_en_list), s32list=stats_en_list)
            attr_value = sai_thrift_attribute_value_t(s32list=attr_value_list)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_ENABLE_COUNTER_LIST, value=attr_value)
            self.client.sai_thrift_set_policer_attribute(policer_id,attr)           
            
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_ENABLE_COUNTER_LIST:
                    print "get stats_en_list =  ",
                    print a.value.s32list.s32list
                    if stats_en_list != a.value.s32list.s32list:
                        raise NotImplementedError()
                        
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1,attr)
            self.client.sai_thrift_remove_policer(policer_id)


class fun_14_get_policer_default_attribute_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)
        port = port_list[0]
        #create policer id
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, None,
                                                    0, 0, 0, 0,
                                                    0, 0, 0, [0,0,0])
                                                    
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        #pdb.set_trace()
        try:
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_CIR:
                    sys_logging("cir: %d" %a.value.u64)
                    if 0 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    sys_logging("cbs: %d" %a.value.u64)
                    if 0 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PIR:
                    sys_logging("pir: %d" %a.value.u64)
                    if 0 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PBS:
                    sys_logging("pbs: %d" %a.value.u64)
                    if 0 != a.value.u64:
                        raise NotImplementedError()        
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    sys_logging("meter type = %d" % a.value.s32)
                    if SAI_METER_TYPE_BYTES != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    sys_logging("policer mode = %d" % a.value.s32)
                    if SAI_POLICER_MODE_SR_TCM != a.value.s32:
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    sys_logging("color source = %d" % a.value.s32)
                    if SAI_POLICER_COLOR_SOURCE_AWARE != a.value.s32:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    sys_logging("green packet action = %d" % a.value.s32)
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    sys_logging("yellow packet action = %d" % a.value.s32)
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    sys_logging("red packet action = %d" % a.value.s32)
                    if SAI_PACKET_ACTION_FORWARD != a.value.s32:
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id)


class fun_15_get_policer_green_pkt_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("Configure policer")
        #create policer id
        stats_en_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS]
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1], stats_en_list=stats_en_list)

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1,attr)
        
        #set policer attr
        attr_value = sai_thrift_attribute_value_t(u64=200000)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
        self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
        sys_logging("Configure fdb entry")
        vlan_id = 100
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
            
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=80)
                                
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_ENABLE_COUNTER_LIST:
                    #sys_logging ("set stats_en_list =  ", stats_en_list)
                    print "set stats_en_list =  ",
                    print stats_en_list
                    print "get stats_en_list =  ",
                    print a.value.s32list.s32list
                    #sys_logging ("get stats_en_list =  ", a.value.s32list.s32list)
                    if stats_en_list != a.value.s32list.s32list:
                        raise NotImplementedError()
                        
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            stats_get_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS, SAI_POLICER_STAT_GREEN_BYTES]
            counters_results = self.client.sai_thrift_get_policer_stats(policer_id,stats_get_list)
            sys_logging("green packets = %d " %(counters_results[0]))
            sys_logging("yellow packets = %d " %(counters_results[1]))
            sys_logging("red packets = %d " %(counters_results[2]))
            sys_logging("green bytes = %d " %(counters_results[3]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 0)
            assert (counters_results[2] == 0)
            assert (counters_results[3] == 84)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            stats_get_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS, SAI_POLICER_STAT_GREEN_BYTES]
            counters_results = self.client.sai_thrift_get_policer_stats(policer_id,stats_get_list)
            sys_logging("green packets = %d " %(counters_results[0]))
            sys_logging("yellow packets = %d " %(counters_results[1]))
            sys_logging("red packets = %d " %(counters_results[2]))
            sys_logging("green bytes = %d " %(counters_results[3]))
            assert (counters_results[0] == 2)
            assert (counters_results[1] == 0)
            assert (counters_results[2] == 0)
            assert (counters_results[3] == 168)
            
            
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1,attr)
            self.client.sai_thrift_remove_policer(policer_id)
            
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class fun_16_get_policer_green_pkt_stats_ext_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        mode1 = SAI_STATS_MODE_READ
        mode2 = SAI_STATS_MODE_READ_AND_CLEAR
        
        sys_logging("Configure policer")
        #create policer id
        stats_en_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS]
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1], stats_en_list=stats_en_list)

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1,attr)
        
        #set policer attr
        attr_value = sai_thrift_attribute_value_t(u64=200000)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
        self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
        sys_logging("Configure fdb entry")
        vlan_id = 100
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
            
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=80)
                                
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_ENABLE_COUNTER_LIST:
                    print "set stats_en_list =  ",
                    print stats_en_list
                    print "get stats_en_list =  ",
                    print a.value.s32list.s32list
                    if stats_en_list != a.value.s32list.s32list:
                        raise NotImplementedError()
                        
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            stats_get_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS, SAI_POLICER_STAT_GREEN_BYTES]
            counters_results = self.client.sai_thrift_get_policer_stats_ext(policer_id,stats_get_list,mode1)
            sys_logging("green packets = %d " %(counters_results[0]))
            sys_logging("yellow packets = %d " %(counters_results[1]))
            sys_logging("red packets = %d " %(counters_results[2]))
            sys_logging("green bytes = %d " %(counters_results[3]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 0)
            assert (counters_results[2] == 0)
            assert (counters_results[3] == 84)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            stats_get_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS, SAI_POLICER_STAT_GREEN_BYTES]
            counters_results = self.client.sai_thrift_get_policer_stats_ext(policer_id,stats_get_list,mode2)
            sys_logging("green packets = %d " %(counters_results[0]))
            sys_logging("yellow packets = %d " %(counters_results[1]))
            sys_logging("red packets = %d " %(counters_results[2]))
            sys_logging("green bytes = %d " %(counters_results[3]))
            assert (counters_results[0] == 2)
            assert (counters_results[1] == 0)
            assert (counters_results[2] == 0)
            assert (counters_results[3] == 168)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            stats_get_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS, SAI_POLICER_STAT_GREEN_BYTES]
            counters_results = self.client.sai_thrift_get_policer_stats_ext(policer_id,stats_get_list,mode2)
            sys_logging("green packets = %d " %(counters_results[0]))
            sys_logging("yellow packets = %d " %(counters_results[1]))
            sys_logging("red packets = %d " %(counters_results[2]))
            sys_logging("green bytes = %d " %(counters_results[3]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 0)
            assert (counters_results[2] == 0)
            assert (counters_results[3] == 84)
            
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1,attr)
            self.client.sai_thrift_remove_policer(policer_id)
            
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

class fun_17_clear_policer_green_pkt_stats_fn(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):

        sys_logging("start test")
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]
        
        sys_logging("Configure policer")
        #create policer id
        stats_en_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS]
        policer_id = sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1], stats_en_list=stats_en_list)

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1,attr)
        
        #set policer attr
        attr_value = sai_thrift_attribute_value_t(u64=200000)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
        self.client.sai_thrift_set_policer_attribute(policer_id,attr)
            
        sys_logging("Configure fdb entry")
        vlan_id = 100
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
            
        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=101,
                                ip_ttl=64,
                                pktlen=80)
                                
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_policer_attribute(policer_id)
            for a in attrs.attr_list:
                if a.id == SAI_POLICER_ATTR_ENABLE_COUNTER_LIST:
                    #sys_logging ("set stats_en_list =  ", stats_en_list)
                    print "set stats_en_list =  ",
                    print stats_en_list
                    print "get stats_en_list =  ",
                    print a.value.s32list.s32list
                    #sys_logging ("get stats_en_list =  ", a.value.s32list.s32list)
                    if stats_en_list != a.value.s32list.s32list:
                        raise NotImplementedError()
                        
            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            stats_get_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS, SAI_POLICER_STAT_GREEN_BYTES]
            counters_results = self.client.sai_thrift_get_policer_stats(policer_id,stats_get_list)
            sys_logging("green packets = %d " %(counters_results[0]))
            sys_logging("yellow packets = %d " %(counters_results[1]))
            sys_logging("red packets = %d " %(counters_results[2]))
            sys_logging("green bytes = %d " %(counters_results[3]))
            assert (counters_results[0] == 1)
            assert (counters_results[1] == 0)
            assert (counters_results[2] == 0)
            assert (counters_results[3] == 84)

            self.ctc_send_packet(0, str(pkt))
            self.ctc_verify_packets( str(pkt), [1], 1)
            
            stats_get_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS, SAI_POLICER_STAT_GREEN_BYTES]
            counters_results = self.client.sai_thrift_get_policer_stats(policer_id,stats_get_list)
            sys_logging("green packets = %d " %(counters_results[0]))
            sys_logging("yellow packets = %d " %(counters_results[1]))
            sys_logging("red packets = %d " %(counters_results[2]))
            sys_logging("green bytes = %d " %(counters_results[3]))
            assert (counters_results[0] == 2)
            assert (counters_results[1] == 0)
            assert (counters_results[2] == 0)
            assert (counters_results[3] == 168)

            stats_clear_list = [SAI_POLICER_STAT_PACKETS]
            self.client.sai_thrift_clear_policer_stats(policer_id,stats_clear_list)

            stats_get_list = [SAI_POLICER_STAT_GREEN_PACKETS, SAI_POLICER_STAT_YELLOW_PACKETS, SAI_POLICER_STAT_RED_PACKETS, SAI_POLICER_STAT_GREEN_BYTES]
            counters_results = self.client.sai_thrift_get_policer_stats(policer_id,stats_get_list)
            sys_logging("green packets = %d " %(counters_results[0]))
            sys_logging("yellow packets = %d " %(counters_results[1]))
            sys_logging("red packets = %d " %(counters_results[2]))
            sys_logging("green bytes = %d " %(counters_results[3]))
            assert (counters_results[0] == 0)
            assert (counters_results[1] == 0)
            assert (counters_results[2] == 0)
            assert (counters_results[3] == 0)
            
            
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1,attr)
            self.client.sai_thrift_remove_policer(policer_id)
            
            sai_thrift_delete_fdb(self.client, vlan_oid, mac1, port1)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            
            attr_value = sai_thrift_attribute_value_t(u16=1)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PORT_VLAN_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)


