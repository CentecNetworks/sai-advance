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
Thrift SAI interface QoS tests
"""
import socket
from switch import *
import sai_base_test

def _sai_thrift_qos_create_policer(client,
                                   meter_type, mode, color_source, 
                                   cir, cbs, pir, pbs, 
                                   green_act, yellow_act, red_act, act_valid = []):
        attr_list = []

        #set meter type
        attr_value = sai_thrift_attribute_value_t(s32=meter_type)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_METER_TYPE, value=attr_value)
        attr_list.append(attr)

        #set mode
        attr_value = sai_thrift_attribute_value_t(s32=mode)
        attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_MODE, value=attr_value)
        attr_list.append(attr)

        #set color source
        if SAI_POLICER_MODE_STORM_CONTROL != mode:  
            attr_value = sai_thrift_attribute_value_t(s32=color_source)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_COLOR_SOURCE, value=attr_value)
            attr_list.append(attr)

        #set cir
        if cir != 0:
            attr_value = sai_thrift_attribute_value_t(u64=cir)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CIR, value=attr_value)
            attr_list.append(attr)

        #set cbs
        if cbs != 0:
            attr_value = sai_thrift_attribute_value_t(u64=cbs)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_CBS, value=attr_value)
            attr_list.append(attr)

        #set pir
        if pir != 0:
            attr_value = sai_thrift_attribute_value_t(u64=pir)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_PIR, value=attr_value)
            attr_list.append(attr)

        #set pbs
        if pbs != 0:
            attr_value = sai_thrift_attribute_value_t(u64=pbs)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_PBS, value=attr_value)
            attr_list.append(attr)    

        #set green action
        if act_valid[0]:
            attr_value = sai_thrift_attribute_value_t(u64=green_act)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_GREEN_PACKET_ACTION, value=attr_value)
            attr_list.append(attr)

        #set yellow action
        if act_valid[1]:
            attr_value = sai_thrift_attribute_value_t(u64=yellow_act)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_YELLOW_PACKET_ACTION, value=attr_value)
            attr_list.append(attr)

        #set red action
        if act_valid[2]:
            attr_value = sai_thrift_attribute_value_t(u64=red_act)
            attr = sai_thrift_attribute_t(id=SAI_POLICER_ATTR_RED_PACKET_ACTION, value=attr_value)
            attr_list.append(attr)

        #create policer id
        return client.sai_thrift_create_policer(attr_list)

@group('Policer')
class PortRFC2697SrTCMBPSPoicer(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        RFC2697 SrTCM Poicer,verify policer attribute
        step1:create policer_id & binding port
        step2:verify policer attr
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
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
                    print "cir: %d" %a.value.u64
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    print "cbs: %d" %a.value.u64
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.u32:
                        print "meter type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_SR_TCM != a.value.u32:
                        print "policer mode error!!! %d" % a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_BLIND != a.value.u32:
                        print "color source error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.u32:
                        print "green drop error!!! %d" % a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.u32:
                        print "yellow drop error!!! %d" % a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.u32:
                        print "red drop error!!! %d" % a.value.u32
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
        print "start test"
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
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
                    print "cir: %d" %a.value.u64
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    print "cbs: %d" %a.value.u64
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_PACKETS != a.value.u32:
                        print "meter type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_SR_TCM != a.value.u32:
                        print "policer mode error!!! %d" % a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_BLIND != a.value.u32:
                        print "color source error!!! %d" % a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.u32:
                        print "green drop error!!! %d" % a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.u32:
                        print "yellow drop error!!! %d" % a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.u32:
                        print "red drop error!!! %d" % a.value.u32
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
        print "start test"
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
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
                    print "cir: %d" %a.value.u64
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    print "cbs: %d" %a.value.u64
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.u32:
                        print "meter type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_SR_TCM != a.value.u32:
                        print "policer mode error!!! %d" % a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_AWARE != a.value.u32:
                        print "color source error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.u32:
                        print "green drop error!!! %d" % a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.u32:
                        print "yellow drop error!!! %d" % a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.u32:
                        print "red drop error!!! %d" % a.value.u32
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
        print "start test"
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
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
                    print "cir: %d" %a.value.u64
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    print "cbs: %d" %a.value.u64
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.u32:
                        print "meter type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_SR_TCM != a.value.u32:
                        print "policer mode error!!! %d" % a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_BLIND != a.value.u32:
                        print "color source error!!! %d" % a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.u32:
                        print "green drop error!!! %d" % a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.u32:
                        print "yellow drop error!!! %d" % a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.u32:
                        print "red drop error!!! %d" % a.value.u32
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
        print "start test"
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
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
                    print "cir: %d" %a.value.u64
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    print "cbs: %d" %a.value.u64
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PIR:
                    print "pir: %d" %a.value.u64
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PBS:
                    print "pbs: %d" %a.value.u64
                    if 4000 != a.value.u64:
                        raise NotImplementedError()        
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.u32:
                        print "meter type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_TR_TCM != a.value.u32:
                        print "policer mode error!!! %d" % a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_BLIND != a.value.u32:
                        print "color source error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.u32:
                        print "green drop error!!! %d" % a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.u32:
                        print "yellow drop error!!! %d" % a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.u32:
                        print "red drop error!!! %d" % a.value.u32
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
        print "start test"
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
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
                    print "cir: %d" %a.value.u64
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    print "cbs: %d" %a.value.u64
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PIR:
                    print "pir: %d" %a.value.u64
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PBS:
                    print "pbs: %d" %a.value.u64
                    if 4000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.u32:
                        print "meter type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_TR_TCM != a.value.u32:
                        print "policer mode error!!! %d" % a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_AWARE != a.value.u32:
                        print "color source error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.u32:
                        print "green drop error!!! %d" % a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_FORWARD != a.value.u32:
                        print "yellow drop error!!! %d" % a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.u32:
                        print "red drop error!!! %d" % a.value.u32
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
        print "start test"
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
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
                    print "cir: %d" %a.value.u64
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_CBS:
                    print "cbs: %d" %a.value.u64
                    if 2000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PIR:
                    print "pir: %d" %a.value.u64
                    if 200000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_PBS:
                    print "pbs: %d" %a.value.u64
                    if 4000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.u32:
                        print "meter type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_TR_TCM != a.value.u32:
                        print "policer mode error!!! %d" % a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_POLICER_ATTR_COLOR_SOURCE:
                    if SAI_POLICER_COLOR_SOURCE_BLIND != a.value.u32:
                        print "color source error!!! %d" % a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_GREEN_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.u32:
                        print "green drop error!!! %d" % a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_POLICER_ATTR_YELLOW_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.u32:
                        print "yellow drop error!!! %d" % a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_POLICER_ATTR_RED_PACKET_ACTION:
                    if SAI_PACKET_ACTION_DROP != a.value.u32:
                        print "red drop error!!! %d" % a.value.u32
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
        print "start test"
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_STORM_CONTROL, 0,
                                                    100000, 0, 0, 0,
                                                    0, 0, 0, [0,0,0])

        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID, value=attr_value)
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
                    print "cir: %d" %a.value.u64
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_BYTES != a.value.u32:
                        print "meter type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_STORM_CONTROL != a.value.u32:
                        print "policer mode error!!! %d" % a.value.u32
                        raise NotImplementedError()                                          
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_FLOOD_STORM_CONTROL_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
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
        print "start test"
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
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
                    print "cir: %d" %a.value.u64
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_PACKETS != a.value.u32:
                        print "meter type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_STORM_CONTROL != a.value.u32:
                        print "policer mode error!!! %d" % a.value.u32
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
        print "start test"
        switch_init(self.client)
        port = port_list[0]

        #create policer id
        policer_id = _sai_thrift_qos_create_policer(self.client,
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
                    print "cir: %d" %a.value.u64
                    if 120000 != a.value.u64:
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_METER_TYPE:
                    if SAI_METER_TYPE_PACKETS != a.value.u32:
                        print "meter type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_POLICER_ATTR_MODE:
                    if SAI_POLICER_MODE_STORM_CONTROL != a.value.u32:
                        print "policer mode error!!! %d" % a.value.u32
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
        print "start test"
        switch_init(self.client)
        port = port_list[0]

        #create policer id 1
        policer_id1 = _sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000, 2000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
        #apply to port
        attr_value = sai_thrift_attribute_value_t(oid=policer_id1)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port,attr)
        
        warmboot(self.client)
        try:
            #create policer id 2
            policer_id2 = _sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_PACKETS, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_AWARE,
                                                    200000, 4000, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,1,1])   
            #apply to port 
            attr_value = sai_thrift_attribute_value_t(oid=policer_id2)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)                                                                                
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port,attr)
            self.client.sai_thrift_remove_policer(policer_id1)
            self.client.sai_thrift_remove_policer(policer_id2)


def _QosMapCreateMapId(client, map_type=None, key_list1=[], key_list2=[], value_list=[]):
    max_num = len(value_list)
    attr_list = []
    map_list = []

    attr_value = sai_thrift_attribute_value_t(s32=map_type)
    attr = sai_thrift_attribute_t(id=SAI_QOS_MAP_ATTR_TYPE, value=attr_value)
    attr_list.append(attr)

    for i in range(max_num):
        if map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
            key = sai_thrift_qos_map_params_t(dot1p=key_list1[i])
            value = sai_thrift_qos_map_params_t(tc=value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
            key = sai_thrift_qos_map_params_t(dot1p=key_list1[i])
            value = sai_thrift_qos_map_params_t(color=value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_DSCP_TO_TC:
            key = sai_thrift_qos_map_params_t(dscp=key_list1[i])
            value = sai_thrift_qos_map_params_t(tc=value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
            key = sai_thrift_qos_map_params_t(dscp=key_list1[i])
            value = sai_thrift_qos_map_params_t(color=value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP:
            key = sai_thrift_qos_map_params_t(tc=key_list1[i], color=key_list2[i])
            value = sai_thrift_qos_map_params_t(dscp=value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P:
            key = sai_thrift_qos_map_params_t(tc=key_list1[i], color=key_list2[i])
            value = sai_thrift_qos_map_params_t(dot1p=value_list[i])
        elif map_type == SAI_QOS_MAP_TYPE_TC_TO_QUEUE:
            key = sai_thrift_qos_map_params_t(tc=key_list1[i])
            value = sai_thrift_qos_map_params_t(queue_index=value_list[i])

        map_list.append(sai_thrift_qos_map_t(key=key, value=value))
    qosmap = sai_thrift_qos_map_list_t(count = len(map_list), map_list = map_list)
    attr_value = sai_thrift_attribute_value_t(qosmap=qosmap)
    attr = sai_thrift_attribute_t(id=SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST, value=attr_value)
    attr_list.append(attr)
    return client.sai_thrift_create_qos_map(attr_list)

@group('QosMap')
class SwitchQosMapSetDefaultTCandUpdateDSCP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Set Switch default TC
        step1:Set Switch default TC
        step2:verify switch attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        #Set switch default tc
        attr_value = sai_thrift_attribute_value_t(u8=7)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DEFAULT_TC, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        #default tc map to dscp
        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_GREEN]
        value_list = [20]
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, key_list1, key_list2 , value_list)
        attr_value = sai_thrift_attribute_value_t(oid=map_id)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr) 

        #port2 update dscp
        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2,attr)

        #Create route
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_dscp=10)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                ip_dscp=20)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])
            ids_list = [SAI_SWITCH_ATTR_QOS_DEFAULT_TC]
            attrs = self.client.sai_thrift_get_switch_attribute(ids_list)
            for a in attrs.attr_list:
                if a.id == SAI_SWITCH_ATTR_QOS_DEFAULT_TC:
                    print "default tc: %d" %a.value.u8
                    if 7 != a.value.u8:
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(u8=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DEFAULT_TC, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2,attr)
            self.client.sai_thrift_remove_qos_map(map_id)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)


@group('QosMap')
class SwitchQosMapTCMaptoQueueandUpdateDSCP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QosMap & apply to switch 
        step1:create qosmap id Tc-->Queue & apply to switch
        step2:verify qosmap attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        #Create QosMap, TC-->queue
        key_list =    [7]
        value_list = [1]
        print "Create QosMap:TC -- > Queue"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_TO_QUEUE, key_list, [], value_list)
        attr_value = sai_thrift_attribute_value_t(oid=map_id)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_TO_QUEUE_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        #Create QosMap, DSCP --> TC
        key_list_dscp = [10]
        value_list_tc = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list_dscp, [], value_list_tc)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_dscp_tc)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr) 

        #tc map to dscp
        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_GREEN]
        value_list1 = [20]
        map_id_tc_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, key_list1, key_list2 , value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dscp)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr) 

        #Create route
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

        #port2 update dscp
        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2,attr)
        
        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_dscp=10)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                ip_dscp=20)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            key_list_temp = [None]*len(key_list)
            value_list_temp = [None]*len(key_list)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    if a.value.u32 != SAI_QOS_MAP_TYPE_TC_TO_QUEUE:
                        print "map type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    if a.value.qosmap.count != len(key_list):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i] = a.value.qosmap.map_list[i].key.tc
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.queue_index
                    print "got key_list:  ",key_list_temp
                    print "got value_list:",value_list_temp
                    if key_list_temp != key_list:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list:
                        print "get value list error!!!"
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2,attr)
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_TO_QUEUE_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_tc_dscp)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

@group('QosMap')
class SwitchQosMapDot1pMaptoTCandUpdateDot1p(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QosMap & apply to switch 
        step1:create qosmap id Dot1p-->TC & apply to switch
        step2:verify qosmap attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]

        #Create QosMap, dot1p -- > TC
        key_list =    [0]
        value_list = [7]
        print "Create QosMap:dot1p -- > TC"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list, [], value_list)
        attr_value = sai_thrift_attribute_value_t(oid=map_id)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        #Create QosMap, TC&Color --> Dot1p
        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_GREEN]
        value_list1 = [7]
        map_id_tc_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, key_list1, key_list2 , value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dot1p)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr) 

        #Create fdb
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102)
        exp_pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=7)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            key_list_temp = [None]*len(key_list)
            value_list_temp = [None]*len(key_list)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    if a.value.u32 != SAI_QOS_MAP_TYPE_DOT1P_TO_TC:
                        print "map type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    if a.value.qosmap.count != len(key_list):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i] = a.value.qosmap.map_list[i].key.dot1p
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.tc
                    print "got key_list:  ",key_list_temp
                    print "got value_list:",value_list_temp
                    if key_list_temp != key_list:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list:
                        print "get value list error!!!"
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_qos_map(map_id_tc_dot1p)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('QosMap')
class SwitchQosMapDot1pMaptoColorandUpdateDot1p(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QosMap & apply to switch 
        step1:create qosmap id Dot1p-->Color & apply to switch
        step2:verify qosmap attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]

        #Create QosMap, dot1p -- > Color
        key_list =    [0]
        value_list = [SAI_PACKET_COLOR_YELLOW]
        print "Create QosMap:dot1p -- > Color"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list, [], value_list)
        attr_value = sai_thrift_attribute_value_t(oid=map_id)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        #Create QosMap, dot1p -- > TC
        key_list1 =    [0]
        value_list1 = [7]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_dot1p_tc)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        #Create QosMap, TC&Color --> Dot1p
        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_YELLOW]
        value_list1 = [7]
        map_id_tc_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, key_list1, key_list2 , value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dot1p)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr) 

        #Create fdb
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102)
        exp_pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=7)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            key_list_temp = [None]*len(key_list)
            value_list_temp = [None]*len(key_list)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    if a.value.u32 != SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
                        print "map type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    if a.value.qosmap.count != len(key_list):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i] = a.value.qosmap.map_list[i].key.dot1p
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.color
                    print "got key_list:  ",key_list_temp
                    print "got value_list:",value_list_temp
                    if key_list_temp != key_list:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list:
                        print "get value list error!!!"
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_tc_dot1p)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

@group('QosMap')
class SwitchQosMapDscpMaptoTCandUpdateDSCP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QosMap & apply to switch 
        step1:create qosmap id DSCP-->TC & apply to switch
        step2:verify qosmap attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        #Create QosMap, DSCP-->TC
        key_list =    [10]
        value_list = [7]
        print "Create QosMap:DSCP-->TC"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list, [], value_list)
        attr_value = sai_thrift_attribute_value_t(oid=map_id)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        #Create QosMap, TC&Color --> DSCP
        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_GREEN]
        value_list1 = [20]
        map_id_tc_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, key_list1, key_list2 , value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dscp)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr) 

        #port2 update dscp
        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2,attr) 

        #Create route
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_dscp=10)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                ip_dscp=20)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            key_list_temp = [None]*len(key_list)
            value_list_temp = [None]*len(key_list)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    if a.value.u32 != SAI_QOS_MAP_TYPE_DSCP_TO_TC:
                        print "map type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    if a.value.qosmap.count != len(key_list):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i] = a.value.qosmap.map_list[i].key.dscp
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.tc
                    print "got key_list:  ",key_list_temp
                    print "got value_list:",value_list_temp
                    if key_list_temp != key_list:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list:
                        print "get value list error!!!"
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2,attr)
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_qos_map(map_id_tc_dscp)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

@group('QosMap')
class SwitchQosMapDscpMaptoColorandUpdateDSCP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QosMap & apply to switch 
        step1:create qosmap id DSCP-->TC & apply to switch
        step2:verify qosmap attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        #Create QosMap, DSCP-->TC
        key_list =    [10]
        value_list = [SAI_PACKET_COLOR_YELLOW]
        print "Create QosMap:DSCP-->Color"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list, [], value_list)
        attr_value = sai_thrift_attribute_value_t(oid=map_id)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        #Create QosMap, DSCP-->TC
        key_list1 =    [10]
        value_list1 = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_dscp_tc)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        #Create QosMap, TC&Color --> DSCP
        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_YELLOW]
        value_list1 = [20]
        map_id_tc_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, key_list1, key_list2 , value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dscp)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr) 

        #port2 update dscp
        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2,attr) 

        #Create route
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_dscp=10)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                ip_dscp=20)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            key_list_temp = [None]*len(key_list)
            value_list_temp = [None]*len(key_list)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    if a.value.u32 != SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
                        print "map type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    if a.value.qosmap.count != len(key_list):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i] = a.value.qosmap.map_list[i].key.dscp
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.color
                    print "got key_list:  ",key_list_temp
                    print "got value_list:",value_list_temp
                    if key_list_temp != key_list:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list:
                        print "get value list error!!!"
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DSCP_TO_COLOR_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2,attr)
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_tc_dscp)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)

@group('QosMap')
class PortQosMapDscpMaptoTCandUpdateDSCP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QosMap & apply to port
        step1:create qosmap id DSCP-->TC & apply to port
        step2:verify qosmap attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        #Create QosMap, DSCP-->TC
        key_list =    [10]
        value_list = [7]
        print "Create QosMap:DSCP-->TC"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list, [], value_list)
        attr_value = sai_thrift_attribute_value_t(oid=map_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        #Create QosMap, TC&Color --> DSCP
        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_GREEN]
        value_list1 = [20]
        map_id_tc_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, key_list1, key_list2 , value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dscp)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr) 

        #port2 update dscp
        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2,attr) 

        #Create route
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_dscp=10)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                ip_dscp=20)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            key_list_temp = [None]*len(key_list)
            value_list_temp = [None]*len(key_list)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    if a.value.u32 != SAI_QOS_MAP_TYPE_DSCP_TO_TC:
                        print "map type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    if a.value.qosmap.count != len(key_list):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i] = a.value.qosmap.map_list[i].key.dscp
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.tc
                    print "got key_list:  ",key_list_temp
                    print "got value_list:",value_list_temp
                    if key_list_temp != key_list:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list:
                        print "get value list error!!!"
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)  
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_qos_map(map_id_tc_dscp)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)            

@group('QosMap')
class PortQosMapDscpMaptoColorandUpdateDSCP(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QosMap & apply to port
        step1:create qosmap id DSCP-->Color & apply to port
        step2:verify qosmap attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port1 = port_list[0]
        port2 = port_list[1]

        #Create route
        v4_enabled = 1
        v6_enabled = 1
        mac_valid = 0
        mac = ''
        vr_id = sai_thrift_create_virtual_router(self.client, v4_enabled, v6_enabled)
        rif_id1 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port1, 0, v4_enabled, v6_enabled, mac)
        rif_id2 = sai_thrift_create_router_interface(self.client, vr_id, SAI_ROUTER_INTERFACE_TYPE_PORT, port2, 0, v4_enabled, v6_enabled, mac)
        addr_family = SAI_IP_ADDR_FAMILY_IPV4
        ip_addr1 = '10.10.10.1'
        dmac1 = '00:11:22:33:44:55'
        sai_thrift_create_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)

        #Create QosMap, DSCP-->Color
        key_list =    [10]
        value_list = [SAI_PACKET_COLOR_YELLOW]
        print "Create QosMap:DSCP-->Color"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_COLOR, key_list, [], value_list)
        attr_value = sai_thrift_attribute_value_t(oid=map_id)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        #Create QosMap, DSCP-->TC
        key_list1 =    [10]
        value_list1 = [7]
        map_id_dscp_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list1, [], value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_dscp_tc)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port1, attr)

        #port2 update dscp
        attr_value = sai_thrift_attribute_value_t(booldata=True)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2,attr) 

        #Create QosMap, TC&Color --> DSCP
        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_YELLOW]
        value_list1 = [20]
        map_id_tc_dscp = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, key_list1, key_list2 , value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dscp)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port2, attr) 

        # send the test packet(s)
        pkt = simple_tcp_packet(eth_dst=router_mac,
                                eth_src='00:22:22:22:22:22',
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=64,
                                ip_dscp=10)
        exp_pkt = simple_tcp_packet(
                                eth_dst='00:11:22:33:44:55',
                                eth_src=router_mac,
                                ip_dst='10.10.10.1',
                                ip_src='192.168.0.1',
                                ip_id=105,
                                ip_ttl=63,
                                ip_dscp=20)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            key_list_temp = [None]*len(key_list)
            value_list_temp = [None]*len(key_list)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    if a.value.u32 != SAI_QOS_MAP_TYPE_DSCP_TO_COLOR:
                        print "map type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    if a.value.qosmap.count != len(key_list):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i] = a.value.qosmap.map_list[i].key.dscp
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.color
                    print "got key_list:  ",key_list_temp
                    print "got value_list:",value_list_temp
                    if key_list_temp != key_list:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list:
                        print "get value list error!!!"
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)  
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_COLOR_MAP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port1, attr)
            attr_value = sai_thrift_attribute_value_t(booldata=False)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_UPDATE_DSCP, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port2, attr)
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_qos_map(map_id_dscp_tc)
            self.client.sai_thrift_remove_qos_map(map_id_tc_dscp)
            sai_thrift_remove_neighbor(self.client, addr_family, rif_id2, ip_addr1, dmac1)
            self.client.sai_thrift_remove_virtual_router(vr_id)
            self.client.sai_thrift_remove_router_interface(rif_id1)
            self.client.sai_thrift_remove_router_interface(rif_id2)  

@group('QosMap')
class SetQosMapAttributeTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QosMap & apply to switch 
        step1:create qosmap id Dot1p-->Color & apply to switch
        step2:set qosmap attr & verify qosmap attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        vlan_id = 10
        port1 = port_list[0]
        port2 = port_list[1]

        #Create QosMap, dot1p -- > Color
        key_list =    [0]
        value_list = [SAI_PACKET_COLOR_YELLOW]
        print "Create QosMap:dot1p -- > Color"
        print "set key_list:  ",key_list
        print "set value_list:",value_list
        map_id = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR, key_list, [], value_list)
        attr_value = sai_thrift_attribute_value_t(oid=map_id)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        #Create QosMap, dot1p -- > TC
        key_list1 =    [0]
        value_list1 = [7]
        map_id_dot1p_tc = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list1, [], value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_dot1p_tc)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr)

        #Create QosMap, TC&Color --> Dot1p
        key_list1 = [7]
        key_list2 = [SAI_PACKET_COLOR_YELLOW]
        value_list1 = [7]
        map_id_tc_dot1p = _QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, key_list1, key_list2 , value_list1)
        attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dot1p)
        attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value=attr_value)
        self.client.sai_thrift_set_switch_attribute(attr) 

        #Create fdb
        mac1 = '00:11:11:11:11:11'
        mac2 = '00:22:22:22:22:22'
        mac_action = SAI_PACKET_ACTION_FORWARD

        vlan_oid = sai_thrift_create_vlan(self.client, vlan_id)
        vlan_member1 = sai_thrift_create_vlan_member(self.client, vlan_oid, port1, SAI_VLAN_TAGGING_MODE_TAGGED)
        vlan_member2 = sai_thrift_create_vlan_member(self.client, vlan_oid, port2, SAI_VLAN_TAGGING_MODE_TAGGED)

        sai_thrift_create_fdb(self.client, vlan_oid, mac2, port2, mac_action)

        pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                ip_dst='10.0.0.1',
                                ip_id=102)
        pkt1 = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=1,
                                ip_dst='10.0.0.1',
                                ip_id=102)
        exp_pkt = simple_tcp_packet(eth_dst='00:22:22:22:22:22',
                                eth_src='00:11:11:11:11:11',
                                ip_dst='10.0.0.1',
                                ip_id=102,
                                dl_vlan_enable=True,
                                vlan_vid=10,
                                vlan_pcp=7)

        warmboot(self.client)
        try:
            self.ctc_send_packet( 0, str(pkt))
            self.ctc_verify_packets( exp_pkt, [1])

            key_list_temp = [None]*len(key_list)
            value_list_temp = [None]*len(key_list)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    if a.value.u32 != SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
                        print "map type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    if a.value.qosmap.count != len(key_list):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i] = a.value.qosmap.map_list[i].key.dot1p
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.color
                    print "got key_list:  ",key_list_temp
                    print "got value_list:",value_list_temp
                    if key_list_temp != key_list:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list:
                        print "get value list error!!!"
                        raise NotImplementedError()

            #set qosmap attr
            map_list = []
            key_list =   [0, 1]
            value_list = [SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_YELLOW]

            print "set key_list:  ",key_list
            print "set value_list:",value_list

            key = sai_thrift_qos_map_params_t(dot1p=key_list[0])
            value = sai_thrift_qos_map_params_t(color=value_list[0])
            map_list.append(sai_thrift_qos_map_t(key=key, value=value))
            key = sai_thrift_qos_map_params_t(dot1p=key_list[1])
            value = sai_thrift_qos_map_params_t(color=value_list[1])
            map_list.append(sai_thrift_qos_map_t(key=key, value=value))
            qosmap = sai_thrift_qos_map_list_t(count = len(map_list), map_list = map_list)
            attr_value = sai_thrift_attribute_value_t(qosmap=qosmap)
            attr = sai_thrift_attribute_t(id=SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST, value=attr_value)
            self.client.sai_thrift_set_qos_map_attribute(map_id, attr)

            map_list = []
            key_list1 =   [0, 1]
            value_list1 = [7, 7]
            key = sai_thrift_qos_map_params_t(dot1p=key_list1[0])
            value = sai_thrift_qos_map_params_t(tc=value_list1[0])
            map_list.append(sai_thrift_qos_map_t(key=key, value=value))
            key = sai_thrift_qos_map_params_t(dot1p=key_list1[1])
            value = sai_thrift_qos_map_params_t(tc=value_list1[1])
            map_list.append(sai_thrift_qos_map_t(key=key, value=value))
            qosmap = sai_thrift_qos_map_list_t(count = len(map_list), map_list = map_list)
            attr_value = sai_thrift_attribute_value_t(qosmap=qosmap)
            attr = sai_thrift_attribute_t(id=SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST, value=attr_value)
            self.client.sai_thrift_set_qos_map_attribute(map_id_dot1p_tc, attr)

            #Send packet
            self.ctc_send_packet( 0, str(pkt1))
            self.ctc_verify_packets( exp_pkt, [1])

            key_list_temp = [None]*len(key_list)
            value_list_temp = [None]*len(key_list)
            attrs = self.client.sai_thrift_get_qos_map_attribute(map_id) 
            for a in attrs.attr_list:
                if a.id == SAI_QOS_MAP_ATTR_TYPE:
                    if a.value.u32 != SAI_QOS_MAP_TYPE_DOT1P_TO_COLOR:
                        print "map type error!!! %d" % a.value.u32
                        raise NotImplementedError()
                if a.id == SAI_QOS_MAP_ATTR_MAP_TO_VALUE_LIST:
                    if a.value.qosmap.count != len(key_list):
                        print "get map list error!!! count: %d" % a.value.qosmap.count
                        raise NotImplementedError()
                    for i in range(a.value.qosmap.count):
                        key_list_temp[i] = a.value.qosmap.map_list[i].key.dot1p
                        value_list_temp[i] = a.value.qosmap.map_list[i].value.color
                    print "got key_list:  ",key_list_temp
                    print "got value_list:",value_list_temp
                    if key_list_temp != key_list:
                        print "get key list error!!!"
                        raise NotImplementedError()
                    if value_list_temp != value_list:
                        print "get value list error!!!"
                        raise NotImplementedError()

        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_TC_AND_COLOR_TO_DOT1P_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr) 
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_COLOR_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)  
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SWITCH_ATTR_QOS_DOT1P_TO_TC_MAP, value=attr_value)
            self.client.sai_thrift_set_switch_attribute(attr)
            self.client.sai_thrift_remove_qos_map(map_id)
            self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc)
            self.client.sai_thrift_remove_qos_map(map_id_tc_dot1p)
            sai_thrift_delete_fdb(self.client, vlan_oid, mac2, port2)
            self.client.sai_thrift_remove_vlan_member(vlan_member1)
            self.client.sai_thrift_remove_vlan_member(vlan_member2)
            self.client.sai_thrift_remove_vlan(vlan_oid)

#Wred
def _sai_thrift_qos_create_wred(client, color_en = [None]*3, min_thrd = [None]*3, max_thrd = [None]*3, drop_prob = [None]*3):
    attr_list = []

    #0:green,1:yellow,2:red
    for i in range(3):
        attr_shift = i*4
        if color_en[i]:
            attr_value = sai_thrift_attribute_value_t(booldata=True)
            attr = sai_thrift_attribute_t(id=(SAI_WRED_ATTR_GREEN_ENABLE+attr_shift), value=attr_value)
            attr_list.append(attr)
        if min_thrd[i]:
            attr_value = sai_thrift_attribute_value_t(u32=min_thrd[i])
            attr = sai_thrift_attribute_t(id=(SAI_WRED_ATTR_GREEN_MIN_THRESHOLD+attr_shift), value=attr_value)
            attr_list.append(attr)
        if max_thrd[i]:
            attr_value = sai_thrift_attribute_value_t(u32=max_thrd[i])
            attr = sai_thrift_attribute_t(id=(SAI_WRED_ATTR_GREEN_MAX_THRESHOLD+attr_shift), value=attr_value)
            attr_list.append(attr)
        if drop_prob[i]:
            attr_value = sai_thrift_attribute_value_t(u32=drop_prob[i])
            attr = sai_thrift_attribute_t(id=(SAI_WRED_ATTR_GREEN_DROP_PROBABILITY+attr_shift), value=attr_value)
            attr_list.append(attr)

    return client.sai_thrift_create_wred_profile(attr_list)         

@group('Wred')
class WredCreateWithEnableGreenDrop(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create WredId
        step1:create wred id & enable green drop
        step2:verify wred attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)

        color_en = [1,0,0]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [50, 30, 10]
        wred_id = _sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        print "Color_en:", color_en
        print "min_thrd:", min_thrd
        print "max_thrd:", max_thrd
        print "drop_prob:", drop_prob
        print "wred_id:",wred_id
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    if a.value.booldata is not True:
                        print "green drop en:%d"%a.value.booldata
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata is not False:
                        print "yellow drop en:%d"%a.value.booldata
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata is not False:
                        print "red drop en:%d"%a.value.booldata
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        print "green min thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        print "yellow min thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    if a.value.u32 != 100:
                        print "red min thrd:",a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 2000:
                        print "green max thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        print "yellow max thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        print "red max thrd:",a.value.u32
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 50:
                        print "green drop prob:",a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    if a.value.u32 != 30:
                        print "yellow drop prob:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        print "red drop prob:",a.value.u32
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
        print "start test"
        switch_init(self.client)

        color_en = [0,1,0]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [50, 10, 10]
        wred_id = _sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        print "Color_en:", color_en
        print "min_thrd:", min_thrd
        print "max_thrd:", max_thrd
        print "drop_prob:", drop_prob
        print "wred_id:",wred_id
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    if a.value.booldata is not False:
                        print "green drop en:%d"%a.value.booldata
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata is not True:
                        print "yellow drop en:%d"%a.value.booldata
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata is not False:
                        print "red drop en:%d"%a.value.booldata
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        print "green min thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        print "yellow min thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    if a.value.u32 != 100:
                        print "red min thrd:",a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 2000:
                        print "green max thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        print "yellow max thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        print "red max thrd:",a.value.u32
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 50:
                        print "green drop prob:",a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        print "yellow drop prob:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        print "red drop prob:",a.value.u32
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
        print "start test"
        switch_init(self.client)

        color_en = [0,0,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [50, 10, 10]
        wred_id = _sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        print "Color_en:", color_en
        print "min_thrd:", min_thrd
        print "max_thrd:", max_thrd
        print "drop_prob:", drop_prob
        print "wred_id:",wred_id
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    if a.value.booldata is not False:
                        print "green drop en:%d"%a.value.booldata
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata is not False:
                        print "yellow drop en:%d"%a.value.booldata
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata is not True:
                        print "red drop en:%d"%a.value.booldata
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        print "green min thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        print "yellow min thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    if a.value.u32 != 100:
                        print "red min thrd:",a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 2000:
                        print "green max thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        print "yellow max thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        print "red max thrd:",a.value.u32
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 50:
                        print "green drop prob:",a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        print "yellow drop prob:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        print "red drop prob:",a.value.u32
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
        print "start test"
        switch_init(self.client)

        color_en = [1,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [10, 10, 10]
        wred_id = _sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        print "Color_en:", color_en
        print "min_thrd:", min_thrd
        print "max_thrd:", max_thrd
        print "drop_prob:", drop_prob
        print "wred_id:",wred_id
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    if a.value.booldata is not True:
                        print "green drop en:%d"%a.value.booldata
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata is not True:
                        print "yellow drop en:%d"%a.value.booldata
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata is not True:
                        print "red drop en:%d"%a.value.booldata
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        print "green min thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        print "yellow min thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    if a.value.u32 != 100:
                        print "red min thrd:",a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 2000:
                        print "green max thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        print "yellow max thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        print "red max thrd:",a.value.u32
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        print "green drop prob:",a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        print "yellow drop prob:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        print "red drop prob:",a.value.u32
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
        print "start test"
        switch_init(self.client)

        color_en = [0,1,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [10, 10, 10]
        wred_id = _sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        print "Color_en:", color_en
        print "min_thrd:", min_thrd
        print "max_thrd:", max_thrd
        print "drop_prob:", drop_prob
        print "wred_id:",wred_id
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    if a.value.booldata is not False:
                        print "green drop en:%d"%a.value.booldata
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    if a.value.booldata is not True:
                        print "yellow drop en:%d"%a.value.booldata
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    if a.value.booldata is not True:
                        print "red drop en:%d"%a.value.booldata
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        print "green min thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    if a.value.u32 != 1000:
                        print "yellow min thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    if a.value.u32 != 100:
                        print "red min thrd:",a.value.u32
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    if a.value.u32 != 2000:
                        print "green max thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        print "yellow max thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        print "red max thrd:",a.value.u32
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        print "green drop prob:",a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        print "yellow drop prob:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    if a.value.u32 != 10:
                        print "red drop prob:",a.value.u32
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

            attrs = self.client.sai_thrift_get_wred_attribute_profile(wred_id)
            for a in attrs.attr_list:
                if a.id == SAI_WRED_ATTR_GREEN_ENABLE:
                    print "new green drop en:%d"%a.value.booldata
                    if a.value.booldata is not True:
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_YELLOW_ENABLE:
                    print "yellow drop en:%d"%a.value.booldata
                    if a.value.booldata is not True:
                        raise NotImplementedError()
                if a.id == SAI_WRED_ATTR_RED_ENABLE:
                    print "red drop en:%d"%a.value.booldata
                    if a.value.booldata is not True:
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_GREEN_MIN_THRESHOLD:
                    print "new green min thrd:",a.value.u32
                    if a.value.u32 != 2000:
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MIN_THRESHOLD:
                    print "yellow min thrd:",a.value.u32
                    if a.value.u32 != 1000:
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MIN_THRESHOLD:
                    print "red min thrd:",a.value.u32
                    if a.value.u32 != 100:
                        raise NotImplementedError()  
                if a.id == SAI_WRED_ATTR_GREEN_MAX_THRESHOLD:
                    print "green max thrd:",a.value.u32
                    if a.value.u32 != 3000:
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_YELLOW_MAX_THRESHOLD:
                    if a.value.u32 != 1500:
                        print "yellow max thrd:",a.value.u32
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_MAX_THRESHOLD:
                    if a.value.u32 != 200:
                        print "red max thrd:",a.value.u32
                        raise NotImplementedError()                          
                if a.id == SAI_WRED_ATTR_GREEN_DROP_PROBABILITY:
                    if a.value.u32 != 50:
                        print "new green drop prob:",a.value.u32
                        raise NotImplementedError()   
                if a.id == SAI_WRED_ATTR_YELLOW_DROP_PROBABILITY:
                    print "yellow drop prob:",a.value.u32
                    if a.value.u32 != 10:
                        raise NotImplementedError() 
                if a.id == SAI_WRED_ATTR_RED_DROP_PROBABILITY:
                    print "red drop prob:",a.value.u32
                    if a.value.u32 != 10:
                        raise NotImplementedError() 
        finally:
            self.client.sai_thrift_remove_wred_profile(wred_id)

def _sai_thrift_create_queue_id(client, queue_type, port, index, wred_id):
    attr_list = []

    attr_value = sai_thrift_attribute_value_t(u32=queue_type)
    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_TYPE, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(oid=port)
    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PORT, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u8=index)
    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_INDEX, value=attr_value)
    attr_list.append(attr)

    if wred_id:
        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        attr_list.append(attr)

    return client.sai_thrift_create_queue(attr_list)

@group('Queue')
class QueueCreateQueueIdWithUcTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create queue id  & UC
        step2:verify queue attr
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[0]
        queue_index = 1
        queue_type = SAI_QUEUE_TYPE_UNICAST

        queueId = _sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0) 
        print "queue_id:",queueId
        print "port:",port
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_TYPE:
                    print "get queue type:%d"%a.value.u32
                    if a.value.u32 != queue_type:
                        raise NotImplementedError() 
                if a.id == SAI_QUEUE_ATTR_PORT:
                    print "get port:",a.value.oid
                    if a.value.oid != port:
                        raise NotImplementedError()    
                if a.id == SAI_QUEUE_ATTR_INDEX:
                    print "get index:%d"%a.value.u8
                    if a.value.u8 != queue_index:
                        raise NotImplementedError()                                          
        finally:
            self.client.sai_thrift_remove_queue(queueId)

@group('Queue')
class QueueCreateQueueIdWithMcTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create queue id & MC
        step2:verify queue attr
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[0]
        queue_index = 1
        queue_type = SAI_QUEUE_TYPE_MULTICAST

        queueId = _sai_thrift_create_queue_id(self.client, queue_type, port, queue_index, 0) 
        print "queue_id:",queueId
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId)
            for a in attrs.attr_list:
                if a.id == SAI_QUEUE_ATTR_TYPE:
                    print "get queue type:%d"%a.value.u32
                    if a.value.u32 != queue_type:
                        raise NotImplementedError() 
                if a.id == SAI_QUEUE_ATTR_PORT:
                    print "get port:",a.value.oid
                    if a.value.oid != port:
                        raise NotImplementedError()    
                if a.id == SAI_QUEUE_ATTR_INDEX:
                    print "get index:%d"%a.value.u8
                    if a.value.u8 != queue_index:
                        raise NotImplementedError()                                          
        finally:
            self.client.sai_thrift_remove_queue(queueId)

@group('Queue')
class QueueSetQueueAttributeWithWredIdTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create QueueId
        step1:create queue id & Set Attr with WredId
        step2:verify queue attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[0]
        queue_index = 1

        #create Wred Id
        color_en = [0,0,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        wred_id = _sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        print "wred_id:",wred_id

        #Create Queue Id
        queueId = _sai_thrift_create_queue_id(self.client, SAI_QUEUE_TYPE_UNICAST, port, queue_index, 0) 
        print "queue_id:",queueId

        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId, attr)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId)
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    print "get wred_id:0x%X"%a.value.oid
                    if a.value.oid != wred_id:
                        raise NotImplementedError()                                      
        finally:
            self.client.sai_thrift_remove_wred_profile(wred_id)
            self.client.sai_thrift_remove_queue(queueId)

@group('Queue')
class GetQueueListFromPortTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Get Queue list from port
        step1:Get queue num & list & set queue attr
        step2:verify queue attr 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[0]
        queueId = 0
        queueId_list = []

        #create Wred Id
        color_en = [0,0,1]
        min_thrd = [1000,1000,100]
        max_thrd = [2000,1500,200]
        drop_prob = [100, 50, 10]
        wred_id = _sai_thrift_qos_create_wred(self.client, color_en, min_thrd, max_thrd, drop_prob)
        print "wred_id:0x%X"%wred_id


        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])
        queueId = queueId_list[0]

        #set attr
        attr_value = sai_thrift_attribute_value_t(oid=wred_id)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_WRED_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_queue_attribute(queueId)
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_WRED_PROFILE_ID:
                    print "get wred_id:0x%X"%a.value.oid
                    if a.value.oid != wred_id:
                        raise NotImplementedError() 
        finally:
            self.client.sai_thrift_remove_queue(queueId)


@group('Policer')
class PolicerStressTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Policer Stress Test
        step1:Create policer Id
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port_num = 32
        port = 0
        test_num = port_num*50
        policer_id = []
        #create policer id
        for i in range(test_num):
            policer_id_temp = _sai_thrift_qos_create_policer(self.client,
                                                    SAI_METER_TYPE_BYTES, SAI_POLICER_MODE_SR_TCM, SAI_POLICER_COLOR_SOURCE_BLIND,
                                                    100000+i*8, 2000+i*4, 0, 0,
                                                    0, 0, SAI_PACKET_ACTION_DROP, [0,0,1])
            print "policer_oid:0x%x"%policer_id_temp
            policer_id.append(policer_id_temp)
        warmboot(self.client)
        try:
            for i in range(test_num):
                attr_value = sai_thrift_attribute_value_t(oid=policer_id[i])
                attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
                self.client.sai_thrift_set_port_attribute(port_list[port],attr)
                print "port[%d] bind policer_oid:0x%x"%(port, policer_id[i])

                port += 1
                if port >= port_num:
                    port = 0
        finally:
            print "Clean Config"
            for i in range(port_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_POLICER_ID, value=attr_value)
                self.client.sai_thrift_set_port_attribute(port_list[i],attr)
            for i in range(test_num):
                self.client.sai_thrift_remove_policer(policer_id[i])

@group('QosMap')
class QosMapStressTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        QoSMap Stress Test
        step1:Create QoSMap Id
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port_num = 32
        domain_num = 7
        map_id_tc_dscp = []
        map_id_tc_dot1p = []
        map_id_dscp_tc = []
        map_id_dot1p_tc = []
        list_color = [SAI_PACKET_COLOR_GREEN, SAI_PACKET_COLOR_YELLOW, SAI_PACKET_COLOR_RED]

        #Create MapId
        for ii in range(domain_num):
            key_list = [ii]
            value_list = [(domain_num-ii)*4]
            map_id_tc_dscp.append(_QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DSCP, key_list, list_color , value_list))
            print "Tc&Color-->Dscp:0x%x"%map_id_tc_dscp[ii]
        for ii in range(domain_num):
            key_list = [ii*4]
            value_list = [(domain_num-ii)]
            map_id_dscp_tc.append(_QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DSCP_TO_TC, key_list, [] , value_list))
            print "Dscp-->Tc:0x%x"%map_id_dscp_tc[ii]
        for ii in range(domain_num):
            key_list = [ii]
            value_list = [domain_num-ii]
            map_id_tc_dot1p.append(_QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_TC_AND_COLOR_TO_DOT1P, key_list, list_color , value_list))
            print "Tc&Color-->Dot1p:0x%x"%map_id_tc_dot1p[ii]
        for ii in range(domain_num):
            key_list = [ii]
            value_list = [domain_num-ii]
            map_id_dot1p_tc.append(_QosMapCreateMapId(self.client, SAI_QOS_MAP_TYPE_DOT1P_TO_TC, key_list, [] , value_list))
            print "Dot1p-->Tc:0x%x"%map_id_dot1p_tc[ii]

        warmboot(self.client)
        try:
            #apply to ports
            for ii in range(port_num):
                print "Port[0x%x] bind ---->>>>"%port_list[ii]
                attr_value = sai_thrift_attribute_value_t(oid=map_id_tc_dscp[ii%domain_num])
                attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
                status = self.client.sai_thrift_set_port_attribute(port_list[ii], attr) 
                print "    [TC_AND_COLOR_TO_DSCP] MapId: 0x%x:"%map_id_tc_dscp[ii%domain_num]
                if status != 0:
                    print "Bind Failed, status=", status
                    raise NotImplementedError() 

                attr_value = sai_thrift_attribute_value_t(oid=map_id_dscp_tc[ii%domain_num])
                attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
                status = self.client.sai_thrift_set_port_attribute(port_list[ii], attr) 
                print "    [DSCP_TO_TC] MapId: 0x%x:"%map_id_dscp_tc[ii%domain_num]
                if status != 0:
                    print "Bind Failed, status=", status
                    raise NotImplementedError() 
        finally:
            print "Clean Config"
            for ii in range(port_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP, value=attr_value)
                status = self.client.sai_thrift_set_port_attribute(port_list[ii], attr) 
                if status != 0:
                    print "disable [SAI_PORT_ATTR_QOS_TC_AND_COLOR_TO_DSCP_MAP] error!, status:",status
    
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP, value=attr_value)
                status = self.client.sai_thrift_set_port_attribute(port_list[ii], attr) 
                if status != 0:
                    print "disable [SAI_PORT_ATTR_QOS_DSCP_TO_TC_MAP] error!, status:",status
    
            for ii in range(domain_num):
                self.client.sai_thrift_remove_qos_map(map_id_dot1p_tc[ii])
                self.client.sai_thrift_remove_qos_map(map_id_tc_dot1p[ii])
                self.client.sai_thrift_remove_qos_map(map_id_dscp_tc[ii])
                self.client.sai_thrift_remove_qos_map(map_id_tc_dscp[ii])

def _sai_thrift_qos_create_scheduler_profile(client,
                                            sched_type = SAI_SCHEDULING_TYPE_STRICT,
                                            sched_weight = 0,
                                            cir = 0, cbs = 0, pir = 0, pbs = 0):
    attr_list = []
    attr_value = sai_thrift_attribute_value_t(s32=sched_type)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_TYPE, value=attr_value)
    attr_list.append(attr)

    if sched_weight:
        attr_value = sai_thrift_attribute_value_t(u8=sched_weight)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, value=attr_value)
        attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u64=cir)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u64=cbs)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u64=pir)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u64=pbs)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE, value=attr_value)
    attr_list.append(attr)
    return client.sai_thrift_create_scheduler_profile(attr_list)

@group('Scheduler')
class QueueSchedulerTypeSPSchedulingTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler SP Scheduling Test
        step1:Create Scheduler Id
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_STRICT
        sched_weight = 0
        cir = 2000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        queueId_list = []

        sched_oid = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        print "sched_oid 0x%x"%sched_oid
        assert(0 != sched_oid)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])
        

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    print "Get Scheduler Type: %d"%a.value.s32
                    if a.value.s32 != sched_type:
                        raise NotImplementedError() 
                #if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                #    print "Get Scheduler Weight: %d"%a.value.u8
                #    if a.value.u8 != 1:
                #        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    print "Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    print "Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    print "Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    print "Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    print "Get queue Scheduler oid: 0x%x"%a.value.oid
                    if a.value.oid != sched_oid:
                        raise NotImplementedError() 
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
            self.client.sai_thrift_remove_queue(queueId_list[1])
            self.client.sai_thrift_remove_queue(queueId_list[0])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid)


@group('Scheduler')
class QueueSchedulerTypeDWRRSchedulingTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler WDRR Scheduling Test
        step1:Create Scheduler Id
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        queueId_list = []

        sched_oid_1 = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        print "sched_oid_1 0x%x"%sched_oid_1
        assert(0 != sched_oid_1)
        sched_oid_2 = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight * 2, cir, cbs, pir, pbs)
        print "sched_oid_2 0x%x"%sched_oid_2
        assert(0 != sched_oid_2)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid_1)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    print "Get Scheduler Type: %d"%a.value.s32
                    if a.value.s32 != sched_type:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    print "Get Scheduler Weight: %d"%a.value.u8
                    if a.value.u8 != sched_weight:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    print "Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    print "Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    print "Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    print "Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    print "Get queue Scheduler1 oid: 0x%x"%a.value.oid
                    if a.value.oid != sched_oid_1:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[1])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    print "Get queue Scheduler2 oid: 0x%x"%a.value.oid
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
            self.client.sai_thrift_remove_queue(queueId_list[1])
            self.client.sai_thrift_remove_queue(queueId_list[0])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)

@group('Scheduler')
class PortSchedulerSchedulingTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler SP Scheduling Test
        step1:Create Scheduler Id
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_STRICT
        sched_weight = 0
        cir = 2000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]

        sched_oid = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        print "sched_oid 0x%x"%sched_oid
        assert(0 != sched_oid)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    print "Get Scheduler Type: %d"%a.value.s32
                    if a.value.s32 != sched_type:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    print "Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    print "Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    print "Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    print "Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:  
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID:
                    print "Get port Scheduler oid: 0x%x"%a.value.oid
                    if a.value.oid != sched_oid:
                        raise NotImplementedError() 
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_QOS_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port, attr)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid)            

@group('Scheduler')
class QueueSchedulerUpdateWeightTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler WDRR Scheduling Test
        step1:Create Scheduler Id
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        queueId_list = []

        sched_oid_1 = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        print "sched_oid_1 0x%x"%sched_oid_1
        assert(0 != sched_oid_1)
        sched_oid_2 = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight * 2, cir, cbs, pir, pbs)
        print "sched_oid_2 0x%x"%sched_oid_2
        assert(0 != sched_oid_2)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        sched_weight = 50
        attr_value = sai_thrift_attribute_value_t(u8=sched_weight)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, value=attr_value)
        self.client.sai_thrift_set_scheduler_attribute(sched_oid_1, attr)

        attr_value = sai_thrift_attribute_value_t(u8=100)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, value=attr_value)
        self.client.sai_thrift_set_scheduler_attribute(sched_oid_2, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid_1)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    print "Get Scheduler Type: %d"%a.value.s32
                    if a.value.s32 != sched_type:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    print "Get Scheduler Weight: %d"%a.value.u8
                    if a.value.u8 != sched_weight:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    print "Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    print "Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    print "Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    print "Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    print "Get queue Scheduler1 oid: 0x%x"%a.value.oid
                    if a.value.oid != sched_oid_1:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[1])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    print "Get queue Scheduler2 oid: 0x%x"%a.value.oid
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
            self.client.sai_thrift_remove_queue(queueId_list[1])
            self.client.sai_thrift_remove_queue(queueId_list[0])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)            

@group('Scheduler')
class QueueSchedulerUpdateTypeTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler WDRR Scheduling Test
        step1:Create Scheduler Id
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        queueId_list = []

        sched_oid_1 = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        print "sched_oid_1 0x%x"%sched_oid_1
        assert(0 != sched_oid_1)
        sched_oid_2 = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight * 2, cir, cbs, pir, pbs)
        print "sched_oid_2 0x%x"%sched_oid_2
        assert(0 != sched_oid_2)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_2)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)

        sched_type = SAI_SCHEDULING_TYPE_STRICT
        attr_value = sai_thrift_attribute_value_t(s32=sched_type)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_TYPE, value=attr_value)
        self.client.sai_thrift_set_scheduler_attribute(sched_oid_1, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid_1)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_TYPE:
                    print "Get Scheduler Type: %d"%a.value.s32
                    if a.value.s32 != sched_type:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    print "Get Scheduler Weight: %d"%a.value.u8
                    if a.value.u8 != sched_weight:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_RATE:
                    print "Get Scheduler MIN_BANDWIDTH_RATE: %d"%a.value.u64
                    if a.value.u64 != cir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MIN_BANDWIDTH_BURST_RATE:
                    print "Get Scheduler MIN_BANDWIDTH_BURST_RATE: %d"%a.value.u64
                    if a.value.u64 != cbs:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_RATE:
                    print "Get Scheduler MAX_BANDWIDTH_RATE: %d"%a.value.u64
                    if a.value.u64 != pir:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_ATTR_MAX_BANDWIDTH_BURST_RATE:
                    print "Get Scheduler MAX_BANDWIDTH_BURST_RATE: %d"%a.value.u64
                    if a.value.u64 != pbs:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[0])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    print "Get queue Scheduler1 oid: 0x%x"%a.value.oid
                    if a.value.oid != sched_oid_1:
                        raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[1])
            for a in attrs.attr_list:  
                if a.id == SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID:
                    print "Get queue Scheduler2 oid: 0x%x"%a.value.oid
                    if a.value.oid != sched_oid_2:
                        raise NotImplementedError() 
        finally:
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_queue_attribute(queueId_list[0], attr)
            self.client.sai_thrift_set_queue_attribute(queueId_list[1], attr)
            self.client.sai_thrift_remove_queue(queueId_list[1])
            self.client.sai_thrift_remove_queue(queueId_list[0])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_2)              

def _sai_thrift_qos_create_scheduler_group(client, 
                                           port_id, 
                                           level, 
                                           max_childs, 
                                           parent_id, 
                                           sched_id = 0):
    attr_list = []

    attr_value = sai_thrift_attribute_value_t(oid=port_id)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PORT_ID, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u8=level)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_LEVEL, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(u8=max_childs)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS, value=attr_value)
    attr_list.append(attr)

    attr_value = sai_thrift_attribute_value_t(oid=parent_id)
    attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
    attr_list.append(attr)

    if sched_id :
        attr_value = sai_thrift_attribute_value_t(oid=sched_id)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        attr_list.append(attr)

    return client.sai_thrift_create_scheduler_group(attr_list)

@group('Scheduler Group')
class QueueSchedulerGroupBindTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 8]
        parent_id = [port, None, None]
        sched_group_id = [None]*6

        sched_group_id[0] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        print "sched_group_id[0]=0x%x"%sched_group_id[0]
        assert(0 != sched_group_id[0])
        parent_id[1] = sched_group_id[0]
        sched_group_id[1] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        print "sched_group_id[1]=0x%x"%sched_group_id[1]
        assert(0 != sched_group_id[1])
        sched_group_id[2] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        print "sched_group_id[2]=0x%x"%sched_group_id[2]
        assert(0 != sched_group_id[2])
        parent_id[2] = sched_group_id[1]
        sched_group_id[3] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[1], 0)
        print "sched_group_id[3]=0x%x"%sched_group_id[3]
        assert(0 != sched_group_id[3])
        sched_group_id[4] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[2], 0)
        print "sched_group_id[4]=0x%x"%sched_group_id[4]
        assert(0 != sched_group_id[4])
        sched_group_id[5] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[2], 0)
        print "sched_group_id[5]=0x%x"%sched_group_id[5]
        assert(0 != sched_group_id[5])

        queueId_list = []
        sched_oid_1 = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        print "sched_oid_1 0x%x"%sched_oid_1
        assert(0 != sched_oid_1)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])
                    attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                    attr_value = sai_thrift_attribute_value_t(oid=sched_group_id[i%3 + 3])
                    print "bind sched group:0x%X"%sched_group_id[i%3 + 3]
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id[2], attr)
        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                        print "Get queue[0x%x] Scheduler Group oid: 0x%x"%(queueId_list[ii], a.value.oid)
                        if a.value.oid != sched_group_id[ii%3 + 3]:
                            raise NotImplementedError() 

            print "Verfy Sched Group[0x%x] Attrs!"%sched_group_id[2]
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id[2])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    print "#Get Sched Oid:0x%x"%a.value.oid
                    if a.value.oid != sched_oid_1:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    print "#Get Levle:", a.value.u8
                    if a.value.u8 != level[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    print "#Get Max Childs:", a.value.u8
                    if a.value.u8 != max_childs[1]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    print "#Get Parent Node:0x%x"%a.value.oid
                    if a.value.oid != parent_id[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    print "#Get Port Id:0x%x"%a.value.oid
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    print "#Get Child Count:",a.value.u32
                    if a.value.u32 != 2:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    print "#Get Child Child List Count:",a.value.objlist.count
                    for o_i in range(a.value.objlist.count):
                        print "#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i])
                        if a.value.objlist.object_id_list[o_i] != sched_group_id[o_i%2 +4]:
                            raise NotImplementedError()       
        finally:
            for ii in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                self.client.sai_thrift_remove_queue(queueId_list[ii])
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id[2], attr)
            for ii in range(6):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id[ii])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)

@group('Scheduler Group')
class QueueSchedulerGroupUpdateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue & Update Parent Node Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 8]
        parent_id = [port, None, None]
        sched_group_id = [None]*6

        sched_group_id[0] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        print "sched_group_id[0]=0x%x"%sched_group_id[0]
        assert(0 != sched_group_id[0])
        parent_id[1] = sched_group_id[0]
        sched_group_id[1] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        print "sched_group_id[1]=0x%x"%sched_group_id[1]
        assert(0 != sched_group_id[1])
        sched_group_id[2] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        print "sched_group_id[2]=0x%x"%sched_group_id[2]
        assert(0 != sched_group_id[2])
        parent_id[2] = sched_group_id[1]
        sched_group_id[3] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[1], 0)
        print "sched_group_id[3]=0x%x"%sched_group_id[3]
        assert(0 != sched_group_id[3])
        sched_group_id[4] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[2], 0)
        print "sched_group_id[4]=0x%x"%sched_group_id[4]
        assert(0 != sched_group_id[4])
        sched_group_id[5] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[2], 0)
        print "sched_group_id[5]=0x%x"%sched_group_id[5]
        assert(0 != sched_group_id[5])

        queueId_list = []
        sched_oid_1 = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        print "sched_oid_1 0x%x"%sched_oid_1
        assert(0 != sched_oid_1)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])
                    attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                    attr_value = sai_thrift_attribute_value_t(oid=sched_group_id[i%3 + 3])
                    print "bind sched group:0x%X"%sched_group_id[i%3 + 3]
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id[2], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_group_id[1])
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id[4], attr)
        
        warmboot(self.client)
        try:
            print "Verfy Sched Group[0x%x] Attrs!"%sched_group_id[4]
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id[4])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    print "#Get Parent Node:0x%x"%a.value.oid
                    if a.value.oid != sched_group_id[1]:
                        raise NotImplementedError()

            print "Verfy Sched Group[0x%x] Attrs!"%sched_group_id[1]
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id[1])
            for a in attrs.attr_list:        
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    print "#Get Child Child List Count:",a.value.objlist.count
                    for o_i in range(a.value.objlist.count):
                        print "#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i])
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    print "#Get Child Count:",a.value.u32
                    if a.value.u32 != 2:
                        raise NotImplementedError()       
        finally:
            for ii in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                self.client.sai_thrift_remove_queue(queueId_list[ii])
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id[2], attr)
            for ii in range(6):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id[ii])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1)

@group('Scheduler Group')
class PortGetSchedulerGroupListTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue & Get Port Sched Group List Test
        step1:Create Scheduler Group Id
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 8]
        parent_id = [port, None, None]
        sched_group_id = [None]*6

        sched_group_id[0] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        print "sched_group_id[0]=0x%x"%sched_group_id[0]
        assert(0 != sched_group_id[0])
        parent_id[1] = sched_group_id[0]
        sched_group_id[1] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        print "sched_group_id[1]=0x%x"%sched_group_id[1]
        assert(0 != sched_group_id[1])
        sched_group_id[2] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        print "sched_group_id[2]=0x%x"%sched_group_id[2]
        assert(0 != sched_group_id[2])
        parent_id[2] = sched_group_id[1]
        sched_group_id[3] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[1], 0)
        print "sched_group_id[3]=0x%x"%sched_group_id[3]
        assert(0 != sched_group_id[3])
        sched_group_id[4] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[2], 0)
        print "sched_group_id[4]=0x%x"%sched_group_id[4]
        assert(0 != sched_group_id[4])
        sched_group_id[5] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[2], 0)
        print "sched_group_id[5]=0x%x"%sched_group_id[5]
        assert(0 != sched_group_id[5])

        queueId_list = []
        sched_oid_1 = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        print "sched_oid_1 0x%x"%sched_oid_1
        assert(0 != sched_oid_1)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])
                    attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                    attr_value = sai_thrift_attribute_value_t(oid=sched_group_id[i%3 + 3])
                    print "bind sched group:0x%X"%sched_group_id[i%3 + 3]
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id[2], attr)

        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                        print "Get queue[0x%x] Scheduler Group oid: 0x%x"%(queueId_list[ii], a.value.oid)
                        if a.value.oid != sched_group_id[ii%3 + 3]:
                            raise NotImplementedError() 

            print "Verfy Sched Group[0x%x] Attrs!"%sched_group_id[2]
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id[2])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    print "#Get Sched Oid:0x%x"%a.value.oid
                    if a.value.oid != sched_oid_1:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    print "#Get Levle:", a.value.u8
                    if a.value.u8 != level[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    print "#Get Max Childs:", a.value.u8
                    if a.value.u8 != max_childs[1]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    print "#Get Parent Node:0x%x"%a.value.oid
                    if a.value.oid != parent_id[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    print "#Get Port Id:0x%x"%a.value.oid
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    print "#Get Child Count:",a.value.u32
                    if a.value.u32 != 2:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    print "#Get Child Child List Count:",a.value.objlist.count
                    for o_i in range(a.value.objlist.count):
                        print "#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i])
                        if a.value.objlist.object_id_list[o_i] != sched_group_id[o_i%2 +4]:
                            raise NotImplementedError() 

            print "Get Port[0x%x] Sched Group List!"%port
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:           
                if a.id == SAI_PORT_ATTR_QOS_SCHEDULER_GROUP_LIST:
                    for i in range(a.value.objlist.count):
                        print ">> Sched Group List[%d]:0x%x"%(i, a.value.objlist.object_id_list[i])
                if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_SCHEDULER_GROUPS:
                    print "Sched Group Count:", a.value.u32
                    if 0 == a.value.u32:
                        raise NotImplementedError()         
        finally:
            for ii in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                self.client.sai_thrift_remove_queue(queueId_list[ii])
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id[2], attr)
            for ii in range(6):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id[ii])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1) 


@group('Scheduler Group')
class QueueSchedulerGroupUpdateSchedulerWeightTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Scheduler Group Bind Queue & Bind Scheduler & Update Weight
        step1:Create Scheduler Group Id & Bind Scheduler & Update Weight
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        sched_type = SAI_SCHEDULING_TYPE_DWRR
        sched_weight = 10
        cir = 4000000
        cbs = 256000
        pir = 1000000
        pbs = 64000
        port = port_list[1]
        level = [0,1,2]
        max_childs = [4, 8]
        parent_id = [port, None, None]
        sched_group_id = [None]*6

        sched_group_id[0] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[0], max_childs[0], parent_id[0], 0)
        print "sched_group_id[0]=0x%x"%sched_group_id[0]
        assert(0 != sched_group_id[0])
        parent_id[1] = sched_group_id[0]
        sched_group_id[1] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        print "sched_group_id[1]=0x%x"%sched_group_id[1]
        assert(0 != sched_group_id[1])
        sched_group_id[2] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[1], max_childs[1], parent_id[1], 0)
        print "sched_group_id[2]=0x%x"%sched_group_id[2]
        assert(0 != sched_group_id[2])
        parent_id[2] = sched_group_id[1]
        sched_group_id[3] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[1], 0)
        print "sched_group_id[3]=0x%x"%sched_group_id[3]
        assert(0 != sched_group_id[3])
        sched_group_id[4] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[2], 0)
        print "sched_group_id[4]=0x%x"%sched_group_id[4]
        assert(0 != sched_group_id[4])
        sched_group_id[5] = _sai_thrift_qos_create_scheduler_group(self.client, port, level[2], max_childs[1], sched_group_id[2], 0)
        print "sched_group_id[5]=0x%x"%sched_group_id[5]
        assert(0 != sched_group_id[5])

        queueId_list = []
        sched_oid_1 = _sai_thrift_qos_create_scheduler_profile(self.client, sched_type, sched_weight, cir, cbs, pir, pbs)
        print "sched_oid_1 0x%x"%sched_oid_1
        assert(0 != sched_oid_1)

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])
                    attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                    attr_value = sai_thrift_attribute_value_t(oid=sched_group_id[i%3 + 3])
                    print "bind sched group:0x%X"%sched_group_id[i%3 + 3]
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)

        attr_value = sai_thrift_attribute_value_t(oid=sched_oid_1)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
        self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id[2], attr)

        sched_weight = 50
        attr_value = sai_thrift_attribute_value_t(u8=sched_weight)
        attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT, value=attr_value)
        self.client.sai_thrift_set_scheduler_attribute(sched_oid_1, attr)  

        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE:
                        print "Get queue[0x%x] Scheduler Group oid: 0x%x"%(queueId_list[ii], a.value.oid)
                        if a.value.oid != sched_group_id[ii%3 + 3]:
                            raise NotImplementedError() 

            print "Verfy Sched Group[0x%x] Attrs!"%sched_group_id[2]
            attrs = self.client.sai_thrift_get_scheduler_group_attribute(sched_group_id[2])
            for a in attrs.attr_list:
                if a.id == SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID:
                    print "#Get Sched Oid:0x%x"%a.value.oid
                    if a.value.oid != sched_oid_1:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_LEVEL:
                    print "#Get Levle:", a.value.u8
                    if a.value.u8 != level[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_MAX_CHILDS:
                    print "#Get Max Childs:", a.value.u8
                    if a.value.u8 != max_childs[1]:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PARENT_NODE:
                    print "#Get Parent Node:0x%x"%a.value.oid
                    if a.value.oid != parent_id[1]:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_PORT_ID:
                    print "#Get Port Id:0x%x"%a.value.oid
                    if a.value.oid != port:
                        raise NotImplementedError() 
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_COUNT:
                    print "#Get Child Count:",a.value.u32
                    if a.value.u32 != 2:
                        raise NotImplementedError()
                if a.id == SAI_SCHEDULER_GROUP_ATTR_CHILD_LIST:
                    print "#Get Child Child List Count:",a.value.objlist.count
                    for o_i in range(a.value.objlist.count):
                        print "#Get Child[%d] Oid:0x%x"%(o_i, a.value.objlist.object_id_list[o_i])
                        if a.value.objlist.object_id_list[o_i] != sched_group_id[o_i%2 +4]:
                            raise NotImplementedError() 

            attrs = self.client.sai_thrift_get_scheduler_attribute(sched_oid_1)
            for a in attrs.attr_list:  
                if a.id == SAI_SCHEDULER_ATTR_SCHEDULING_WEIGHT:
                    print "Get Scheduler Weight: %d"%a.value.u8
                    if a.value.u8 != sched_weight:
                        raise NotImplementedError() 
        finally:
            for ii in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_PARENT_SCHEDULER_NODE, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[ii], attr)
                self.client.sai_thrift_remove_queue(queueId_list[ii])
            attr_value = sai_thrift_attribute_value_t(oid=0)
            attr = sai_thrift_attribute_t(id=SAI_SCHEDULER_GROUP_ATTR_SCHEDULER_PROFILE_ID, value=attr_value)
            self.client.sai_thrift_set_scheduler_group_attribute(sched_group_id[2], attr)
            for ii in range(6):
                self.client.sai_thrift_remove_scheduler_group(sched_group_id[ii])
            self.client.sai_thrift_remove_scheduler_profile(sched_oid_1) 
         

def _sai_thrift_qos_create_buffer_profile(client, 
                                          th_mode, 
                                          static_th = 0, 
                                          dynamic_th = 0, 
                                          xon_th = 0, 
                                          xoff_th = 0):
    attr_list = []

    attr_value = sai_thrift_attribute_value_t(s32=th_mode)
    attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE, value=attr_value)
    attr_list.append(attr)

    if static_th:
        attr_value = sai_thrift_attribute_value_t(u32=static_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH, value=attr_value)
        attr_list.append(attr)

    if dynamic_th:
        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        attr_list.append(attr)        

    if xon_th:
        attr_value = sai_thrift_attribute_value_t(u32=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        attr_list.append(attr) 

    if xoff_th:
        attr_value = sai_thrift_attribute_value_t(u32=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        attr_list.append(attr)

    return client.sai_thrift_create_buffer_profile(attr_list)

@group('Buffer')
class PortGetIngressPGListTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Get Port Ingress Priority Group List Test
        step1:Get Port Attrs
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[1]
        pg_list = []

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:           
            if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                print "Ingress PG Num:",a.value.u32
                assert(0 != a.value.u32)
            if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                for i in range(a.value.objlist.count):
                    pg_list.append(a.value.objlist.object_id_list[i])
                    assert(0 != pg_list[i])
                    print "Ingress PG List[%d]:0x%x"%(i, a.value.objlist.object_id_list[i])
        try:
            pass
        finally:
            pass

@group('Buffer')
class PortEnableFlowCtlTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Port Enable Flow Contorl Test
        step1:Get Port Attrs
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[1]

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:
            if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL:
                print "default flowctl:", a.value.u8
                flowctl = a.value.u8

        flowctl = -1
        attr_value = sai_thrift_attribute_value_t(u8=flowctl)
        attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL, value=attr_value)
        self.client.sai_thrift_set_port_attribute(port, attr)
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_port_attribute(port)
            for a in attrs.attr_list:
                if a.id == SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL:
                    print "default flowctl:", a.value.u8
                    if flowctl != a.value.u8:
                        raise NotImplementedError()
        finally:
            attr_value = sai_thrift_attribute_value_t(u8=0)
            attr = sai_thrift_attribute_t(id=SAI_PORT_ATTR_PRIORITY_FLOW_CONTROL, value=attr_value)
            self.client.sai_thrift_set_port_attribute(port, attr)

@group('Buffer')
class BufferProfileCreateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Create Buffer Profile Id Test
        step1:Create Buffer Profile Id
        step2:verify 
        step3:clean up
        """
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 2000000
        dynamic_th = 0
        xon_th = 1000000
        xoff_th = 1200000

        buf_prof_id = _sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        assert(0 != buf_prof_id)
        print "Create Buffer Profile id:0x%X"%buf_prof_id
        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_id)
            for a in attrs.attr_list:
                if a.id == SAI_BUFFER_PROFILE_ATTR_THRESHOLD_MODE:
                    if a.value.s32 != th_mode:
                        raise NotImplementedError() 
                if a.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                    if a.value.s8 != dynamic_th:
                        raise NotImplementedError()
                if a.id == SAI_BUFFER_PROFILE_ATTR_SHARED_STATIC_TH:
                    if a.value.u32 != static_th:
                        raise NotImplementedError()
                if a.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                    if a.value.u32 != xoff_th:
                        raise NotImplementedError()
                if a.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                    if a.value.u32 != xon_th:
                        raise NotImplementedError()
        finally:
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class PortSetIngressPGBindBufferProfileTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Get Port Ingress Priority Group List Test
        step1:Get Port Attrs
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[1]
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 2000000
        dynamic_th = 0
        xon_th = 1000000
        xoff_th = 1200000
        pg_list = []

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:           
            if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                pg_num = a.value.u32
                print "Ingress PG Num:",a.value.u32
            if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                for i in range(a.value.objlist.count):
                    pg_list.append(a.value.objlist.object_id_list[i])
                    assert(0 != pg_list[i])
                    print "Ingress PG List[%d]:0x%x"%(i, a.value.objlist.object_id_list[i])

        buf_prof_id = _sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        assert(0 != buf_prof_id)
        print "Create Buffer Profile id:0x%X"%buf_prof_id

        for i in range(pg_num):
            attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
            attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
            self.client.sai_thrift_set_priority_group_attribute(pg_list[i], attr)

        warmboot(self.client)
        try:
            for i in range(pg_num):
                print "Get PG:0x%x    >>>"%pg_list[i]
                attrs = self.client.sai_thrift_get_priority_group_attribute(pg_list[i])
                for a in attrs.attr_list:
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE:
                        print "<<< Buffer Oid:0x%x"%a.value.oid
                        if a.value.oid != buf_prof_id:
                            raise NotImplementedError()
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_PORT:
                        print "<<< Port Oid:0x%x"%a.value.oid
                        if a.value.oid != port:
                            raise NotImplementedError()    
                    if a.id == SAI_INGRESS_PRIORITY_GROUP_ATTR_INDEX:
                        print "<<< Index:",a.value.u8
                        if a.value.u8 != i:
                            raise NotImplementedError() 
        finally:
            for i in range(pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                self.client.sai_thrift_set_priority_group_attribute(pg_list[i], attr)
                self.client.sai_thrift_remove_priority_group(pg_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class PortSetIngressPGBindBufferProfUpdateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Get Port Ingress Priority Group List Test
        step1:Get Port Attrs & Create Buffer Profile
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[1]
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 2000000
        dynamic_th = 0
        xon_th = 1000000
        xoff_th = 1200000
        pg_list = []

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:           
            if a.id == SAI_PORT_ATTR_NUMBER_OF_INGRESS_PRIORITY_GROUPS:
                pg_num = a.value.u32
                print "Ingress PG Num:",a.value.u32
            if a.id == SAI_PORT_ATTR_INGRESS_PRIORITY_GROUP_LIST:
                for i in range(a.value.objlist.count):
                    pg_list.append(a.value.objlist.object_id_list[i])
                    assert(0 != pg_list[i])
                    print "Ingress PG List[%d]:0x%x"%(i, a.value.objlist.object_id_list[i])

        buf_prof_id = _sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        assert(0 != buf_prof_id)
        print "Create Buffer Profile id:0x%X"%buf_prof_id

        for i in range(pg_num):
            attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
            attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
            self.client.sai_thrift_set_priority_group_attribute(pg_list[i], attr)

        xoff_th = 2000000
        xon_th  = 1500000
        attr_value = sai_thrift_attribute_value_t(u32=xoff_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XOFF_TH, value=attr_value)
        self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_id, attr)

        attr_value = sai_thrift_attribute_value_t(u32=xon_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_XON_TH, value=attr_value)
        self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_id, attr)

        warmboot(self.client)
        try:
            attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_id)
            for a in attrs.attr_list:  
                if a.id == SAI_BUFFER_PROFILE_ATTR_XOFF_TH:
                    print "Get xoff_th:", a.value.u32
                    if a.value.u32 != xoff_th:
                        raise NotImplementedError()
                if a.id == SAI_BUFFER_PROFILE_ATTR_XON_TH:
                    print "Get xon_th:", a.value.u32
                    if a.value.u32 != xon_th:
                        raise NotImplementedError()
        finally:
            for i in range(pg_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_INGRESS_PRIORITY_GROUP_ATTR_BUFFER_PROFILE, value=attr_value)
                self.client.sai_thrift_set_priority_group_attribute(pg_list[i], attr)
                self.client.sai_thrift_remove_priority_group(pg_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class QueueBindBufferProfileStaticModeTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Get Port Ingress Priority Group List Test
        step1:Get Port Attrs
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[1]
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_STATIC
        static_th = 2000000
        dynamic_th = 0
        xon_th = 1000000
        xoff_th = 1200000
        queueId_list = []

        buf_prof_id = _sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        assert(0 != buf_prof_id)
        print "Create Buffer Profile id:0x%X"%buf_prof_id

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])
                    attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)

        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        print "Get queue[0x%x] Buffer Profile oid: 0x%x"%(queueId_list[ii], a.value.oid)
                        if a.value.oid != buf_prof_id:
                            raise NotImplementedError() 
        finally:
            for i in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                self.client.sai_thrift_remove_queue(queueId_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class QueueBindBufferProfileDynamicModeTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Get Port Ingress Priority Group List Test
        step1:Get Port Attrs
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[1]
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = -2
        xon_th = 1000000
        xoff_th = 1200000
        queueId_list = []

        buf_prof_id = _sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        assert(0 != buf_prof_id)
        print "Create Buffer Profile id:0x%X"%buf_prof_id

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])
                    attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)

        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        print "Get queue[0x%x] Buffer Profile oid: 0x%x"%(queueId_list[ii], a.value.oid)
                        if a.value.oid != buf_prof_id:
                            raise NotImplementedError() 
        finally:
            for i in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                self.client.sai_thrift_remove_queue(queueId_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)

@group('Buffer')
class QueueBindBufferProfileUpdateTest(sai_base_test.ThriftInterfaceDataPlane):
    def runTest(self):
        """
        Get Port Ingress Priority Group List Test
        step1:Get Port Attrs
        step2:verify 
        step3:clean up
        """
        print "start test"
        switch_init(self.client)
        port = port_list[1]
        th_mode = SAI_BUFFER_PROFILE_THRESHOLD_MODE_DYNAMIC
        static_th = 0
        dynamic_th = -2
        xon_th = 1000000
        xoff_th = 1200000
        queueId_list = []

        buf_prof_id = _sai_thrift_qos_create_buffer_profile(self.client, th_mode, static_th, dynamic_th, xon_th, xoff_th)
        assert(0 != buf_prof_id)
        print "Create Buffer Profile id:0x%X"%buf_prof_id

        attrs = self.client.sai_thrift_get_port_attribute(port)
        for a in attrs.attr_list:  
            if a.id == SAI_PORT_ATTR_QOS_NUMBER_OF_QUEUES:
                print "queue number:%d"%a.value.u32
                queue_num = a.value.u32
            if a.id == SAI_PORT_ATTR_QOS_QUEUE_LIST:
                for i in range(a.value.objlist.count):
                    queueId_list.append(a.value.objlist.object_id_list[i])
                    print "queue_oid[%d]:0x%X"%(i, a.value.objlist.object_id_list[i])
                    attr_value = sai_thrift_attribute_value_t(oid=buf_prof_id)
                    attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                    self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)

        dynamic_th = 1
        attr_value = sai_thrift_attribute_value_t(s8=dynamic_th)
        attr = sai_thrift_attribute_t(id=SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH, value=attr_value)
        self.client.sai_thrift_set_buffer_profile_attribute(buf_prof_id, attr)

        warmboot(self.client)
        try:
            for ii in range(queue_num):
                attrs = self.client.sai_thrift_get_queue_attribute(queueId_list[ii])
                for a in attrs.attr_list:  
                    if a.id == SAI_QUEUE_ATTR_BUFFER_PROFILE_ID:
                        print "Get queue[0x%x] Buffer Profile oid: 0x%x"%(queueId_list[ii], a.value.oid)
                        if a.value.oid != buf_prof_id:
                            raise NotImplementedError() 
            attrs = self.client.sai_thrift_get_buffer_profile_attribute(buf_prof_id)
            for a in attrs.attr_list:  
                if a.id == SAI_BUFFER_PROFILE_ATTR_SHARED_DYNAMIC_TH:
                    print "Get dynamic_th:", a.value.s8
                    if a.value.s8 != dynamic_th:
                        raise NotImplementedError() 
        finally:
            for i in range(queue_num):
                attr_value = sai_thrift_attribute_value_t(oid=0)
                attr = sai_thrift_attribute_t(id=SAI_QUEUE_ATTR_BUFFER_PROFILE_ID, value=attr_value)
                self.client.sai_thrift_set_queue_attribute(queueId_list[i], attr)
                self.client.sai_thrift_remove_queue(queueId_list[i])
            self.client.sai_thrift_remove_buffer_profile(buf_prof_id)